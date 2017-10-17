#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
convenient API to download beauty picture.
"""
from setuptools import setup, find_packages
from beauty import beauty

VERSION = beauty.__version__.split()[1]

setup(
    name='beauty',
    version=VERSION,
    url='https://github.com/zhongjiajie/beauty',
    license='MIT',
    author='zhongjiajie',
    author_email='zhongjiajie955@hotmail.com',
    description=__doc__.strip('\n'),
    packages=find_packages(),
    include_package_data=True,
    # scripts=['bin/beauty.py'],
    install_requires=[
        'docopt >= 0.6.2',
        'requests >= 2.13.0'
    ],
    platforms='any',
    entry_points={
        'console_scripts': [
            'beauty=beauty.beauty:main'
        ]
    },
    classifiers=[
        # As from https://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: System :: Systems Administration',
    ]
)
