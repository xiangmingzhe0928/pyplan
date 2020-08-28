#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Student:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    def __repr__(self):
        return f'__repr : name:{self._name} ===> age:{self._age}'

    def __str__(self):
        return f'__str: name:{self._name} ===> age:{self._age}'


if __name__ == '__main__':
    student = Student('zhangsan', 20)
    # 未定义__str__时使用__repr
    print(student)
