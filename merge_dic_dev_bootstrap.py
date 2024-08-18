# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:24:28 2023

@author: DELINTE Nicolas
"""

import os
import sys
import json
import warnings
import numpy as np
import nibabel as nib
from unravel.utils import tensor_to_DTI, get_streamline_density
from unravel.core import (get_fixel_weight, get_microstructure_map,
                          get_weighted_mean, tensor_to_peak)
from unravel.analysis import get_metric_along_trajectory
from unravel.stream import extract_nodes, get_roi_sections_from_nodes

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from dipy.io.streamline import load_tractogram


def to_float64(val):
    """
    Used if *val* is an instance of numpy.float32.
    """

    return np.float64(val)
            
            
            
            
            
            
            
            
def merge_json_dics(folder_path, trajectory: bool = False,
                    method: str = 'ang', weighting: str = 'tsl'):

    merged_dict = {}
    
    # Iterate through files in the directory
    for name in os.listdir(folder_path):
      if "out_" in name:
        fille_path = os.path.join(folder_path, name)    
  
        # Iterate through files in the directory
        for filename in os.listdir(fille_path):
            file_path = os.path.join(fille_path, filename)
    
            # Check if the file is a JSON file
            if filename == "unravel_IRM_101001_E1_ang_tsl.json":
                if weighting in filename and method in filename:
                    if trajectory:
                        if 'trajectory' not in filename:
                            continue
                    else:
                        if 'trajectory' in filename:
                            continue
                    try:
                        with open(file_path, 'r') as file:
                            data = json.load(file)['Dev']
                            data = {name: data["IRM_101001_E1"]}
                            merged_dict.update(data)  # Merge dictionaries
                    except Exception as e:
                        print(f"Error reading file '{file_path}': {e}")

    if trajectory:
        dic_file = output_path + 'unravel_trajectory.json'
    else:
        dic_file = output_path + 'unravel_dev_bootstrap.json'
    json.dump(merged_dict, open(dic_file, 'w'), default=to_float64)

    return merged_dict





if __name__ == '__main__':



    method = 'ang'
    weighting = 'tsl'
    trajectory = False


    output_path = "/globalscratch/users/d/u/dujardin/"#sys.argv[4]


    #Merge dictionaries from JSON files in the folder
    merged_dictionary = merge_json_dics(output_path, trajectory=trajectory,
                                        method=method, weighting=weighting)
                                        
                                        
                                        
                                        
    