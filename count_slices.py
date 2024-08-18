import numpy as np
import nibabel as nib
import os


home = os.path.realpath(__file__)
path_components = home.split(os.path.sep)  # Split the path using the separator appropriate for the platform
# Remove the last two components
new_path_components = path_components[:-2]
home = os.path.sep.join(new_path_components)
root = home.replace("home", "globalscratch")

f_path=root + "/studies/study/"

patients = ['IRM_101502_E0', 'IRM_101401_E3', 'IRM_100801_E3', 'IRM_100902_E0', 'IRM_102101_E3', 'IRM_101602_E1', 'IRM_102202_E2', 'IRM_101201_E1', 'IRM_100401_E3', 'IRM_102401_E0', 'IRM_101902_E0', 'IRM_100802_E3', 'IRM_101702_E2', 'IRM_102102_E3', 'IRM_101502_E3', 'IRM_101401_E0', 'IRM_100302_E1', 'IRM_100201_E2', 'IRM_100402_E0', 'IRM_101301_E1', 'IRM_101802_E0', 'IRM_100801_E0', 'IRM_101602_E2', 'IRM_101701_E1', 'IRM_102101_E0', 'IRM_101001_E0', 'IRM_102401_E3', 'IRM_100401_E0', 'IRM_102202_E1', 'IRM_101501_E3', 'IRM_100301_E1', 'IRM_100901_E3', 'IRM_100701_E1', 'IRM_102102_E0', 'IRM_101902_E1', 'IRM_102102_E2', 'IRM_100701_E3', 'IRM_102202_E3', 'IRM_100202_E0', 'IRM_100301_E3', 'IRM_100401_E2', 'IRM_101201_E0', 'IRM_100801_E2', 'IRM_101901_E1', 'IRM_101802_E2', 'IRM_101001_E2', 'IRM_100101_E1', 'IRM_101602_E0', 'IRM_100402_E2', 'IRM_101202_E0', 'IRM_101301_E3', 'IRM_101502_E1', 'IRM_101401_E2', 'IRM_101702_E0', 'IRM_100102_E2', 'IRM_100401_E1', 'IRM_102401_E2', 'IRM_101501_E2', 'IRM_102202_E0', 'IRM_101901_E2', 'IRM_101802_E1', 'IRM_100801_E1', 'IRM_102101_E1', 'IRM_102002_E2', 'IRM_100101_E2', 'IRM_101001_E1', 'IRM_100302_E0', 'IRM_100201_E3', 'IRM_101401_E1', 'IRM_101202_E3', 'IRM_101301_E0']

for patient in patients:
  
  img = nib.load(f_path + "/data_1/" + patient + ".nii.gz")
  sh = np.shape(img)
  if sh[2] != 68:
    print(patient + ": ", sh)