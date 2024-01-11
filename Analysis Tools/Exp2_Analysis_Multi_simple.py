# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 2022

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
from statsmodels.stats.anova import AnovaRM

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m+h, m-h

#cme_list = ['a_SER50G50W50_','b_SER500G500W500_','c_SER2500G2500W2500_','d_SER5000G5000W5000_','e_SER25000G25000W25000_','f_SER25000G25000W25000_']
cme_list = ['a_SER10G10W0_BKGD_RI20']

for current_cme in cme_list:
    CI = 0.9 #confidence interval
    rounded = 3
    first_schedule_post_training = 1 #initial schedule = 1, not 0
    exp_name = "Exp2-2"
    crit_name_element = current_cme
    subset_range = False
    ss_start = 1500
    ss_end = 20500
    
    
    if subset_range == True: 
        export_file_name = f'{exp_name}_{crit_name_element}_subset({ss_start}_{ss_end})_analysis_v2.xlsx'
    else:      
        export_file_name = f'{exp_name}_{crit_name_element}_analysis_v2.xlsx'
    export_folder = f"{exp_name}_data_analysis" 
    export_path = str(Path(f"C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/Dissertation Testing/{exp_name} Results/{export_folder}/{export_file_name}"))
    raw_data_folder = f"{exp_name}_raw_data"
    raw_data_path = str(Path(f"C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/Dissertation Testing/{exp_name} Results/{raw_data_folder}"))
    # 
    file_list = glob.glob(f"{raw_data_path}/*{crit_name_element}*.csv")
    
    # print(file_list)
    matching_reps = pd.DataFrame([], columns=['rep','a','b','PVAF'])
    se_plus_holder_holder = pd.DataFrame([])
    ext_holder_holder = pd.DataFrame([])
    first_file = True
    print(f'file list length = {len(file_list)}')
    if len(file_list) == 0:
        print('no files found!')
        sys.exit()
        
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
        sched = 1
        bx_name = 'bx_' + str(rep_num)
        r_name = 'r_' + str(rep_num)
        rep_name = 'rep_' + str(rep_num)
        sum_holder = pd.DataFrame([], columns=['sched',r_name,bx_name])
        se_plus_holder = pd.DataFrame([])
        ext_holder = pd.DataFrame([])
     
        # print(f'sched_max = {sched_max}')                          
        while sched <= sched_max:
        # print(f'data type = {type(temp_data)}')
            if subset_range == True:
                sched_r1 = temp_data.loc[temp_data["schedule"] == sched, "R1"][ss_start:ss_end].sum()
                
                sched_b1 = temp_data.loc[temp_data["schedule"] == sched, "B1"][ss_start:ss_end].sum()
                
            else:
                sched_r1 = temp_data.loc[temp_data["schedule"] == sched, "R1"].sum()
                
                sched_b1 = temp_data.loc[temp_data["schedule"] == sched, "B1"].sum()
               
            
            # print(f'B1 Sum = {sched_b1}')
            # sum per schedule 
            temp_df = pd.DataFrame([[sched,sched_r1,sched_b1]], \
                                    columns=['sched',r_name,bx_name])
            # temp_df = pd.DataFrame([[sched,sched_r1,sched_b1]], \
            #                        columns=['sched','R1','B1'])
            
            sum_holder = sum_holder.append(temp_df)
            sched += 1
       
        # se_plus_holder[rep_name] = sum_holder.loc[sum_holder["sched"] == 2, bx_name]
        # se_plus_holder = se_plus_holder[rep_name].append(sum_holder.loc[sum_holder["sched"] == 2, bx_name])
        # se_plus_holder = se_plus_holder[rep_name].append(sum_holder.loc[sum_holder["sched"] == 4, bx_name])
        # se_plus_holder.loc[2,[rep_name]] = sum_holder.loc[sum_holder["sched"] == 2, bx_name]
        # print(sum_holder.loc[sum_holder["sched"] == 2, bx_name])
    
        # print(sum_holder.head(10))
        first_set = True
        for s in range(int(first_schedule_post_training),int(sched_max),2):
            if first_set:
                first_set = False
                # print(f's = {s}')
                se_plus_holder = sum_holder.loc[sum_holder["sched"] == s, bx_name]
                ext_holder = sum_holder.loc[sum_holder["sched"] == s+1, bx_name]
                
                # print(se_plus_holder.head())
            else:
                # print(f's = {s}')
                
                se_plus_holder = se_plus_holder.append(sum_holder.loc[sum_holder["sched"] == s, bx_name])
                ext_holder = ext_holder.append(sum_holder.loc[sum_holder["sched"] == s+1, bx_name])
                # print(se_plus_holder.head())
        
        se_plus_holder.reset_index()
        ext_holder.reset_index()
        
        if first_file == True:
            first_file = False
            sum_holder_holder = sum_holder
            sum_holder_holder.set_index('sched')
            se_plus_holder_holder[rep_name] = pd.DataFrame({rep_name:list(se_plus_holder)})
            ext_holder_holder[rep_name] = pd.DataFrame({rep_name:list(ext_holder)})
            # behavior_holder_holder = pd.DataFrame(sum_holder[bx_name])
            
            # print(se_plus_holder_holder.head())
            # print(ext_holder_holder.head())
        else:   
            # sum_holder_holder = pd.concat([sum_holder_holder, sum_holder], axis=1, join="outer")    
            sum_holder_holder = sum_holder_holder.join(sum_holder.set_index('sched'),on='sched')
            # se_temp = pd.DataFrame({rep_name:list(ext_holder)})
            # se_plus_holder_holder[rep_name] = pd.DataFrame({rep_name:list(se_plus_holder)})
            # ext_holder_holder[rep_name] = pd.DataFrame({rep_name:list(ext_holder)})
            se_plus_holder_holder[rep_name] = pd.DataFrame({rep_name:list(se_plus_holder)})
            ext_holder_holder[rep_name] = pd.DataFrame({rep_name:list(ext_holder)})
            # print(se_plus_holder_holder.head())
            # print(ext_holder_holder.head())
            # se_temp = pd.DataFrame({rep_name:list(se_plus_holder)})
            # ext_temp = pd.DataFrame({rep_name:list(ext_holder)})
            # se_plus_holder_holder = se_plus_holder_holder.join(se_temp)
            # ext_holder_holder = se_plus_holder_holder.join(ext_temp)
            # behavior_holder_holder[bx_name] = sum_holder[bx_name]
        
        # matching_data = pd.DataFrame([], columns=['sched','log(b1/b2)','log(r1/r2)'])
        [rows,col] = sum_holder.shape
        # df.to_numpy().sum()
    
    
        
    stats_data = pd.DataFrame([],columns=['mean','sem','CI+','CI-','stdev','max','min'])
    stats_ext_data = pd.DataFrame([],columns=['mean','sem','CI+','CI-','stdev','max','min'])
    
    #se per row
    max_index = se_plus_holder_holder.index.values.max()
    for se_row in range(0,max_index+1):
    
        temp_values = se_plus_holder_holder.iloc[se_row]
        # print(temp_values)
        se_plus_values = np.ndarray.flatten(temp_values.to_numpy())
        # se_plus_values = np.ndarray.flatten(se_plus_holder_holder[se_row].to_numpy())
        index_name = str(se_row) + '_SE+'
        # schedule = behavior_holder_holder.iloc[sched_row]
        [a_mean,a_CI_plus,a_CI_minus] = mean_confidence_interval(se_plus_values,confidence = CI)
        a_stdev = scipy.stats.tstd(se_plus_values)
        a_sem = scipy.stats.sem(se_plus_values)
        a_max = se_plus_values.max()
        a_min = se_plus_values.min()
        # print("")
        # print(f'a(mean) = {round(a_mean,3)}, CI+ = {round(a_CI_plus,3)}, CI- = {round(a_CI_minus,3)}')
        # print(f'a(stdev) = {round(a_stdev,3)}, max = {round(a_max,3)}, min = {round(a_min,3)}')
        # print(f'a_CI_plus = {a_CI_plus}')
        # print(f'type - a_CI_plus = {type(a_CI_plus)}')
        rounded_a = round(a_mean,rounded)
        rounded_a_CI_plus = round(a_CI_plus,rounded)
        rounded_a_CI_minus = round(a_CI_minus,rounded)
        rounded_a_sem = round(a_sem,rounded)
        rounded_a_stdev = round(a_stdev,rounded)
        rounded_a_max = round(a_max,rounded)
        rounded_a_min = round(a_min,rounded)
        
        a_stats_data = pd.DataFrame([[rounded_a,rounded_a_sem,rounded_a_CI_plus,rounded_a_CI_minus, \
                                    rounded_a_stdev,rounded_a_max,rounded_a_min]], index =[index_name], \
                                  columns=['mean','sem','CI+','CI-','stdev','max','min'])
        
        stats_data = stats_data.append(a_stats_data)    
    
    #ext per row
    max_index = ext_holder_holder.index.values.max()
    for se_row in range(0,max_index+1):
    
        temp_values = ext_holder_holder.iloc[se_row]
        # print(temp_values)
        ext_values = np.ndarray.flatten(temp_values.to_numpy())
        # se_plus_values = np.ndarray.flatten(se_plus_holder_holder[se_row].to_numpy())
        index_name = str(se_row) + '_SE-'
        # schedule = behavior_holder_holder.iloc[sched_row]
        [a_mean,a_CI_plus,a_CI_minus] = mean_confidence_interval(ext_values,confidence = CI)
        a_stdev = scipy.stats.tstd(ext_values)
        a_sem = scipy.stats.sem(ext_values)
        a_max = ext_values.max()
        a_min = ext_values.min()
        # print("")
        # print(f'a(mean) = {round(a_mean,3)}, CI+ = {round(a_CI_plus,3)}, CI- = {round(a_CI_minus,3)}')
        # print(f'a(stdev) = {round(a_stdev,3)}, max = {round(a_max,3)}, min = {round(a_min,3)}')
        # print(f'a_CI_plus = {a_CI_plus}')
        # print(f'type - a_CI_plus = {type(a_CI_plus)}')
        rounded_a = round(a_mean,rounded)
        rounded_a_CI_plus = round(a_CI_plus,rounded)
        rounded_a_CI_minus = round(a_CI_minus,rounded)
        rounded_a_sem = round(a_sem,rounded)
        rounded_a_stdev = round(a_stdev,rounded)
        rounded_a_max = round(a_max,rounded)
        rounded_a_min = round(a_min,rounded)
        
        a_stats_data = pd.DataFrame([[rounded_a,rounded_a_sem,rounded_a_CI_plus,rounded_a_CI_minus, \
                                    rounded_a_stdev,rounded_a_max,rounded_a_min]], index =[index_name], \
                                  columns=['mean','sem','CI+','CI-','stdev','max','min'])
        
        stats_ext_data = stats_ext_data.append(a_stats_data)   
        # print(stats_ext_data)
    #se combined
    se_plus_values = np.ndarray.flatten(se_plus_holder_holder.to_numpy())
    
    # schedule = behavior_holder_holder.iloc[sched_row]
    [a_mean,a_CI_plus,a_CI_minus] = mean_confidence_interval(se_plus_values,confidence = CI)
    a_stdev = scipy.stats.tstd(se_plus_values)
    a_sem = scipy.stats.sem(se_plus_values)
    a_max = se_plus_values.max()
    a_min = se_plus_values.min()
    # print("")
    # print(f'a(mean) = {round(a_mean,3)}, CI+ = {round(a_CI_plus,3)}, CI- = {round(a_CI_minus,3)}')
    # print(f'a(stdev) = {round(a_stdev,3)}, max = {round(a_max,3)}, min = {round(a_min,3)}')
    # print(f'a_CI_plus = {a_CI_plus}')
    # print(f'type - a_CI_plus = {type(a_CI_plus)}')
    rounded_a = round(a_mean,rounded)
    rounded_a_CI_plus = round(a_CI_plus,rounded)
    rounded_a_CI_minus = round(a_CI_minus,rounded)
    rounded_a_sem = round(a_sem,rounded)
    rounded_a_stdev = round(a_stdev,rounded)
    rounded_a_max = round(a_max,rounded)
    rounded_a_min = round(a_min,rounded)
    
    a_stats_data = pd.DataFrame([[rounded_a,rounded_a_sem,rounded_a_CI_plus,rounded_a_CI_minus, \
                                rounded_a_stdev,rounded_a_max,rounded_a_min]], index =['all_se+'], \
                              columns=['mean','sem','CI+','CI-','stdev','max','min'])
    
    stats_data = stats_data.append(a_stats_data)
        
    ext_values = np.ndarray.flatten(ext_holder_holder.to_numpy())
    
    # schedule = behavior_holder_holder.iloc[sched_row]
    [b_mean,b_CI_plus,b_CI_minus] = mean_confidence_interval(np.ndarray.flatten(ext_values),confidence = CI)
    b_stdev = scipy.stats.tstd(ext_values)
    b_sem = scipy.stats.sem(ext_values)
    b_max = ext_values.max()
    b_min = ext_values.min()
    # print("")
    # print(f'a(mean) = {round(a_mean,3)}, CI+ = {round(a_CI_plus,3)}, CI- = {round(a_CI_minus,3)}')
    # print(f'a(stdev) = {round(a_stdev,3)}, max = {round(a_max,3)}, min = {round(a_min,3)}')
    
    rounded_b = round(b_mean,rounded)
    rounded_b_CI_plus = round(b_CI_plus,rounded)
    rounded_b_CI_minus = round(b_CI_minus,rounded)
    rounded_b_sem = round(b_sem,rounded)
    rounded_b_stdev = round(b_stdev,rounded)
    rounded_b_max = round(b_max,rounded)
    rounded_b_min = round(b_min,rounded)
    
    b_stats_data = pd.DataFrame([[rounded_b,rounded_b_sem,rounded_b_CI_plus,rounded_b_CI_minus, \
                                rounded_b_stdev,rounded_b_max,rounded_b_min]], index =['all_ext'], \
                              columns=['mean','sem','CI+','CI-','stdev','max','min'])
    
    stats_ext_data = stats_ext_data.append(b_stats_data)
    ###############################################################################
    #ANOVA attempt:
    # se_plus_holder_holder
    # # ext_holder_holder
    
    # ANOVA_base = se_plus_holder_holder.append(ext_holder_holder)
    # ANOVA_base.reset_index(inplace=True)
    
    # t_anova_base = ANOVA_base.transpose(copy=True)
    # t_anova_base = t_anova_base.rename(columns = {'index':'subject_id'})
    
    # anova_results = AnovaRM(t_anova_base, 'RT', 'subject_id', within=['TrialType'], aggregate_func='mean')
    # # res = AnovaRM(flanks, 'RT', 'SubID', within=['TrialType'], aggregate_func='mean')
    
    # print(res.fit())
    
    # print(f'{t_anova_base.head()}')
    
    ###############################################################################
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(export_path, engine='xlsxwriter')
    
    # Write each dataframe to a different worksheet.
    sum_holder_holder.to_excel(writer, sheet_name='all_data')
    se_plus_holder_holder.to_excel(writer, sheet_name='SE_only')
    ext_holder_holder.to_excel(writer, sheet_name='EXT_only')
    stats_data.to_excel(writer, sheet_name='se_plus_combined_stats')
    stats_ext_data.to_excel(writer, sheet_name='ext_combined_stats')
    
    
    # Close the Pandas Excel writer and output the Excel file.
    writer.close()
