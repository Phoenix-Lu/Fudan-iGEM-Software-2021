import requests
from bs4 import BeautifulSoup
import time
import re
from openpyxl import workbook
from openpyxl import load_workbook
#from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

#全篇的sleep函数可以优化
#打不开的情况需要try函数优化


class Part:
    # part_num(BBa.), part_name(CAP), part_id(内部代码), part_type(com/pro...),star（包含队伍使用和独特的标记)
    def __init__(self, part_num, part_name, part_id, part_url,
                 short_desc, part_type, team, year, sequence, contents,
                 stars, assemble_std, linking_parts, parts_used, using_parts, len):
        self.part_num = part_num
        self.part_name = part_name
        self.part_id = part_id
        self.part_url = part_url
        self.short_desc = short_desc
        self.year = year
        self.sequence = sequence
        #stars 需要再细化
        self.stars = stars
        self.assemble_std = assemble_std
        self.contents = contents
        # self.linking_parts = linking_parts
        # how to get
        self.parts_used = parts_used
        self.using_parts = using_parts
        self.len = len
        self.part_type = part_type
        self.team = team

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
        print(f"part_used = {self.parts_used}")
        print(f"using_parts = {self.using_parts}")
        print(f"len = {self.len}")
        print("------------------------------")




all_team_with_urls = []
all_parts = []
whole_Parts = []

def inter():
    # 需要标注输入格式,届时可以通过前端重写
    print("Which year would you want to scan for? Input 'years'")

    return 0


def web_analysis_and_get_team_lists(year):
    # year 可变
    # 此处的地址可能需要更改

    #desktop地址： ‘D:\chromedriver.exe’
    #laptop地址：'C:\Python x64\Python\chromedriver.exe'
    driver = webdriver.Chrome('D:\chromedriver.exe')
    front_url = "https://igem.org/Team_Parts?year="
    url = front_url + year
    driver.get(url)
    time.sleep(5)
    # 时间可能需要更长
    one_team_with_url = []
    the_list = driver.find_elements_by_xpath('/html/body/div/div[3]/div/div/div/div[4]/table/tbody/tr/td/div/a')
    for item in the_list:
        one_team_with_url = [year, str(item.text), str(item.get_attribute('href'))]
        all_team_with_urls.append(one_team_with_url)

    for item in all_team_with_urls:
        print(item)

    print('-------all_team_with_urls get----------')
    driver.close()
    return all_team_with_urls


'''
    xpath:
/html/body/div/div[3]/div/div/div/div[4]/table[4]/tbody/\
 tr[1]/td[1]/div/a
a 内有我们需要的内容
tr为行，td为列，可以定位到具体的元素了

//*[@id="Table_1"]/tbody/tr[1]/td[3]q
'''


def set_star_database():
    return


def get_parts_urls(all_team_with_urls):
    for a_team in all_team_with_urls:
        year = a_team[0]
        team = a_team[1]
        url = a_team[2]
        # desktop地址： ‘D:\chromedriver.exe’
        # laptop地址：'C:\Python x64\Python\chromedriver.exe'
        driver = webdriver.Chrome('D:\chromedriver.exe')
        driver.get(url)
        time.sleep(5)
        #先将基础属性放在列表里
        part_num_list = []
        part_numurl_list = []
        part_type_list = []
        part_desc = []
        part_designer = []
        part_len = []
        #得到第一张表的数据（favored）
        for item in driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[1]/tbody/tr/td[3]/a'):
            part_num_list.append(str(item.text))
            part_numurl_list.append(item.get_attribute('href'))
        for item in driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[1]/tbody/tr/td[4]'):
            part_type_list.append(str(item.text))
        for item in driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[1]/tbody/tr/td[5]'):
            part_desc.append(str(item.text))
        for item in driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[1]/tbody/tr/td[6]'):
            part_designer.append(str(item.text))
        for item in driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[1]/tbody/tr/td[7]'):
            part_len.append(str(item.text))
        #为第第一张表（favored）创建类
            #star第一个1代表favor
        for i in range(0, len(part_num_list)):
            new_part = Part(part_num_list[i], '', '', part_numurl_list[i], part_desc[i], part_type_list[i], team, year, '', '', '1', '', [], [], [], part_len[i])
            whole_Parts.append(new_part)

        part_num_list = []
        part_numurl_list = []
        part_type_list = []
        part_desc = []
        part_designer = []
        part_len = []
        #得到第二张表的数据（NOT favored）
        for item in driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[2]/tbody/tr/td[3]/a'):
            part_num_list.append(str(item.text))
            part_numurl_list.append(item.get_attribute('href'))
        for item in driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[2]/tbody/tr/td[4]'):
            part_type_list.append(str(item.text))
        for item in driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[2]/tbody/tr/td[5]'):
            part_desc.append(str(item.text))
        for item in driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[2]/tbody/tr/td[6]'):
            part_designer.append(str(item.text))
        for item in driver.find_elements_by_xpath('/html/body/div/div[4]/div/div/table[2]/tbody/tr/td[7]'):
            part_len.append(str(item.text))
        # 为第第一张表（favored）创建类
            # star第一个1代表favor
        for i in range(0, len(part_num_list)):
             new_part = Part(part_num_list[i], '', '', part_numurl_list[i], part_desc[i], part_type_list[i], team, year, '', '', '0', '', [], [], [], part_len[i])
             whole_Parts.append(new_part)
        print("-----------get_parts_urls-----------")
        driver.close()
    return


