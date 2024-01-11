# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 12:48:23 2022

@author: Cyrus
"""
#import libraries
import numpy as np
import pandas as pd

# # creating a dataframe
# df = pd.DataFrame({'Name': ['Raj', 'Akhil', 'Sonum', 'Tilak', 'Divya', 'Megha','seven','eight','nine','ten','eleven','tweleve'],
# 				'Age': [20, 22, 21, 19, 17, 23, 12, 12,12,8,9,10],
# 				'Rank': [1, np.nan, 8, 9, 4, np.nan,12,8,10,7,7,7]})

# # printing the dataframe
# print('DATAFRAME')
# print(df)

# print('SORTED DATAFRAME')
# df.sort_values(by = ['Age', 'Rank'], ascending = [True, False], na_position = 'first',inplace=True)

# print(df)

dic = {"one":1,"two":{"a":"aaa","b":"bbb"},"three":3}
test1 = dic.get('tw')
print(f'test1 = {test1}')
if not test1 == None:
    print('not none!')
else:
    print('none')        