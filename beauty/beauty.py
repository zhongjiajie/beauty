#!/usr/bin/env python
# -*- coding:utf-8 -*-

u"""Usage:
  beauty.py scan <NAME> [-n=<num>] [-p=<path>]
  beauty.py download <NAME> [-n=<num>] [-f=<list>] [-p=<path>]
  beauty.py (--help | -h)
  beauty.py --version

Options:
  --help -h                     Show this screen.
  --version                     Show version.
  --num -n=<num>                Number of picture to download, [default 10].
  --filter -f=<list>            Filter from parameter --num album number
  --path -p=<path>              Path to download picture, [default `$cmd_path/pic/`].

Arguments:
  NAME                          Album name to download or scan, including
  NAME = {
    'dgc' : 'DGC',     'ligui':  '丽柜写真',   'ru1mm': 'Ru1mm如壹',  '3agirl': '3Agirl写真',
    'tgod': '推女神',   'xiuren': '秀人网',    'donggan': '动感小站',  'topqueen': 'TopQueen',
    'bomb': 'Bombtv',  'mygirl': '美媛馆',     'scute': 's-cute套图', 'rqstar': 'RQ_STAR写真',
    'disi': '第四印象', 'rosi':   'rosi写真',  'tuigirl': '推女郎',    '4kstar': '4K-STAR写真',
    'pans': 'pans写真', 'simei':  '丝魅VIP',   'youguowang': '尤果网', 'tpimage': 'Tpimage套图',
    'beautyleg': 'Beautyleg写真', 'onlytease': 'OnlyTease写真',
  }
"""
import os
import random
import re
import shutil

import requests
from docopt import docopt

from user_agents import agents


class Beauty(object):
    _SMALL_PIC_TMP_REGEX = r'<div class="listBox" id="imgList">.*?</div>'
    _SMALL_PIC_NAME_REGEX = r'<a href="(.*?)" title="(.*?)" class="picLink"><img src="(.*?)"'
    _SAMLL_NEXT_PAGE_REGEX = r'<a target=\'_self\' href=\'(.*?)\'>下一页</a></li>'
    _BIG_PIC_REGEX = r'<img alt=".*?" src="(.*?)" />'
    _BIG_NEXT_PAGE_TMP_REGEX = r'<div class="pages"(.*?)</ul>'
    _BIG_NEXT_PAGE_REGEX = r'<a href=\'(.*?)\''

    _SMALL_PIC_TMP_PATTERN = re.compile(_SMALL_PIC_TMP_REGEX, re.S)
    _SMALL_PIC_NAME_PATTERN = re.compile(_SMALL_PIC_NAME_REGEX)
    _SAMLL_NEXT_PAGE_PATTERN = re.compile(_SAMLL_NEXT_PAGE_REGEX)
    _BIG_PIC_PATTERN = re.compile(_BIG_PIC_REGEX)
    _BIG_NEXT_PAGE_TMP_PATTERN = re.compile(_BIG_NEXT_PAGE_TMP_REGEX, re.S)
    _BIG_NEXT_PAGE_PATTERN = re.compile(_BIG_NEXT_PAGE_REGEX)

    def __init__(self, url, scan=False, download=False, filter=None, path=None, num=None):
        """初始化参数及正则表达式"""
        self.url = url
        self.is_download = download
        self.is_scan = scan
        self.filter_list = eval(filter) if filter else None
        self.path = path if path else './pic'
        self.num = int(num) if num else 10  # 0下载全量 其他下载指定数量

    @staticmethod
    def get_response(url):
        """获取网页源代码"""
        headers = {
            'User-Agent': random.choice(agents)
        }
        response = requests.get(url, headers=headers)

        return response

    def parse(self):
        """Beauty主函数"""
        big_pic_name = []
        html = self.get_response(self.url).content
        big_pic_name.extend(self._parse_small_pic(html))

        while len(big_pic_name) < self.num:
            samll_next_page = self._parse_small_next_page(html)
            html = self.get_response(samll_next_page).content
            big_pic_name.extend(self._parse_small_pic(html))

        pic_no_dct = {os.path.basename(i[0]).split('.')[0]: list(i)
                      for i in big_pic_name[:self.num]}
        # 下载指定album
        if self.filter_list:
            pic_no_dct = {key: pic_no_dct[key] for key in pic_no_dct
                          if int(key) in self.filter_list}
        # 下载图片
        if self.is_download:
            for album in pic_no_dct:
                big_pic_url = pic_no_dct[album][0]
                album_name = pic_no_dct[album][1].decode('utf8')

                html = self.get_response(big_pic_url).content
                for url in self._parse_big_pic(html, url=big_pic_url):
                    pic_no_dct[album].append(url)
                folder = u'{album}_{name}'.format(album=album, name=album_name)
                self._download_pic(folder, pic_no_dct[album][3:])
        # 浏览图片
        elif self.is_scan:
            scan_dct = {key: pic_no_dct[key][2] for key in pic_no_dct}
            self._scan_pic(scan_dct)

    def _parse_small_pic(self, html):
        """解析小图"""
        mid_html = self._SMALL_PIC_TMP_PATTERN.findall(html)[0]
        pic_url_name = self._SMALL_PIC_NAME_PATTERN.findall(mid_html)

        return pic_url_name

    def _parse_small_next_page(self, html):
        """解析下一页小图"""
        part_url = self._SAMLL_NEXT_PAGE_PATTERN.findall(html)[0]

        return self._subsite_url(part_url)

    def _parse_big_pic(self, html, **kwargs):
        """解析大图"""
        for url in self._parse_big_sub(html, **kwargs):
            yield url

    def _parse_big_sub(self, html, **kwargs):
        """解析大图子函数"""
        next_page_mid = self._BIG_NEXT_PAGE_TMP_PATTERN.findall(html)[0]
        next_page = self._BIG_NEXT_PAGE_PATTERN.findall(next_page_mid)[-1]

        yield self._BIG_PIC_PATTERN.findall(html)[0]

        while next_page != '#':
            html = self.get_response(os.path.split(kwargs['url'])[0]
                                     + '/' + next_page).content
            next_page_mid = self._BIG_NEXT_PAGE_TMP_PATTERN.findall(html)[0]
            next_page = self._BIG_NEXT_PAGE_PATTERN.findall(next_page_mid)[-1]

            yield self._BIG_PIC_PATTERN.findall(html)[0]

    def _subsite_url(self, part_url):
        """返回子页面完整url"""
        return self.url + part_url

    def _scan_pic(self, dct):
        """浏览图片"""
        path = '{path}/scan'.format(path=self.path)
        self._create_folder(path)
        for album_no in dct:
            file_name = '{album_no}.jpg'.format(album_no=album_no)
            pic_path = '{path}/{file_name}'.format(
                path=path, file_name=file_name)
            self._download(pic_path, dct[album_no])

    def _download_pic(self, folder, url_lst):
        """下载大图"""
        path = u'{path}/{folder}'.format(path=self.path, folder=folder)
        self._create_folder(path)
        len_ = len(url_lst)
        curr_ = 0

        for url in url_lst:
            curr_ += 1
            print u'{album} total picture num:{total_no}, ' \
                  u'downloading NO.{pic_no} picture\r'. \
                format(album=folder, total_no=len_, pic_no=curr_),

            file_name = u'{album}_{part}.jpg'.format(
                album=folder.split('_')[0], part=curr_)
            pic_path = u'{path}/{file_name}'.format(
                path=path, file_name=file_name)
            self._download(pic_path, url)

        print u'finish download album {album}'.format(album=folder)

    def _download(self, path, url):
        """下载图片"""
        with open(path, 'wb+') as f:
            try:
                f.write(self.get_response(url).content)
            except:
                print 'download picture {url} fail.'.format(url=url)

    def _create_folder(self, path):
        """创建文件夹"""
        if os.path.exists(path):
            self._del_path(path)
        os.makedirs(path)

    @staticmethod
    def _del_path(path):
        """删除文件或文件夹"""
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


