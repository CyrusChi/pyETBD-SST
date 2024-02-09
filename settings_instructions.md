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

<br/>

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
> Only use if the procdure_settings>selection_modifier_type: "reinforcement_context_kernel" is specified! 

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

**"output_entropy_moving_avg_length"** : **(integer value)**
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
>Untested, Keep 'false'

**"reinforcement_context_user_modifier"** : **(integer value)**
>Untested, Keep 'false'

**"reinforcement_capture_length"** : **(integer value)**
>Untested, Keep 'false'

</details>
<br/>
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

## Parameters

<details>
<summary>List of Parameters</summary>
<br/>

### General Format

There two groups over arching groups within the experiment schedule settings, and those are the **'target_list'** and the **'schedule_list'**. (Although these are called lists, they are mostly written in a nested dictionary format following the JSON specifications)

Within the **'target_list'**, there is another dictionary called **'target_id'**. (the target_id dictionary is the only item in target list)

Each target id is identified by it's key, which is a integer starting from the number 1. The dictionary value is another dictionary containing all the parameters associated with the target id. 



Within the **'schdule_list'**, there is another dictionary called **'schedule_set_no'**. (the schedule_set_no dictionary is the only item in schedule list)

Each schedule set number is identified by it's key, which is a integer starting from the number 1. The dictionary value is another dictionary containing all the parameters associated with the schedule. 

### Target List Parameters

<details>
<summary>See Parameters</summary>
<br/>

**"target_type"** : **'string'**
>There are currently two major target types (**'primary'** and **'background'**) with their own sub parameters. The type of target primarily effects the output style, but it also impacts how random background targets are generated using the **'background_generator'**. Primary targets are always reported in the output, while background target data is optional. 

<details>
<summary>'primary' target</summary>
<br/>

**'primary'**
>Primary targets are meant to represent the targets typically identified by an experimenter in their experiment, like a key, lever, or switch. Their range of operation is defined by the highest and lowest value in terms of the phenotype space. 

Subparameters:

**"target_high"** : **(integer value)**
>High end of the phenotype space for the target (inclusive)

**"target_low"** : **(integer value)**
>Low end of the phenotype space for the target (inclusive)

**"reward_continvency_type"** : **'string'**
>Untested, do not use. May be omitted.

</details>
<br/>

<details>
<summary>'background' target</summary>
<br/>

**'background'**
>Background targets are meant to represent the targets typically _not_ identified by an experimenter in their experiment. This represents all kinds of distractions, or other rewards that are not typically controlled within an experiment.

There are currently two styles of background targets: **'high_low'** and **'background_generator'**.

The background type: **'background_generator'** should be placed last on the list of target ids if more than one target is generated.


<details>
<summary>'background_style' : 'high_low'</summary>
<br/>

This style the same high and low subparameters as the 'primary' target.

Subparameters:
**"target_high"** : **(integer value)**
>High end of the phenotype space for the target (inclusive)

**"target_low"** : **(integer value)**
>Low end of the phenotype space for the target (inclusive)

</details>
<br/>

<details>
<summary>'background_style' : 'background_generator'</summary>
<br/>

This style is designed to pick background targets following the subparameters listed in the settings file.  

Each target will get it's own target id, starting from the target id of the generator, and increasing by one for each background target.

> [!CAUTION]
> If the settings chosen for the background are too stringent, the program will stop itself if there are not enough eligible background targets. Since the background targets are chosen randomly, this can result in some repititions working fine while others stop due to not having enough background targets. 

The settings for the background generator are contained within the **'background_generator_settings'**.

**'generator_type'** : **'string'**
> There are multiple generator types, and each one has it's own subsettings. 

**'random_nonsequential_post_screening'**
> Creates one or more background classes that are non-sequential and chosen at random. 

<details>
<summary>See subparameters</summary>
<br/>

**"screen_out_equal_or_less"** : **integer** or **null**
>Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have a hamming distance less than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!NOTE]
> With two, 40 phenotype target classes, a screen out larger than one can make the remaining space too small for a 200 digit background target class.

**"remove_avg_hamming_equal_or_less"** : **number** or **null**
> Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have an average hamming distance less than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!IMPORTANT]
> This parameter requires "removal_function_type" to be set to work.

**"remove_std_hamming_equal_or_greater"** : **number** or **null**
> Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have a standard deviation of it's hamming distances greater than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!NOTE]
> The max standard deviation for a 10 digit genotype is around 4.2.

