#!/usr/bin/python3
# -*- coding: utf-8 -*-


for x in range(1, 10):
    for i in range(1, x + 1):
        print(f'{i}*{x} = {x * i}', end='\t')
    print()
