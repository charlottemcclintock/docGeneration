
# import modules
import pyodbc 
import pandas as pd 
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import os
import json

# import local classes
from topfive import TopFive
from doc import BuildDocument

for place_name in ['Place1', 'Place2']:

    # set place
    place = place_name

    # make an example folder if not already in existence
    if mission not in os.listdir('../test_examples'):
        os.mkdir(f'../test_examples/{[place}')

    # run visualization scripts
    topfive = TopFive([place=place)
    doc = BuildDocument(place=place)

# %%
