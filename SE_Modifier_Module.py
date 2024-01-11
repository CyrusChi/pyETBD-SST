# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 15:45:16 2023
This Module is designed to hold the functions used to modify ETBD Selection/Mutation
based on the stimulus element and should allow the user to modify which one they 
want to use via the settings.
@author: Cyrus
"""
import numpy
import collections
import Organism_Module
import General_Functions_Module as gen_funct
from Data_Module import Exp_Data

class Stimulus_ETBD_Modifier:
    subclasses = {}
        
    def __int__(self):
        pass 
    
    @classmethod
    def register_subclass(cls, SE_ETBD_modifier_type):
        def decorator(subclass):
            cls.subclasses[SE_ETBD_modifier_type] = subclass
            return subclass
      
        return decorator    
    
    @classmethod
    def calculate(cls, SE_ETBD_modifier_type, *args, **kargs):
        if SE_ETBD_modifier_type not in cls.subclasses:
            raise ValueError('Bad SE ETBD modifier type {}'.format(SE_ETBD_modifier_type))
      
        return cls.subclasses[SE_ETBD_modifier_type]( *args, **kargs)
    
###############################################################################

@Stimulus_ETBD_Modifier.register_subclass('none')
class No_Modifier(Stimulus_ETBD_Modifier):
    
    def __init__(self):
        pass
   
    def __new__(self, individual_se, *args, **kargs):
        
        if individual_se == "load_parameters":
            current_selection_modifier = None
        else:
            default_percent_replace = Organism_Module.Organism.percent_replace
            current_selection_modifier = default_percent_replace
        return current_selection_modifier

###############################################################################

@Stimulus_ETBD_Modifier.register_subclass('power_function_entropy_modifier')
class Power_Function_Entropy(Stimulus_ETBD_Modifier):
    
# 	"selection_modifier_parameters":
# 	{
#             "entropy_power_conversion_a":0.065,
#             "entropy_power_conversion_b":2,
#             "selection_se_entropy_mod_lower_limit":5
# 	}

    
    
    def __init__(self):
        pass
   
    def __new__(self, individual_se, *args, **kargs):
        # print(f'individual_se = {individual_se}')
        # print(f'procedure_settings = {procedure_settings}')
         
        if individual_se == "load_parameters":
            procedure_settings = Exp_Data.procedure_settings
            Power_Function_Entropy.load(procedure_settings)
            current_selection_modifier = None
        else:
            current_selection_modifier = Power_Function_Entropy.calculate(individual_se, *args, **kargs)
        return current_selection_modifier
    
    def load(procedure_settings):
        print('loading SE ETBD Modifier parameters')
        se_etbd_mod_settings = procedure_settings.get("selection_modifier_parameters")
        Exp_Data.entropy_power_conversion_a = se_etbd_mod_settings.get('entropy_power_conversion_a')
        Exp_Data.entropy_power_conversion_b = se_etbd_mod_settings.get('entropy_power_conversion_b')
        Exp_Data.selection_se_entropy_mod_lower_limit = se_etbd_mod_settings.get('selection_se_entropy_mod_lower_limit')
        Exp_Data.selection_modifier_dict = {}
        # Exp_Data.mutation_se_entropy_mod_lower_limit = se_etbd_mod_settings.get('mutation_se_entropy_mod_lower_limit')
        
        check_failure = False
        error_items = ""      

        if not se_etbd_mod_settings:
            check_failure = True
            error_items = ''.join([error_items,'selection_modifier_parameters, '])
        if Exp_Data.entropy_power_conversion_a == None:
            check_failure = True
            error_items = ''.join([error_items,'entropy_power_conversion_a, '])
        if Exp_Data.entropy_power_conversion_b == None:
            check_failure = True
            error_items = ''.join([error_items,'entropy_power_conversion_b, '])
        if Exp_Data.selection_se_entropy_mod_lower_limit == None:
            check_failure = True
            error_items = ''.join([error_items,'selection_se_entropy_mod_lower_limit, '])            
        # if Exp_Data.mutation_se_entropy_mod_lower_limit == None:
        #     check_failure = True
        #     error_items = ''.join([error_items,'mutation_se_entropy_mod_lower_limit, '])    
        

        if check_failure == True:
            print("The following settings are missing:")
            print(f'{error_items}')
            print('\n')
            raise ValueError
       
    
    def calculate(individual_se, *args, **kargs):
        
        default_percent_replace = Organism_Module.Organism.percent_replace
        se_entropy_mod_lower_limit = Exp_Data.selection_se_entropy_mod_lower_limit
        a = Exp_Data.entropy_power_conversion_a
        b = Exp_Data.entropy_power_conversion_b
        decimal_max = Organism_Module.Organism.decimal_max
        bx_pop_behaviors = Organism_Module.Organism.Behaviors.get(individual_se)
        
        if not isinstance(bx_pop_behaviors, type(None)):
            
            pop_entropy = gen_funct.get_entropy(bx_pop_behaviors,decimal_max)
            
            #power function conversion from 0-5 to 0-1 scale
            replace_modifier = (a)*pop_entropy**b
             
            if replace_modifier > 1:
                modified_percent_replace = default_percent_replace
            elif replace_modifier*default_percent_replace > se_entropy_mod_lower_limit:
                modified_percent_replace = int(replace_modifier*default_percent_replace)
            else:
                modified_percent_replace = int(se_entropy_mod_lower_limit)
            
            # print(f'en*%repl = {round(replace_modifier,2)}',end=" ")
            # print(f'mod select = {modified_percent_replace}')
        else:
            modified_percent_replace = default_percent_replace
            # print(f'mod select (no entropy)= {modified_percent_replace}')
        
        # print(f'individual_se = {individual_se}') 
        # print(f'pop_entropy = {pop_entropy}') 
        # print(f'modified_percent_replace = {modified_percent_replace}')
        Exp_Data.selection_modifier_dict[individual_se] = modified_percent_replace
        return modified_percent_replace    
###############################################################################

@Stimulus_ETBD_Modifier.register_subclass('reinforcement_context_kernel')
class Reinforcement_Context_Kernel(Stimulus_ETBD_Modifier):
    
    
    # 	"selection_modifier_parameters":
    # 	{
    #             "starting_selection_modifier":100,
    #             "max_rc_stream_length":100,
    #             "window_no_change_boundary_lower":0.1,
    #             "window_no_change_boundary_higher":0.2,
    #             "selection_percentage_min":1,
    #             "selection_boundary":0.2
    # 	}
    
    
    
        # Exp_Data.starting_selection_modifier = se_etbd_mod_settings.get('starting_selection_modifier')
        # Exp_Data.max_rc_stream_length = se_etbd_mod_settings.get('max_rc_stream_length')
        # Exp_Data.window_no_change_boundary_lower = se_etbd_mod_settings.get('window_no_change_boundary_lower')
        # Exp_Data.window_no_change_boundary_higher = se_etbd_mod_settings.get('window_no_change_boundary_higher')
        # Exp_Data.selection_percentage_min = se_etbd_mod_settings.get('selection_percentage_min')
        # Exp_Data.selection_boundary = se_etbd_mod_settings.get('selection_boundary')
    
    def __init__(self):
        pass
   
    def __new__(self, individual_se, *args, **kargs):
        # print(f'individual_se = {individual_se}')
        # print(f'procedure_settings = {procedure_settings}')
         
        if individual_se == "load_parameters":
            procedure_settings = Exp_Data.procedure_settings
            Reinforcement_Context_Kernel.load(procedure_settings)
            current_selection_modifier = None
        else:
            current_selection_modifier = Reinforcement_Context_Kernel.calculate(individual_se, *args, **kargs)
        return current_selection_modifier
    
    def load(procedure_settings):
        print('loading SE ETBD Modifier parameters')
        #starting_modifier
        #max_rc_stream_length
        #window_no_change_boundary_lower
        #window_no_change_boundary_higher
        #selection_boundary
        #selection_min
        #
        Exp_Data.selection_modifier_dict = {}
        Exp_Data.rc_stream_past_dict = {}
        Exp_Data.rc_stream_current_dict = {}
        Exp_Data.rc_stream_length_dict = {}
        # Exp_Data.rc_stream_step_dict = {}
        Exp_Data.rc_stream_length_goal_dict = {}
        Exp_Data.rc_stream_setting_up = {}
        
        #this is currently just for exporting rc diff
        Exp_Data.rc_current_diff = {}
        
        se_etbd_mod_settings = procedure_settings.get("selection_modifier_parameters")
        Exp_Data.starting_selection_modifier = se_etbd_mod_settings.get('starting_selection_modifier')
        Exp_Data.max_rc_stream_length = se_etbd_mod_settings.get('max_rc_stream_length')
        Exp_Data.window_no_change_boundary_lower = se_etbd_mod_settings.get('window_no_change_boundary_lower')
        Exp_Data.window_no_change_boundary_higher = se_etbd_mod_settings.get('window_no_change_boundary_higher')
        Exp_Data.selection_percentage_min = se_etbd_mod_settings.get('selection_percentage_min')
        Exp_Data.selection_boundary = se_etbd_mod_settings.get('selection_boundary')
        Exp_Data.starting_rc_stream_length = se_etbd_mod_settings.get('starting_rc_stream_length')
        Exp_Data.min_rc_stream_length = se_etbd_mod_settings.get('min_rc_stream_length')
        Exp_Data.rc_stream_window_step_shorter = se_etbd_mod_settings.get('rc_stream_window_step_shorter')
        Exp_Data.rc_stream_window_step_longer = se_etbd_mod_settings.get('rc_stream_window_step_longer')
        Exp_Data.selection_modifier_step_up = se_etbd_mod_settings.get('selection_modifier_step_up')
        Exp_Data.selection_modifier_step_down = se_etbd_mod_settings.get('selection_modifier_step_down')
        check_failure = False
        error_items = ""      

        if not se_etbd_mod_settings:
            check_failure = True
            error_items = ''.join([error_items,'selection_modifier_parameters, '])
        if Exp_Data.starting_selection_modifier == None:
            check_failure = True
            error_items = ''.join([error_items,'starting_selection_modifier, '])
        if Exp_Data.max_rc_stream_length == None:
            check_failure = True
            error_items = ''.join([error_items,'max_rc_stream_length, '])
        if Exp_Data.window_no_change_boundary_lower == None:
            check_failure = True
            error_items = ''.join([error_items,'window_no_change_boundary_lower, '])            
        if Exp_Data.window_no_change_boundary_higher == None:
            check_failure = True
            error_items = ''.join([error_items,'window_no_change_boundary_higher, '])
        if Exp_Data.selection_percentage_min == None:
            check_failure = True
            error_items = ''.join([error_items,'selection_percentage_min, '])  
        if Exp_Data.selection_boundary == None:
            check_failure = True
            error_items = ''.join([error_items,'selection_boundary, ']) 
        if Exp_Data.starting_rc_stream_length == None:
            check_failure = True
            error_items = ''.join([error_items,'selection_boundary, ']) 
        if Exp_Data.min_rc_stream_length == None:
            check_failure = True
            error_items = ''.join([error_items,'min_rc_stream_length, '])    
        if Exp_Data.rc_stream_window_step_shorter == None:
            check_failure = True
            error_items = ''.join([error_items,'rc_stream_window_step_shorter, '])
        if Exp_Data.rc_stream_window_step_longer == None:
            check_failure = True
            error_items = ''.join([error_items,'rc_stream_window_step_longer, '])
        if Exp_Data.selection_modifier_step_up == None:
            check_failure = True
            error_items = ''.join([error_items,'selection_modifier_step_up, '])
        if Exp_Data.selection_modifier_step_down == None:
            check_failure = True
            error_items = ''.join([error_items,'selection_modifier_step_down, '])
             
        if check_failure == True:
            print("The following settings are missing:")
            print(f'{error_items}')
            print('\n')
            raise ValueError
                
        if Exp_Data.window_no_change_boundary_lower > Exp_Data.window_no_change_boundary_higher:
            print(f'window_no_change_boundary_lower ({Exp_Data.window_no_change_boundary_lower}) \
                  cannot be larger than window_no_change_boundary_higher ({Exp_Data.window_no_change_boundary_higher})!')
            raise ValueError
            
    def find_rc_difference(individual_se):
        past_list = Exp_Data.rc_stream_past_dict.get(individual_se)
        current_list = Exp_Data.rc_stream_current_dict.get(individual_se)
    
        past_count = past_list.count(1)
        past_len = len(past_list)
        past_ratio = past_count/past_len
        
        current_count = current_list.count(1)
        current_len = len(current_list)
        current_ratio = current_count/current_len
        
        rc_difference = current_ratio - past_ratio
        
        #currently updated for output only
        Exp_Data.rc_current_diff.update({individual_se:rc_difference})
        
        return rc_difference
    
    def modify_selection_delta(individual_se,rc_difference):
        
        current_selection_modifier = Exp_Data.selection_modifier_dict.get(individual_se)
        
        selection_boundary = Exp_Data.selection_boundary
        selection_modifier_max = 100
        selection_modifier_min = 0
        selection_modifier_step_up = Exp_Data.selection_modifier_step_up
        selection_modifier_step_down = Exp_Data.selection_modifier_step_down
        
        if abs(rc_difference) > 1:
            if rc_difference > 0:
                rc_difference = 1
            else:
                rc_difference = -1
        
        if abs(rc_difference) > selection_boundary \
        and current_selection_modifier < selection_modifier_max:
            current_selection_modifier += selection_modifier_step_up           
            if current_selection_modifier > selection_modifier_max:
                current_selection_modifier = selection_modifier_max
            Exp_Data.selection_modifier_dict[individual_se] = current_selection_modifier
            
        elif abs(rc_difference) <= selection_boundary \
        and current_selection_modifier > selection_modifier_min:     
            current_selection_modifier -= selection_modifier_step_down
            if current_selection_modifier < selection_modifier_min:
                current_selection_modifier = selection_modifier_min
            Exp_Data.selection_modifier_dict[individual_se] = current_selection_modifier
            
        else:
            pass
        
    def calculate_window_goal(individual_se,rc_difference):
        window_boundary_lower = Exp_Data.window_no_change_boundary_lower
        window_boundary_higher = Exp_Data.window_no_change_boundary_higher
        current_goal_length = Exp_Data.rc_stream_length_goal_dict.get(individual_se)
        max_length = Exp_Data.max_rc_stream_length
        min_length = Exp_Data.min_rc_stream_length
        step_shorter = Exp_Data.rc_stream_window_step_shorter
        step_longer = Exp_Data.rc_stream_window_step_longer
        
        
        # print(f'rc_diff = {abs(rc_difference)}')
        # print(f'current_goal_length = {current_goal_length}')
        # print(f'min_length = {min_length}')
        # print(f'max_length = {max_length}')
        
        if abs(rc_difference) <= window_boundary_lower\
        and current_goal_length >= (min_length+step_shorter):    
          
            Exp_Data.rc_stream_length_goal_dict.update({individual_se:current_goal_length-step_shorter})
            # print(f'abs(rc) = {abs(rc_difference)} step = {step}')
        
        elif abs(rc_difference) > window_boundary_lower\
        and abs(rc_difference) <= window_boundary_higher:
            #no change so we pass
            pass
            # print(f'abs(rc) = {abs(rc_difference)} step = {step}')
        
        elif abs(rc_difference) > window_boundary_higher\
        and current_goal_length <= (max_length-step_longer):    
         
            Exp_Data.rc_stream_length_goal_dict.update({individual_se:current_goal_length+step_longer})
            # print(f'abs(rc) = {abs(rc_difference)} step = {step}')
            
        else:
            #this case occurs when we are greater than the max or smaller than the min.
            pass
            # print(f'abs(rc) = {abs(rc_difference)} step = {step}')
            
   
    
    def calculate_next_window_step(individual_se):
        past_stream = Exp_Data.rc_stream_past_dict.get(individual_se)
        current_stream = Exp_Data.rc_stream_current_dict.get(individual_se)
        
        current_length = (len(past_stream) + len(current_stream))/2
        goal_length = numpy.ceil(Exp_Data.rc_stream_length_goal_dict.get(individual_se))
        starting_setup_check = Exp_Data.rc_stream_setting_up.get(individual_se)
        
        max_length = Exp_Data.max_rc_stream_length
        min_length = Exp_Data.min_rc_stream_length
        
        if starting_setup_check:
            if current_length < goal_length:
                active_step = 1
            if current_length >= goal_length:
                Exp_Data.rc_stream_setting_up.update({individual_se:False})
                active_step = Reinforcement_Context_Kernel.calculate_next_window_step(individual_se)
        else:
            if current_length == goal_length:
                active_step = 0
            elif current_length < goal_length\
            and current_length < max_length:
                active_step = 1
            elif current_length > goal_length\
            and current_length > min_length:
                active_step = -1
            else:
                active_step = 0
                
        return active_step
        
    def calculate(individual_se, *args, **kargs):
        
        # print(f'se = {individual_se}')
        reinforcer_type = Exp_Data.reinforcer_type
        default_percent_replace = Organism_Module.Organism.percent_replace
        selection_percentage_min = Exp_Data.selection_percentage_min
        starting_selection_modifier = Exp_Data.starting_selection_modifier
        starting_goal_length = Exp_Data.starting_rc_stream_length
        
        if reinforcer_type is not None:
            current_r = 1
        else:
            current_r = 0
        

        
        #check if the current SE is loaded into the system
        se_length = Exp_Data.rc_stream_length_dict.get(individual_se)
        
            #if it isn't, 
        if se_length == None:
            #indicate setting up
            Exp_Data.rc_stream_setting_up.update({individual_se:True})
            #set selection modifier to the starting value
            Exp_Data.selection_modifier_dict.update({individual_se:starting_selection_modifier})
            #add the C and P into the system, with P as 0, and C as current_r
            Exp_Data.rc_stream_past_dict.update({individual_se:collections.deque([0])})
            Exp_Data.rc_stream_current_dict.update({individual_se:collections.deque([current_r])})
            #actual length = 1, starting goal = starting_goal_length
            Exp_Data.rc_stream_length_dict.update({individual_se:1})
            Exp_Data.rc_stream_length_goal_dict.update({individual_se:starting_goal_length})
                
            # #find RC ratio
            # difference = Reinforcement_Context_Kernel.find_rc_difference(individual_se)
            # Reinforcement_Context_Kernel.modify_selection_delta(individual_se,difference)
            
            #calculate next step (add 1 or normal)
            # Reinforcement_Context_Kernel.calculate_window_goal(individual_se,difference)
            # Exp_Data.rc_stream_step_dict.update({individual_se:next_step})
            
        else:
            past_stream = Exp_Data.rc_stream_past_dict.get(individual_se)
            current_stream = Exp_Data.rc_stream_current_dict.get(individual_se)
            
            active_step = Reinforcement_Context_Kernel.calculate_next_window_step(individual_se)
            
            
            if len(current_stream) != len(past_stream):
                #if it is uneven, (only case is delta +1,step 2)

                #add current_rc to c
                current_stream.append(current_r)
                
                #c do not remove one
                #p do not remove one
                
                #update current stream
                Exp_Data.rc_stream_current_dict.update({individual_se:current_stream})
                
                #modify selection once set up is complete
                if not Exp_Data.rc_stream_setting_up.get(individual_se):
                    difference = Reinforcement_Context_Kernel.find_rc_difference(individual_se)
                    Reinforcement_Context_Kernel.modify_selection_delta(individual_se,difference)
                
                    #calculate next step
                    Reinforcement_Context_Kernel.calculate_window_goal(individual_se,difference)
                    # Exp_Data.rc_stream_step_dict.update({individual_se:next_step})
                
                #update current length
                current_length = (len(current_stream)+len(past_stream))/2
                Exp_Data.rc_stream_length_dict.update({individual_se:current_length})
                
            else:
            #if it is even, check for step          
                
                if  active_step == 1:
                    
                    #add current_r to C
                    current_stream.append(current_r)
                    #transfer one C to P
                    past_stream.append(current_stream[0])
                    current_stream.popleft()
                    #P do nothing
                    
                    #set next step to None <- this should never cause any problems
                    # Exp_Data.rc_stream_step_dict.update({individual_se:None})
                    #update past and current streams
                    Exp_Data.rc_stream_current_dict.update({individual_se:current_stream})
                    Exp_Data.rc_stream_past_dict.update({individual_se:past_stream})
                    
                    #this has a bias towards the current stream, since the current stream is 
                    #SHORTER than the past stream, the bias will reduce the longer the window is.
                    #this bias might be ok. "when there was high variation, more weight is 
                    #temporarily placed on the current results"
                    
                    
                    #calculate selection once set up is complete
                    if not Exp_Data.rc_stream_setting_up.get(individual_se):
                        #find RC difference
                        difference = Reinforcement_Context_Kernel.find_rc_difference(individual_se)
                        #calculate window goal
                        Reinforcement_Context_Kernel.calculate_window_goal(individual_se,difference)
                        #calculate selection change
                        Reinforcement_Context_Kernel.modify_selection_delta(individual_se,difference)
                    
                    #update current length
                    current_length = (len(current_stream)+len(past_stream))/2
                    Exp_Data.rc_stream_length_dict.update({individual_se:current_length})
                    
                elif active_step == -1:

                    #add current_r to C
                    current_stream.append(current_r)  
                    #transfer two C to P
                    past_stream.append(current_stream[0])
                    current_stream.popleft()
                    past_stream.append(current_stream[0])
                    current_stream.popleft()
                    #P drop three
                    past_stream.popleft()
                    past_stream.popleft()
                    past_stream.popleft()
                    
                    #update past and current streams
                    Exp_Data.rc_stream_current_dict.update({individual_se:current_stream})
                    Exp_Data.rc_stream_past_dict.update({individual_se:past_stream})
                    
                    #find RC difference
                    difference = Reinforcement_Context_Kernel.find_rc_difference(individual_se)
                    #calculate selection change
                    Reinforcement_Context_Kernel.modify_selection_delta(individual_se,difference)
                    
                    #calculate window goal
                    Reinforcement_Context_Kernel.calculate_window_goal(individual_se,difference)
                    # Exp_Data.rc_stream_step_dict.update({individual_se:next_step})
                    
                    #update current length
                    current_length = (len(current_stream)+len(past_stream))/2
                    Exp_Data.rc_stream_length_dict.update({individual_se:current_length})
                    
                elif active_step == 0:
                    #add current_r to C
                    current_stream.append(current_r) 
                    #transfer one C to P
                    past_stream.append(current_stream[0])
                    current_stream.popleft()
                    #P drop one
                    past_stream.popleft()
                    #update past and current streams
                    Exp_Data.rc_stream_current_dict.update({individual_se:current_stream})
                    Exp_Data.rc_stream_past_dict.update({individual_se:past_stream})
                    
                    #find RC difference
                    difference = Reinforcement_Context_Kernel.find_rc_difference(individual_se)
                    #calculate selection change
                    Reinforcement_Context_Kernel.modify_selection_delta(individual_se,difference)
                    
                    #calculate window goal
                    Reinforcement_Context_Kernel.calculate_window_goal(individual_se,difference)
                    # Exp_Data.rc_stream_step_dict.update({individual_se:next_step})
                else:
                    print(f'active_step value {active_step}, was not -1, 0, or 1')
                    raise ValueError
                    
                # default_percent_replace = Organism_Module.Organism.percent_replace
                # selection_percentage_min = Exp_Data.selection_percentage_min 
        current_selection_modifier = Exp_Data.selection_modifier_dict[individual_se]    
        
        modified_percent_replace = default_percent_replace * (current_selection_modifier/100)
        # print(f'l(c) = {len(Exp_Data.rc_stream_current_dict.get(individual_se))}; l(p) = {len(Exp_Data.rc_stream_past_dict.get(individual_se))}')
        # print("")
        if modified_percent_replace < selection_percentage_min:
            modified_percent_replace = selection_percentage_min
                
        return modified_percent_replace
                
                        
                
        
        #find RC difference
            #find r/length for past and current (proportion)
            #RC_diff = current - past (range is 1 to -1)
            
        #next step calcuation
            #if length = 1, check for only add 1, or normal
            #if length = length_max, check for only subtract, or normal
            
            #if ABS(RC_diff) <= window_no_change_boundary_lower
                #next step = -1
                
            #if ABS(RC_diff) <= window_no_change_boundary_higher
            #and ABS(RC_diff) > window_no_change_boundary_lower
                #next step = 0
            #elif ABS(RC_diff) > window_no_change_boundary_higher
                #next step = +1
                
            
        #selection mod calculation
            #if ABS(RC_diff) <= selection_boundary
            #and selection mod not selection_percentage_min:   
                #selection mod -1
                
            #if ABS(RC_diff) > selection_boundary
            #and selection mod not 100:
                #selction mod + 1 
            
                
        
        
###############################################################################        