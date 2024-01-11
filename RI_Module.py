# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 12:44:00 2022

@author: Cyrus
"""
import numpy

class Ri_Schedule:
    ri_registry = []
    
    def __init__(self,target_id, mean = 0):
        self.ri_registry.append(self)
        self.mean = mean
        self.ri_ticks_into_interval = 1
        self.get_new_interval()
        self.reinforcement_set_up = False
        self.target_id = target_id

    @classmethod
    def get_ri_registry(cls):
        return cls.ri_registry    
    
    @classmethod
    def clear_ri_registry(cls):
       cls.ri_registry = []
    
    @classmethod
    def ticktock(cls):
        for schedules in cls.ri_registry:
            schedules.ri_ticks_into_interval += 1
    
    @staticmethod 
    def load_ri_schedules(schedule_set_no,reinforcement_environment):
        for schedule_target in (reinforcement_environment["schedule_list"]["schedule_set_no"] \
        [schedule_set_no]["active_target_id_no"].keys()):
          
            #create RI schedule 
            if (reinforcement_environment["schedule_list"]["schedule_set_no"][schedule_set_no] \
            ["active_target_id_no"][schedule_target]["reinforcement_rate_type"]) == "RI":
                temp_mean = reinforcement_environment \
                ["schedule_list"]["schedule_set_no"][schedule_set_no] \
                ["active_target_id_no"][schedule_target]["reinforcement_rate"]
                
                # print("Ri_Schedule with id = ",schedule_target," and mean = ",temp_mean)
                Ri_Schedule(schedule_target,temp_mean)
    
    @staticmethod 
    def is_reinforcement_set_up(hit_target, is_passive = True):
        # print("registry length = ", len(Ri_Schedule.ri_registry))
        # for RI_object in Ri_Schedule.ri_registry: #this loop is for printing
        #     print("{} is {} ticks into interval".format(RI_object.target_id, RI_object.ri_ticks_into_interval))
        #     print("{}'s current_interval is {}".format(RI_object.target_id,RI_object.current_interval ))
            
        for RI_object in Ri_Schedule.ri_registry:
            # print("hit_target = ",hit_target)
            # print("target_id for this object is = ", RI_object.target_id)
            # print("{} is {} ticks into interval".format(RI_object.target_id, RI_object.ri_ticks_into_interval))
            if RI_object.target_id == hit_target:
                # print("ri_ticks_into_interval = ",RI_object.ri_ticks_into_interval)  
                # print("current_interval = ",RI_object.current_interval )
                # print("reinforcement rate = ",RI_object.mean )
                if RI_object.ri_ticks_into_interval >= RI_object.current_interval \
                and RI_object.mean != 0:
                    if not is_passive:
                        RI_object.get_new_interval()
                        RI_object.ri_ticks_into_interval = 0
                    # print("the target hit was a RI target, AND reinforcement was set up!")
                    return True
                else:
                    # print("the target hit was a RI target, but reinforcement was NOT set up!")
                    return False
        
        # print("the target hit was not a RI target")  
        return False

    def get_new_interval(self):
        
        self.current_interval = -1 * self.mean * numpy.log(1 - numpy.random.random())
       
    def reset_ticks_into_interval(self):
        self.ri_ticks_into_interval = 0
    
    def get_mean(self):
        return self.mean

    def set_mean(self, value):
        self.mean = value
        self.get_new_interval()
        self.ri_ticks_into_interval = 0
    
    def get_target_id(self):
        return self.target_id