#!/usr/bin/python3
# -*- coding: utf-8 -*-

from functools import wraps


def _flat(v):
    """
    flat list item
    """
    for i in v:
        if type(i) == list:
            yield from _flat(i)
        else:
            yield i


def log_dec(fn):
    """
    Decorator
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        print('-------before----')
        fn(*args, **kwargs)
        print('-------end----')

    return wrapper


@log_dec
def test_log(a):
    print('this is call function ', a)


print(list(_flat([1, 2, [3, 4], 'python'])))
test_log(2)
