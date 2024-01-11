# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 14:00:52 2022

@author: Cyrus
"""
#get random background target zones, 10 ri, 10, rr
#but NOT including each other or the primary targets, 471-511, and 512,552
import numpy
import collections

total_range = collections.deque(range(1024))
background_classes = {}

#.count(x)
#.remove(x)
#.index(x)
target1 = collections.deque(range(471,512))
target2 = collections.deque(range(512,553))
for num in target1:
    total_range.remove(num)
for num in target2:
    total_range.remove(num)
counter = 0
for bkgrd in range(20):
    counter +=1
    acceptable = False
    while acceptable == False:
        target_low = numpy.random.choice(total_range,1)
        
        checker = 0
        for n in range(8):
            value = target_low+n
            checker += total_range.count(value)
        if checker == 8:
            acceptable = True
            for j in range(8): 
                total_range.remove(target_low+j)
            background_classes.update({counter:[int(target_low),int(target_low+7)]})

print(background_classes)