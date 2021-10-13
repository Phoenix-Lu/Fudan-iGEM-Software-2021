# noinspection PyUnresolvedReferences
import requests
# noinspection PyUnresolvedReferences
from bs4 import BeautifulSoup
import time
# noinspection PyUnresolvedReferences
import re
# noinspection PyUnresolvedReferences
import multiprocessing
import threading
import queue
# noinspection PyUnresolvedReferences
import eventlet
# noinspection PyUnresolvedReferences
import openpyxl
# noinspection PyUnresolvedReferences
import io
# noinspection PyUnresolvedReferences
import sys
# noinspection PyUnresolvedReferences
import re
# noinspection PyUnresolvedReferences
import copy
# eventlet.monkey_patch()
# noinspection PyUnresolvedReferences
from multiprocessing import Process, Pool
from openpyxl import workbook
from openpyxl import load_workbook

# from lxml import etree
# noinspection PyUnresolvedReferences
from re import sub
from selenium import webdriver
# noinspection PyUnresolvedReferences
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
# noinspection PyUnresolvedReferences
from Bio.Blast.Applications import NcbiblastnCommandline
# noinspection PyUnresolvedReferences
from Bio.Blast.Applications import NcbimakeblastdbCommandline
# noinspection PyUnresolvedReferences
import os
# noinspection PyUnresolvedReferences

#from fp_growth import find_frequent_itemsets
# noinspection PyUnresolvedReferences
from Bio.Blast import NCBIXML
all_team_with_urls = []
whole_Parts = []
global process_count
global all_process
#global fpgrowth_database

# 全篇的sleep函数可以优化
# 打不开的情况需要try函数优化
# 整体上，以年为记的part为全局变量




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
# def main():


def find_and_set_seqr(part_id):
    wb = load_workbook('D:\completed_collection\\2005collection.xlsx')
    ws = wb['Sheet']
    for cell in ws['A']:
        if cell.value == part_id:
            row = cell.row
            part_name = ws['B'+str(row)].value
            part_url = ws['D'+str(row)].value
            part_year = ws['H'+str(row)].value
            part_seq = ws['I'+str(row)].value
            if 'Part' in part_seq:
                part_seq = 'ATTATT'
            part_contents = ws['J'+str(row)].value
            part_status = ws['K'+str(row)].value
            part_stars = ws['M'+str(row)].value
            part_twins = ws['N'+str(row)].value
            part_assemble = ws['O'+str(row)].value
            part_usingparts = ws ['Q'+str(row)].value
            part_usedparts = ws['P'+str(row)].value
            part_len = ws['R'+str(row)].value
            part_type = ws['F'+str(row)].value
            part_team = ws['G'+str(row)].value
            part_release = ws['K'+ str(row)].value

            #注意如果sequence格子中的不是序列的报错行为

            target_seqr = SeqRecord(part_seq)
            target_seqr.id = part_id
            target_seqr.name = part_name
            target_seqr.description = part_contents
            target_seqr.annotations['url'] = part_url
            target_seqr.annotations['year'] = part_year
            target_seqr.annotations['status'] = part_status
            target_seqr.annotations['stars'] = part_stars
            target_seqr.annotations['twins'] = part_twins
            target_seqr.annotations['assemble'] = part_assemble
            target_seqr.annotations['using_parts'] = part_usingparts
            target_seqr.annotations['used_parts'] = part_usedparts
            target_seqr.annotations['len'] = part_len
            target_seqr.annotations['type'] = part_type
            target_seqr.annotations['team'] = part_team
            target_seqr.annotations['release'] = part_release
            return target_seqr

#目前只对05年有效，记得正式使用时做更改

