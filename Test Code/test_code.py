# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 08:55:46 2022

@author: Cyrus
"""
# import json
import numpy

print("hello world")
# print(globals())
print(numpy.pi)

#json data pulling schedules
# a.alldata["experiments"][0]["schedules"][0]
#list(test_dict.keys())[1]) #converts dict_keys into a list
#Dictionary1.update({'C': 'Geeks'})

with open('test.txt', 'r') as f: # r = read, w = write, a = append, r+
    size_to_read = 100
    # f.seek(0) #where to start
    f_contents = f.read(size_to_read) # number of characters to read

    while len(f_contents) > 0:
        print(f_contents, end='*')
        f_contents = f.read(size_to_read)
    # f_contents = f.read()
    # f_contents = f.readlines()
    # f_contents = f.readline()    
    for line in f:
        print(line, end = '*')
        
    pass

with open('test2.txt', 'w') as f:
    # f.write('test')
    pass

############
# import csv
import csv

with open('names.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file) #csv.reader
    with open('new_names.csv', 'w') as new_file:
        fieldnames = ['first_name', 'last_name']

        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')

        csv_writer.writeheader()

        for line in csv_reader:
            del line['email']
            csv_writer.writerow(line)
            

####################################
#setter getter
class Employee:

    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    
    @fullname.setter
    def fullname(self, name):
        first, last = name.split(' ')
        self.first = first
        self.last = last
    
    @fullname.deleter
    def fullname(self):
        print('Delete Name!')
        self.first = None
        self.last = None


emp_1 = Employee('John', 'Smith')
emp_1.fullname = "Corey Schafer"

print(emp_1.first)
print(emp_1.email)
print(emp_1.fullname)

del emp_1.fullname
######################################

# try:
#     f = open('curruptfile.txt')
#     # if f.name == 'currupt_file.txt':
#     #     raise Exception
# except IOError as e:
#     print('First!')
# except Exception as e:
#     print('Second')
# else:
#     print(f.read())
#     f.close()
# finally:
#     print("Executing Finally...")

print('End of program')
class Experiment:
    pass

    def __init__(self):
        pass
    
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    
########################
# Decorators
# from functools import wraps


# def my_logger(orig_func):
#     import logging
#     logging.basicConfig(filename='{}.log'.format(orig_func.__name__), level=logging.INFO)

#     @wraps(orig_func)
#     def wrapper(*args, **kwargs):
#         logging.info(
#             'Ran with args: {}, and kwargs: {}'.format(args, kwargs))
#         return orig_func(*args, **kwargs)

#     return wrapper


# def my_timer(orig_func):
#     import time

#     @wraps(orig_func)
#     def wrapper(*args, **kwargs):
#         t1 = time.time()
#         result = orig_func(*args, **kwargs)
#         t2 = time.time() - t1
#         print('{} ran in: {} sec'.format(orig_func.__name__, t2))
#         return result

#     return wrapper

# import time


# @my_logger
# @my_timer
# def display_info(name, age):
#     time.sleep(1)
#     print('display_info ran with arguments ({}, {})'.format(name, age))

# display_info('Tom', 22)