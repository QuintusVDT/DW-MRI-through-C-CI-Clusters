# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 23:17:22 2024

@author: quent
"""

from unravel.utils import fuse_trk
import sys
import os
import shutil

home = os.path.realpath(__file__)
path_components = home.split(os.path.sep)  # Split the path using the separator appropriate for the platform

new_path_components = path_components[:-2]
home = os.path.sep.join(new_path_components)
print(home)
root = home.replace("home", "globalscratch")
print(root)

tracto_folder = "/globalscratch/users/d/u/dujardin/studies/tractography/"

patient_list = os.listdir(root + "/NIFTI/")

#patient = sys.argv[1]


for patient in patient_list:
  try:
  
    toi = f"/globalscratch/users/d/u/dujardin/studies/study/subjects/{patient}/dMRI/tractography/tois/{patient}_fused.trk"
  
    shutil.copy(toi, tracto_folder)
    """
    fuse_trk(f"/globalscratch/users/d/u/dujardin/studies/study/subjects/{patient}/dMRI/tractography/tois/{patient}_cst_right_cross.trk", f"/globalscratch/users/d/u/dujardin/studies/study/subjects/{patient}/dMRI/tractography/tois/{patient}_cst_right.trk", f"/globalscratch/users/d/u/dujardin/studies/study/subjects/{patient}/dMRI/tractography/tois/{patient}_right_fused.trk")
    fuse_trk(f"/globalscratch/users/d/u/dujardin/studies/study/subjects/{patient}/dMRI/tractography/tois/{patient}_cst_left_cross.trk", f"/globalscratch/users/d/u/dujardin/studies/study/subjects/{patient}/dMRI/tractography/tois/{patient}_cst_left.trk", f"/globalscratch/users/d/u/dujardin/studies/study/subjects/{patient}/dMRI/tractography/tois/{patient}_left_fused.trk")
    fuse_trk(f"/globalscratch/users/d/u/dujardin/studies/study/subjects/{patient}/dMRI/tractography/tois/{patient}_right_fused.trk", f"/globalscratch/users/d/u/dujardin/studies/study/subjects/{patient}/dMRI/tractography/tois/{patient}_left_fused.trk", f"/globalscratch/users/d/u/dujardin/studies/study/subjects/{patient}/dMRI/tractography/tois/{patient}_fused.trk")
  """  
  except Exception as e:
    print(f"{patient} encountered {e}")