def transform_fasta_database():
    wb = load_workbook('whole_collection_processed.xlsx')
    ws = wb['Sheet1']
    seqrlst = []
    replacer = []
    for cell in ws['A']:
        if cell.value != '' and cell.value != 'part_num':
                row = cell.row
                part_id = ws['A'+str(row)].value
                part_name = ws['B' + str(row)].value
                part_url = ws['D' + str(row)].value
                part_year = ws['H' + str(row)].value
                part_seq = ws['I' + str(row)].value

                if part_seq == 'NA':
                    part_seq = "attatt"
                    print(str(part_id) +'处理A')
                    print('now seq ='+ part_seq)
                if ('Part' in part_seq):
                    part_seq = "attatt"
                    print(str(part_id) +'处理B')
                    print('now seq ='+ part_seq)


                part_contents = ws['J' + str(row)].value
                try:
                    part_contents.encode(encoding='gbk')
                except:
                    replacer.append(part_contents)
                    part_contents = 'somethingwaitingtobereplaced0010'
                part_status = ws['K' + str(row)].value
                part_stars = ws['M' + str(row)].value
                part_twins = ws['N' + str(row)].value
                part_assemble = ws['O' + str(row)].value
                part_usingparts = ws['Q' + str(row)].value
                part_usedparts = ws['P' + str(row)].value
                part_len = ws['R' + str(row)].value
                part_type = ws['F' + str(row)].value
                part_team = ws['G' + str(row)].value
                part_release = ws['K' + str(row)].value

                # 注意如果sequence格子中的不是序列的报错行为
                #Imp
                target_seqr = SeqRecord(Seq(part_seq))
                target_seqr.id = part_id
                target_seqr.name = part_name
                #target_seqr.description = part_contents
                target_seqr.annotations['url'] = part_url
                target_seqr.annotations['year'] = part_year
                target_seqr.annotations['status'] = part_status
                target_seqr.annotations['stars'] = part_stars
                target_seqr.annotations['twins'] = part_twins
                target_seqr.annotations['assemble'] = part_assemble
                target_seqr.annotations['using_parts'] = part_usingparts
                target_seqr.annotations['used_parts'] = part_usedparts
                target_seqr.annotations['len'] = part_len
                target_seqr.annotations['type'] = part_type
                target_seqr.annotations['team'] = part_team
                target_seqr.annotations['release'] = part_release
                seqrlst.append(target_seqr)

    #print(seqrlst[0].seq)
    #print(len(seqrlst))
    #SeqIO.write(seqrlst[2], "D:\completed_collection\\test.faa", 'fasta')
    SeqIO.write(seqrlst, "whole_collection_fasta.fasta", "fasta")
    return 1
'''
    with open("whole_collection_fasta.fasta", "r+", encoding='gb18030') as file:
        prefasta = str(file.read())

    for i in range(len(replacer)):
        prefasta = prefasta.replace('somethingwaitingtobereplaced0010',replacer[i],1)

    with open("whole_collection_fasta.fasta", "r+", encoding='gb18030') as file:
        file.write(prefasta)
'''



#blast需要安装ncbi本地blast
def do_blast(working_seqr):
    #ncbiblast安装的路径很关键，决定cmd参数，各种路径都不要有空格
    cline = NcbimakeblastdbCommandline(cmd=r"C:\Program Files\NCBI\blast-2.12.0+\bin\makeblastdb" , dbtype="nucl",out="temp_db",title="test",input_file="whole_collection_fasta.fasta")
    #print(cline)
    cline()
    out_path = str(working_seqr.id) + "_blastresult.xml"
    blastn_cline = NcbiblastnCommandline(cmd=r"C:\Program Files\NCBI\\blast-2.12.0+\\bin\\blastn",query="whole_collection_fasta.fasta", db="temp_db", evalue=0.001, outfmt = 5, out = out_path)
    #print(blastn_cline)
    blastn_cline()
    result_handle = open(out_path, encoding='gb18030', errors= 'ignore')
    blast_records=NCBIXML.parse(result_handle)
    E_VALUE_THRESH = 0.00000000000000000000000000000001  # 给出所有大于等于某一特定阈值的BLAST命中结果的一些汇总信息，建议取零
    for blast_record in blast_records:
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                if hsp.expect <= E_VALUE_THRESH:
                    result_path = 'BlastHistoryResult\\' +str(working_seqr.id) + '_BlastAnalysis'
                    with open(result_path, "a+") as blastanalysis:
                        blastanalysis.write('****Alignment****\n')
                        blastanalysis.write('sequence:'+alignment.title+"\n")
                        blastanalysis.write('ilength:'+ str(alignment.length)+"\n")
                        blastanalysis.write('e value:'+ str(hsp.expect)+"\n")
                        blastanalysis.write(hsp.query[0:75] + '...'+"\n")
                        blastanalysis.write(hsp.match[0:75] + '...'+"\n")
                        blastanalysis.write(hsp.sbjct[0:75] + '...'+"\n")
    os.remove('temp_db.ndb')
    os.remove('temp_db.nhr')
    os.remove('temp_db.nin')
    os.remove('temp_db.not')
    os.remove('temp_db.nsq')
    os.remove('temp_db.ntf')
    os.remove('temp_db.nto')
    result_handle.close()
    os.remove(out_path)

    #print('end')


