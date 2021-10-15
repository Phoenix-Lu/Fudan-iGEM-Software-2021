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





# def main():





#这一步先直接对excel做处理,给出每个part引用的对象，再生成excel给出各part被引用的上级和被引用数







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


