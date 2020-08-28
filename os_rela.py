#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

"""
    列出当前列表所有.py
    os.path.splitext(): [filePath, fileExtension]
"""
print(os.listdir('.'))
print(os.path.abspath('.'))
print(os.getcwd())
# 获取所有python文件
print([x for x in os.listdir('.') if os.path.splitext(x)[1] == '.py'])
# max key ==> [1,2,3]
print(max([1, 2, 3], [4], [11, 299], key=lambda x: len(x), ))
