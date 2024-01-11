 # -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 11:39:38 2022

@author: Cyrus
"""
from scipy.stats import entropy
import numpy
from Data_Module import Exp_Data
from Background_Generator_Module import Background_Generator
#from Organism_Module import Organism
import Organism_Module
import copy
from numba import njit
import numpy as np

def set_up_targets(target_parameters):
    background_check = False
    background_generator_check = False
    no_of_bits = Organism_Module.Organism.number_of_binary_digits
    unique_check = numpy.array([],dtype=int)
    
    experiment_targets = target_parameters['target_id'].keys()
    print(f' experiment_targets = {experiment_targets}')
    print(f' target_parameters = {target_parameters}')
    #typical target setup
    past_target = 0
    for target_id in experiment_targets:
        
        try:
            int(target_id)
        except:
            print(f'Error! target_id({target_id}) must be a string containing a number')
            raise ValueError
        if int(target_id) != past_target+1:
            print('Error! targets need to be a string containing sequential numbers starting from 1')
            raise ValueError
            
        past_target += 1
        
        target_type = target_parameters["target_id"][target_id]["target_type"]
        print(f'target_type = {target_type}')
        if target_type != "background":
            target_high = target_parameters["target_id"][target_id]["target_high"]
            target_low = target_parameters["target_id"][target_id]["target_low"]
            target_range = numpy.arange(target_low,target_high+1)
            Exp_Data.target_value_dictionary.update({target_id:target_range})
            unique_check = numpy.append(unique_check,target_range)
            print(f'target ID {target_id} = {target_range}')
        else:
            background_check = True
            Exp_Data.background_target_active = True
    
    #background target generator - collect primary targets        
    if background_check == True:
        primary_targets = copy.deepcopy(Exp_Data.target_value_dictionary)
        
    #background target setup
    if background_check == True:
        background_counter = 1
        for target_id2 in experiment_targets:   
            target_type = target_parameters["target_id"][target_id2]["target_type"]
            if target_type == "background":    
                
                bkgd_style = target_parameters["target_id"][target_id2]["background_style"]
                
                if bkgd_style == "high_low":
                    if background_generator_check == True:
                        print('Error! Background_generator targets must be run last!')
                        raise ValueError
                        
                    target_high = target_parameters["target_id"][target_id2]["target_high"]
                    target_low = target_parameters["target_id"][target_id2]["target_low"]
                    background_range = numpy.arange(target_low,target_high+1)
                    Exp_Data.target_value_dictionary.update({target_id2:background_range})
                    unique_check = numpy.append(unique_check,background_range)
                    print(f'Target ID = {target_id2} = {background_range}')
                    background_counter =+ 1
                    print(f'background number {background_counter} ')
                    
                    
                if bkgd_style == "random":
                    if background_generator_check == True:
                        print('Error! Background_generator targets must be run last!')
                        raise ValueError
                        
                    no_of_phenotypes = target_parameters["target_id"][target_id2]["no_of_phenotypes"]
                    
                    base_range = numpy.arange(2**no_of_bits)
                    
                    other_targets = Exp_Data.target_value_dictionary.keys()
                    for target_keys in other_targets:
                    
                        temp_range = Exp_Data.target_value_dictionary[target_keys]
                        
                        base_range = numpy.delete(base_range,numpy.isin(base_range,temp_range))
                    
                    print(f'base range size = {base_range.size}')
                    try:
                        background_range = numpy.random.choice(base_range,no_of_phenotypes,replace=False)
                    except:
                        print(f'Not enough values remain for {background_counter} background {target_id2}!')
                        print(f'Only {base_range.size} digits remain and {no_of_phenotypes} digits are needed')
                        raise
                    background_counter =+ 1       
                    print(f'Target ID {target_id2} = {background_range}')
                    print(f'background range number {background_counter}')

                    Exp_Data.target_value_dictionary.update({target_id2:background_range})
                    unique_check = numpy.append(unique_check,background_range)
                
                if bkgd_style == "background_generator":
                    background_generator_check = True
                    #background target generator - collect passive_removal targets
                    all_previous_targets = Exp_Data.target_value_dictionary
                    #primary_targets
                    primary_targets_keys = primary_targets.keys()
                    passive_removal = {}
                    for p_target_key in all_previous_targets.keys():
                        if p_target_key in primary_targets_keys:
                            continue    
                        else:
                            passive_removal.update({p_target_key:all_previous_targets[p_target_key]})
                    
                    print(f'no_of_bits({no_of_bits})')
                    print(f'target_id2({target_id2})')
                    print(f'primary_targets = \n{primary_targets}')
                    print(f'passive_removal = \n{passive_removal}')
                    #background target generator - set up 
                    background_generator_settings = target_parameters["target_id"][target_id2]["background_generator_settings"]
                    background_type = target_parameters["target_id"][target_id2]["background_generator_settings"]["generator_type"]
                    Background_Generator.setup(no_of_bits,target_id2,primary_targets,background_generator_settings,passive_removal)
                    
                    #background target generator - generate targets
                    generated_background_targets = Background_Generator.generate(background_type)
                    print('\n')
                    print(f'generated targets = \n{generated_background_targets}')
                    Exp_Data.target_value_dictionary.update(generated_background_targets)
                    
                    #check for uniqueness
                    for target5 in generated_background_targets.keys():
                        gen_range = generated_background_targets[target5]
                        unique_check = numpy.append(unique_check,gen_range)
    
    unique_check_check = numpy.unique(unique_check)
    if unique_check.size != unique_check_check.size:
        raise ValueError('target classes are overlapping!')
            
#Exp_Data.target_value_dictionary.update({target_id:target_range})        
        
def check_targets(emitted_bx,Schedule_target_ids):
    for target_id in Schedule_target_ids:
        target_range = Exp_Data.target_value_dictionary[target_id]
        if numpy.isin(emitted_bx,target_range):
            # print (f'hit target {target_id}!')
            return target_id
    
    return None

    #bx_in = numpy.isin(bx,background_range)
# ==old way====================================================================
#   def check_targets(emitted_bx,target_max_min_info,Schedule_target_ids):
#     id_list = []
#     max_list = []
#     min_list = []
#     
#     # load target max min id info
#     
#     for target_id in Schedule_target_ids:
#         id_list.append(target_id)
#         max_list.append(target_max_min_info["target_id"][target_id]["target_high"])
#         min_list.append(target_max_min_info["target_id"][target_id]["target_low"])
#     # print(id_list)
#     # print(max_list)
#     # print(min_list)
#     
#     for target_index in range(len(id_list)):
#         # print("max_list[target_index] = ",max_list[target_index])
#         # print("min_list[target_index] = ", min_list[target_index])
#         # print("emitted_bx = ", emitted_bx)
#         
#         if max_list[target_index] >= emitted_bx and min_list[target_index] <= emitted_bx:
#             # print("Bx = {} hit target {}! Max = {} min = {}" \
#                    # .format(emitted_bx,id_list[target_index],max_list[target_index],min_list[target_index]))
#             return id_list[target_index]
#         else:
#             continue
#         
#     # print("Bx = {} did NOT hit any targets".format(emitted_bx))
#     return None
# =============================================================================

# =============================================================================
# def convert_to_binary(decimal_bx):
#     binary_bx = bin(decimal_bx)[2:len(bin(decimal_bx))]
#     return binary_bx
# =============================================================================


###############################################################################
# version 1
# #this version uses strings
# def convert_to_binary(decimal_bx,num_of_bits):
#     format_string="{:0>"+str(num_of_bits)+"b}"
#     binary_bx = format_string.format(decimal_bx)
#     return binary_bx


# def convert_to_decimal(binary_bx):
#     decimal_bx = int(binary_bx,2)
#     return decimal_bx

# def pad_binary(binary_num, binary_digits):
  
#     while True:
        
#         if len(binary_num) == binary_digits:
#             return binary_num
#         elif len(binary_num) > binary_digits:
#             raise ValueError ("binary string too long error")
#         else:
#             binary_num = "0" + binary_num
            
#     return binary_num  
###############################################################################

###############################################################################
#version 2
#This version uses lists
def int_to_bool_list(decimal_bx,binary_digits):
        return [bool(decimal_bx & (1<<n)) for n in range(binary_digits)]

def bool_list_to_int(bool_list):
        return int(''.join(map(str, map(int, bool_list))), 2)
###############################################################################

###############################################################################
#Ryan's version 
#this version uses numpy arrays
@njit
def dec_to_bin(num, bits):
    binary = np.zeros(bits, dtype=np.int8)
    i = bits - 1
    while num > 0 and i >= 0:
        binary[i] = num % 2
        num //= 2
        i -= 1

    return binary


@njit
def bin_to_dec(binary):
    num = 0
    for i in range(len(binary)):
        num += binary[i] * 2 ** (len(binary) - i - 1)

    return num
###############################################################################

@njit 
def normalize_histogram(bx_pop,decimal_max):
    bx_pop_histogram = numpy.histogram(bx_pop, bins=25, range=(0,decimal_max))   
    
    histo_sum = numpy.sum(bx_pop_histogram[0])
    normalized_histogram = bx_pop_histogram[0]/histo_sum
    
    return normalized_histogram

def get_entropy(bx_pop,decimal_max):
    
    #the number of bins is based on the target size, which is currently 40. 
    #each bin has 40-41 digits each. 
    # bx_pop_histogram = numpy.histogram(bx_pop, bins=25, range=(0,decimal_max),\
    #                    normed=None, weights=None, density=None)   
    
    # histo_sum = numpy.sum(bx_pop_histogram[0])
    # normalized_histogram = bx_pop_histogram[0]/histo_sum
    normalized_histogram = normalize_histogram(bx_pop,decimal_max)
    bx_pop_entropy = entropy(normalized_histogram, base=2)
    
    return bx_pop_entropy

def generate_schedule_order(schedule_settings,schedule_randomization_cutoff = False):
    final_list = []
    
    cut_off = schedule_randomization_cutoff

    key_list = schedule_settings["schedule_list"]["schedule_set_no"].keys()

    # check to make sure it is all intergers, or intergers as strings
    try:
        key_list2 = list(map(int, key_list))
    except:
        print('the dictionary has a non-integer string!')
        raise
        
    key_list2_ar = numpy.array(key_list2)
    
# =============================================================================
#     #check uniqueness This shouldn't be necessary since dictionary keys must be unique
#     
#     key_list2_ar_unique = numpy.unique(key_list2_ar)
#     if len(key_list2_ar) != len(key_list2_ar_unique):
#         print('Dictionary values are not unique!')
#         raise
# =============================================================================

    key_list3_ar = numpy.sort(key_list2_ar)
    if cut_off == False:
        key_cut_off_mask = numpy.zeros(len(key_list2_ar), dtype=bool)
    else:
        key_cut_off_mask = numpy.greater_equal(key_list3_ar,cut_off)
    key_ordered_mask = numpy.invert(key_cut_off_mask)
    ordered_items = key_list3_ar[key_ordered_mask]
    shuffled_items = key_list3_ar[key_cut_off_mask]
    numpy.random.shuffle(shuffled_items)

    final_list.extend(list(ordered_items))
    final_list.extend(list(shuffled_items))
    final_list2 = list(map(str,final_list))
    
    return final_list2