#!/usr/bin/python3
# -*- coding: utf-8 -*-
# mingzhe.xiang
# 2020/8/25 17:18
from collections import defaultdict


def is_permutation(str1, str2):
    if str1 is None or str2 is None:
        return False
    if len(str1) != len(str2):
        return False
    unq_s1 = defaultdict(int)
    unq_s2 = defaultdict(int)
    for c1 in str1:
        unq_s1[c1] += 1
    for c2 in str2:
        unq_s2[c2] += 1
    print(f'unq_s1:{unq_s1};unq_s2:{unq_s2}')
    return unq_s1 == unq_s2


def is_permutation2(str1, str2):
    if str1 is None or str2 is None:
        return False
    if len(str1) != len(str2):
        return False
    return sorted(str1) == sorted(str2)


if __name__ == '__main__':
    print(f"nice && cine: {is_permutation('nice', 'cine')}")
    print(f"'' && '': {is_permutation('', '')}")
    print(f"one && one2: {is_permutation('one', 'one2')}")
