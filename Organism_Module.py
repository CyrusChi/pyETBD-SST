# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 18:05:09 2022

@author: Cyrus
"""
import time
import numpy
import math
import General_Functions_Module as gen_funct
import collections
import Output_Module
from Parameter_Module import parameter_holder
from Data_Module import Exp_Data
from SE_Modifier_Module import Stimulus_ETBD_Modifier
from numba import njit
from numba import jit
import numpy as np

class Organism:
    Behaviors = {}
    bx_pop_size = None
    reinforcer_magnitude = {}
    number_of_binary_digits = None
    decimal_max = None
    percent_replace = None
    mutation_rate = None
    reward_context_on = False
    reward_context_target_id = None
    reward_context_varied_id = None
    reward_list_target = None
    reward_list_varied = None
    reward_setup_counter = 0
    current_reward_modifier = None
    user_set_reward_modifer_modifier = 1
    reinforcement_capture_length = None
    linear_cutoff_value = None
    cut_off_used = 0
    
    def __init__(self):
        pass
    
    @staticmethod
    def selectable_linear_fitness_check(generated_landscape,reinforcer_magnitude):
        contained_fitnesses = 0
        # emitted_bx_in_landscape = False
        gl = generated_landscape
        rm = reinforcer_magnitude
        for index in range(len(generated_landscape)):
            x = gl[index]
            parent_probability = -1*((2/(9*rm**2))*x) + 2/(3*rm)
            if parent_probability > 0:
                contained_fitnesses += 1
            
        
        # for behavior in generated_landscape:
        #     # if behavior == 0:
        #     #     emitted_bx_in_landscape = True
            
        #     if behavior <= reinforcer_magnitude*3:
        #         contained_fitnesses += 1
        
        # print(f'contained_fitnesses = {contained_fitnesses}')        
        # print(f'emitted_bx_in_landscape = {emitted_bx_in_landscape}') 
        # if contained_fitnesses < 2:
        #     raise ValueError("not enough fitnesses exist!")
        
        if contained_fitnesses <= Organism.linear_cutoff_value:
            Organism.cut_off_used += 1
            # print(f'only {contained_fitnesses} behaviors in range! alt selection used')
            return False
        else:
            # print(f'{contained_fitnesses} behaviors in range')
            return True
    
    
    @staticmethod
    def check_viewed_se_for_new(viewed):
        for se in viewed:
            if Organism.is_se_new(se) == True:
                # print("new SE, {}, detected".format(se))
                Organism.create_new_bx_pop(se)
            else:
                # print("SE, {}, is NOT new".format(se))
                continue
    
    @classmethod
    def set_linear_cutoff_value(cls, value):
        cls.linear_cutoff_value = value
            
    @classmethod
    def reset_reward_counter(cls):
        cls.reward_setup_counter = 0
    
    @classmethod
    def reset_reward_modifier(cls):
        cls.current_reward_modifier = 1
        
    @classmethod
    def is_se_new(cls,se_value):
        if se_value in cls.Behaviors:
            # print("is_se_new is returning False")
            return False
        else:
            # print("is_se_new is returning True")
            return True
    
    @classmethod
    def set_reinforcement_context_info(cls, reward_context_switch, target_target_id, \
                                       varied_target_id,user_modifer, capture_length = 500):        
        cls.reward_context_on = reward_context_switch
        if cls.reward_context_on == True:
            cls.reward_context_target_id = target_target_id
            cls.reward_context_varied_id = varied_target_id
            cls.user_set_reward_modifer_modifier = user_modifer
            cls.reinforcement_capture_length = capture_length
            cls.reward_list_target = collections.deque([0] * capture_length)
            cls.reward_list_varied = collections.deque([0] * capture_length)
        
        
    @classmethod
    def create_new_bx_pop(cls,se_value):
        random_pop = numpy.random.choice(range(0,cls.decimal_max),cls.bx_pop_size,replace = True)
        cls.Behaviors[se_value] = random_pop
    
    @classmethod
    def reset_behavior_pop(cls):
        cls.Behaviors.clear()
    
    @classmethod
    def get_behavior_pop_dict(cls):
        return cls.Behaviors   
    
    @classmethod
    def get_specific_behavior_pop(cls,stimulus_element):
        # print("key = ",stimulus_element)
        # print(cls.Behaviors.keys())
        # print(cls.Behaviors)
        # print("stimulus_element type = ", type(stimulus_element))
        return cls.Behaviors[stimulus_element]
    
    @classmethod
    def set_population_size(cls,size):
        cls.bx_pop_size = size   
    
    @classmethod
    def set_percent_replace(cls,percent_replace):
        cls.percent_replace = percent_replace       
    
    @classmethod
    def set_mutation_rate(cls,mut_rate):
        cls.mutation_rate = mut_rate 
     
    @classmethod
    def set_reinforcer_magnitude(cls,key_value_pairs):
        cls.reinforcer_magnitude.update(key_value_pairs)
     
    @classmethod
    def set_number_of_binary_digits(cls,digits):
        cls.number_of_binary_digits = digits      
        cls.decimal_max = 2**digits
    
    @classmethod
    def schedule_reset_check(cls,reset_settings):    
        if reset_settings == True:
            print("reset between schedules = true")
            cls.reset_behavior_pop()
            if cls.reward_context_on == True:
                cls.reset_reward_counter()
                cls.reset_reward_modifier()
            if Output_Module.Output.output_entropy:
                Output_Module.Output.reset_entropy_setup_counter()
            Exp_Data.se_view_count_dic = {}
            
        else:
            print("reset between schedules = false")
    
            
    @classmethod
    def collect_reinforcement_context_data(cls, current_gen, hit_target_id,reinforcer_type):
        # reward_array_target = numpy.zeros(500)
        # reward_array_varied = numpy.zeros(500)
        # reward_setup_counter = 0
        # reward_context_target_id = None
        # reward_context_varied_id = None
        if cls.reward_context_on == True:
            
            if cls.reward_setup_counter < cls.reinforcement_capture_length:
                #start filling up array
                if hit_target_id == cls.reward_context_target_id \
                and reinforcer_type != None:
                    # print(f'target {hit_target_id}, set to 1')
                    cls.reward_list_target[current_gen] = 1
                if hit_target_id == cls.reward_context_varied_id \
                and reinforcer_type != None:
                    # print(f'varied {hit_target_id}, set to 1')
                    cls.reward_list_varied[current_gen] = 1
                cls.reward_setup_counter += 1
                # print(f'target {hit_target_id}, reinforcer_type = {reinforcer_type}')
                # print(f'current gen = {current_gen}, counter = {cls.reward_setup_counter}')
                # print(f'current modifer = {cls.current_reward_modifier}')
                # print(f'list.target = {cls.reward_list_target}')
                # print(f'list.varied = {cls.reward_list_varied}')
                
            else:
                #remove next earliest element and add the newest element to the end.
                # print(f' past {cls.reinforcement_capture_length}!')
                # print(f'current gen = {current_gen}, counter = {cls.reward_setup_counter}')
                if hit_target_id == cls.reward_context_target_id \
                and reinforcer_type != None:
                    cls.reward_list_target.popleft()
                    cls.reward_list_target.append(1)
                else:
                    cls.reward_list_target.popleft()
                    cls.reward_list_target.append(0)
                if hit_target_id == cls.reward_context_varied_id \
                and reinforcer_type != None:
                    cls.reward_list_varied.popleft()
                    cls.reward_list_varied.append(1)
                else:
                    cls.reward_list_varied.popleft()
                    cls.reward_list_varied.append(0)
                cls.current_reward_modifier = cls.calculate_reward_modifier()
                # print(f'list.target = {cls.reward_list_target}')
                # print(f'list.varied = {cls.reward_list_varied}')
                # print(f'current modifer = {cls.current_reward_modifier}')
                
    @classmethod
    def calculate_reward_modifier(cls):
        if cls.reward_setup_counter < cls.reinforcement_capture_length:
            return 1
        else:
            rv = sum(cls.reward_list_varied)
            rt = sum(cls.reward_list_target)
            
            if rt == 0:
                raise ZeroDivisionError(f"target target has no reinforcers in the last {cls.reinforcement_capture_length} generations!")
            
            um = cls.user_set_reward_modifer_modifier
            
            if um > 1 or um < 0:
                raise ValueError("user reward modifier must be between zero and one (inclusive)!")
                                 
            x = rv/rt
            modifier = (x/(x+1)+0.5)*um
            
            return modifier
    
    @classmethod
    def log_children(cls,mutated_children):
        for individal_se in mutated_children.keys():
            if len(cls.Behaviors[individal_se]) < len(mutated_children[individal_se]):
                raise ValueError("children population exceeds population limits!")
            elif len(cls.Behaviors[individal_se]) == len(mutated_children[individal_se]):
                cls.Behaviors[individal_se] = mutated_children[individal_se]
                # print("children logged!")
            elif len(cls.Behaviors[individal_se]) > len(mutated_children[individal_se]):
                # print("children < original bx!")
                # if the percentage replaced is less than 100, collect old bx to pad new bx list
               
                pop_gap = len(cls.Behaviors[individal_se]) - len(mutated_children[individal_se])
                kept_index_list = numpy.random.choice(range(len(cls.Behaviors[individal_se])),pop_gap)
                for index in kept_index_list:
                    mutated_children[individal_se].append(cls.Behaviors[individal_se][int(index)])
            
            cls.Behaviors[individal_se] = numpy.asarray(mutated_children[individal_se])
###############################################################################            
class Organism_Methods:
    pass
###############################################################################
class Observation(Organism_Methods):
    subclasses = {}
    
    @classmethod
    def register_subclass(cls, observation_type):
        def decorator(subclass):
            cls.subclasses[observation_type] = subclass
            return subclass
      
        return decorator    
    
    @classmethod
    def look(cls, observation_type, *args, **kargs):
        if observation_type not in cls.subclasses:
            raise ValueError('Bad observation type {}'.format(observation_type))
      
        return cls.subclasses[observation_type](*args, **kargs)

@Observation.register_subclass('observe_up_to_five')
class Observe_Up_to_Five(Observation):
    def __init__(self,near_registry):
       pass
   
    def __new__(self,near_registry):
        temp_view = Observe_Up_to_Five.look(near_registry)
        return temp_view
    
    def look(near_registry):
        if len(near_registry) >= 5:
            temp_observed = numpy.random.choice(near_registry,5, replace = False)
        else:
            temp_observed = numpy.random.choice(near_registry,len(near_registry), replace = False)
    
        return temp_observed
  
@Observation.register_subclass('observe_up_to_three')
class Observe_Up_to_Three(Observation):
    def __init__(self):
        pass
    def __new__(self,near_registry):
        temp_view = Observe_Up_to_Five.look(near_registry)
        return temp_view
    
    def look(near_registry):
        if len(near_registry) >= 3:
            temp_observed = numpy.random.choice(near_registry,3, replace = False)
        else:
            temp_observed = numpy.random.choice(near_registry,len(near_registry), replace = False)
    
        return temp_observed
 
@Observation.register_subclass('observe5_low_entropy_5percent')
class Observe_5to_Low_Entropy5(Observation):
    #this class is designed to select 5 random SE, and from those SE,
    #select and return the bx pop with the lowest entropy,
    #and also to take the bx pops that have entropies 
    #within 10% of the lowest one
    
    def __init__(self):
        pass
    def __new__(self,near_registry):
        temp_view = Observe_5to_Low_Entropy5.look(near_registry)
        return temp_view
    
    def look(near_registry):
        #gen_funct
        observed_entropies = []
        se_focused_on = []
        # print("")
        # print(f'near registry = {near_registry}')
        if len(near_registry) >= 5:
            
            temp_observed = numpy.random.choice(near_registry,5, replace = False)
        else:
            temp_observed = numpy.random.choice(near_registry,len(near_registry), replace = False)
            
        # print(f'temp_observed = {temp_observed}')
        Organism.check_viewed_se_for_new(temp_observed)  
        for bx_pop_key in temp_observed:
            try:
                bx_pop_behaviors = Organism.Behaviors[bx_pop_key]
            except:
                continue
            
            pop_entropy = gen_funct.get_entropy(bx_pop_behaviors,Organism.decimal_max)
            observed_entropies.append(pop_entropy)
        min_entropy = min(observed_entropies)
        range_max = min_entropy + min_entropy*0.05
        # print(f'range min = {min_entropy}')
        # print(f'range max = {range_max}')
        for index in range(len(observed_entropies)):
            if observed_entropies[index] <= range_max:
                # print(f'entropy lower than max {observed_entropies[index]}')
                se_focused_on.append(temp_observed[index])
        # print(f'observed_entropies = {observed_entropies}')        
        # print(f'se_focused_on = {se_focused_on}')
        
        return se_focused_on
###############################################################################
@Observation.register_subclass('observe5_low_entropy_2pop')
class Observe_5to_Low_Entropy2(Observation):
    #this class is designed to select 5 random SE, and from those SE,
    #select and return the 2 bx pop with the lowest entropies
    
    def __init__(self):
        pass
    def __new__(self,near_registry):
        temp_view = Observe_5to_Low_Entropy2.look(near_registry)
        return temp_view
    
    def look(near_registry):
        #gen_funct
        observed_entropies = []
        se_focused_on = []
        # print("")
        # print(f'near registry = {near_registry}')
        if len(near_registry) >= 5:
            
            temp_observed = numpy.random.choice(near_registry,5, replace = False)
        else:
            temp_observed = numpy.random.choice(near_registry,len(near_registry), replace = False)
            
        # print(f'temp_observed = {temp_observed}')
        Organism.check_viewed_se_for_new(temp_observed)  
        for bx_pop_key in temp_observed:
            try:
                bx_pop_behaviors = Organism.Behaviors[bx_pop_key]
            except:
                continue
            
            pop_entropy = gen_funct.get_entropy(bx_pop_behaviors,Organism.decimal_max)
            observed_entropies.append(pop_entropy)
        min_entropy = min(observed_entropies)
        observed_entropies2 = observed_entropies.copy()
        observed_entropies2.remove(min_entropy)
        second_lowest_entropy = min(observed_entropies2)
        #range_max = min_entropy + min_entropy*0.05
        # print(f'range min = {min_entropy}')
        # print(f'range max = {range_max}')
        for index in range(len(observed_entropies)):
            if observed_entropies[index] == min_entropy:
                # print(f'entropy lower than max {observed_entropies[index]}')
                se_focused_on.append(temp_observed[index])
            if observed_entropies[index] == second_lowest_entropy:
                se_focused_on.append(temp_observed[index])
        # print(f'observed_entropies = {observed_entropies}')        
        # print(f'se_focused_on = {se_focused_on}')
        
        return se_focused_on 
###############################################################################
@Observation.register_subclass('observe5_low_entropy_x_percent')
class Observe5_to_X_Entropy(Observation):
    #this class is designed to select 5 random SE, and from those SE,
    #select and return the bx pop with the lowest entropy,
    #and also to take the bx pops that have entropies 
    #within 10% of the lowest one
    
    def __init__(self):
        pass
    def __new__(self,near_registry):
        temp_view = Observe5_to_X_Entropy.look(near_registry)
        return temp_view
    
    def look(near_registry):
        #gen_funct
        observed_entropies = []
        se_focused_on = []
        # print("")
        # print(f'near registry = {near_registry}')
        if len(near_registry) >= 5:
            
            temp_observed = numpy.random.choice(near_registry,5, replace = False)
        else:
            temp_observed = numpy.random.choice(near_registry,len(near_registry), replace = False)
            
        
        
        # print(f'temp_observed = {temp_observed}')
        Organism.check_viewed_se_for_new(temp_observed)  
        for bx_pop_key in temp_observed:
            try:
                bx_pop_behaviors = Organism.Behaviors[bx_pop_key]
            except:
                continue
            
            pop_entropy = gen_funct.get_entropy(bx_pop_behaviors,Organism.decimal_max)
            observed_entropies.append(pop_entropy)
        min_entropy = min(observed_entropies)
        try:
            entropy_limit = parameter_holder.get_entropy_percentage() * 0.01
        except KeyError:
            print("'observation_entropy_percentage' value missing from procedure settings")
        
        # print(f'entropy limit = {entropy_limit}')
        range_max = min_entropy + min_entropy * entropy_limit
        # print(f'range min = {min_entropy}')
        # print(f'range max = {range_max}')
        for index in range(len(observed_entropies)):
            if observed_entropies[index] <= range_max:
                # print(f'entropy lower than max {observed_entropies[index]}')
                se_focused_on.append(temp_observed[index])
        # print(f'observed_entropies = {observed_entropies}')        
        # print(f'se_focused_on = {se_focused_on}')
        
        return se_focused_on
###############################################################################

@Observation.register_subclass('observe5_inverse_proportion_entropy')
class Observe5_Inverse_Proportion_Entropy(Observation):
    #this class is designed to select 5 random SE, and from those SE,
    #select and return one bx pop randomly, weighted by the inverse of entropy
    #(SE with lower entropies are more likely to be chosen)
    
    def __init__(self):
        pass
    def __new__(self,near_registry):
        temp_view = Observe5_Inverse_Proportion_Entropy.look(near_registry)
        return temp_view
    
    def look(near_registry):
        #gen_funct
        observed_entropies = []
        se_focused_on = []
        # print("")
        # print(f'near registry = {near_registry}')
        if len(near_registry) >= 5:
            
            temp_observed = numpy.random.choice(near_registry,5, replace = False)
        else:
            temp_observed = numpy.random.choice(near_registry,len(near_registry), replace = False)
            
        
        
        # print(f'temp_observed = {temp_observed}')
        Organism.check_viewed_se_for_new(temp_observed)  
        for bx_pop_key in temp_observed:
            try:
                bx_pop_behaviors = Organism.Behaviors[bx_pop_key]
            except:
                continue
            
            pop_entropy = gen_funct.get_entropy(bx_pop_behaviors,Organism.decimal_max)
            observed_entropies.append(pop_entropy)
 
        # a = range(1024) #max entropy ~= 4.644 for a flat population (testcode6)
        # normal random 200 would have an average entropy of 4.55, so the min value is around 0.094
        
        inversed_observed_entropies = [4.644 - x for x in observed_entropies]
        sum_entropies_sum = sum(inversed_observed_entropies)
        proportional_inversed_entropies = [x/sum_entropies_sum for x in inversed_observed_entropies]
        se_focused_on = numpy.random.choice(temp_observed,1, replace = False, p = proportional_inversed_entropies )
        
        # print(f'observed_entropies = {observed_entropies}\n')
        # print(f'inversed_observed_entropies = {inversed_observed_entropies}\n')
        # print(f'proportional_inversed_entropies = {proportional_inversed_entropies}\n')
        # print(f'se_focused_on = {se_focused_on}\n')
        
        return se_focused_on
    
###############################################################################
class Emission(Organism_Methods):
    subclasses = {}
    
    @classmethod
    def register_subclass(cls, emission_type):
        def decorator(subclass):
            cls.subclasses[emission_type] = subclass
            return subclass
      
        return decorator    
    
    @classmethod
    def emit(cls, emission_type, viewed_se, *args, **kargs):
        if emission_type not in cls.subclasses:
            raise ValueError('Bad Emission type {}'.format(emission_type))
      
        return cls.subclasses[emission_type](viewed_se,*args, **kargs)

@Emission.register_subclass('random_emission')
class Random_Emission(Emission):
    def __init__(self,viewed_se):
       pass
   
    def __new__(self,viewed_se):
        emitted_bx = Random_Emission.emit(viewed_se)
        return emitted_bx
    
    def emit(viewed_se):
        chosen_bx_pop_key = numpy.random.choice(viewed_se,1, replace = False)
        emitted_bx = numpy.random.choice(Organism.get_specific_behavior_pop(chosen_bx_pop_key[0]),1, replace = False)
        return emitted_bx, chosen_bx_pop_key
###############################################################################
class Selection_Loop(Organism_Methods):
    subclasses = {}
    
    @classmethod
    def register_subclass(cls, selection_loop_type):
        def decorator(subclass):
            cls.subclasses[selection_loop_type] = subclass
            return subclass
      
        return decorator    
    
    @classmethod
    def run_loop(cls, selection_loop_type, emitted_behavior, reinforcer_type, \
                 chosen_bx_pop_dummy, viewed_se, procedure_settings, *args, **kargs):
        if selection_loop_type not in cls.subclasses:
            raise ValueError('Bad Selection Loop type {}'.format(selection_loop_type))
      
        return cls.subclasses[selection_loop_type](emitted_behavior, reinforcer_type, \
                     chosen_bx_pop_dummy, viewed_se, procedure_settings, *args, **kargs)

###############################################################################
@Selection_Loop.register_subclass('all_se_viewed')
class All_Se_Viewed(Selection_Loop):
    def __init__(self):
       pass
   
    def __new__(self, emitted_behavior, reinforcer_type, chosen_bx_pop, viewed_se, procedure_settings, *args, **kargs):
        
        # print("viewed_se type = ",type(viewed_se))
        # print("procedure_settings type = ",type(procedure_settings))
        all_se_parents_dict = All_Se_Viewed.run_loop2(emitted_behavior, reinforcer_type, \
                                               chosen_bx_pop, viewed_se, procedure_settings, *args, **kargs)
        
        return all_se_parents_dict
    
 #   emitted_behavior, reinforcer_type,chosen_bx_pop_dummy, viewed_se, procedure_settings

    def run_loop2(emitted_behavior, reinforcer_type, \
                  chosen_bx_pop, viewed_se, procedure_settings, *args, **kargs):
            
        # print("selection_loop run.")
        
        #get from procedure_settings- unrewarded_parent_selection_type and rewarded_parent_selection_type
        unrewarded_parent_selection_type = procedure_settings["unrewarded_parent_selection_type"]
        rewarded_parent_selection_type = procedure_settings["rewarded_parent_selection_type"]
        rewarded_selection_landscape_type = procedure_settings["rewarded_selection_landscape_type"]
        unrewarded_selection_landscape_type = procedure_settings["unrewarded_selection_landscape_type"]
        under_min_behaviors_selection_type = procedure_settings["linear_under_min_behaviors_selection_type"]
        
        all_se_parents_dict = {}
        #for loop for each se
        for individual_se in viewed_se:
            
            #recombination modifier here
            
            #if reinforcer_type is not None:
            if reinforcer_type is not None:
                # print("rewarded selection loop")
                
                #reinforcement magnitude and modifier                
                reinforcer_magnitude = Organism.reinforcer_magnitude[reinforcer_type]
                # print(f'reinforcer_magnitude = {reinforcer_magnitude}')
                if Organism.reward_context_on == True\
                and Organism.current_reward_modifier is not None:
                
                    reinforcer_magnitude = reinforcer_magnitude*Organism.current_reward_modifier
                # print(f'reinforcer_magnitude after modifier = {reinforcer_magnitude}')
                #generated_landscape = Selection_Landscape generation
                generated_landscape = Selection_Landscape.generate_landscape(rewarded_selection_landscape_type, \
                                                                             emitted_behavior, individual_se,*args, **kargs)
 
                #how many fitnesses fall into the range?
                enough_behaviors = Organism.selectable_linear_fitness_check(generated_landscape,reinforcer_magnitude)
                   
                if enough_behaviors == True:    
                #rewarded_parent_selection_type                                                             
                    new_parents = Selection_Parents.generate_parents(rewarded_parent_selection_type, individual_se,\
                                                                     reinforcer_magnitude,Organism.percent_replace,\
                                                                     Organism.bx_pop_size, generated_landscape, *args, **kargs) 
                else:
                #alt low behaviors in range selection_type
                    new_parents = Selection_Parents.generate_parents(under_min_behaviors_selection_type, individual_se,\
                                                                     reinforcer_magnitude,Organism.percent_replace,\
                                                                     Organism.bx_pop_size, generated_landscape, *args, **kargs)
                
                all_se_parents_dict.update({individual_se:new_parents})                                                                                                              
                
                #inputs: reinforcer_type_magnitude, % replacement, bx_pop_size, bx's for se, generated_landscape
                
            else:               
            #else:
                # print("unrewarded selection loop")
                reinforcer_magnitude = None
                
                
                generated_landscape = Selection_Landscape.generate_landscape(unrewarded_selection_landscape_type, emitted_behavior, 
                                                                             individual_se,*args, **kargs)
             

                
                
                #unrewarded_parent_type
                # gl_start_time = time.time()
                new_parents = Selection_Parents.generate_parents(unrewarded_parent_selection_type, individual_se,\
                                                                 reinforcer_magnitude,Organism.percent_replace,\
                                                                 Organism.bx_pop_size, generated_landscape, *args, **kargs)
                # gl_end_time = time.time()
                # print(f'parent time = {gl_end_time-gl_start_time}')   
                #inputs: reinforcer_type_magnitude, % replacement, bx_pop_size, bx's for se, generated_landscape
        #return parents_list
                all_se_parents_dict.update({individual_se:new_parents}) 
              
        return all_se_parents_dict
    
###############################################################################
@Selection_Loop.register_subclass('all_se_viewed_selection_se_time_modified')
class All_Se_Viewed_Selection_Se_Time_Modified(Selection_Loop):
    def __init__(self):
       pass
   
    def __new__(self, emitted_behavior, reinforcer_type, chosen_bx_pop, viewed_se, procedure_settings, *args, **kargs):
        
        # print("viewed_se type = ",type(viewed_se))
        # print("procedure_settings type = ",type(procedure_settings))
        all_se_parents_dict = All_Se_Viewed_Selection_Se_Time_Modified.run_loop2(emitted_behavior, reinforcer_type, \
                                               chosen_bx_pop, viewed_se, procedure_settings, *args, **kargs)
        
        return all_se_parents_dict
    
 #   emitted_behavior, reinforcer_type,chosen_bx_pop_dummy, viewed_se, procedure_settings

    def run_loop2(emitted_behavior, reinforcer_type, \
                  chosen_bx_pop, viewed_se, procedure_settings, *args, **kargs):
            
        # print("selection_loop run.")
        
        #get from procedure_settings- unrewarded_parent_selection_type and rewarded_parent_selection_type
        unrewarded_parent_selection_type = procedure_settings["unrewarded_parent_selection_type"]
        rewarded_parent_selection_type = procedure_settings["rewarded_parent_selection_type"]
        rewarded_selection_landscape_type = procedure_settings["rewarded_selection_landscape_type"]
        unrewarded_selection_landscape_type = procedure_settings["unrewarded_selection_landscape_type"]
        under_min_behaviors_selection_type = procedure_settings["linear_under_min_behaviors_selection_type"]
        
        all_se_parents_dict = {}
        #for loop for each se
        for individual_se in viewed_se:
            
            #selection modifier
            se_view_count = Exp_Data.se_view_count_dic[individual_se]
            se_time_reference = Exp_Data.se_time_reference
            se_time_mod_lower_limit = Exp_Data.selection_se_time_mod_lower_limit
            default_precent_replace = Organism.percent_replace
            se_proportion = se_view_count/se_time_reference
            test_value = (1 - se_proportion)
            if test_value*default_precent_replace > se_time_mod_lower_limit:
                modified_precent_replace = int(test_value*default_precent_replace)
            else:
                modified_precent_replace = int(se_time_mod_lower_limit)
            
            # print(f't*%repl = {round(test_value*default_precent_replace,2)}',end=" ")
            # print(f'mod select = {modified_precent_replace}')
            
            #if reinforcer_type is not None:
            if reinforcer_type is not None:
                # print("rewarded selection loop")
                
                #reinforcement magnitude and modifier                
                reinforcer_magnitude = Organism.reinforcer_magnitude[reinforcer_type]
                # print(f'reinforcer_magnitude = {reinforcer_magnitude}')
                if Organism.reward_context_on == True\
                and Organism.current_reward_modifier is not None:
                
                    reinforcer_magnitude = reinforcer_magnitude*Organism.current_reward_modifier
                # print(f'reinforcer_magnitude after modifier = {reinforcer_magnitude}')
                #generated_landscape = Selection_Landscape generation
                generated_landscape = Selection_Landscape.generate_landscape(rewarded_selection_landscape_type, \
                                                                             emitted_behavior, individual_se,*args, **kargs)
 
                #how many fitnesses fall into the range?
                enough_behaviors = Organism.selectable_linear_fitness_check(generated_landscape,reinforcer_magnitude)
                   
                if enough_behaviors == True:    
                #rewarded_parent_selection_type                                                             
                    new_parents = Selection_Parents.generate_parents(rewarded_parent_selection_type, individual_se,\
                                                                     reinforcer_magnitude,modified_precent_replace,\
                                                                     Organism.bx_pop_size, generated_landscape, *args, **kargs) 
                else:
                #alt low behaviors in range selection_type
                    new_parents = Selection_Parents.generate_parents(under_min_behaviors_selection_type, individual_se,\
                                                                     reinforcer_magnitude,modified_precent_replace,\
                                                                     Organism.bx_pop_size, generated_landscape, *args, **kargs)
                
                all_se_parents_dict.update({individual_se:new_parents})                                                                                                              
                
                #inputs: reinforcer_type_magnitude, % replacement, bx_pop_size, bx's for se, generated_landscape
                
            else:               
            #else:
                # print("unrewarded selection loop")
                reinforcer_magnitude = None
                
                
                generated_landscape = Selection_Landscape.generate_landscape(unrewarded_selection_landscape_type, emitted_behavior, 
                                                                             individual_se,*args, **kargs)
             

                
                
                #unrewarded_parent_type
                # gl_start_time = time.time()
                new_parents = Selection_Parents.generate_parents(unrewarded_parent_selection_type, individual_se,\
                                                                 reinforcer_magnitude,modified_precent_replace,\
                                                                 Organism.bx_pop_size, generated_landscape, *args, **kargs)
                # gl_end_time = time.time()
                # print(f'parent time = {gl_end_time-gl_start_time}')   
                #inputs: reinforcer_type_magnitude, % replacement, bx_pop_size, bx's for se, generated_landscape
        #return parents_list
                all_se_parents_dict.update({individual_se:new_parents}) 
              
        return all_se_parents_dict

###############################################################################
@Selection_Loop.register_subclass('all_se_viewed_selection_se_entropy_modified')
class All_Se_Viewed_Selection_Se_Entropy_Modified(Selection_Loop):
    def __init__(self):
       pass
   
    def __new__(self, emitted_behavior, reinforcer_type, chosen_bx_pop, viewed_se, procedure_settings, *args, **kargs):
        
        # print("viewed_se type = ",type(viewed_se))
        # print("procedure_settings type = ",type(procedure_settings))
        all_se_parents_dict = All_Se_Viewed_Selection_Se_Entropy_Modified.run_loop2(emitted_behavior, reinforcer_type, \
                                               chosen_bx_pop, viewed_se, procedure_settings, *args, **kargs)
        
        return all_se_parents_dict
    
 #   emitted_behavior, reinforcer_type,chosen_bx_pop_dummy, viewed_se, procedure_settings

    def run_loop2(emitted_behavior, reinforcer_type, \
                  chosen_bx_pop, viewed_se, procedure_settings, *args, **kargs):
            
        # print("selection_loop run.")
        
        #get from procedure_settings- unrewarded_parent_selection_type and rewarded_parent_selection_type
        unrewarded_parent_selection_type = procedure_settings["unrewarded_parent_selection_type"]
        rewarded_parent_selection_type = procedure_settings["rewarded_parent_selection_type"]
        rewarded_selection_landscape_type = procedure_settings["rewarded_selection_landscape_type"]
        unrewarded_selection_landscape_type = procedure_settings["unrewarded_selection_landscape_type"]
        under_min_behaviors_selection_type = procedure_settings["linear_under_min_behaviors_selection_type"]
        
        all_se_parents_dict = {}
        default_precent_replace = Organism.percent_replace
        #for loop for each se
        for individual_se in viewed_se:
            
            #selection modifier -entropy

            bx_pop_behaviors = Organism.Behaviors.get(individual_se)
            if not isinstance(bx_pop_behaviors, type(None)):
                
                pop_entropy = gen_funct.get_entropy(bx_pop_behaviors,Organism.decimal_max)
                
                se_entropy_mod_lower_limit = Exp_Data.selection_se_entropy_mod_lower_limit
                
                
                #power function conversion from 0-5 to 0-1 scale
                a = Exp_Data.entropy_power_conversion_a
                b = Exp_Data.entropy_power_conversion_b
                replace_modifier = (a)*pop_entropy**b
                 
                if replace_modifier > 1:
                    modified_precent_replace = default_precent_replace
                elif replace_modifier*default_precent_replace > se_entropy_mod_lower_limit:
                    modified_precent_replace = int(replace_modifier*default_precent_replace)
                else:
                    modified_precent_replace = int(se_entropy_mod_lower_limit)
                
                # print(f'en*%repl = {round(replace_modifier,2)}',end=" ")
                # print(f'mod select = {modified_precent_replace}')
            else:
                modified_precent_replace = default_precent_replace
                # print(f'mod select (no entropy)= {modified_precent_replace}')
                
            #if reinforcer_type is not None:
            if reinforcer_type is not None:
                # print("rewarded selection loop")
                
                #reinforcement magnitude and modifier                
                reinforcer_magnitude = Organism.reinforcer_magnitude[reinforcer_type]
                # print(f'reinforcer_magnitude = {reinforcer_magnitude}')
                if Organism.reward_context_on == True\
                and Organism.current_reward_modifier is not None:
                
                    reinforcer_magnitude = reinforcer_magnitude*Organism.current_reward_modifier
                # print(f'reinforcer_magnitude after modifier = {reinforcer_magnitude}')
                #generated_landscape = Selection_Landscape generation
                generated_landscape = Selection_Landscape.generate_landscape(rewarded_selection_landscape_type, \
                                                                             emitted_behavior, individual_se,*args, **kargs)
 
                #how many fitnesses fall into the range?
                enough_behaviors = Organism.selectable_linear_fitness_check(generated_landscape,reinforcer_magnitude)
                   
                if enough_behaviors == True:    
                #rewarded_parent_selection_type                                                             
                    new_parents = Selection_Parents.generate_parents(rewarded_parent_selection_type, individual_se,\
                                                                     reinforcer_magnitude,modified_precent_replace,\
                                                                     Organism.bx_pop_size, generated_landscape, *args, **kargs) 
                else:
                #alt low behaviors in range selection_type
                    new_parents = Selection_Parents.generate_parents(under_min_behaviors_selection_type, individual_se,\
                                                                     reinforcer_magnitude,modified_precent_replace,\
                                                                     Organism.bx_pop_size, generated_landscape, *args, **kargs)
                
                all_se_parents_dict.update({individual_se:new_parents})                                                                                                              
                
                #inputs: reinforcer_type_magnitude, % replacement, bx_pop_size, bx's for se, generated_landscape
                
            else:               
            #else:
                # print("unrewarded selection loop")
                reinforcer_magnitude = None
                
                
                generated_landscape = Selection_Landscape.generate_landscape(unrewarded_selection_landscape_type, emitted_behavior, 
                                                                             individual_se,*args, **kargs)
             

                
                
                #unrewarded_parent_type
                # gl_start_time = time.time()
                new_parents = Selection_Parents.generate_parents(unrewarded_parent_selection_type, individual_se,\
                                                                 reinforcer_magnitude,modified_precent_replace,\
                                                                 Organism.bx_pop_size, generated_landscape, *args, **kargs)
                # gl_end_time = time.time()
                # print(f'parent time = {gl_end_time-gl_start_time}')   
                #inputs: reinforcer_type_magnitude, % replacement, bx_pop_size, bx's for se, generated_landscape
        #return parents_list
                all_se_parents_dict.update({individual_se:new_parents}) 
              
        return all_se_parents_dict

###############################################################################
@Selection_Loop.register_subclass('all_se_viewed_w_se_modifier')
class Selection_Loop_w_Se_Modifier(Selection_Loop):
    def __init__(self):
       pass
   
    def __new__(self, emitted_behavior, reinforcer_type, chosen_bx_pop, viewed_se, procedure_settings, *args, **kargs):
        
        # print("viewed_se type = ",type(viewed_se))
        # print("procedure_settings type = ",type(procedure_settings))
        all_se_parents_dict = Selection_Loop_w_Se_Modifier.run_loop(emitted_behavior, reinforcer_type, \
                                               chosen_bx_pop, viewed_se, procedure_settings, *args, **kargs)
        
        return all_se_parents_dict
    
 #   emitted_behavior, reinforcer_type,chosen_bx_pop_dummy, viewed_se, procedure_settings

    def run_loop(emitted_behavior, reinforcer_type, \
                    chosen_bx_pop, viewed_se, procedure_settings, *args, **kargs):
              
        # print("selection_loop run.")
        
        #get from procedure_settings- unrewarded_parent_selection_type and rewarded_parent_selection_type
        unrewarded_parent_selection_type = procedure_settings["unrewarded_parent_selection_type"]
        rewarded_parent_selection_type = procedure_settings["rewarded_parent_selection_type"]
        rewarded_selection_landscape_type = procedure_settings["rewarded_selection_landscape_type"]
        unrewarded_selection_landscape_type = procedure_settings["unrewarded_selection_landscape_type"]
        under_min_behaviors_selection_type = procedure_settings["linear_under_min_behaviors_selection_type"]
        selection_modifier_type = procedure_settings["selection_modifier_type"]
        
        all_se_parents_dict = {}

        #for loop for each se
        for individual_se in viewed_se:
              
            modified_precent_replace = Stimulus_ETBD_Modifier.calculate(selection_modifier_type,individual_se)
                
            #if reinforcer_type is not None:
            if reinforcer_type is not None:
                # print("rewarded selection loop")
                
                #reinforcement magnitude and modifier                
                reinforcer_magnitude = Organism.reinforcer_magnitude[reinforcer_type]
                # print(f'reinforcer_magnitude = {reinforcer_magnitude}')
                if Organism.reward_context_on == True\
                and Organism.current_reward_modifier is not None:
                
                    reinforcer_magnitude = reinforcer_magnitude*Organism.current_reward_modifier
                # print(f'reinforcer_magnitude after modifier = {reinforcer_magnitude}')
                #generated_landscape = Selection_Landscape generation
                generated_landscape = Selection_Landscape.generate_landscape(rewarded_selection_landscape_type, \
                                                                             emitted_behavior, individual_se,*args, **kargs)
 
                #how many fitnesses fall into the range?
                enough_behaviors = Organism.selectable_linear_fitness_check(generated_landscape,reinforcer_magnitude)
                   
                if enough_behaviors == True:    
                #rewarded_parent_selection_type                                                             
                    new_parents = Selection_Parents.generate_parents(rewarded_parent_selection_type, individual_se,\
                                                                     reinforcer_magnitude,modified_precent_replace,\
                                                                     Organism.bx_pop_size, generated_landscape, *args, **kargs) 
                else:
                #alt low behaviors in range selection_type
                    new_parents = Selection_Parents.generate_parents(under_min_behaviors_selection_type, individual_se,\
                                                                     reinforcer_magnitude,modified_precent_replace,\
                                                                     Organism.bx_pop_size, generated_landscape, *args, **kargs)
                
                all_se_parents_dict.update({individual_se:new_parents})                                                                                                              
                
                #inputs: reinforcer_type_magnitude, % replacement, bx_pop_size, bx's for se, generated_landscape
                
            else:               
            #else:
                # print("unrewarded selection loop")
                reinforcer_magnitude = None
                
                
                generated_landscape = Selection_Landscape.generate_landscape(unrewarded_selection_landscape_type, emitted_behavior, 
                                                                             individual_se,*args, **kargs)
             

                
                
                #unrewarded_parent_type
                # gl_start_time = time.time()
                new_parents = Selection_Parents.generate_parents(unrewarded_parent_selection_type, individual_se,\
                                                                 reinforcer_magnitude,modified_precent_replace,\
                                                                 Organism.bx_pop_size, generated_landscape, *args, **kargs)
                # gl_end_time = time.time()
                # print(f'parent time = {gl_end_time-gl_start_time}')   
                #inputs: reinforcer_type_magnitude, % replacement, bx_pop_size, bx's for se, generated_landscape
        #return parents_list
                all_se_parents_dict.update({individual_se:new_parents}) 
              
        return all_se_parents_dict
    
###############################################################################


###############################################################################
class Selection_Landscape(Organism_Methods):
    subclasses = {}
    
    @classmethod
    def register_subclass(cls, selection_landscape_type):
        def decorator(subclass):
            cls.subclasses[selection_landscape_type] = subclass
            return subclass
      
        return decorator    
    
    @classmethod
    def generate_landscape(cls, selection_landscape_type, emitted_bx, individual_se, *args, **kargs):
        if selection_landscape_type not in cls.subclasses:
            raise ValueError('Bad selection landscape type {}'.format(selection_landscape_type))
      
        return cls.subclasses[selection_landscape_type](selection_landscape_type, emitted_bx, individual_se,*args, **kargs)

@Selection_Landscape.register_subclass('circular_landscape')
class Linear_Fitness(Selection_Landscape):
    def __init__(self):
       pass
   
    def __new__(self,selection_landscape_type, emitted_bx, individual_se):
        generated_landscape = Linear_Fitness.generate_landscape(selection_landscape_type, emitted_bx, individual_se)
        return generated_landscape
    
    def generate_landscape(selection_landscape_type, emitted_bx, individual_se): 
        generated_landscape = []
        behaviors = Organism.Behaviors[individual_se]
        for ea_bx in behaviors:
            oneway = abs(ea_bx - emitted_bx)
            otherway = Organism.decimal_max - 0 + 1 - oneway
            if oneway <= otherway:
                generated_landscape.append(int(oneway))
            else:
                generated_landscape.append(int(otherway))
        
        # print("emitted_bx = ",emitted_bx) 
        # print("behaviors = ",behaviors) 
        # print(f'generated_landscape = {generated_landscape}')
        return generated_landscape  
# oneWay = abs(objBehavior.get_integer_value() - self.m_behavior_list[self.m_indexOfEmittedBehavior].get_integer_value())
# 				otherWay = self.get_high_phenotype() - self.get_low_phenotype() + 1 - oneWay


@Selection_Landscape.register_subclass('none')
class No_Fitness(Selection_Landscape):
    def __init__(self):
       pass
   
    def __new__(self,selection_landscape_type, emitted_bx, individual_se):
        generated_landscape = No_Fitness.generate_landscape(selection_landscape_type, emitted_bx, individual_se)
        return generated_landscape
    
    def generate_landscape(selection_landscape_type, emitted_bx, individual_se): 
        generated_landscape = None
        return generated_landscape
    

###############################################################################
class Selection_Parents(Organism_Methods):
    subclasses = {}
    
    @classmethod
    def register_subclass(cls, parent_selection_type):
        def decorator(subclass):
            cls.subclasses[parent_selection_type] = subclass
            return subclass
      
        return decorator    
    
    @classmethod
    def generate_parents(cls, parent_selection_type, *args, **kargs):
        if parent_selection_type not in cls.subclasses:
            raise ValueError('Bad Parent Selection type {}'.format(parent_selection_type))
      
        return cls.subclasses[parent_selection_type](*args, **kargs)

                                       
###############################################################################

@Selection_Parents.register_subclass('linear_roulette_function')
class Linear__Roulette_Selection(Selection_Parents):
    def __init__(self):
       pass
   
    def __new__(self,individual_se, reinforcer_magnitude, percent_replace, \
                bx_pop_size, generated_landscape, *args, **kargs):
        
        parent_dict = Linear__Roulette_Selection.generate_parents(individual_se, reinforcer_magnitude, percent_replace, \
                                                     bx_pop_size, generated_landscape, *args, **kargs)
        return parent_dict
    
    def generate_parents(individual_se, reinforcer_magnitude, percent_replace, \
                         bx_pop_size, generated_landscape, *args, **kargs):
        # print(f'individual_se = {individual_se}')
        # print(f'reinforcer_magnitude = {reinforcer_magnitude}')
        # print(f'percent_replace = {percent_replace}')
        # print(f'bx_pop_size = {bx_pop_size}')
        # print(f'generated_landscape = {generated_landscape}')
        # print(f'generated_landscape type = {type(generated_landscape)}')
        
        
        
        parent_dict = {}    
        probability_landscape = []
        parent_pairs_generated = 0            
        replacement_num = int((bx_pop_size * percent_replace)/100)
        
        rm = reinforcer_magnitude
        gl = generated_landscape
        x = None
        probability_landscape = numpy.zeros(len(generated_landscape))
        
        for index in range(len(generated_landscape)):
            x = gl[index]
            parent_probability = -1*((2/(9*rm**2))*x) + 2/(3*rm)
            if parent_probability < 0:
                parent_probability = 0
            probability_landscape[index] = parent_probability
            
        total_prob = numpy.sum(probability_landscape)
        probability_landscape = probability_landscape / total_prob
        bx_list = Organism.Behaviors[individual_se]

        while parent_pairs_generated < replacement_num:

            #find father & mother
            [father_bx,mother_bx] = numpy.random.choice(bx_list, 2, \
                                    replace = False, p=probability_landscape )
        
            parent_pairs_generated += 1
            parent_dict.update({parent_pairs_generated:[father_bx,mother_bx]})

        return parent_dict

###############################################################################
#not yet fully implemented!!!
@Selection_Parents.register_subclass('linear_roulette_function_njit')
class Linear_Roulette_Selection_Njit(Selection_Parents):
    def __init__(self):
       pass
   
    def __new__(self,individual_se, reinforcer_magnitude, percent_replace, \
                bx_pop_size, generated_landscape, *args, **kargs):
        
        parent_dict = Linear_Roulette_Selection_Njit.generate_parents(individual_se, reinforcer_magnitude, percent_replace, \
                                                     bx_pop_size, generated_landscape, *args, **kargs)
        return parent_dict
    
    
    def generate_parents(individual_se, reinforcer_magnitude, percent_replace, \
                         bx_pop_size, generated_landscape, *args, **kargs):
        # print(f'individual_se = {individual_se}')
        # print(f'reinforcer_magnitude = {reinforcer_magnitude}')
        # print(f'percent_replace = {percent_replace}')
        # print(f'bx_pop_size = {bx_pop_size}')
        # print(f'generated_landscape = {generated_landscape}')
        # print(f'generated_landscape type = {type(generated_landscape)}')
        
        # print('roulette parents!')
        # generated_landscape is a list
        parent_dict = {}    
        # probability_landscape = []
                    
        replacement_num = int((bx_pop_size * percent_replace)/100)
        
        rm = reinforcer_magnitude
        
        
        gl_ar = numpy.asarray(generated_landscape)
        # gl_length = len(generated_landscape)
        bx_list = Organism.Behaviors[individual_se]
        bx_ar = numpy.asarray(bx_list)
        options = numpy.array((replacement_num,rm)) 
        # print(f'gl_ar = {type(gl_ar)}')
        # print(f'bx_ar = {type(bx_ar)}')
        # print(f'gl_length = {type(gl_length)}')
        # print(f'replacement_num = {type(replacement_num)}')
        # print(f'rm = {type(rm)}')
        parents_ar = Linear_Roulette_Selection_Njit.speed_roulette_selection\
                     (gl_ar,bx_ar,options)
        
        
        for row in range(replacement_num):
            
            mother_bx = parents_ar[row,0]
            father_bx = parents_ar[row,1]
            
            parent_dict.update({row:[father_bx,mother_bx]})
        # print(parent_dict)    
        return parent_dict   
    
    
    # def rand_choice_nb(arr, prob):
        
    #     #param arr: A 1D numpy array of values to sample from.
    #     #param prob: A 1D numpy array of probabilities for the given samples.
    #     #return: A random sample from the given array with a given probability.
        
    #     return arr[np.searchsorted(np.cumsum(prob), np.random.random(), side="right")]
    
    @njit
    def numba_choice(population, weights, num_choices):
        k = num_choices #number of choices
        
        # Get cumulative weights
        wc = np.cumsum(weights)
        # Total of weights
        m = wc[-1]
        # Arrays of sample and sampled indices
        sample = np.empty(k, population.dtype)
        sample_idx = np.full(k, -1, np.int32)
        # Sampling loop
        i = 0
        while i < k:
            # Pick random weight value
            r = m * np.random.rand()
            # Get corresponding index
            idx = np.searchsorted(wc, r, side='right')
            # Check index was not selected before
            # If not using Numba you can just do `np.isin(idx, sample_idx)`
            for j in range(i):
                if sample_idx[j] == idx:
                    continue
            # Save sampled value and index
            sample[i] = population[idx]
            sample_idx[i] = population[idx]
            i += 1
        return sample
    
    @njit
    def speed_roulette_selection(gl_ar,bx_ar,options):
        
        replacement_num = options[0]
        rm = options[1]
        
        gl_length = len(gl_ar)
        x = None
        probability_landscape = numpy.zeros(gl_length)
        parents_ar = np.zeros((replacement_num,2))
        for index in range(gl_length):
            x = gl_ar[index]
            parent_probability = -1*((2/(9*rm**2))*x) + 2/(3*rm)
            if parent_probability < 0:
                parent_probability = 0
            probability_landscape[index] = parent_probability
            
        total_prob = numpy.sum(probability_landscape)
        norm_probability_landscape = probability_landscape / total_prob
        
        parent_pairs_generated = 0
        # print(f'bx_ar = {type(bx_ar)}')
        # print(f'norm_probability_landscape = {type(norm_probability_landscape)}')
        while parent_pairs_generated < replacement_num:

            #find father & mother
            # [father_bx,mother_bx] = numpy.random.choice(bx_ar, 2, \
            #                         replace = False, p=probability_landscape )
            # sample = Linear_Roulette_Selection_Njit.numba_choice(bx_ar,norm_probability_landscape,2)
            
            #------------------------------------------------------------------
            # speed_roulette_selection was not connecting to numba_choice correctly when using NJIT
            # so I just reproduced it here.
            k = 2 #number of choices
            # Get cumulative weights
            wc = np.cumsum(norm_probability_landscape)
            # Total of weights
            m = wc[-1]
            # Arrays of sample and sampled indices
            sample = np.empty(k, bx_ar.dtype)
            sample_idx = np.full(k, -1, np.int32)
            # Sampling loop
            i = 0
            while i < k:
                # Pick random weight value
                r = m * np.random.rand()
                # Get corresponding index
                idx = np.searchsorted(wc, r, side='right')
                # Check index was not selected before
                # If not using Numba you can just do `np.isin(idx, sample_idx)`
                for j in range(i):
                    if sample_idx[j] == idx:
                        continue
                # Save sampled value and index
                sample[i] = bx_ar[idx]
                sample_idx[i] = bx_ar[idx]
                i += 1
            #------------------------------------------------------------------
            
            # sample = numpy.array((0,0))
            mother_bx = sample[0]
            father_bx = sample[1]
            # mother_bx_index = numpy.where(bx_ar == mother_bx)[0]
            
            # father_choice_ar = np.delete(bx_ar, mother_bx_index)
            # father_prop_ar = np.delete(probability_landscape, mother_bx_index)
            
            # father_total_prob = numpy.sum(father_prop_ar)
            # norm_father_probability_landscape = probability_landscape / father_total_prob
       
            # father_bx = Linear_Roulette_Selection_Njit.rand_choice_nb(father_choice_ar,norm_father_probability_landscape)
       
            parents_ar[parent_pairs_generated,0] = mother_bx
            parents_ar[parent_pairs_generated,1] = father_bx
           
            parent_pairs_generated += 1
        
        return parents_ar
    #     parents_ar = Random_Fitness_Simplified_Njit.speed_selection(bx_pop,replacement_num)                    
    #     #     #find father & mother
    #     #     mother_bx = None
    #     #     father_bx = None
    #     #     [father_bx,mother_bx] = numpy.random.choice(bx_pop, 2, replace = False)           
    #     #     parent_pairs_generated += 1
    #     #     parent_dict.update({parent_pairs_generated:[father_bx,mother_bx]})
    #     for row in range(replacement_num):
            
    #         mother_bx = parents_ar[row,0]
    #         father_bx = parents_ar[row,1]
            
    #         parent_dict.update({row:[father_bx,mother_bx]})
    #     # print(parent_dict)    
    #     return parent_dict   
    
    # @njit
    # def speed_selection(bx_pop,replacement_num):
    #     parent_pairs_generated = 0
    #     parents_ar = np.zeros((replacement_num,2))
    #     while parent_pairs_generated < replacement_num:
                            
    #         #find father & mother
    #         mother_bx = None
    #         father_bx = None
    #         [father_bx,mother_bx] = numpy.random.choice(bx_pop, 2, replace = False)           
    #         parents_ar[parent_pairs_generated,0] = mother_bx
    #         parents_ar[parent_pairs_generated,1] = father_bx
    #         parent_pairs_generated += 1
            
    #     return parents_ar
###############################################################################


@Selection_Parents.register_subclass('linear_selection_function')
class Linear_Selection(Selection_Parents):
    def __init__(self):
       pass
   
    def __new__(self,individual_se, reinforcer_magnitude, percent_replace, \
                bx_pop_size, generated_landscape, *args, **kargs):
        
        parent_dict = Linear_Selection.generate_parents(individual_se, reinforcer_magnitude, percent_replace, \
                                                     bx_pop_size, generated_landscape, *args, **kargs)
        return parent_dict
    
    def generate_parents(individual_se, reinforcer_magnitude, percent_replace, \
                         bx_pop_size, generated_landscape, *args, **kargs):
            parent_dict = {}    
            parent_pairs_generated = 0            
            replacement_num = int((bx_pop_size * percent_replace)/100)
            mother_while_counter = 0 #for debugging only
            father_printed = False  #for debugging only
            father_loop_counter = 0 #for debugging only
            while parent_pairs_generated < replacement_num:
                                
                #find father
                drawin_fitnesss = int(3 * reinforcer_magnitude * (1 - math.sqrt(1 - numpy.random.random())) + 0.5) - 1
                father_bx = None
                index_pos_list = []
                
                for gl_index in range(len(generated_landscape)):
                    if generated_landscape[gl_index] == drawin_fitnesss:
                        index_pos_list.append(gl_index)
                        
                if len(index_pos_list) != 0:
                    index_of_father = numpy.random.choice(index_pos_list, 1)
                    father_bx = int(Organism.Behaviors[individual_se][index_of_father])
                else:
                    if father_loop_counter > 3000 and father_printed == False:  #for debugging only
                        print('father while loop > 3000 and continuing.')
                        father_printed == True
                    
                    father_loop_counter += 1 #for debugging only
                    continue
                
                mother_not_found = True
                #find mother
                mother_printed = False
                mother_loop_counter = 0
                while mother_not_found == True:
                    mother_while_counter += 1 #for debugging only
                    mother_loop_counter += 1 #for debugging only
                    if mother_loop_counter > 3000 and mother_printed == False:  #for debugging only
                        print('mother while loop > 3000 and continuing.')
                        mother_printed == True
                    drawin_fitnesss = int(3 * reinforcer_magnitude * (1 - math.sqrt(1 - numpy.random.random())) + 0.5) - 1
                    
                    index_pos_list = []
                    for gl_index in range(len(generated_landscape)):
                        if generated_landscape[gl_index] == drawin_fitnesss:
                            index_pos_list.append(gl_index)
                            
                    if len(index_pos_list) != 0:
                        index_of_mother = numpy.random.choice(index_pos_list, 1)
                        if index_of_mother != index_of_father:
                            mother_bx = int(Organism.Behaviors[individual_se][index_of_mother])
                            mother_not_found = False
                    else:
                        continue
                
                parent_pairs_generated += 1
                parent_dict.update({parent_pairs_generated:[father_bx,mother_bx]})
                #alt method, never set up
                # index_pos_list = list(locate(generated_landscape, lambda a: a == drawin_fitnesss))    
            print("")   
            print(f' mother while loops = {mother_while_counter}') 
            print(f' father while loops = {father_loop_counter}') 
            return parent_dict
###############################################################################
# this version only draws the father based on the linear function
# the mother behavior is drawn at random from the entire pool.
@Selection_Parents.register_subclass('weaker_linear_roulette_selection_function')
class Weaker_Linear_Roulette_Selection(Selection_Parents):
    def __init__(self):
       pass
   
    def __new__(self,individual_se, reinforcer_magnitude, percent_replace, \
                bx_pop_size, generated_landscape, *args, **kargs):
        
        parent_dict = Weaker_Linear_Roulette_Selection.generate_parents(individual_se, reinforcer_magnitude, percent_replace, \
                                                     bx_pop_size, generated_landscape, *args, **kargs)
        return parent_dict
    
    def generate_parents(individual_se, reinforcer_magnitude, percent_replace, \
                         bx_pop_size, generated_landscape, *args, **kargs):
        
        parent_dict = {}    
        probability_landscape = []
        parent_pairs_generated = 0            
        replacement_num = int((bx_pop_size * percent_replace)/100)
        
        rm = reinforcer_magnitude
        gl = generated_landscape
        x = None
        probability_landscape = numpy.zeros(len(generated_landscape))
        
        for index in range(len(generated_landscape)):
            x = gl[index]
            parent_probability = -1*((2/(9*rm**2))*x) + 2/(3*rm)
            if parent_probability < 0:
                parent_probability = 0
            probability_landscape[index] = parent_probability
            
        total_prob = numpy.sum(probability_landscape)
        probability_landscape = probability_landscape / total_prob
        bx_list = Organism.Behaviors[individual_se]

        while parent_pairs_generated < replacement_num:

            #find father 
            father_index = numpy.random.choice(range(len(bx_list)), 1, \
                                    replace = False, p=probability_landscape )
            father_bx = bx_list[father_index]
            unique_mother = False
            
            #find mother
            while unique_mother == False:
                mother_index = numpy.random.choice(range(len(bx_list)), 1, \
                                        replace = False)
                if mother_index != father_index:
                    unique_mother = True
                
            mother_bx = bx_list[mother_index]
            parent_pairs_generated += 1
            parent_dict.update({parent_pairs_generated:[father_bx,mother_bx]})

        return parent_dict
###############################################################################
        
@Selection_Parents.register_subclass('random_fitness')
class Random_Fitness(Selection_Parents):
    def __init__(self):
       pass
   
    def __new__(self,individual_se, reinforcer_magnitude, percent_replace, \
                bx_pop_size, generated_landscape, *args, **kargs):
        
        parent_dict = Random_Fitness.generate_parents(individual_se, reinforcer_magnitude, percent_replace, \
                                                     bx_pop_size, generated_landscape, *args, **kargs)
        return parent_dict
    
    def generate_parents(individual_se, reinforcer_magnitude, percent_replace, \
                bx_pop_size, generated_landscape, *args, **kargs):
        parent_dict = {}    
        parent_pairs_generated = 0            
        replacement_num = int((bx_pop_size * percent_replace)/100)
        mother_while_counter = 0
     
        while parent_pairs_generated < replacement_num:
                            
            #find father
            
            father_bx = None
                       
            index_of_father = numpy.random.choice(range(len(Organism.Behaviors[individual_se])), 1)
            father_bx = int(Organism.Behaviors[individual_se][index_of_father])
          
            
            mother_not_found = True
            #find mother
            
            while mother_not_found == True:
                mother_while_counter =+1                     
                index_of_mother = numpy.random.choice(range(len(Organism.Behaviors[individual_se])), 1)
                if mother_while_counter > 100:
                    print('mother while loop > 100 and continuing.')
                if index_of_mother != index_of_father:
                    mother_bx = int(Organism.Behaviors[individual_se][index_of_mother])
                    mother_not_found = False
                else:
                    continue
            # print(f' mother while loops = {mother_while_counter}')
            parent_pairs_generated += 1
            parent_dict.update({parent_pairs_generated:[father_bx,mother_bx]})
            # index_pos_list = list(locate(generated_landscape, lambda a: a == drawin_fitnesss))    
                
               
        # print("")    
        # print(f' mother while loops = {mother_while_counter}')          
        return parent_dict   
###############################################################################
@Selection_Parents.register_subclass('random_fitness_simplifed')
class Random_Fitness_Simplified(Selection_Parents):
    def __init__(self):
       pass
   
    def __new__(self,individual_se, reinforcer_magnitude, percent_replace, \
                bx_pop_size, generated_landscape, *args, **kargs):
        
        parent_dict = Random_Fitness_Simplified.generate_parents(individual_se, reinforcer_magnitude, percent_replace, \
                                                     bx_pop_size, generated_landscape, *args, **kargs)
        return parent_dict
    
    def generate_parents(individual_se, reinforcer_magnitude, percent_replace, \
                bx_pop_size, generated_landscape, *args, **kargs):
        parent_dict = {}    
        parent_pairs_generated = 0            
        replacement_num = int((bx_pop_size * percent_replace)/100)
        
     
        while parent_pairs_generated < replacement_num:
                            
            #find father & mother
            mother_bx = None
            father_bx = None
            [father_bx,mother_bx] = numpy.random.choice(Organism.Behaviors[individual_se], 2, replace = False)           
            parent_pairs_generated += 1
            parent_dict.update({parent_pairs_generated:[father_bx,mother_bx]})
            
                   
        return parent_dict   

###############################################################################
@Selection_Parents.register_subclass('random_fitness_simplifed_njit')
class Random_Fitness_Simplified_Njit(Selection_Parents):
    def __init__(self):
       pass
   
    def __new__(self,individual_se, reinforcer_magnitude, percent_replace, \
                bx_pop_size, generated_landscape, *args, **kargs):
        
        parent_dict = Random_Fitness_Simplified_Njit.generate_parents(individual_se, reinforcer_magnitude, percent_replace, \
                                                     bx_pop_size, generated_landscape, *args, **kargs)
        return parent_dict
    
    
    def generate_parents(individual_se, reinforcer_magnitude, percent_replace, \
                bx_pop_size, generated_landscape, *args, **kargs):
        parent_dict = {}    
                   
        replacement_num = int((bx_pop_size * percent_replace)/100)
        bx_pop = Organism.Behaviors[individual_se]
        # print(f'bx_pop = {type(bx_pop)}')
        # while parent_pairs_generated < replacement_num:
        parents_ar = Random_Fitness_Simplified_Njit.speed_selection(bx_pop,replacement_num)                    
        #     #find father & mother
        #     mother_bx = None
        #     father_bx = None
        #     [father_bx,mother_bx] = numpy.random.choice(bx_pop, 2, replace = False)           
        #     parent_pairs_generated += 1
        #     parent_dict.update({parent_pairs_generated:[father_bx,mother_bx]})
        for row in range(replacement_num):
            
            mother_bx = parents_ar[row,0]
            father_bx = parents_ar[row,1]
            
            parent_dict.update({row:[father_bx,mother_bx]})
        # print(parent_dict)    
        return parent_dict   
    
    @njit
    def speed_selection(bx_pop,replacement_num):
        parent_pairs_generated = 0
        parents_ar = np.zeros((replacement_num,2))
        while parent_pairs_generated < replacement_num:
                            
            #find father & mother
            mother_bx = None
            father_bx = None
            [father_bx,mother_bx] = numpy.random.choice(bx_pop, 2, replace = False)           
            parents_ar[parent_pairs_generated,0] = mother_bx
            parents_ar[parent_pairs_generated,1] = father_bx
            parent_pairs_generated += 1
            
        return parents_ar
###############################################################################
###############################################################################
@Selection_Parents.register_subclass('under_min_throw_error')
class Under_Min_Behaviors_Error(Selection_Parents):
    def __init__(self):
       pass
   
    def __new__(self, *args, **kargs):
        
        Under_Min_Behaviors_Error.generate_parents(*args, **kargs)
        
    
    def generate_parents(individual_se, reinforcer_magnitude, percent_replace, \
                bx_pop_size, generated_landscape, *args, **kargs):
        
        raise ValueError("not enough behaviors within range!")
            
                


###############################################################################
class Recombination(Organism_Methods):
    subclasses = {}
    
    @classmethod
    def register_subclass(cls, recombination_type):
        def decorator(subclass):
            cls.subclasses[recombination_type] = subclass
            return subclass
      
        return decorator    
    
    @classmethod
    def combine(cls, recombination_type, parents_dict, num_of_bits, *args, **kargs):
        if recombination_type not in cls.subclasses:
            raise ValueError('Bad Recombination type {}'.format(recombination_type))
      
        return cls.subclasses[recombination_type](parents_dict, num_of_bits, *args, **kargs)

@Recombination.register_subclass('bitwise_recombination')
class Bitwise_Recombination(Recombination):
    def __init__(self):
       pass
   
    def __new__(self,parents_dict, num_of_bits):
        new_children_dict = Bitwise_Recombination.combine(parents_dict, num_of_bits)
        return new_children_dict
    
    def combine(parents_dict, num_of_bits):
        new_children_dict = {}
        
# =============================================================================
#         for indv_se in parents_dict.keys():
#             new_children_dict.update({indv_se:[]})  
#             for parent_pair_no in parents_dict[indv_se]:
#                   father = parents_dict[indv_se][parent_pair_no][0]
#                   mother = parents_dict[indv_se][parent_pair_no][1]
#                   father = gen_funct.pad_binary(gen_funct.convert_to_binary(father),num_of_bits)
#                   mother = gen_funct.pad_binary(gen_funct.convert_to_binary(mother),num_of_bits)
#                   child_string = ""
#                   if len(father) == len(mother):
#                       for bit in range(len(father)):
#                           bit_par = [father[bit], mother[bit]]
#                           child_bit = numpy.array2string(numpy.random.choice(bit_par,1))[2]
#                           child_string = child_string + child_bit
#                           child = gen_funct.convert_to_decimal(child_string)
#                           
#                   else:
#                       raise ValueError("binary versions of father and mother not equal length!")
#                       
#                   new_children_dict[indv_se] += [child]
# =============================================================================
        for indv_se in parents_dict.keys():
            new_children_dict.update({indv_se:[]})  
            for parent_pair_no in parents_dict[indv_se]:
                  father = int(parents_dict[indv_se][parent_pair_no][0])
                  mother = int(parents_dict[indv_se][parent_pair_no][1])
                  father = gen_funct.int_to_bool_list(father,num_of_bits)
                  mother = gen_funct.int_to_bool_list(mother,num_of_bits)
                  # print("father ",*father)
                  # print("mother ",*mother)
                  child_bool_list = [None]*num_of_bits
                  if len(father) == len(mother):
                      for bit in range(len(father)):
                          bit_par = [father[bit], mother[bit]]
                          child_bit = numpy.random.choice(bit_par,1)
                          child_bool_list[bit] = child_bit
                      # print("child ",*child_bool_list)    
                      child = gen_funct.bool_list_to_int(child_bool_list)        
                  else:
                      raise ValueError("binary versions of father and mother not equal length!")
                      
                  new_children_dict[indv_se] += [child]                  
        return new_children_dict
        
###############################################################################
@Recombination.register_subclass('bitwise_recombination_njit')
class Bitwise_Recombination_Njit(Recombination):
    def __init__(self):
       pass
   
    def __new__(self,parents_dict, num_of_bits):
        new_children_dict = Bitwise_Recombination_Njit.combine(parents_dict, num_of_bits)
        return new_children_dict
    
    @njit
    def bitwise_combine(mother_geno, father_geno):
        child_geno = np.zeros(len(mother_geno), dtype=np.int8)
        for i in range(len(child_geno)):
            if mother_geno[i] == father_geno[i]:
                child_geno[i] = mother_geno[i]
            else:
                child_geno[i] = np.random.randint(0, 2)
    
        return child_geno
        
    def combine(parents_dict, num_of_bits):
        new_children_dict = {}
        
# =============================================================================
        for indv_se in parents_dict.keys():
            new_children_dict.update({indv_se:[]})  
            for parent_pair_no in parents_dict[indv_se]:
                father = parents_dict[indv_se][parent_pair_no][0]
                mother = parents_dict[indv_se][parent_pair_no][1]
                father = gen_funct.dec_to_bin(father,num_of_bits)
                mother = gen_funct.dec_to_bin(mother,num_of_bits)
                # print("father ",*father)
                # print("mother ",*mother)
                np.empty(num_of_bits)
                  
                child_binary_ar = Bitwise_Recombination_Njit.bitwise_combine(mother, father)
                  # for bit in range(len(father)):
                  #     bit_par = [father[bit], mother[bit]]
                  #     child_bit = numpy.random.choice(bit_par,1)
                  #     child_bool_list[bit] = child_bit
                # print("child ",*child_bool_list)    
                child = gen_funct.bin_to_dec(child_binary_ar)        

                      
                new_children_dict[indv_se] += [child]                  
        return new_children_dict
        
###############################################################################


class Mutation(Organism_Methods):
    subclasses = {}
    
    @classmethod
    def register_subclass(cls, mutation_type):
        def decorator(subclass):
            cls.subclasses[mutation_type] = subclass
            return subclass
      
        return decorator    
    
    @classmethod
    def mutate(cls, mutation_type, *args, **kargs):
        if mutation_type not in cls.subclasses:
            raise ValueError('Bad Mutation type {}'.format(mutation_type))
        
        return cls.subclasses[mutation_type](*args, **kargs)

@Mutation.register_subclass('bitflip_by_individual')
class Bitflip_individual(Mutation):
    def __init__(self):
       pass
   
    def __new__(self,children_dict):
        
        mutation_rate = Organism.mutation_rate
        num_of_bits = Organism.number_of_binary_digits
        
        if children_dict == "load_parameters":
            post_mutation_children = None
        else:
            post_mutation_children = Bitflip_individual.mutate(children_dict, mutation_rate, num_of_bits)
        return post_mutation_children
    
    def mutate(children_dict, mutation_rate, num_of_bits):
        post_mutation_children = {}
        for indv_se in children_dict.keys():
                        
            post_mutation_children.update({indv_se:[]})  
            if mutation_rate > 100:
                raise ValueError("mutation rate cannoy be over 100!")
            children_to_mutate = int(len(children_dict[indv_se])*mutation_rate/100)
            # print("len of chidren = ",len(children_dict[indv_se]))
            # print("type = ",type(len(children_dict[indv_se])))
            mutation_index_list = numpy.random.choice(range(len(children_dict[indv_se])),children_to_mutate)
            # print("mut index list = ",mutation_index_list )
            for index in mutation_index_list:
                # print("index = ", index)
                child_to_mutate = children_dict[indv_se][index]
                
# ==string based methods=======================================================
#                 
# better          #megha_change
#                 #child_to_mutate_binary = gen_funct.convert_to_binary(child_to_mutate,num_of_bits)
#                 #finished megha_change
#                 
# older           #print("child to mutate = ",child_to_mutate)
#                 #child_to_mutate_binary = gen_funct.pad_binary(gen_funct.convert_to_binary(child_to_mutate),num_of_bits) 
#                 
#                 #print("child to mutate(binary) = ",child_to_mutate_binary)
#                
#                 # if child_to_mutate_binary[mutate_bit_index] == 1:
#                 #     child_to_mutate_binary = child_to_mutate_binary[:mutate_bit_index] + "0" + \
#                 #                              child_to_mutate_binary[mutate_bit_index+1:]
#                     
#                 # else:
#                 #     child_to_mutate_binary = child_to_mutate_binary[:mutate_bit_index] + "1" + \
#                 #                              child_to_mutate_binary[mutate_bit_index+1:]
#                 # # print ("NEW child_to_mutate_binary = ",child_to_mutate_binary)
#                 # children_dict[indv_se][index] = gen_funct.convert_to_decimal(child_to_mutate_binary)
#
# =============================================================================
                
                child_to_mutate_binary = gen_funct.int_to_bool_list(child_to_mutate,num_of_bits)
                
                mutate_bit_index = int(numpy.random.choice(range(len(child_to_mutate_binary)),1))
                # print("")
                # print ("OLD child_to_mutate_binary = ",child_to_mutate_binary)
                # print("")
                # print("mutate_bit_index = ",mutate_bit_index)
                # print("child_to_mutate_binary[mutate_bit_index] = ", child_to_mutate_binary[mutate_bit_index])

                if child_to_mutate_binary[mutate_bit_index] == True:
                    child_to_mutate_binary[mutate_bit_index] = False
                    
                else:
                    child_to_mutate_binary[mutate_bit_index] = True
                # print("")    
                # print ("NEW child_to_mutate_binary = ",child_to_mutate_binary)
                children_dict[indv_se][index] = gen_funct.bool_list_to_int(child_to_mutate_binary)
            post_mutation_children[indv_se] += children_dict[indv_se]


        return post_mutation_children
    
###############################################################################
@Mutation.register_subclass('bitflip_by_individual_se_time_modified')
class Bitflip_individual_se_mod(Mutation):
    def __init__(self):
       pass
   
    def __new__(self,children_dict):
        
        mutation_rate = Organism.mutation_rate
        num_of_bits = Organism.number_of_binary_digits
        
        if children_dict == "load_parameters":
            post_mutation_children = None
        else:
            post_mutation_children = Bitflip_individual_se_mod.mutate(children_dict, mutation_rate, num_of_bits)
        return post_mutation_children
    
    def mutate(children_dict, mutation_rate, num_of_bits):
        post_mutation_children = {}
        for indv_se in children_dict.keys():
            
            #modify mutation rate
            SE_view_count = Exp_Data.se_view_count_dic[indv_se]
            SE_time_reference = Exp_Data.se_time_reference
            SE_time_mod_lower_limit = Exp_Data.mutation_se_time_mod_lower_limit
            
            SE_view_proportion = SE_view_count/SE_time_reference
            test_value = (1 - SE_view_proportion)
            if test_value*mutation_rate > SE_time_mod_lower_limit:
                mutation_rate_modifier = test_value
            else: 
                mutation_rate_modifier = SE_time_mod_lower_limit/mutation_rate
            
            post_mutation_children.update({indv_se:[]})  
            if mutation_rate > 100:
                raise ValueError("mutation rate cannoy be over 100!")
            children_to_mutate = int(len(children_dict[indv_se])*(mutation_rate*mutation_rate_modifier)/100)
            # print("len of chidren = ",len(children_dict[indv_se]))
            # print("type = ",type(len(children_dict[indv_se])))
            
            # print(f' default mutation = {mutation_rate}')
            # print(f' t*mut = {round(test_value*mutation_rate,2)}',end=" ")
            # print(f' mut = {round(mutation_rate_modifier*mutation_rate,2)}',end=" ")
            # print(f' c = {children_to_mutate}')
            
            if children_to_mutate > 0:
                
                mutation_index_list = numpy.random.choice(range(len(children_dict[indv_se])),children_to_mutate)
                # print("mut index list = ",mutation_index_list )
                for index in mutation_index_list:
                    # print("index = ", index)
                    child_to_mutate = children_dict[indv_se][index]
                               
                    child_to_mutate_binary = gen_funct.int_to_bool_list(child_to_mutate,num_of_bits)
                    
                    mutate_bit_index = int(numpy.random.choice(range(len(child_to_mutate_binary)),1))
                    
                    if child_to_mutate_binary[mutate_bit_index] == True:
                        child_to_mutate_binary[mutate_bit_index] = False
                        
                    else:
                        child_to_mutate_binary[mutate_bit_index] = True
                    # print("")    
                    # print ("NEW child_to_mutate_binary = ",child_to_mutate_binary)
                    children_dict[indv_se][index] = gen_funct.bool_list_to_int(child_to_mutate_binary)
                post_mutation_children[indv_se] += children_dict[indv_se]
            else:
                post_mutation_children[indv_se] += children_dict[indv_se]
                
        return post_mutation_children
   
###############################################################################
@Mutation.register_subclass('bitflip_by_individual_se_entropy_modified')
class Bitflip_individual_se_entropy_mod(Mutation):
    def __init__(self):
       pass
   
    def __new__(self,children_dict):
        
        mutation_rate = Organism.mutation_rate
        num_of_bits = Organism.number_of_binary_digits
        
        if children_dict == "load_parameters":
            post_mutation_children = None
        else:
            post_mutation_children = Bitflip_individual_se_entropy_mod.mutate(children_dict, mutation_rate, num_of_bits)
        return post_mutation_children
    
    def mutate(children_dict, default_mutation_rate, num_of_bits):
        post_mutation_children = {}
        for indv_se in children_dict.keys():         
            
            #modify mutation rate
            
            bx_pop_behaviors = Organism.Behaviors.get(indv_se)

            pop_entropy = gen_funct.get_entropy(bx_pop_behaviors,Organism.decimal_max)
            
            se_entropy_mod_lower_limit = Exp_Data.mutation_se_entropy_mod_lower_limit
            
            #power function conversion from 0-5 to 0-1 scale
            a = Exp_Data.entropy_power_conversion_a
            b = Exp_Data.entropy_power_conversion_b
            mutation_rate_modifier = (a)*pop_entropy**b
            
            if mutation_rate_modifier > 1:
                modified_mutation_rate = default_mutation_rate
            elif mutation_rate_modifier*default_mutation_rate > se_entropy_mod_lower_limit:
                modified_mutation_rate = mutation_rate_modifier*default_mutation_rate
            else: 
                modified_mutation_rate = se_entropy_mod_lower_limit
                
            post_mutation_children.update({indv_se:[]})  
            if modified_mutation_rate > 100:
                raise ValueError("mutation rate cannoy be over 100!")
            children_to_mutate = int(len(children_dict[indv_se])*(modified_mutation_rate)/100)
            # print("len of chidren = ",len(children_dict[indv_se]))
            # print("type = ",type(len(children_dict[indv_se])))
            
            # print(f' default mutation = {mutation_rate}')
            # print(f' mut_mod = {round(mutation_rate_modifier,2)}',end=" ")
            # print(f' mut = {round(modified_mutation_rate,2)}',end=" ")
            # print(f' c = {children_to_mutate}')
                           
            if children_to_mutate > 0:
                
                mutation_index_list = numpy.random.choice(range(len(children_dict[indv_se])),children_to_mutate)
                # print("mut index list = ",mutation_index_list )
                for index in mutation_index_list:
                    # print("index = ", index)
                    child_to_mutate = children_dict[indv_se][index]
                               
                    child_to_mutate_binary = gen_funct.int_to_bool_list(child_to_mutate,num_of_bits)
                    
                    mutate_bit_index = int(numpy.random.choice(range(len(child_to_mutate_binary)),1))
                    
                    if child_to_mutate_binary[mutate_bit_index] == True:
                        child_to_mutate_binary[mutate_bit_index] = False
                        
                    else:
                        child_to_mutate_binary[mutate_bit_index] = True
                    # print("")    
                    # print ("NEW child_to_mutate_binary = ",child_to_mutate_binary)
                    children_dict[indv_se][index] = gen_funct.bool_list_to_int(child_to_mutate_binary)
                post_mutation_children[indv_se] += children_dict[indv_se]
            else:
                post_mutation_children[indv_se] += children_dict[indv_se]
                
        return post_mutation_children
    
###############################################################################
@Mutation.register_subclass('bitflip_by_individual_se_entropy_modified_min1')
class Bitflip_individual_se_entropy_mod_min1(Mutation):
    def __init__(self):
       pass
   
    def __new__(self,children_dict):
        
        default_mutation_rate = Organism.mutation_rate
        num_of_bits = Organism.number_of_binary_digits
        
        if children_dict == "load_parameters":
            post_mutation_children = None
        else:
            post_mutation_children = Bitflip_individual_se_entropy_mod_min1.mutate(children_dict, default_mutation_rate, num_of_bits)
        return post_mutation_children
    
    def mutate(children_dict, default_mutation_rate, num_of_bits):
        post_mutation_children = {}
        for indv_se in children_dict.keys():         
            
            #modify mutation rate
            
            bx_pop_behaviors = Organism.Behaviors.get(indv_se)

            pop_entropy = gen_funct.get_entropy(bx_pop_behaviors,Organism.decimal_max)
            
            se_entropy_mod_lower_limit = Exp_Data.mutation_se_entropy_mod_lower_limit
            
            #power function conversion from 0-5 to 0-1 scale
            a = Exp_Data.entropy_power_conversion_a
            b = Exp_Data.entropy_power_conversion_b
            mutation_rate_modifier = (a)*pop_entropy**b
            
            if mutation_rate_modifier > 1:
                modified_mutation_rate = default_mutation_rate
            elif mutation_rate_modifier*default_mutation_rate > se_entropy_mod_lower_limit:
                modified_mutation_rate = mutation_rate_modifier*default_mutation_rate
            else: 
                modified_mutation_rate = se_entropy_mod_lower_limit
                
            post_mutation_children.update({indv_se:[]})  
            if modified_mutation_rate > 100:
                raise ValueError("mutation rate cannoy be over 100!")
            children_to_mutate = int(len(children_dict[indv_se])*(modified_mutation_rate)/100)
            # print("len of chidren = ",len(children_dict[indv_se]))
            # print("type = ",type(len(children_dict[indv_se])))
            
            # print(f' default mutation = {mutation_rate}')
            # print(f' mut_mod = {round(mutation_rate_modifier,2)}',end=" ")
            # print(f' mut = {round(modified_mutation_rate,2)}',end=" ")
            # print(f' c = {children_to_mutate}')
            
            #if children_to_mutate == 0:
            #    children_to_mutate = 1
            
            if children_to_mutate > 0:
                
                mutation_index_list = numpy.random.choice(range(len(children_dict[indv_se])),children_to_mutate)
                # print("mut index list = ",mutation_index_list )
                for index in mutation_index_list:
                    # print("index = ", index)
                    child_to_mutate = children_dict[indv_se][index]
                               
                    child_to_mutate_binary = gen_funct.int_to_bool_list(child_to_mutate,num_of_bits)
                    
                    mutate_bit_index = int(numpy.random.choice(range(len(child_to_mutate_binary)),1))
                    
                    if child_to_mutate_binary[mutate_bit_index] == True:
                        child_to_mutate_binary[mutate_bit_index] = False
                        
                    else:
                        child_to_mutate_binary[mutate_bit_index] = True
                    # print("")    
                    # print ("NEW child_to_mutate_binary = ",child_to_mutate_binary)
                    children_dict[indv_se][index] = gen_funct.bool_list_to_int(child_to_mutate_binary)
                post_mutation_children[indv_se] += children_dict[indv_se]
            else:
                post_mutation_children[indv_se] += children_dict[indv_se]
                
        return post_mutation_children

###############################################################################
@Mutation.register_subclass('bitflip_by_individual_min1')
class Bitflip_individual_min1(Mutation):
    def __init__(self):
       pass
   
    def __new__(self,children_dict):
        
        default_mutation_rate = Organism.mutation_rate
        num_of_bits = Organism.number_of_binary_digits
        
        if children_dict == "load_parameters":
            post_mutation_children = None
        else:
            post_mutation_children = Bitflip_individual_min1.mutate(children_dict, default_mutation_rate, num_of_bits)
        return post_mutation_children
    
    def mutate(children_dict, default_mutation_rate, num_of_bits):
        post_mutation_children = {}
        for indv_se in children_dict.keys():         
                      
            modified_mutation_rate = default_mutation_rate
            bx_pop_behaviors = Organism.Behaviors.get(indv_se)
            
            post_mutation_children.update({indv_se:[]})  
            if modified_mutation_rate > 100:
                raise ValueError("mutation rate cannoy be over 100!")
            children_to_mutate = int(len(children_dict[indv_se])*(modified_mutation_rate)/100)
            # print("len of chidren = ",len(children_dict[indv_se]))
            # print("type = ",type(len(children_dict[indv_se])))
            
            # print(f' default mutation = {mutation_rate}')
            # print(f' mut_mod = {round(mutation_rate_modifier,2)}',end=" ")
            # print(f' mut = {round(modified_mutation_rate,2)}',end=" ")
            # print(f' c = {children_to_mutate}')
            
            if children_to_mutate == 0:
            #if there are no children to mutate, mutate one of the original bx population    
                bx_pop_mut_index = numpy.random.choice(range(len(bx_pop_behaviors)),1)
                child_to_mutate = Organism.Behaviors[indv_se][bx_pop_mut_index]
                           
                child_to_mutate_binary = gen_funct.int_to_bool_list(child_to_mutate,num_of_bits)
                 
                mutate_bit_index = int(numpy.random.choice(range(len(child_to_mutate_binary)),1))
                 
                if child_to_mutate_binary[mutate_bit_index] == True:
                    child_to_mutate_binary[mutate_bit_index] = False
                     
                else:
                    child_to_mutate_binary[mutate_bit_index] = True
                # print("")    
                # print ("NEW child_to_mutate_binary = ",child_to_mutate_binary)
                Organism.Behaviors[indv_se][bx_pop_mut_index] = gen_funct.bool_list_to_int(child_to_mutate_binary)
            
            if children_to_mutate > 0:
                
                mutation_index_list = numpy.random.choice(range(len(children_dict[indv_se])),children_to_mutate)
                # print("mut index list = ",mutation_index_list )
                for index in mutation_index_list:
                    # print("index = ", index)
                    child_to_mutate = children_dict[indv_se][index]
                               
                    child_to_mutate_binary = gen_funct.int_to_bool_list(child_to_mutate,num_of_bits)
                    
                    mutate_bit_index = int(numpy.random.choice(range(len(child_to_mutate_binary)),1))
                    
                    if child_to_mutate_binary[mutate_bit_index] == True:
                        child_to_mutate_binary[mutate_bit_index] = False
                        
                    else:
                        child_to_mutate_binary[mutate_bit_index] = True
                    # print("")    
                    # print ("NEW child_to_mutate_binary = ",child_to_mutate_binary)
                    children_dict[indv_se][index] = gen_funct.bool_list_to_int(child_to_mutate_binary)
                post_mutation_children[indv_se] += children_dict[indv_se]
            else:
                post_mutation_children[indv_se] += children_dict[indv_se]
                
        return post_mutation_children
    
###############################################################################
@Mutation.register_subclass('bitflip_by_individual_min1_every_x')
class Bitflip_individual_min1_every_x(Mutation):
    def __init__(self):
       pass
   
    def __new__(self,children_dict):
        
        default_mutation_rate = Organism.mutation_rate
        num_of_bits = Organism.number_of_binary_digits
        
        if children_dict == "load_parameters":
            procedure_settings = Exp_Data.procedure_settings
            Bitflip_individual_min1_every_x.load(procedure_settings)
            post_mutation_children = None
        else:
            post_mutation_children = Bitflip_individual_min1_every_x.mutate(children_dict, default_mutation_rate, num_of_bits)
        return post_mutation_children

    
    def load(procedure_settings):
        print('loading Bitflip_individual_min1_every_x parameters')
        #mutation_min_every_x_modifier
        
        Exp_Data.mutation_min_every_x_modifier = None
        Exp_Data.mutation_min_every_x_count_dict = {}
        
        mutation_mod_settings = procedure_settings.get("mutation_modifier_parameters")
        Exp_Data.mutation_min_every_x_modifier = mutation_mod_settings.get('mutation_min_every_x_modifier')
        
        check_failure = False
        error_items = ""      
       
        
        # if not mutation_mod_settings:
        #     check_failure = True
        #     error_items = ''.join([error_items,'mutation_modifier_parameters, '])
        # if Exp_Data.mutation_min_every_x_modifier == None:
        #     check_failure = True
        #     error_items = ''.join([error_items,'mutation_min_every_x_modifier, '])
        
        if not mutation_mod_settings:
            check_failure = True
            error_items = ''.join([error_items,'mutation_modifier_parameters, '])
        if Exp_Data.mutation_min_every_x_modifier == None or Exp_Data.mutation_min_every_x_modifier == 0:
            if Exp_Data.mutation_min_every_x_modifier == 0:
                print('mutation min every x was (0), and was converted to (None)')
                Exp_Data.mutation_min_every_x_modifier = None
            print('every x modifier is not active. Mutation might not occur if selection modifier is too low')
                 
        if check_failure == True:
            print("The following settings are missing:")
            print(f'{error_items}')
            print('\n')
            raise ValueError
                
        if Exp_Data.mutation_min_every_x_modifier != None:
            if Exp_Data.mutation_min_every_x_modifier < 0:
                print(f'mutation_min_every_x_modifier({Exp_Data.mutation_min_every_x_modifier}) \
                      must be null or a positive interger')
                raise ValueError

    
    def mutate(children_dict, default_mutation_rate, num_of_bits):
        
        max_count_at_zero = Exp_Data.mutation_min_every_x_modifier
        current_at_zero_count_dict = Exp_Data.mutation_min_every_x_count_dict
        
        post_mutation_children = {}
        for indv_se in children_dict.keys():         
                      
            modified_mutation_rate = default_mutation_rate
            bx_pop_behaviors = Organism.Behaviors.get(indv_se)
            
            post_mutation_children.update({indv_se:[]})  
            if modified_mutation_rate > 100:
                raise ValueError("mutation rate cannoy be over 100!")
            children_to_mutate = int(len(children_dict[indv_se])*(modified_mutation_rate)/100)
            # print("len of chidren = ",len(children_dict[indv_se]))
            # print("type = ",type(len(children_dict[indv_se])))
            
            # print(f' default mutation = {mutation_rate}')
            # print(f' mut_mod = {round(mutation_rate_modifier,2)}',end=" ")
            # print(f' mut = {round(modified_mutation_rate,2)}',end=" ")
            # print(f' c = {children_to_mutate}')
            
            if not max_count_at_zero == None:
                if children_to_mutate == 0:
                #if there are no children to mutate, add to count
                    # print('no children to mutate')
                    se_count = current_at_zero_count_dict.get(indv_se)
                    if se_count == None:
                        Exp_Data.mutation_min_every_x_count_dict.update({indv_se:1})
                        # print(f'{indv_se}:1')
                    elif se_count < max_count_at_zero:
                        Exp_Data.mutation_min_every_x_count_dict.update({indv_se:se_count+1})
                        # print(f'{indv_se}:{se_count+1}')
               #if count => max do a single random mutation to the original pop     
                    else:
                        # print(f'{indv_se}:{se_count} MUTATE!')
                        Exp_Data.mutation_min_every_x_count_dict.update({indv_se:0})
                
                        bx_pop_mut_index = numpy.random.choice(range(len(bx_pop_behaviors)),1)
                        child_to_mutate = Organism.Behaviors[indv_se][bx_pop_mut_index]
                                   
                        child_to_mutate_binary = gen_funct.int_to_bool_list(child_to_mutate,num_of_bits)
                         
                        mutate_bit_index = int(numpy.random.choice(range(len(child_to_mutate_binary)),1))
                         
                        if child_to_mutate_binary[mutate_bit_index] == True:
                            child_to_mutate_binary[mutate_bit_index] = False
                             
                        else:
                            child_to_mutate_binary[mutate_bit_index] = True
                        # print("")    
                        # print ("NEW child_to_mutate_binary = ",child_to_mutate_binary)
                        Organism.Behaviors[indv_se][bx_pop_mut_index] = gen_funct.bool_list_to_int(child_to_mutate_binary)
            
            if children_to_mutate > 0:
                
                mutation_index_list = numpy.random.choice(range(len(children_dict[indv_se])),children_to_mutate)
                # print("mut index list = ",mutation_index_list )
                for index in mutation_index_list:
                    # print("index = ", index)
                    child_to_mutate = children_dict[indv_se][index]
                               
                    child_to_mutate_binary = gen_funct.int_to_bool_list(child_to_mutate,num_of_bits)
                    
                    mutate_bit_index = int(numpy.random.choice(range(len(child_to_mutate_binary)),1))
                    
                    if child_to_mutate_binary[mutate_bit_index] == True:
                        child_to_mutate_binary[mutate_bit_index] = False
                        
                    else:
                        child_to_mutate_binary[mutate_bit_index] = True
                    # print("")    
                    # print ("NEW child_to_mutate_binary = ",child_to_mutate_binary)
                    children_dict[indv_se][index] = gen_funct.bool_list_to_int(child_to_mutate_binary)
                post_mutation_children[indv_se] += children_dict[indv_se]
            else:
                post_mutation_children[indv_se] += children_dict[indv_se]
                
        return post_mutation_children
    
