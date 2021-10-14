import re
import multiprocessing
import threading
import queue
import eventlet
import openpyxl
import io
import sys
import re
import copy
from multiprocessing import Process, Pool
from openpyxl import workbook
from openpyxl import load_workbook
from re import sub
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os

class Part:
    # part_num(BBa.), part_name(CAP), part_id(内部代码), part_type(com/pro...),star（包含队伍使用和独特的标记)
    def __init__(self, part_num, part_name, part_id, part_url,
                 short_desc, part_type, team, year, sequence, contents,
                 stars, assemble_std, linking_parts, parts_used, using_parts, len, released, sample, twin):
        self.part_num = part_num
        self.part_name = part_name
        self.part_id = part_id
        self.part_url = part_url
        self.short_desc = short_desc
        self.year = year
        self.sequence = sequence
        # stars 需要再细化
        self.stars = stars
        self.assemble_std = assemble_std
        self.contents = contents
        self.linking_parts = linking_parts
        # how to get
        self.parts_used = parts_used
        self.using_parts = using_parts
        self.len = len
        self.part_type = part_type
        self.team = team
        self.released = released
        self.sample = sample
        self.twin = twin

    def print_parts(self):
        print(f"part_num = {self.part_num}")
        print(f"part_name = {self.part_name}")

        print(f"part_id = {self.part_id}")
        print(f"part_url = {self.part_url}")
        print(f"part_type = {self.part_type}")
        print(f"part_team = {self.team}")
        print(f"part_year = {self.year}")
        print(f"part_sequence = {self.sequence}")
        print(f"part_stars = {self.stars}")
        print(f"part_desc = {self.short_desc}")
        print(f"part_assemble_std = {self.assemble_std}")
        print(f"contents"f" = {self.contents}")
        print(f"parts_used = {self.parts_used}")
        print(f"using_parts = {self.using_parts}")
        print(f"len = {self.len}")
        print("------------------------------")


class myThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print("开启线程：" + self.name)
        process_data(self.q)
        print("退出线程：" + self.name)


def process_data(q):
    while not exitFlag:
        # queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            # queueLock.release()
            if curStep == 1:
                get_parts_urls_one(data)
            else:
                get_parts_details_one(data)
        # else:
        # queueLock.release()
        time.sleep(1)




def web_analysis_and_get_team_lists(year):
    # year 可变
    # 此处的地址可能需要更改
    # desktop地址： ‘D:\chromedriver.exe’
    # laptop地址：'C:\Python x64\Python\chromedriver.exe'
    print(f"---Start getting team lists in {year}---")
    driver = webdriver.Chrome('D:\chromedriver.exe')
    front_url = "https://igem.org/Team_Parts?year="
    url = front_url + year

    # 此处未检查！
    i = 0
    while 1:
        try:
            driver.get(url)
            WebDriverWait(driver, 30, 1).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="topBanner"]/a/img')), message='')
            break
        except:
            i = i + 1
            if i > 10:
                try:
                    driver.close()
                except:
                    pass
                return
            print("刷新")
            j = 0
            while 1:
                try:
                    driver.refresh()
                    break
                except:
                    j = j + 1
                    if j > 5:
                        try:
                            driver.close()
                        except:
                            pass
                        return
                    pass
            pass
    time.sleep(1)

    one_team_with_url = []
    the_list = driver.find_elements_by_xpath('/html/body/div/div[3]/div/div/div/div[4]/table/tbody/tr/td/div/a')
    for item in the_list:
        one_team_with_url = [year, str(item.text), str(item.get_attribute('href'))]
        all_team_with_urls.append(one_team_with_url)

    print(f"---Ending getting team lists in {year}---")
    while 1:
        try:
            driver.close()
            break
        except:
            pass
    return all_team_with_urls


