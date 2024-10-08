# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 09:48:12 2023

@author: DELINTE Nicolas
"""


import os
import sys
import json
import nibabel as nib
from dipy.io.streamline import load_tractogram, save_tractogram
from dipy.io.stateful_tractogram import Space, StatefulTractogram
from regis.core import find_transform, apply_transform
from unravel.stream import extract_nodes, remove_outlier_streamlines
import numpy as np
import subprocess


def register_rois_to_subj(fa_path: str, rois_path: str, mni_fa_path: str,
                          output_path: str, static_mask_path: str):
    '''
    Two-step registration to obtain label in the diffusion space.

    Parameters
    ----------
    fa_path : str
        Path to FA file.
    roi_path : str
        DESCRIPTION.
    mni_fa_path : str
        DESCRIPTION.
    output_path : str
        DESCRIPTION.

    Returns
    -------
    None.

    '''

    static_mask = nib.load(static_mask_path).get_fdata()

    map_mni_to_subj = find_transform(mni_fa_path, fa_path,
                                     hard_static_mask=static_mask)

    for roi_path in os.listdir(rois_path):

        output_filename = output_path+roi_path.split('/')[-1]

        apply_transform(rois_path+roi_path, map_mni_to_subj,
                        static_file=fa_path,
                        output_path=output_filename, binary=True,
                        binary_thresh=0.25)


def tract_to_trk(input_file: str, space_file: str):
    '''


    Parameters
    ----------
    input_file : str
        DESCRIPTION.
    output_file : str
        DESCRIPTION.

    Returns
    -------
    None.

    '''

    tract = load_tractogram(input_file, space_file)

    sft_reg = StatefulTractogram(tract.streamlines, nib.load(space_file),
                                 Space.RASMM)

    save_tractogram(sft_reg, input_file[:-3]+'trk', bbox_valid_check=False)

    # save_trk(tract, input_file[:-3]+'trk')


def tracking(patient: str, root: str, roi: str, side=None,
             number: int = 1000, angle: int = 15, num_rois: int = 4,
             max_length: int = 200, max_attempts: int = 2000,
             cutoff: float = 0.1, cross: bool = False):

    fod_file = root+'subjects/'+patient + \
        '/dMRI/ODF/MSMT-CSD/'+patient+'_MSMT-CSD_WM_ODF.nii.gz'
    if cross:
        tck_file = (root+'subjects/'+patient+'/dMRI/tractography/tois/' +
                    patient+'_'+region+'_'+side+'_cross.tck')
    else:
        tck_file = (root+'subjects/'+patient+'/dMRI/tractography/tois/' +
                    patient+'_'+region+'_'+side+'.tck')

    if not os.path.isdir(root+'/subjects/'+patient+'/dMRI/tractography/tois/'):
        os.mkdir(root+'/subjects/'+patient+'/dMRI/tractography/tois/')

    if side == 'center':
        seed_file = output_roi_path+region+'.nii.gz'
        include1_file = output_roi_path+'cc_right.nii.gz'
        include2_file = output_roi_path+'cc_left.nii.gz'
    elif side is not None:
        if side == 'left':
            other_side='right'
        else:
            other_side='left'        
        
        seed_file = output_roi_path+region+'_1_'+side+'.nii.gz'
        include1_file = output_roi_path+region+'_2_'+side+'.nii.gz'
        include2_file = output_roi_path+region+'_3_'+side+'.nii.gz'
        exclude2_file = output_roi_path+region+'_3_'+other_side+'.nii.gz'
        if cross:
          include3_file = output_roi_path+region+'_4_'+other_side+'.nii.gz'
          exclude3_file = output_roi_path+region+'_4_'+side+'.nii.gz'

        else:
          include3_file = output_roi_path+region+'_4_'+side+'.nii.gz'
          exclude3_file = output_roi_path+region+'_4_'+other_side+'.nii.gz'
        
    params = {'fod': 'msmt-CSD', 'algo': 'IFOD2', 'number': number,
              'angle': angle}

    if num_rois == 2:

        os.system('tckgen ' +
                  fod_file + ' ' +
                  tck_file + ' ' +
                  # '-act '+tt_file + ' ' +
                  # '-seed_gmwmi '+seed_file + ' ' +
                  # '-backtrack ' +
                  # '-crop_at_gmwmi ' +
                  '-include '+include1_file + ' ' +
                  '-seed_image '+seed_file + ' ' +
                  '-max_attempts_per_seed ' + str(max_attempts) + ' ' +
                  #'-seed ' + str(max_attempts*select) + ' ' +
                  '-cutoff '+str(cutoff)+' ' +
                  '-maxlength ' + str(max_length) + ' ' +
                  '-select '+str(number)+' ' +
                  '-angle '+str(angle)+' -force')#seed instead of max_attempts_per_seed#'-max_attempts_per_seed ' + str(max_attempts) + ' ' +
                  
                  
    elif num_rois == 3:

        os.system('tckgen ' +
                  fod_file + ' ' +
                  tck_file + ' ' +
                  # '-act '+tt_file + ' ' +
                  # '-seed_gmwmi '+seed_file + ' ' +
                  # '-backtrack ' +
                  # '-crop_at_gmwmi ' +
                  '-include '+include1_file + ' ' +
                  '-include '+include2_file + ' ' +
                  '-exclude '+exclude2_file + ' ' +
                  '-seed_image '+seed_file + ' ' +
                  '-max_attempts_per_seed ' + str(max_attempts) + ' ' +
                  #'-seed ' + str(max_attempts*select) + ' ' +
                  '-cutoff '+str(cutoff)+' ' +
                  '-maxlength ' + str(max_length) + ' ' +
                  '-select '+str(number)+' ' +
                  '-angle '+str(angle)+' -force')
    else:
        os.system('tckgen ' +
                  fod_file + ' ' +
                  tck_file + ' ' +
                  # '-act '+tt_file + ' ' +
                  # '-seed_gmwmi '+seed_file + ' ' +
                  # '-backtrack ' +
                  # '-crop_at_gmwmi ' +
                  '-include '+include1_file + ' ' +
                  '-include '+include2_file + ' ' +
                  '-include '+include3_file + ' ' +
                  '-exclude '+exclude2_file + ' ' +
                  '-exclude '+exclude3_file + ' ' +
                  '-seed_image '+seed_file + ' ' +
                  '-max_attempts_per_seed ' + str(max_attempts) + ' ' +
                  #'-seed ' + str(max_attempts*select) + ' ' +
                  '-cutoff '+str(cutoff)+' ' +
                  '-maxlength ' + str(max_length) + ' ' +
                  '-select '+str(number)+' ' +
                  '-angle '+str(angle)+' -force')

    tract_to_trk(tck_file, fod_file)

    trk_file = tck_file[:-4]+'.trk'
    try:
        point_array = extract_nodes(trk_file)
        remove_outlier_streamlines(trk_file, point_array, outlier_ratio=0)
    except:
        print('No streamlines removed due to insufficient streamlines')

    with open(tck_file[:-4]+'.txt', 'w') as outfile:
        json.dump(params, outfile)


if __name__ == '__main__':

    home = os.path.realpath(__file__)
    path_components = home.split(os.path.sep)  # Split the path using the separator appropriate for the platform
    # Remove the last two components
    new_path_components = path_components[:-2]
    home = os.path.sep.join(new_path_components)
    less_roi = False

    root = sys.argv[2]
    patient = sys.argv[1]

    fa_path = (root + '/subjects/' + patient + '/dMRI/microstructure/dti/'
               + patient + '_FA.nii.gz')
    mni_fa_path = home + "/atlas/FSL_HCP1065_FA_1mm.nii.gz"
    rois_path = home + "/atlas_rois/"
    static_mask_path = (root + '/subjects/' + patient + '/masks/' + patient
                        + '_brain_mask.nii.gz')

    output_roi_path = root + '/subjects/' + patient + '/dMRI/tractography/rois/'
    
    


    if not os.path.exists(root + '/subjects/' + patient + '/dMRI/tractography/'):
        os.mkdir(root + '/subjects/' + patient + '/dMRI/tractography/')

    if not os.path.exists(output_roi_path):
        os.mkdir(output_roi_path)
        
  
    #register_rois_to_subj(fa_path, rois_path, mni_fa_path, output_roi_path,
    #                      static_mask_path)
  
    # ARC -------------------------------
    img = nib.load(root + "/data_1/" + patient + ".nii.gz")
    sh = np.shape(img)
    print("dimension: ", sh)
    for region in ['cst']:
        # For 42 slices -----------------------------------
        
        if np.min(sh[:3]) < 50:
          print("Patient ", patient, " uses 42 slices")
          tracking(patient, root, roi=region, side='left', num_rois=2, angle=15,
                   number=2000, max_attempts=3000, cutoff=0.08)
          tracking(patient, root, roi=region, side='right', num_rois=2, angle=15,
                   number=2000, max_attempts=3000, cutoff=0.08)
          tracking(patient, root, roi=region, side='left', num_rois=2, angle=15,
                   number=2000, max_attempts=3000, cutoff=0.08, cross=True)
          tracking(patient, root, roi=region, side='right', num_rois=2, angle=15,
                   number=2000, max_attempts=3000, cutoff=0.08, cross=True)
                   
        elif less_roi:
          tracking(patient, root, roi=region, side='left', num_rois=3, angle=15,
                   number=2000, max_attempts=3000, cutoff=0.08)
          tracking(patient, root, roi=region, side='right', num_rois=3, angle=15,
                   number=2000, max_attempts=3000, cutoff=0.08)
          tracking(patient, root, roi=region, side='left', num_rois=3, angle=15,
                   number=2000, max_attempts=3000, cutoff=0.08, cross=True)
          tracking(patient, root, roi=region, side='right', num_rois=3, angle=15,
                   number=2000, max_attempts=3000, cutoff=0.08, cross=True)

        # Else -----------------------------------------------
        else:
          tracking(patient, root, roi=region, side='left', angle=15,
                   number=2000, max_attempts=3000, cutoff=0.08)
          tracking(patient, root, roi=region, side='right', angle=15,
                   number=2000, max_attempts=3000, cutoff=0.08)
          tracking(patient, root, roi=region, side='left', angle=15,
                   number=2000, max_attempts=3000, cutoff=0.08, cross=True)
          tracking(patient, root, roi=region, side='right', angle=15,
                   number=2000, max_attempts=3000, cutoff=0.08, cross=True)
                   
                   
                   
