# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 09:04:43 2022

@author: Cyrus

Experiment Runner Class
-loading parameters
-check loaded parameters (optional)
-repition loop    
    -generate environment
    -environment shuffler
    -run procedure
    -output data
    -reset environment 
-end experiment

"""
#multi
from multiprocessing import Pool, freeze_support, cpu_count,Process,current_process
from os import getpid
#multi/end

import time
import Parameter_Module
import Organism_Module
import General_Functions_Module
import Output_Module
import numpy
from SE_Modifier_Module import Stimulus_ETBD_Modifier
from Data_Module import Exp_Data
from SE_Module import Stimulus_Element_Holder
from RI_Module import Ri_Schedule
from RR_Module import Rr_Schedule
from FI_Module import Fi_Schedule
from FR_Module import Fr_Schedule

class Experiment_Runner:
    
    test_attribute =3
    #initialize
    def __init__(self, setting_files):
        temp_data=None
        for paths in setting_files:
            # print(setting_files)
            temp_data = Parameter_Module.load_settings(setting_files)
        self.all_parameters = Parameter_Module.parameter_holder(temp_data)
        
        #record loaded settings into console output
        # print(Parameter_Module.parameter_holder.all_parameters)
        # print(repr(Parameter_Module.parameter_holder.all_parameters))
        
        # print(self.all_parameters)
        # print(list(self.all_parameters.get_dict_keys()))
        # print(type(self.all_parameters.get_repititions()))
        #######################################
        #set Organism class variables
        organism_settings = self.all_parameters.get_organism_settings()
        Organism_Module.Organism.set_population_size(organism_settings["population_size"])
        Organism_Module.Organism.set_reinforcer_magnitude(organism_settings["reinforcer_magnitude_data"])
        Organism_Module.Organism.set_number_of_binary_digits(organism_settings["number_of_binary_digits"])
        Organism_Module.Organism.set_percent_replace(organism_settings["percent_replace"])
        Organism_Module.Organism.set_mutation_rate(organism_settings["mutation_rate"])
        
        procedure_settings = self.all_parameters.get_procedure_settings()
        Organism_Module.Organism.set_linear_cutoff_value(procedure_settings["linear_selection_min_behaviors"])
        Exp_Data.procedure_settings = procedure_settings

        ######################################
                
        #setup output variables
        Exp_Data.filename_modifier = self.all_parameters.get_filename_modifier()
        # print("filename_modifier "+filename_modifier)
        Exp_Data.primary_targets = self.all_parameters.get_primary_target_ids()
        Exp_Data.background_targets = self.all_parameters.get_background_target_ids()
        Exp_Data.default_gen_num = self.all_parameters.get_default_generation_num()
        Exp_Data.experiment_gen_num = self.all_parameters.get_experiment_generation_num()
        Exp_Data.total_schedule_num = self.all_parameters.get_total_schedule_num()
        
        
        Output_Module.Output.set_output_emitted_behavior_population(self.all_parameters.get_output_emitted_behavior_population())
        Output_Module.Output.set_output_type_record(self.all_parameters.get_output_type())
        Output_Module.Output.set_output_entropy(self.all_parameters.get_output_entropy())
        Output_Module.Output.set_output_entropy_length(self.all_parameters.get_output_entropy_length())
        Output_Module.Output.set_output_background(self.all_parameters.get_output_background())
        Output_Module.Output.set_output_selection_modifier(self.all_parameters.get_output_selection_modifier())
        Output_Module.Output.setup(Output_Module.Output.output_type_record,\
                                   Exp_Data.primary_targets,Exp_Data.default_gen_num,\
                                   Exp_Data.filename_modifier,Exp_Data.total_schedule_num)
        #######################################################################
        
        #set up modifier items
        #from primary targets, identify target and varied
        Exp_Data.reward_context_switch = self.all_parameters.get_reinforcement_context_active()
        [Exp_Data.target_target_id,Exp_Data.varied_target_id] = self.all_parameters.\
                                              get_target_varied_ids\
                                              (Exp_Data.reward_context_switch,Exp_Data.primary_targets)
        Exp_Data.user_modifier = self.all_parameters.get_user_modifier()
        Exp_Data.capture_length = self.all_parameters.get_reinforcement_capture_length()
        Organism_Module.Organism.set_reinforcement_context_info\
                                 (Exp_Data.reward_context_switch, Exp_Data.target_target_id, \
                                  Exp_Data.varied_target_id, Exp_Data.user_modifier,Exp_Data.capture_length)

        #######################################################################
                                     
        
        self.repitition_loop(self.all_parameters.get_repititions())
        
    #loading parameters
    # def get_parameter_keys(self):
    #     return (list(self.all_parameters.get_dict_keys()))
    
    def repitition_loop(self,repititions = None):
        try:
            if repititions == None:
                raise Exception
        except Exception:
            print('no repititions listed!')
       
 
       
        
        
        #run phase
# Multi Threading--------------------------------------------------------------       
        #multi
        # all_args = [(self.all_parameters.get_total_schedule_num(), repitition_set) for repitition_set in range(0,repititions)]
        # # call freeze_support() if in Windows
        # # if os.name == "nt":
        # #     freeze_support()

        # # you can use whatever, but your machine core count is usually a good choice (although maybe not the best)
        # pool = Pool(30)
        # print("cpu_count"+str(30)) 
        # # pool = Pool(cpu_count()-1)
        # # print("cpu_count"+str(cpu_count()-1)) 
       
        # pool.map(self.wrapped_some_function_call, all_args)
       

       
       #multi/end
# ----------------------------------------------------------------------------- 
       
# ==for windows================================================================

        repitition_number = 0
        for repitition_set in range(0,repititions):
            repitition_number += 1
            print("Repitition number ", repitition_number)

            self.experiment_loop(self.all_parameters.get_total_schedule_num(),repitition_set)            

  
# =============================================================================
        print("end of program")

    def wrapped_some_function_call(self,args): 
        """
        we need to wrap the call to unpack the parameters 
        we build before as a tuple for being able to use pool.map
        this wrapping is for running on Linux
        """ 
        self.experiment_loop(*args) 


    def experiment_loop(self,num_schedules,repitition_number):
        
        print(current_process())
        print("I'm process", getpid())
        print("repitition_number: "+str(repitition_number))
        seed_prompt = (getpid() * int(time.time())) % 123456789
        numpy.random.seed(seed_prompt)
        print(f'numpy seed prompt = {seed_prompt}')
        
        # Set up phase


        #resets    
                # reset Bx pop
                # reset SE Environment
        Organism_Module.Organism.reset_behavior_pop()
        Organism_Module.Organism.reset_reward_counter()

        Stimulus_Element_Holder.clear_registry()
        Output_Module.Output.reset_entropy_setup_counter()
        
        #load/clear out old data - SE_ETBD modifier data
        selection_modifier_type = Exp_Data.procedure_settings.get("selection_modifier_type")
        Stimulus_ETBD_Modifier.calculate(selection_modifier_type,"load_parameters")
        
        mutation_type = Exp_Data.procedure_settings.get("mutation_type")
        Organism_Module.Mutation.mutate(mutation_type, 'load_parameters')
        
        # Generate SE environment
        Stimulus_Element_Holder.load_stimulus_environment(self.all_parameters.get_stimulus_environment_settings())
        # print(f'Se Num_dict = {Stimulus_Element_Holder.se_num_dic}')
        # print(f'Se Num_dict type = {type(Stimulus_Element_Holder.se_num_dic)}')
        print("SE near items = ",Stimulus_Element_Holder.get_se_registry()["near"])
        print("SE far items = ",Stimulus_Element_Holder.get_se_registry()["far"])
        
        #needed for serial code (not multi-processing)
        Exp_Data.clear_target_value_dictionary()
        
        Exp_Data.repitition_number = repitition_number
        Output_Module.Output.set_current_schedule(None)
        schedule_settings = self.all_parameters.get_experiment_schedule_settings()
        population_reset_switch = self.all_parameters.get_population_reset_between_schedules()
        schedule_randomization = self.all_parameters.check_schedule_order_randomization()
        default_gen_per_schedule = self.all_parameters.get_default_generation_num()
        if schedule_randomization == True:
            schedule_randomization_cutoff = self.all_parameters.get_schedule_order_randomization_cutoff()
        else:
            schedule_randomization_cutoff = False
        #set up targets
        #set up targets in the Data Module

        if Exp_Data.time_check == True: 
            target_time_start = time.time()
        
        target_settings = self.all_parameters.get_target_info()
        General_Functions_Module.set_up_targets(target_settings)

        if Exp_Data.time_check == True: 
            target_time_end = time.time() 
            print("Target time is {} seconds".format(target_time_end - target_time_start))

        #set up stimulus environment shifting rules
        Exp_Data.se_shift_setup(self.all_parameters.get_se_shift_rules_dict())
            
        #resets
            #reset SE environment
            #reset reinforcement Schedules
        Ri_Schedule.clear_ri_registry()
        Rr_Schedule.clear_rr_registry()
        Fi_Schedule.clear_fi_registry()
        Fr_Schedule.clear_fr_registry()
                #reset Bx pop
        print(f'population_reset_settings = {population_reset_switch}')
        print(f'reward_context_on = {Organism_Module.Organism.reward_context_on}')
        
        #notify program that this is a first schedule in a repitition
        # print(f' first schedule = {Exp_Data.first_schedule_check}')
        Exp_Data.first_schedule_check = True
        # print(f' first schedule = {Exp_Data.first_schedule_check}')       
        #set up schedules
        #find schedules that are done in order
        #find schedules that need to be randomized.
        schedule_list = General_Functions_Module.generate_schedule_order(schedule_settings,schedule_randomization_cutoff)
        
        print(f'schedule order = {schedule_list}')
        
        # for schedule_set_no in (schedule_settings["schedule_list"]["schedule_set_no"].keys()):
        for schedule_set_no in schedule_list:
            Exp_Data.schedule_set_no = schedule_set_no
            schedule_time_start = time.time()
            # reset RI/RR schedules each schedule
            Ri_Schedule.clear_ri_registry()
            Rr_Schedule.clear_rr_registry()
            Fi_Schedule.clear_fi_registry()
            Fr_Schedule.clear_fr_registry()
            
            #reset bX pop per schedule ################################
            #this resets:
                #(1) all stored behavior populations (organism module)
                #(2) stored entropy output (output module)
                #(3) view SE counters (data module)
                
            Organism_Module.Organism.schedule_reset_check(population_reset_switch)
    
            
            
            #adjust stimulus environment, if necessary
            
            #get the current schedule's near set from user data
            schedule_based_near_list = schedule_settings["schedule_list"]["schedule_set_no"][schedule_set_no] \
            ["se_near_set"]
            
            #move compare near/far with current schedule's set. move the correct ones to near, and the rest to far
            Stimulus_Element_Holder.update_se_by_schedule(schedule_based_near_list)
            print("")
            print("")
            print("")
            print("changed near list = ",Stimulus_Element_Holder.get_se_registry()["near"])
            print("changed far list = ",Stimulus_Element_Holder.get_se_registry()["far"])        
            
            print("schedule set = ",schedule_set_no)
            
            #RI/RR/FI/FR schedule generation        
            Ri_Schedule.load_ri_schedules(schedule_set_no,schedule_settings)
            Rr_Schedule.load_rr_schedules(schedule_set_no,schedule_settings)
            Fi_Schedule.load_fi_schedules(schedule_set_no,schedule_settings)
            Fr_Schedule.load_fr_schedules(schedule_set_no,schedule_settings)
 
            #set schedule unique gen number if present
            unique_gen_check = schedule_settings["schedule_list"]["schedule_set_no"][schedule_set_no]\
                .get("nondefault_schedule_generation_count")
            if unique_gen_check == None:
                schedule_gen_num = default_gen_per_schedule
                print(f'\nschedule #{schedule_set_no} has default generations')
            else:
                specific_schedule_gen_number = schedule_settings["schedule_list"]["schedule_set_no"][schedule_set_no]\
                    ["nondefault_schedule_generation_count"]
                schedule_gen_num = specific_schedule_gen_number
                print(f'\nschedule #{schedule_set_no} has {schedule_gen_num} generations')
            
            #run schedule loop
            self.schedule_loop(schedule_gen_num,schedule_set_no) 
            
            #export data per schedule, if type is correct
            if Output_Module.Output.check_if_per_schedule() == True:
                Output_Module.Output.export(Output_Module.Output.output_type_record,\
                                            repitition_number,schedule_set_no)
            
            schedule_time_end = time.time()
            print(f"schedule time is {schedule_time_end - schedule_time_start} seconds")
            
            if Exp_Data.first_schedule_check == True:
                Exp_Data.first_schedule_check = False
            
        #export data per repitition, if type is correct
        if Output_Module.Output.check_if_per_repitition() == True:
            
            Output_Module.Output.export(Output_Module.Output.output_type_record,\
                                        Exp_Data.repitition_number,Exp_Data.schedule_set_no)
        
        print(f'cut offs run = {Organism_Module.Organism.cut_off_used}') 
        print("end of experiment")
        
    def schedule_loop(self,default_gen_num,schedule_set_no):
        generation_number = 1
        procedure_settings = self.all_parameters.get_procedure_settings()
        #target_max_min_info = self.all_parameters.get_target_info()
        selection_loop_type = procedure_settings["selection_loop_type"]
        recombination_type = procedure_settings["recombination_type"]
        mutation_type = procedure_settings["mutation_type"]
        
        #list of the ids for the active targets
        schedule_active_targets = self.all_parameters.get_schedule_active_targets(schedule_set_no)
        
        for current_gen in range(0,default_gen_num):
            #debugging switch (checking time)
           
            
            Exp_Data.current_gen = current_gen
            if Exp_Data.time_check == True: 
                generation_time_start = time.time()
                
            if generation_number == 1 \
            or generation_number == 20500 \
            or generation_number % 1000 == 0:
                # print("")
                # print("")
                print("generation number = ", generation_number)
            generation_number += 1
            
            #re/set reinforcer type
            Exp_Data.reinforcer_type = None
            
            #add or remove SE from the "near" range based on what
            #reinforcers are set up for delivery
            
            Stimulus_Element_Holder.reinforcement_setup_based_se_switch()
            
            
            #observation (example:up to 5)
            if Exp_Data.time_check == True: 
                view_time_start = time.time()
            viewed_se = Organism_Module.Observation.look(procedure_settings["observation_type"], \
                                                         Stimulus_Element_Holder.get_se_registry()["near"])
            Exp_Data.record_observed_se(viewed_se)
            if Exp_Data.time_check == True: 
                view_time_end = time.time()
                print("Observation time is {} seconds".format(view_time_end - view_time_start))
             
            #checks for new, and if new, create a random bx pop
            Organism_Module.Organism.check_viewed_se_for_new(Exp_Data.viewed_se)    
            
            # print("")
            if Exp_Data.time_check == True: 
                emit_time_start = time.time()
            [Exp_Data.emitted_behavior, Exp_Data.chosen_bx_pop_se] = Organism_Module.Emission.emit(procedure_settings["emission_type"],Exp_Data.viewed_se)
            # print ("emitted bx = ",Exp_Data.emitted_behavior)    
            if Exp_Data.time_check == True: 
                emit_time_end = time.time() 
                print("Emission time is {} seconds".format(emit_time_end - emit_time_start))
            # print("viewed stimulus elements = ", Exp_Data.viewed_se)
            
            #check targets
            #check targets: returns target id number, or None
            if Exp_Data.time_check == True: 
                target_time_start = time.time()
            Exp_Data.hit_target_id = General_Functions_Module.check_targets \
                            (Exp_Data.emitted_behavior,schedule_active_targets)
            
            # print("hit_target_id = ",Exp_Data.hit_target_id)
            
            #check if reinforcement is set up
            if Exp_Data.hit_target_id is not None:
                
                #advance specific RR/FR timer (peckpeck.target_id)
                Rr_Schedule.peckpeck(Exp_Data.hit_target_id)
                Fr_Schedule.peckpeck(Exp_Data.hit_target_id)
                
                #check if reinforcement is set up
                if Ri_Schedule.is_reinforcement_set_up(Exp_Data.hit_target_id,False) \
                or Fi_Schedule.is_reinforcement_set_up(Exp_Data.hit_target_id,False) \
                or Rr_Schedule.is_reinforcement_set_up(Exp_Data.hit_target_id,False) \
                or Fr_Schedule.is_reinforcement_set_up(Exp_Data.hit_target_id,False):
                    Exp_Data.reinforcer_type = self.all_parameters.get_reinforcement_type(schedule_set_no,Exp_Data.hit_target_id)
                    # print("reinforcement type = ", Exp_Data.reinforcer_type)
                else:
                    Exp_Data.reinforcer_type = None
            else:
                Exp_Data.reinforcer_type = None
                
            if Exp_Data.time_check == True: 
                target_time_end = time.time()
                print("target time is {} seconds".format(target_time_end - target_time_start))
            
            #collect modifier info
            if Exp_Data.time_check == True: 
                modifier_time_start = time.time()
            
            #reinforcement context data collection
            Organism_Module.Organism.collect_reinforcement_context_data \
                                     (Exp_Data.current_gen, Exp_Data.hit_target_id,Exp_Data.reinforcer_type)     
            
            
            
            if Exp_Data.time_check == True:      
                modifier_time_end = time.time()
                print("modifier time is {} seconds".format(modifier_time_end - modifier_time_start))
            
            if Exp_Data.time_check == True:             
                selection_time_start = time.time()
            # selection of parents
            parents_dict = Organism_Module.Selection_Loop.run_loop(selection_loop_type, Exp_Data.emitted_behavior,\
                                                                   Exp_Data.reinforcer_type, Exp_Data.chosen_bx_pop_se, \
                                                                   Exp_Data.viewed_se, procedure_settings)
            if Exp_Data.time_check == True: 
                selection_time_end = time.time()
                print("Selection time is {} seconds".format(selection_time_end - selection_time_start))
            # print(parents_dict)
            
            # selection landscape (circular)
            # Selection Method (continuous linear)
            # perameters: FDF mean, %replace <-- random
            # inputs: viewed_se, emitted_behavior, reinforcer
            
            
            
            #recombination of parents (200 parents, or population size *2)
            #bit-wise
            if Exp_Data.time_check == True: 
                recomb_time_start = time.time()
                
            children_dict = Organism_Module.Recombination.combine(recombination_type, parents_dict,\
                                                                  Organism_Module.Organism.number_of_binary_digits)
            if Exp_Data.time_check == True: 
                recomb_time_end = time.time()
                print("recombination time is {} seconds".format(recomb_time_end - recomb_time_start))   
            
            #mutation of children
            #inputs mutation_type, mutation rate, 
            
            if Exp_Data.time_check == True: 
                mutation_time_start = time.time()
                
            mutated_children = Organism_Module.Mutation.mutate(mutation_type, children_dict)
            if Exp_Data.time_check == True: 
                mutation_time_end = time.time()
                print("mutation time is {} seconds".format(mutation_time_end - mutation_time_start))  
            
                # add children back in / replace old
            #inputs child_list, len(child_list), bx_pop_size
            # print("mutant dict = ", mutated_children)   
            #add children back in / replace old
            #inputs child_list, len(child_list), bx_pop_size
            # print("pre red_1[0] = ",Organism_Module.Organism.Behaviors["red_1"][0]) 
            # print("pre red_1[0] type = ",type(Organism_Module.Organism.Behaviors["red_1"])) 
            if Exp_Data.time_check == True: 
                log_time_start = time.time()
            
            #Set the children to be the original population.
            #if the number of children is less than the original population size, 
            #add random old behaviors to the children to maintain population size.
            Organism_Module.Organism.log_children(mutated_children)
            
            if Exp_Data.time_check == True: 
                log_time_end = time.time()
                print("log chidlren time is {} seconds".format(log_time_end - log_time_start))  
            # print("post red_1[0] = ",Organism_Module.Organism.Behaviors["red_1"][0]) 
            # print("post red_1[0] type = ",type(Organism_Module.Organism.Behaviors["red_1"])) 
            
            # print("Modified Organism_Module.Organism.behaviors = ", Organism_Module.Organism.Behaviors)
            #advance RI/FI timers (ticktock)
            Ri_Schedule.ticktock()
            Fi_Schedule.ticktock()
            
            #capture output
            if Exp_Data.time_check == True: 
                capture_time_start = time.time()
                
            Output_Module.Output.capture(Output_Module.Output.output_type_record,\
                                         Exp_Data.schedule_set_no, Exp_Data.current_gen, Exp_Data.emitted_behavior,\
                                         Exp_Data.reinforcer_type, Exp_Data.hit_target_id)
            
            if Exp_Data.time_check == True: 
                capture_time_end = time.time()
                print("capture time is {} seconds".format(capture_time_end - capture_time_start))      
            
            if Exp_Data.time_check == True: 
                generation_time_end = time.time()
                print("generation time is {} seconds".format(generation_time_end - generation_time_start))
            Exp_Data.clear_gen_data()
           
        print("end of schedule")

        
    


    
    
 
    