# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 19:23:18 2022

@author: Cyrus


#Run Experiment_Runner

"""
if __name__ == '__main__':
    import time
    import glob
    import argparse
    from pathlib import Path
    from Experiment_Module import Experiment_Runner

    #Define command line arguments
    parser = argparse.ArgumentParser(description='"python3.8 main.py -s C:/Users/mbassi/Documents/Cyrus/SST_ETBD_09_04_22/SST-ETBD Code/inputs " Setting file folder')
    parser.add_argument("-s", "--settingsFolder", dest="settingsFolder", required=True, help="the settingsFolder")
     #parse command line arguments
    args = parser.parse_args()
    
    starttime = time.time()
    #settings_folder = str(Path("C:/Users/mbassi/Documents/Cyrus/SST_ETBD_09_04_22/SST-ETBD Code/inputs"))
    settings_folder = str(Path(args.settingsFolder))
    setting_files = glob.glob(settings_folder + "/*settings*.json")
    a = Experiment_Runner(setting_files)
    endtime = time.time()
    print("runtime = {} seconds".format(endtime - starttime))
    # data_folder = Path("C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/SST-ETBD Code/inputs")
    # file_to_open = data_folder / "experiment_2_2_1.json"
    # a = Experiment_Runner(file_to_open)







