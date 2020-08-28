#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import zipfile

"""

简单的压缩程序,只为解决公司平台限制.工作使用

"""

# 工作中用到是固定的过滤文件夹 暂写死 后续考虑 argparse
IGNORE_DIRS = ('.idea', '.git')


def zip_dir(target_dir=os.getcwd(), include_empty_dir=True):
    zip_file_name = target_dir + '.zip'
    parent_path = os.path.split(target_dir)[0]
    ignore_paths = list(map(lambda x: os.path.join(target_dir, x), IGNORE_DIRS))
    try:
        zip_file = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
        # 遍历目录文件信息
        for root, dirs, files in os.walk(target_dir):
            if [x for x in ignore_paths if root.startswith(x)]:
                continue

            # 定义压缩目录起始
            new_file_path = root.replace(parent_path, '')
            new_file_path = new_file_path and new_file_path + os.sep

            # 压缩空目录
            if include_empty_dir and not dirs and not files:
                zip_file.write(os.path.join(root), new_file_path)
                continue
            # 压缩文件
            for file in files:
                zip_file.write(os.path.join(root, file), new_file_path + file)
    finally:
        if zip_file:
            zip_file.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        zip_dir(sys.argv[1], False)
    else:
        zip_dir()
