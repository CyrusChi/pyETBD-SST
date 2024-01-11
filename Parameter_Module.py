# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 13:00:11 2022

@author: Cyrus
Parameter Loader
"""
import json
import sys
from pathlib import Path
from os import sep

def load_settings(file_list = None, print_status = True):
    data = {}
    try:    
        if file_list is None:
            raise Exception
    except Exception:
        print('no files listed!')
        sys.exit()
    #print(file_list)
    for input_file in file_list:
        temp_data=None;
        with open(Path(input_file),'r') as exp_file:
            if print_status:
                print("reading from " + input_file)
            try:
                temp_data = json.load(exp_file)
            except FileNotFoundError:
                print("setting file not found!")
                sys.exit()
            except:
                print("there was an error in loading settings!")
                sys.exit()
                
        # print("input_file"+input_file)
        
        start_index = input_file.rfind(sep) + 1
        # if input_file.rfind("\\") == -1:
        #     start_index = input_file.rfind("/") + 1
        # else:
        #     start_index = input_file.rfind("\\") + 1
        
        end_index = input_file.rfind(".")
        key_name = input_file[start_index:end_index]
        # print("key_name "+key_name)
        data.update({key_name:temp_data})
        
    return data

class parameter_holder:
    
    all_parameters = {}
    
    def __init__(self, data_dict = None):
        if data_dict is None:
            print("parameter dictionary missing.")
            self.parameter_holder = []
            return
        self.all_parameters = data_dict
        parameter_holder.all_parameters = data_dict
        return 
    
    def __print__(self):
        return 'Dictionary has {} elements.'.format(len(self.all_parameters))
    def __repr__(self):
        return f'List of all parameters \n{parameter_holder.all_parameters}'   

    def get_dict_keys(self):
        return self.all_parameters.keys()
    def get_repititions(self):
        return self.all_parameters["experiment_general_settings"]["repetitions"]  
    def get_total_schedule_num(self):
        return len(self.all_parameters["experiment_schedule_settings"]["schedule_list"]["schedule_set_no"])
    def get_default_generation_num(self):
        return self.all_parameters["experiment_general_settings"]["default_generations_per_schedule"]
    
    def get_experiment_generation_num(self):
        total_experiment_generations = 0
        default_gen_per_schedule = self.all_parameters["experiment_general_settings"]["default_generations_per_schedule"]
        sched_keys = self.all_parameters["experiment_schedule_settings"] \
            ["schedule_list"]["schedule_set_no"].keys()
        for specific_sched in sched_keys:
            specific_gen_count = self.all_parameters["experiment_schedule_settings"] \
                ["schedule_list"]["schedule_set_no"][specific_sched].get("nondefault_schedule_generation_count")
            if specific_gen_count != None:
                total_experiment_generations = total_experiment_generations + specific_gen_count
            else:
                total_experiment_generations = total_experiment_generations + default_gen_per_schedule
        return total_experiment_generations
    
    def check_schedule_order_randomization(self):
        check = self.all_parameters["experiment_general_settings"].get("random_shuffle_schedule_x_and_after")
        if check == None:
            return False
        else:
            return True
    def get_schedule_order_randomization_cutoff(self):
        return self.all_parameters["experiment_general_settings"]["random_shuffle_schedule_x_and_after"]
    def get_stimulus_environment_settings(self):
        return self.all_parameters["stimulus_environment_settings"]
    def get_experiment_schedule_settings(self):
        return self.all_parameters["experiment_schedule_settings"]
    def get_procedure_settings(self):
        return self.all_parameters["procedure_settings"]
    def get_organism_settings(self):
        return self.all_parameters["organism_settings"]
    def get_population_reset_between_schedules(self):
        return self.all_parameters["experiment_general_settings"]["population_reset_between_schedules"]
    def get_target_info(self):
        return self.all_parameters["experiment_schedule_settings"]["target_list"]
    def get_schedule_active_targets(self,schedule_set_no):
        return list(self.all_parameters["experiment_schedule_settings"]["schedule_list"] \
               ["schedule_set_no"][schedule_set_no]["active_target_id_no"].keys())
    #nondefault_schedule_generation_count
    def get_schedule_gen_count(self,schedule_set_no):
        check = self.all_parameters["experiment_schedule_settings"]["schedule_list"] \
               ["schedule_set_no"][schedule_set_no].get("nondefault_schedule_generation_count")
        if check == None:
            return False
        else:
            return check
            
    def get_reinforcement_type(self,schedule_set_no,target_no):
        return self.all_parameters["experiment_schedule_settings"]["schedule_list"] \
               ["schedule_set_no"][schedule_set_no]["active_target_id_no"][target_no]["reinforcer"]

    def get_background_target_ids(self):
        background_target_list = []
        all_target_ids = self.all_parameters["experiment_schedule_settings"]["target_list"] \
                                            ["target_id"].keys()
        for target in all_target_ids:
            test_target_type = self.all_parameters["experiment_schedule_settings"]["target_list"] \
                               ["target_id"][target]["target_type"]
            if test_target_type == "background":
                background_target_list.append(target)           
        return background_target_list
    
    def get_primary_target_ids(self):
        primary_target_list = []
        all_target_ids = self.all_parameters["experiment_schedule_settings"]["target_list"] \
                                            ["target_id"].keys()
        for target in all_target_ids:
            test_target_type = self.all_parameters["experiment_schedule_settings"]["target_list"] \
                               ["target_id"][target]["target_type"]
            if test_target_type == "primary":
                primary_target_list.append(target)           
        return primary_target_list
    def get_filename_modifier(self):
        return self.all_parameters["experiment_general_settings"]["filename_modifier"]
    def get_output_type(self):
        return self.all_parameters["experiment_general_settings"]["data_output_type"]
    def get_target_varied_ids(self,fdf_mod_active,primary_target_list):
        if fdf_mod_active == True:
            for target in primary_target_list:
                test_target_type = self.all_parameters["experiment_schedule_settings"]["target_list"] \
                                   ["target_id"][target]["reward_continvency_type"]
                if test_target_type == "target":
                    target_target_id = target
                elif test_target_type == "varied":
                    varied_target_id = target    
                else:
                    raise KeyError("a primary target was not labeled varied/target")
            return [target_target_id,varied_target_id]
        else:
            return [None,None]
    def get_reinforcement_context_active(self):
        return self.all_parameters["experiment_general_settings"]\
                                  ["reinforcement_context_magnitude_modifer_active"]
                            
    def get_user_modifier(self):
        return self.all_parameters["experiment_general_settings"]\
                                  ["reinforcement_context_user_modifier"]
    
    def get_reinforcement_capture_length(self):
        return self.all_parameters["experiment_general_settings"]\
                                  ["reinforcement_capture_length"]
                                  
    def get_output_entropy(self):
        return self.all_parameters["experiment_general_settings"]\
                                  ["output_entropy"]
    
    def get_output_emitted_behavior_population(self):
        return self.all_parameters["experiment_general_settings"]\
                                  ["output_emitted_behavior_population"]                              
    
    def get_output_selection_modifier(self):                       
        return self.all_parameters["experiment_general_settings"]\
                                  ["output_selection_modifier"]        
        
    def get_output_background(self):
        return self.all_parameters["experiment_general_settings"]\
                                  ["output_background"]
                                  
    def get_output_entropy_length(self):
        return self.all_parameters["experiment_general_settings"]\
                                  ["output_entropy_moving_avg_length"]  
    def get_entropy_percentage():
        return parameter_holder.all_parameters["procedure_settings"]\
                                  ["observation_entropy_percentage"]  
    
    def get_se_shift_rules_dict(self):
        #for now, this is specific for reinforcement set up shift dictionary
        return self.all_parameters["stimulus_environment_settings"]\
                                  ["se_shift_rules"]["reinforcement_setup"]
            