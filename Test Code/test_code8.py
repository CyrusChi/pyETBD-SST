# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 10:35:34 2022

@author: Cyrus
"""
import numpy

base_range = numpy.arange(10)
target1_range = numpy.arange(3,7)
target2_range = numpy.arange(2)
print(numpy.isin(base_range,target1_range))
mod_range = numpy.delete(base_range,numpy.isin(base_range,target1_range))
print(base_range)
print(f'mod_range1= {mod_range}')
mod_range = numpy.delete(mod_range,numpy.isin(mod_range,target2_range))
print(f'mod_range2= {mod_range}')
print(mod_range)
background_range = numpy.random.choice(mod_range,4,replace=False)
print(f'background = {background_range}')
bx = 8
bx_in = numpy.isin(bx,background_range)
#numpy.isin(10,a['1'],assume_unique=False)
print(bx_in)

a = numpy.array([1, 2, 3,3, 4,5,6,7,8,9,10])
print(f' a = {a.size}')
aaa = numpy.unique(a)
print(f' u = {aaa.size}')