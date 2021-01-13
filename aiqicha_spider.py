#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Administrator
@file: aiqicha_spider.py
@time: 2021/01/{DAY}
"""
from selenium.common.exceptions import TimeoutException
import sys
'''
用途：信息收集公司名称获取当前公司URL
https://aiqicha.baidu.com/s?q=%E4%B8%AD%E6%96%87%E8%81%94%E7%9B%9F

'''
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import urllib.request
import random
#通过selenium调用浏览器获取当前页面源码


url_aiqicha = 'https://aiqicha.baidu.com/'
def selenium_webdir():
    global driver
    driver=webdriver.Ie()
    driver.set_window_size(480, 400)
    time.sleep(3)


#输入url，获取当前浏览器源码
def selenium_getpage_source(u):
    rand = random.randint(2, 6)
    page_source = ''
    print('随机延迟等待',rand)
    time.sleep(rand)
    driver.get(u)
    try:
        time.sleep(2)
        print('获取当前页面源码')
        page_source = driver.page_source
        return page_source
    except:
        print('加载异常')
        time.sleep(5)

#输入url，获取当前浏览器源码
def selenium_set(u):
    rand = random.randint(2, 10)
    page_source = ''
    print('随机延迟等待',rand)
    driver.get(u)
    time.sleep(5)
    try:
        driver.find_element_by_xpath('//*[@id="aqc-header-search-input"]').clear()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="aqc-header-search-input"]').send_keys(name)
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[1]/header/div/div[2]/button').click()
        time.sleep(2)
        print('获取当前页面源码')
        page_source = driver.page_source
        return page_source
    except:
        print('加载异常')
        time.sleep(5)

#获取域名
def  soup_href_html(htmldata2):
    print('正在获取域名')
    soup = BeautifulSoup(htmldata2, 'lxml')
    for div_child in soup.find_all('div', class_='content-info-child'):
        for a_href in div_child.find_all('a',class_='website'):
            #print('a_href:',a_href)
            w_url=a_href.text   #获取文本内容
            print('获取域名成功:',w_url)
            write_url(w_url+'|'+name)

def aiqicha():
    selenium_webdir()
    global name
    for i in (open(dic_txt,'r')):
        print('''
        *************************开始获取****************************
        ''')
        name=i.strip('\n')
        aiqicha_url = url_aiqicha + 's?q=' + name+'&t=0'
        print('正在获取的公司域',aiqicha_url)
        HTMLget=selenium_getpage_source(aiqicha_url)
        #print('len：',len(HTMLget))
        soup_html(HTMLget)
        print('''
                *************************当前公司获取完成****************************
                ''')
    print('关闭浏览器')
    driver.quit()

def write_url(uu):
    o=open('url.txt','a')
    o.write(uu+'\n')
    o.close()




#获取当前页href
def soup_html(htmldata):
    soup = BeautifulSoup(htmldata, 'lxml')
    for div_card in soup.find_all('div',class_='card'):
        #print('div_card#',div_card)
        for h3_href in div_card.find_all('h3',class_='title'):
            #print('h3_href：', h3_href)
            for a_href in h3_href.find_all('a'):
                href=a_href.get('href')
                print('href:',href)
                url_href=url_aiqicha+href
                print('url_href:',url_href)
                time.sleep(2)
                hrdf_data=selenium_getpage_source(url_href)
                soup_href_html(hrdf_data)
        pass


if __name__=="__main__":
    print(
    '''
    ***************************************************
                    ******作者：ximi******
            ******爱企查获取获取发布的官方域名******
    ***************************************************
    python aiqicha_spider.py butianname.txt
    '''
    )
    dic_txt=sys.argv[1]
    #dic_txt='butianname.txt'
    aiqicha()
    pass