#这一步先直接对excel做处理,给出每个part引用的对象，再生成excel给出各part被引用的上级和被引用数

def get_cite_parts():
    global fpgrowth_database
    wb = load_workbook('whole_collection_processed.xlsx')
    ws = wb['Sheet1']
    dic = {}
    for i in range(ws.min_row+1, ws.max_row+1):
        cites = []
        print (i)
        content = ws['J'+str(i)].value
        ID = ws['A'+str(i)].value
        split_words = content.split(' ')
        for a_word in split_words:
            if  'BBa_' in a_word:
                a_word = ''.join(filter(str.isdigit, a_word))
                a_word = 'BBa_' + a_word
                cites.append(a_word)
                if a_word not in dic:
                    dic[a_word] = [ID]
                if a_word in dic and ID not in dic[a_word]:
                    dic[a_word].append(ID)
                continue
            if re.search( "[A-Z]\d{4}" , a_word ) and not re.search("[^a-zA-Z0-9]",a_word):
                #a_word = ''.join(filter(str.isdigit, a_word))
                a_word = 'BBa_' + a_word
                cites.append(a_word)
                if a_word not in dic:
                    dic[a_word] = [ID]
                if a_word in dic and ID not in dic[a_word]:
                    dic[a_word].append(ID)

        ws['S' + str(i)].value = ' '.join(cites)

    j = 0
    for cell in ws['A']:
        row = cell.row
        value = dic.get(cell.value, [])
        if len(value):
            ws['U' + str(row)].value = ' '.join(value)
            ws['V' + str(row)].value = len(value)
            j += 1
            print(j)




    wb.save('whole_collection_processed.xlsx')




    fpgrowth_database=[]
   # for i in dic:
        #fpgrowth_database.append(list(tuple(dic[i])))
    #print(fpgrowth_database)
    #print(dic)

    #with open( 'D:\completed_collection\\fp_db.txt',"w+") as db:
        #for i in dic:
            #db.write(i+" is cited by ["+",".join(dic[i])+"]\n")
    #生成所有part被引用情况的ex
    wb = workbook.Workbook()
    ws1 = wb.active
    ws1.append(['part_num', 'cited by',"cited times"])
    for i in dic:
        ws1.append([i, str(dic[i]),len(dic[i])])
    wb.save(f'fp_db.xlsx')
    return

#给到所有有共同引用的part组合和共同引用数，生成excel
def fp_get():
    wb = load_workbook('fp_db.xlsx')
    ws = wb['Sheet']
    fpgrowth_database = []
    for cell in ws['B']:
        if cell.row > 1:
            content = cell.value.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '')
            data = content.split(',')
            fpgrowth_database.append(data)
    fp_fin = []
    fp_result = list(find_frequent_itemsets(fpgrowth_database,1,include_support=True))
    for i in range(len(fp_result)):
        if len(fp_result[i][0]) == 2:
            fp_fin.append(fp_result[i])
    #print(fp_result)
    wb = workbook.Workbook()
    ws1 = wb.active
    ws1.append(['part_num1', 'part_num2', "shared citing times"])
    for i in fp_fin:
        ws1.append([i[0][0], i[0][1], i[1]])
    wb.save(f'fp_sharedciting_result.xlsx')
    #print(fp_fin)
    return

#找到和part ID有共同引用的parts并给出共同引用数
def get_relevant_parts(part_id):
    friends = []
    wb = load_workbook('fp_sharedciting_result.xlsx')
    ws = wb['Sheet']
    for cell in ws['A']:
        if cell.value == part_id:
            row = cell.row
            friend = ws['B' + str(row)].value
            relevance = ws['C' + str(row)].value
            friends.append([relevance,friend])
    for cell in ws['B']:
        if cell.value == part_id:
            row = cell.row
            friend = ws['A' + str(row)].value
            relevance = ws['C' + str(row)].value
            friends.append([relevance,friend])
            friends.append([relevance,friend])
            friends.sort(reverse=True)
    print(friends)



if __name__ == '__main__':
    #set_database()
    get_cite_parts()  #注意改completed_collection!加下划线连接
    #working_seqr = find_and_set_seqr('BBa_J07009')
    #transform_fasta_database()  # 改了一下，现在不用改包也不会有encoding error
    #do_blast(working_seqr)  #跑这个要谨慎，一跑一个多G就无了
    #set_database()
    #fp_get()  #跑这个前必须先跑过get_cite_parts获得数据库
    #get_relevant_parts('BBa_J13100')  #跑这个前必须先跑过fp_get获得数据库
    #return 0


