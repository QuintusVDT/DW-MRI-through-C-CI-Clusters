# -*- coding: utf-8 -*-
"""

@author: DELINTE Nicolas

"""

import os
import json
import elikopy
import subprocess
import sys

home = os.path.realpath(__file__)
path_components = home.split(os.path.sep)  # Split the path using the separator appropriate for the platform

# Remove the last two components
new_path_components = path_components[:-2]
home = os.path.sep.join(new_path_components)
print(home)
root = home.replace("home", "globalscratch")
print(root)


n = sys.argv[1]

if n == "0":
  f_path=root + "/studies/study/"
  email = "rien@quedal.be"
  output_path = root + "/outfinal/"
else:
  f_path=root + f"/studies/study_{n}/"
  email = "rien@quedal.be"
  output_path = root + f"/out_{n}/"



if not os.path.exists(output_path):
  os.makedirs(output_path)
  print(f"succesfully created {output_path}")

study=elikopy.core.Elikopy(f_path, slurm=True, slurm_email='',cuda=False)

study.patient_list(f_path)
patient_list = os.listdir(root + "/NIFTI/")
#patient_list = ['IRM_100301_E0', 'IRM_100701_E1', 'IRM_101702_E2', 'IRM_101802_E0', 'IRM_101902_E0', 'IRM_102401_E2']












print(patient_list)


for Patient in patient_list:

    os.system('sbatch -J '+Patient +' ' + home + '/code/submitIter.sh '+Patient+" "+f_path +" "+email+" "+output_path)#+f"_{i}/"