# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 17:16:32 2022

@author: Cyrus
"""
# loop_number = 1
# repetitions = 6
# for i in range(0,repetitions):
#     print("loop number ", loop_number)
#     loop_number += 1

# import glob
# # from pathlib import Path
# import json
# data_folder = Path("C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/SST-ETBD Code/inputs")
# file_index = 0
# settingfilenames = []
# for file in glob.glob("C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/SST-ETBD Code/inputs/*settings*.json"):
#     start_index = file.rfind("\\") + 1
#     end_index = file.rfind(".")
#     settingfilenames.append(file[start_index:end_index])
#     file_index += 1
# a = "C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/SST-ETBD Code/inputs"
# b = "\\*settings*.json"
# print(a+b)

# a = "C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/SST-ETBD Code/inputs/experiment_schedule_settings.json"
# with open(a,'r') as test_file:     
#     c = json.load(test_file)
    # print(c["schedule_list"]["schedule_set_no"].keys())
# generation_number = 2000
# if generation_number % 1000 == 0 \
# or generation_number == 1 \
# or generation_number == 20500:
#     print("generation number ", generation_number)


# class stimulus_element_holder:
    
#     def __init__(self,locations,se_types):
#         pass

# x = {
#  	"global_environment":
#          {
#          "Location_id":
#              {
#              "L1":"near",			
#              "L2":"far"
#              }
#         },
    
#      "stimulus_elements":
#     	{	 
#     		"se_type_1":
#     		{
#     			"se_quantity":5,
#     			"se_stimulus":"red",
#     			"se_start_location":"near"
#     		},
#     		"se_type_2":
#     		{
#     			"se_quantity":5,
#     			"se_stimulus":"green",
#     			"se_start_location":"far"
#     		},
#     		"se_type_3":
#     		{
#     			"se_quantity":5,
#     			"se_stimulus":"wall",
#     			"se_start_location":"near"
#     		}	
#     	}
#     }
    
# # se1_q = x["stimulus_elements"]["se_type_1"]["se_quantity"]
# # se1_st = x["stimulus_elements"]["se_type_1"]["se_stimulus"]


# se_dict = {}
# for gobal_locations in x["global_environment"]["Location_id"].values():
#     se_dict.update({gobal_locations:[]})

#     for types in x["stimulus_elements"].keys():
#         for quantity in range(1,x["stimulus_elements"][types]["se_quantity"]+1):
#             se_id = print(str(quantity)+x["stimulus_elements"][types]["se_stimulus"])
#             se_id = str(quantity)+x["stimulus_elements"][types]["se_stimulus"]
#             if gobal_locations == x["stimulus_elements"][types]["se_start_location"]: 
#                 se_dict[gobal_locations] += [se_id]

    
#a = stimulus_element_holder("near,far",x,y)
        
        