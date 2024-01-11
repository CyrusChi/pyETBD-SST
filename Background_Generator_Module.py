# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 11:37:23 2022

@author: Cyrus
"""
import numpy as np
import pandas as pd
from numba import njit
import General_Functions_Module as gen_funct
# import matplotlib

@njit
def int_to_bool_list(decimal_bx,binary_digits):
        return [bool(decimal_bx & (1<<n)) for n in range(binary_digits)]
    
def bool_list_to_int(bool_list):
        return int(''.join(map(str, map(int, bool_list))), 2)

class Background_Generator:
    subclasses = {}
    
    # target classes
    target_dict = {}
    passive_removal_dict = {}
    
    #range
    no_of_bits = None
    range_max = None
    range_set = None

    #parameters
    screen_out_equal_or_less = None
    starting_background_target_number = None
    remove_avg_hamming_equal_or_less = None
    remove_std_hamming_equal_or_greater = None
    removal_function_type = None
    
    #individal digits backgrounds
    number_of_nonsequential_targets = None
    nonsequential_background_target_size = None
   
    #continous target backgrounds
    number_of_continuous_targets = None
    continuous_background_target_length = None


    #value of avg background selection
    closest_to_value = None

    # output_type = "random_nonsequential_post_screening"
    #output types: "random_nonsequential_post_screening"
    #              "max_mean_nonsequential_post_screening"
    #              "max_mean_std_nonsequential_post_screening"
    #              "max_mean_continuous_post_screening"
    #              "max_mean_std_continuous_post_screening" 
    #              "random_continuous_post_screening" 
    #              "closest_hamming_to_x_nonsequential" (not implemented)
    #              "closest_hamming_to_x_continuous" (not implemented)

    
    def __init__(self):
       pass
    
    @classmethod
    def clear_background_dicts(cls):
        cls.target_dict = {}
        cls.passive_removal_dict = {}

    @classmethod
    def set_no_of_bits(cls,no_of_bits):
        cls.no_of_bits = no_of_bits
        cls.range_max = 2**no_of_bits
        cls.range_set = np.arange(cls.range_max)
        
    @classmethod
    def setup(cls,no_of_bits,start_id,target_dict,background_generator_settings,passive_removal = None):
        
        cls.set_no_of_bits(no_of_bits)
        cls.starting_background_target_number = int(start_id)
        cls.target_dict = target_dict
        if passive_removal != None:
            cls.passive_removal_dict = passive_removal
        for key in background_generator_settings.keys():
            #parameters
            if key == "screen_out_equal_or_less":
                cls.screen_out_equal_or_less = background_generator_settings[key]
            if key == "remove_avg_hamming_equal_or_less":
                cls.remove_avg_hamming_equal_or_less = background_generator_settings[key]
            if key == "remove_std_hamming_equal_or_greater":    
                cls.remove_std_hamming_equal_or_greater = background_generator_settings[key]
            if key == "removal_function_type":      
                cls.removal_function_type = background_generator_settings[key]
            
                #individal digits backgrounds
            if key == "number_of_nonsequential_targets":      
                cls.number_of_nonsequential_targets = background_generator_settings[key]
            if key == "nonsequential_background_target_size":      
                cls.nonsequential_background_target_size = background_generator_settings[key]
               
                #continous target backgrounds
            if key == "number_of_continuous_targets":     
                cls.number_of_continuous_targets = background_generator_settings[key]
            if key == "continuous_background_target_length":      
                cls.continuous_background_target_length = background_generator_settings[key]
            
   
    @classmethod
    def default_setup(cls):
        # target_class1 = np.arange(509,515, dtype = "int")
        # target_class2 = np.arange(515,521, dtype = "int")
        target_class1 = np.arange(471,512, dtype = "int")
        target_class2 = np.arange(512,553, dtype = "int") 
        
        cls.target_dict.update({1:target_class1,2:target_class2})
        cls.passive_removal_dict = {}
               
        # target_classes = numpy.vstack((target_class1,target_class2))

        #range
        cls.set_no_of_bits(10)
        # cls.no_of_bits = 10
        # cls.range_max = 2**cls.no_of_bits
        # cls.range_set = np.arange(cls.range_max)

        #parameters
        cls.screen_out_equal_or_less = 1
        cls.starting_background_target_number = 3
        cls.remove_avg_hamming_equal_or_less = None #.2
        cls.remove_std_hamming_equal_or_greater = .8 #.8
        cls.removal_function_type = 'percentage'
        
        #noncontinuous target backgrounds
        cls.number_of_nonsequential_targets = 1
        cls.nonsequential_background_target_size = 400

        #continous target backgrounds
        cls.number_of_continuous_targets = 2
        cls.continuous_background_target_length = 40
        
        #value of avg background selection (not ready)
        cls.closest_to_value = 5
    
    @classmethod
    def settings_check(cls,check_type = None):
        check_failure = False
        error_items = ""
        blank_settings = ""
        # #individal digits backgrounds
        # number_of_nonsequential_targets = None
        # nonsequential_background_target_size = None
       
        # #continous target backgrounds
        # number_of_continuous_targets = None
        # continuous_background_target_length = None
        # print(f'blank_settings = {blank_settings}')
        
        if check_type == None:
            print(f'check_type = {check_type}')
            print('it is assumed that the correct default settings will be used')
            print('and that checking is not required')
        elif check_type == "basic":
            print(f'check_type = {check_type}')
            if not cls.target_dict:
                check_failure = True
                error_items = ''.join([error_items,'target_dict, '])
            if cls.no_of_bits == None:
                check_failure = True
                error_items = ''.join([error_items,'no_of_bits, '])
            if cls.range_max == None:
                check_failure = True
                error_items = ''.join([error_items,'range_max, '])
            if cls.range_set.all() == None:
                check_failure = True
                error_items = ''.join([error_items,'range_set, '])            
            if cls.starting_background_target_number == None:
                check_failure = True
                error_items = ''.join([error_items,'starting_background_target_number, '])
            if cls.removal_function_type == None:
                blank_settings = ''.join([blank_settings,'removal_function_type (default=value), '])
                # print(f'blank_settings = {blank_settings}')
            if cls.screen_out_equal_or_less == None or cls.screen_out_equal_or_less == 0:
                blank_settings = ''.join([blank_settings,'screen_out_equal_or_less, '])
                # print(f'blank_settings = {blank_settings}')
            if cls.remove_avg_hamming_equal_or_less == None:
                blank_settings = ''.join([blank_settings,'remove_avg_hamming_equal_or_less, '])
                # print(f'blank_settings = {blank_settings}')
            if cls.remove_std_hamming_equal_or_greater == None:
                blank_settings = ''.join([blank_settings,'remove_std_hamming_equal_or_greater, '])
                # print(f'blank_settings = {blank_settings}')
            if not cls.passive_removal_dict:
                blank_settings = ''.join([blank_settings,'passive_removal_dict, '])
                
        elif check_type == "noncontinuous":
            print(f'check_type = {check_type}')
            if cls.number_of_nonsequential_targets == None:
                check_failure = True
                error_items = ''.join([error_items,'number_of_nonsequential_targets, '])
            if cls.nonsequential_background_target_size == None:
                check_failure = True
                error_items = ''.join([error_items,'nonsequential_background_target_size, '])
                
        elif check_type == "continuous":
            print(f'check_type = {check_type}')
            if cls.number_of_continuous_targets == None:
                check_failure = True
                error_items = ''.join([error_items,'number_of_continuous_targets, '])
            if cls.continuous_background_target_length == None:
                check_failure = True
                error_items = ''.join([error_items,'continuous_background_target_length, '])
        else:
            print('check type chosen is not on the list!')
            raise KeyError
        
        
        if len(blank_settings) != 0:
            print("The following parameters are unused:")
            print(f'{blank_settings}')
            print('\n')
        if check_failure == True:
            print("The following settings are missing:")
            print(f'{error_items}')
            print('\n')
            raise ValueError
        
    # @classmethod
    # def is_se_new(cls,se_value):
    #     if se_value in cls.Behaviors:
    #         # print("is_se_new is returning False")
    #         return False
    #     else:
    #         # print("is_se_new is returning True")
    #         return True
    @staticmethod
    def hamming_distance_comparison(target1,target2,no_of_bits,return_type ='mean_std'):
        target1_binary_dict = {}
        target2_binary_dict = {}
        
        for target1_digit in target1:
            temp_target_binary = int_to_bool_list(target1_digit,no_of_bits)
            target1_binary_dict.update({target1_digit:temp_target_binary})
        
        for target2_digit in target2:
            temp_range_binary = int_to_bool_list(target2_digit,no_of_bits)
            target2_binary_dict.update({target2_digit:temp_range_binary})
        
        #binary digit dictionaries for both targets and range
        target1_binary_df = pd.DataFrame(target1_binary_dict)
        target2_binary_df = pd.DataFrame(target2_binary_dict)
        
        # target1_binary_df.columns
        # b1 = sum_holder.loc[sum_holder["sched"] == sched_row, "B1"]
        
        #set range column to be all possible decimal digits
        hamming_df = pd.DataFrame({"Range":target2_binary_df.columns})
        print("finding Hamming distance for...",end = " ")
        #calculate the hamming distance for target x all range values
        for t_no in target1_binary_df.columns:
            t_no_hamming_holder = []
            
            print(t_no,end=" ")
            for r_no in target2_binary_df.columns:
                temp_compare = target1_binary_df.loc\
                                [target1_binary_df[t_no] != target2_binary_df[r_no],t_no]
                temp_hamming = len(temp_compare)
                t_no_hamming_holder.append(temp_hamming)
            hamming_df[t_no] = t_no_hamming_holder
            
        # hamming_df.set_index("Range")
        print("")
        # print(hamming_df.columns)
        hammings_comparison_matrix_df = hamming_df
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
        
        #add mean hamming distance and standard diviation for each range digit
        hammings_comparison_matrix_df['mean'] = hammings_comparison_matrix_df.drop(["Range"],axis=1).mean(axis=1)
        hammings_comparison_matrix_df['std'] = hammings_comparison_matrix_df.drop(["Range",'mean'],axis=1).std(axis=1)
        if return_type == 'mean_std':
            #get the mean of the average digit hamming distance for the entire target 
            avg_target_hamming_mean = hammings_comparison_matrix_df['mean'].mean()
            avg_target_hamming_std = hammings_comparison_matrix_df['std'].mean()
            data_dict = {'mean':avg_target_hamming_mean,"std":avg_target_hamming_std}    
            return data_dict
        elif return_type == 'matrix':
            return hammings_comparison_matrix_df

#create hamming table==========================================================    
    @classmethod
    def hamming_matrix_generation(cls):
        
        Background_Generator.settings_check("basic")
        #create boolean arrays
            #each digit in the target classes
            #each digit in the range, except the target classes.
        
        #local naming
        local_passive_removal_dict = cls.passive_removal_dict
        local_target_dict = cls.target_dict
        local_range_set = cls.range_set
        local_no_of_bits = cls.no_of_bits
        
        if local_passive_removal_dict:
            passive_removal_digits = []
            for removal_keys in local_passive_removal_dict.keys():
                if len(passive_removal_digits) == 0:
                    passive_removal_digits = local_passive_removal_dict[removal_keys]
                    continue        
            
                passive_removal_digits = np.concatenate((passive_removal_digits,local_passive_removal_dict[removal_keys]),axis=None)
        
        target_digits = []
        for target_keys in local_target_dict.keys():
            if len(target_digits) == 0:
                target_digits = local_target_dict[target_keys]
                continue
            
            target_digits = np.concatenate((target_digits,local_target_dict[target_keys]),axis=None)

        #remove range and target overlap 
        range_set = np.delete(local_range_set,np.isin(local_range_set,target_digits))
        #remove passive range (for other background targets)
        if local_passive_removal_dict:
            range_set = np.delete(local_range_set,np.isin(local_range_set,passive_removal_digits))
        
        target_binary_dict = {}
        range_binary_dict = {}
        for target_digit in target_digits:
            temp_target_binary = int_to_bool_list(target_digit,local_no_of_bits)
            target_binary_dict.update({target_digit:temp_target_binary})

        for range_digit in range_set:
            temp_range_binary = int_to_bool_list(range_digit,local_no_of_bits)
            range_binary_dict.update({range_digit:temp_range_binary})

        #binary digit dictionaries for both targets and range
        target_binary_df = pd.DataFrame(target_binary_dict)
        range_binary_df = pd.DataFrame(range_binary_dict)

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

        print("")

        hammings_comparison_matrix_df = hamming_df.copy()
        
        return hammings_comparison_matrix_df
###############################################################################
#create hamming table v2========================================================    
    @classmethod
    def fast_hamming_matrix_generation(cls):
        
        Background_Generator.settings_check("basic")
        #create boolean arrays
            #each digit in the target classes
            #each digit in the range, except the target classes.
        
        #local naming
        local_passive_removal_dict = cls.passive_removal_dict
        local_target_dict = cls.target_dict
        local_range_set = cls.range_set
        local_no_of_bits = cls.no_of_bits
        
        if local_passive_removal_dict:
            passive_removal_digits = []
            for removal_keys in local_passive_removal_dict.keys():
                if len(passive_removal_digits) == 0:
                    passive_removal_digits = local_passive_removal_dict[removal_keys]
                    continue        
            
                passive_removal_digits = np.concatenate((passive_removal_digits,local_passive_removal_dict[removal_keys]),axis=None)
        
        target_digits = []
        for target_keys in local_target_dict.keys():
            if len(target_digits) == 0:
                target_digits = local_target_dict[target_keys]
                continue
            
            target_digits = np.concatenate((target_digits,local_target_dict[target_keys]),axis=None)

        #remove range and target overlap 
        range_set = np.delete(local_range_set,np.isin(local_range_set,target_digits))
        #remove passive range (for other background targets)
        if local_passive_removal_dict:
            range_set = np.delete(local_range_set,np.isin(local_range_set,passive_removal_digits))
        
        # target_binary_dict = {}

        # for target_digit in target_digits:
        #     temp_target_binary = int_to_bool_list(target_digit,local_no_of_bits)
        #     target_binary_dict.update({target_digit:temp_target_binary})

        # for range_digit in range_set:
        #     temp_range_binary = int_to_bool_list(range_digit,local_no_of_bits)
        #     range_binary_dict.update({range_digit:temp_range_binary})
        
        # print(f' target_digits = {type(target_digits)}')
        # print(f' target_digits length = {len(target_digits)}')
        # print(f' range_set = {type(range_set)}')
        # print(f' range_set length = {len(range_set)}')
        # #binary digit dictionaries for both targets and range
        # target_binary_df = pd.DataFrame(target_binary_dict)

        # #set range column to be all possible decimal digits
        hamming_df = pd.DataFrame({"Range":range_set})

        hamming_ar = Background_Generator.fast_comparison(target_digits,range_set,local_no_of_bits)
        
        for digit_index in range(len(target_digits)):
            hamming_df[target_digits[digit_index]] = hamming_ar[:,digit_index]
            # print(f'target_digits[digit_index]= {target_digits[digit_index]}')
            # print(hamming_ar[:,digit_index])

        hammings_comparison_matrix_df = hamming_df.copy()
        
        return hammings_comparison_matrix_df
    
    @njit    
    def fast_comparison(target_digits,range_set,bits):
        hamming_ar = np.zeros((len(range_set),len(target_digits))) 
        # print(hamming_ar.shape)
        #dec_to_bin(num, bits)
        #bin_to_dec(binary)
        r_count = -1
        
        for r_no in range_set:
            t_count = -1
            r_count += 1
            r_no_bin = gen_funct.dec_to_bin(r_no,bits)
            for t_no in target_digits:
                t_count += 1
                t_no_bin = gen_funct.dec_to_bin(t_no,bits)
                
                h_count = 0
                for bit in range(len(r_no_bin)):
                    if r_no_bin[bit] != t_no_bin[bit]:
                        h_count += 1
                hamming_ar[r_count,t_count] = h_count
        # print(f"r_count = {r_count}")
        # print(hamming_ar[r_count,:])    
        # print("")
        return hamming_ar
###############################################################################
#low hamming distance screening process =======================================
    @classmethod
    def low_hamming_screening(cls,pre_screened_hammings_df):
        
        individual_hamming_bar = cls.screen_out_equal_or_less
        avg_hamming_bar = cls.remove_avg_hamming_equal_or_less
        std_hamming_bar = cls.remove_std_hamming_equal_or_greater
        removal_function_type = cls.removal_function_type
        if len(pre_screened_hammings_df) == 0:
            print('no Hamming Distance pandas dataframe supplied!')
            print('use hamming_matrix_generation method to create dataframe')
            raise KeyError
        
        current_rows = len(pre_screened_hammings_df.iloc[:,1])
        print("\n")
        print(f'started at {current_rows} rows.')
        print(f'all range rows with a Hamming distance of {individual_hamming_bar} or less will be removed.')
        print("\n")
        
        if individual_hamming_bar != None:
            for i in pre_screened_hammings_df.columns:
                if i == "Range":
                    continue
                pre_screened_hammings_df = pre_screened_hammings_df\
                                            [pre_screened_hammings_df[i] > individual_hamming_bar]
                # current_temp_rows = len(pre_screened_hammings_df.iloc[:,1])
                # removed_temp_rows = current_rows - current_temp_rows
                # current_rows = current_temp_rows
                # t = which column (target class digit) we are checking
                # r = numer of rows (range digits) we removed due to the screening
                
                # print(f't{i}', end = "")
                # print(f'-{removed_temp_rows}r',end=" ")
            
            final_rows = len(pre_screened_hammings_df.iloc[:,1])
            
            print("\n")
            print(f'row count after individual hamming screening = {final_rows}')
    
        #add mean hamming distance and standard diviation for each range digit
        pre_screened_hammings_df['mean'] = pre_screened_hammings_df.drop(["Range"],axis=1).mean(axis=1)
        pre_screened_hammings_df['std'] = pre_screened_hammings_df.drop(["Range",'mean'],axis=1).std(axis=1)
                
        # b = pre_screened_hammings_df[pre_screened_hammings_df['mean'] > 4.9]
        # print(b)
        
        ps_mean_max = pre_screened_hammings_df['mean'].max()
        ps_mean_min = pre_screened_hammings_df['mean'].min()
        ps_std_max = pre_screened_hammings_df['std'].max()
        ps_std_min = pre_screened_hammings_df['std'].min()
        
        #catch user trying to sort when there is no difference betwen max and min
        #the code is set to throw an error rather than just notify the user
        #in order to make sure the user doesn't assume settings are working when they are not.
        
        if ps_mean_max == ps_mean_min and avg_hamming_bar != None:
            print('the max and the min avg hamming distances are equal!')
            print('no sorting by a percentage of the mean can occur')
            raise ValueError
            
        if ps_std_max == ps_std_min and std_hamming_bar != None:
            print('the max and the min std hamming distances are equal!')
            print('no sorting by a percentage of the mean can occur')
            raise ValueError
        
        
        if removal_function_type == 'percentage':
           
                
            if avg_hamming_bar != None:
  
                if avg_hamming_bar > 1 and avg_hamming_bar < 101:
                    avg_hamming_bar = avg_hamming_bar * 0.01 * (ps_mean_max-ps_mean_min) + ps_mean_min
                elif avg_hamming_bar <= 1 and avg_hamming_bar >= 0:
                    avg_hamming_bar = avg_hamming_bar * (ps_mean_max-ps_mean_min) + ps_mean_min
                else:
                    print(f'unexpected background avg removal number({avg_hamming_bar})')
                    print('percentage removal should be between 0 to 1(inc), or 2 to 100')
                    raise ValueError
            
            if std_hamming_bar != None:
                if std_hamming_bar > 1 and std_hamming_bar < 101:
                    std_hamming_bar = std_hamming_bar * 0.01 * (ps_std_max-ps_std_min) + ps_std_min
                elif std_hamming_bar <= 1 and std_hamming_bar > 0:
                    std_hamming_bar = std_hamming_bar * (ps_std_max-ps_std_min) + ps_std_min
                else:
                    print(f'unexpected background std removal number({avg_hamming_bar})')
                    print('percentage removal should be between 0 to 1(inc), or 2 to 100')
                    raise ValueError
                    
        elif removal_function_type == 'value':
            pass
        
        elif removal_function_type == None:
            pass
        
        else:
            print(f'removal_function_type({removal_function_type}) not recognized')
            print('currently, the only types are "percentage", "value", or None')
            raise ValueError
            
        if avg_hamming_bar != None:
            #target_range_hamming_df = target_range_hamming_df[~target_range_hamming_df["Range"].isin(delete_range)]
            #dataframe[dataframe['Percentage'] > 80]
            
            #remove everything under bar
            pre_screened_hammings_df = pre_screened_hammings_df[pre_screened_hammings_df['mean'] > avg_hamming_bar]
            length_post_avg_hamming_removal = len(pre_screened_hammings_df.iloc[:,1])
            print("\n")
            print(f'row count after avg Hamming Dist Removal = {length_post_avg_hamming_removal}')        
            
            if removal_function_type == 'percentage' or removal_function_type == 'value' or removal_function_type == None:
                print(f'removal type = {removal_function_type}')
                print('\n')
        if std_hamming_bar != None:
            #remove everything over the bar
            pre_screened_hammings_df = pre_screened_hammings_df[pre_screened_hammings_df['std'] < std_hamming_bar]
            length_post_std_hamming_removal = len(pre_screened_hammings_df.iloc[:,1])
            print("\n")
            print(f'row count after std Hamming Dist Removal = {length_post_std_hamming_removal}')    
            if removal_function_type == 'percentage' or removal_function_type == 'value' or removal_function_type == None:
                print(f'removal type = {removal_function_type}')
                print('\n')
        # c = screened_hammings_df[screened_hammings_df['mean'] > 4.9]
        # print(c)
        screened_hammings_df = pre_screened_hammings_df
        mean_max = screened_hammings_df['mean'].max()
        mean_min = screened_hammings_df['mean'].min()
        std_max = screened_hammings_df['std'].max()
        std_min = screened_hammings_df['std'].min()
        r = 3
        print(f'background range statistics, post filtering (rounded {r})')
        print(f'mean max = {round(mean_max,r)} and mean min = {round(mean_min,r)}')
        print(f'std max = {round(std_max,r)} and std min = {round(std_min,r)}')
        print('(std worst case is probably around 4.2 for a 10 digit bit string)')
        return screened_hammings_df

#consecutive targets process (all) ============================================
    @classmethod
    def potential_continuous_target_finder(cls,screened_hammings_df):
        
        Background_Generator.settings_check("continuous")
        
        #shorten/localize perameter name
        target_length = cls.continuous_background_target_length
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
        
        return any_possible_target_list_ar
        #subproduct: any_possible_target_list_ar (np.array)
        #consecutive targets process (all) FINISHED============================


###############################################################################
    @classmethod
    def register_subclass(cls, output_type):
        def decorator(subclass):
            cls.subclasses[output_type] = subclass
            return subclass
      
        return decorator    
    
    @classmethod
    def generate(cls, output_type, *args, **kargs):
        if output_type not in cls.subclasses:
            raise ValueError('Bad output type {}'.format(output_type))
      
        return cls.subclasses[output_type](*args, **kargs)
###############################################################################

###############################################################################
#changed fortesting fast hamming
@Background_Generator.register_subclass('random_nonsequential_post_screening')
class Post_Screening_Random_Noncontinuous_Background(Background_Generator):

    def __init__(self):
       pass
   
    def __new__(self,*args, **kargs):
        background_targets = Post_Screening_Random_Noncontinuous_Background.generate(*args, **kargs)
        return background_targets
    
    def generate( *args, **kargs):
        
        Background_Generator.settings_check("noncontinuous")
        pre_screened_hammings_df = Background_Generator.fast_hamming_matrix_generation()        
        # pre_screened_hammings_df = Background_Generator.hamming_matrix_generation()  
        # print(pre_screened_hammings_df)
        screened_hammings_df = Background_Generator.low_hamming_screening(pre_screened_hammings_df)
        
        #convert common veriable to process specific variable
        background_target_size = Background_Generator.nonsequential_background_target_size
        potential_targets_df = screened_hammings_df
        target_number1 = Background_Generator.starting_background_target_number
        number_of_nonsequential_targets = Background_Generator.number_of_nonsequential_targets
        
        #non-sequential background digit quanity check ========================
        available_digits = len(screened_hammings_df)
        
        if background_target_size > available_digits:
            print(f' Error! Not enough available digits({available_digits})\
                  for the target size({background_target_size}!)')
            raise ValueError
        #non-sequential background digit quanity check FINISHED================
        
        #random non-sequential digit background process========================

        collected_targets1 = {}
        for target_no in range(1,number_of_nonsequential_targets+1):
            #make the range into a list and choose values randomly
            potential_background_list = potential_targets_df['Range'].values.tolist()
            random_background = np.random.choice(potential_background_list,background_target_size,replace = False)
            
            #remove already chosen 'Range' values from dataframe
            potential_targets_df = potential_targets_df[~potential_targets_df["Range"].isin(random_background)]
            collected_targets1.update({str(target_number1):random_background})
            
            
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

        return collected_targets1
        #final product = collected_targets1 (dictionary {str:np.array})
        #random non-sequential digit background process FINISHED===============
 
###############################################################################

@Background_Generator.register_subclass('max_mean_nonsequential_post_screening')
class Post_Screening_MaxMean_Noncontinuous_Background(Background_Generator):

    def __init__(self):
       pass
   
    def __new__(self,*args, **kargs):
        background_targets = Post_Screening_MaxMean_Noncontinuous_Background.generate(*args, **kargs)
        return background_targets
    
    def generate( *args, **kargs):
        
        Background_Generator.settings_check("noncontinuous")
        pre_screened_hammings_df = Background_Generator.fast_hamming_matrix_generation()  
        # pre_screened_hammings_df = Background_Generator.hamming_matrix_generation() 
        screened_hammings_df = Background_Generator.low_hamming_screening(pre_screened_hammings_df)
        
        # max individual digit background process (mean only)==========================

        #number_of_nonsequential_targets
        #starting_background_target_number
        #convert common veriable to process specific variable
        potential_meanmax_targets_df = screened_hammings_df
        target_number2 = Background_Generator.starting_background_target_number
        number_of_nonsequential_targets = Background_Generator.number_of_nonsequential_targets
        background_target_size = Background_Generator.nonsequential_background_target_size
        #checking the number of unique mean hamming distances
        unique_means = potential_meanmax_targets_df['mean'].unique()
        # print(potential_meanmax_targets_df['mean'].unique())

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
                        # a = potential_meanmax_targets_df[potential_meanmax_targets_df['mean']==uni_mean]
                        # b = potential_meanmax_targets_df
                        # print(f'all = {b.shape}')
                        # print(f'uni-mean = {a.shape}')
                        potential_meanmax_targets_df = potential_meanmax_targets_df[~potential_meanmax_targets_df['mean'].isin([uni_mean])]
                        # print(f'all = {potential_meanmax_targets_df.shape}')
                    else:
                        #if the current number of digits at this mean greater than remianing_digit_counter
                        #randomly take digits from the range and escape from loop
                        chosen_values = np.random.choice(range_list,remianing_digit_counter,replace = False)
                        temp_meanmax_background.extend(chosen_values)
                        potential_meanmax_targets_df = potential_meanmax_targets_df[~potential_meanmax_targets_df['Range'].isin(chosen_values)]
                        remianing_digit_counter = 0
                        # print(f'background length = {len(temp_meanmax_background)}')
                        
                        break
            
            if remianing_digit_counter > 0:
                print(f'remianing_digit_counter({remianing_digit_counter}) is greater than zero!')
                print(f'not enough digits were present to finish target {target_number2}')
            
            # #remove already chosen 'Range' values from dataframe
            # potential_targets_df = potential_targets_df[~potential_targets_df["Range"].isin(random_background)]
            
            temp_meanmax_background_ar = np.array(temp_meanmax_background)
            collected_targets2.update({str(target_number2):temp_meanmax_background_ar})
            
            target_number2 += 1
            
            #clear collector list
            temp_meanmax_background = []
            
            available_digits = len(potential_meanmax_targets_df)
            if background_target_size > available_digits:
                print(f'not enough available digits({available_digits})\
                      for the target size({background_target_size}!)')
                print(f'only {target_number2} of {number_of_nonsequential_targets} targets generated')
                raise ValueError
                
        # print(collected_targets2)
        
        return collected_targets2
        # final product = collected_targets2 (dictionary - str:np.array)
        # max individual digit background process (mean only) FINISHED=========
        
###############################################################################

@Background_Generator.register_subclass('max_mean_std_nonsequential_post_screening')
class Post_Screening_MaxMeanStd_Noncontinuous_Background(Background_Generator):

    def __init__(self):
       pass
   
    def __new__(self,*args, **kargs):
        background_targets = Post_Screening_MaxMeanStd_Noncontinuous_Background.generate(*args, **kargs)
        return background_targets
    
    def generate( *args, **kargs):
        
        Background_Generator.settings_check("noncontinuous")
        pre_screened_hammings_df = Background_Generator.fast_hamming_matrix_generation()        
        # pre_screened_hammings_df = Background_Generator.hamming_matrix_generation() 
        screened_hammings_df = Background_Generator.low_hamming_screening(pre_screened_hammings_df)
        
        # MEAN&STD SORTED======================================================
        #sort by mean values, then standard deviation values
        screened_hammings_df.sort_values(by = ['mean', 'std'], ascending = [False, True], na_position = 'first',inplace=True)
        
        #reset index and remove old index values
        screened_hammings_df.reset_index(inplace=True)
        screened_hammings_df = screened_hammings_df.drop("index", axis = 1)
        # =============================================================================

        
        # max individual digit background process (mean std)==========================

        #convert common veriable to process specific variable
        potential_mean_std_max_targets_df = screened_hammings_df
        target_number5 = Background_Generator.starting_background_target_number
        number_of_nonsequential_targets = Background_Generator.number_of_nonsequential_targets
        background_target_size = Background_Generator.nonsequential_background_target_size
        
        #check availability of possible digits
        available_digits = len(potential_mean_std_max_targets_df)
        if background_target_size > available_digits:
            print(f'not enough available digits({available_digits})\
                  for the target size({background_target_size}!)')
            print('no targets generated')
            raise ValueError
        
        
        collected_targets5 = {}
        no_of_columns = len(potential_mean_std_max_targets_df.columns)
        # a = potential_mean_std_max_targets_df.iloc[0:10,no_of_columns-2:no_of_columns]
        # print(f'a out = \n{a}')
        for target_no2 in range(1,number_of_nonsequential_targets+1):
            temp_mean_std_max_background = []
            duplicate_range = []
            # a = potential_mean_std_max_targets_df.iloc[0:10,no_of_columns-2:no_of_columns]
            # print(f'a in = \n{a}')
            #reset index and remove old index values
            potential_mean_std_max_targets_df.reset_index(inplace=True)
            potential_mean_std_max_targets_df = potential_mean_std_max_targets_df.drop("index", axis = 1)
            
            # a = potential_mean_std_max_targets_df.iloc[0:10,no_of_columns-2:no_of_columns]
            # print(f'a after reset = \n{a}')
            remianing_digit_counter = background_target_size
            # range_list = potential_mean_std_max_targets_df["Range"].values.tolist()
            past_mean = None
            past_std = None
            
            for ind in potential_mean_std_max_targets_df.index:
                current_mean = potential_mean_std_max_targets_df["mean"][ind]
                current_std = potential_mean_std_max_targets_df["std"][ind]
                future_mean = potential_mean_std_max_targets_df["mean"][ind+1]
                future_std = potential_mean_std_max_targets_df["std"][ind+1]
                #first pass -if first and second mean and std are equal, put range value into duplicate_range
                if past_mean == None and past_std == None and\
                    potential_mean_std_max_targets_df.iloc[0,no_of_columns-2] == potential_mean_std_max_targets_df.iloc[1,no_of_columns-2] and\
                    potential_mean_std_max_targets_df.iloc[0,no_of_columns-1] == potential_mean_std_max_targets_df.iloc[1,no_of_columns-1]:   
                    # print('first pass a')
                    past_mean = current_mean
                    past_std = current_std
                    duplicate_range.append(potential_mean_std_max_targets_df["Range"][ind])
                    continue
                
                #first pass -first and second mean and std not equal
                elif past_mean == None and past_std == None:
                    # print('first pass b')
                    past_mean = current_mean
                    past_std = current_std
                    temp_mean_std_max_background.append(potential_mean_std_max_targets_df["Range"][ind])
                    range_value = potential_mean_std_max_targets_df['Range'][ind]
                    potential_mean_std_max_targets_df = potential_mean_std_max_targets_df[~potential_mean_std_max_targets_df['Range'].isin([range_value])]
                    # target_range_hamming_df = target_range_hamming_df[~target_range_hamming_df["Range"].isin(delete_range)]
                    remianing_digit_counter = remianing_digit_counter - 1
                    continue
                
                #identical past and current mean and std
                if current_mean == past_mean and current_std == past_std:
                    # print(f'dup mean = {current_mean}, std = {current_std}')
                    duplicate_range.append(potential_mean_std_max_targets_df["Range"][ind])
                    continue
                
                #past present future not equal, and no duplicate range
                elif not duplicate_range and (current_mean != future_mean or current_std != future_std): 
                    past_mean = current_mean
                    past_std = current_std
                    # print(f'not dup mean = {current_mean}, std = {current_std}')
                    temp_mean_std_max_background.append(potential_mean_std_max_targets_df["Range"][ind])
                    range_value = potential_mean_std_max_targets_df['Range'][ind]
                    potential_mean_std_max_targets_df = potential_mean_std_max_targets_df[~potential_mean_std_max_targets_df['Range'].isin([range_value])]
                    remianing_digit_counter = remianing_digit_counter - 1
                    continue
                
                #past present not equal, present and future equal, and no duplicate range
                elif not duplicate_range and current_mean == future_mean and current_std == future_std:     
                    # print('present and future equal, no current dup')
                    past_mean = current_mean
                    past_std = current_std
                    duplicate_range.append(potential_mean_std_max_targets_df["Range"][ind])
                    continue
                
                else: #past present not equal, duplicate range present
                    past_mean = current_mean
                    past_std = current_std
                    
                    #deal with duplicate set 
                    if len(duplicate_range) < remianing_digit_counter:
                        # print(f'dup_range length({len(duplicate_range)}) < remaining({remianing_digit_counter})')
                        temp_mean_std_max_background.extend(duplicate_range)
                        potential_mean_std_max_targets_df = potential_mean_std_max_targets_df[~potential_mean_std_max_targets_df['Range'].isin(duplicate_range)]
                        remianing_digit_counter = remianing_digit_counter - len(duplicate_range)
                        duplicate_range = []
                     
                        
                    if len(duplicate_range) >= remianing_digit_counter:
                        # print(f'dup_range length({len(duplicate_range)}) >= remaining({remianing_digit_counter})')
                        chosen_values = np.random.choice(duplicate_range,remianing_digit_counter,replace = False)
                        temp_mean_std_max_background.extend(chosen_values)
                        potential_mean_std_max_targets_df = potential_mean_std_max_targets_df[~potential_mean_std_max_targets_df['Range'].isin(chosen_values)]
                        remianing_digit_counter = 0 
                        duplicate_range = []
                        break
                    
                    
                    #deal with current value
                    
                    #if it has a dup
                    if current_mean == future_mean and current_std == future_std:
                        duplicate_range.append(potential_mean_std_max_targets_df["Range"][ind])
                    #if it is unique
                    else:
                        temp_mean_std_max_background.append(potential_mean_std_max_targets_df["Range"][ind])
                        range_value = potential_mean_std_max_targets_df['Range'][ind]
                        potential_mean_std_max_targets_df = potential_mean_std_max_targets_df[~potential_mean_std_max_targets_df['Range'].isin([range_value])]
                        remianing_digit_counter = remianing_digit_counter - 1
                    
                    
                if remianing_digit_counter == 0:
                    break
                elif remianing_digit_counter < 0:
                    print('remianing_digit_counter is less than zero!\nThis should never happen.')
                    raise ValueError
                    # temp_mean_std_max_background = np.random.choice(temp_mean_std_max_background,background_target_size,replace = False)
                    # duplicate_range = []
                    # break
                elif remianing_digit_counter > 0:
                    continue
            
            if remianing_digit_counter > 0 and len(duplicate_range) < remianing_digit_counter:
                print(f'remianing_digit_counter({remianing_digit_counter}) is greater than zero!')
                print(f'not enough digits were present to finish target {target_number5}')
                raise KeyError
            elif  remianing_digit_counter > 0 and len(duplicate_range) >= remianing_digit_counter:
                # print('final_catch')
                temp_mean_std_max_background.extend(np.random.choice(remianing_digit_counter,duplicate_range,replace = False))
 
            temp_mean_std_max_background_ar = np.array(temp_mean_std_max_background)
            collected_targets5.update({str(target_number5):temp_mean_std_max_background_ar})
            target_number5 += 1
            
            available_digits = len(potential_mean_std_max_targets_df)
            if background_target_size > available_digits:
                print(f'not enough available digits({available_digits})\
                      for the target size({background_target_size}!)')
                print(f'only {target_no2} of {number_of_nonsequential_targets} targets generated')
                raise ValueError
            
        return collected_targets5
        #final product: collected_targets5 (dictionary str:np.array)
        #random consecutive targets process FINISHED===================================
        
        
@Background_Generator.register_subclass('random_continuous_post_screening')
class Post_Screening_Continuous_Target_Background(Background_Generator):

    def __init__(self):
       pass
   
    def __new__(self,*args, **kargs):
        background_targets = Post_Screening_Continuous_Target_Background.generate(*args, **kargs)
        return background_targets
    
    def generate( *args, **kargs):
        
        Background_Generator.settings_check("continuous")
        pre_screened_hammings_df = Background_Generator.fast_hamming_matrix_generation()        
        # pre_screened_hammings_df = Background_Generator.hamming_matrix_generation()
        screened_hammings_df = Background_Generator.low_hamming_screening(pre_screened_hammings_df)
        possible_target_list_ar = Background_Generator.potential_continuous_target_finder(screened_hammings_df)
        
        #random consecutive targets process ===========================================

        #covert to process specific variable
        target_number3 = Background_Generator.starting_background_target_number
        number_of_continuous_targets = Background_Generator.number_of_continuous_targets
        target_length = Background_Generator.continuous_background_target_length
        
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
            collected_targets3.update({str(target_number3):temp_target_range})
            target_number3 += 1
            
        # print(f'collected_targets3 = {collected_targets3}')    
        
        return collected_targets3
        #final product: collected_targets3 (dictionary str:np.array)
        #random consecutive targets process FINISHED===================================
        
@Background_Generator.register_subclass('max_mean_continuous_post_screening')
class Post_Screening_Max_Mean_Continuous_Target_Background(Background_Generator):

    def __init__(self):
       pass
   
    def __new__(self,*args, **kargs):
        background_targets = Post_Screening_Max_Mean_Continuous_Target_Background.generate(*args, **kargs)
        return background_targets
    
    def generate( *args, **kargs):
        
        Background_Generator.settings_check("continuous")
        pre_screened_hammings_df = Background_Generator.fast_hamming_matrix_generation()        
        # pre_screened_hammings_df = Background_Generator.hamming_matrix_generation() 
        screened_hammings_df = Background_Generator.low_hamming_screening(pre_screened_hammings_df)
        possible_target_list_ar = Background_Generator.potential_continuous_target_finder(screened_hammings_df)
                
        #max consecutive targets process (mean only)==============================================

        #renaming
        target_number4 = Background_Generator.starting_background_target_number
        all_background_df = screened_hammings_df
        target_length = Background_Generator.continuous_background_target_length
        number_of_continuous_targets = Background_Generator.number_of_continuous_targets
        # print(f'possible_target_list_ar len = {possible_target_list_ar.size}')

        target_range_hamming_dic = {}

        #get the average hamming for each possible target
        for p_target in possible_target_list_ar:
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
                # print_dup_value = target_range_hamming_df['duplicates'][ind]
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
            chosen_targets_max.update({str(target_number4):temp_range2})
            target_number4 += 1
            
        # print(f'targets chosen (max type) = {chosen_targets_max}')    
        return chosen_targets_max
    
        #final product:   chosen_targets_max (dictionary str:np.array)
        #max consecutive targets process (mean only) FINISHED==================

###############################################################################
#in development 12.27.2022
@Background_Generator.register_subclass('max_mean_std_continuous_post_screening')
class Post_Screening_Max_Mean_Std_Continuous_Target_Background(Background_Generator):

    def __init__(self):
       pass
   
    def __new__(self,*args, **kargs):
        background_targets = Post_Screening_Max_Mean_Std_Continuous_Target_Background.generate(*args, **kargs)
        return background_targets
    
    def generate( *args, **kargs):
        
        Background_Generator.settings_check("continuous")
        pre_screened_hammings_df = Background_Generator.fast_hamming_matrix_generation()        
        # pre_screened_hammings_df = Background_Generator.hamming_matrix_generation() 
        screened_hammings_df = Background_Generator.low_hamming_screening(pre_screened_hammings_df)
        possible_target_list_ar = Background_Generator.potential_continuous_target_finder(screened_hammings_df)
                
        #max consecutive targets process (mean only)==============================================

        #renaming
        target_number6 = Background_Generator.starting_background_target_number
        all_background_df = screened_hammings_df
        target_length = Background_Generator.continuous_background_target_length
        number_of_continuous_targets = Background_Generator.number_of_continuous_targets
        # print(f'possible_target_list_ar len = {possible_target_list_ar.size}')

        target_range_hamming_dic = {}

        #get the average hamming for each possible target
        for p_target in possible_target_list_ar:
            #create the range for this individual target, based on target_length 
            p_target_range = np.arange(p_target,p_target+target_length+1).tolist()
            # print(f'range = {p_target_range}')
            
            #get the mean of the average digit hamming distance for the entire target 
            temp_target_hamming_mean = all_background_df.loc\
                [all_background_df["Range"].isin(p_target_range),"mean"].mean()
            
            #get the mean of the standard deviation digit hamming distance for the entire target 
            temp_target_hamming_std = all_background_df.loc\
                [all_background_df["Range"].isin(p_target_range),"std"].mean()
            
            #store the mean in the dictionary
            target_range_hamming_dic.update({p_target:temp_target_hamming_mean})
            
        #print for checking dictionary length
        # print(f'len = {len(target_range_hamming_dic.keys())}')

        target_range_hamming_df = pd.DataFrame.from_dict\
            (target_range_hamming_dic,orient='index',columns=["avg_mean"])

        #add average std as a column
        target_range_hamming_df['avg_std'] = temp_target_hamming_std      

        #make the range its own column, instead of the index
        target_range_hamming_df.reset_index(inplace=True)
        target_range_hamming_df = target_range_hamming_df.rename(columns = {'index':'Range'})

        # MEAN&STD SORTED======================================================
        #sort by mean values (largest first), then standard deviation values (smallest first)
        target_range_hamming_df.sort_values(by = ['avg_mean', 'avg_std'], ascending = [False, True], na_position = 'first',inplace=True)
        
        #reset index and remove old index values
        target_range_hamming_df.reset_index(inplace=True)
        target_range_hamming_df = target_range_hamming_df.drop("index", axis = 1)
        
        #saving a copy in case we need to debug
        # printing_df = target_range_hamming_df
        # =============================================================================        
       
        # #note which rows have duplicate hamming distance values with 'True' in the new duplicates column
        # target_range_hamming_df['duplicates'] = target_range_hamming_df.duplicated(subset="hamming_dist", keep=False)
        # # print(f'df size = {len(target_range_hamming_df.index)}')
        # # print(f'df head20 = {target_range_hamming_df.head(20)}')

        #target collection loop
        targets_chosen = []
        # duplicate_rows = False
        past_avg_mean = None
        past_avg_std = None
        number_targets_chosen = 0
        duplicate_range = []
        # test_error_counter = 0
        # no_of_columns = len(target_range_hamming_df.columns)
        
        #reset index and remove old index values
        target_range_hamming_df.reset_index(inplace=True)
        target_range_hamming_df = target_range_hamming_df.drop("index", axis = 1)
        
        #run through every value in the datafrom from 0 upwards
        index_max = target_range_hamming_df.index.max()
        for ind in target_range_hamming_df.index:
            current_avg_mean = target_range_hamming_df["avg_mean"][ind]
            current_avg_std = target_range_hamming_df["avg_std"][ind]
                        
            #if the value was removed in a previous iteration, skip this value
            try:
                target_range_hamming_df['Range'][ind]
            except:
                # print('removed ind')
                # test_error_counter += 1
                # print(f'{ind}')
                continue
            
            try:
                future_avg_mean = target_range_hamming_df["avg_mean"][ind+1]
                future_avg_std = target_range_hamming_df["avg_std"][ind+1]
            except:
                next_index_exists = False
                if (ind+2) <= index_max:
                    future_test_range = np.arange(ind+2,index_max+1)
                    for test_index in future_test_range:
                        if test_index in target_range_hamming_df.index:
                            future_avg_mean = target_range_hamming_df["avg_mean"][test_index]
                            future_avg_std = target_range_hamming_df["avg_std"][test_index]
                            next_index_exists = True
                            break
                    if next_index_exists != True:
                        if len(duplicate_range) == 0:
                            future_avg_mean = -1
                            future_avg_std = -1
                        else:
                            future_avg_mean = current_avg_mean
                            future_avg_std = current_avg_std
                            
            #first pass -if first and second mean and std are equal, put range value into duplicate_range
            if past_avg_mean == None and past_avg_std == None and\
                current_avg_mean == future_avg_mean and\
                current_avg_std == future_avg_std:   
                # print('first pass a')
                past_avg_mean = current_avg_mean
                past_avg_std = current_avg_std
                duplicate_range.append(target_range_hamming_df["Range"][ind])
                continue
                
            #first pass -first and second mean and std not equal
            elif past_avg_mean == None and past_avg_std == None:
                # print('first pass b')
                past_avg_mean = current_avg_mean
                past_avg_std = current_avg_std
                targets_chosen.append(target_range_hamming_df["Range"][ind])
                range_value = target_range_hamming_df['Range'][ind]
                
                #remove conflicting targets from temp_target_list, and target_range_hamming_df
                delete_range = np.arange(range_value-target_length,range_value+target_length+1)
                target_range_hamming_df = target_range_hamming_df[~target_range_hamming_df['Range'].isin([delete_range])]
                # target_range_hamming_df = target_range_hamming_df[~target_range_hamming_df["Range"].isin(delete_range)]
                number_targets_chosen += 1
                continue
            # #current range digit under investigation    
            # current_hamming_value = target_range_hamming_df['hamming_dist'][ind]
            
            #past (equal) current 
            if current_avg_mean == past_avg_mean and current_avg_std == past_avg_std:
                # print(f'dup mean = {current_mean}, std = {current_std}')
                duplicate_range.append(target_range_hamming_df["Range"][ind])
                continue
            
            #past (not equal) present (not equal) future, and no duplicate range
            
            elif len(duplicate_range) == 0 and (current_avg_mean != future_avg_mean or current_avg_std != future_avg_std): 
                past_avg_mean = current_avg_mean
                past_avg_std = current_avg_std
                # print(f'not dup mean = {current_avg_mean}, std = {current_avg_std}')
                targets_chosen.append(target_range_hamming_df["Range"][ind])
                #remove conflicting targets from target_range_hamming_df
                range_value = target_range_hamming_df['Range'][ind]
                delete_range = np.arange(range_value-target_length,range_value+target_length+1)
                target_range_hamming_df = target_range_hamming_df[~target_range_hamming_df['Range'].isin([delete_range])]
                number_targets_chosen += 1
                continue
            
            #past (not equal) present (equal) future, and no duplicate range
            elif len(duplicate_range) == 0 and current_avg_mean == future_avg_mean and current_avg_std == future_avg_std:     
                # print('present and future equal, no current dup')
                past_avg_mean = current_avg_mean
                past_avg_std = current_avg_std
                duplicate_range.append(target_range_hamming_df["Range"][ind])
                continue
            
            else: #past (not equal) present (equal) future, duplicate range present
                past_avg_mean = current_avg_mean
                past_avg_std = current_avg_std
                
                #deal with duplicate set 
                while len(duplicate_range) != 0 and number_targets_chosen < number_of_continuous_targets:
                    
                    temp_choice = np.random.choice(duplicate_range,1,replace = False)
                    targets_chosen.append(temp_choice)
                    
                    #remove conflicting targets from target_range_hamming_df
                    range_value = temp_choice
                    delete_range = np.arange(range_value-target_length,range_value+target_length+1)
                    target_range_hamming_df = target_range_hamming_df[~target_range_hamming_df['Range'].isin([delete_range])]
                    duplicate_range = np.delete(duplicate_range,np.isin(duplicate_range,delete_range))
                    # temp_target_list = np.delete(temp_target_list,np.isin(temp_target_list,delete_range))
                    number_targets_chosen += 1
                             
                if number_targets_chosen == number_of_continuous_targets:
                    break
                
                #if the current 'range' digit was deleted by the previous process (while loop)
                #go to the next range digit
                try:
                    target_range_hamming_df['Range'][ind]
                except:
                    # print('removed ind while in -> case = not dup, p_target_list')
                    # remaining_digits = len(target_range_hamming_df['Range'])
                    # print(f'remaining = {remaining_digits}')
                    continue
                
                #this shouldn't be necessary, but just in case...
                duplicate_range = []
                
                duplicate_range.append(target_range_hamming_df['Range'][ind])
                continue
                
            

        #this is to catch the situation where all digits are duplicates 
        #(this happens with mirror targets), or when the last few are duplicates
        while len(duplicate_range) != 0 and number_targets_chosen < number_of_continuous_targets:
            # print('final catch')
            #complete one choice on temp_target_list
            # print(f'temp_target_list = {temp_target_list}')
            temp_choice = np.random.choice(duplicate_range,1)
            
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
            duplicate_range = np.delete(duplicate_range,np.isin(duplicate_range,delete_range))
            # print("post")
            # print(f'targets_chosen length = {len(targets_chosen)}')
            # print(target_range_hamming_df)
            # print(temp_target_list)
            # range_set = np.delete(range_set,np.isin(range_set,target_digits))
            

        if number_targets_chosen < number_of_continuous_targets:
            print(f'End catch: Error! number_targets_chosen({number_targets_chosen}) is less than number_of_continuous_targets({number_of_continuous_targets})!')
            raise ValueError
            
        chosen_targets_dict = {}
        for temp_target in targets_chosen:
            temp_range = np.arange(temp_target,temp_target+target_length+1)
            chosen_targets_dict.update({str(target_number6):temp_range})
            target_number6 += 1
    
            # print(f'temp target_type = {type(temp_target)}')
            # a = printing_df.loc[printing_df['Range']==temp_target[0],'avg_mean']
            # b = printing_df.loc[printing_df['Range']==temp_target[0],'avg_std']
            # print(f'for target {temp_target}, mean = {a}, std = {b}')
        
        return chosen_targets_dict
    
        #final product:   chosen_targets_dict (dictionary str:np.array)
        #max consecutive targets process (mean and std) FINISHED===============

###############################################################################
                
                
