# pyETBD-SST
created and maintained by Cyrus N. Chi

implemented in Python 3.7.11 

## Project Description
This project is a python-based version of Dr. J. J McDowell's Evolutionary Theory of Behavioral Dynamics (ETBD) that allows for the use of stimulus elements as discriminative stimuli. The stimulus elements are based on Estes' Stimulus Sampling Theory (SST). Use of only one stimulus element in the local environment allows the pyETBD-SST to perform identically to the basic computational ETBD.

Further discussion of the current state of this project can (eventually) be found in the Emory Thesis and Dissertation Repository, under the title, "Implementation of Discriminative Stimuli in the Evolutionary Theory of Behavior Dynamics"

## Table of Contents

1. [Abstract](https://github.com/CyrusChi/pyETBD-SST/edit/main/README.md#abstract)
2. [Creating Setting Instructions](https://github.com/CyrusChi/pyETBD-SST/edit/main/README.md#creating-settings-instructions) 
3. [To run the program](https://github.com/CyrusChi/pyETBD-SST/edit/main/README.md#to-run-the-program)
4. [Current Task List](https://github.com/CyrusChi/pyETBD-SST/edit/main/README.md#current-task-list)
5. [References](https://github.com/CyrusChi/pyETBD-SST/edit/main/README.md#references)

## Abstract

Implementation of Discriminative Stimuli in the Evolutionary Theory of Behavior Dynamics

By Cyrus N. Chi, M.S., M.A.

McDowell’s evolutionary theory of behavioral dynamics (ETBD) is a complexity theory that treats behaviors within an organism as ‘agents’ that interact with each other according to evolutionary principles. The theory has been used to animate artificial organisms (AOs) that produce behaviors that are considered the predictions of the theory. The theory’s predictions have been found to be congruent with a number of quantitative findings in environments with reinforcers and punishers. However, the theory as it currently exists does not have a paradigm for engaging with discriminative stimuli in the environment. In order to enhance the theory, elements of Estes’ stimulus sampling theory were adapted into a form compatible with the ETBD and added to the ETBD’s functional loop. AOs animated by the modified ETBD were tested in concurrent schedule, and multiple schedule environments. When AOs were found to not appropriately behave in a similar manner to live organisms, additional modifications based on behavioral principles (e.g. reinforcement based attention, background reinforcement) were added to improve AO functioning. The results show that the modified ETBD was able to replicate the previous finding on concurrent schedule behavior and predict learning based on discriminative stimuli, but not all features of live organism behavior was able to be reproduced with the modified ETBD described here. The principles that functioned well (e.g. entropy-based observation) and the additional principles deemed necessary (i.e. durability of learning, selectivity for stimuli) to model discriminative stimulus behavior are discussed.

Keywords: ETBD, Stimulus Sampling Theory, Stimulus Control, Complexity Theory

## Creating Settings Instructions

### See [instructions](settings_instructions.md) for how to set up or modify settings.


### Example settings can be found in the inputs folder for the following experiments:

<details>
<summary>See Experiments</summary>
<br/>

1. RI RI Concurrent Schedules based on McDowell et al., 2008 
    
    with only neutral one stimulus element
    >Folder: concurrent_se1_2008_rep

2. RI RI Concurrent Schedules based on McDowell et al., 2008 

    with neutral 10 stimulus elements, 2% entropy-based observation, and 200 behavior population
    >Folder: concurrent_se10_en02

3. Multiple schedules with alternating RI 70 and Extinction, 
    
    with 5 red, 5 green, and 5 wall (i.e. neutral) stimuli, background reinforcement uses a RI 20, with 200 background targets
    >Folder: mult_sched_se_r5g5w5_bk_ri20

4. Multiple schedules with alternating RI 70 and Extinction, 

    with 10 red, 10 green, and 0 wall (i.e. neutral) stimuli, background reinforcement uses a RI 20, with 200 background targets
    >Folder: mult_sched_se_r10g10w0_bk_ri20

5. Stimulus Gradient Experiments based on Guttman and Kalish 1956, 

    with 5 red, 5 green, and 5 wall (i.e. neutral) stimuli, background reinforcement uses a RI 10, population mutation rate of 100
    >Folder: stim_gradient_x_wall_x_bkgd_ri10_rm05_mmr100

6. Stimulus Gradient Experiments based on Guttman and Kalish 1956, 
    
    with 10 red, 10 green, and 0 wall (i.e. neutral) stimuli, no background reinforcement, population mutation rate of 100
    >Folder: stim_gradient_y_wall_y_bkgd_ri10_rm05_mmr100

</details>

## To run the program

### Download and run on a desktop
1. download project files
2. pip install the modules in [requirements.txt](requirements.txt)
3. Modify or create new settings in inputs
4. Create a folder named 'outputs'
5. Run using the following line ('inputs/test' being an example of a folder where the settings files are stored)
> **python3 main.py -s inputs/test**
6. Behavior data will be in outputs folder as CSV files

> [!NOTE]
> This runs only one experiment at a time. A seperate batching method is needed in order to run multiple experiments. (TBD)

### Running the program in github (TBD)


## Current Task List
- [x] Make experiment settings examples for the project's major components
- [ ] Write up instructions for how to set up parameters manually
- [ ] Make muti-processing a user setting
- [ ] Make batch experiment file
- [ ] Clean up code + add comments
- [ ] add the original response to low parent condition as a parameter
- [ ] add Entropy Observe all X percent
- [ ] add punishment
- [ ] add durability weights
- [ ] add selectivity function

### References

McDowell, J. J (2004). A computational model of selection by consequences. Journal of the Experimental Analysis of Behavior, 81(3), 297-317. [https://doi.org/10.1901/jeab.2004.81-297](https://doi.org/10.1901/jeab.2004.81-297)

McDowell, J. J (2019), On the current status of the evolutionary theory of behavior dynamics. Journal of the Experimental Analysis of Behavior, 111: 130-145. [https://doi.org/10.1002/jeab.495](https://doi.org/10.1002/jeab.495)
 