# 未完成
def get_status(driver, a_part):
    try:
        item = driver.find_elements_by_xpath('//*[@id="part_status_wrapper"]/div[1]/a')
        a_part.released = str(item[0].text)
    except:
        a_part.released = ""
    try:
        item = driver.find_elements_by_xpath('//*[@id="part_status_wrapper"]/div[2]/a')
        a_part.sample = str(item[0].text)
    except:
        a_part.sample = ""
    try:
        item = driver.find_elements_by_xpath('//*[@id="part_status_wrapper"]/div[3]')
        a_part.stars.append = str(item[0].text)
    except:
        pass
    try:
        item = driver.find_elements_by_xpath('//*[@id="mw-content-text"]/p')
        a_part.part_name = str(item[0].text)
        for eachitem in item:
            a_part.contents.append(str(eachitem.text))
    except:
        pass
    return


def get_twin_parts(driver, a_part):
    try:
        item = driver.find_elements_by_xpath('//*[@id="part_status_wrapper"]/div[5]/a')
        url = str(item[0].get_attribute('href'))
    except:
        a_part.parts_twin = 'None'
        pass
    try:
        driver.get(url)
        WebDriverWait(driver, 10, 1).until(
            EC.presence_of_element_located((By.XPATH, '/html/body')),
            message='')
    except:
        pass
    time.sleep(1)

    twin_parts = []
    list = driver.find_elements_by_class_name('noul_link.part_link')
    for item in list:
        twin_parts.append(str(item.text))
    if len(twin_parts) == 0:
        twin_parts.append('None')
    a_part.twin = twin_parts
    while 1:
        try:
            driver.back()
            break
        except:
            pass

    return


# 输入某一年所有队伍的url，输出这一年所有part的基础信息(全局变量中)
def get_parts_urls(all_team_with_urls):
    print("---Start getting parts urls and basic info--- ")
    # for a_team in all_team_with_urls:

    return


def get_parts_urls_one(a_team):
    global all_process
    global process_count
    year = a_team[0]
    team = a_team[1]
    url = a_team[2]
    # desktop地址： ‘D:\chromedriver.exe’
    # laptop地址：'C:\Python x64\Python\chromedriver.exe'
    i = 0
    while 1:
        try:
            driver = webdriver.Chrome('D:\chromedriver.exe')
            break
        except:
            i = i + 1
            if i > 10: return
            pass
    while 1:
        # try:
        i = 0
        while 1:
            try:
                driver.get(url)
                WebDriverWait(driver, 10, 1).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="new_menubar"]/ul/li[1]/div[1]')), message='')
                break
            except:
                i = i + 1
                if i > 10:
                    try:
                        driver.close()
                    except:
                        pass
                    return
                print("刷新")
                j = 0
                while 1:
                    try:
                        driver.refresh()
                        break
                    except:
                        j = j + 1
                        if j > 5:
                            try:
                                driver.close()
                            except:
                                pass
                            return
                        pass
                pass
        time.sleep(1)

        # 先将基础属性放在列表里
        part_num_list = []
        part_numurl_list = []
        part_type_list = []
        part_desc = []
        part_designer = []
        part_len = []

        try:
            # 得到第一张表的数据（favored）
            items = driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[1]/tbody/tr/td[3]/a')
            for item in items:
                part_num_list.append(str(item.text))
                part_numurl_list.append(item.get_attribute('href'))
            items = driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[1]/tbody/tr/td[4]')
            for item in items:
                part_type_list.append(str(item.text))
            items = driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[1]/tbody/tr/td[5]')
            for item in items:
                part_desc.append(str(item.text))
            items = driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[1]/tbody/tr/td[6]')
            for item in items:
                part_designer.append(str(item.text))
            items = driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[1]/tbody/tr/td[7]')
            for item in items:
                part_len.append(str(item.text))
        except:
            pass
        # 为第第一张表（favored）创建类
        # star第一个1代表favor
        for i in range(0, len(part_num_list)):
            new_part = Part(part_num_list[i], '', '', part_numurl_list[i], part_desc[i], part_type_list[i], team, year,
                            '', [], '1', '', [], [], [], part_len[i], '', '', [])
            whole_Parts.append(new_part)
            all_process = all_process + 1

        time1 = time.time()

        part_num_list = []
        part_numurl_list = []
        part_type_list = []
        part_desc = []
        part_designer = []
        part_len = []
        # 得到第二张表的数据（NOT favored）
        try:
            items = driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[2]/tbody/tr/td[3]/a')
            for item in items:
                part_num_list.append(str(item.text))
                part_numurl_list.append(item.get_attribute('href'))
                # part_numurl_list.append('http://parts.igem.org/wiki/index.php?title=Part:BBa_J23100')
            time2 = time.time()
            if time2 - time1 > 5:
                try:
                    driver.refresh()
                except:
                    pass
            time1 = time.time()
            items = driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[2]/tbody/tr/td[4]')
            for item in items:
                part_type_list.append(str(item.text))
            time2 = time.time()
            if time2 - time1 > 5:
                try:
                    driver.refresh()
                except:
                    pass
            time1 = time.time()
            items = driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[2]/tbody/tr/td[5]')
            for item in items:
                part_desc.append(str(item.text))
            time2 = time.time()
            if time2 - time1 > 5:
                try:
                    driver.refresh()
                except:
                    pass
            time1 = time.time()
            items = driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[2]/tbody/tr/td[6]')
            for item in items:
                part_designer.append(str(item.text))
            time2 = time.time()
            if time2 - time1 > 5:
                try:
                    driver.refresh()
                except:
                    pass
            items = driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[2]/tbody/tr/td[7]')
            for item in items:
                part_len.append(str(item.text))
            # 为第一张表（favored）创建类
            # star第一个1代表favor
        except:
            pass
        for i in range(0, len(part_num_list)):
            new_part = Part(part_num_list[i], '', '', part_numurl_list[i], part_desc[i], part_type_list[i], team, year,
                            '', [], '0', '', [], [], [], part_len[i], '', '', [])
            whole_Parts.append(new_part)
            all_process = all_process + 1


        while 1:
            try:
                driver.close()
                break
            except:
                pass
        return
    # except:
    # print('timeout')
    # pass


