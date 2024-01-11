# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 11:45:24 2023

@author: Cyrus
"""
import numpy
import collections

a = collections.deque([0])
a.append(1)
a.append(2)
a.append(3)
a.append(4)
a.append(5)
a.append(6)

b = collections.deque([10])
b.append(a[1])
print(a)
print(b)