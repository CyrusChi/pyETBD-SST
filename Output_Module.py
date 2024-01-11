# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 19:47:50 2022

@author: Cyrus
"""
#create reinforcer set (these are based on which target is reinforced)
#create behavior set (these are based on which target behavior is emitted)
import numpy
import collections
import Organism_Module
import General_Functions_Module
from Data_Module import Exp_Data
from SE_Module import Stimulus_Element_Holder

class Output:
    
    setupclasses = {}
    captureclasses = {} 
    exportclasses = {}
    
    stream_log = []
    output_column_titles = []
    entropy_moving_average = []
    current_schedule = None
    primary_target_ids = None
    output_type_record = None
    Output_filename_modifer = None
    output_row_index = None
    output_entropy = False
    output_selection_modifier = False
    output_background = False
    entropy_setup_counter = 0
    output_entropy_moving_avg_length = 0
    output_emitted_behavior_population = False
    
    @staticmethod
    def get_output_row_index():
        return Output.output_row_index
    
    @classmethod
    def increment_x_index(cls):
        cls.output_row_index += 1
    
    @classmethod
    def reset_entropy_setup_counter(cls):
        cls.entropy_setup_counter = 0
        cls.entropy_moving_average = collections.deque([0] * Output.output_entropy_moving_avg_length)
    
        
    @classmethod
    def set_output_emitted_behavior_population(cls,value = False):
        cls.output_emitted_behavior_population = value
    
    @classmethod
    def set_output_entropy(cls,value = False):
        cls.output_entropy = value
    
    @classmethod
    def set_output_selection_modifier(cls,value = False):
        cls.output_selection_modifier = value
    
    @classmethod
    def set_output_background(cls,value = False):
        cls.output_background = value
    
    @classmethod
    def set_output_entropy_length(cls,value = 0):
        cls.output_entropy_moving_avg_length = value
    
    @classmethod
    def set_output_row_index(cls,value):
        cls.output_row_index = value
    
    @classmethod
    def set_output_type_record(cls,output_type_record):
        cls.output_type_record = output_type_record
 
    @classmethod
    def set_current_schedule(cls,new_schedule):
        cls.current_schedule = new_schedule
        
    @classmethod
    def generate_empty_stream_log(cls,max_gen,output_items):
        if cls.output_entropy:
            cls.stream_log = numpy.zeros([max_gen,output_items],dtype = float)
        
        else:
            cls.stream_log = numpy.zeros([max_gen,output_items],dtype = int)
   
    @classmethod
    def clear_stream_log(cls):
        cls.stream_log.fill(0)
   
    @classmethod
    def check_if_per_schedule(cls):
        if cls.output_type_record == "stream_output_per_schedule":
            return True
        else:
            return False
    
    @classmethod
    def check_if_per_repitition(cls):
        if cls.output_type_record == "stream_output_per_repitition" or \
           cls.output_type_record == "stream_output_per_repitition_2" or \
           cls.output_type_record == "stream_output_per_repitition_3" or \
           cls.output_type_record == "stream_output_per_repitition_4":
            return True
        else:
            return False
            
   
  
###############################################################################
    @classmethod
    def register_setupclass(cls, output_type):
        def decorator(subclass):
            cls.setupclasses[output_type] = subclass
            return subclass
      
        return decorator    
    
    @classmethod
    def setup(cls, output_type, *args, **kargs):
        if output_type not in cls.setupclasses:
            raise ValueError('Bad output type {}'.format(output_type))
      
        return cls.setupclasses[output_type](*args, **kargs)
###############################################################################
    @classmethod
    def register_captureclass(cls, output_type):
        def decorator(subclass):
            cls.captureclasses[output_type] = subclass
            return subclass
      
        return decorator    
    
    @classmethod
    def capture(cls, output_type, *args, **kargs):
        if output_type not in cls.captureclasses:
            raise ValueError('Bad output type {}'.format(output_type))
      
        return cls.captureclasses[output_type](*args, **kargs)

###############################################################################
    @classmethod
    def register_exportclass(cls, output_type):
        def decorator(subclass):
            cls.exportclasses[output_type] = subclass
            return subclass
      
        return decorator    
    
    @classmethod
    def export(cls, output_type, *args, **kargs):
        if output_type not in cls.exportclasses:
            raise ValueError('Bad output type {}'.format(output_type))
      
        return cls.exportclasses[output_type](*args, **kargs)
    
###############################################################################   
# The next 3 sections are for 'stream_output_per_schedule'
###############################################################################

@Output.register_setupclass('stream_output_per_schedule')
class Stream_Setup(Output):
    
# Associated Experiment_Module line:===========================================
# Output_Module.Output.setup(Output_Module.Output.output_type_record,\
#                            primary_targets,experiment_gen_num,\
#                            filename_modifier,total_schedule_num)    
# =============================================================================
    
    def __init__(self):
       pass
   
    def __new__(self,primary_targets, experiment_gen_num, filename_mod, *args, **kargs):
        Stream_Setup.setup(primary_targets, experiment_gen_num, filename_mod, *args, **kargs)
        
    
    def setup(primary_targets, experiment_gen_num, filename_mod,*args, **kargs):
        pass
        #set up primary targets
        #set up output column titles
        #set up output array
        total_counter = 0
        Output.output_column_titles.append("emitted_bx")
        total_counter += 1
        
        Output.primary_target_ids = primary_targets
        Output.Output_filename_modifer = filename_mod
        
        
        counter = 1
        for target in primary_targets:
            Output.output_column_titles.append(f'R{counter}')
            counter += 1
            total_counter += 1
        counter = 1
        for target in primary_targets:
            Output.output_column_titles.append(f'B{counter}')
            counter += 1
            total_counter += 1    
        
        if Output.output_entropy == True:    
            Output.output_column_titles.append('avg_entropy')
            total_counter += 1
            Output.output_column_titles.append('moving_avg_entropy')
            total_counter += 1
            
            Output.entropy_moving_average = collections.deque([0] * Output.output_entropy_moving_avg_length)
            
        Output.generate_empty_stream_log(experiment_gen_num,total_counter)
        



###############################################################################
@Output.register_captureclass('stream_output_per_schedule')
class Stream_Capture(Output):
    
#Associated Experiment_Module Line:============================================
#   Output_Module.Output.capture(Output_Module.Output.output_type_record,\
#                                schedule_set_no, current_gen, emitted_behavior,\
#                                reinforcer_type, hit_target_id)
# =============================================================================
    
    def __init__(self):
       pass
   
    def __new__(self, schedule, generation, emitted_bx,\
                reinforcer_type, hit_target_id,*args, **kargs):
        Stream_Capture.capture(schedule, generation, emitted_bx,\
                       reinforcer_type, hit_target_id,*args, **kargs)
        
    
    def capture(schedule, generation, emitted_bx,\
                reinforcer_type, hit_target_id,*args, **kargs):
        
        
        
        if Output.current_schedule == None:
            Output.set_current_schedule(int(schedule))
            
        elif Output.current_schedule != int(schedule):
            raise ValueError("schedule changed occured without export occuring!")
        
        # print(Output.current_schedule)
        #reinforcers and behaviors must be in list format    
        x_index = generation
        #emitted, R1, R2, B1, B2 
        
        # Output.capture("stream_output",1,2,3,[4,5,6],[7,8])
        # print("schedule = ", schedule) #1
        # print("generation = ", generation) #2
        # print("emitted_bx = ", emitted_bx) #3
        # print("reinforcers = ", reinforcers) #4, 5, 6 
        # print("behaviors = ", behaviors) #7, 8
        #reinforcer_type, hit_target_id
        counter = 0
        reinforcers = []
        behaviors = []
        
        Output.stream_log[x_index].put([counter],[int(emitted_bx)])
        counter += 1 
        
        if hit_target_id is not None:  
            for target in Output.primary_target_ids:
                if hit_target_id == target:
                    behaviors.append(1)
                    if reinforcer_type != None:
                        reinforcers.append(1)
                    else:
                        reinforcers.append(0)
                else:
                    behaviors.append(0)
                    reinforcers.append(0)
                    
                    
        else:
            for target in Output.primary_target_ids:
                behaviors.append(0)
                reinforcers.append(0)

        
        for given in reinforcers:
            Output.stream_log[x_index].put([counter],[given])
            counter += 1
        for hit in behaviors:
            Output.stream_log[x_index].put([counter],[hit])
            counter += 1
        
        if Output.output_entropy == True:
            near_list_entropies = []
            moving_average_ready = False
            # claculate current entropy
            decimal_max = Organism_Module.Organism.decimal_max
            near_list = Stimulus_Element_Holder.se_registry["near"]
            for bx_pop_key in near_list:
                
                try:
                    bx_pop_behaviors = Organism_Module.Organism.Behaviors[bx_pop_key]
                except:
                    continue
                
                pop_entropy = General_Functions_Module.get_entropy(bx_pop_behaviors,decimal_max)
                near_list_entropies.append(pop_entropy)
            current_entropy = numpy.average(near_list_entropies)
            current_entropy = round(current_entropy,3)
            if Output.entropy_setup_counter < Output.output_entropy_moving_avg_length:
                # print(f'entropy_setup_counter = {Output.entropy_setup_counter}')
                # print(f'output_entropy_moving_avg_length = {Output.output_entropy_moving_avg_length}')
                # print('len of list ={len(entropy_moving_average)}')
                current_index = Output.entropy_setup_counter
                Output.entropy_moving_average[current_index] = current_entropy
                Output.entropy_setup_counter += 1
            else:
                #adjust moving adverage
                moving_average_ready = True
                Output.entropy_moving_average.popleft()
                Output.entropy_moving_average.append(current_entropy)
                moving_entropy = numpy.average(Output.entropy_moving_average)
            #add current entropy
            Output.stream_log[x_index].put([counter],current_entropy)
            counter += 1
            #if xindex greater than length, add moving average
            if moving_average_ready:
                Output.stream_log[x_index].put([counter],moving_entropy)
                counter += 1
            else:
                Output.stream_log[x_index].put([counter],0)
                counter += 1
 
###############################################################################

@Output.register_exportclass('stream_output_per_schedule')
class Stream_Export(Output):
    
# Associated Experiment_Module Line:===========================================
#  #export data per schedule, if type is correct
#  if Output_Module.Output.check_if_per_schedule() == True:
#      Output_Module.Output.export(Output_Module.Output.output_type_record,\
#                                  repitition_number,schedule_set_no)    
# =============================================================================
    
    def __init__(self):
       pass
   
    def __new__(self, rep,schedule_set_no,*args, **kargs):
        Stream_Export.export(rep,schedule_set_no,*args, **kargs)
        
    
    def export(rep,schedule_set_no,*args, **kargs):
        collected_headers = ""
        for header in Output.output_column_titles:
            if collected_headers == "":
                collected_headers = f'{header}'
            else:
                collected_headers = f'{collected_headers},{header}'
        
        
        new_schedule = int(schedule_set_no) + 1
        modifier = Output.Output_filename_modifer
        #result.astype(int)
        if Output.output_entropy == True:
            numpy.savetxt(f'outputs/{modifier}rep{rep}sched{schedule_set_no}.csv', \
                          Output.stream_log, fmt='%1.3f',delimiter=",",\
                          comments = "", header = collected_headers) 
            
         
        else:
            numpy.savetxt(f'outputs/{modifier}rep{rep}sched{schedule_set_no}.csv', \
                          Output.stream_log.astype(int), fmt = '%d',delimiter=",",\
                          comments = "", header = collected_headers) 
                    
        Output.set_current_schedule(new_schedule)
        #file based on rep
        #export based on schedule, same file until next rep
        
###############################################################################   
# The next 3 sections are for 'stream_output_per_repitition'
###############################################################################


@Output.register_setupclass('stream_output_per_repitition')
class Stream_Output_Per_Repitition_Setup(Output):
    
# Associated Experiment_Module line:===========================================
# Output_Module.Output.setup(Output_Module.Output.output_type_record,\
#                            primary_targets,experiment_gen_num,\
#                            filename_modifier,total_schedule_num)    
# =============================================================================   
    
    def __init__(self):
       pass
   
    def __new__(self,primary_targets, experiment_gen_num, \
                filename_mod, total_schedule_num, *args, **kargs):
        Stream_Output_Per_Repitition_Setup.setup(primary_targets, experiment_gen_num, \
                        filename_mod, total_schedule_num, *args, **kargs)
        
    
    def setup(primary_targets, experiment_gen_num, filename_mod, \
              total_schedule_num, *args, **kargs):
        pass
        #set up primary targets
        #set up output column titles
        #set up output array
        total_counter = 0
        Output.output_column_titles.append("schedule")
        total_counter += 1
        Output.output_column_titles.append("emitted_bx")
        total_counter += 1
        
        Output.primary_target_ids = primary_targets
        Output.Output_filename_modifer = filename_mod
        
        
        counter = 1
        for target in primary_targets:
            Output.output_column_titles.append(f'R{counter}')
            counter += 1
            total_counter += 1
        counter = 1
        for target in primary_targets:
            Output.output_column_titles.append(f'B{counter}')
            counter += 1
            total_counter += 1
        
        
        
        if Output.output_entropy == True:    
            Output.output_column_titles.append('avg_entropy')
            total_counter += 1
            Output.output_column_titles.append('moving_avg_entropy')
            total_counter += 1
            
            Output.entropy_moving_average = collections.deque([0] * Output.output_entropy_moving_avg_length)
            
        print(f'primary_targets = {primary_targets}')
        print(f'experiment_gen_num type = {experiment_gen_num}')
        print(f'filename_mod = {filename_mod}')
        print(f'total_schedule_num type = {total_schedule_num}')
        
        gen_per_file = experiment_gen_num
        print(f'gen_per_file = {gen_per_file}')
        print(f'gen_per_file type = {type(gen_per_file)}')
        Output.generate_empty_stream_log(gen_per_file,total_counter)
    



###############################################################################
@Output.register_captureclass('stream_output_per_repitition')
class Stream_Output_Per_Repitition_Capture(Output):

#Associated Experiment_Module Line:============================================
#   Output_Module.Output.capture(Output_Module.Output.output_type_record,\
#                                schedule_set_no, current_gen, emitted_behavior,\
#                                reinforcer_type, hit_target_id)
# =============================================================================

    def __init__(self):
       pass
   
    def __new__(self, schedule, generation, emitted_bx,\
                reinforcer_type, hit_target_id,*args, **kargs):
        Stream_Output_Per_Repitition_Capture.capture(schedule, generation, emitted_bx,\
                       reinforcer_type, hit_target_id,*args, **kargs)
        
    
    def capture(schedule, generation, emitted_bx,\
                reinforcer_type, hit_target_id,*args, **kargs):
        
        Output.set_current_schedule(int(schedule))
        
        if int(schedule) == 1 and generation == 0:
            Output.set_output_row_index(0)
        
        # print(Output.current_schedule)
        #reinforcers and behaviors must be in list format    
        
        
        #scheduled,emitted, R1, R2, B1, B2 
        x_index = Output.get_output_row_index()
        # print(f'x_index ={x_index}')
        # Output.capture("stream_output",1,2,3,[4,5,6],[7,8])
        # print("schedule = ", schedule) #1
        # print("generation = ", generation) #2
        # print("emitted_bx = ", emitted_bx) #3
        # print("reinforcers = ", reinforcers) #4, 5, 6 
        # print("behaviors = ", behaviors) #7, 8
        #reinforcer_type, hit_target_id
        counter = 0
        reinforcers = []
        behaviors = []
        
        Output.stream_log[x_index].put([counter],[int(schedule)])
        counter += 1 
        Output.stream_log[x_index].put([counter],[int(emitted_bx)])
        counter += 1 
        
        if hit_target_id is not None:  
            for target in Output.primary_target_ids:
                if hit_target_id == target:
                    behaviors.append(1)
                    if reinforcer_type != None:
                        reinforcers.append(1)
                    else:
                        reinforcers.append(0)
                else:
                    behaviors.append(0)
                    reinforcers.append(0)
                    
                    
        else:
            for target in Output.primary_target_ids:
                behaviors.append(0)
                reinforcers.append(0)

        
        for given in reinforcers:
            Output.stream_log[x_index].put([counter],[given])
            counter += 1
        for hit in behaviors:
            Output.stream_log[x_index].put([counter],[hit])
            counter += 1
        
        if Output.output_entropy == True:
            near_list_entropies = []
            moving_average_ready = False
            # claculate current entropy
            decimal_max = Organism_Module.Organism.decimal_max
            near_list = Stimulus_Element_Holder.se_registry["near"]
            for bx_pop_key in near_list:
                
                try:
                    bx_pop_behaviors = Organism_Module.Organism.Behaviors[bx_pop_key]
                except:
                    continue
                
                pop_entropy = General_Functions_Module.get_entropy(bx_pop_behaviors,decimal_max)
                near_list_entropies.append(pop_entropy)
            current_entropy = numpy.average(near_list_entropies)
            current_entropy = round(current_entropy,3)
            if Output.entropy_setup_counter < Output.output_entropy_moving_avg_length:
                # print(f'entropy_setup_counter = {Output.entropy_setup_counter}')
                # print(f'output_entropy_moving_avg_length = {Output.output_entropy_moving_avg_length}')
                # print('len of list ={len(entropy_moving_average)}')
                current_index = Output.entropy_setup_counter
                Output.entropy_moving_average[current_index] = current_entropy
                Output.entropy_setup_counter += 1
            else:
                #adjust moving adverage
                moving_average_ready = True
                Output.entropy_moving_average.popleft()
                Output.entropy_moving_average.append(current_entropy)
                moving_entropy = numpy.average(Output.entropy_moving_average)
            #add current entropy
            Output.stream_log[x_index].put([counter],current_entropy)
            counter += 1
            #if xindex greater than length, add moving average
            if moving_average_ready:
                Output.stream_log[x_index].put([counter],moving_entropy)
                counter += 1
            else:
                Output.stream_log[x_index].put([counter],0)
                counter += 1
            
       
        # print(f'stream_log[{x_index}] = {Output.stream_log[x_index]}')
        Output.increment_x_index()
###############################################################################

@Output.register_exportclass('stream_output_per_repitition')
class Stream_Output_Per_Repitition_Export(Output):
    
# Associated Experiment_Module Line:===========================================
# #export data per repitition, if type is correct
# if Output_Module.Output.check_if_per_repitition() == True:
#     Output_Module.Output.export(Output_Module.Output.output_type_record,\
#                                 repitition_number,schedule_set_no)    
# =============================================================================
    
    def __init__(self):
       pass
   
    def __new__(self, rep,schedule_set_no,*args, **kargs):
        Stream_Output_Per_Repitition_Export.export(rep,schedule_set_no,*args, **kargs)
        
    
    def export(rep,schedule_set_no,*args, **kargs):
        collected_headers = ""
        for header in Output.output_column_titles:
            if collected_headers == "":
                collected_headers = f'{header}'
            else:
                collected_headers = f'{collected_headers},{header}'
        
        
        
        modifier = Output.Output_filename_modifer
        #result.astype(int)
        if Output.output_entropy == True:
            numpy.savetxt(f'outputs/{modifier}rep{rep}_allschedules.csv', \
                          Output.stream_log,fmt='%1.3f', delimiter=",",\
                          comments = "", header = collected_headers) 
            
         
        else:
            numpy.savetxt(f'outputs/{modifier}rep{rep}_allschedules.csv', \
                          Output.stream_log.astype(int), fmt = '%d',delimiter=",",\
                          comments = "", header = collected_headers) 
                    
        Output.clear_stream_log()
        
        #file based on rep
        #export based on schedule, same file until next rep       
        
###############################################################################   
# The next 3 sections are for 'stream_output_per_repitition_2'
###############################################################################


@Output.register_setupclass('stream_output_per_repitition_2')
class Stream_Output_Per_Repitition_2_Setup(Output):
    
# Associated Experiment_Module line:===========================================
# Output_Module.Output.setup(Output_Module.Output.output_type_record,\
#                            primary_targets,experiment_gen_num,\
#                            filename_modifier,total_schedule_num)    
# =============================================================================   
    
    def __init__(self):
       pass
   
    def __new__(self, *args, **kargs):
        Stream_Output_Per_Repitition_2_Setup.setup(*args, **kargs)
        
    
    def setup(*args, **kargs):
        pass
        #set up primary targets
        #set up output column titles
        #set up output array
        total_counter = 0
        Output.output_column_titles.append("schedule")
        total_counter += 1
        Output.output_column_titles.append("emitted_bx")
        total_counter += 1
        Output.output_column_titles.append("emitted_se")
        total_counter += 1
        Output.output_column_titles.append("num_se_obs")
        total_counter += 1
        Output.primary_target_ids = Exp_Data.primary_targets
        Output.Output_filename_modifer = Exp_Data.filename_modifier
        
        
        counter = 1
        for target in Exp_Data.primary_targets:
            Output.output_column_titles.append(f'R{counter}')
            counter += 1
            total_counter += 1
        counter = 1
        for target in Exp_Data.primary_targets:
            Output.output_column_titles.append(f'B{counter}')
            counter += 1
            total_counter += 1
        
        if Output.output_background == True:

            counter = 1
            for target in Exp_Data.background_targets:
                Output.output_column_titles.append(f'BK-R{counter}')
                counter += 1
                total_counter += 1    
            
            counter = 1
            for target in Exp_Data.background_targets:
                Output.output_column_titles.append(f'BK-B{counter}')
                counter += 1
                total_counter += 1    
            
            
        if Output.output_entropy == True:    
            
            Output.output_column_titles.append('obs_SE_entropy')
            total_counter += 1
            
            Output.output_column_titles.append('emitted_SE_entropy')
            total_counter += 1
          
            Output.output_column_titles.append('moving_avg_obs_SE_entropy')
            total_counter += 1
            
            Output.entropy_moving_average = collections.deque([0] * Output.output_entropy_moving_avg_length)
            
        print(f'primary_targets = {Exp_Data.primary_targets}')
        print(f'background_targets = {Exp_Data.background_targets}')
        print(f'experiment_gen_num type = {Exp_Data.experiment_gen_num}')
        print(f'filename_mod = {Exp_Data.filename_modifier}')
        print(f'total_schedule_num type = {Exp_Data.total_schedule_num}')
        
        gen_per_file = Exp_Data.experiment_gen_num
        print(f'gen_per_file = {gen_per_file}')
        # print(f'gen_per_file type = {type(gen_per_file)}')
        Output.generate_empty_stream_log(gen_per_file,total_counter)
    



###############################################################################
@Output.register_captureclass('stream_output_per_repitition_2')
class Stream_Output_Per_Repitition_2_Capture(Output):

#Associated Experiment_Module Line:============================================
#   Output_Module.Output.capture(Output_Module.Output.output_type_record,\
#                                schedule_set_no, current_gen, emitted_behavior,\
#                                reinforcer_type, hit_target_id)
# =============================================================================

    def __init__(self):
       pass
   
    def __new__(self,*args, **kargs):
        Stream_Output_Per_Repitition_2_Capture.capture(*args, **kargs)
        
    
    def capture(*args, **kargs):
        first_schedule_check = Exp_Data.first_schedule_check
        schedule = Exp_Data.schedule_set_no
        generation = Exp_Data.current_gen
        emitted_bx = Exp_Data.emitted_behavior
        reinforcer_type = Exp_Data.reinforcer_type
        hit_target_id = Exp_Data.hit_target_id
        background_target_ids = Exp_Data.background_targets
        
        Output.set_current_schedule(int(schedule))
        
        if first_schedule_check == True and generation == 0:
            Output.set_output_row_index(0)
        
        # print(Output.current_schedule)
        #reinforcers and behaviors must be in list format    
        
        
        #scheduled,emitted, R1, R2, B1, B2 
        x_index = Output.get_output_row_index()
        # print(f'x_index ={x_index}')
        # Output.capture("stream_output",1,2,3,[4,5,6],[7,8])
        # print("schedule = ", schedule) #1
        # print("generation = ", generation) #2
        # print("emitted_bx = ", emitted_bx) #3
        # print("reinforcers = ", reinforcers) #4, 5, 6 
        # print("behaviors = ", behaviors) #7, 8
        #reinforcer_type, hit_target_id
        counter = 0
        reinforcers = []
        behaviors = []
        
        Output.stream_log[x_index].put([counter],[int(schedule)])
        counter += 1 
        Output.stream_log[x_index].put([counter],[int(emitted_bx)])
        counter += 1 
        # print(f'SE NUM type = {type(Stimulus_Element_Holder.se_num_dic)}')
        # print(f'ED NUM type = {type(Exp_Data.chosen_bx_pop_se)}')
        se_string = numpy.array2string(Exp_Data.chosen_bx_pop_se)
        se_string = se_string[2:len(se_string)-2]
        se_num = Stimulus_Element_Holder.se_num_dic[se_string]
        Output.stream_log[x_index].put([counter],[int(se_num)])
        counter += 1 
        Output.stream_log[x_index].put([counter],[int(Exp_Data.observed_se_num)])
        counter += 1 
        
        if hit_target_id is not None:  
                      
            for target in Output.primary_target_ids:
                if hit_target_id == target:
                    behaviors.append(1)
                    if reinforcer_type != None:
                        reinforcers.append(1)
                    else:
                        reinforcers.append(0)
                else:
                    behaviors.append(0)
                    reinforcers.append(0)   
        else:
            for target in Output.primary_target_ids:
                behaviors.append(0)
                reinforcers.append(0)
        
        for given in reinforcers:
            Output.stream_log[x_index].put([counter],[given])
            counter += 1
        for hit in behaviors:
            Output.stream_log[x_index].put([counter],[hit])
            counter += 1
        
        if Output.output_background == True:
            
            bk_reinforcers = []
            bk_behaviors = []
            
            if hit_target_id is not None:  
                for bk_target in background_target_ids:
                    if hit_target_id == bk_target:
                        bk_behaviors.append(1)
                        if reinforcer_type != None:
                            bk_reinforcers.append(1)
                        else:
                            bk_reinforcers.append(0)
                    else:
                        bk_behaviors.append(0)
                        bk_reinforcers.append(0)   
            else:
                for bk_target in background_target_ids:
                    bk_behaviors.append(0)
                    bk_reinforcers.append(0)
            
            for bk_given in bk_reinforcers:
                Output.stream_log[x_index].put([counter],[bk_given])
                counter += 1
            for bk_hit in bk_behaviors:
                Output.stream_log[x_index].put([counter],[bk_hit])
                counter += 1    
        
        if Output.output_entropy == True:
            obs_se_entropies = []
            moving_average_ready = False
            # claculate current entropy
            decimal_max = Organism_Module.Organism.decimal_max
            obs_se_list = Exp_Data.viewed_se
            for bx_pop_key in obs_se_list:
                
                try:
                    bx_pop_behaviors = Organism_Module.Organism.Behaviors[bx_pop_key]
                except:
                    continue
                
                pop_entropy = General_Functions_Module.get_entropy(bx_pop_behaviors,decimal_max)
                obs_se_entropies.append(pop_entropy)
                if bx_pop_key == Exp_Data.chosen_bx_pop_se:
                    emitted_se_entropy = pop_entropy
            obs_se_entropy = numpy.average(obs_se_entropies)
            obs_se_entropy = round(obs_se_entropy,3)
            if Output.entropy_setup_counter < Output.output_entropy_moving_avg_length:
                # print(f'entropy_setup_counter = {Output.entropy_setup_counter}')
                # print(f'output_entropy_moving_avg_length = {Output.output_entropy_moving_avg_length}')
                # print('len of list ={len(entropy_moving_average)}')
                current_index = Output.entropy_setup_counter
                Output.entropy_moving_average[current_index] = obs_se_entropy
                Output.entropy_setup_counter += 1
            else:
                #adjust moving adverage
                moving_average_ready = True
                Output.entropy_moving_average.popleft()
                Output.entropy_moving_average.append(obs_se_entropy)
                obs_se_moving_entropy = numpy.average(Output.entropy_moving_average)
                
            #add obs_se_entropy entropy
            Output.stream_log[x_index].put([counter],obs_se_entropy)
            counter += 1
            
            #add emitted_se_entropy entropy
            Output.stream_log[x_index].put([counter],emitted_se_entropy)
            counter += 1
            
            #if xindex greater than length, add moving average
            if moving_average_ready:
                Output.stream_log[x_index].put([counter],obs_se_moving_entropy)
                counter += 1
            else:
                Output.stream_log[x_index].put([counter],0)
                counter += 1
            
       
        # print(f'stream_log[{x_index}] = {Output.stream_log[x_index]}')
        Output.increment_x_index()
###############################################################################

@Output.register_exportclass('stream_output_per_repitition_2')
class Stream_Output_Per_Repitition_2_Export(Output):
    
# Associated Experiment_Module Line:===========================================
# #export data per repitition, if type is correct
# if Output_Module.Output.check_if_per_repitition() == True:
#     Output_Module.Output.export(Output_Module.Output.output_type_record,\
#                                 repitition_number,schedule_set_no)    
# =============================================================================
    
    def __init__(self):
       pass
   
    def __new__(self,*args, **kargs):
        Stream_Output_Per_Repitition_2_Export.export(*args, **kargs)
        
    
    def export(*args, **kargs):
        rep = Exp_Data.repitition_number
        # print(f'export rep = {rep}')
        collected_headers = ""
        for header in Output.output_column_titles:
            if collected_headers == "":
                collected_headers = f'{header}'
            else:
                collected_headers = f'{collected_headers},{header}'
        
        
        
        modifier = Output.Output_filename_modifer
        #result.astype(int)
        if Output.output_entropy == True:
            numpy.savetxt(f'outputs/{modifier}rep{rep}_allschedules.csv', \
                          Output.stream_log,fmt='%1.3f', delimiter=",",\
                          comments = "", header = collected_headers) 
            
         
        else:
            numpy.savetxt(f'outputs/{modifier}rep{rep}_allschedules.csv', \
                          Output.stream_log.astype(int), fmt = '%d',delimiter=",",\
                          comments = "", header = collected_headers) 
                    
        Output.clear_stream_log()
        
        #file based on rep
        #export based on schedule, same file until next rep       

###############################################################################   
# The next 3 sections are for 'stream_output_per_repitition_3'
###############################################################################


@Output.register_setupclass('stream_output_per_repitition_3')
class Stream_Output_Per_Repitition_3_Setup(Output):
    
# Associated Experiment_Module line:===========================================
# Output_Module.Output.setup(Output_Module.Output.output_type_record,\
#                            primary_targets,experiment_gen_num,\
#                            filename_modifier,total_schedule_num)    
# =============================================================================   

#list for capture: schedule, emitted_bx, emitted_se, num_se_obs, 
#                  primary_targets, bkgd_targets, emitted_SE_entropy,
#                  SE_mod_length, Selection_modifier,
    
    def __init__(self):
       pass
   
    def __new__(self, *args, **kargs):
        Stream_Output_Per_Repitition_3_Setup.setup(*args, **kargs)
        
    
    def setup(*args, **kargs):
        
        #set up primary targets
        #set up output column titles
        #set up output array
        total_counter = 0
        Output.output_column_titles.append("schedule")
        total_counter += 1
        Output.output_column_titles.append("emitted_bx")
        total_counter += 1
        Output.output_column_titles.append("emitted_se")
        total_counter += 1
        Output.output_column_titles.append("num_se_obs")
        total_counter += 1
        Output.primary_target_ids = Exp_Data.primary_targets
        Output.Output_filename_modifer = Exp_Data.filename_modifier
        
        
        counter = 1
        for target in Exp_Data.primary_targets:
            Output.output_column_titles.append(f'R{counter}')
            counter += 1
            total_counter += 1
        counter = 1
        for target in Exp_Data.primary_targets:
            Output.output_column_titles.append(f'B{counter}')
            counter += 1
            total_counter += 1
        
        if Output.output_background == True:

            counter = 1
            for target in Exp_Data.background_targets:
                Output.output_column_titles.append(f'BK-R{counter}')
                counter += 1
                total_counter += 1    
            
            counter = 1
            for target in Exp_Data.background_targets:
                Output.output_column_titles.append(f'BK-B{counter}')
                counter += 1
                total_counter += 1    
            
            
        if Output.output_entropy == True:    
            
            # Output.output_column_titles.append('obs_SE_entropy')
            # total_counter += 1
            
            Output.output_column_titles.append('emitted_SE_entropy')
            total_counter += 1
          
            # Output.output_column_titles.append('moving_avg_obs_SE_entropy')
            # total_counter += 1
            #                  SE_mod_length, Selection_modifier,
        
        if Output.output_selection_modifier == True:
            
            #selection modifier window length
            Output.output_column_titles.append('SE_win_len')
            total_counter += 1
            
            #slection modifier window length goal
            Output.output_column_titles.append('SE_win_goal')
            total_counter += 1
            
            #RC difference
            Output.output_column_titles.append('rc_diff')
            total_counter += 1
            
            #selction modifier
            Output.output_column_titles.append('Sel_mod')
            total_counter += 1
         
        
            # Output.entropy_moving_average = collections.deque([0] * Output.output_entropy_moving_avg_length)
        
        if Output.output_emitted_behavior_population == True: 
            pop_size = Organism_Module.Organism.bx_pop_size
            for bx_value in range(1,pop_size+1):
                bx_title = "bx" + str(bx_value)
                Output.output_column_titles.append(bx_title)
                total_counter += 1
            
            
        print(f'primary_targets = {Exp_Data.primary_targets}')
        print(f'background_targets = {Exp_Data.background_targets}')
        print(f'experiment_gen_num type = {Exp_Data.experiment_gen_num}')
        print(f'filename_mod = {Exp_Data.filename_modifier}')
        print(f'total_schedule_num type = {Exp_Data.total_schedule_num}')
        
        gen_per_file = Exp_Data.experiment_gen_num
        print(f'gen_per_file = {gen_per_file}')
        # print(f'gen_per_file type = {type(gen_per_file)}')
        Output.generate_empty_stream_log(gen_per_file,total_counter)
    



###############################################################################
@Output.register_captureclass('stream_output_per_repitition_3')
class Stream_Output_Per_Repitition_3_Capture(Output):

#Associated Experiment_Module Line:============================================
#   Output_Module.Output.capture(Output_Module.Output.output_type_record,\
#                                schedule_set_no, current_gen, emitted_behavior,\
#                                reinforcer_type, hit_target_id)
# =============================================================================



    def __init__(self):
       pass
   
    def __new__(self,*args, **kargs):
        Stream_Output_Per_Repitition_3_Capture.capture(*args, **kargs)
        
    
    def capture(*args, **kargs):
        first_schedule_check = Exp_Data.first_schedule_check
        schedule = Exp_Data.schedule_set_no
        generation = Exp_Data.current_gen
        emitted_bx = Exp_Data.emitted_behavior
        reinforcer_type = Exp_Data.reinforcer_type
        hit_target_id = Exp_Data.hit_target_id
        background_target_ids = Exp_Data.background_targets
        se_string = numpy.array2string(Exp_Data.chosen_bx_pop_se)
        se_string = se_string[2:len(se_string)-2]
        current_selection_modifier = Exp_Data.selection_modifier_dict.get(se_string)
        current_rc_stream_length = Exp_Data.rc_stream_length_dict.get(se_string)
        current_rc_stream_goal = Exp_Data.rc_stream_length_goal_dict.get(se_string)
        current_rc_diff = Exp_Data.rc_current_diff.get(se_string)
        child_bx_pop = Organism_Module.Organism.Behaviors[se_string]
        
        Output.set_current_schedule(int(schedule))
        
        if first_schedule_check == True and generation == 0:
            Output.set_output_row_index(0)
        
        # print(Output.current_schedule)
        #reinforcers and behaviors must be in list format    
        
        
        #scheduled,emitted, R1, R2, B1, B2 
        x_index = Output.get_output_row_index()
        # print(f'x_index ={x_index}')
        # Output.capture("stream_output",1,2,3,[4,5,6],[7,8])
        # print("schedule = ", schedule) #1
        # print("generation = ", generation) #2
        # print("emitted_bx = ", emitted_bx) #3
        # print("reinforcers = ", reinforcers) #4, 5, 6 
        # print("behaviors = ", behaviors) #7, 8
        #reinforcer_type, hit_target_id
        counter = 0
        reinforcers = []
        behaviors = []
        
        Output.stream_log[x_index].put([counter],[int(schedule)])
        counter += 1 
        Output.stream_log[x_index].put([counter],[int(emitted_bx)])
        counter += 1 
        # print(f'SE NUM type = {type(Stimulus_Element_Holder.se_num_dic)}')
        # print(f'ED NUM type = {type(Exp_Data.chosen_bx_pop_se)}')

        se_num = Stimulus_Element_Holder.se_num_dic[se_string]
        Output.stream_log[x_index].put([counter],[int(se_num)])
        counter += 1 
        Output.stream_log[x_index].put([counter],[int(Exp_Data.observed_se_num)])
        counter += 1 
        
        if hit_target_id is not None:  
                      
            for target in Output.primary_target_ids:
                if hit_target_id == target:
                    behaviors.append(1)
                    if reinforcer_type != None:
                        reinforcers.append(1)
                    else:
                        reinforcers.append(0)
                else:
                    behaviors.append(0)
                    reinforcers.append(0)   
        else:
            for target in Output.primary_target_ids:
                behaviors.append(0)
                reinforcers.append(0)
        
        for given in reinforcers:
            Output.stream_log[x_index].put([counter],[given])
            counter += 1
        for hit in behaviors:
            Output.stream_log[x_index].put([counter],[hit])
            counter += 1
        
        if Output.output_background == True:
            
            bk_reinforcers = []
            bk_behaviors = []
            
            if hit_target_id is not None:  
                for bk_target in background_target_ids:
                    if hit_target_id == bk_target:
                        bk_behaviors.append(1)
                        if reinforcer_type != None:
                            bk_reinforcers.append(1)
                        else:
                            bk_reinforcers.append(0)
                    else:
                        bk_behaviors.append(0)
                        bk_reinforcers.append(0)   
            else:
                for bk_target in background_target_ids:
                    bk_behaviors.append(0)
                    bk_reinforcers.append(0)
            
            for bk_given in bk_reinforcers:
                Output.stream_log[x_index].put([counter],[bk_given])
                counter += 1
            for bk_hit in bk_behaviors:
                Output.stream_log[x_index].put([counter],[bk_hit])
                counter += 1    
        
        if Output.output_entropy == True:
            # obs_se_entropies = []
            # moving_average_ready = False
            # claculate current entropy
            decimal_max = Organism_Module.Organism.decimal_max
            obs_se_list = Exp_Data.viewed_se
            for bx_pop_key in obs_se_list:
                
                try:
                    bx_pop_behaviors = Organism_Module.Organism.Behaviors[bx_pop_key]
                except:
                    continue
                
                pop_entropy = General_Functions_Module.get_entropy(bx_pop_behaviors,decimal_max)
                # obs_se_entropies.append(pop_entropy)
                if bx_pop_key == Exp_Data.chosen_bx_pop_se:
                    emitted_se_entropy = pop_entropy
            # obs_se_entropy = numpy.average(obs_se_entropies)
            # obs_se_entropy = round(obs_se_entropy,3)
            # if Output.entropy_setup_counter < Output.output_entropy_moving_avg_length:
            #     # print(f'entropy_setup_counter = {Output.entropy_setup_counter}')
            #     # print(f'output_entropy_moving_avg_length = {Output.output_entropy_moving_avg_length}')
            #     # print('len of list ={len(entropy_moving_average)}')
            #     current_index = Output.entropy_setup_counter
            #     Output.entropy_moving_average[current_index] = obs_se_entropy
            #     Output.entropy_setup_counter += 1
            # else:
            #     #adjust moving adverage
            #     moving_average_ready = True
            #     Output.entropy_moving_average.popleft()
            #     Output.entropy_moving_average.append(obs_se_entropy)
            #     obs_se_moving_entropy = numpy.average(Output.entropy_moving_average)
                
            # #add obs_se_entropy entropy
            # Output.stream_log[x_index].put([counter],obs_se_entropy)
            # counter += 1
            
            #add emitted_se_entropy entropy
            Output.stream_log[x_index].put([counter],emitted_se_entropy)
            counter += 1
            
            # #if xindex greater than length, add moving average
            # if moving_average_ready:
            #     Output.stream_log[x_index].put([counter],obs_se_moving_entropy)
            #     counter += 1
            # else:
            #     Output.stream_log[x_index].put([counter],0)
            #     counter += 1
        if Output.output_selection_modifier == True:
            
            Output.stream_log[x_index].put([counter],current_rc_stream_length)
            counter += 1
            
            Output.stream_log[x_index].put([counter],current_rc_stream_goal)
            counter += 1
            
            Output.stream_log[x_index].put([counter],current_rc_diff)
            counter += 1
            
            
            Output.stream_log[x_index].put([counter],current_selection_modifier)
            counter += 1
 
        if Output.output_emitted_behavior_population == True: 
            for bx in child_bx_pop:
                Output.stream_log[x_index].put([counter],bx)
                counter += 1
 
    
        # print(f'stream_log[{x_index}] = {Output.stream_log[x_index]}')
        Output.increment_x_index()
###############################################################################

@Output.register_exportclass('stream_output_per_repitition_3')
class Stream_Output_Per_Repitition_3_Export(Output):
    
# Associated Experiment_Module Line:===========================================
# #export data per repitition, if type is correct
# if Output_Module.Output.check_if_per_repitition() == True:
#     Output_Module.Output.export(Output_Module.Output.output_type_record,\
#                                 repitition_number,schedule_set_no)    
# =============================================================================
    
    def __init__(self):
       pass
   
    def __new__(self,*args, **kargs):
        Stream_Output_Per_Repitition_3_Export.export(*args, **kargs)
        
    
    def export(*args, **kargs):
        rep = Exp_Data.repitition_number
        # print(f'export rep = {rep}')
        collected_headers = ""
        for header in Output.output_column_titles:
            if collected_headers == "":
                collected_headers = f'{header}'
            else:
                collected_headers = f'{collected_headers},{header}'
        
        print('inside output module export')
        
        modifier = Output.Output_filename_modifer
        #result.astype(int)
        if Output.output_entropy == True:
            numpy.savetxt(f'outputs/{modifier}rep{rep}_allschedules.csv', \
                          Output.stream_log,fmt='%1.3f', delimiter=",",\
                          comments = "", header = collected_headers) 
            
         
        else:
            numpy.savetxt(f'outputs/{modifier}rep{rep}_allschedules.csv', \
                          Output.stream_log.astype(int), fmt = '%d',delimiter=",",\
                          comments = "", header = collected_headers) 
                    
        Output.clear_stream_log()
        
        #file based on rep
        #export based on schedule, same file until next rep       