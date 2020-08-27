#!/usr/bin/python3
# -*- coding: utf-8 -*-
# mingzhe.xiang
# 2020/8/25 18:23

import os

"""
    列出当前列表所有.py
    os.path.splitext(): [filePath, fileExtension]
"""
print(os.listdir('.'))
print(os.path.abspath('.'))
# 获取所有python文件
print([x for x in os.listdir('.') if os.path.splitext(x)[1] == '.py'])
print(list(map(lambda x: os.path.split(x)[1], [x for x in os.listdir('.')])))
