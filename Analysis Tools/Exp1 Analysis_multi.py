# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 12:08:02 2022

@author: Cyrus
"""
import scipy.stats
import math
import numpy as np
import pandas as pd
import glob
import sys
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
exp_name = "Exp1-2"
crit_name_element = "POP200_BKGD_RI04_RM20r"
sched_start = 3
subset_range = False
ss_start = 1500
ss_end = 20500

if subset_range == True: 
    export_file_name = f'{exp_name}_{crit_name_element}_subset({ss_start}_{ss_end})_analysis.xlsx'
else:      
    export_file_name = f'{exp_name}_{crit_name_element}_analysis.xlsx'
export_folder = f"{exp_name}_data_analysis" 
export_path = str(Path(f"C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/Dissertation Testing - Initial Inputs and Results/{exp_name} Results/{export_folder}/{export_file_name}"))
raw_data_folder = f"{exp_name}_raw_data"
raw_data_path = str(Path(f"C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/Dissertation Testing - Initial Inputs and Results/{exp_name} Results/{raw_data_folder}"))
# 
file_list = glob.glob(f"{raw_data_path}/*{crit_name_element}*.csv")
if not(file_list):
    print(f' \n The file list based on {crit_name_element} is empty!')
    sys.exit()
    
# print(f'file_list = {file_list}')
matching_reps = pd.DataFrame([], columns=['rep','a','b','PVAF'])
first_file = True
first_matching = True
for input_file in file_list:
    # print(f'input_file = {input_file}')
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
        raise
    except:
        raise
        
    sched_max = temp_data["schedule"].max()
    
    b1_name = 'b1_' + str(rep_num)
    b2_name = 'b2_' + str(rep_num)
    r1_name = 'r1_' + str(rep_num)
    r2_name = 'r2_' + str(rep_num)
    
    sum_holder = pd.DataFrame([], columns=['sched',r1_name,r2_name,b1_name,b2_name])
    
    # sum_holder = pd.DataFrame([], columns=['sched','R1','R2','B1','B2'])
    # print("")  
    # print(f'sched_max = {sched_max}')                          
    sched = sched_start
    while sched <= sched_max:
    # print(f'data type = {type(temp_data)}')
        if subset_range == True:
            sched_r1 = temp_data.loc[temp_data["schedule"] == sched, "R1"][ss_start:ss_end].sum()
            sched_r2 = temp_data.loc[temp_data["schedule"] == sched, "R2"][ss_start:ss_end].sum()
            sched_b1 = temp_data.loc[temp_data["schedule"] == sched, "B1"][ss_start:ss_end].sum()
            sched_b2 = temp_data.loc[temp_data["schedule"] == sched, "B2"][ss_start:ss_end].sum()
        else:
            sched_r1 = temp_data.loc[temp_data["schedule"] == sched, "R1"].sum()
            sched_r2 = temp_data.loc[temp_data["schedule"] == sched, "R2"].sum()
            sched_b1 = temp_data.loc[temp_data["schedule"] == sched, "B1"].sum()
            sched_b2 = temp_data.loc[temp_data["schedule"] == sched, "B2"].sum()
        
        # print(f'B1 Sum = {sched_b1}')
        # sum per schedule 

        temp_df = pd.DataFrame([[sched,sched_r1,sched_r2,sched_b1,sched_b2]], \
                               columns=['sched',r1_name,r2_name,b1_name,b2_name])
        
        sum_holder = sum_holder.append(temp_df)
        sched += 1
    
    if first_file == True:
        first_file = False
        sum_holder_holder = sum_holder
        sum_holder_holder.set_index('sched')
        # behavior_holder_holder = pd.DataFrame(sum_holder[bx_name])
        # print(sum_holder_holder.head())
        # print(behavior_holder_holder.head(1))
        # print(type(sum_holder))
        # print(type(sum_holder_holder))
    else:   
        # sum_holder_holder = pd.concat([sum_holder_holder, sum_holder], axis=1, join="outer")    
        sum_holder_holder = sum_holder_holder.join(sum_holder.set_index('sched'),on='sched')
        # print(type(sum_holder_holder))
        # print(sum_holder_holder.head())
        # behavior_holder_holder[bx_name] = sum_holder[bx_name]
    
    # print(sum_holder)
    
    [rows,col] = sum_holder.shape
    
    #new frame log(b1/b2),log(r1/r2) by schedule
    # print(f'sum_holder = {sum_holder}')
    b_log_name = 'log(b1/b2)_' + str(rep_num)
    r_log_name = 'log(r1/r2)_' + str(rep_num)
    matching_data = pd.DataFrame([], columns=['sched',b_log_name,r_log_name])
    for sched_row in range(sched_start,rows+1):
        
        b1 = sum_holder.loc[sum_holder["sched"] == sched_row, b1_name]
        b2 = sum_holder.loc[sum_holder["sched"] == sched_row, b2_name]
        r1 = sum_holder.loc[sum_holder["sched"] == sched_row, r1_name]
        r2 = sum_holder.loc[sum_holder["sched"] == sched_row, r2_name]
        #row_sched = sum_holder['sched'][sched_row]
        # print(f'b1 = {b1}')
        # log (b1/b2)
        # log (r1/r2)
        logb1b2 = math.log10(b1[0]/b2[0])
        logr1r2 = math.log10(r1[0]/r2[0])
        
        matching_temp = pd.DataFrame([[sched_row,logb1b2,logr1r2]], \
                                     columns=['sched',b_log_name,r_log_name])
        matching_data = matching_data.append(matching_temp)
    
    
    if first_matching:
        first_matching = False
        matching_data_holder = matching_data
        matching_data_holder.set_index('sched')
        # print(matching_data_holder.head())
        # print(type(matching_data))
        # print(type(matching_data_holder))
    else:
        matching_data_holder = matching_data_holder.join(matching_data.set_index('sched'),on='sched')
        
        # print(matching_data_holder.head())
    #new frame, one line per rep        
    
# =============================================================================
# polyfit method
# =============================================================================
#     #calculate slope (a)
#     # [slope, log_intercept_b] = np.polyfit(matching_data['log(r1/r2)'],matching_data['log(b1/b2)'],1)
#     # print(f'slope = {slope}')
#     
#     #calculate intercept (b)
#     # logb_mean = matching_data['log(b1/b2)'].mean()
#     # logr_mean = matching_data['log(r1/r2)'].mean()
#     # log_intercept_b = logb_mean - logr_mean*slope
#     # intercept_b = 10 ** log_intercept_b
#     # print(f'log_intercept_b = {log_intercept_b}')
#     # print(f'intercept_b = {intercept_b}')
# =============================================================================
    
    #calculate slope (a)
    #calculate intercept (b)
    #calculate PVAF
    
    
 
    
    
    [slope_scipy, intercept_scipy, r_value_scipy, p_value_scipy, std_err_scipy] = \
        scipy.stats.linregress(matching_data[r_log_name],matching_data[b_log_name])
    intercept_b_scipy = 10 ** intercept_scipy
    PVAF = r_value_scipy**2
    # print(f'slope_scipy = {slope_scipy}')
    # print(f'intercept_b_scipy = {intercept_b_scipy}')
    
    # print(f'r_value_scipy^2 = {PVAF}')
    # print(f'std_err_scipy = {std_err_scipy}')
    #New frame = rep, a, b, PVAF (key factor?)
    #build line by line
    
    #new frame = avg a, avg b, avg PVAF +/- SEM
    
    
    matching_reps_temp = pd.DataFrame([[rep_num,slope_scipy,intercept_b_scipy,PVAF]], \
                                      columns=['rep','a','b','PVAF'])
    print("")  
    matching_reps = matching_reps.append(matching_reps_temp)
    
print(matching_reps)


stats_data = pd.DataFrame([],columns=['mean','sem','CI+','CI-','stdev','max','min'])


# a set #######################################################################
[a_mean,a_CI_plus,a_CI_minus] = mean_confidence_interval(matching_reps['a'],confidence = CI)
a_stdev = scipy.stats.tstd(matching_reps['a'])
a_sem = scipy.stats.sem(matching_reps['a'])
a_max = matching_reps['a'].max()
a_min = matching_reps['a'].min()
print("")
print(f'a(mean) = {round(a_mean,3)}, CI+ = {round(a_CI_plus,3)}, CI- = {round(a_CI_minus,3)}')
print(f'a(stdev) = {round(a_stdev,3)}, max = {round(a_max,3)}, min = {round(a_min,3)}')

rounded_a = round(a_mean,rounded)
rounded_a_CI_plus = round(a_CI_plus,rounded)
rounded_a_CI_minus = round(a_CI_minus,rounded)
rounded_a_sem = round(a_sem,rounded)
rounded_a_stdev = round(a_stdev,rounded)
rounded_a_max = round(a_max,rounded)
rounded_a_min = round(a_min,rounded)

a_stats_data = pd.DataFrame([[rounded_a,rounded_a_sem,rounded_a_CI_plus,rounded_a_CI_minus, \
                            rounded_a_stdev,rounded_a_max,rounded_a_min]], index =['a'], \
                          columns=['mean','sem','CI+','CI-','stdev','max','min'])

stats_data = stats_data.append(a_stats_data)    

# b set #######################################################################
[b_mean,b_CI_plus,b_CI_minus] = mean_confidence_interval(matching_reps['b'],confidence = CI)
b_stdev = scipy.stats.tstd(matching_reps['b'])
b_sem = scipy.stats.sem(matching_reps['b'])
b_max = matching_reps['b'].max()
b_min = matching_reps['b'].min()

rounded_b = round(b_mean,rounded)
rounded_b_CI_plus = round(b_CI_plus,rounded)
rounded_b_CI_minus = round(b_CI_minus,rounded)
rounded_b_sem = round(b_sem,rounded)
rounded_b_stdev = round(b_stdev,rounded)
rounded_b_max = round(b_max,rounded)
rounded_b_min = round(b_min,rounded)

b_stats_data = pd.DataFrame([[rounded_b,rounded_b_sem,rounded_b_CI_plus,rounded_b_CI_minus, \
                            rounded_b_stdev,rounded_b_max,rounded_b_min]], index =['b'], \
                          columns=['mean','sem','CI+','CI-','stdev','max','min'])

stats_data = stats_data.append(b_stats_data)    

# PVAF set ####################################################################
[p_mean,p_CI_plus,p_CI_minus] = mean_confidence_interval(matching_reps['PVAF'],confidence = CI)
p_stdev = scipy.stats.tstd(matching_reps['PVAF'])
p_sem = scipy.stats.sem(matching_reps['PVAF'])
p_max = matching_reps['PVAF'].max()
p_min = matching_reps['PVAF'].min()

rounded_p = round(p_mean,rounded)
rounded_p_CI_plus = round(p_CI_plus,rounded)
rounded_p_CI_minus = round(p_CI_minus,rounded)
rounded_p_sem = round(p_sem,rounded)
rounded_p_stdev = round(p_stdev,rounded)
rounded_p_max = round(p_max,rounded)
rounded_p_min = round(p_min,rounded)

p_stats_data = pd.DataFrame([[rounded_p,rounded_p_sem,rounded_p_CI_plus,rounded_p_CI_minus, \
                            rounded_p_stdev,rounded_p_max,rounded_p_min]], index =['PVAF'], \
                          columns=['mean','sem','CI+','CI-','stdev','max','min'])

stats_data = stats_data.append(p_stats_data)  
###############################################################################






###############################################################################
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(export_path, engine='xlsxwriter')

# Write each dataframe to a different worksheet.
sum_holder_holder.to_excel(writer, sheet_name='sums')
matching_data_holder.to_excel(writer, sheet_name='matching')
matching_reps.to_excel(writer, sheet_name='lin_reg_results')
stats_data.to_excel(writer, sheet_name='stats')

# Close the Pandas Excel writer and output the Excel file.
writer.close()

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