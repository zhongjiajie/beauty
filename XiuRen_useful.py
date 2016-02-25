# -*- coding:utf-8 -*-

import re
import os
import time
import random
import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool

#从IE,chrome,edge,safari,360浏览器中随机选取ua,模拟他们访问
def GetUa():
    UaList = ['Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
              'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
              'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
              'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)']
    ua = random.choice(UaList)
    return ua

#访问URL并放回‘utf-8’格式的HTML
def GetHtml(url):
    try:
        head = {'User-Agent':GetUa()}  #模仿浏览器的头文件
        # data = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #         'Accept-Encoding':'gzip, deflate, sdch',
        #         'Accept-Language':'zh-CN,zh;q=0.8',
        #         'Host':'www.du114.com',
        #         'Upgrade-Insecure-Requests':'1',
        #         'User-Agent':GetUa()}
        html0 = requests.get(url,headers=head,timeout =30)  #设置超时30S
        html0.encoding = 'utf-8'
        html1 = html0.text
        return html1
    except:
        with open(r'failure_download_url.txt','a') as f:  #如果下载失败，将失败的URL写入文件failure_download_url.txt，并打印在屏幕
            f.write(url + '\n')
        print 'download ' + url + ' failure!'

#获取当前页面所有个人的链接，其中大部分一个页面有30个秀人链接
def EachPagePerson(html):
    html1 = re.search('<ul class="liL">(.*?)</div>',html,re.S).group(1)
    person_url = re.findall('<li><a href="(.*?)" title="',html1,re.S)
    # person_name = re.findall('" title="(.*?)" class="',html1,re.S)
    return person_url

#获取秀人网的所有页面，其中每个页面有多位秀人
def GetAllPage(html):
    content = re.findall("href='(.*?)</a></li>",html,re.S)[-1][0:-4]   #获取有用部分总体，总体在<li>标签下
    url_part = content[0:-7]   #所有页面部分的url
    page_number = int(content[-7:-5])   #获取所有页面的总页数

    all_page_url = []  #所有页面的URL
    for number in range (1,page_number+1):
        page_url = url0 + url_part + str(number) + '.html'  #组成各个页面的URL
        all_page_url.append(page_url)
    return all_page_url

#获取单个秀人的所有图片真是地址
def PersonAllUrl(html):
    try:
        person_page = int(re.search('<ul><li><a>(.*?): </a></li><li>',html,re.S).group(1)[1:-1]) #个人所拥有的图片总数
        useful_content = re.search('<p align="center">(.*?)" /></a></p>',html,re.S).group(1)  #获得有用的html，包含图片真实地址
        target_url = BeautifulSoup(useful_content).img['src'] #获取目标图片的字符串
        target_name = BeautifulSoup(useful_content).img['alt'] #获取目标的系列名称，作为文件夹

        part_of_url = target_url[0:-5] #提取该URL的部分，为了后面生成所有的URL做准备
        frist_page = re.search('(.*?)\.jpg',target_url,re.S).group(1)[-1:] #获取当前的图片位于该系列图片的张数
        frist_page = int(frist_page)

        now_page = frist_page
        person_all_url = []
        while now_page < person_page + frist_page: #遍历该秀人所有的张数
            now_url = part_of_url + str(now_page) + '.jpg' #
            # print now_url
            now_page = now_page + 1
            with open('all_url.txt','a') as f: #记录下所有的图片真实链接
                f.write(now_url + '\n')
            person_all_url.append(now_url) #组成该秀人的所有图片链接列表
        return target_name,person_all_url
    except:
        with open('html_error.txt','a') as f:  #如果该秀人的HTML与别的秀人的HTML不同，则写入文件html_error.txt等待后面处理
            f.write(html + '\n' + '###############################################################')

#获取每张图片的真实地址后，下载图片到制定的目录中
def DownloadPicture(url):
    try:
        # data = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #         'Accept-Encoding':'gzip, deflate, sdch',
        #         'Accept-Language':'zh-CN,zh;q=0.8',
        #         'Host':'www.du114.com',
        #         'Upgrade-Insecure-Requests':'1',
        #         'User-Agent':GetUa()}
        head = {'User-Agent':GetUa()}  #模拟浏览器
        html = requests.get(url,headers=head,timeout =30)
        picture_name = url[-6:].replace('/','_') #对单张图片URL进行处理，作为图片的名称

        with open(r'E://Photo//%s//%s'%(person_name,picture_name), "wb+") as f:  #在特定文件夹写入图片
            f.write(html.content)
        # print 'download ' + url + ' OK!'
        sleep_time = random.uniform(5,7)
        time.sleep(sleep_time)
    except:
        with open(r'failure_download_url.txt','a') as f:  #如果下载失败，将失败的URL写入文件failure_download_url.txt，并打印在屏幕
            f.write(url + '\n')
        print 'download ' + url + ' failure!'

if __name__ == '__main__':
    # url0 = 'http://www.du114.com/a/xiuren/' #套图超时中的秀人网地址
    url0 = 'http://www.du114.com/gaoqingtaotu/xiuren/'
    html0 = GetHtml(url0)  #获取'http://www.du114.com/a/xiuren/'的HTML
    # print html0
    all_page_url = GetAllPage(html0)  #获取'http://www.du114.com/a/xiuren/'所有的页面URL
    print all_page_url

    all_person_url = []
    for each_page in all_page_url:
        page_html = GetHtml(each_page)  #获取当前页面的HTML
        person_url = EachPagePerson(page_html)  #从分析出来的HTML里面选出当前页面全部秀人的url
        for each in person_url:
            all_person_url.append(each) #遍历所有的页面，并把所有的秀人首页URL链接起来，生成 all_person_url列表
        # print all_person_url

    global person_name  #定义下载目录文件夹为全局变量，主要用于DownloadPicture（url）函数
    for each_person_url in all_person_url:
        person_html = GetHtml(each_person_url)  #将每一个秀人首页HTML
        person_name,person_all_url = PersonAllUrl(person_html) #从他们首页中获取图片真实的地址以及系列名称

        if not os.path.exists(r'E://Photo//%s'%person_name):    #判断文件夹中是否有该系列名称的文件夹，没有则建立一个文件夹
            os.mkdir(r'E://Photo//%s'%person_name)

        pool = ThreadPool(4)  #初始化一个4线程
        pool.map(DownloadPicture,person_all_url)  #多线程下载
        pool.close()
        pool.join()

        sleep_time = random.uniform(3,5)  #除了下载时的SLEEP之外，在下载完一个文件夹后，同样SLEEP一段时间
        time.sleep(sleep_time)