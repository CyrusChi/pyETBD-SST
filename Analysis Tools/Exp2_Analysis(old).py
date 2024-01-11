# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 17:08:34 2022

@author: Cyrus
"""
import scipy.stats
import math
import numpy as np
import pandas as pd
import glob
from pathlib import Path
from os import sep

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m+h, m-h

CI = 0.9 #confidence interval
rounded = 3
exp_name = "Exp2c"
crit_name_element = "POP400_"

transition_range = True #this is always true for right now
transition_set = "odd" # alt: 'even' # for either 70 to Ext, or Ext to 70
#eventually i might want to make a transition_set = 'all' not sure what it
#would be for though.
t_start = 1 # min 1, useful for cutting off any training periods
t_end = 7 # if the number is greater than the number of transitions, then it
          # will end at the final transition.

data_type = ''
data_style = "CR" # or 'kernel', 'chunking' or 'CR' # CR = cumulative record
#kernel might not be necessary
observation_style = "generation" # or "target_hit" 
#target hit may not make sense due to RI style used... in the current version,
#time still ticks even though the target was not hit. 
obs_start = 1 # 1 = first step after transition 
obs_end = 150 #observation period end around the transition 
window_width = 10 # the width of the window for chunking/averaging

total_possible_blocks = math.floor((obs_end - obs_start+1)/window_width)


if transition_range == True: 
    export_file_name = f'{exp_name}_{crit_name_element}_T_subset({t_start}_{t_end}_{transition_set})_analysis.xlsx'
else:      
    export_file_name = f'{exp_name}_{crit_name_element}_analysis.xlsx'
export_folder = f"{exp_name}_data_analysis" 
export_path = str(Path(f"C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/Dissertation Testing - Initial Inputs and Results/{exp_name} Results/{export_folder}/{export_file_name}"))
raw_data_folder = f"{exp_name}_raw_data"
raw_data_path = str(Path(f"C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/Dissertation Testing - Initial Inputs and Results/{exp_name} Results/{raw_data_folder}"))
# 
file_list = glob.glob(f"{raw_data_path}/*{crit_name_element}*.csv")

# print(file_list)
# matching_reps = pd.DataFrame([], columns=['rep','a','b','PVAF'])

for input_file in file_list:
    
    start_index = input_file.rfind(sep) + 1
    
    
    end_index = input_file.rfind(".")
    key_name = input_file[start_index:end_index]

    
    #find rep
    rep_end_index = input_file.rfind("_")
    rep_start_index = input_file.rfind("rep")+3
    rep_num = int(input_file[rep_start_index:rep_end_index])
    print(f'rep_num = {rep_num}')
    try:
       temp_data = pd.read_csv(input_file)
    except FileNotFoundError:
           print("raw data file not found!")      
    
    sched_max = temp_data["schedule"].max()
    transition_max = sched_max-1
    sched = 1
    
    if transition_range == True:
        if t_end > transition_max:
            print(f't_end ({t_end}) greater than transition_max ({transition_max})')
            print('t_end will be set to tranistion max')
            t_end == transition_max
        if t_start < 1:
            KeyError(f't_start ({t_start}) cannot be less than 1!)')
        if t_start > t_end:
            KeyError(f't_start ({t_start}) cannot be greater than t_end({t_end})!)')

    #create tranistion list
    #transition loop
    #all transition data loop
        #per transition
            #data type 
# temp_data[temp_data['schedule']==1].index.max()
  

    
# obs_start = 1; % 1 = first step after transition 
# obs_end = 150; %observation period end around the transition 

# analysis_type = 'chunking'; % 'gaussian' = moving average w/ gaussian, 'chunks'
# windowWidth = 5; %Kernel length - 5, based on corrado 2005 data (gaussian)
# c_windowWidth = 10; %the width of the window for chunking
# pre_block = 1;
# total_possible_blocks = floor((obs_end - obs_start+1)/c_windowWidth);

    
#     sum_holder = pd.DataFrame([], columns=['sched','R1','R2','B1','B2'])
#     # print("")  
#     # print(f'sched_max = {sched_max}')                          
#     while sched <= sched_max:
#     # print(f'data type = {type(temp_data)}')
#         if subset_range == True:
#             sched_r1 = temp_data.loc[temp_data["schedule"] == sched, "R1"][ss_start:ss_end].sum()
#             sched_r2 = temp_data.loc[temp_data["schedule"] == sched, "R2"][ss_start:ss_end].sum()
#             sched_b1 = temp_data.loc[temp_data["schedule"] == sched, "B1"][ss_start:ss_end].sum()
#             sched_b2 = temp_data.loc[temp_data["schedule"] == sched, "B2"][ss_start:ss_end].sum()
#         else:
#             sched_r1 = temp_data.loc[temp_data["schedule"] == sched, "R1"].sum()
#             sched_r2 = temp_data.loc[temp_data["schedule"] == sched, "R2"].sum()
#             sched_b1 = temp_data.loc[temp_data["schedule"] == sched, "B1"].sum()
#             sched_b2 = temp_data.loc[temp_data["schedule"] == sched, "B2"].sum()
        
#         # print(f'B1 Sum = {sched_b1}')
#         # sum per schedule 

#         temp_df = pd.DataFrame([[sched,sched_r1,sched_r2,sched_b1,sched_b2]], \
#                                columns=['sched','R1','R2','B1','B2'])
        
#         sum_holder = sum_holder.append(temp_df)
#         sched += 1
    
#     matching_data = pd.DataFrame([], columns=['sched','log(b1/b2)','log(r1/r2)'])
#     [rows,col] = sum_holder.shape
    
#     #new frame log(b1/b2),log(r1/r2) by schedule
#     # print(f'sum_holder = {sum_holder}')
#     for sched_row in range(1,rows+1):
        
#         b1 = sum_holder.loc[sum_holder["sched"] == sched_row, "B1"]
#         b2 = sum_holder.loc[sum_holder["sched"] == sched_row, "B2"]
#         r1 = sum_holder.loc[sum_holder["sched"] == sched_row, "R1"]
#         r2 = sum_holder.loc[sum_holder["sched"] == sched_row, "R2"]
#         #row_sched = sum_holder['sched'][sched_row]
#         # print(f'b1 = {b1}')
#         # log (b1/b2)
#         # log (r1/r2)
#         logb1b2 = math.log10(b1[0]/b2[0])
#         logr1r2 = math.log10(r1[0]/r2[0])
        
#         matching_temp = pd.DataFrame([[sched_row,logb1b2,logr1r2]], \
#                                      columns=['sched','log(b1/b2)','log(r1/r2)'])
#         matching_data = matching_data.append(matching_temp)
    
#     #new frame, one line per rep        
    
# # =============================================================================
# # polyfit method
# # =============================================================================
# #     #calculate slope (a)
# #     # [slope, log_intercept_b] = np.polyfit(matching_data['log(r1/r2)'],matching_data['log(b1/b2)'],1)
# #     # print(f'slope = {slope}')
# #     
# #     #calculate intercept (b)
# #     # logb_mean = matching_data['log(b1/b2)'].mean()
# #     # logr_mean = matching_data['log(r1/r2)'].mean()
# #     # log_intercept_b = logb_mean - logr_mean*slope
# #     # intercept_b = 10 ** log_intercept_b
# #     # print(f'log_intercept_b = {log_intercept_b}')
# #     # print(f'intercept_b = {intercept_b}')
# # =============================================================================
    
#     #calculate slope (a)
#     #calculate intercept (b)
#     #calculate PVAF
    
    
 
    
    
#     [slope_scipy, intercept_scipy, r_value_scipy, p_value_scipy, std_err_scipy] = \
#         scipy.stats.linregress(matching_data['log(r1/r2)'],matching_data['log(b1/b2)'])
#     intercept_b_scipy = 10 ** intercept_scipy
#     PVAF = r_value_scipy**2
#     # print(f'slope_scipy = {slope_scipy}')
#     # print(f'intercept_b_scipy = {intercept_b_scipy}')
    
#     # print(f'r_value_scipy^2 = {PVAF}')
#     # print(f'std_err_scipy = {std_err_scipy}')
#     #New frame = rep, a, b, PVAF (key factor?)
#     #build line by line
    
#     #new frame = avg a, avg b, avg PVAF +/- SEM
    
    
#     matching_reps_temp = pd.DataFrame([[rep_num,slope_scipy,intercept_b_scipy,PVAF]], \
#                                       columns=['rep','a','b','PVAF'])
#     print("")  
#     matching_reps = matching_reps.append(matching_reps_temp)
    
# print(matching_reps)


# stats_data = pd.DataFrame([],columns=['mean','sem','CI+','CI-','stdev','max','min'])


# # a set #######################################################################
# [a_mean,a_CI_plus,a_CI_minus] = mean_confidence_interval(matching_reps['a'],confidence = CI)
# a_stdev = scipy.stats.tstd(matching_reps['a'])
# a_sem = scipy.stats.sem(matching_reps['a'])
# a_max = matching_reps['a'].max()
# a_min = matching_reps['a'].min()
# print("")
# print(f'a(mean) = {round(a_mean,3)}, CI+ = {round(a_CI_plus,3)}, CI- = {round(a_CI_minus,3)}')
# print(f'a(stdev) = {round(a_stdev,3)}, max = {round(a_max,3)}, min = {round(a_min,3)}')

# rounded_a = round(a_mean,rounded)
# rounded_a_CI_plus = round(a_CI_plus,rounded)
# rounded_a_CI_minus = round(a_CI_minus,rounded)
# rounded_a_sem = round(a_sem,rounded)
# rounded_a_stdev = round(a_stdev,rounded)
# rounded_a_max = round(a_max,rounded)
# rounded_a_min = round(a_min,rounded)

# a_stats_data = pd.DataFrame([[rounded_a,rounded_a_sem,rounded_a_CI_plus,rounded_a_CI_minus, \
#                             rounded_a_stdev,rounded_a_max,rounded_a_min]], index =['a'], \
#                           columns=['mean','sem','CI+','CI-','stdev','max','min'])

# stats_data = stats_data.append(a_stats_data)    

# # b set #######################################################################
# [b_mean,b_CI_plus,b_CI_minus] = mean_confidence_interval(matching_reps['b'],confidence = CI)
# b_stdev = scipy.stats.tstd(matching_reps['b'])
# b_sem = scipy.stats.sem(matching_reps['b'])
# b_max = matching_reps['b'].max()
# b_min = matching_reps['b'].min()

# rounded_b = round(b_mean,rounded)
# rounded_b_CI_plus = round(b_CI_plus,rounded)
# rounded_b_CI_minus = round(b_CI_minus,rounded)
# rounded_b_sem = round(b_sem,rounded)
# rounded_b_stdev = round(b_stdev,rounded)
# rounded_b_max = round(b_max,rounded)
# rounded_b_min = round(b_min,rounded)

# b_stats_data = pd.DataFrame([[rounded_b,rounded_b_sem,rounded_b_CI_plus,rounded_b_CI_minus, \
#                             rounded_b_stdev,rounded_b_max,rounded_b_min]], index =['b'], \
#                           columns=['mean','sem','CI+','CI-','stdev','max','min'])

# stats_data = stats_data.append(b_stats_data)    

# # PVAF set ####################################################################
# [p_mean,p_CI_plus,p_CI_minus] = mean_confidence_interval(matching_reps['PVAF'],confidence = CI)
# p_stdev = scipy.stats.tstd(matching_reps['PVAF'])
# p_sem = scipy.stats.sem(matching_reps['PVAF'])
# p_max = matching_reps['PVAF'].max()
# p_min = matching_reps['PVAF'].min()

# rounded_p = round(p_mean,rounded)
# rounded_p_CI_plus = round(p_CI_plus,rounded)
# rounded_p_CI_minus = round(p_CI_minus,rounded)
# rounded_p_sem = round(p_sem,rounded)
# rounded_p_stdev = round(p_stdev,rounded)
# rounded_p_max = round(p_max,rounded)
# rounded_p_min = round(p_min,rounded)

# p_stats_data = pd.DataFrame([[rounded_p,rounded_p_sem,rounded_p_CI_plus,rounded_p_CI_minus, \
#                             rounded_p_stdev,rounded_p_max,rounded_p_min]], index =['PVAF'], \
#                           columns=['mean','sem','CI+','CI-','stdev','max','min'])

# stats_data = stats_data.append(p_stats_data)  
###############################################################################






###############################################################################
# Create a Pandas Excel writer using XlsxWriter as the engine.
# writer = pd.ExcelWriter(export_path, engine='xlsxwriter')

# Write each dataframe to a different worksheet.
# sum_holder.to_excel(writer, sheet_name='sums')
# matching_data.to_excel(writer, sheet_name='matching')
# matching_reps.to_excel(writer, sheet_name='lin_reg_results')
# stats_data.to_excel(writer, sheet_name='stats')

# Close the Pandas Excel writer and output the Excel file.
# writer.close()

# for input_file in file_list:
#     temp_data=None;
# filename = "foo.csv"
# with pd.read_csv(filename) as exp1_file:
#     pass
# C:\Users\Cyrus\Documents\Emory\Lab\Dissertation Explorations\Dissertation Testing - Initial Inputs and Results\Exp1k Results\Exp1k_raw_data 
#     try:
#         temp_data = pd.read_csv(filename)
#     except FileNotFoundError:
#         print("setting file not found!")