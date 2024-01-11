# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 20:05:44 2023

Created to look at emitted behaviors during a schedule, over multiple AOs

Schedule Range:
1. All schedules
2. specific schedules

Anaylsis range:
1. Entire Schedule
2. Specified range within a schedule
    2a. based on starting and ending gen

Analysis Style:
1. absolute histogram (bin = 40)
2. relative histogram (bin = 40)

Statistical measures (for all AOs)
1. average per bin 
2. standard deviation per bin
3. standard error per bin
4. median per bin (optional)

@author: Cyrus
"""
"""
==================
Animated histogram
==================

Use histogram's `.BarContainer` to draw a bunch of rectangles for an animated
histogram.
"""
# import xlsxwriter
# import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython import display
import matplotlib as mpl 
from matplotlib.patches import Polygon

import ffmpy

import scipy.stats
import math


import glob
from pathlib import Path
from os import sep
mpl.use("Agg")
mpl.rcParams['animation.ffmpeg_path'] = r'C:\Users\Cyrus\Documents\Python_stuff\ffmpeg\bin\ffmpeg.exe'

#Inputs########################################################################

#file information
exp_name = "ExpTRd"
folder_name = "ExpTRd"
crit_name_element = "TRd1_Win1t3_SelMod3"
export_folder = f"{folder_name}_data_analysis" 
export_path = str(Path(f"C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/Dissertation Testing - Initial Inputs and Results/{exp_name} Results/{export_folder}/bp"))


# subset_range = False
# ss_start = 1500
# ss_end = 20500


#inputs
analysis_type = "single_SE_stream" 
#'final_row_aggregation','single_SE_stream' 'check_data_available' 'final_SE_data'
schedule_no = 1 #None or interger value
schedule_max = None #None or interger value

# generation options
anchor_point = 0 #int to begin at a specific # , 0 for start, negative values to signifiy
#counting from the back (data will be analysized/displayed forward)
instances = 100 #will truncate of there are not enough, count number or percentage, btw 1 and 100
# anchorpoint, instances
# +ap, +inst --> count forwards from START to find start, then collect forward
# -ap, +inst --> count backwards from the END to find start, then collect inst forward
# +ap, -inst --> this can be done, not coded right now
# -ap, -inst --> this can be done, not coded right now
# ap = 0, +inst --> start from the beginning and count forward
# ap = 0, -inst --> count backward the END to find starting  (analysis still forward)
# ap = any, inst = 0 > collect everything

#SE selection(s)
SE = [0] #list Ex: [1,5,7], or [11]

#stats parameters (bx pop only)
histogram_bins = 30
hist_min = 0
hist_max = 1023
hist_range_tuple = (hist_min,hist_max)
HIST_BINS = np.linspace(hist_min, hist_max, histogram_bins+1)
# print(len(HIST_BINS))
# print(HIST_BINS)
CI = 0.9 #confidence interval
rounded = 3

SE_str = str(SE)

#parameter checking
if schedule_no != None and schedule_max != None:
    print('schedule_no and schedule_max cannot be active at the same time!')
    raise ValueError

if analysis_type == 'final_row_aggregation':
    analysis_type_str = 'f_row_ag'
elif analysis_type == 'single_SE_stream':
    analysis_type_str = 'SE_stre'
elif analysis_type == 'final_SE_data':
    analysis_type_str = 'SE_dat'
    
def generate_export_path(file_name_components,export_path,file_type):
    temp_file_name = ""
    for item in range(len(file_name_components)):
        temp_file_name = temp_file_name + '_' + str(file_name_components[item])
    
    type_string = f'_{file_type}.{file_type}'
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

def prepare_animation(bar_container):
    
    def animate(frame_number):
        # simulate new data coming in
        data = list(temp_data_bxpop.iloc[frame_number,:])
        n, _ = np.histogram(data, HIST_BINS, range=hist_range_tuple)
        
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='white', alpha=1)
        
        # place a text box in upper left in axes coords
        ax.text(0.05, 0.95, frame_number, transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=props)
        
        
        for count, rect in zip(n, bar_container.patches):
            rect.set_height(count)
        return bar_container.patches
    return animate
    
def prepare_subset(pre_subset_data_bxpop,anchor_point, instances):
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
        return pre_subset_data_bxpop
    if type(anchor_point) == int and type(instances) == int:
        abs_ap = abs(anchor_point)
        abs_inst = abs(instances)
        max_rows = len(pre_subset_data_bxpop.index)
        
        if abs_ap > max_rows:
            print(f'abs anchor_point({abs(anchor_point)}) cannot be greater than number of rows({max_rows})')
            raise ValueError
            
        if anchor_point >= 0 and instances == abs_inst:
            if anchor_point + instances > max_rows:
                print(f'anchor_point({anchor_point}) + instances({instances}) is greater than number of rows({max_rows})')
                print(f'result will be truncated by {anchor_point + instances - max_rows} values')
                bx_pop_subset = pre_subset_data_bxpop.iloc[anchor_point:(max_rows),:]
            else:
                bx_pop_subset = pre_subset_data_bxpop.iloc[anchor_point:(anchor_point+instances),:]
        elif anchor_point == 0 and instances != abs_inst:
            if max_rows - abs_inst < 0:
                print(f' number of instances({instances}) is greater than number of rows({max_rows})')
                print(f'result will be truncated by {abs(max_rows - abs_inst)} values')
                bx_pop_subset = pre_subset_data_bxpop.iloc[0:(max_rows),:] 
            else:
                bx_pop_subset = pre_subset_data_bxpop.iloc[(max_rows-abs_inst):(max_rows),:] 
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
                bx_pop_subset = pre_subset_data_bxpop.iloc[(max_rows-abs_ap):(max_rows),:] 
            else: #abs_ap > instances: 
               bx_pop_subset = pre_subset_data_bxpop.iloc[(max_rows-abs_ap):(max_rows-abs_ap+instances),:]      
            
        # else: # anchor_point < 0
        #     max_rows = len(temp_data_bxpop.index)
             

    else:
        print(f'anchor_point({anchor_point}) and instances({instances}) must be integer values')
        raise ValueError
    
    return bx_pop_subset

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

if analysis_type == 'final_SE_data':
    output_data_holder = pd.DataFrame([],columns=['rep','Schedule','SE','reinforcers','count','entropy','sel_mod','win_goal'])
    stats_data = pd.DataFrame([],columns=['mean','sem','CI+','CI-','stdev','max','min'])
# final_row_aggregation variables
if analysis_type == 'final_row_aggregation':
    final_row_agg_output = pd.DataFrame([], columns=['rep','SE'])
    for each_bin in range(1,histogram_bins+1):
        bin_name = 'bin_' + str(each_bin)
        final_row_agg_output[bin_name] = []
        
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
    bx_counter = 1
    start_column_name = 'bx' + str(bx_counter)
    max_columns = len(temp_data.columns)
    start_column = temp_data.columns.get_loc(start_column_name)
    
    find_end = False
     
    next_column = start_column+1
    
    while find_end == False:
        bx_counter += 1
        next_column_name = "bx" + str(bx_counter)
        if next_column_name in temp_data.columns:
            next_column += 1
        else:
            final_column = next_column
            find_end = True
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
    #output the amount of data is present with the given settings.
    
    if analysis_type == 'check_data_available':
        print(f'total number of schedules = {len(temp_data.schedule.unique())}')
        for each_se in range(len(SE)):
            temp_data_bxpop = temp_data.iloc[list(temp_data.emitted_se == SE[each_se]),start_column:final_column ]
            temp_data_bxpop.reset_index(drop=True)
            subset_data = prepare_subset(temp_data_bxpop,anchor_point, instances)
            subset_data.reset_index(drop=True)
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
    #find bx pop histogram at the end of a given schedule and avg across reps
    if analysis_type == 'final_row_aggregation':

        for each_se in range(len(SE)):
            temp_data_bxpop = temp_data.iloc[list(temp_data.emitted_se == SE[each_se]),start_column:final_column ]
            temp_data_bxpop.reset_index(drop=True)
            subset_data = prepare_subset(temp_data_bxpop,anchor_point, instances)
            subset_data.reset_index(drop=True)
            max_row = len(subset_data.index)-1
            print(f'max row = {max_row}')
            
            data = list(subset_data.iloc[max_row,:])
            n, _ = np.histogram(data, HIST_BINS, range=hist_range_tuple)
            current_index = len(final_row_agg_output.index)
            #df.loc[len(df.index)] = ['Amy', 89, 93]
            #rep, SE, bin_1,bin2...
            data_list = []
            data_list.append(rep_num)
            data_list.append(SE[each_se])
            # print(n)
            for ea_bin in range(len(n)):
                bin_name = 'bin_' + str(ea_bin+1)
                bin_value = n[ea_bin]
                data_list.append(bin_value)
            # print(len(final_row_agg_output.columns))
            # print(len(data_list))
            final_row_agg_output.loc[len(final_row_agg_output.index)] = data_list
        # [rows,col] = final_row_agg_output.shape
        print(final_row_agg_output.shape)

        if file_counter == len(file_list):
            
        # histogram_bins
            for bin_x in range(1,histogram_bins+1):
                bin_name = 'bin_' + str(bin_x)
                current_bin = final_row_agg_output[bin_name]
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
            for bin_edge in HIST_BINS:
                if first == True:
                    first = False
                    left_edge = bin_edge
                    continue
                right_edge = bin_edge
                midpoint = (right_edge + left_edge)/2
                bin_mid_points.append(midpoint)
                #set up for next round
                left_edge = right_edge
                
            # print(max(h_data))
            data_height_max = max(h_data)
            max_height_index = stats_data[stats_data['mean'] == data_height_max].index.values
            sem_of_max_height_value = stats_data.iloc[max_height_index,1].values[0]
            print(f' max value = {data_height_max}, index = {max_height_index}, SEM = {stats_data.iloc[max_height_index,1].values}')
            # print(bin_mid_points)
            # print(len(bin_mid_points))
            fig, ax = plt.subplots()
            # _, _, bar_container = ax.bar(HIST_BINS,data, lw=1,
            #                               ec="yellow", fc="green", alpha=0.5)
            if math.isnan(sem_of_max_height_value):
                figure_height = data_height_max*1.1
            else:
                figure_height = (sem_of_max_height_value+data_height_max)*1.1
            plt.ylim(top=(figure_height))  # set safe limit to ensure that all data is visible
            plt.switch_backend('QtAgg')
            # plt.show()
            
            # PNG file output #################################################
            
#             "1":
# 			{
# 				"target_type":"primary",
# 				"target_high": 511,
# 				"target_low": 471,
# 				"reward_continvency_type":"target"
# 			},
# 			"2":
# 			{
# 				"target_type":"primary",
# 				"target_high": 552,
# 				"target_low": 512,
# 				"reward_continvency_type":"varied"
            
            plt.bar(bin_mid_points, h_data, width=30, color=(0.2, 0.4, 0.6, 0.6), yerr=SEM, capsize=6)
            #plot shapes
            # ax = fig.add_subplot(111, aspect='equal')
            # plt.axes()
            rectangle = plt.Rectangle((471,0), 40, figure_height, fc=(mpl.colors.to_rgba('green', alpha=.25)),ec=None,label='target class 1')
            plt.gca().add_patch(rectangle)
            rectangle2 = plt.Rectangle((512,0), 40, figure_height, fc=(mpl.colors.to_rgba('purple', alpha=.25)),ec=None,label='target class 2')
            plt.gca().add_patch(rectangle2)
            plt.legend()
            plt.xlabel('Phenotype Bins')
            plt.ylabel('Quanitity')
            plt.title('Bx Population')
            # plt.axis('scaled')
            # plt.show()


            
            
            
            file_name_components = [crit_name_element,'_',analysis_type_str,'_sched',schedule_str,'_SE',\
                                    SE_str,'_a(inst)',anchor_point,'(',instances,')']
            export_final = generate_export_path(file_name_components,export_path,'png')
            
            plt.savefig(export_final)
            
            ###################################################################
            # EXCEL file output #####################################################
            
            export_final = generate_export_path(file_name_components,export_path,'xlsx')
            print(export_final)
            print(f'lines of data used = {len(final_row_agg_output.index)}')
            print(stats_data.iloc[:,0:4])
        
            writer = pd.ExcelWriter(export_final, engine='xlsxwriter')

            # Write each dataframe to a different worksheet.
            final_row_agg_output.to_excel(writer, sheet_name='final_rows')

            stats_data.to_excel(writer, sheet_name='combined_stats')

            # Close the Pandas Excel writer and output the Excel file.
            writer.close()
            ###################################################################
            
        # print(final_row_agg_output.head())
            #n = values in each BIN, and _ is the edges of the histogram
            
        #     print(f'se{SE[each_se]}, rows{max_num_rows}')
        #     SE_exist = max_rows_counter.get(SE[each_se])
        #     if SE_exist != None:
        #         max_rows_counter.update({SE[each_se]:SE_exist+max_num_rows})
        #     else:
        #         max_rows_counter.update({SE[each_se]:max_num_rows})
        # if file_counter == len(file_list):
        #     print(f'lines of data in selected set = {max_rows_counter}')    

###############################################################################    
    #single SE over time
    if analysis_type == 'single_SE_stream':
        if len(SE) != 1:
            print(f'SE list ({SE}) contains more than one value!')
            raise ValueError
            

        temp_data_bxpop = temp_data.iloc[list(temp_data.emitted_se == SE[0]),start_column:final_column ]
        
        temp_data_bxpop.reset_index(drop=True)
        subset_data = prepare_subset(temp_data_bxpop,anchor_point, instances)
        subset_data.reset_index(drop=True)
        max_num_rows = len(subset_data.index)
        print(f'num_rows = {max_num_rows}')
        

        
        # histogram our data with numpy
        # data = np.random.randn(1000)
        data = list(subset_data.iloc[0,:])
        n, _ = np.histogram(data, HIST_BINS, range=hist_range_tuple)
        # print(np.histogram(data, HIST_BINS))
        row_counter = 0
        ###############################################################################
        # To animate the histogram, we need an ``animate`` function, which generates
        # a random set of numbers and updates the heights of rectangles. We utilize a
        # python closure to track an instance of `.BarContainer` whose `.Rectangle`
        # patches we shall update.

        ###############################################################################
        # Using :func:`~matplotlib.pyplot.hist` allows us to get an instance of
        # `.BarContainer`, which is a collection of `.Rectangle` instances. Calling
        # ``prepare_animation`` will define ``animate`` function working with supplied
        # `.BarContainer`, all this is used to setup `.FuncAnimation`.
        
        fig, ax = plt.subplots()
        _, _, bar_container = ax.hist(data, HIST_BINS, lw=1,
                                      ec="yellow", fc="green", alpha=0.5)
        ax.set_ylim(top=200)  # set safe limit to ensure that all data is visible.
        
        ani = animation.FuncAnimation(fig, prepare_animation(bar_container), max_num_rows,
                                      repeat=False, blit=True)
        
        # draw the animation
        #display.display(html)
        # name = analysis_type + '_sched' + schedule_str + '_SE' + SE_str + '_repnum' + str(rep_num)
        # print(f'name = {name}')
        file_name_components = [analysis_type,'_sched',schedule_str,'_SE',SE_str,'_repnum',str(rep_num)]
        export_gif_path = generate_export_path(file_name_components,export_path,'gif')
        export_mp4_path = generate_export_path(file_name_components,export_path,'mp4')
        # name_post_gif = "_gif.gif"
        # name_post_mp4 = "_mp4.mp4"
        # gif_name = name + name_post_gif
        # mp4_name = name + name_post_mp4
        # export_mp4_file_name = f'{exp_name}_{crit_name_element}_' + mp4_name
        # export_gif_file_name = f'{exp_name}_{crit_name_element}_' + gif_name
        # export_mp4_path = str(Path(f"C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/Dissertation Testing - Initial Inputs and Results/{exp_name} Results/{export_folder}/{export_mp4_file_name}"))
        # export_gif_path = str(Path(f"C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/Dissertation Testing - Initial Inputs and Results/{exp_name} Results/{export_folder}/{export_gif_file_name}"))
        # f = r"C:\Users\Cyrus\Downloads\animation_gif.gif" 
        writergif = animation.PillowWriter(fps=5) 
        ani.save(export_gif_path, writer=writergif)
        
        #f = r"C:\Users\Cyrus\Downloads\animation_mp4.mp4" 
        # writervideo = animation.FFMpegWriter(fps=2, extra_args=['-itsoffset','00:00:00.300']) 
        writervideo = animation.FFMpegWriter(fps=2)
        ani.save(export_mp4_path, writer=writervideo)
###############################################################################

###############################################################################
    #find SE data
    if analysis_type == 'final_SE_data':
        
        
        right_column = temp_data.columns.get_loc('Sel_mod')
        left_column = temp_data.columns.get_loc('schedule')
        for each_se in range(len(SE)):
            temp_data_bxpop = temp_data.iloc[list(temp_data.emitted_se == SE[each_se]),:]
            temp_data_bxpop.reset_index(drop=True)
            subset_data = prepare_subset(temp_data_bxpop,anchor_point, instances)
            subset_data.reset_index(drop=True)
            max_row = len(subset_data.index)-1
            print(f'max row = {max_row}')
            
            schedule_loc = subset_data.columns.get_loc('schedule')
            reinforcer_loc = subset_data.columns.get_loc('BK-R3')
            entropy_loc = subset_data.columns.get_loc('emitted_SE_entropy')
            sel_mod_loc = subset_data.columns.get_loc('Sel_mod')
            win_goal_loc = subset_data.columns.get_loc('SE_win_goal')
            
            data = list(subset_data.iloc[max_row,:])
            output_rep = rep_num
            output_sched = subset_data.iloc[max_row,schedule_loc]
            output_SE = each_se
            outout_reinforcers = subset_data.iloc[:,reinforcer_loc].sum()
            output_occurances = len(subset_data.index)
            output_entropy = subset_data.iloc[max_row,entropy_loc]
            output_sel_mod = subset_data.iloc[max_row,sel_mod_loc]
            output_win_goal = subset_data.iloc[max_row,win_goal_loc]
            
            temp_output_data = pd.DataFrame([[output_rep,output_sched,output_SE,outout_reinforcers, \
                                        output_occurances,output_entropy,output_sel_mod,output_win_goal]],\
                                      columns=['rep','Schedule','SE','reinforcers','count','entropy','sel_mod','win_goal'])

            output_data_holder = output_data_holder.append(temp_output_data)

        if file_counter == len(file_list):
        
            # # Stats Data for Sel_mod, win_goal,entropy, reinforcers,count
            items = ['reinforcers','count','entropy','sel_mod','win_goal']
            for it in items:
                current_items = output_data_holder[it]
            # for bin_x in range(1,len(win_goal_bins)+1):
            #     bin_name = 'bin_' + str(bin_x)
            #     current_bin = final_row_agg_output[bin_name]
                # print(it)
                # print(len(current_items))
                [a_mean,a_CI_plus,a_CI_minus] = mean_confidence_interval(current_items,confidence = CI)
                a_stdev = scipy.stats.tstd(current_items)
                a_sem = scipy.stats.sem(current_items)
                a_max = current_items.max()
                a_min = current_items.min()
                a_CI_raw = a_CI_plus - a_mean
                # print("")
                # print(f'a(mean) = {round(a_mean,3)}, CI+ = {round(a_CI_plus,3)}, CI- = {round(a_CI_minus,3)}')
                # print(f'a(stdev) = {round(a_stdev,3)}, max = {round(a_max,3)}, min = {round(a_min,3)}')
                
                rounded_a = round(a_mean,rounded)
                rounded_a_CI_plus = round(a_CI_plus,rounded)
                rounded_a_CI_raw = round(a_CI_raw,rounded)
                rounded_a_CI_minus = round(a_CI_minus,rounded)
                rounded_a_sem = round(a_sem,rounded)
                rounded_a_stdev = round(a_stdev,rounded)
                rounded_a_max = round(a_max,rounded)
                rounded_a_min = round(a_min,rounded)
    
                a_stats_data = pd.DataFrame([[rounded_a,rounded_a_sem,rounded_a_CI_plus,rounded_a_CI_raw,rounded_a_CI_minus, \
                                            rounded_a_stdev,rounded_a_max,rounded_a_min]], index =[it], \
                                          columns=['mean','sem','CI+','CI_raw','CI-','stdev','max','min'])
    
                stats_data = stats_data.append(a_stats_data)  
            
            #Window Goal Histogram data
            # WIN_HIST_BINS = np.linspace(200, 0, 22)
            win_data = list(output_data_holder['win_goal'])
            win_goal_bins = (0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200)
            win_hist_n, _ = np.histogram(win_data, win_goal_bins,range=(0,200))
            
           
            
            # Plot output
            win_hist_lst = list(win_hist_n)
            # SEM = list(stats_data.iloc[:,1])
            first = True
            WG_mid_points = []
            for bin_edge in win_goal_bins:
                if first == True:
                    first = False
                    left_edge = bin_edge
                    continue
                right_edge = bin_edge
                midpoint = (right_edge + left_edge)/2
                WG_mid_points.append(midpoint)
                #set up for next round
                left_edge = right_edge
                
            # matplotlib plotting
            # data_height_max = max(win_hist_lst)
            
            # fig, ax = plt.subplots()
       
            # figure_height = (data_height_max)*1.1
            # plt.ylim(top=(figure_height))  # set safe limit to ensure that all data is visible
            # # plt.switch_backend('QtAgg')
            
            # # print(f' len mid points ={len(bin_mid_points)}')
            # # print(f' len h_data ={len(win_hist_lst)}')
            # plt.bar(WG_mid_points, win_hist_lst, width=30, color=(0.2, 0.4, 0.6, 0.6), capsize=6)

            # plt.legend()
            # plt.xlabel('Window Goal Bins')
            # plt.ylabel('Quanitity')
            # plt.title('Window Goal Histogram')
            # WG_figure_no = plt.gcf().number
            # print(f'The WG plot number is = {WG_figure_no}')
            # plt.show()
            wingoal_data = {'x': WG_mid_points, 'y': win_hist_lst}
            wingoal_pd = pd.DataFrame.from_dict(wingoal_data)
            
            
            #Selection Modifier Histogram data
            # SM_HIST_BINS = np.linspace(100, 0, 22)
            selmod_data = list(output_data_holder['sel_mod'])
            selmod_bins = (0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100)
            selmod_hist_n, _ = np.histogram(selmod_data, selmod_bins,range=(0,100))    
            
            # Plot output
            selmod_hist_lst = list(selmod_hist_n)
            # SEM = list(stats_data.iloc[:,1])
            first = True
            SM_mid_points = []
            for bin_edge in selmod_bins:
                if first == True:
                    first = False
                    left_edge = bin_edge
                    continue
                right_edge = bin_edge
                midpoint = (right_edge + left_edge)/2
                SM_mid_points.append(midpoint)
                #set up for next round
                left_edge = right_edge
                
            # matplotlib plotting
            # data_height_max = max(selmod_hist_lst)
            
            # fig, ax = plt.subplots()
       
            # figure_height = (data_height_max)*1.1
            # plt.ylim(top=(figure_height))  # set safe limit to ensure that all data is visible
            # # plt.switch_backend('QtAgg')
            
            # plt.bar(SM_mid_points, selmod_hist_lst, width=30, color=(0.2, 0.4, 0.6, 0.6), capsize=6)

            # plt.legend()
            # plt.xlabel('Selection Mod Bins')
            # plt.ylabel('Quanitity')
            # plt.title('Selection Modifier Histogram')
            # SM_figure_no = plt.gcf().number
            # print(f'The SM plot number is = {SM_figure_no}')
            # plt.show()
            selmod_data = {'x': SM_mid_points, 'y': selmod_hist_lst}
            selmod_pd = pd.DataFrame.from_dict(selmod_data)
            
            
            
            file_name_components = [crit_name_element,'',analysis_type_str,'_sched',schedule_str,'_SE',\
                                    SE_str,'_a(inst)',anchor_point,'(',instances,')']
            # export_final = generate_export_path(file_name_components,export_path,'png')
            # plt.gcf().number
            # plt.savefig(export_final)
            
            ###################################################################
            # EXCEL file output #####################################################
            
            export_final = generate_export_path(file_name_components,export_path,'xlsx')
            print(export_final)
            print(f'lines of data used = {len(output_data_holder.index)}')
            # print(stats_data.iloc[:,0:4])
        
            writer = pd.ExcelWriter(export_final, engine='xlsxwriter')

            # Write dataframe to a different worksheet.
            output_data_holder.to_excel(writer, sheet_name='final_rows')
            wingoal_pd.to_excel(writer, sheet_name='win_hist_data')
            selmod_pd.to_excel(writer, sheet_name='sel_mod_hist_data')
            stats_data.to_excel(writer, sheet_name='combined_stats')

            # Create a chart object.
            workbook = writer.book
            worksheet = writer.sheets['win_hist_data']
            
            chart = workbook.add_chart({'type': 'column'})
            
            # Configure the series of the chart from the dataframe data.
            chart.add_series({
                'categories': '=win_hist_data!$B$2:$B$21',
                'values':     '=win_hist_data!$C$2:$C$21',
                'gap':        5,
            })
            
            worksheet2 = writer.sheets['sel_mod_hist_data']
            chart2 = workbook.add_chart({'type': 'column'})
            
            # Configure the series of the chart from the dataframe data.
            chart2.add_series({
                'categories': '=sel_mod_hist_data!$B$2:$B$21',
                'values':     '=sel_mod_hist_data!$C$2:$C$21',
                'gap':        5,
            })
            
            # You can also use array notation to define the chart values.
            #    chart.add_series({
            #        'values':     ['Sheet1', 1, 1, 7, 1],
            #        'gap':        2,
            #    })
            
            # Configure the chart axes.
            chart.set_y_axis({'major_gridlines': {'visible': False}})
            chart2.set_y_axis({'major_gridlines': {'visible': False}})
            
            # Set Titles and Axes Names
            # chart.set_title({
            #     'name': 'Test Results',
            #     'name_font': {
            #         'name': 'Calibri',
            #         'color': 'blue',
            #     },
            # })

            # chart.set_x_axis({
            #     'name': 'Month',
            #     'name_font': {
            #         'name': 'Courier New',
            #         'color': '#92D050'
            #     },
            #     'num_font': {
            #         'name': 'Arial',
            #         'color': '#00B0F0',
            #     },
            # })

            # chart.set_y_axis({
            #     'name': 'Units',
            #     'name_font': {
            #         'name': 'Century',
            #         'color': 'red'
            #     },
            #     'num_font': {
            #         'bold': True,
            #         'italic': True,
            #         'underline': True,
            #         'color': '#7030A0',
            #     },
            # })
            
            
            # Turn off chart legend. It is on by default in Excel.
            chart.set_legend({'position': 'none'})
            chart2.set_legend({'position': 'none'})
            
            # Insert the chart into the worksheet.
            worksheet.insert_chart('E2', chart)
            worksheet2.insert_chart('E2', chart2)


            # Close the Pandas Excel writer and output the Excel file.
            writer.close()
###############################################################################

