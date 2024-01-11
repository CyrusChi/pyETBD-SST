# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 17:21:24 2022

@author: Cyrus
"""
# import numpy

class Fr_Schedule:
    fr_registry = []
    
    def __init__(self,target_id, mean = 0):
        self.fr_registry.append(self)
        self.mean = mean
        self.fr_pecks_into_ratio = 0
        self.get_new_ratio()
        self.reinforcement_set_up = False
        self.target_id = target_id

    @classmethod
    def get_fr_registry(cls):
        return cls.fr_registry    
    
    @classmethod
    def clear_fr_registry(cls):
       cls.fr_registry = []
    
    @staticmethod  
    def load_fr_schedules(schedule_set_no,reinforcement_environment):
        for schedule_target in (reinforcement_environment["schedule_list"]["schedule_set_no"] \
        [schedule_set_no]["active_target_id_no"].keys()):
          
            #create FR schedule    
            if (reinforcement_environment["schedule_list"]["schedule_set_no"][schedule_set_no] \
            ["active_target_id_no"][schedule_target]["reinforcement_rate_type"]) == "FR":
                temp_mean =  reinforcement_environment \
                ["schedule_list"]["schedule_set_no"][schedule_set_no] \
                ["active_target_id_no"][schedule_target]["reinforcement_rate"]
                
                # print("FR_Schedule with id = ",schedule_target," and mean = ",temp_mean)
                Fr_Schedule(schedule_target,temp_mean)
        

    def peckpeck(hit_target_id):
        for Fr_object in Fr_Schedule.fr_registry:
            if Fr_object.target_id == hit_target_id:
                Fr_object.fr_pecks_into_ratio += 1
                # print("Target {} got pecked!".format(Fr_object.target_id))
    
    @staticmethod 
    def is_reinforcement_set_up(hit_target, is_passive = True):
        
        # for Fr_object in Fr_Schedule.fr_registry: #this loop is for printing
            # print("{} is {} pecks into ratio".format(Fr_object.target_id, Fr_object.fr_pecks_into_ratio))
            # print("{}'s current_interval is {}".format(Fr_object.target_id,Fr_object.current_ratio ))
        
        for fr_object in Fr_Schedule.fr_registry:
            if fr_object.target_id == hit_target:
                if fr_object.fr_pecks_into_ratio >= fr_object.current_ratio and fr_object.mean != 0:
                    if not is_passive:
                        fr_object.get_new_ratio()
                        fr_object.fr_pecks_into_ratio = 0
                    # print("the target hit was a FR target, AND reinforcement was set up!")
                    return True
                else:
                    # print("the target hit was a FR target, but reinforcement was NOT set up!")
                    return False
        
        # print("the target hit was not a FR target")          
        return False
      
    def get_new_ratio(self):
        
        self.current_ratio = self.mean
        
    def reset_pecks_into_ratio(self):
        self.fr_pecks_into_ratio = 0
    
    def get_mean(self):
        return self.mean

    def set_mean(self, value):
        self.mean = value
        self.get_new_ratio()
        self.fr_pecks_into_ratio = 0
    
    def get_target_id(self):
        return self.target_id
            