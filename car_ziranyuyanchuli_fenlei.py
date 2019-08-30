# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 15:10:07 2019

@author: Administrator
"""
import sys
sys.path.append('C:/Users/Administrator/Desktop/qicheziti')

import random
import re
import time
import json
import requests
import csv
from selenium import webdriver
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from AutoHomeFont import get_new_font_dict

browser = webdriver.Chrome()

from fake_useragent import UserAgent
ua = UserAgent()



##获取详情页，需要输入两个参数
def get_one_page(page,bbsid):
    print('正在读取第:%d页'%(page))
    try:
        params = {
            'pageindex': page,
            'pagesize': '50',
            'bbs': 'c',
            'bbsid': bbsid,
            'fields': 'topicid,title,post_memberid,post_membername,postdate,ispoll,ispic,isrefine,replycount,viewcount,videoid,isvideo,videoinfo,qainfo,tags,topictype,imgs,jximgs,url,piccount,isjingxuan,issolve,liveid,livecover,topicimgs',
            'orderby': 'topicid-'
        }
        headers = {
            'User-Agent': ua.random
        }
        url = 'https://club.autohome.com.cn/frontapi/topics/getByBbsId?' + urlencode(params)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
            return None
    except requests.exceptions:
        return None


def article_content(urls):
    try:
        headers = {
            'User-Agent': ua.random
        }
        response = requests.get(urls, headers=headers)
        if response.status_code == 200:
            return response.text
            return None
    except requests.exceptions:
        return None
    time.sleep(random.uniform(0.3, 1))
  
def sele_request(urls):
    browser.get(urls)
    return browser.page_source   
    
def parse_doc(content):
    doc = pq(content)
    #首先先判断这一页网页是不是没有文字，只是视频，那么这个寻找会出错
    origin = re.search(',url\(\'//(.*ttf)\'\)', content)
    if str(origin)=='None':
        return None
    else:
        # 那么便开始通过字体库进行解析
        ttfUrl = re.findall(',url\(\'//(.*ttf)\'\)', content)[0]
        ttfRes = requests.get("https://" + ttfUrl)
        with open('temp.ttf', 'wb') as fw:
            fw.write(ttfRes.content)
        print("新一轮反爬虫字体下载成功..." )
        standardFontPath = 'standardFont.ttf'
        newFontPath = 'temp.ttf'
        font_dict = get_new_font_dict(standardFontPath, newFontPath)
        con = doc('.tz-paragraph').text().strip().encode('unicode_escape')
        for key, value in font_dict.items():
            new_key = r"\u" + key[3:].lower()
            con = con.replace(str.encode(new_key), str.encode(value))
        postContent = con.decode('unicode_escape').replace(" ", "").replace("\n", "").replace("\xa0", "")
        return postContent
    
##返回一个json数据,然后进行解析，并且将第二个参数放入表格做列区分
def parse_json_data(html,bbsid):
    data = json.loads(html)
    if data and 'result' in data.keys():
        result_list = data.get('result').get('list')
        for item in result_list:
            urls = item.get('url')
            con_d = sele_request(urls)
            con = parse_doc(con_d)
            yield{
                    'bbsid':bbsid,
                    '用户ID':item.get('post_memberid'),
                    '发布时间':item.get('postdate')[0:10],
                    '帖子类型':item.get('topictype'),
                    '内容':con
                    }


def save_to_csv(dics):
    with open('C:/Users/Administrator/Desktop/文件集合/chuangku.csv','a',encoding='utf_8_sig',newline='') as csvfile:
        fieldnames = ['bbsid','用户ID','发布时间','帖子类型','内容']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writerow(dics)
        
                   
def main():
    for (bbsid,order) in [('3335',35)]:
        for page in range(1,order):    
            html = get_one_page(page,bbsid)
            par_con = parse_json_data(html,bbsid)
            for item in par_con:
                save_to_csv(item)
                time.sleep(2.6)
if __name__ == '__main__':
    main()


#,('3959',220),('448',365),('526',365),('364',280),('3954',295),('358',140),('314',365),('1007',85),('4235',275)

'''
browser = webdriver.Chrome()
urls='http://club.autohome.com.cn/bbs/thread/6694b6a39b214e3a/82807460-1.html'
browser.get(urls)
m=browser.find_element_by_css_selector('#F0 > div.conright.fr > div.rconten')
if m != None:
    return m.text
else:
    browser.find_element_by_xpath('//*[@id="embed-captcha"]/div/div[2]/div[1]/div[3]/span[1]').click()
    m=browser.find_element_by_css_selector('#F0 > div.conright.fr > div.rconten')
    return m.text


if sub != None:
    return sub.text
else:
    sub.find_element_by_xpath('//*[@id="embed-captcha"]/div/div[2]/div[1]/div[3]/span[1]').click()
    return sub.text
'''






