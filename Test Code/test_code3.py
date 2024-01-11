# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 20:23:47 2022

@author: Cyrus
"""
import Parameter_Module
import glob
from pathlib import Path
from RI_Module import Ri_Schedule
from RR_Module import Rr_Schedule
from SE_Module import Stimulus_Element_Holder
import Organism_Module
import General_Functions_Module
# import time

class Test_Runner:
    
    test_attribute =3
    #initialize
    def __init__(self, setting_files):
        for paths in setting_files:
            temp_data = Parameter_Module.load_settings(setting_files)
        self.all_parameters = Parameter_Module.parameter_holder(temp_data)

        #######################################
        #set Organism class variables
        organism_settings = self.all_parameters.get_organism_settings()
        Organism_Module.Organism.set_population_size(organism_settings["population_size"])
        Organism_Module.Organism.set_reinforcer_magnitude(organism_settings["reinforcer_magnitude_data"])
        Organism_Module.Organism.set_number_of_binary_digits(organism_settings["number of binary digits"])
        Organism_Module.Organism.set_percent_replace(organism_settings["percent_replace"])
        Organism_Module.Organism.set_mutation_rate(organism_settings["mutation_rate"])
 
        ######################################

        self.test_loop(self.all_parameters.get_repititions())
        
    def test_loop(self,repititions):
        schedule_settings = self.all_parameters.get_experiment_schedule_settings()
        reinforcement_environment = self.all_parameters.get_experiment_schedule_settings()
        Stimulus_Element_Holder.load_stimulus_environment(self.all_parameters.get_stimulus_environment_settings())
        pop_reset_settings = self.all_parameters.get_population_reset_style()
        # print("pop_reset_settings type = ",pop_reset_settings )
        # print(reinforcement_environment.keys())
        # print(len(reinforcement_environment["target_list"]["target_id"]))
        #xx = len(reinforcement_environment["target_list"]["target_id"])
        # count = 0
        # for ids in (reinforcement_environment["target_list"]["target_id"].keys()):
        #     print("ids = ", ids)
        #     Ri_Schedule(ids,0)
                          
        #     x = Ri_Schedule.get_ri_registry()
        #     print("mean =", x[count].mean)
        #     count += 1
        
        # print("mean of x[0] = ", x[0].get_mean())
        # print("mean of x[1] = ", x[1].get_mean()) 
        # x[0].set_mean(50)
        # print("mean of x[0] = ", x[0].mean)    
        # print("mean of x[1] = ", x[1].mean)   
        # print("id of x[0] = ", x[0].get_target_id())
        # print("id of x[1] = ", x[1].get_target_id())
        
        # print("ticks = ",x[0].ri_ticks_into_interval)
        # print("ticks = ",x[1].ri_ticks_into_interval)
        # Ri_Schedule.ticktock()
        # print("ticktock!")
        # print("ticks = ",x[0].ri_ticks_into_interval)
        # print("ticks = ",x[1].ri_ticks_into_interval)
        # print("c_interval = ",x[0].current_interval)
        # print("c_interval = ",x[1].current_interval)
        # print("target id 1 gets a new interval")
        # x[0].get_new_interval()
        # print("c_interval = ",x[0].current_interval)
        # print("c_interval = ",x[1].current_interval)
        
        # fake schedule loop
        for schedule_set_no in (reinforcement_environment["schedule_list"]["schedule_set_no"].keys()):
            Organism_Module.Organism.Schedule_reset_check(pop_reset_settings)
            Ri_Schedule.clear_ri_registry()
            Rr_Schedule.clear_rr_registry()
            # print("")
            # print("schedule set = ",schedule_set_no)
            
            schedule_based_near_list = reinforcement_environment["schedule_list"]["schedule_set_no"][schedule_set_no] \
            ["se_near_set"]
            
              
            #move compare near/far with current schedule's set. move the correct ones to near, and the rest to far
            Stimulus_Element_Holder.update_se_by_schedule(schedule_based_near_list)      
            
            #RI/RR schedule generation        
            Ri_Schedule.load_ri_schedules(schedule_set_no,schedule_settings)
            Rr_Schedule.load_rr_schedules(schedule_set_no,schedule_settings)
            
            self.schedule_loop(self.all_parameters.get_default_generation_num(),schedule_set_no)
            
            
    def schedule_loop(self,default_gen_num,schedule_set_no):
        generation_number = 1
        target_max_min_info = self.all_parameters.get_target_info()
        
        #list of the ids for the active targets
        schedule_active_targets = self.all_parameters.get_schedule_active_targets(schedule_set_no)
        
        
        for i in range(0,default_gen_num):
            # print("")
            # print("")
            # print("generation number ", generation_number)
            generation_number += 1
            parents_dict = {}
            children_dict = {}
            
            #re/set reinforcer type
            reinforcer_type = None
            
            procedure_settings = self.all_parameters.get_procedure_settings()
            selection_loop_type = procedure_settings["selection_loop_type"]
            recombination_type = procedure_settings["recombination_type"]
            mutation_type = procedure_settings["mutation_type"]
            #observation (up to 5)
            
            # print("")
            # print("")
            # print(Stimulus_Element_Holder.get_se_registry()["near"])
            viewed_se = Organism_Module.Observation.look(procedure_settings["observation_type"], \
                                                         Stimulus_Element_Holder.get_se_registry()["near"])
            
            # print ("viewed_se = ",viewed_se)
            #checks for new, and if new, create a random bx pop
            Organism_Module.Organism.check_viewed_se_for_new(viewed_se)
            # print("")
            
            
            #emission
            # # print("emission type", procedure_settings["emission_type"])
            # print("org behavior keys = ",  Organism_Module.Organism.get_behavior_pop_dict().keys())
            # print("org behavior value type = ",Organism_Module.Organism.get_behavior_pop_dict().values())
            
            [emitted_behavior, chosen_bx_pop_se] = Organism_Module.Emission.emit(procedure_settings["emission_type"],viewed_se)

            # print ("emitted bx = ",emitted_behavior)
            
            #check targets: returns target id number, or None
            hit_target_id = General_Functions_Module.check_targets \
                            (emitted_behavior,target_max_min_info,schedule_active_targets)
            
            # print("hit_target_id = ",hit_target_id)
            
            if hit_target_id is not None:
                
                #advance specific RR timer (peckpeck.target_id)
                Rr_Schedule.peckpeck(hit_target_id)
                
                #check if reinforcement is set up
                if Ri_Schedule.is_reinforcement_set_up(hit_target_id) \
                or Rr_Schedule.is_reinforcement_set_up(hit_target_id):
                    reinforcer_type = self.all_parameters.get_reinforcement_type(schedule_set_no,hit_target_id)
                    # print("reinforcement type = ", reinforcer_type)
                else:
                    reinforcer_type = None
            
            
            #selection Loop
            ########################
            #selection of parents
            # selection landscape (circular)
            # Selection Method (continuous linear)
            # perameters: FDF mean, %replace <-- random
            # inputs: viewed_se, emitted_behavior, reinforcer
            
            parents_dict = Organism_Module.Selection_Loop.run_loop(selection_loop_type, emitted_behavior,\
                                                                   reinforcer_type, chosen_bx_pop_se, \
                                                                   viewed_se, procedure_settings)
            
            # print("parents dict = ",parents_dict)
            
            
            #recombination of parents (200 parents, or population size *2)
            #bit-wise
            #parse parents_list - each se
            #convert pair to binary, combine into child, return to decimal, put into dictionary
            #inputs: parents_list, Organism.number_of_binary_digits
            children_dict = Organism_Module.Recombination.combine(recombination_type, parents_dict,\
                                                                  Organism_Module.Organism.number_of_binary_digits)
            
            # print("children dict = ", children_dict)
            # print("children dict length keys=", len(children_dict.keys()))
            # print("children dict length values=", len(children_dict["red_1"]))
            #mutation of children
            #inputs mutation_type, mutation rate, 
            # print("child dict = ", children_dict)
            mutated_children = Organism_Module.Mutation.mutate(mutation_type, children_dict,\
                                                               Organism_Module.Organism.mutation_rate, \
                                                               Organism_Module.Organism.number_of_binary_digits)
            
            # print("mutant dict = ", mutated_children)   
            #add children back in / replace old
            #inputs child_list, len(child_list), bx_pop_size
            # print("pre red_1[0] = ",Organism_Module.Organism.Behaviors["red_1"][0]) 
            # print("pre red_1[0] type = ",type(Organism_Module.Organism.Behaviors["red_1"])) 
            
            Organism_Module.Organism.log_children(mutated_children)
            # print("post red_1[0] = ",Organism_Module.Organism.Behaviors["red_1"][0]) 
            # print("post red_1[0] type = ",type(Organism_Module.Organism.Behaviors["red_1"])) 
            
            # print("Modified Organism_Module.Organism.behaviors = ", Organism_Module.Organism.Behaviors)
            #advance RI timers (ticktock)
            Ri_Schedule.ticktock()
            
            # print("viewed stimulus elements = ", viewed_se)
           
           
            # emission
            # ....
            
        print("end of schedule")
            
          
            
settings_folder = str(Path("C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/SST-ETBD Code/inputs"))
setting_files = glob.glob(settings_folder + "/*settings*.json")
a = Test_Runner(setting_files)
