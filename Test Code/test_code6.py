# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 16:20:16 2022
entropy function testing 
@author: Cyrus
"""
# calculate the entropy for a dice roll
from scipy.stats import entropy
from scipy.stats import sem
import numpy
# discrete probabilities
results = []
for time in range(1000):
    a = numpy.random.choice(range(1024),200)
    # a = range(1024) #max entropy ~= 4.644 for a flat population
    b = numpy.histogram(a, bins=25, range=(0,1024), normed=None, weights=None, density=None)   
    #use 25 bins, because this is about 40.9 digits per bin. 
    #just larger than a target class
    #range_top = 2**Organism.number_of_binary_digits
    #bin_number = 2**(Organism.number_of_binary_digits-6)
    # print(f'b = {b[0]}')
    # print(f'b type = {type(b[0])}')
    c = numpy.sum(b[0])
    d = b[0]/c
    # print(f'd = {d}')
    # p = [3/6, 0/6, 2/6, 0/6, 1/6, 0/6]
    # calculate entropy
    e = entropy(b[0], base=2)
    # print the result
    # print('entropy: %.3f bits' % e)
    results.append(e)
 
    
final = sum(results)/1000
st_error = sem(results)
max_entropy = max(results)
print (f'avg = {final}, SEM = {st_error}, max = {round(max_entropy,4)}')