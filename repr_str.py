#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Student:

    def __init__(self, name, age):
        self._name = name
        self._age = age

    def __repr__(self):
        return f'__repr__ : name:{self._name} ===> age:{self._age}'

    def __str__(self):
        # return self.__repr__()
        return f'__str__: name:{self._name} ===> age:{self._age}'

    @classmethod
    def f(cls):
        print(f'fff{cls}')


if __name__ == '__main__':
    student = Student('zhangsan', 20)
    # 未定义__str__时使用__repr__
    print(student)
    # iterable时 使用__repr__
    print([student, Student('sisi', 22)])
    # print(dir(student))
    print(Student.f())