# 未完成，从全局PART中，开始进行操作
def get_parts_details():
    # for a_part in whole_Parts:
    return


def get_parts_details_one(a_part):
    global all_process
    global process_count
    url = a_part.part_url
    while 1:
        # try:
        # with eventlet.Timeout(45, True):
        i = 0
        while 1:
            try:
                driver = webdriver.Chrome('D:\chromedriver.exe')
                break
            except:
                i = i + 1
                if i > 10: return
                pass

        i = 0
        gotten = False
        while 1:
            try:
                driver.get(url)
                WebDriverWait(driver, 2, 1).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="new_menubar"]/ul/li[1]/div[1]')), message='')
                gotten = True
                break
            except:
                i = i + 1
                if i > 10:
                    break
                print("刷新")
                while 1:
                    try:
                        driver.refresh()
                        break
                    except:
                        pass
                pass
        time.sleep(1)
        # 以上打开了part的主网页界面

        if not gotten:
            return

        # -------------------------------------------
        get_status(driver, a_part)
        get_using_parts_and_other_info(driver, a_part)
        get_assemble_std(driver, a_part)
        get_used_parts(driver, a_part)
        get_twin_parts(driver, a_part)
        # GET_SEQUENCE 自带关闭整个窗口的作用，所以所有数据获取请在这句之前玩完成
        get_sequence(driver, a_part)
        print(f'{process_count}/{all_process} is done')
        process_count = process_count + 1
        # -------------------------------------------

        break
    # except:
    # print('timeout')
    # pass

    return


