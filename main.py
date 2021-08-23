import requests
from bs4 import BeautifulSoup
import time
import re
from openpyxl import workbook
from openpyxl import load_workbook
from lxml import etree
from selenium import webdriver


class Part:
    # part_num(BBa.), part_name(CAP), part_id(内部代码), part_type(com/pro...),star（包含队伍使用和独特的标记)
    def __init__(self, part_num, part_name, part_id, part_url,
                 short_desc, part_type, team, year, sequence, contents,
                 stars, assemble_std, linking_parts, parts_used, using_parts):
        self.part_num = part_num
        self.part_name = part_name
        self.part_id = part_id
        self.part_url = part_url
        self.short_desc = short_desc
        self.part_type = part_type
        self.team = team
        self.year = year
        self.sequence = sequence
        self.stars = stars
        self.assemble_std = assemble_std
        self.contents = contents
        # self.linking_parts = linking_parts
        # how to get
        self.parts_used = parts_used
        self.using_parts = using_parts


all_team_with_urls = []
all_parts = []


def inter():
    # 需要标注输入格式,届时可以通过前端重写
    print("Which year would you want to scan for? Input 'years'")

    return 0


def web_analysis_and_get_team_lists(year):
    # year 可变
    # 此处的地址可能需要更改
    driver = webdriver.Chrome('C:\Python x64\Python\chromedriver.exe')
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
        driver = webdriver.Chrome('C:\Python x64\Python\chromedriver.exe')
        driver.get(url)
        time.sleep(5)
        the_list =

    return


# 可能需要拆分
def get_parts_details():
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


'''
def get_team_lists(year):
    front_url = "https://igem.org/Team_Parts?year="
    url = front_url + year
    print(f"--------Now it's searching for {year}, url:{url} --------")
    strhtlm = requests.get(url)
    soup = BeautifulSoup(strhtlm.text, 'lxml')
    urls = []
    for item in soup.find_all('a'):
        urls.append(item.get('href'))
'''
'''
        result={
            "title":item.get_text(),
            "link":item.get('href'),
            #'ID':re.findall('\d+',item.get('href'))
        }
        print(result)
'''
'''
    # table_Tea ms_from_Asia > tbody > tr: > td: > div > a
    # table_Teams_from_Asia > tbody > tr:nth-child(1) > td:nth-child(2) > div > a
    # table_Teams_from_Asia > tbody > tr:nth-child(1) > td:nth-child(1) > div > a
    del urls[0]
    del urls[0]
    print(f"lists_geted:{urls}\n{urls.count} team in all")
    print("--------get_lists_ended--------\n")
    return urls


def get_parts(urls, year):
    print(f"Now searching for parts in {year}")
    count = 1
    answer = []
    for url in urls:
        time.sleep(1)
        print(f"Wait for a while,NO.{count}\n")
        count = count + 1
        print("\n")
        team_name = url[67:]
        strhtlm = requests.get(url)
        soup = BeautifulSoup(strhtlm.text, 'lxml')
        parts_list = []
        parts_urls = []
        for item in soup.find_all('a'):
            parts_list.append(item.get_text())
            parts_urls.append(item.get('href'))
        for i in range(1, 5):
            if (parts_list == []):
                break
            else:
                del parts_list[0]
                del parts_urls[0]
        '''
'''
        while '' in parts_list:
            list.remove('')



            if (parts_list[0]==['']):
                break
            else:
                del parts_list[0]
                del parts_urls[0]
                '''
'''
        this_team = Team_parts(year, team_name, parts_list, parts_urls, [], [])
        answer.append(this_team)
    print("--------got all parts--------")
    return answer

'''

'''
def get_detailed_parts (team_parts_lists):
    for item in team_parts_lists:
        detailed_url = item.part_url
        for url in detailed_url:
            strhtlm = requests.get(url)
            website = etree.HTML(strhtlm.text)
            item.part_type = website.xpath('//*[@id="content"]/div[2]/div[1]/text()')
            print(item.part_type)
            if (item.part_type == ['coding']):
                item.basic_parts == [website.xpath('//*[@id="content"]/div[2]/div[2]/text()')]
            #if (item.part_type == )

        return (team_parts_lists)
        '''

"""MAIN"""

'''
def main():

    # 更改此处【2020】为想要查看年份即可，这里以2020为例：
    for year in [2019]:
        urls = get_team_lists(str(year))
        # urls = ['http://parts.igem.org/cgi/partsdb/pgroup.cgi?pgroup=iGEM2020&group=AFCM-Egypt']
        team_pars_list = get_parts(urls, str(year))
        # for item in team_pars_list:
        #    print(f"{item.year}, {item.team_name}, {item.part_name}, {item.part_url}")
        # print(f"all parts in {year} are printed")\
        # output = get_detailed_parts(team_pars_list)
        sotre_parts(team_pars_list)
    print("All_Exit")

'''


def main():
    year = '2020'
    # for year in range(2020):
    web_analysis_and_get_team_lists(str(year))
    return 0


main()
#test for github