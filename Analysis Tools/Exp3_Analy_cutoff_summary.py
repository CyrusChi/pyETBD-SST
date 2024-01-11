# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 10:46:40 2023

Updated 8.26.23
@author: Cyrus

Analysis v4 
for Experiment 3I (stimulus generalization)
can make both individual experiment summaries, as well as a group summary
"""
from natsort import natsorted
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
exp_name = "Exp3I-1"
folder_name = "Exp3I-1"
# crit_name_element = "Exp3I-s4_TRNOWALL_RI10_RM05_MMRNull_"
write_indiviual_summaries = True
write_group_summary = True
training_schedule = 2 #by actual schedule number, NOT index
training_test_range = 200
training_cutoff = 0 #percentage of behaviors on target class. can set to 0 for no cut off.
training_limit = False #Int (typically 30) or False

exp_element = "MMR"
pre_crit_name_element_list = ['RI10_RM05_MMR01_','RI10_RM05_MMR05_','RI10_RM05_MMR10_','RI10_RM05_MMR15_'\
                             ,'RI10_RM05_MMR20_','RI10_RM05_MMR30_','RI10_RM05_MMR40_','RI10_RM05_MMR50_'\
                             ,'RI10_RM05_MMR75_','RI10_RM05_MMR100_','RI10_RM05_MMR500_','RI10_RM05_MMR1000_'\
                             ,'RI10_RM05_MMR2000_','RI10_RM05_MMR5000_','RI10_RM05_MMR10000_','RI10_RM05_MMRNull_']
# crit_name_element_list = ['RI10_RM05_MMR01_','RI10_RM05_MMR05_','RI10_RM05_MMR10_']
# prefix_str = "1_X_WALL_X_BKGD_"
# prefix_str = "1_WALL_X_BKGD_"
# prefix_str = "1_X_WALL_BKGD_"
# prefix_str = "1_WALL_BKGD_"
prefix_list =["1_X_WALL_X_BKGD_","1_WALL_X_BKGD_","1_X_WALL_BKGD_","1_WALL_BKGD_"]
for prefix_str in prefix_list:
    crit_name_element_list = [prefix_str + sub for sub in pre_crit_name_element_list]
    #summary tasks:
    # 1.find and collect unique name element
    # 1.collect means 
    # 2.collect CI
    summary_means = pd.DataFrame([], index=[5,4,3,2,1,0,-1,-2,-3,-4,-5],columns=[])
    summary_confidence_intervals = pd.DataFrame([], index=[5,4,3,2,1,0,-1,-2,-3,-4,-5], columns=[])
    summary_info = pd.DataFrame([], columns=['exp','unique_id','limit_reached','tt_range','pass_crit','pass_count','total_count','avg_test_stdev'])
    #tt_range = train test range
    raw_data_folder = f"{folder_name}_raw_data"
    raw_data_path = str(Path(f"C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/Dissertation Testing - Initial Inputs and Results/{exp_name} Results/{raw_data_folder}"))
    export_folder = f"{folder_name}_data_analysis" 
    
    summary_file_name = f'{exp_name}_{prefix_str}_anal_sum_v1.xlsx'
    summary_export_path = str(Path(f"C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/Dissertation Testing - Initial Inputs and Results/{exp_name} Results/{export_folder}/{summary_file_name}"))
    
    for crit_name_element in crit_name_element_list:
        
        
        export_file_name = f'{exp_name}_{crit_name_element}_analysis_v4.xlsx'
        
        export_path = str(Path(f"C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/Dissertation Testing - Initial Inputs and Results/{exp_name} Results/{export_folder}/{export_file_name}"))
       
        
        # 
        file_list = glob.glob(f"{raw_data_path}/*{crit_name_element}*.csv")
        
        uni_start_index = file_list[0].rfind(exp_element)
        uni_end_index = file_list[0].find("_",uni_start_index)
        unique_element_str = file_list[0][uni_start_index:uni_end_index]
        
        # print(file_list)
        matching_reps = pd.DataFrame([], columns=['rep','a','b','PVAF'])
        sum_holder_holder = pd.DataFrame([], columns=['sched','r_name','bx_name'])
        behavior_holder_holder = pd.DataFrame([], columns=['sched','r_name','bx_name'])
        stats_data = pd.DataFrame([], columns=['sched','r_name','bx_name'])
        training_data = pd.DataFrame([], columns=['rep','limit_reached?','passed?','%','test_range','bx'])
        print(f'number of files to be analyzed: {len(file_list)}')
        first_file = True
        passed_reps = 0
        file_list = natsorted(file_list)
        
        for input_file in file_list:
            
            start_index = input_file.rfind(sep) + 1
            
            
            end_index = input_file.rfind(".")
            key_name = input_file[start_index:end_index]
        
            
            #find rep
            rep_end_index = input_file.rfind("_")
            rep_start_index = input_file.rfind("rep")+3
            rep_num = int(input_file[rep_start_index:rep_end_index])
            # print(input_file)
            print(f'rep_num = {rep_num}')
            try:
               temp_data = pd.read_csv(input_file)
            except FileNotFoundError:
                   print("raw data file not found!")  
            sched_max = temp_data["schedule"].max()
            sched = 1
            bx_name = 'bx_' + str(rep_num)
            r_name = 'r_' + str(rep_num)
            sum_holder = pd.DataFrame([], columns=['sched',r_name,bx_name])
            
            # training_index_max = temp_data.loc[temp_data["schedule"] == training_schedule, "B1"].index.max()
            training_index_len = len(temp_data.loc[temp_data["schedule"] == training_schedule, "B1"])
            training_index_min = training_index_len-training_test_range
            # print(f'rep_num = {rep_num}')
            # print(f'training_index_max = {training_index_max}')
            # print(f'training_index_len = {training_index_len}')
            training_sum = sched_b1 = temp_data.loc[temp_data["schedule"] == training_schedule, "B1"]\
                                                   [training_index_min:training_index_len].sum()
        
            # print(f'training_sum = {training_sum}')
            test_percentage = round(training_sum/training_test_range,2)
            # print(f'training_sum.shape = {training_sum.shape}')
            pass_value = training_cutoff * training_test_range
            
            training_pass = False
            if training_sum >= pass_value:
                passed_reps += 1
                training_pass = True
            else:
                print(f'criteria({pass_value}) failed!({training_sum})')
            if training_limit and passed_reps > training_limit:
                print(f'file({passed_reps}) limit({training_limit}) reached')
                continue
            limit_reached = False
            
            if type(training_limit) == int and training_limit <= passed_reps:
                limit_reached = True
                limit_txt = str(training_limit) + '/' + str(limit_reached)
            elif type(training_limit) == int:
                limit_reached = False
                limit_txt = str(passed_reps) + '/' + str(training_limit) + '/' + str(limit_reached)
            else:
                limit_txt = 'no_limit'
    
            
            temp_training_data = pd.DataFrame([[rep_num,limit_txt,training_pass,test_percentage,training_test_range,\
                                                training_sum]], index =[rep_num],\
                                                columns=['rep','limit_reached?','passed?','%','test_range','bx'])
                
            training_data = training_data.append(temp_training_data)
                # a_stats_data = pd.DataFrame([[rounded_a,rounded_a_sem,rounded_a_CI_plus,rounded_a_CI_minus, \
                #                             rounded_a_stdev,rounded_a_max,rounded_a_min]], index =[sched_row], \
                #                           columns=['mean','sem','CI+','CI-','stdev','max','min'])
            
            if training_pass:
                
                
                # print("")  
                # print(f'sched_max = {sched_max}')                          
                while sched <= sched_max:
                # print(f'data type = {type(temp_data)}')
            
                    sched_r1 = temp_data.loc[temp_data["schedule"] == sched, "R1"].sum()
                    
                    sched_b1 = temp_data.loc[temp_data["schedule"] == sched, "B1"].sum()
                       
                    
                    # print(f'B1 Sum = {sched_b1}')
                    # sum per schedule 
                    
                    temp_df = pd.DataFrame([[sched,sched_r1,sched_b1]], \
                                            columns=['sched',r_name,bx_name])
                    
                    sum_holder = sum_holder.append(temp_df)
            
                    sched += 1
                #pd.concat([df1, df4], axis=1, join="inner")    
                if first_file == True:
                    first_file = False
                    sum_holder_holder = sum_holder
                    sum_holder_holder.set_index('sched')
                    behavior_holder_holder = pd.DataFrame(sum_holder[bx_name])
                    
                    # print(behavior_holder_holder.head(1))
                else:   
                    # sum_holder_holder = pd.concat([sum_holder_holder, sum_holder], axis=1, join="outer")    
                    sum_holder_holder = sum_holder_holder.join(sum_holder.set_index('sched'),on='sched')
                    
                    behavior_holder_holder[bx_name] = sum_holder[bx_name]
                    # print(behavior_holder_holder.head(1))
                #df.set_index('key').join(other.set_index('key'))
                # matching_data = pd.DataFrame([], columns=['sched','log(b1/b2)','log(r1/r2)'])
                # all_data = pd.DataFrame([], columns=['sched'])
                
                [rows,col] = behavior_holder_holder.shape
                
                #rep_num
                # print(f'sum_holder = {sum_holder}')
                #all_data
                #bx data
                #bx data statistics
                stats_data = pd.DataFrame([],columns=['mean','sem','CI+','CI-','stdev','max','min'])
                
                for sched_row in range(0,rows):
                    schedule = behavior_holder_holder.iloc[sched_row]
                    [a_mean,a_CI_plus,a_CI_minus] = mean_confidence_interval(schedule,confidence = CI)
                    a_stdev = scipy.stats.tstd(schedule)
                    a_sem = scipy.stats.sem(schedule)
                    a_max = schedule.max()
                    a_min = schedule.min()
                    # print("")
                    # print(f'a(mean) = {round(a_mean,3)}, CI+ = {round(a_CI_plus,3)}, CI- = {round(a_CI_minus,3)}')
                    # print(f'a(stdev) = {round(a_stdev,3)}, max = {round(a_max,3)}, min = {round(a_min,3)}')
            
                    rounded_a = round(a_mean,rounded)
                    rounded_a_CI_plus = round(a_CI_plus,rounded)
                    rounded_a_CI_minus = round(a_CI_minus,rounded)
                    rounded_a_sem = round(a_sem,rounded)
                    rounded_a_stdev = round(a_stdev,rounded)
                    rounded_a_max = round(a_max,rounded)
                    rounded_a_min = round(a_min,rounded)
            
                    a_stats_data = pd.DataFrame([[rounded_a,rounded_a_sem,rounded_a_CI_plus,rounded_a_CI_minus, \
                                                rounded_a_stdev,rounded_a_max,rounded_a_min]], index =[sched_row], \
                                              columns=['mean','sem','CI+','CI-','stdev','max','min'])
            
                    stats_data = stats_data.append(a_stats_data)  
                
                #the original use of training_schedule is by schedule but here is it by index
                #therefore, the number does NOT need to be incremented by 1
                first_test_schedule = int(training_schedule) 
                last_test_schedule = int(sched_max)
                # temp_data.loc[temp_data["schedule"] == sched, "R1"]
                # print(f'stats_data.shape = {stats_data.shape}')
                # print(first_test_schedule)
                # print(last_test_schedule)
                crit_stdev =stats_data['stdev'][first_test_schedule:last_test_schedule].mean()
                # print(crit_stdev_data)
                #use stats data to create reordered data
                analysis_data = pd.DataFrame([], columns=['count','index','mean','sem','CI'])
                schedule_reorder = [11,10,9,8,7,12,2,3,4,5,6]
                index_list = [5,4,3,2,1,0,-1,-2,-3,-4,-5]
                # print('stats_data')
                # print(stats_data.shape)
                # print(stats_data.head())
                for i in range(len(schedule_reorder)):
                    current_index = schedule_reorder[i]
                    current_row = index_list[i]
                    # print(f'current_index = {current_index}')
                    mean_value = stats_data.iloc[current_index, stats_data.columns.get_indexer(['mean'])].values
                    sem_value = stats_data.iloc[current_index, stats_data.columns.get_indexer(['sem'])].values
                    CIpLus_value = stats_data.iloc[current_index, stats_data.columns.get_indexer(['CI+'])].values
                    CI_value = CIpLus_value - mean_value
                    
                    analysis_temp = pd.DataFrame([[passed_reps,current_row,mean_value[0],sem_value[0],CI_value[0]]],\
                                                  index = [i],\
                                                  columns=['count','index','mean','sem','CI'])
                    
                    analysis_data = analysis_data.append(analysis_temp) 
                    summary_means.loc[summary_means.index[i], unique_element_str] = mean_value[0]
                    summary_confidence_intervals.loc[summary_confidence_intervals.index[i], unique_element_str] = CI_value[0]
                    
                    # df.loc[df.index[someRowNumber], 'New Column Title'] = "some value"
                    
                #collect summary Data
                
                # summary_means[unique_element_str] = analysis_data['mean']
                # summary_confidence_intervals[unique_element_str] = analysis_data['CI']
                
    
            
                # get positive and negative trendlines with linear regression
                #PVAF, alpha, intercept, avg intercept
                intercept_data = pd.DataFrame([], columns=['PVAF','slope','intecept','avg_intercept'])
                positive_x_values = analysis_data.iloc[0:6, analysis_data.columns.get_indexer(['index'])].to_numpy()
                positive_y_values = analysis_data.iloc[0:6, analysis_data.columns.get_indexer(['mean'])].to_numpy()
                # positive_x_values = analysis_data.iloc[0:6, analysis_data.columns.get_indexer(['index'])]
                # positive_y_values = analysis_data.iloc[0:6, analysis_data.columns.get_indexer(['mean'])]
                
                positive_x_values = positive_x_values.reshape(len(positive_x_values))
                positive_y_values = positive_y_values.reshape(len(positive_y_values))
                
                # print(type(positive_x_values))
                # print(positive_x_values.dtype)
                # print(positive_y_values.shape)
                
                [pos_slope, pos_intercept, pos_r_value, pos_p_value, pos_std_err] = \
                    scipy.stats.linregress(positive_x_values.astype(float),positive_y_values.astype(float))
                pos_PVAF = pos_r_value**2
                
                negative_x_values = analysis_data.iloc[5:11, analysis_data.columns.get_indexer(['index'])].values
                negative_y_values = analysis_data.iloc[5:11, analysis_data.columns.get_indexer(['mean'])].values
                
                negative_x_values = negative_x_values.reshape(len(negative_x_values))
                negative_y_values = negative_y_values.reshape(len(negative_y_values))
                
                [neg_slope, neg_intercept, neg_r_value, neg_p_value, neg_std_err] = \
                    scipy.stats.linregress(negative_x_values.astype(float),negative_y_values.astype(float))
                neg_PVAF = neg_r_value**2
                
                avg_intercept = (pos_intercept + neg_intercept)/2
                
                pos_intercept_temp = pd.DataFrame([[pos_PVAF,pos_slope,pos_intercept,avg_intercept]],\
                                              index = ['pos'],\
                                              columns=['PVAF','slope','intecept','avg_intercept'])
                
                neg_intercept_temp = pd.DataFrame([[neg_PVAF,neg_slope,neg_intercept,avg_intercept]],\
                                              index = ['neg'],\
                                              columns=['PVAF','slope','intecept','avg_intercept'])
                    
                intercept_data = intercept_data.append(pos_intercept_temp)     
                intercept_data = intercept_data.append(neg_intercept_temp)     
            # [slope_scipy, intercept_scipy, r_value_scipy, p_value_scipy, std_err_scipy] = \
            #     scipy.stats.linregress(matching_data['log(r1/r2)'],matching_data['log(b1/b2)'])
            # intercept_b_scipy = 10 ** intercept_scipy
            # PVAF = r_value_scipy**2
            # print(f'slope_scipy = {slope_scipy}')
            # print(f'intercept_b_scipy = {intercept_b_scipy}')
            
            # print(f'r_value_scipy^2 = {PVAF}')
            # print(f'std_err_scipy = {std_err_scipy}')
            #New frame = rep, a, b, PVAF (key factor?)
        
        
            #     b1 = stats_data.loc[stats_data["sched"] == stats_data, 'mean']
               
            #     r1 = sum_holder.loc[sum_holder["sched"] == sched_row, "R1"]
             
            #     #row_sched = sum_holder['sched'][sched_row]
            #     # print(f'b1 = {b1}')
            #     # log (b1/b2)
            #     # log (r1/r2)
            #     # logb1b2 = math.log10(b1[0]/b2[0])
            #     # logr1r2 = math.log10(r1[0]/r2[0])
            #     bx_name = 'bx_' + str(rep_num)
            #     r_name = 'r_' + str(rep_num)
            #     all_data_rep_temp = pd.DataFrame([[sched_row,b1,r1]], \
            #                                  columns=['sched',bx_name,r_name])
            #     all_data = all_data.append(all_data_rep_temp)
            
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
            
            
         
            
            
            # [slope_scipy, intercept_scipy, r_value_scipy, p_value_scipy, std_err_scipy] = \
            #     scipy.stats.linregress(matching_data['log(r1/r2)'],matching_data['log(b1/b2)'])
            # intercept_b_scipy = 10 ** intercept_scipy
            # PVAF = r_value_scipy**2
            # print(f'slope_scipy = {slope_scipy}')
            # print(f'intercept_b_scipy = {intercept_b_scipy}')
            
            # print(f'r_value_scipy^2 = {PVAF}')
            # print(f'std_err_scipy = {std_err_scipy}')
            #New frame = rep, a, b, PVAF (key factor?)
            #build line by line
            
            #new frame = avg a, avg b, avg PVAF +/- SEM
            
            
            # matching_reps_temp = pd.DataFrame([[rep_num,slope_scipy,intercept_b_scipy,PVAF]], \
            #                                   columns=['rep','a','b','PVAF'])
            # print("")  
            # matching_reps = matching_reps.append(matching_reps_temp)
            
        # print(matching_reps)
        
        #behavior_holder_holder
        
        
        
        # a set #######################################################################
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
        
        # b set #######################################################################
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
        
        # PVAF set ####################################################################
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
    
        temp_summary_info = pd.DataFrame([[exp_name,unique_element_str,limit_txt,training_test_range,training_cutoff,passed_reps,len(file_list),crit_stdev]],\
                                         columns=['exp','unique_id','limit_reached','tt_range','pass_crit','pass_count','total_count','avg_test_stdev'])
        
        summary_info = summary_info.append(temp_summary_info)
        
        print(f'passed_reps = {passed_reps}')
        print('')
        if passed_reps == 0:
            print(f'no individual excel file created for {crit_name_element}')
            print('no passing reps')
            continue
            
            
                ###############################################################################
        if write_indiviual_summaries:
            # Create a Pandas Excel writer using XlsxWriter as the engine.
            writer = pd.ExcelWriter(export_path, engine='xlsxwriter')
            
            training_data.to_excel(writer, sheet_name='training_data')
            # Write each dataframe to a different worksheet.
            sum_holder_holder.to_excel(writer, sheet_name='all_data')
            # behavior_holder_holder['sched'] = sum_holder['sched']
            # behavior_holder_holder.set_index('sched')
            
            behavior_holder_holder.to_excel(writer, sheet_name='bx_only')
            # matching_data.to_excel(writer, sheet_name='matching')
            # matching_reps.to_excel(writer, sheet_name='lin_reg_results')
            stats_data.to_excel(writer, sheet_name='stats')
            
            analysis_data.to_excel(writer, sheet_name='ordered')
            
            intercept_data.to_excel(writer, sheet_name='intercept')
            
            # Close the Pandas Excel writer and output the Excel file.
            writer.close()
    
    if write_group_summary:
        writer = pd.ExcelWriter(summary_export_path, engine='xlsxwriter')
        
        summary_means.to_excel(writer, sheet_name='means')
        summary_confidence_intervals.to_excel(writer, sheet_name='CI')
        summary_info.to_excel(writer, sheet_name='info')
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