# 已完成,used代表使用了该part的part，需要额外打开页面
def get_used_parts(driver, a_part):
    try:
        item = driver.find_elements_by_xpath('//*[@id="part_status_wrapper"]/div[4]/a')
        if len(item) == 0:
            a_part.parts_used = 'None'
            return
        url = str(item[0].get_attribute('href'))
    except:
        a_part.parts_used = 'None'
        return

    k = 0
    while 1:
        try:
            driver.get(url)
            WebDriverWait(driver, 10, 1).until(
                EC.presence_of_element_located((By.XPATH, '/html/body')),
                message='')
            break
        except:
            print("刷新")
            if k > 5: break
            while 1:
                try:
                    driver.refresh()
                    break
                except:
                    k = k + 1
                    pass
            pass
    time.sleep(2)

    used_parts = []
    list = driver.find_elements_by_class_name('noul_link.part_link')
    for item in list:
        used_parts.append(str(item.text))
    if len(used_parts) == 0:
        used_parts.append('None')
    a_part.parts_used = used_parts
    while 1:
        try:
            driver.back()
            break
        except:
            pass

    return


# 已完成
def get_assemble_std(driver, a_part):
    assemble_lists = []
    for item in driver.find_elements_by_xpath('//*[@id="assembly_compatibility"]/div/ul/li'):
        if str(item.get_attribute("class")) == "boxctrl box_green":
            assemble_lists.append('1')
        else:
            assemble_lists.append('0')
    # assemble_lists.append(str(item.get_attribute("class")))
    a_part.assemble_std = assemble_lists
    return


# 这一部分写part主页面内的所有内容。using代表该part的组成part,不需要额外打开页面加载；
# 已完成，不关闭窗口
def get_using_parts_and_other_info(driver, a_part):
    if a_part.part_type != 'Composite':
        a_part.using_parts = ['self']
    else:
        using_parts_list = []
        for item in driver.find_elements_by_xpath('//*[@id="seq_features_div"]/div[1]/div[4]/div/div[2]'):
            using_parts_list.append(str(item.text))
        # 以下确认了编号的统一
        for i in range(0, len(using_parts_list)):
            if 'BBa' in using_parts_list[i]:
                continue
            else:
                using_parts_list[i] = 'BBa_' + using_parts_list[i]

        a_part.using_parts = using_parts_list
    return


# 自带关闭，已完成
def get_sequence(driver, a_part):
    while 1:
        try:
            WebDriverWait(driver, 10, 1).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="new_menubar"]/ul/li[1]/div[1]')),
                message='')
            try:
                sequence_entrance = driver.find_elements_by_xpath('//*[@id="seq_features_div"]/div[1]/div[1]/span[5]')
                # webdriver.ActionChains(driver).move_to_element(sequence_entrance[0]).click(sequence_entrance[0]).perform().find_elements_by_xpath("/html/body/pre/text()")
                webdriver.ActionChains(driver).move_to_element(sequence_entrance[0]).click(
                    sequence_entrance[0]).perform()
                break
            except:
                print(f"{a_part.part_num} 没有序列或序列获取失败")
                driver.close()
                return
        except:
            i = 0
            while 1:
                try:
                    driver.refresh()
                    break
                except:
                    i = i + 1
                    if i > 10:
                        try:
                            driver.close()
                        except:
                            pass
                        return
                    pass
            pass

    time.sleep(2)
    # 切换窗口到新跳出的窗口
    handles = driver.window_handles
    index_handle = driver.current_window_handle  # 备注：可能需要在操作前，先关闭其他浏览器窗口
    for handle in handles:
        if handle != index_handle:
            driver.switch_to.window(handle)
    sequence = driver.find_elements_by_xpath("/html/body/pre")  # 备注：所有xpath出来都是list，记得切换为元素
    if len(sequence) > 0:
        a_part.sequence = str(sequence[0].text)
    while 1:
        try:
            driver.close()
            break
        except:
            pass
    handle = driver.window_handles[0]
    driver.switch_to.window(handle)
    while 1:
        try:
            driver.close()
            break
        except:
            pass
    return


