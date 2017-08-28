#!/usr/bin/env python
# -*- coding:utf-8 -*-

u"""Usage:
  beauty.py scan <NAME> [-n=<num>] [-p=<path>]
  beauty.py download <NAME> [-n=<num>] [-f=<list>] [-p=<path>]
  beauty.py (--help | -h)
  beauty.py --version
  
Arguments:
  NAME                          Album name to download or scan, including
  NAME = {
    'xiuren':     '秀人网',
    'mygirl':     '美媛馆',
    'beautyleg':  'Beautyleg写真',
    'tgod':       '推女神',
    'youguowang': '尤果网',
    'scute':      's-cute套图',
    'topqueen':   'TopQueen',
    'dgc':        'DGC',
    'bomb':       'Bomb.tv',
    'rqstar':     'RQ_STAR写真',
    'tpimage':    'Tpimage套图',
    'onlytease':  'OnlyTease写真',
    'pans':       'pans写真',
    'donggan':    '动感小站',
    '3agirl':     '3Agirl写真',
    'simei':      '丝魅VIP',
    'rosi':       'rosi写真',
    'ligui':      '丽柜写真',
    'disi':       '第四印象',
    'ru1mm':      'Ru1mm如壹',
    '4kstar':     '4K-STAR写真',
    'tuigirl':    '推女郎'
}

Options:
  --help -h                     Show this screen.
  --version                     Show version.
  --num -n=<num>                Number of picture to download, [default 10].
  --filter -f=<list>            Filter from parameter --num album number
  --path -p=<path>              Path to download picture, [default `$project/pic/`].
"""

# test
# from pprint import pprint

from docopt import docopt

from beauty import Beauty

__version__ = 'beauty v0.2'

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

    # test
    # pprint(kwargs)

    beauty = Beauty(**kwargs)
    beauty.parse()


if __name__ == '__main__':
    main()