# 从part主界面出发的 主函数
def get_parts_details():
    for a_part in whole_Parts:
        url = a_part.part_url
        driver = webdriver.Chrome('D:\chromedriver.exe')
        driver.get(url)
        time.sleep(5)
        #以上打开了part的主网页界面
        #-------------------------------------------
        get_using_parts_and_other_info(driver, a_part)
        get_assemble_std(driver, a_part)
        #get_used_parts(driver, a_part)
        get_assemble_std(driver, a_part)
        #GET_SEQUENCE 自带关闭整个窗口的作用，所以所有数据获取请在这句之前玩完成
        get_sequence(driver, a_part)
    return 0


#used代表使用了该part的part，需要额外打开页面
def get_used_parts():
    for a_part in whole_Parts:
        url = a_part.part_url
        driver = webdriver.Chrome('D:\chromedriver.exe')
        driver.get(url)
        time.sleep(5)
    return

#已完成
def get_assemble_std(driver, a_part):
    assemble_lists = []
    for item in driver.find_elements_by_xpath('//*[@id="assembly_compatibility"]/div/ul/li'):
         if str(item.get_attribute("class")) == "boxctrl box_green" :
             assemble_lists.append('1')
         else:
             assemble_lists.append('0')
        #assemble_lists.append(str(item.get_attribute("class")))


    a_part.assemble_std = assemble_lists
    return


#这一部分写part主页面内的所有内容。using代表该part的组成part,不需要额外打开页面加载；
#已完成，不关闭窗口
def get_using_parts_and_other_info(driver, a_part):
    if a_part.part_type != 'Composite':
        a_part.using_parts = ['self']
    else:
        using_parts_list = []
        for item in driver.find_elements_by_xpath('//*[@id="seq_features_div"]/div[1]/div[4]/div/div[2]'):
            using_parts_list.append(str(item.text))
        #以下确认了编号的统一
        for i in range(0, len(using_parts_list)):
            if 'BBa' in using_parts_list[i]:
                continue
            else:
                using_parts_list[i] = 'BBa_'+ using_parts_list[i]

        a_part.using_parts = using_parts_list
    return

#自带关闭，已完成
def get_sequence(driver, a_part):
    sequence_entrance = driver.find_elements_by_xpath('//*[@id="seq_features_div"]/div[1]/div[1]/span[5]')
    #webdriver.ActionChains(driver).move_to_element(sequence_entrance[0]).click(sequence_entrance[0]).perform().find_elements_by_xpath("/html/body/pre/text()")
    webdriver.ActionChains(driver).move_to_element(sequence_entrance[0]).click(sequence_entrance[0]).perform()
    time.sleep(1)
    #切换窗口到新跳出的窗口
    handles = driver.window_handles
    index_handle = driver.current_window_handle#备注：可能需要在操作前，先关闭其他浏览器窗口
    for handle in handles:
        if handle != index_handle:
            driver.switch_to.window(handle)
    sequence = driver.find_elements_by_xpath("/html/body/pre")#备注：所有xpath出来都是list，记得切换为元素
    a_part.sequence = str(sequence[0].text)
    driver.close()
    handle = driver.window_handles[0]
    driver.switch_to.window(handle)
    driver.close()
    return


def store_parts(team_parts_list):
    wb = workbook.Workbook()
    ws = wb.active
    ws.append(['year', 'team', 'parts', 'parts_urls', 'basic_parts'])
    for Team_parts in team_parts_list:
        print(Team_parts.part_name)
        print(Team_parts.part_url)
        print(len(Team_parts.part_name))
        for part_id in range(1, len(Team_parts.part_name)):
            ws.append([str(Team_parts.year), str(Team_parts.team_name), str(Team_parts.part_name[part_id]),
                       str(Team_parts.part_url[part_id])])
    wb.save('D:\\2019collection.xlsx')
    print('--------parts are stored-------')





def main():
    year = '2004'
    # for year in range(2020):
    #all_team_with_urls = web_analysis_and_get_team_lists(str(year))
    #anothoer test_example:  ['2020','teamB',' http://parts.igem.org/cgi/partsdb/pgroup.cgi?pgroup=iGEM2020&group=Fudan']
    all_team_with_urls = [['2020', 'teamA', 'http://parts.igem.org/cgi/partsdb/pgroup.cgi?pgroup=iGEM2020&group=GDSYZX']]
    get_parts_urls(all_team_with_urls)
    get_parts_details()
    for item in whole_Parts:
        item.print_parts()
    return 0


main()
