import elikopy
import json
import os
import sys
import subprocess

def has_nii_gz_file(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.nii.gz'):
            return True
    return False

f_path=sys.argv[2]

study=elikopy.core.Elikopy(f_path, slurm=True, slurm_email=sys.argv[3],cuda=False)

patient_list=[sys.argv[1]]#study.patient_list(f_path)

home = os.path.realpath(__file__)
path_components = home.split(os.path.sep)  # Split the path using the separator appropriate for the platform
# Remove the last two components
new_path_components = path_components[:-2]
home = os.path.sep.join(new_path_components)

#if not has_nii_gz_file(f_path + "/subjects/" + sys.argv[1] + "/dMRI/microstructure/mf"):
study.fingerprinting(dictionary_path=home+'/Dictionaries/fixed_rad_dist_wide.mat',peaksType='MSMT-CSD',patient_list_m=patient_list)
#study.tracking(patient_list_m=patient_list, folder_path=f_path, streamline_number=500000, max_angle=20)

#with open("/auto/home/users/d/u/dujardin/out_comparison/hello_world.txt", "a") as file:
#  file.write("mf" + sys.argv[1])