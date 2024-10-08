import sys
import json
import nibabel as nib
from dipy.io.streamline import load_tractogram, save_tractogram
from dipy.io.stateful_tractogram import Space, StatefulTractogram
from regis.core import find_transform, apply_transform
from unravel.stream import extract_nodes, remove_outlier_streamlines
import numpy as np
import subprocess
import os

patient = "IRM_100302_E1"

home = "/home/users/d/u/dujardin/"
root = "/globalscratch/users/d/u/dujardin/studies/study/"
glob = "/globalscratch/users/d/u/dujardin/"
patient_list = os.listdir(glob + "/NIFTI/")


for patient in patient_list:

  if patient != "IRM_100301_E0":
    
    fa_path = (root + '/subjects/' + patient + '/dMRI/microstructure/dti/' + patient + '_FA.nii.gz')
    mni_fa_path = home + "/atlas/FSL_HCP1065_FA_1mm.nii.gz"
    #mni_fa_path = root+'subjects/'+patient + \
    #      '/dMRI/ODF/MSMT-CSD/'+patient+'_MSMT-CSD_WM_ODF.nii.gz'
    static_mask_path = (root + '/subjects/' + patient + '/masks/' + patient
                            + '_brain_mask.nii.gz')
    rois_path = home + "/atlas_rois/"
    roi_path = "cst_4_right.nii.gz"
    
    
    static_mask = nib.load(static_mask_path).get_fdata()
    
    map_mni_to_subj = find_transform(mni_fa_path, fa_path, hard_static_mask=static_mask, only_affine=True)
    
    for roi_path in os.listdir(rois_path):
      transformed = apply_transform(rois_path+roi_path, map_mni_to_subj, static_file=fa_path, binary=True, binary_thresh=0.25)
      score = np.count_nonzero(transformed)
      if score == 0:
        print(patient)
        print(roi_path)                     
                        
                        