> [!IMPORTANT]
> This parameter requires "removal_function_type" to be set to work.

**"removal_function_type"** : **string** ('percentage' or 'value')
> Allows **"remove_avg_hamming_equal_or_less"** and/or **"remove_std_hamming_equal_or_greater"** to function as a percentage of the range for that parameter or a flat value.

**"number_of_nonsequential_targets"** : **integer** 
> The number of targets to be created. This parameter is non-sequential target class specific.

**"nonsequential_background_target_size"** : **integer** 
> The number of digits in one target class. This parameter is non-sequential target class specific.

</details>
<br/>

**'max_mean_nonsequential_post_screening'**
> Creates one or more background classes that are non-sequential and are chosen based on average hamming distance from the primary targets, going from largest to smallest

<details>
<summary>See subparameters</summary>
<br/>

**"screen_out_equal_or_less"** : **integer** or **null**
>Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have a hamming distance less than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!NOTE]
> With two, 40 phenotype target classes, a screen out larger than one can make the remaining space too small for a 200 digit background target class.

**"remove_avg_hamming_equal_or_less"** : **number** or **null**
> Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have an average hamming distance less than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!IMPORTANT]
> This parameter requires "removal_function_type" to be set to work.

**"remove_std_hamming_equal_or_greater"** : **number** or **null**
> Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have a standard deviation of it's hamming distances greater than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!NOTE]
> The max standard deviation for a 10 digit genotype is around 4.2.

> [!IMPORTANT]
> This parameter requires "removal_function_type" to be set to work.

**"removal_function_type"** : **string** ('percentage' or 'value')
> Allows **"remove_avg_hamming_equal_or_less"** and/or **"remove_std_hamming_equal_or_greater"** to function as a percentage of the range for that parameter or a flat value.

**"number_of_nonsequential_targets"** : **integer** 
> The number of targets to be created. This parameter is non-sequential target class specific.

**"nonsequential_background_target_size"** : **integer** 
> The number of digits in one target class. This parameter is non-sequential target class specific.

</details>
<br/>

**'max_mean_std_nonsequential_post_screening'**
> Creates one or more background classes that are non-sequential and are chosen based on average hamming distance from the primary targets, going from largest to smallest. If multple phenotypes have the same average hamming distance, they are additionally sorted from smallest standard deviation to largest, and picked in that order.

<details>
<summary>See subparameters</summary>
<br/>

**"screen_out_equal_or_less"** : **integer** or **null**
>Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have a hamming distance less than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!NOTE]
> With two, 40 phenotype target classes, a screen out larger than one can make the remaining space too small for a 200 digit background target class.

**"remove_avg_hamming_equal_or_less"** : **number** or **null**
> Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have an average hamming distance less than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!IMPORTANT]
> This parameter requires "removal_function_type" to be set to work.

**"remove_std_hamming_equal_or_greater"** : **number** or **null**
> Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have a standard deviation of it's hamming distances greater than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!NOTE]
> The max standard deviation for a 10 digit genotype is around 4.2.

> [!IMPORTANT]
> This parameter requires "removal_function_type" to be set to work.

**"removal_function_type"** : **string** ('percentage' or 'value')
> Allows **"remove_avg_hamming_equal_or_less"** and/or **"remove_std_hamming_equal_or_greater"** to function as a percentage of the range for that parameter or a flat value.

**"number_of_nonsequential_targets"** : **integer** 
> The number of targets to be created. This parameter is non-sequential target class specific.

**"nonsequential_background_target_size"** : **integer** 
> The number of digits in one target class. This parameter is non-sequential target class specific.

</details>
<br/>


**'max_mean_continuous_post_screening'**
> Creates one or more background classes that are continous in phenotype space and are chosen based on average hamming distance from the primary targets, going from largest to smallest

<details>
<summary>See subparameters</summary>
<br/>

**"screen_out_equal_or_less"** : **integer** or **null**
>Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have a hamming distance less than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!NOTE]
> With two, 40 phenotype target classes, a screen out larger than one can make the remaining space too small for a 200 digit background target class.

**"remove_avg_hamming_equal_or_less"** : **number** or **null**
> Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have an average hamming distance less than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!IMPORTANT]
> This parameter requires "removal_function_type" to be set to work.

**"remove_std_hamming_equal_or_greater"** : **number** or **null**
> Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have a standard deviation of it's hamming distances greater than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!NOTE]
> The max standard deviation for a 10 digit genotype is around 4.2.

