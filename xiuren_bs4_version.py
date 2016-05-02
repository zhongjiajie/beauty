#!/usr/bin/python
# -*- coding:utf8 -*-
#------------------------------------#
#---脚本：xiuren_bs4_version.py
#---作者：zhongjiajie
#---日期：2016/04/23
#---功能：将第一个版本的正则模块改用成了BeautifulSoup模块，成功爬取所有的页面
#------------------------------------#
import requests
import random
import Queue
from bs4 import BeautifulSoup
import os
import time

#---根据数据类型解析url---#
#--返回格式化soup--#
def getSoupFromUrl(url):
    try:
        #如果输入的是string类型
        head = {'User-Agent':changeUa()}
        m_str_content = requests.get(url=url,headers=head,timeout=30).content
        m_html_soup = BeautifulSoup(m_str_content,"html5lib")
        return m_html_soup
    except:
        writerNormalLog('can not get soup from %s'%url)

#-----从IE,chrome,edge,safari,360浏览器中随机选取ua,模拟他们访问-----#
def changeUa():
    UaList = ['Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
              'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
              'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
              'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)']
    #随机选择上面的一个UA
    ua = random.choice(UaList)
    return ua

#-----获取所有页面的url-----#
def getPageQueue(url):
    m_str_url = url
    #初始化队列
    m_list_pageUrlQueue = Queue.Queue(maxsize=-1)
    #计算传进来的url字符串长度
    s_n_srcUrlNum = len(m_str_url)
    m_str_srcurl = m_str_url[0:s_n_srcUrlNum]
    while(m_str_url):
        try:
            m_list_pageUrlQueue.put(m_str_url)
            # print m_str_srcurl
            str_soup = getSoupFromUrl(m_str_url)
            m_str_partOfPage = str_soup.find(name='div',attrs={'class':'pages'}).find(name='li',text='下一页').a['href']
            m_str_url = m_str_srcurl + m_str_partOfPage
            # print m_str_url
        except:
            writerNormalLog('suceed get all page of %s!'%url)
            break
    return m_list_pageUrlQueue

#-----单个页面所有人的url-----#
def getPersonQueue(queue):
    #初始化个人url队列
    m_queue_personUrl = Queue.Queue(maxsize=-1)
    #初始化个人作品名队列
    m_queue_personName = Queue.Queue(maxsize=-1)
    while (queue.empty() != True):
        m_soup_eachPage = getSoupFromUrl(queue.get())
        #作品集中页面
        try:
            m_list_eachPagePerson = m_soup_eachPage.find(name='ul',attrs={'class':'liL'}).find_all('li')
            for m_str_eachPerson in m_list_eachPagePerson:
                #当前页面所有人url
                m_url_person = m_str_eachPerson.find(name='a')['href']
                # print m_url_person
                #当前页面所有人作品名
                m_str_name = m_str_eachPerson.find(name='a')['title']
                # print m_str_name
                m_queue_personUrl.put(m_url_person)
                m_queue_personName.put(m_str_name)
        except:
            writeErrorLog('can not person url [%s] or person name [%s],getPersonQueue function do not well!'%m_url_person,m_str_name)
    return m_queue_personUrl,m_queue_personName

#-----单个作品的所有图片url-----#
def getPicUrl(srcUrl,url):
    #初始化个人url队列
    m_queue_eachPicUrl = Queue.Queue(maxsize=-1)
    m_url_nextPage = url
    #翻页操作
    while True:
        #单页图片
        try:
            m_soup_personPic = getSoupFromUrl(m_url_nextPage)
            m_url_personPic = m_soup_personPic.find(name='p',attrs={'align':'center'}).img['src']
            # print m_url_personPic
            m_queue_eachPicUrl.put(m_url_personPic)
            m_str_partOfPage = m_soup_personPic.find(name='div',attrs={'class':'pages'}).find(name='li',attrs={'class':'thisclass'}).next_sibling.a['href']
            if (m_str_partOfPage != '#'):
                m_url_nextPage = srcUrl + m_str_partOfPage
            else:
                writerNormalLog('suceed get person url [%s]'%url)
                break
        except:
            writeErrorLog('can not get picture url [%s],getPicUrl function do not well'%m_url_personPic)
    return m_queue_eachPicUrl

#-----下载图片-----#
def downloadPic(path,urlQueue,name):
    #若不存在创建目录
    if (os.path.exists(path+name) == False):
        os.makedirs(path+name)
        # writerNormalLog('suceed create folder %s'%(path+name))
    s_n_picName = 1
    while (urlQueue.empty() != True):
        try:
            m_url_eachPicOfperson = urlQueue.get()
            # print url
            head = {'User-Agent':changeUa()}  #模拟浏览器
            content = requests.get(m_url_eachPicOfperson,headers=head,timeout =30).content
            with open(path+name+'/%s.jpg'%s_n_picName, "wb+") as f:  #在特定文件夹写入图片
                f.write(content)
                writerNormalLog('suceed download picture %s'%m_url_eachPicOfperson)
            s_n_picName += 1
            #一个作品内部的暂停
            # sleep_time = random.uniform(1,2)
            # time.sleep(sleep_time)
        except:
            writeErrorLog('can not download %s,downloadPic function do not well'%m_url_eachPicOfperson)
    return 0

#------日志模块------#
  #获取当前系统时间 返回 年-月-日 时:分:秒
def getNowTime():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

  #---写错误日志到xiuren.log---#
def writeErrorLog(errorContent):
    cues = '  ERROR_LOG    '      #日志类型提示
    delimiter = '--------------------------------------------------------------------------------'
    errorDetail = '[' + getNowTime() + ']' + cues + errorContent
    with open(r'xiuren.log','a') as f:
        f.write(delimiter   + '\n' +
                errorDetail + '\n' +
                delimiter   + '\n')

  #---写正常日志到xiuren.log---#
def writerNormalLog(normalContent):
    cues = '  NORMAL_LOG   '      #日志类型提示
    normalDetail = '[' + getNowTime() + ']' + cues + normalContent
    with open(r'xiuren.log','a') as f:
        f.write(normalDetail + '\n')

#删除上次日志文件
if os.path.exists('./xiuren.log'):
    os.remove('xiuren.log')
#文件存放路径
path = 'E:/beauty/'
#网站url
s_str_srcUrl = 'http://www.du114.com/gaoqingtaotu/xiuren/'
#获取所有的页面
m_list_pageUrlQueue = getPageQueue(s_str_srcUrl)
#获得每个页面所有作品链接，作品名称
m_queue_allPersonUrl,m_queue_allPersonName = getPersonQueue(m_list_pageUrlQueue)
#遍历作品队列
while (m_queue_allPersonName.empty() != True):
    m_url_eachPerson = m_queue_allPersonUrl.get() #单个作品url
    m_str_eachPersonName = m_queue_allPersonName.get() #单个作品名称
    #单个作品的所有图片url
    m_queue_eachNameUrl = getPicUrl(s_str_srcUrl,m_url_eachPerson)
    #下载图片
    downloadPic(path,m_queue_eachNameUrl,m_str_eachPersonName)
    #作品与作品之间的暂停
    # sleep_time = random.uniform(2,3)
    # time.sleep(sleep_time)