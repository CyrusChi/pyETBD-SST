# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 10:36:21 2022

@author: Cyrus
"""

import Data_Module
from RI_Module import Ri_Schedule
from RR_Module import Rr_Schedule
from FI_Module import Fi_Schedule
from FR_Module import Fr_Schedule

class Stimulus_Element_Holder:
    se_registry = {}
    #every SE should have a number
    se_num_dic = {}
        
    def __int__(self):
        pass
    
    @classmethod
    def clear_registry(cls):
        cls.se_registry = {}
        cls.se_num_dic = {} 
        
    @classmethod
    def load_stimulus_environment(cls,se_settings):
        se_count = 0
        se_dict = {}
        for gobal_locations in se_settings["global_environment"]["Location_id"].values():
            se_dict.update({gobal_locations:[]})
        
            for types in se_settings["stimulus_elements"].keys():
                for quantity in range(1,se_settings["stimulus_elements"][types]["se_quantity"]+1):
                    if gobal_locations == se_settings["stimulus_elements"][types]["se_start_location"]: 
                        # se_id = print(str(quantity)+"_"+se_settings["stimulus_elements"][types]["se_stimulus"])
                        se_id = se_settings["stimulus_elements"][types]["se_stimulus"] + "_" + str(quantity)
                        se_dict[gobal_locations] += [se_id]
                        cls.se_num_dic.update({se_id:se_count})
                        se_count += 1
                    else:
                        break
        cls.se_registry = se_dict

    @classmethod
    def get_se_registry(cls):
        return cls.se_registry 
    
    @classmethod
    def set_se_registry(cls, key, value):
        cls.se_registry[key] = value

    @classmethod
    def check_if_se_in_location(cls, location, se_id = None):
        if se_id == None:
            print('se_id is empty and cannot be checked')
            raise
        if se_id in cls.se_registry[location]:
            return True
        else:
            return False
    
    @classmethod
    def check_se_existance(cls, se_id = None):
        if se_id == None:
            print('se_id is empty and cannot be checked')
            raise
        for se_keys in cls.se_registry.keys():
            if se_id in cls.se_registry[se_keys]:
                return True
        
        return False
    
    @classmethod
    def shift_se(cls, se_id, from_location, to_location):
        if not se_id in cls.se_registry[from_location]:
            print("shift se error")
            print(f'the se_id {se_id} is not present in the from location {from_location}!')
            raise
            
        if se_id in cls.se_registry[to_location]:
            print("shift se error")
            print(f'the se_id {se_id} is present in the to location {to_location}!')
            raise
        cls.se_registry[from_location].remove(se_id)
        cls.se_registry[to_location].append(se_id)
            
    @classmethod
    def reinforcement_setup_based_se_switch(cls):
        #check if reinforcement is set up (passive) for target ID - 1(T/F)
        #check if SE pair is in "near" - 2(T/F)
        #case 1T, 2F -> move SE from far to near
        #case 1F, 2T -> move SE from near to far
        #case 1T, 2T -> do nothing
        #casr 1F, 2F -> do nothing 
        
        target_dict = Data_Module.Exp_Data.se_shift_reinforcement_setup_pairs
        if not target_dict == {}:
            for target in target_dict.keys():    
               
                if Ri_Schedule.is_reinforcement_set_up(target,True) \
                or Fi_Schedule.is_reinforcement_set_up(target,True) \
                or Rr_Schedule.is_reinforcement_set_up(target,True) \
                or Fr_Schedule.is_reinforcement_set_up(target,True):
                    set_up_state = True
                    # print(f'SE - target {target} reinforcer set up state is TRUE')
                else:
                    set_up_state = False
                    # print(f'SE - target {target} reinforcer set up state is FALSE')
                    
                linked_se_id = target_dict[target]
                if Stimulus_Element_Holder.check_if_se_in_location("near",linked_se_id):
                    SE_in_near = True
                    # print(f'SE - {linked_se_id} in near is TRUE')
                else: 
                    SE_in_near = False
                    # print(f'SE - {linked_se_id} in near is FALSE')
                    
                if set_up_state \
                and not SE_in_near:
                    # print('T - F condition')
                    # print("BEFORE: far to near")
                    # print(f'far = {Stimulus_Element_Holder.se_registry["far"]}')
                    # print(f'near = {Stimulus_Element_Holder.se_registry["near"]}')
                    
                    Stimulus_Element_Holder.shift_se(linked_se_id,"far","near")
                    
                    # print("After: far to near")
                    # print(f'far = {Stimulus_Element_Holder.se_registry["far"]}')
                    # print(f'near = {Stimulus_Element_Holder.se_registry["near"]}')
                    
                if not set_up_state \
                and SE_in_near:
                    
                    # print('F - T condition')
                    # print("BEFORE: near to far")
                    # print(f'far = {Stimulus_Element_Holder.se_registry["far"]}')
                    # print(f'near = {Stimulus_Element_Holder.se_registry["near"]}')
                    
                    Stimulus_Element_Holder.shift_se(linked_se_id,"near","far")
                    
                    # print("After: near to far")
                    # print(f'far = {Stimulus_Element_Holder.se_registry["far"]}')
                    # print(f'near = {Stimulus_Element_Holder.se_registry["near"]}')
                
                # if set_up_state \
                # and SE_in_near: 
                #     print('both true, do nothing')
                
                # if not set_up_state \
                # and not SE_in_near: 
                #     print('both false, do nothing')
                
        else:
            # print("target dict is empty!")
            pass
        
        

    
    @classmethod
    def update_se_by_schedule(cls, schedule_based_near_list = None):
        
        near_registry_items = Stimulus_Element_Holder.get_se_registry()["near"]
        far_registry_items = Stimulus_Element_Holder.get_se_registry()["far"]
        
        near_check= []
        far_check = []
        # print("")
        #checking if the current items in "near" list are the same as the scheduled "near" items
        for wanted_se_index in range(len(schedule_based_near_list)):
            # print("")
            # print("list item = ",schedule_based_near_list[wanted_se_index])
            for current_se_index in range(len(near_registry_items)):
                [current_se_id, dummy] =  near_registry_items[current_se_index].split("_")
                if  wanted_se_index == 0:
                    if current_se_id == schedule_based_near_list[wanted_se_index]:
                        near_check.append(True) # True = it should be in near
                    else:
                        near_check.append(False)
                else:
                    # print("current_se_index = ", current_se_index)
                    # print("current_se_id = ",current_se_id)
                    # print("schedule_based_near_list[wanted_se_index] = ", schedule_based_near_list[wanted_se_index])
                    # print("near_check[current_se_index] = ",near_check[current_se_index])
                    if current_se_id == schedule_based_near_list[wanted_se_index] \
                    and near_check[current_se_index] == False:
                        near_check[current_se_index] = True
                        # print("found to be true")
                    # else:
                        # print("found to be false")
            # print("near check values = ",near_check)            
        #checking if the current items in "far" list are the same as the scheduled "near" items
        for wanted_se_index in range(len(schedule_based_near_list)):
            # print("")
            # print("list item = ",schedule_based_near_list[wanted_se_index])
            for current_se_index in range(len(far_registry_items)):
                [current_se_id, dummy] =  far_registry_items[current_se_index].split("_")
                if  wanted_se_index == 0:
                    if current_se_id == schedule_based_near_list[wanted_se_index]:
                        far_check.append(True) # True = it should be in near
                    else:
                        far_check.append(False)
                else:
                    # print("current_se_index = ", current_se_index)
                    # print("current_se_id = ",current_se_id)
                    # print("schedule_based_near_list[wanted_se_index] = ", schedule_based_near_list[wanted_se_index])
                    # print("near_check[current_se_index] = ",near_check[current_se_index])
                    if current_se_id == schedule_based_near_list[wanted_se_index] \
                    and far_check[current_se_index] == False:
                        far_check[current_se_index] = True
                        # print("found to be true")
                    else:
                        # print("found to be false") 
                        continue
            # print("far check values = ",far_check)        
            #check for near things to be kicked out
            #check for outer things to be brought in
        
        #create a new set of "near" and "far" lists based on the user schedule settings for this schedule 
        new_near = []
        for index_near in range(len(near_check)):
            if near_check[index_near] == True:
                new_near.append(near_registry_items[index_near])
        for index_far in range(len(far_check)):
            if far_check[index_far] == True:
                new_near.append(far_registry_items[index_far])
        
        new_far = []
        for index_near in range(len(near_check)):
            if near_check[index_near] == False:
                new_far.append(near_registry_items[index_near])
        for index_far in range(len(far_check)):
            if far_check[index_far] == False:
                new_far.append(far_registry_items[index_far])
        
        # print("old near list = ",near_registry_items)
        # print("old far list = ",far_registry_items)
        # print("new near list = ",new_near)
        # print("new far list = ",new_far)
        # print("")
        
        #Setting the generated lists into the record.
        Stimulus_Element_Holder.set_se_registry("near",new_near) 
        Stimulus_Element_Holder.set_se_registry("far",new_far)
        
        
    
    
    
    
    
    
    
    
    