> [!IMPORTANT]
> This parameter requires "removal_function_type" to be set to work.

**"removal_function_type"** : **string** ('percentage' or 'value')
> Allows **"remove_avg_hamming_equal_or_less"** and/or **"remove_std_hamming_equal_or_greater"** to function as a percentage of the range for that parameter or a flat value.

**"number_of_continuous_targets"** : **integer** 
> The number of targets to be created. This parameter is continous target class specific.

**"continuous_background_target_length"** : **integer** 
> The number of continuous digits in one target class. This parameter is continous target class specific.

</details>
<br/>

**'max_mean_std_continuous_post_screening'**
> Creates one or more background classes that are continous in phenotype space and are chosen based on average hamming distance from the primary targets, going from largest to smallest. If multple phenotypes have the same average hamming distance, they are additionally sorted from smallest standard deviation to largest, and picked in that order.

<details>
<summary>See subparameters</summary>
<br/>

**"screen_out_equal_or_less"** : **integer** or **null**
>Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have a hamming distance less than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!NOTE]
> With two, 40 phenotype target classes, a screen out larger than one can make the remaining space too small for a 200 digit background target class.

**"remove_avg_hamming_equal_or_less"** : **number** or **null**
> Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have an average hamming distance less than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!IMPORTANT]
> This parameter requires "removal_function_type" to be set to work.

**"remove_std_hamming_equal_or_greater"** : **number** or **null**
> Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have a standard deviation of it's hamming distances greater than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!NOTE]
> The max standard deviation for a 10 digit genotype is around 4.2.

> [!IMPORTANT]
> This parameter requires "removal_function_type" to be set to work.

**"removal_function_type"** : **string** ('percentage' or 'value')
> Allows **"remove_avg_hamming_equal_or_less"** and/or **"remove_std_hamming_equal_or_greater"** to function as a percentage of the range for that parameter or a flat value.

**"number_of_continuous_targets"** : **integer** 
> The number of targets to be created. This parameter is continous target class specific.

**"continuous_background_target_length"** : **integer** 
> The number of continuous digits in one target class. This parameter is continous target class specific.

</details>
<br/>

**'random_continuous_post_screening'**
> Creates one or more background classes that are continous in phenotype space and chosen at random. 

<details>
<summary>See subparameters</summary>

**"screen_out_equal_or_less"** : **integer** or **null**
>Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have a hamming distance less than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!NOTE]
> With two, 40 phenotype target classes, a screen out larger than one can make the remaining space too small for a 200 digit background target class.

**"remove_avg_hamming_equal_or_less"** : **number** or **null**
> Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have an average hamming distance less than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!IMPORTANT]
> This parameter requires "removal_function_type" to be set to work.

**"remove_std_hamming_equal_or_greater"** : **number** or **null**
> Comparies the binary values of all possible background targets with the binary values of each phenotype of the primary targets and calculates the hamming distance. Removes all phenotypes that have a standard deviation of it's hamming distances greater than or equal to the value set here from becoming a background target. Set value to **null** to turn off feature. 

> [!NOTE]
> The max standard deviation for a 10 digit genotype is around 4.2.

> [!IMPORTANT]
> This parameter requires "removal_function_type" to be set to work.

**"removal_function_type"** : **string** ('percentage' or 'value')
> Allows **"remove_avg_hamming_equal_or_less"** and/or **"remove_std_hamming_equal_or_greater"** to function as a percentage of the range for that parameter or a flat value.

**"number_of_continuous_targets"** : **integer** 
> The number of targets to be created. This parameter is continous target class specific.

**"continuous_background_target_length"** : **integer** 
> The number of continuous digits in one target class. This parameter is continous target class specific.

<br/>
</details>

</details>

</details>

</details>



### Schedule List Parameters

<details>
<summary>See Parameters</summary>
<br/>

There are three categories of settings for each arranged schedule. There is the **"nondefault_schedule_generation_count"** (optional), the **"active_target_id_no"**, and the **"se_near_set"**.

**"nondefault_schedule_generation_count"** : **integer**
>This overrides the default number of generations in order to allow the schedule to have a different number of generations.

**"active_target_id_no"** : \{ **integer** : \{**reinforcement specifications**\} \}
>The active target id dictionary specificies which targets on the targets list are active during this schedule, based on the target id. The target id should be placed into the space labeled, **integer**. 

<details>
<summary>Reinforcement Specifications</summary>

