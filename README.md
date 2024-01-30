# pyETBD-SST
created and maintained by Cyrus N. Chi

implemented in Python 3.7.11 

## Project Description
This project is a python-based version of Dr. J. J McDowell's Evolutionary Theory of Behavioral Dynamics (ETBD) that allows for the use of stimulus elements as discriminative stimuli. The stimulus elements are based on Estes' Stimulus Sampling Theory (SST). Use of only one stimulus element in the local environment allows the pyETBD-SST to perform identically to the basic computational ETBD.

Further discussion of the current state of this project can (eventually) be found in the Emory Thesis and Dissertation Repository, under the title, "Implementation of Discriminative Stimuli in the Evolutionary Theory of Behavior Dynamics"

## Table of Contents

1. [Abstract](https://github.com/CyrusChi/pyETBD-SST/edit/main/README.md#abstract)
2. [To run the program](https://github.com/CyrusChi/pyETBD-SST/edit/main/README.md#to-run-the-program)
3. [Current Task List](https://github.com/CyrusChi/pyETBD-SST/edit/main/README.md#current-task-list)

## Abstract

Implementation of Discriminative Stimuli in the Evolutionary Theory of Behavior Dynamics

By Cyrus N. Chi, M.S., M.A.

McDowell’s evolutionary theory of behavioral dynamics (ETBD) is a complexity theory that treats behaviors within an organism as ‘agents’ that interact with each other according to evolutionary principles. The theory has been used to animate artificial organisms (AOs) that produce behaviors that are considered the predictions of the theory. The theory’s predictions have been found to be congruent with a number of quantitative findings in environments with reinforcers and punishers. However, the theory as it currently exists does not have a paradigm for engaging with discriminative stimuli in the environment. In order to enhance the theory, elements of Estes’ stimulus sampling theory were adapted into a form compatible with the ETBD and added to the ETBD’s functional loop. AOs animated by the modified ETBD were tested in concurrent schedule, and multiple schedule environments. When AOs were found to not appropriately behave in a similar manner to live organisms, additional modifications based on behavioral principles (e.g. reinforcement based attention, background reinforcement) were added to improve AO functioning. The results show that the modified ETBD was able to replicate the previous finding on concurrent schedule behavior and predict learning based on discriminative stimuli, but not all features of live organism behavior was able to be reproduced with the modified ETBD described here. The principles that functioned well (e.g. entropy-based observation) and the additional principles deemed necessary (i.e. durability of learning, selectivity for stimuli) to model discriminative stimulus behavior are discussed.

Keywords: ETBD, Stimulus Sampling Theory, Stimulus Control, Complexity Theory



## To run the program
1. pip install the modules in [requirements.txt](requirements.txt)
2. Modify settings in inputs
3. Create a folder named 'outputs'
4. Run using the following line ('inputs/test' being the folder where the settings files are stored)
> **python3 main.py -s inputs/test**
6. Behavior data will be in outputs folder as excel files

> [!NOTE]
> This runs only one experiment at a time. A seperate batching method is needed in order to run multiple experiments. (TBD)


## Current Task List
- [x] Make experiment settings examples for the project's major components
- [ ] Write up instructions for how to set up parameters manually
- [ ] Make batch experiment file
- [ ] Make muti-processing a user setting
- [ ] Clean up code + add comments
- [ ] add the original response to low parent condition as a parameter
- [ ] add Entropy Observe all X percent
- [ ] add punishment
- [ ] add durability weights
- [ ] add selectivity function
 
