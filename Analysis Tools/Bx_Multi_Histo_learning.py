# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 20:05:19 2023

Created to look at behavior populations over multiple AOs (schedule, SEs)

Schedule Range:
1. All schedules
2. specific schedule(s)

SE Range:
1. all SE
2. specific SE
3. specific SE type(s)

generation range:
1. Entire Schedule
2. Specified range within a schedule
    2a. based on starting and ending gen
3. Entire experiment
4. Bx histogram for specific SE

Analysis Style:
1. absolute histogram (bin = 40)
2. relative histogram (bin = 40)

Statistical measures (for all AOs):
1. average per bin 
2. standard deviation per bin
3. standard error per bin
4. median per bin (optional)

Output:
1. specific SE Bx Pop stream over schedule/gen
2. specific SE/SE group statisitical measures
3. specific SE/SE group statisitical measures over a certain range
@author: Cyrus
"""
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from IPython import display
import matplotlib as mpl 
# from matplotlib.patches import Polygon

# import ffmpy

import scipy.stats
# import math


import glob
from pathlib import Path
from os import sep
# mpl.use("Agg")
# mpl.rcParams['animation.ffmpeg_path'] = r'C:\Users\Cyrus\Documents\Python_stuff\ffmpeg\bin\ffmpeg.exe'

#Inputs########################################################################
anchor_list = [0]
    
for anchor in anchor_list:

    #file information
    exp_name = "Exp2q"
    folder_name = "Exp2q"
    crit_name_element = "G10_R10_W0"
    export_folder = f"{folder_name}_data_analysis" 
    export_path = str(Path(f"C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/Dissertation Testing - Initial Inputs and Results/{exp_name} Results/{export_folder}/bxhist"))
    
    
    # subset_range = False
    # ss_start = 1500
    # ss_end = 20500
    
    
    #inputs
    analysis_type = "emitted_bx_histogram" 
    #'emitted_bx_histogram' 'check_data_available'
    schedule_no = 4 #None or interger value
    schedule_max = None #None or interger value
    
    # generation options
    anchor_point = anchor #int to begin at a specific # , 0 for start, negative values to signifiy
    #counting from the back (data will be analysized/displayed forward)
    instances = 50 #will truncate of there are not enough, 0 = all bx
    # anchorpoint, instances
    # +ap, +inst --> count forwards from START to find start, then collect forward
    # -ap, +inst --> count backwards from the END to find start, then collect inst forward
    # +ap, -inst --> this can be done, not coded right now
    # -ap, -inst --> this can be done, not coded right now
    # ap = 0, +inst --> start from the beginning and count forward
    # ap = 0, -inst --> count backward the END to find starting  (analysis still forward)
    # ap = any, inst = 0 > collect everything
    
    #SE selection(s)
    SE = [] #list Ex: [1,5,7], or [11], or [] for all data
    
    #histogram parameters
    histogram_bins = 30
    hist_min = 0
    hist_max = 1023
    hist_range_tuple = (hist_min,hist_max)
    HIST_BINS = np.linspace(hist_min, hist_max, histogram_bins+1)
    quantity_type = 'absolute' #'absolute' or 'relative' absolute or relative
    
    #stats parameters
    CI = 0.9 #confidence interval
    rounded = 3
    
    #plot inputs
    yplot_top = None #None - default 10% larger than largest errorbar
    yplot_bottom = None #None - default 0
    xplot_left = None  #None - default all data, 400
    xplot_right = None #None -default all data, 600
    
    #create strings for indexing or output file names
    # analysis_type = "emitted_bx_histogram" 
    #'emitted_bx_histogram' 'check_data_available'
    if analysis_type == 'emitted_bx_histogram':
        analysis_type_str = 'em_bx_hist'
    
        
    SE_str = str(SE)
    qty_str = quantity_type[:3]
    plot_str = ''
    plot_inputs = False
    if yplot_top != None:
        plot_str = plot_str + 'yt' + str(yplot_top) + '_'
        plot_inputs = True
    if yplot_bottom != None:
        plot_str = plot_str + 'yb' + str(yplot_bottom) + '_'
        plot_inputs = True
    if xplot_left != None:
        plot_str = plot_str + 'xl' + str(xplot_left) + '_'
        plot_inputs = True
    if xplot_right != None:
        plot_str = plot_str + 'xr' + str(xplot_right) + '_'
        plot_inputs = True
    if plot_inputs == True:
        plot_str = 'plot_' + plot_str
        
    #parameter checking
    if schedule_no != None and schedule_max != None:
        print('schedule_no and schedule_max cannot be active at the same time!')
        raise ValueError
    
    def generate_export_path(file_name_components,export_path,file_type):
        temp_file_name = ""
        for item in range(len(file_name_components)):
            temp_file_name = temp_file_name + '_' + str(file_name_components[item])
        
        type_string = f'.{file_type}'
        # type_string = f'_{file_type}.{file_type}'
        final_export_string = export_path + temp_file_name + type_string
        return final_export_string
    
    # if subset_range == True: 
    #     export_file_name = f'{exp_name}_{crit_name_element}_subset({ss_start}_{ss_end})_analysis_v2.xlsx'
    # else:      
    #     export_file_name = f'{exp_name}_{crit_name_element}_analysis_v2.xlsx'
    
    def mean_confidence_interval(data, confidence=0.95):
        a = 1.0 * np.array(data)
        n = len(a)
        m, se = np.mean(a), scipy.stats.sem(a)
        h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
        return m, m+h, m-h
    
    # def prepare_animation(bar_container):
        
    #     def animate(frame_number):
    #         # simulate new data coming in
    #         data = list(temp_data_bxpop.iloc[frame_number,:])
    #         n, _ = np.histogram(data, HIST_BINS, range=hist_range_tuple)
    #         for count, rect in zip(n, bar_container.patches):
    #             rect.set_height(count)
    #         return bar_container.patches
    #     return animate
        
    def prepare_subset(pre_subset_data_emittedbx,anchor_point, instances):
        # anchorpoint, instances
        # +ap, +inst --> count forwards from START to find start, then collect forward
        # -ap, +inst --> count backwards from the END to find start, then collect inst forward
        # +ap, -inst --> this can be done, not coded right now
        # -ap, -inst --> this can be done, not coded right now
        # ap = 0, +inst --> start from the beginning and count forward
        # ap = 0, -inst --> count backward the END to find starting  (analysis still forward)
        # ap = any, inst = 0 > collect everything
        
        if instances == 0:
            print('instances = 0. No subsetting done.')
            return pre_subset_data_emittedbx
        if type(anchor_point) == int and type(instances) == int:
            abs_ap = abs(anchor_point)
            abs_inst = abs(instances)
            max_rows = len(pre_subset_data_emittedbx.index)
            
            if abs_ap > max_rows:
                print(f'abs anchor_point({abs(anchor_point)}) cannot be greater than number of rows({max_rows})')
                raise ValueError
                
            if anchor_point >= 0 and instances == abs_inst:
                if anchor_point + instances > max_rows:
                    print(f'anchor_point({anchor_point}) + instances({instances}) is greater than number of rows({max_rows})')
                    print(f'result will be truncated by {anchor_point + instances - max_rows} values')
                    bx_emitted_subset = pre_subset_data_emittedbx.iloc[anchor_point:(max_rows),:]
                else:
                    bx_emitted_subset = pre_subset_data_emittedbx.iloc[anchor_point:(anchor_point+instances),:]
            elif anchor_point == 0 and instances != abs_inst:
                if max_rows - abs_inst < 0:
                    print(f' number of instances({instances}) is greater than number of rows({max_rows})')
                    print(f'result will be truncated by {abs(max_rows - abs_inst)} values')
                    bx_emitted_subset = pre_subset_data_emittedbx.iloc[0:(max_rows),:] 
                else:
                #     print(f'max_rows = {max_rows}, abs_inst = {abs_inst}')
                #     print(f'type = {type(pre_subset_data_emittedbx)}')
                    bx_emitted_subset = pre_subset_data_emittedbx.iloc[(max_rows-abs_inst):(max_rows),:] 
            # elif anchor_point == abs_ap and instances == abs_inst:
            #     #already taken care of
            elif anchor_point != abs_ap and instances != abs_inst:
                #this can be done, not coded right now
                print('instances may only be negative if the anchor_point = 0')
                raise ValueError
            elif anchor_point == abs_ap and instances != abs_inst:
                #this can be done, not coded right now
                print('instances may only be negative if the anchor_point = 0')
                raise ValueError
            elif anchor_point != abs_ap and instances == abs_inst:
                if abs_ap < instances:
                    print(f'number of instances({instances}) is greater than number of rows({abs_ap})')
                    print(f'result will be truncated by {abs_inst - abs_ap} values')
                    bx_emitted_subset = pre_subset_data_emittedbx.iloc[(max_rows-abs_ap):(max_rows),:] 
                else: #abs_ap > instances: 
                   bx_emitted_subset = pre_subset_data_emittedbx.iloc[(max_rows-abs_ap):(max_rows-abs_ap+instances),:]      
                
            # else: # anchor_point < 0
            #     max_rows = len(temp_data_bxpop.index)
                 
    
        else:
            print(f'anchor_point({anchor_point}) and instances({instances}) must be integer values')
            raise ValueError
        
        return bx_emitted_subset
    
    # anchor_point = 0 #int to begin at a specific # , "end" to count backwards, 0 for start
    # count_type = 'gen' #'gen' or 'percentage'
    # percent_or_count = 10
    
    ###############################################################################
    #CODE START#
    ###############################################################################
    
    raw_data_folder = f"{folder_name}_raw_data"
    raw_data_path = str(Path(f"C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/Dissertation Testing - Initial Inputs and Results/{exp_name} Results/{raw_data_folder}"))
    # 
    file_list = glob.glob(f"{raw_data_path}/*{crit_name_element}*.csv")
    
    # print(file_list)
    matching_reps = pd.DataFrame([], columns=['rep','a','b','PVAF'])
    sum_holder_holder = pd.DataFrame([], columns=['sched','r_name','bx_name'])
    behavior_holder_holder = pd.DataFrame([], columns=['sched','r_name','bx_name'])
    stats_data = pd.DataFrame([], columns=['sched','r_name','bx_name'])
    print(f'number of files to be analyzed: {len(file_list)}')
    first_file = True
    last_file = False
    file_counter = 0
    max_rows_counter = {}
    
    # emitted_bx_histogram variables
    if analysis_type == 'emitted_bx_histogram':
        rep_histogram_output = pd.DataFrame([], columns=['rep'])
        for each_bin in range(1,histogram_bins+1):
            bin_name = 'bin_' + str(each_bin)
            rep_histogram_output[bin_name] = []
            
        stats_data = pd.DataFrame([],columns=['mean','sem','CI+','CI-','stdev','max','min'])
    
    for input_file in file_list:
        file_counter += 1
        start_index = input_file.rfind(sep) + 1
        
        
        end_index = input_file.rfind(".")
        key_name = input_file[start_index:end_index]
    
        
        #find rep
        rep_end_index = input_file.rfind("_")
        rep_start_index = input_file.rfind("rep")+3
        rep_num = int(input_file[rep_start_index:rep_end_index])
        print("")
        print(f'rep_num = {rep_num}')
        try:
           temp_data = pd.read_csv(input_file)
        except FileNotFoundError:
               print("raw data file not found!")
        
        
        
        
        sched_max = temp_data["schedule"].max()
        sched = 1
        
        # print("")  
        # df[df.columns[1:4]]
        
        # bxpop stuff###
        # bx_counter = 1
        # start_column_name = 'bx' + str(bx_counter)
        # max_columns = len(temp_data.columns)
        # start_column = temp_data.columns.get_loc(start_column_name)
        
        # find_end = False
         
        # next_column = start_column+1
        
        # while find_end == False:
        #     bx_counter += 1
        #     next_column_name = "bx" + str(bx_counter)
        #     if next_column_name in temp_data.columns:
        #         next_column += 1
        #     else:
        #         final_column = next_column
        #         find_end = True
        # df_new = df[df['Pid'] == 'p01']
        
        #check for targeting bx pop columns
        # print(f'max_columns = {max_columns}')
        # print(f'start_column = {start_column}')
        # print(f'final_column = {final_column}')
        
        #schedule restrictions
        # df.iloc[df.Humidity > 50, :]
        if schedule_no != None:
            temp_data = temp_data.iloc[list(temp_data.schedule == schedule_no),:]
            schedule_str = str(schedule_no) + 'EQ'
            print(f'data from schedule {schedule_no} only')
        elif schedule_max != None:
            temp_data = temp_data.iloc[list(temp_data.schedule <= schedule_max),:]
            schedule_str = str(schedule_max) + 'EQorL'
            print(f'data from schedule {schedule_max} or less')
        else:
            print('data from all schedules')
            schedule_str = 'None'
            
        #File name component used for all exported files    
        # name = analysis_type + '_sched' + schedule_str + '_SE' + SE_str + '_repnum' + str(rep_num)
        # print(f'name = {name}')
        
    ###############################################################################
    #CHECK_DATA_AVAILABLE 
    ###############################################################################   
    #output the amount of data is present with the given settings.
        
        if analysis_type == 'check_data_available':
            print(f'total number of schedules = {len(temp_data.schedule.unique())}')
            if len(SE) == 0:
                temp_data_emittedbx = temp_data[['schedule','emitted_bx','emitted_se']]
                subset_data = prepare_subset(temp_data_emittedbx,anchor_point, instances)
                subset_data.reset_index(drop=True)
                data_length = len(subset_data.index)
                print(f'rep_{rep_num}, all data rows {data_length}')
                data_exist = max_rows_counter.get('all_data')
                if data_exist != None:
                    max_rows_counter.update({'all_data':data_length+data_exist})
                else:
                    max_rows_counter.update({'all_data':len(subset_data.index)})
            else:
                for each_se in range(len(SE)):
                    temp_data_emittedbx = temp_data[['schedule','emitted_bx','emitted_se']]
                    subset_data = prepare_subset(temp_data_emittedbx,anchor_point, instances)
                    subset_data = subset_data.iloc[list(subset_data.emitted_se == SE[each_se]),0:2 ]
                    subset_data.reset_index(drop=True)
                    # subset_data = prepare_subset(subset_data,anchor_point, instances)
                    # subset_data.reset_index(drop=True)
                    max_num_rows = len(subset_data.index)
                    print(f'rep_{rep_num}, se_{SE[each_se]}, data_rows_{max_num_rows}')
                    SE_exist = max_rows_counter.get(SE[each_se])
                    if SE_exist != None:
                        max_rows_counter.update({SE[each_se]:SE_exist+max_num_rows})
                    else:
                        max_rows_counter.update({SE[each_se]:max_num_rows})
            if file_counter == len(file_list):
                print(f'lines of data in selected set = {max_rows_counter}')
    
    ###############################################################################
    # EMITTED BX HISTOGRAM
    ###############################################################################
        #find bx histogram for the given data and avg across reps
        
        if analysis_type == 'emitted_bx_histogram':
            if len(SE) == 0:
                temp_data_emittedbx = temp_data[['schedule','emitted_bx','emitted_se']]
                subset_data = prepare_subset(temp_data_emittedbx,anchor_point, instances)
                subset_data.reset_index(drop=True)
                
                data = list(subset_data['emitted_bx'])
                
                n, _ = np.histogram(data, HIST_BINS, range=hist_range_tuple)
                current_index = len(rep_histogram_output.index)
                # print(f' type(n) = {type(n)}')
                # print(f'n = {n}')
                if quantity_type == 'relative':
                    sum_n = np.sum(n)
                    n = np.divide(n,sum_n)
                    # print(f'n = {n}')
                #df.loc[len(df.index)] = ['Amy', 89, 93]
                #rep, SE, bin_1,bin2...
                data_list = []
                data_list.append(rep_num)
                # data_list.append(SE[each_se])
                # print(n)
                for ea_bin in range(len(n)):
                    bin_name = 'bin_' + str(ea_bin+1)
                    bin_value = n[ea_bin]
                    data_list.append(bin_value)
                # print(len(final_row_agg_output.columns))
                # print(len(data_list))
                rep_histogram_output.loc[len(rep_histogram_output.index)] = data_list
                
                # data_length = len(subset_data.index)
                # print(f'rep_{rep_num}, all data rows {data_length}')
                # data_exist = max_rows_counter.get('all_data')
                # if data_exist != None:
                #     max_rows_counter.update({'all_data':data_length+data_exist})
                # else:
                #     max_rows_counter.update({'all_data':len(subset_data.index)})
            else:
                for each_se in range(len(SE)):
                    temp_data_emittedbx = temp_data.iloc[list(temp_data.emitted_se == SE[each_se]),0:2]
                    temp_data_emittedbx.reset_index(drop=True)
                    subset_data = prepare_subset(temp_data_emittedbx,anchor_point, instances)
                    subset_data.reset_index(drop=True)
                    max_row = len(subset_data.index)-1
                    print(f'max row = {max_row}')
                    
                    data = list(subset_data['emitted_bx'])
                    
                    n, _ = np.histogram(data, HIST_BINS, range=hist_range_tuple)
                    current_index = len(rep_histogram_output.index)
                    #df.loc[len(df.index)] = ['Amy', 89, 93]
                    #rep, SE, bin_1,bin2...
                    data_list = []
                    data_list.append(rep_num)
                    # data_list.append(SE[each_se])
                    # print(n)
                    for ea_bin in range(len(n)):
                        bin_name = 'bin_' + str(ea_bin+1)
                        bin_value = n[ea_bin]
                        data_list.append(bin_value)
                    # print(len(final_row_agg_output.columns))
                    # print(len(data_list))
                    rep_histogram_output.loc[len(rep_histogram_output.index)] = data_list
                # [rows,col] = final_row_agg_output.shape
            print(rep_histogram_output.shape)
    
            if file_counter == len(file_list):
                
            # histogram_bins
                for bin_x in range(1,histogram_bins+1):
                    bin_name = 'bin_' + str(bin_x)
                    current_bin = rep_histogram_output[bin_name]
                    [a_mean,a_CI_plus,a_CI_minus] = mean_confidence_interval(current_bin,confidence = CI)
                    a_stdev = scipy.stats.tstd(current_bin)
                    a_sem = scipy.stats.sem(current_bin)
                    a_max = current_bin.max()
                    a_min = current_bin.min()
                    a_CI_raw = a_CI_plus - a_mean
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
                                                rounded_a_stdev,rounded_a_max,rounded_a_min]], index =[bin_x-1], \
                                              columns=['mean','sem','CI+','CI-','stdev','max','min'])
        
                    stats_data = stats_data.append(a_stats_data)  
                    
                # Plot output
                h_data = list(stats_data.iloc[:,0])
                SEM = list(stats_data.iloc[:,1])
                first = True
                bin_mid_points = []
                width_length = None
                for bin_edge in HIST_BINS:
                    if first == True:
                        first = False
                        left_edge = bin_edge
                        continue
                    right_edge = bin_edge
                    midpoint = (right_edge + left_edge)/2
                    bin_mid_points.append(midpoint)
                    if width_length == None:
                        width_length = right_edge - left_edge
                    elif (right_edge - left_edge) < width_length:
                        width_length = right_edge - left_edge
                    else:
                        pass
                    #set up for next round
                    left_edge = right_edge
                    
                # print(max(h_data))
                width_length = width_length - 1
                data_height_max = max(h_data)
                max_height_index = stats_data[stats_data['mean'] == data_height_max].index.values
                sem_of_max_height_value = stats_data.iloc[max_height_index,1].values
                if len(sem_of_max_height_value) > 1:
                    sem_of_max_height_value = sem_of_max_height_value.max()
                else:
                    pass
                # print(f' max value = {data_height_max}, index = {max_height_index}, SEM = {stats_data.iloc[max_height_index,1].values}')
                # print(bin_mid_points)
                # print(len(bin_mid_points))
                fig, ax = plt.subplots()
                # _, _, bar_container = ax.bar(HIST_BINS,data, lw=1,
                #                               ec="yellow", fc="green", alpha=0.5)
                figure_height = (sem_of_max_height_value+data_height_max)*1.1
                # print(f'ax type = {type(ax)}')
                
                # ax.set_ylim(top=(figure_height))  # set safe limit to ensure that all data is visible
                # ax.set_xlim((466,547))
                # ax.set_xbound(lower=466, upper=547)
                plt.switch_backend('QtAgg')
                # plt.show()
                
                # PNG file output #################################################
                
                plt.bar(bin_mid_points, h_data, width=width_length, color=(0.2, 0.4, 0.6, 0.6), yerr=SEM, capsize=6)
                # ax.set_ylim(top=(20))
                #plot shapes
                # ax = fig.add_subplot(111, aspect='equal')
                # plt.axes()
                if yplot_top != None and yplot_bottom != None:
                    plt.ylim(top=yplot_top,bottom=yplot_bottom)
                    figure_height = yplot_top
                elif yplot_top != None and yplot_bottom == None:
                    plt.ylim(top=yplot_top)
                    figure_height = yplot_top
                elif yplot_top == None and yplot_bottom != None:
                    plt.lim(bottom=yplot_bottom)
                else:
                    plt.ylim(top=figure_height)
                if xplot_left != None and xplot_right != None:
                    plt.xlim((xplot_left, xplot_right))
                elif xplot_left == None and xplot_right != None:
                    plt.xlim(right=xplot_right)
                elif xplot_left != None and xplot_right == None:
                    plt.xlim(left=xplot_left)
                else:
                    pass
                
                rectangle = plt.Rectangle((471,0), 40, figure_height, fc=(mpl.colors.to_rgba('green', alpha=.35)),ec=None,label='target class 1')
                plt.gca().add_patch(rectangle)
                rectangle2 = plt.Rectangle((512,0), 40, figure_height, fc=(mpl.colors.to_rgba('purple', alpha=.35)),ec=None,label='target class 2')
                plt.gca().add_patch(rectangle2)
                plt.legend()
                plt.xlabel('Phenotype Bins')
                plt.ylabel('Quanitity')
                plt.title('Emitted Behavior Histogram')
                
    
                
                file_name_components = [crit_name_element,'_',analysis_type_str,'_sched',schedule_str,'_SE',\
                                        SE_str,'_a(inst)',anchor_point,'(',instances,')',\
                                        '_qtyT-',qty_str,'_',plot_str]
                export_final = generate_export_path(file_name_components,export_path,'png')
                
                plt.savefig(export_final)
                
                ###################################################################
                # EXCEL file output #####################################################
                # file_name_components = [crit_name_element,'_',analysis_type_str,'_sched',schedule_str,'_SE',\
                #                         SE_str,'_a(inst)',anchor_point,'(',instances,')',\
                #                         '_qtyT-',qty_str,'_',plot_str]
                file_name_components = [crit_name_element,'_sch',schedule_str,\
                                        '_a(inst)',anchor_point,'(',instances,')']
                                        
                export_final = generate_export_path(file_name_components,export_path,'xlsx')
                # print(export_final)
                print(f'lines of data used = {len(rep_histogram_output.index)}')
                # print(stats_data.iloc[:,0:4])
            
                writer = pd.ExcelWriter(export_final, engine='xlsxwriter')
    
                # Write each dataframe to a different worksheet.
                rep_histogram_output.to_excel(writer, sheet_name='rep_histogram')
    
                stats_data.to_excel(writer, sheet_name='combined_stats')
    
                # Close the Pandas Excel writer and output the Excel file.
                writer.close()
                ###################################################################
            
