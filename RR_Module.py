# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 17:21:24 2022

@author: Cyrus
"""
import numpy

class Rr_Schedule:
    rr_registry = []
    
    def __init__(self,target_id, mean = 0):
        self.rr_registry.append(self)
        self.mean = mean
        self.rr_pecks_into_ratio = 0
        self.get_new_ratio()
        self.reinforcement_set_up = False
        self.target_id = target_id

    @classmethod
    def get_rr_registry(cls):
        return cls.rr_registry    
    
    @classmethod
    def clear_rr_registry(cls):
       cls.rr_registry = []
    
    @staticmethod  
    def load_rr_schedules(schedule_set_no,reinforcement_environment):
        for schedule_target in (reinforcement_environment["schedule_list"]["schedule_set_no"] \
        [schedule_set_no]["active_target_id_no"].keys()):
          
            #create RR schedule    
            if (reinforcement_environment["schedule_list"]["schedule_set_no"][schedule_set_no] \
            ["active_target_id_no"][schedule_target]["reinforcement_rate_type"]) == "RR":
                temp_mean =  reinforcement_environment \
                ["schedule_list"]["schedule_set_no"][schedule_set_no] \
                ["active_target_id_no"][schedule_target]["reinforcement_rate"]
                
                # print("RR_Schedule with id = ",schedule_target," and mean = ",temp_mean)
                Rr_Schedule(schedule_target,temp_mean)
        

    def peckpeck(hit_target_id):
        for Rr_object in Rr_Schedule.rr_registry:
            if Rr_object.target_id == hit_target_id:
                Rr_object.rr_pecks_into_ratio += 1
                # print("Target {} got pecked!".format(Rr_object.target_id))
    
    @staticmethod 
    def is_reinforcement_set_up(hit_target, is_passive = True):
        
        # for Rr_object in Rr_Schedule.rr_registry: #this loop is for printing
            # print("{} is {} pecks into ratio".format(Rr_object.target_id, Rr_object.rr_pecks_into_ratio))
            # print("{}'s current_interval is {}".format(Rr_object.target_id,Rr_object.current_ratio ))
        
        for rr_object in Rr_Schedule.rr_registry:
            if rr_object.target_id == hit_target:
                if rr_object.rr_pecks_into_ratio >= rr_object.current_ratio and rr_object.mean != 0:
                    if not is_passive:
                        rr_object.get_new_ratio()
                        rr_object.rr_pecks_into_ratio = 0
                    # print("the target hit was a RR target, AND reinforcement was set up!")
                    return True
                else:
                    # print("the target hit was a RR target, but reinforcement was NOT set up!")
                    return False
        
        # print("the target hit was not a RR target")          
        return False
      
    def get_new_ratio(self):
        
        self.current_ratio = -1 * self.mean * numpy.log(1 - numpy.random.random())
        
    def reset_pecks_into_ratio(self):
        self.rr_pecks_into_ratio = 0
    
    def get_mean(self):
        return self.mean

    def set_mean(self, value):
        self.mean = value
        self.get_new_ratio()
        self.rr_pecks_into_ratio = 0
    
    def get_target_id(self):
        return self.target_id
            