# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 13:45:27 2022

@author: Cyrus

edit notes: 
1.need to add std info to add std informed max conditions (done)
2.edit outputs to be uniform, background target (done)
3.modify to give only one output type at a time. (done)
4.max sequential targets still had some investigation print lines.(done)
5.create mean and std informed max conditions
6.add option for multiple nonsequential targets (done)
"""
import numpy as np
import pandas as pd
import matplotlib

def int_to_bool_list(decimal_bx,binary_digits):
        return [bool(decimal_bx & (1<<n)) for n in range(binary_digits)]
    
def bool_list_to_int(bool_list):
        return int(''.join(map(str, map(int, bool_list))), 2)


#target classes
# target_class1 = np.arange(471,512, dtype = "int")
# target_class2 = np.arange(512,553, dtype = "int")
target_class1 = np.arange(509,515, dtype = "int")
target_class2 = np.arange(515,521, dtype = "int")
# target_classes = numpy.vstack((target_class1,target_class2))



#range
no_of_bits = 10
range_max = 2**no_of_bits
range_set = np.arange(range_max)

#parameters
screen_out_equal_or_less = 2
starting_background_target_number = 3

#individal digits backgrounds
number_of_nonsequential_targets = 1
background_target_size = 100
count_after_screenout = True

#continous target backgrounds
number_of_continuous_targets = 16
continuous_background_target_length = 12
# count_of_possible_continuous_nonoverlapping_targets = True

#value of avg background selection
closest_to_value = 5

output_type = "random_post_screening"
#output types: "random_post_screening"
#              "max_individual_hamming"
#              "closest_hamming_to_x" (not ready)
#              "max_continuous_hamming"
#              "closest_continuous_hamming_to_x" (not ready)
#              "random_continous_targets" 

#create hamming table==========================================================

#create boolean arrays
    #each digit in the target classes
    #each digit in the range, except the target classes.
    
target_digits = np.concatenate((target_class1,target_class2),axis=None)

#remove range and target overlap 
range_set = np.delete(range_set,np.isin(range_set,target_digits))
target_binary_dict = {}
range_binary_dict = {}
for target_digit in target_digits:
    temp_target_binary = int_to_bool_list(target_digit,no_of_bits)
    target_binary_dict.update({target_digit:temp_target_binary})

for range_digit in range_set:
    temp_range_binary = int_to_bool_list(range_digit,no_of_bits)
    range_binary_dict.update({range_digit:temp_range_binary})

#binary digit dictionaries for both targets and range
target_binary_df = pd.DataFrame(target_binary_dict)
range_binary_df = pd.DataFrame(range_binary_dict)

# target_binary_df.columns
# b1 = sum_holder.loc[sum_holder["sched"] == sched_row, "B1"]

#set range column to be all possible decimal digits
hamming_df = pd.DataFrame({"Range":range_binary_df.columns})
print("finding Hamming distance for...",end = " ")
#calculate the hamming distance for target x all range values
for t_no in target_binary_df.columns:
    t_no_hamming_holder = []
    
    print(t_no,end=" ")
    for r_no in range_binary_df.columns:
        temp_compare = target_binary_df.loc\
                        [target_binary_df[t_no] != range_binary_df[r_no],t_no]
        temp_hamming = len(temp_compare)
        t_no_hamming_holder.append(temp_hamming)
    hamming_df[t_no] = t_no_hamming_holder
    
# hamming_df.set_index("Range")
print("")
# print(hamming_df.columns)
temp_screened_hammings_df = hamming_df
# print(hamming_df[471].iloc[1:10])
# # class_23 = titanic[titanic["Pclass"].isin([2, 3])]
# zero471 = len(hamming_df[hamming_df[471].isin([0])])
# print(f' 471 number of zeros = {zero471}')
# one471 = len(hamming_df[hamming_df[471].isin([1])])
# print(f' 471 number of ones = {one471}')
# all471 = len(hamming_df[471])
# print(f' 471 numbers total = {all471}')
# print("")
# print("rows remaining...", end=" ")

#low hamming distance screening process =======================================
current_rows = len(temp_screened_hammings_df.iloc[:,1])
print(f'started at {current_rows} rows.')
print(f'all range rows with a Hamming distance of {screen_out_equal_or_less} or less will be removed.')
for i in hamming_df.columns:
    if i == "Range":
        continue
    temp_screened_hammings_df = temp_screened_hammings_df\
                                [temp_screened_hammings_df[i] > screen_out_equal_or_less]
    current_temp_rows = len(temp_screened_hammings_df.iloc[:,1])
    removed_temp_rows = current_rows - current_temp_rows
    current_rows = current_temp_rows
    # t = which column (target class digit) we are checking
    # r = numer of rows (range digits) we removed due to the screening
    print(f't{i}', end = "")
    print(f'-{removed_temp_rows}r',end=" ")
print("\n")
final_rows = len(temp_screened_hammings_df.iloc[:,1])
screened_hammings_df = temp_screened_hammings_df
print(f'final row count = {final_rows}')

#add mean hamming distance and standard diviation for each range digit
screened_hammings_df['mean'] = screened_hammings_df.drop(["Range"],axis=1).mean(axis=1)
screened_hammings_df['std'] = screened_hammings_df.drop(["Range",'mean'],axis=1).std(axis=1)

# MOVE TO MEAN&STD SORTED======================================================
# #sort by mean values, then standard deviation values
# screened_hammings_df.sort_values(by = ['mean', 'std'], ascending = [False, True], na_position = 'first',inplace=True)
# 
# #reset index and remove old index values
# screened_hammings_df.reset_index(inplace=True)
# screened_hammings_df = screened_hammings_df.drop("index", axis = 1)
# =============================================================================

#print lines for investigations
# screened_hammings_df['sum'] = screened_hammings_df.drop(["Range","mean"],axis=1).sum(axis=1)
# print(screened_hammings_df['mean'])
# print(screened_hammings_df['sum'])
# print(screened_hammings_df.shape)
# print(screened_hammings_df.iloc[2,:])
# screened_hammings_df.iloc[2,1:9].hist()


#final product = screened_hammings_df
#low hamming distance screening process FINISHED ==============================

#non-sequential background digit quanity check ================================
available_digits = len(screened_hammings_df)

if background_target_size > available_digits:
    print(f'not enough available digits({available_digits})\
          for the target size({background_target_size}!)')
    raise ValueError

#non-sequential background digit quanity check FINISHED========================



    


#random non-sequential digit background process================================
#number_of_nonsequential_targets
#starting_background_target_number
#convert common veriable to process specific variable
potential_targets_df = screened_hammings_df
target_number1 = starting_background_target_number

collected_targets1 = {}
for target_no in range(1,number_of_nonsequential_targets+1):
    #make the range into a list and choose values randomly
    potential_background_list = potential_targets_df['Range'].values.tolist()
    random_background = np.random.choice(potential_background_list,background_target_size,replace = False)
    
    #remove already chosen 'Range' values from dataframe
    potential_targets_df = potential_targets_df[~potential_targets_df["Range"].isin(random_background)]
    collected_targets1.update({target_number1:random_background})
    
    
    #escape loop if number of targets reached
    if target_no >= number_of_nonsequential_targets:
        break
    
    target_number1 += 1
    
    available_digits = len(potential_targets_df)
    if background_target_size > available_digits:
        print(f'not enough available digits({available_digits})\
              for the target size({background_target_size}!)')
        print(f'only {target_no} of {number_of_nonsequential_targets} targets generated')
        raise ValueError

print(collected_targets1)
#final product = collected_targets1 (dictionary {int:np.array})
#random non-sequential digit background process FINISHED=======================


# max individual digit background process (mean only)==========================

#number_of_nonsequential_targets
#starting_background_target_number
#convert common veriable to process specific variable
potential_meanmax_targets_df = screened_hammings_df
target_number2 = starting_background_target_number

#checking the number of unique mean hamming distances
unique_means = potential_meanmax_targets_df['mean'].unique()
print(potential_meanmax_targets_df['mean'].unique())

#fix order, just in case it is not in order
unique_means = np.sort(unique_means)

#change order from ascending to decending
unique_means = np.flip(unique_means)

#investigation printing
# for uni_mean in unique_means:
#     count_means = len(potential_meanmax_targets_df[potential_meanmax_targets_df['mean']==uni_mean])
#     print(f'mean = {uni_mean}, qty = {count_means}')
    
collected_targets2 = {}
temp_meanmax_background = []
for target_no2 in range(1,number_of_nonsequential_targets+1):
    remianing_digit_counter = background_target_size
    for uni_mean in unique_means:
        range_at_value = potential_meanmax_targets_df[potential_meanmax_targets_df['mean']==uni_mean]
        count_at_value = len(range_at_value)
        # print(f'count_at_value = {count_at_value}')
        # print(f'remianing_digit_counter = {remianing_digit_counter}')
        range_list = range_at_value["Range"].values.tolist()
        # print(f'range_at_value list = {range_list}')
        if count_at_value != 0:
            
            if count_at_value <= remianing_digit_counter:
                #if the current number of digits at this mean is less than the remaining
                #number of digits needed, take all digits
                temp_meanmax_background.extend(range_list)
                # print(temp_meanmax_background)
                # print(f'background length = {len(temp_meanmax_background)}')
                remianing_digit_counter = remianing_digit_counter-count_at_value
                #target_range_hamming_df = target_range_hamming_df[~target_range_hamming_df["Range"].isin(delete_range)]
                potential_meanmax_targets_df = potential_meanmax_targets_df[~potential_meanmax_targets_df['mean']==uni_mean]
            else:
                #if the current number of digits at this mean greater than remianing_digit_counter
                #randomly take digits from the range and escape from loop
                chosen_values = np.random.choice(range_list,remianing_digit_counter,replace = False)
                temp_meanmax_background.extend(chosen_values)
                potential_meanmax_targets_df = potential_meanmax_targets_df[~potential_meanmax_targets_df['Range'].isin(chosen_values)]
                # print(f'background length = {len(temp_meanmax_background)}')
                
                break
    temp_meanmax_background_ar = np.array(temp_meanmax_background)
    collected_targets2.update({target_number2:temp_meanmax_background_ar})
    
    
    #escape loop if number of targets reached
    if target_number2 >= number_of_nonsequential_targets:
        break
    target_number2 += 1
    
    available_digits = len(potential_meanmax_targets_df)
    if background_target_size > available_digits:
        print(f'not enough available digits({available_digits})\
              for the target size({background_target_size}!)')
        print(f'only {target_no} of {number_of_nonsequential_targets} targets generated')
        raise ValueError
        
print(collected_targets2)

# final product = collected_targets2 (dictionary - int:np.array)
# max individual digit background process (mean only) FINISHED=================

#consecutive targets process (all) ============================================

#shorten/localize perameter name
target_length = continuous_background_target_length
screened_background_df = screened_hammings_df

#sort background list
all_background_list = screened_background_df['Range'].values.tolist()
all_background_list = np.sort(all_background_list)
# print(f'all_background_list = {all_background_list}')

#for loop finds all possible digits in the all background list that:
#have {target_length} number of digits sequentially "in front" of it
#the targets of these digits may overlap (and often do) 
#the possible_target_list is the product of this process
length_counter = 0
possible_target_list = []
past_digit = -1

for current_number in all_background_list:
    length_counter += 1
    if past_digit == -1:
        past_digit = current_number
        continue
    # print(f'past_digit = {past_digit}, current = {current_number}')
    # print(f'l = {length_counter},',end=" " )
    if (past_digit + 1) != current_number:
        # print('break!')
        past_digit = current_number
        length_counter = 0
        continue    
    
    if length_counter >= target_length:
        possible_target_list.append(current_number-target_length) 

    past_digit = current_number
# print(f'potential_targets = {len(possible_target_list)}')

#convert list to an np.array
any_possible_target_list_ar = np.array(possible_target_list)

#check if array is empty
if not np.any(any_possible_target_list_ar):
    print('the possible target list is empty!')
    raise ValueError

#subproduct: any_possible_target_list_ar (np.array)
#consecutive targets process (all) FINISHED====================================


#random consecutive targets process ===========================================

#covert to process specific variable
target_number3 = starting_background_target_number
possible_target_list_ar = any_possible_target_list_ar

#for loop collects one target per loop
collected_targets3 = {}    
for t in range(1,number_of_continuous_targets+1):
    # print(f'potential_targets = {len(possible_target_list_ar)}')
    
    #check if array is empty
    if not np.any(possible_target_list_ar):
        print(f'there are no more possible targets after {len(collected_targets3.keys())} were chosen!')
        print(f'target list = {collected_targets3.keys()}')
        raise ValueError
    
    #randomly choose from possible_target_list_ar
    temp_target = np.random.choice(possible_target_list_ar,1)
    temp_target_range = np.arange(temp_target,temp_target+target_length+1)
    
    #remove overlapping values from the possible_target_list_ar, looking forwards and backwards 
    delete_range = np.arange(temp_target-target_length+1,temp_target+target_length+1)
    possible_target_list_ar = np.delete(possible_target_list_ar,np.isin(possible_target_list_ar,delete_range))
    
    #add target to the dictionary
    collected_targets3.update({target_number3:temp_target_range})
    target_number3 += 1
    
print(f'collected_targets3 = {collected_targets3}')    
  
#final product: collected_targets3 (dictionary)
#random consecutive targets process FINISHED===================================    


#max consecutive targets process (mean only)==============================================


#renaming
possible_max_target_list_ar = any_possible_target_list_ar
target_number4 = starting_background_target_number
all_background_df = screened_hammings_df
# print(f'possible_max_target_list_ar len = {possible_max_target_list_ar.size}')

target_range_hamming_dic = {}

#get the average hamming for each possible target
for p_target in possible_max_target_list_ar:
    #create the range for this individual target, based on target_length 
    p_target_range = np.arange(p_target,p_target+target_length+1).tolist()
    # print(f'range = {p_target_range}')
    
    #get the mean of the average digit hamming distance for the entire target 
    temp_target_hamming = all_background_df.loc\
        [all_background_df["Range"].isin(p_target_range),"mean"].mean()
    
    #store the mean in the dictionary
    target_range_hamming_dic.update({p_target:temp_target_hamming})
    
    #unused code trying to the do the same thing in a different way
    # index_range = np.arange(len(target_range_hamming_dic.keys()))
    
#target_range_hamming_df = pd.DataFrame.from_dict\
#    (target_range_hamming_dic,orient='columns',index=[index_range],columns=['keys','values'])

#set up pd.dataframe from dictionary
#range is the index, and there is one column,"hamming_dist"

#print for checking dictionary length
# print(f'len = {len(target_range_hamming_dic.keys())}')

target_range_hamming_df = pd.DataFrame.from_dict\
    (target_range_hamming_dic,orient='index',columns=["hamming_dist"])

#make the range its own column, instead of the index
target_range_hamming_df.reset_index(inplace=True)
target_range_hamming_df = target_range_hamming_df.rename(columns = {'index':'Range'})

#sort dataframe by the hamming_dist value in descending order (highest first)
target_range_hamming_df = target_range_hamming_df.sort_values("hamming_dist",ascending=False)

#reset index and remove old index values
target_range_hamming_df.reset_index(inplace=True)
target_range_hamming_df = target_range_hamming_df.drop("index", axis = 1)

#note which rows have duplicate hamming distance values with 'True' in the new duplicates column
target_range_hamming_df['duplicates'] = target_range_hamming_df.duplicated(subset="hamming_dist", keep=False)
# print(f'df size = {len(target_range_hamming_df.index)}')
# print(f'df head20 = {target_range_hamming_df.head(20)}')

#target collection loop
targets_chosen = []
duplicate_rows = False
past_hamming_value = -1
number_targets_chosen = 0
temp_target_list = []
# test_error_counter = 0

#run through every value in the datafrom from 0 upwards
for ind in target_range_hamming_df.index:
    
    #if the value was removed in a previous iteration, skip this value
    try:
        target_range_hamming_df['Range'][ind]
    except:
        # print('removed ind')
        # test_error_counter += 1
        # print(f'{ind}')
        continue
    
    #current range digit under investigation    
    current_hamming_value = target_range_hamming_df['hamming_dist'][ind]
    
    #if the is the first loop, set the past_hamming_value to the current one
    if past_hamming_value == -1:
        past_hamming_value = current_hamming_value
    
    #case: dup = true, hammings match
    #since there is potentially a duplicate, add this to a list and move to next value
    #the hamming value check is to make sure the transition between two different
    #sets with duplicates is caught
    if target_range_hamming_df['duplicates'][ind] == True and\
        past_hamming_value == current_hamming_value:
        # print("case: dup = true, hammings match")
        #add to list
        temp_target_list.append(target_range_hamming_df['Range'][ind])
        # print(f'ttl-len = {len(temp_target_list)}', end = " ")
        
        #shows that the previous row had a duplicate
        duplicate_rows = True
        #go collect next value
        continue
    
    #case: previous rows had the same hammings and were duplicates, but the current isn't
    #critical element is that duplicate_rows == True, indicating we are recording a
    #temp_target_list
    elif past_hamming_value != current_hamming_value and duplicate_rows == True:
        # print('previous rows had the same hammings and were duplicates, but the current isnt')
        # print(f'past hamming = {past_hamming_value}, current = {current_hamming_value}')
        print_dup_value = target_range_hamming_df['duplicates'][ind]
        # print(f'dup val = {print_dup_value}')
        while len(temp_target_list) != 0 and number_targets_chosen < number_of_continuous_targets:
            #complete one choice on temp_target_list
            temp_choice = np.random.choice(temp_target_list,1)
            
            number_targets_chosen += 1
            #add chosen target to targets_chosen list
            targets_chosen.append(temp_choice)
            
            #remove conflicting targets from temp_target_list, and target_range_hamming_df
            delete_range = np.arange(temp_choice-target_length,temp_choice+target_length+1)
            # print("case = not dup, p_target_list")
            # print('pre')
            # print(f'temp_choice = {temp_choice}')
            # print(delete_range)
            # print(target_range_hamming_df)
            # print(temp_target_list)
            target_range_hamming_df = target_range_hamming_df[~target_range_hamming_df["Range"].isin(delete_range)]
            temp_target_list = np.delete(temp_target_list,np.isin(temp_target_list,delete_range))
            # print("post")
            # print(target_range_hamming_df)
            # print(temp_target_list)
        if number_targets_chosen == number_of_continuous_targets:
            break
        
        duplicate_rows = False
        temp_target_list = []
        
        #if the current 'range' digit was deleted by the previous process (while loop)
        #go to the next range digit
        try:
            target_range_hamming_df['Range'][ind]
        except:
            # print('removed ind while in -> case = not dup, p_target_list')
            # remaining_digits = len(target_range_hamming_df['Range'])
            # print(f'remaining = {remaining_digits}')
            continue
        
        if target_range_hamming_df['duplicates'][ind] == False:
            #take care of the current nonduplicate range number 
            temp_choice = target_range_hamming_df['Range'][ind]
            targets_chosen.append(temp_choice)
            # print("case = not dup, post false value")
            # print('pre')
            # print(f'temp_choice = {temp_choice}')
            # print(delete_range)
            # print(target_range_hamming_df)
            # print(temp_target_list)
            
            delete_range = np.arange(temp_choice-target_length,temp_choice+target_length+1)
            target_range_hamming_df = target_range_hamming_df[~target_range_hamming_df["Range"].isin(delete_range)]
            # print("post")
            # print(target_range_hamming_df)
            # print(temp_target_list)
            number_targets_chosen += 1
            
            if number_targets_chosen == number_of_continuous_targets:
                break
            
        else:
            # if the 'duplicates' column shows true, do same as the 
            #case: dup = true, hammings match
            #add to list
            # print('dup = true, after hamming mismatch')
            temp_target_list.append(target_range_hamming_df['Range'][ind])
             
            #shows that this row is known to have a duplicate
            duplicate_rows = True
            #go collect next value
            continue
                    
    #case not a duplicate
    elif target_range_hamming_df['duplicates'][ind] == False and duplicate_rows == False:    
        # print('case not a duplicate')
        #as long as there is no duplicates, you can just choose it
        temp_choice = target_range_hamming_df['Range'][ind]
        targets_chosen.append(temp_choice)
        number_targets_chosen += 1
     
        if number_targets_chosen == number_of_continuous_targets:
            break    
        #remove conflicting targets from target_range_hamming_df
        delete_range = np.arange(temp_choice-target_length,temp_choice+target_length+1)
        # print("case = not dup, unique")
        # print('pre')
        # print(f'temp_choice = {temp_choice}')
        # print(delete_range)
        # print(target_range_hamming_df)
        # print(f'temp_choice = {temp_choice}')
        # print("df in delete range:")
        # print(target_range_hamming_df[target_range_hamming_df["Range"].isin(delete_range)])
        
        target_range_hamming_df = target_range_hamming_df[~target_range_hamming_df["Range"].isin(delete_range)]
        # target_range_hamming_df.drop(target_range_hamming_df[target_range_hamming_df["Range"].isin(delete_range)],axis = 0, inplace = True)
        # print("post")
        # print(target_range_hamming_df)

        #this shouldn't be necessary, but you know.. paranoid
        temp_target_list = []

#this is to catch the situation where all digits are duplicates 
#(this happens with mirror targets), or when the last few are duplicates
while len(temp_target_list) != 0 and number_targets_chosen < number_of_continuous_targets:
    # print('final catch')
    #complete one choice on temp_target_list
    # print(f'temp_target_list = {temp_target_list}')
    temp_choice = np.random.choice(temp_target_list,1)
    
    number_targets_chosen += 1
    #add chosen target to targets_chosen list
    targets_chosen.append(temp_choice)
    delete_range = np.arange(temp_choice-target_length,temp_choice+target_length+1)
    #remove conflicting targets from temp_target_list, and target_range_hamming_df
    # print("case = end_catch")
    # print('pre')
    # print(f'temp_choice = {temp_choice}')
    # print(f'delete_range = {delete_range}')
    # print(target_range_hamming_df)
    # print(temp_target_list)
    target_range_hamming_df = target_range_hamming_df[~target_range_hamming_df["Range"].isin(delete_range)]
    temp_target_list = np.delete(temp_target_list,np.isin(temp_target_list,delete_range))
    # print("post")
    # print(f'targets_chosen length = {len(targets_chosen)}')
    # print(target_range_hamming_df)
    # print(temp_target_list)
    # range_set = np.delete(range_set,np.isin(range_set,target_digits))
    

if number_targets_chosen < number_of_continuous_targets:
    print(f'End catch: Error! number_targets_chosen({number_targets_chosen}) is less than number_of_continuous_targets({number_of_continuous_targets})!')
    raise ValueError
    
chosen_targets_max = {}
for temp_target2 in targets_chosen:
    temp_range2 = np.arange(temp_target2,temp_target2+target_length+1)
    chosen_targets_max.update({target_number4:temp_range2})
    target_number4 += 1
    
print(f'targets chosen (max type) = {chosen_targets_max}')    

#final product:   chosen_targets_max (dictionary)
#max consecutive targets process (mean only) FINISHED==========================

    # print(df['Name'][ind], df['Stream'][ind])
#for each possible target, get the average hamming for the entire target.
#sequence the target choices by max hamming
#grab target by max hamming
#remove overlapping targets
#repeat

# print("post screening")
# print(temp_screened_hammings_df["Range"])    
# print(len(temp_screened_hammings_df[500]))
# true_list500 = target_binary_df.loc[target_binary_df[500]== True,500]
# true_list501 = target_binary_df.loc[target_binary_df[501]== True,501]
# compare_list500 = target_binary_df.loc\
#                   [target_binary_df[500] != target_binary_df[501],500]
# print(target_binary_df[500] != target_binary_df[501])
# # compare_list = target_binary_df.loc[target_binary_df[500]== \
# #                target_binary_df.loc[target_binary_df[501]],500]

# print(target_binary_dict[500])
# print(target_binary_dict[501])
# print(len(true_list500))
# print(len(true_list501))
# print(compare_list500)
# print(len(compare_list500))
# print(compare_list)
#compare lists to get hammining distance per digit in target class
#and put this into a matching array

#screen out numbers with hamminging distances lower than the screen out values

#count the remaining numbers in the range

#calucuate a average hamming value for each range digit

#return max values

#find values closes to X, and return those values 

#calcuate the number of possible continous targets
#calculate the number of possible continous targets without overlap

