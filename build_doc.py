
#%%
# import modules
import pyodbc 
import os
import pandas as pd
import datetime
from pprint import pprint
import json

# import local classes
from class_structure import Viz
from topfive import TopFive
from doc import BuildDocument

'''
Iterate over places, run all visualization scripts, build documents. Includes
some basic run time tracking and try/except pairs to track what breaks without 
stopping.
'''

# empty dictionary to track run times
run_times = {}
bugs = []

for mission in focus_group:

    # start time for each mission
    start_time = datetime.datetime.now()

    print(f'\nFetching data, rendering visualizations, writing text, and building document for {place}. \n')

    # make an example folder if not already in existence
    if mission not in os.listdir('../test_examples'):
        os.mkdir(f'../test_examples/{place}')

    # run each visualization script, track runtimes
    viz_runtimes={}
    for script in [TopFive]: # most visualization scripts not included in this barebones version 
        
        print(f'\n\nRunning {script.__name__}.')
        # start time
        script_start_time = datetime.datetime.now()
        try:
            # run script
            script(place)
        except:
            bugs.append({'script': script, 'place': place})
            print(f'Failed to build {script} for {place}')

        # end time, append to dict
        script_end_time = datetime.datetime.now()
        duration = script_end_time - script_start_time
        duration = duration.total_seconds() 
        viz_runtimes[script.__name__] = duration

    # once all content is generated, build document
    try:
        BuildDocument(place)
    except:
        bugs.append({'script': 'BuildDocument', 'place': place})
        print(f'Failed to build document for {place}')

    # end time for mission, update runtime dict
    end_time = datetime.datetime.now()
    total_run = end_time - start_time
    total_run = total_run.total_seconds() 
    run_times[mission] = {'total_runtime': total_run, 
                        'viz_runtimes': viz_runtimes}

# print run times to console
pprint(run_times)

# write out run times
with open('temp_data/run_time_test.json', 'w') as f: 
    json.dump(run_times, f)

# write out list of bugs
pd.DataFrame(bugs).to_csv('temp_data/bugs.csv')
# %%