__version__ = 'beauty 0.3.2'

NAME = {
    'xiuren': ['http://www.55156.com/gaoqingtaotu/xiuren/', u'秀人网'],
    'mygirl': ['http://www.55156.com/a/Mygirl/', u'美媛馆'],
    'beautyleg': ['http://www.55156.com/a/Beautyleg/', u'Beautyleg写真'],
    'tgod': ['http://www.55156.com/a/TGOD/', u'推女神'],
    'youguowang': ['http://www.55156.com/gaoqingtaotu/youguowang/', u'尤果网'],
    'scute': ['http://www.55156.com/a/s-cute/', u's-cute套图'],
    'topqueen': ['http://www.55156.com/a/TopQueen/', u'TopQueen'],
    'dgc': ['http://www.55156.com/a/DGC/', u'DGC'],
    'bomb': ['http://www.55156.com/a/Bomb.tv/', u'Bomb.tv'],
    'rqstar': ['http://www.55156.com/a/RQ_STARxiezhen/', u'RQ_STAR写真'],
    'tpimage': ['http://www.55156.com/a/Tpimage/', u'Tpimage套图'],
    'onlytease': ['http://www.55156.com/a/OnlyTease/', u'OnlyTease写真'],
    'pans': ['http://www.55156.com/a/pans/', u'pans写真'],
    'donggan': ['http://www.55156.com/a/donggan/', u'动感小站'],
    '3agirl': ['http://www.55156.com/a/3Agirl/', u'3Agirl写真'],
    'simei': ['http://www.55156.com/a/simei/', u'丝魅VIP'],
    'rosi': ['http://www.55156.com/a/rosi/', u'rosi写真'],
    'ligui': ['http://www.55156.com/a/ligui/', u'丽柜写真'],
    'disi': ['http://www.55156.com/a/disi/', u'第四印象'],
    'ru1mm': ['http://www.55156.com/a/Ru1mm/', u'Ru1mm如壹'],
    '4kstar': ['http://www.55156.com/a/4K-STAR/', u'4K-STAR写真'],
    'tuigirl': ['http://www.55156.com/gaoqingtaotu/TuiGirl/', u'推女郎']
}


def main():
    args = docopt(__doc__, version=__version__)

    # 校验名称有对应的URL
    if args['<NAME>'] not in NAME:
        print __doc__
        exit(0)

    kwargs = {
        'scan': args['scan'],
        'download': args['download'],
        'url': NAME[args['<NAME>']][0],
        'num': args['--num'],
        'filter': args['--filter'],
        'path': args['--path']
    }

    beauty = Beauty(**kwargs)
    beauty.parse()


if __name__ == '__main__':
    main()
