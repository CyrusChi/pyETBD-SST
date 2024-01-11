# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 20:22:10 2023

@author: Cyrus
"""
import numpy as np
final_list = []
shuffle_schedule_x_and_after = 3
cut_off = shuffle_schedule_x_and_after

dic = {"1":"a","2":"b","3":"c","4":"d","5":"e","6":"f","7":"f"}

key_list = dic.keys()
# key_list2 = list(key_list)
print(f'dic get = {dic.get("7")}')
print(f'dic = {dic["7"]}')
# check to make sure it is all intergers, or intergers as strings
try:
    key_list2 = list(map(int, key_list))
except:
    print('the dictionary has a non-integer string!')
    raise

#check uniqueness This shouldn't be necessary since dictionary keys must be unique
key_list2_ar = np.array(key_list2)
key_list2_ar_unique = np.unique(key_list2_ar)
if len(key_list2_ar) != len(key_list2_ar_unique):
    print('Dictionary values are not unique!')
    raise

key_list3_ar = np.sort(key_list2_ar)
key_cut_off_mask = np.greater_equal(key_list3_ar,cut_off)
key_ordered_mask = np.invert(key_cut_off_mask)
ordered_items = key_list3_ar[key_ordered_mask]
shuffled_items = key_list3_ar[key_cut_off_mask]
np.random.shuffle(shuffled_items)

print(f'pre = {shuffled_items}')


# np.shuffle(shuffled_items_pre)
# print(f'post = {shuffled_items_pre}')
# print(f'{np.greater_equal(key_list3_ar,cut_off)}')
# print(f'{key_ordered_mask}')
# print(key_list3_ar[key_ordered_mask])
# # print(key_list)
# np.random.shuffle(key_list2_ar)
# # print(key_list2)
# print(f'len(list) = {len(key_list3_ar)}')


final_list.extend(list(ordered_items))
final_list.extend(list(shuffled_items))
final_list2 = list(map(str,final_list))

print(f'key_list = {key_list}')
print(f'key_list2 = {key_list2}')
print(f'key_list3_ar = {key_list3_ar}')

print(f'final list = \n{final_list}')
print(f'final list2 = \n{final_list2}')