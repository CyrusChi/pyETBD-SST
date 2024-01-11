# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 21:01:30 2022

@author: Cyrus
"""
from Background_Generator_Module import Background_Generator
import numpy as np
import time

#background generator output types
#output types: "random_nonsequential_post_screening"
#              "max_mean_nonsequential_post_screening"
#              "max_mean_std_nonsequential_post_screening"
#              "max_mean_continuous_post_screening"
#              "max_mean_std_continuous_post_screening" 
#              "random_continuous_post_screening" 
#              "closest_hamming_to_x_nonsequential" (not implemented)
#              "closest_hamming_to_x_continuous" (not implemented)

#------------------------------------------------------------------------------
#Generate background targets based on built default set up (for testing)

Background_Generator.default_setup()
background_targets1 = Background_Generator.generate('random_nonsequential_post_screening')
print('\n')
print(background_targets1)

#------------------------------------------------------------------------------
# compare to target classes 
# return types:'mean_std'
#              'matrix'

# target_class1 = np.arange(509,521, dtype = "int")
# target_class2 = np.arange(84,125, dtype = "int")    
# no_of_bits = 10
# return_type = 'mean_std'
# answer = Background_Generator.hamming_distance_comparison(target_class1,target_class2,no_of_bits,return_type)
# print(answer)

#------------------------------------------------------------------------------
# #checking timing for hamming_matrix_generation
# Background_Generator.default_setup()
# starttime = time.time()
# pre_screened_hammings_df = Background_Generator.hamming_matrix_generation()
# endtime = time.time()
# print("runtime = {} seconds".format(endtime - starttime))
# print(pre_screened_hammings_df)

#-----------------------------------------------------------------------
#hamming matrix backup code

       # #set range column to be all possible decimal digits
       # hamming_df = pd.DataFrame({"Range":range_binary_df.columns})
       # # test_hamming_df = pd.DataFrame({"Range":range_binary_df.columns})
       # print("finding Hamming distance for...",end = " ")
       # #calculate the hamming distance for target x all range values
       # # holding_dict = {}
       # # array_length = len(range_binary_df.columns)
       # # hamming_array = np.zeros(array_length,dtype=int)
       # for t_no in target_binary_df.columns:
       #     t_no_hamming_holder = []
           
       #     # array_index = 0
       #     print(t_no,end=" ")
       #     for r_no in range_binary_df.columns:
       #         temp_compare = target_binary_df.loc\
       #                         [target_binary_df[t_no] != range_binary_df[r_no],t_no]
       #         temp_hamming = len(temp_compare)
       #         # hamming_array[array_index] = temp_hamming
       #         # array_index += 1
       #         t_no_hamming_holder.append(temp_hamming)
       #     # hamming_df[t_no] = hamming_array
       #     hamming_df[t_no] = t_no_hamming_holder
       #     # holding_dict.update({t_no:t_no_hamming_holder})
       #     # holding_dict.update({t_no:hamming_array})