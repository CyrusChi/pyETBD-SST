# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 10:46:58 2022

@author: Cyrus
"""
from SE_Module import Stimulus_Element_Holder

class Exp_Data:
    #this class holds the data for the current gen/schedule/rep/etc
    
    #testing data
    time_check = False
    
    #parameter data
    procedure_settings = {}
    
    #experiment data
    primary_targets = []
    background_targets = []
    default_gen_num = None
    filename_modifier = None
    total_schedule_num = None
    target_value_dictionary = {}
    background_target_active = False
    first_schedule_check = None
    experiment_gen_num = None
     
    #modifer items
    reward_context_switch = None
    target_target_id = None
    varied_target_id = None
    user_modifier = None
    capture_length = None
    se_view_count_dic = {}
    
    selection_modifier_dict = {}
    rc_stream_past_dict = {}
    rc_stream_current_dict = {}
    rc_stream_length_dict = {}
    rc_stream_step_dict = {}
    rc_stream_length_goal_dict = {}
    rc_current_diff = {}
    
    entropy_power_conversion_a = None
    entropy_power_conversion_b = None
    selection_se_entropy_mod_lower_limit = None
    
    #these settings are NOT controlled by the JSON files!! (yet)
    #time reference in generations
    #lower limits are a number between 0 and 100 and represent a percentage of
    #the number of the population to become parents or mutants respectively
    #the percentage will never be lower than the lower limit
    se_time_reference = 20000
    selection_se_time_mod_lower_limit = 5
    mutation_se_entropy_mod_lower_limit = 10
    
    #experiment loop current data
    repitition_number = None
    schedule_set_no = None
    current_gen = None
    se_shift_reinforcement_setup_pairs = {}
    
    #current gen data
    emitted_behavior = None
    reinforcer_type = None
    hit_target_id = None
    viewed_se = []
    chosen_bx_pop_se = None
    observed_se_num = None
    
    def __init__(self):
        pass
    
    @classmethod
    def clear_target_value_dictionary(cls):
        cls.target_value_dictionary = {}
    
    @classmethod
    def clear_gen_data(cls):
        cls.emitted_behavior = None
        cls.reinforcer_type = None
        cls.hit_target_id = None
        cls.viewed_se = []
        cls.chosen_bx_pop_se = None
        cls.observed_se_num = None
    
    # Unused
    # @classmethod
    # def clear_exp_data(cls):
    #     cls.clear_gen_data()
        
    #     #experiment data
    #     cls.primary_targets = []
    #     cls.default_gen_num = None
    #     cls.filename_modifier = None
    #     cls.total_schedule_num = None
        
    #     #modifer items
    #     cls.reward_context_switch = None
    #     cls.target_target_id = None
    #     cls.varied_target_id = None
    #     cls.user_modifier = None
    #     cls.capture_length = None
        
    #     #experiment loop current data
    #     cls.repitition_number = None
    #     cls.schedule_set_no = None
    #     cls.current_gen = None
    
    # @classmethod
    # def load_se_etbd_modifier_settings(cls,procedure_settings):
    #     se_etbd_mod_settings = procedure_settings.get("selection_modifier_parameters")
    #     if not se_etbd_mod_settings == None:
    #         for key,val in se_etbd_mod_settings.items():
    #             exec(key + '=val')
                
    
    @classmethod
    def se_shift_setup(cls,se_shift_dict):
        for target_ids in se_shift_dict.keys():
            if not Exp_Data.check_target_existance(target_ids):
                print(f'target id {target_ids} is not on the list of targets!')
                raise
            linked_se = se_shift_dict[target_ids]
            if not Stimulus_Element_Holder.check_se_existance(linked_se):
                print(f'linked_se {linked_se} is not on the list of SEs!')
                raise
                
        cls.se_shift_reinforcement_setup_pairs = se_shift_dict
        
    
    @classmethod
    def record_observed_se(cls,viewed_se):
        cls.viewed_se = viewed_se
        cls.observed_se_num = len(viewed_se)
        for se in viewed_se:
            current_count = cls.se_view_count_dic.get(se)
            if current_count == None:
                cls.se_view_count_dic.update({se:1})
                # print(f'se = {se} count = {current_count}')
            else:
                cls.se_view_count_dic.update({se:current_count+1})
                # print(f'se = {se} count = {current_count+1}')
    @classmethod
    def check_target_existance(cls,target_id_checked):
        if target_id_checked in Exp_Data.primary_targets\
        or target_id_checked in Exp_Data.background_targets:
            return True
        else:
            return False
    
    