# 下一个需要完成的，一年一存
def store_parts():
    wb = workbook.Workbook()
    ws1 = wb.active
    ws1.append(['part_num', 'part_name', 'part_id', 'part_url',
                'short_desc', 'part_type', 'team', 'year', 'sequence', 'contents', 'released', 'sample',
                'stars', 'twins', 'assemble_std', 'parts_used', 'using_parts', 'len'])
    for a_part in whole_Parts:
        ws1.append([a_part.part_num, a_part.part_name, a_part.part_id, a_part.part_url, a_part.short_desc, \
                    a_part.part_type, a_part.team, a_part.year, a_part.sequence, ' '.join(a_part.contents),
                    a_part.released, a_part.sample, a_part.stars, ' '.join(a_part.twin), \
                    ' '.join(a_part.assemble_std),
                    ' '.join(a_part.parts_used), ' '.join(a_part.using_parts), a_part.len])
    wb.save(f'D:\\{year}collection.xlsx')
    return


def set_database():
    global finished
    global process_count
    global all_process
    process_count = 0
    all_process = 0
    # year = '2004'
    # for year in range(2020):
    # all_team_with_urls = web_analysis_and_get_team_lists(str(year))
    # anothoer test_example:  ['2020','teamB',' http://parts.igem.org/cgi/partsdb/pgroup.cgi?pgroup=iGEM2020&group=Fudan']
    '''
    all_team_with_urls = [['2019', 'teamA', 'http://parts.igem.org/cgi/partsdb/pgroup.cgi?pgroup=iGEM2020&group=GDSYZX']]
    get_parts_urls(all_team_with_urls)  # 所有信息存在全局变量 whole_Parts 中
    get_parts_details()  # 所有信息存在全局变量 whole_Parts 中，并且一个一存/一年一存
    return 0
    '''

    queueLock = threading.Lock()
    workQueue = queue.Queue(10000)
    threadList = ["Thread1", "Thread2", "Thread3", "Thread4", "Thread5", "Thread6", "Thread7", "Thread8", "Thread9",
                  "Thread10", "Thread11", "Thread12", "Thread13", "Thread14", "Thread15", "Thread16"]
    # threadList = ["Thread1", "Thread2", "Thread3", "Thread4", "Thread5", "Thread6"]
    # threadList = ["Thread1"]

    years = [2012]
    # years = [2004, 2005, 2006]
    for year in years:
        exitFlag = 0
        all_team_with_urls = web_analysis_and_get_team_lists(str(year))
        # get_parts_urls(all_team_with_urls) #所有信息存在全局变量 whole_Parts 中

        curStep = 1  # 当前为step1，获取基本信息
        threads = []
        threadID = 1

        # 创建新线程
        for tName in threadList:
            thread = myThread(threadID, tName, workQueue)
            thread.start()
            threads.append(thread)
            threadID += 1

        # 填充队列
        # queueLock.acquire()
        for word in all_team_with_urls:
            workQueue.put(word)
        # workQueue.put(all_team_with_urls[100])
        # queueLock.release()

        # 等待队列清空
        while not workQueue.empty():
            pass

        # 通知线程是时候退出
        exitFlag = 1

        # 等待所有线程完成
        for t in threads:
            t.join()

        curStep = 2  # 当前为step2，获取detail
        exitFlag = 0
        # 所有信息存在全局变量 whole_Parts 中，并且一年一存
        threads = []
        threadID = 1
        finished = 0

        # queueLock.acquire()
        for word in whole_Parts:
            workQueue.put(word)
        # queueLock.release()

        # 创建新线程
        for tName in threadList:
            thread = myThread(threadID, tName, workQueue)
            thread.start()
            threads.append(thread)
            threadID += 1

        # 填充队列

        # 等待队列清空
        while not workQueue.empty():
            pass

        # 通知线程是时候退出
        exitFlag = 1

        # 等待所有线程完成
        for t in threads:
            t.join()

        store_parts()
        print(f"---Details of parts in {year} are saved---")

        whole_Parts = []
        all_team_with_urls = []