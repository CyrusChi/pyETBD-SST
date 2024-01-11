# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 12:44:00 2022

@author: Cyrus
"""
# import numpy

class Fi_Schedule:
    Fi_registry = []
    
    def __init__(self,target_id, mean = 0):
        self.fi_registry.append(self)
        self.mean = mean
        self.fi_ticks_into_interval = 1
        self.get_new_interval()
        self.reinforcement_set_up = False
        self.target_id = target_id

    @classmethod
    def get_fi_registry(cls):
        return cls.fi_registry    
    
    @classmethod
    def clear_fi_registry(cls):
       cls.fi_registry = []
    
    @classmethod
    def ticktock(cls):
        for schedules in cls.fi_registry:
            schedules.fi_ticks_into_interval += 1
    
    @staticmethod 
    def load_fi_schedules(schedule_set_no,reinforcement_environment):
        for schedule_target in (reinforcement_environment["schedule_list"]["schedule_set_no"] \
        [schedule_set_no]["active_target_id_no"].keys()):
          
            #create fi schedule 
            if (reinforcement_environment["schedule_list"]["schedule_set_no"][schedule_set_no] \
            ["active_target_id_no"][schedule_target]["reinforcement_rate_type"]) == "FI":
                temp_mean = reinforcement_environment \
                ["schedule_list"]["schedule_set_no"][schedule_set_no] \
                ["active_target_id_no"][schedule_target]["reinforcement_rate"]
                
                # pfint("Fi_Schedule with id = ",schedule_target," and mean = ",temp_mean)
                Fi_Schedule(schedule_target,temp_mean)
    
    @staticmethod 
    def is_reinforcement_set_up(hit_target, is_passive = True):
        # print("registry length = ", len(Fi_Schedule.fi_registry))
        # for FI_object in Fi_Schedule.fi_registry: #this loop is for printing
        #     print("{} is {} ticks into interval".format(FI_object.target_id, FI_object.fi_ticks_into_interval))
        #     print("{}'s current_interval is {}".format(FI_object.target_id,FI_object.current_interval ))
            
        for FI_object in Fi_Schedule.fi_registry:
            # print("hit_target = ",hit_target)
            # print("target_id for this object is = ", FI_object.target_id)
            # print("{} is {} ticks into interval".format(FI_object.target_id, FI_object.fi_ticks_into_interval))
            if FI_object.target_id == hit_target:
                # print("fi_ticks_into_interval = ",FI_object.fi_ticks_into_interval)  
                # print("current_interval = ",FI_object.current_interval )
                # print("reinforcement rate = ",FI_object.mean )
                if FI_object.fi_ticks_into_interval >= FI_object.current_interval and FI_object.mean != 0:
                    if not is_passive:
                        FI_object.get_new_interval()
                        FI_object.fi_ticks_into_interval = 0
                    # print("the target hit was a FI target, AND reinforcement was set up!")
                    return True
                else:
                    # print("the target hit was a FI target, but reinforcement was NOT set up!")
                    return False
        
        # print("the target hit was not a FI target")  
        return False

    def get_new_interval(self):
        
        self.current_interval = self.mean
       
    def reset_ticks_into_interval(self):
        self.fi_ticks_into_interval = 0
    
    def get_mean(self):
        return self.mean

    def set_mean(self, value):
        self.mean = value
        self.get_new_interval()
        self.fi_ticks_into_interval = 0
    
    def get_target_id(self):
        return self.target_id