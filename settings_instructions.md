# Settings Instructions

This document will take the reader through the process of setting up their own parameters for the pyETBD-SST

# Table of Contents

0. General Setup Information
1. Experiment General Settings
2. Schedule Settings
3. Organism Settings
4. Procedure Settings
5. Stimulus Element Settings

# General Setup Information

pyETBD-SST has been designed to be modular, and has very few builtin settings that can't be changed.  

The pyETBD-SST has one necessary folder:
>outputs

A folder for inputs is useful but not necessary as long as you can specify the setting file location. 

All settings are in JSON format, but these instructions will not review the file format. 

Using an online JSON format checker is very helpful for finding syntax errors in the parameter setup. 

# Experiment General Settings


## Example

<details>
<summary>Example Experiment General Settings File</summary>

\{ 
	
    "repetitions":10,

	"default_generations_per_schedule":20000,

	"random_shuffle_schedule_x_and_after":null,

	"data_output_type":"stream_output_per_repitition_3",

	"output_entropy":true,

	"output_selection_modifier":true,

	"output_background":true,

	"output_emitted_behavior_population":false,

	"output_entropy_moving_avg_length":5,

	"population_reset_between_schedules":false,

	"experiment_timer_style":"generations",

	"filename_modifier":"mult_sched_se_r5g5w5_bkgd_ri20",

	"reinforcement_context_magnitude_modifer_active":false,

	"reinforcement_context_user_modifier":1,

	"reinforcement_capture_length":10
\}
</details>
<br/>

## Parameters

<details>
<summary>List of Parameters</summary>
<br/>

**"repetitions"** : **(integer value)**  
>This number determines the number of total idential runs the program will make using the parameters given. Each repetition can be considered an unique artifical organism, if the behavioral populations are not reset between schedules. If the behavioral populations are reset between schedules, then each schedule can be considered an unique artifical organism.
<br/>

**"default_generations_per_schedule"** : **(integer value)**  

>This number determines the number of generations in each schedule. This can be over written for a specific schedule using the "nondefault_schedule_generation_count" parameter in the experiment_schedule_settings file.
<br/>

**"random_shuffle_schedule_x_and_after"** : **(integer value)** or **null**
>This parameter will cause all schedules prior to the chosen schedule to be run in the order set in the experiment_schedule_settings file, and schedule X and everything after will have a random order. This was done to mimic the stimulus generalization experiments, which utilize this experimental setup.
<br/>

**"data_output_type"** : **'string'**
>This parameter determines the code used to generate the output CSV file. No other output file types are currently supported.

<details>
<summary>Current Data Output Types</summary>
<br/>

**'stream_output_per_repitition_3'**
>Current Version. Outputs all the data in one repitition into a single CSV file. One generation per line.
Output includes: 
1. Schedule Number
2. Emitted Behavior Phenotype
3. Stimulus Element number the emitted behavior was drawn from (number is based on the order created by settings)
4. Number of observed stimulus elements sent to the following step (after the number has been reduced by entropy selection)
5. Reinforcement recieved for behavior on X target that generation (RX = record for target X reinforcement, value can be "1" or "0")  
	The number of columns will vary based on the number of targets
6. Behavior emitted in X target for that generation (BX = record for target X behavior, value can be "1" or "0")  
	The number of columns will vary based on the number of targets

Extra information can be added to output based on the following settings:
1. output_entropy
2. output_selection_modifier
3. output_background
4. output_emitted_behavior_population

**'stream_output_per_repitition_2'**	
>Older version, Do not use

**'stream_output_per_repitition'**
>Older version, Do not use

**'stream_output_per_schedule'**
>TBD

</details>
<br/>

**"output_entropy"** : **true** or **false**
>Output will contain a column with the entropy for the stimulus element a behavior was emitted from that generation.

**"output_selection_modifier"** : **true** or **false**
>Output will contain columns for window length, window length goal, rc difference, and the selection modifier percentage

> [!WARNING]
> Only use if the Procdure>selection_modifier type: "reinforcement_context_kernel" is specified! 

**"output_background"** : **true** or **false**
>Adds columns to output CSV for background target behavior emitted and reinforcement recieved
1. Reinforcement recieved for behavior on X background target that generation  
	(BK-RX = record for background target X reinforcement, value can be "1" or "0")  
	The number of columns will vary based on the number of targets
2. Behavior emitted in X target for that generation  
	(BK-BX = record for background target X behavior, value can be "1" or "0")  
	The number of columns will vary based on the number of targets

**"output_emitted_behavior_population"** : **true** or **false**
>The behavior population that the emitted behavior was drawn from will be recorded by phenotype

