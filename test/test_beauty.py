# -*- coding:utf-8 -*-

import unittest
from beauty import Beauty
import random

class TestBeauty(unittest.TestCase):
    _url = 'http://www.55156.com/gaoqingtaotu/xiuren/'

    def test_class_arg(self):
        """test class arg"""
        filter = '[1,2,3,4]'
        path = '/tmp/pic'
        num = ['10', 10]
        beauty = Beauty(self._url, filter=filter, path=path, num=random.choice(num))
        self.assertEquals(self._url, beauty.url)
        self.assertEquals(eval(filter), beauty.filter_list)
        self.assertEquals(path, beauty.path)
        self.assertIn(beauty.num, num)

    def test_scan_pic(self):
        """test beauty scan function"""
        beauty = Beauty(self._url, scan=True)
        self.assertTrue(beauty.is_scan)
        self.assertFalse(beauty.is_download)

    def test_download_pic(self):
        """test beauty download function"""
        beauty = Beauty(self._url, download=True)
        self.assertTrue(beauty.is_download)
        self.assertFalse(beauty.is_scan)



