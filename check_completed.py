import os
import numpy as np
import subprocess
import platform
import sys


def has_nii_gz_file(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.nii.gz'):
            return True
    return False




home = os.path.realpath(__file__)
path_components = home.split(os.path.sep)  # Split the path using the separator appropriate for the platform

# Remove the last two components
new_path_components = path_components[:-2]
home = os.path.sep.join(new_path_components)
globalscratch = home.replace("home", "globalscratch")

if sys.argv[1] == "0":
  study_root = globalscratch + "/studies/study/"
else:
  study_root = globalscratch + "/studies/study_" + sys.argv[1]

subject_root = study_root + "/subjects/"

patient_list = [name for name in os.listdir(subject_root) if os.path.isdir(os.path.join(subject_root, name))]
patient_list.sort()
check = np.zeros((len(patient_list), 10), dtype=int)

i = 0

for patient in patient_list:

  if os.path.exists(subject_root + patient + "/dMRI/"):
    dmri = subject_root + patient + "/dMRI/"
    folders = [name for name in os.listdir(dmri) if os.path.isdir(os.path.join(dmri, name))]
  else:
    dmri = ''
    folders = ''
    
  
  if 'preproc' in folders:
    preproc = dmri + "/preproc/"
    direc = os.listdir(preproc)
    if 'bet' in direc and has_nii_gz_file(preproc + '/bet') and 'eddy' in direc and has_nii_gz_file(preproc + '/eddy') and 'gibbs' in direc and has_nii_gz_file(preproc + '/gibbs') and        'mppca' in direc and has_nii_gz_file(preproc + '/mppca') and 'quality_control' in direc:
  
      check[i][0] = 1
      
  if 'microstructure' in folders:
    micro = dmri + "/microstructure"
    direc = os.listdir(micro)
    if 'dti' in direc and has_nii_gz_file(micro + "/dti"):
      check[i][1] = 1
    if 'diamond' in direc and has_nii_gz_file(micro + "/diamond"):
      check[i][2] = 1
    if 'noddi' in direc and has_nii_gz_file(micro + "/noddi"):
      check[i][3] = 1
    if 'mf' in direc and has_nii_gz_file(micro + "/mf"):
      check[i][4] = 1
  
  if 'ODF' in folders:
    micro = dmri + "/ODF"
    direc = os.listdir(micro)
    if 'CSD' in direc and has_nii_gz_file(micro + "/CSD"):
      check[i][5] = 1
    if 'MSMT-CSD' in direc and has_nii_gz_file(micro + "/MSMT-CSD"):
      check[i][6] = 1
      
      
  if 'tractography' in folders:
    micro = dmri + "/tractography"
    direc = os.listdir(micro)
    if 'rois' in direc and has_nii_gz_file(micro + "/rois") and 'tois' in direc and len(os.listdir(micro + "/tois")) > 0:
      check[i][7] = 1
      
  if os.path.exists(study_root + "data_1/" + patient + ".nii.gz") and os.path.exists(study_root + "data_1/" + patient + ".bvec") and os.path.exists(study_root + "data_1/" + patient + ".bval") and os.path.exists(study_root + "data_1/" + patient + ".json") and os.path.exists(study_root + "T1/" + patient + "_T1.json") and os.path.exists(study_root + "T1/" + patient + "_T1.nii.gz"):# and os.path.exists(study_root + "T2/" + patient + "_T2.json") and os.path.exists(study_root + "T2/" + patient + "_T2.nii.gz"):
    check[i][9] = 1
    
    
  out = globalscratch + "/out/"
  folders = os.listdir(out)
  for f in folders:
    if 'unravel' in f and patient in f and '.json' in f:
      check[i][8] = 1
    
    
      
  i+=1

file_path = globalscratch + "/out/check.txt"

#os.remove(file_path)
with open(file_path, "w") as file:
  file.write("             " + " prep" + " dti " + " diam"  + " nodd"+ "  mf " + " CSD "+ " MSMC" + " trac" + " unrav" + "    conversion" + "\n")
  i = 0
  for patient in patient_list:
    file.write(patient + "  " + str(check[i][0]) + "  " + "  " + str(check[i][1]) + "  " + "  " + str(check[i][2]) + "  " + "  " + str(check[i][3]) + "  " + "  " + str(check[i][4]) + "  " + "  " + str(check[i][5]) + "  " + "  " + str(check[i][6]) + "  " + "  " + str(check[i][7]) + "    " + str(check[i][8]) + "            "  + str(check[i][9]) + "\n")
    i +=1 
  

file.close()

system = platform.system()
if system == 'Windows':
    subprocess.run(['start', '', file_path], shell=True)
elif system == 'Darwin':  # macOS
    subprocess.run(['open', file_path])
else:  # Linux and other systems
    subprocess.run(['nano', '-w', file_path])

redo = []
i = 0
for patient in patient_list:
  if check[i][4] == 0:
    redo.append(patient)
  i+=1
    
    
print(redo)
  