**"reinforcement_rate_type"** : **string**
> The reinforcement type can be **'RI'** (random interval), **'RR'** (random ratio), **'FI'** (fixed interval), or **'FR'** (fixed ratio).
Only one reinforcement type can be used at one time, for each target.

**"reinforcement_rate"** : **value**
> The reinforcement rate is measured in generations. The random schedules are randomized using an exponential distribution.

**"reinforcer"** : **string**
> The reinforcer is term that is defined in the organism_settings>reinforcer_magnitude_data. In the reinforcer magnitude data, this string is linked to a value, which is it's reinforcer magnitude, or the mean of the linear density function. As shown in the example above, if the "reinforcer":"pellet", then "pellet" must be in the reinforcer_magnitude_data, in the form "pellet":40.  

</details>

<br/>

**"se_near_set"** : \[ **string\(s\)** \]
>the se_near_set is a list of names of stimulus elements, that will be present in the local environment during the schedule. The names of stimulus elements must correspond to the names of stimulus elements in the stimulus_environment_settings.

> [!IMPORTANT]
> This parameter is the only one that uses a list, so it's syntax is different from the typical dictionary syntax of the other parameters.

</details>


</details>
<br/>
<br/>

# Organism Settings

## Example

<details>
<summary>Example Organism Settings File</summary>

\{  

	"population_size":200,
	"number_of_binary_digits":10,
	"percent_replace":100,
	"mutation_rate":10,
	"reinforcer_magnitude_data":  

	{  

			"pellet":5,
			"scratch":40,
			"weak-pellet":60

	}  

\}

</details>

## Parameters

<details>
<summary>List of Parameters</summary>
<br/>

**"population_size"** : **integer**
> Population size sets the number of behaviors in the population. Typical default is 100 for most ETBD experiments. 200 behaviors or above is recommended for experiments that involve more than one stimulus elements.

**"number_of_binary_digits"** : **integer**
> This setting determines the number of digits in the genotype and the total range of the phenoype space. The number used in the standard experimental set up is 10, which creates a phenotype range of 1024. If the number of digits is 11, then the phenotype range would be 2048. 

**"percent_replace"** : **integer** (between 0 and 100)
> The value sets the default percentage of the behavior population that is replaced by new child behaviors. This can be modified by process settings during the experiment, like the selection modifier. 

**"mutation_rate"** : **integer**
> This value sets the percentage of the new child behaviors (created during recombination) that undergo mutation. 

**"reinforcer_magnitude_data"** : \{ **string** : **value** \}
> This setting is designed to mirror how an organism might value a particular kind of reinforcer. In the example settings above, the "pellet" is highly valued and consequently has a value of "5". The reinforcer magnitude data is linked to the experiment schedule settings through the **string** assigned here. The **value** is the mean of the selection densitiy function. The lower the reinforcer magnitude, the closer the parent behaviors (created during the selection step) will be to the emitted behavior.

</details>
<br/>
<br/>

# Procedure Settings

## Example

<details>
<summary>Example Procedure Settings File</summary>

{

	"observation_type":"observe5_low_entropy_x_percent",  
	"observation_entropy_percentage":2,  

	"emission_type":"random_emission",  

	"selection_loop_type":"all_se_viewed_w_se_modifier", 

	"selection_modifier_type":"power_function_entropy_modifier",  
	"selection_modifier_parameters":  

		{  
			"entropy_power_conversion_a":0.0625,  
			"entropy_power_conversion_b":2,  
			"selection_se_entropy_mod_lower_limit":0  
		},  
		
	"rewarded_selection_landscape_type":"circular_landscape",  
	"rewarded_parent_selection_type":"linear_roulette_function_njit", 	
	"linear_under_min_behaviors_selection_type":"random_fitness_simplifed_njit",  
	"linear_selection_min_behaviors":2,  

	"unrewarded_selection_landscape_type":"none", 	
	"unrewarded_parent_selection_type":"random_fitness_simplifed_njit",  
 
	"recombination_type":"bitwise_recombination_njit",  
	"mutation_type":"bitflip_by_individual_min1_every_x",  
	"mutation_modifier_parameters":  

		{  
        	"mutation_min_every_x_modifier":100  
		} 

}  

</details>

## Parameters

<details>
<summary>List of Parameters</summary>
<br/>

</details>
<br/>
<br/>

# Stimulus Environment Settings

## Example

<details>
<summary>Example Stimulus Environment Settings File</summary>

TBD

</details>

## Parameters

<details>
<summary>List of Parameters</summary>
<br/>

</details>
<br/>