> [!IMPORTANT]
> This can expand the output file size dramaticly depending on the number of behaviors in a population. 

**"output_entropy_moving_avg_length"** : **(interger value)**
>Not functional with 'stream_output_per_repitition_3'

**"population_reset_between_schedules"** : **true** or **false**
>If true, all behavioral populations will be deleted between schedules

**"experiment_timer_style"** : **'string'**
>Currently not functional. This setting does nothing.

**"filename_modifier"** : **'string'**
>Allows naming of the output file. The repitition number and 'allschedules' will be appended at the end.  
For a filename_modifier : 'Exp1-2_POP200_BKGD_RI01_RM20_'  
The output file : 'Exp1-2_POP200_BKGD_RI01_RM20_rep0_allschedules.csv' 

**"reinforcement_context_magnitude_modifer_active"** : **true** or **false**
>Untested

**"reinforcement_context_user_modifier"** : **(interger value)**
>Untested

**"reinforcement_capture_length"** : **(interger value)**
>Untested

</details>
<br/>

# Experiment Schedule Settings

## Example

<details>
<summary>Example Experiment Schedule Settings File</summary>

{ 
	
	"target_list":	
	{	
		"target_id":	
		{	
			"1":	
			{	
				"target_type":"primary",	
				"target_high": 511,	
				"target_low": 471,	
				"reward_continvency_type":"target"	
			},	
			"2":	
			{	
				"target_type":"primary",	
				"target_high": 552,	
				"target_low": 512,	
				"reward_continvency_type":"varied"	
			},				
			"3":	
			{	
				"target_type":"background",	
				"background_style":"high_low",	
				"target_high": 470,	
				"target_low": 410	
			},	
			"4":	
			{	
				"target_type":"background",	
				"background_style":"high_low",	
				"target_high": 613,	
				"target_low": 553	
			},				
			"5":	
			{	
				"target_type":"background",	
				"background_style":"background_generator",	
				"background_generator_settings":	
				{    
	    			    "generator_type":"random_nonsequential_post_screening",    
	                           "screen_out_equal_or_less":1,    
	                           "remove_avg_hamming_equal_or_less":null,    
	                           "remove_std_hamming_equal_or_greater":null,    
	                           "removal_function_type":"percentage",    
	                		   "number_of_nonsequential_targets":1,
	                           "nonsequential_background_target_size":200	
				}
			}
	
		}
	
	},
	
	"schedule_list":
	{
		"schedule_set_no":
		{
			"1":	
			{	
				"nondefault_schedule_generation_count":20000,	
				"active_target_id_no":	
				{	
					"1":
					{
						"reinforcement_rate_type":"RI",	
						"reinforcement_rate": 0,
						"reinforcer":"pellet"
					},
					"5":
					{
						"reinforcement_rate_type":"RI",
						"reinforcement_rate": 10,
						"reinforcer":"scratch"
					}
				},
				"se_near_set":
				[
					"trainingwall","wall"	
				]
	        },
			"2":
			{
				"nondefault_schedule_generation_count":20000,
				"active_target_id_no":
				{
					"1":
					{
						"reinforcement_rate_type":"RI",
						"reinforcement_rate": 10,
						"reinforcer":"pellet"
					}
				},
				"se_near_set":
				[
					"trainingwall","redone","redtwo","redthree","redfour","redfive"
				]
            },
			"3":
			{
				"active_target_id_no":
				{
					"1":
					{
						"reinforcement_rate_type":"RI",
						"reinforcement_rate": 0,
						"reinforcer":"pellet"
					},
					"5":
					{
						"reinforcement_rate_type":"RI",
						"reinforcement_rate": 10,
						"reinforcer":"scratch"
					}
				},
				"se_near_set":
				[
					"wall","redone","redtwo","redthree","redfour","rminusone"	
				]

            }

		}

	}

}
        
    


</details>
<br/>

## Parameters

<details>
<summary>List of Parameters</summary>
<br/>
 



</details>
<br/>

# Organism Settings

## Example

<details>
<summary>Example Organism Settings File</summary>

TBD

</details>
<br/>

## Parameters

<details>
<summary>List of Parameters</summary>
<br/>

</details>
<br/>

# Procedure Settings

## Example

<details>
<summary>Example Procedure Settings File</summary>

TBD

</details>
<br/>

## Parameters

<details>
<summary>List of Parameters</summary>
<br/>

</details>
<br/>

# Stimulus Environment Settings

## Example

<details>
<summary>Example Stimulus Environment Settings File</summary>

TBD

</details>
<br/>

## Parameters

<details>
<summary>List of Parameters</summary>
<br/>

</details>
<br/>
