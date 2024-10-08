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
from unravel.utils import tensor_to_DTI, get_streamline_density, tract_to_ROI
from unravel.core import (get_fixel_weight, get_microstructure_map,
                          get_weighted_mean, tensor_to_peak, total_segment_length)
from unravel.analysis import get_metric_along_trajectory
from unravel.stream import extract_nodes, get_roi_sections_from_nodes


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from dipy.io.streamline import load_tractogram



def get_unique_filename(full_path):
    """
    Generate a unique filename by appending a number if the file already exists.
    Works with the full path provided as the argument.
    """
    directory, filename = os.path.split(full_path)
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{extension}"
        counter += 1
        
    return os.path.join(directory, new_filename)

def to_float64(val):
    """
    Used if *val* is an instance of numpy.float32.
    """

    return np.float64(val)

def has_nii_gz_file(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.nii.gz'):
            return True
    return False

def create_tensor_metrics(path: str):
    '''


    Parameters
    ----------
    path : str
        Ex: '/.../diamond/subjectName'

    Returns
    -------
    None.

    '''

    for tensor in ['t0', 't1']:

        img = nib.load(path + '_diamond_' + tensor + '.nii.gz')
        t = img.get_fdata()

        FA, AD, RD, MD = tensor_to_DTI(t)

        metric = {}
        metric['FA'] = FA
        metric['MD'] = MD
        metric['AD'] = AD
        metric['RD'] = RD

        for m in metric:
            out = nib.Nifti1Image(metric[m].real, img.affine)
            out.header.get_xyzt_units()
            out.to_filename(path + '_diamond_' + m + '_' + tensor + '.nii.gz')


def get_mean_tracts(trk_file: str, micro_path: str, trajectory: bool = False,
                    method: str = 'ang', weighting: str = 'tsl'):
    '''
    Return means for all metrics for a single patient using UNRAVEL

    Parameters
    ----------
    trk_file : str
        DESCRIPTION.
    micro_path : str
        Patient specific path to microstructure folder

    Returns
    -------
    mean : TYPE
        DESCRIPTION.
    dev : TYPE
        DESCRIPTION.

    '''

    trk = load_tractogram(trk_file, 'same')
    trk.to_vox()
    trk.to_corner()

    subject = micro_path.split('/')[-4]

    mean_dic = {}
    dev_dic = {}

    # Streamlines properties ---------------------
    """

    if trajectory:
        print(trk_file)
        point_array = extract_nodes(trk_file, level=3)
        roi_sections = get_roi_sections_from_nodes(trk_file, point_array)
    else:
        mean_dic['stream_count'] = len(trk.streamlines._offsets)
        dev_dic['stream_count'] = 0
        
    """
    if trajectory:
        point_array = extract_nodes(trk_file, level=3)
        roi_sections = get_roi_sections_from_nodes(trk_file, point_array)
        mean_dic['voxel_count'] = np.unique(roi_sections,
                                            return_counts=True)[1].tolist()
        dev_dic['voxel_count'] = 0
    else:
        mean_dic['stream_count'] = len(trk.streamlines._offsets)
        dev_dic['stream_count'] = 0
        mean_dic['voxel_count'] = np.sum(tract_to_ROI(trk_file))
        dev_dic['voxel_count'] = 0

    # DTI ----------------------------------

    metric_list = ['FA', 'AD', 'MD', 'RD']
    
    if os.path.exists(micro_path + 'dti/') and has_nii_gz_file(micro_path + 'dti/'):
    
        for m in metric_list:
    
            map_file = micro_path + 'dti/' + subject + '_' + m + '.nii.gz'
    
            metric_maps = nib.load(map_file).get_fdata()[..., np.newaxis]
    
            fixel_weights = get_streamline_density(trk)[..., np.newaxis]
    
            if trajectory:
                mean, dev = get_metric_along_trajectory(fixel_weights, metric_maps,
                                                        roi_sections,
                                                        weighting=weighting)
                mean = mean.tolist()
                dev = dev.tolist()
            else:
                microstructure_map = metric_maps[..., -1]
                mean, dev = get_weighted_mean(microstructure_map, fixel_weights,
                                              weighting=weighting)
    
            mean_dic[m+'_DTI'] = mean
            dev_dic[m+'_DTI'] = dev
            
    else: 
      for m in metric_list:
        mean_dic[m+'_DTI'] = 0
        dev_dic[m+'_DTI'] = 0
            
            
            
    # NODDI ----------------------------------

    metric_list = ['fextra', 'fintra', 'fiso', 'odi']
    
    if os.path.exists(micro_path + 'noddi/') and has_nii_gz_file(micro_path + 'noddi/'):
    
        for m in metric_list:
    
            map_file = micro_path + 'noddi/' + subject + "_noddi" + '_' + m + '.nii.gz'
    
            metric_maps = nib.load(map_file).get_fdata()[..., np.newaxis]
    
            fixel_weights = get_streamline_density(trk)[..., np.newaxis]
    
            if trajectory:
                mean, dev = get_metric_along_trajectory(fixel_weights, metric_maps,
                                                        roi_sections,
                                                        weighting=weighting)
                mean = mean.tolist()
                dev = dev.tolist()
            else:
                microstructure_map = metric_maps[..., -1]
                mean, dev = get_weighted_mean(microstructure_map, fixel_weights,
                                              weighting=weighting)
    
            mean_dic[m] = mean
            dev_dic[m] = dev
            
    else: 
      for m in metric_list:
        mean_dic[m] = 0
        dev_dic[m] = 0

    # Diamond ------------------------------
    
    metric_list = ['FA', 'MD', 'RD', 'AD']
    
    if os.path.exists(micro_path + 'diamond/') and has_nii_gz_file(micro_path + 'diamond/'):
    
        tensor_files = [micro_path + 'diamond/' + subject + '_diamond_t0.nii.gz',
                        micro_path + 'diamond/' + subject + '_diamond_t1.nii.gz']
    
        peaks = np.stack((tensor_to_peak(nib.load(tensor_files[0]).get_fdata()),
                          tensor_to_peak(nib.load(tensor_files[1]).get_fdata())),
                         axis=4)
    
        fixel_weights = get_fixel_weight(trk, peaks, method=method)
        tsl = total_segment_length(fixel_weights)
        n_eff = (np.sum(tsl)*np.sum(tsl))/np.sum(tsl*tsl)
        mean_dic["n"] = n_eff
        dev_dic["n"] = 0
        #modif
        hei = nib.load(micro_path + 'diamond/' + subject
                         + '_diamond_hei.nii.gz').get_fdata()
        metric_maps = np.stack((hei[:, :, :, 0, 0], hei[:, :, :, 0, 1]), axis=3)
    
        if trajectory:
            mean, dev = get_metric_along_trajectory(fixel_weights, metric_maps,
                                                    roi_sections,
                                                    weighting=weighting)
            mean = mean.tolist()
            dev = dev.tolist()
        else:
            microstructure_map = get_microstructure_map(fixel_weights, metric_maps)
            mean, dev = get_weighted_mean(microstructure_map, fixel_weights,
                                          weighting=weighting)
    
        mean_dic['hei'] = mean
        dev_dic['hei'] = dev
        
        #modif
    
        fracs = nib.load(micro_path + 'diamond/' + subject
                         + '_diamond_fractions.nii.gz').get_fdata()
        metric_maps = np.stack((fracs[:, :, :, 0, 0], fracs[:, :, :, 0, 1]), axis=3)
    
        if trajectory:
            mean, dev = get_metric_along_trajectory(fixel_weights, metric_maps,
                                                    roi_sections,
                                                    weighting=weighting)
            mean = mean.tolist()
            dev = dev.tolist()
        else:
            microstructure_map = get_microstructure_map(fixel_weights, metric_maps)
            mean, dev = get_weighted_mean(microstructure_map, fixel_weights,
                                          weighting=weighting)
    
        mean_dic['frac_dmd'] = mean
        dev_dic['frac_dmd'] = dev
    
        
    
        if not os.path.isfile(micro_path + 'diamond/' + subject
                              + '_diamond_FA_t0.nii.gz'):
    
            create_tensor_metrics(micro_path + 'diamond/' + subject)
    
        for m in metric_list:
    
            map_files = [micro_path + 'diamond/' + subject + '_diamond_' + m
                         + '_t0.nii.gz', micro_path + 'diamond/' + subject
                         + '_diamond_' + m + '_t1.nii.gz']
    
            metric_maps = np.stack((nib.load(map_files[0]).get_fdata(),
                                    nib.load(map_files[1]).get_fdata()),
                                   axis=3)
    
            if trajectory:
                mean, dev = get_metric_along_trajectory(fixel_weights, metric_maps,
                                                        roi_sections,
                                                        weighting=weighting)
                mean = mean.tolist()
                dev = dev.tolist()
            else:
                microstructure_map = get_microstructure_map(fixel_weights,
                                                            metric_maps)
                                                            
                # Create a NIfTI image
                nifti_img = nib.Nifti1Image(microstructure_map, nib.load(map_files[0]).affine)
                
                # Save the NIfTI image to a file
                
                #nib.save(nifti_img, output_path +  f'{subject}_{m}.nii.gz')
                mean, dev = get_weighted_mean(microstructure_map, fixel_weights,
                                              weighting=weighting)
    
            mean_dic[m] = mean
            dev_dic[m] = dev
            
    else:
      mean_dic['frac_dmd'] = 0
      dev_dic['frac_dmd'] = 0
      mean_dic['hei'] = 0
      dev_dic['hei'] = 0
      for m in metric_list:
        mean_dic[m] = 0
        dev_dic[m] = 0
      

    # Microstructure fingerprinting --------

    metric_list = ['fvf', 'frac', 'DIFF_ex']
    if os.path.exists(micro_path + 'mf/') and has_nii_gz_file(micro_path + 'mf/'):
    
        tensor_files = [micro_path + 'mf/' + subject + '_mf_peak_f0.nii.gz',
                        micro_path + 'mf/' + subject + '_mf_peak_f1.nii.gz']
    
        peaks = np.stack((nib.load(tensor_files[0]).get_fdata(),
                          nib.load(tensor_files[1]).get_fdata()),
                         axis=4)
    
        fixel_weights = get_fixel_weight(trk, peaks, method=method)
    
        
    
        for m in metric_list:
    
            map_files = [micro_path + 'mf/' + subject + '_mf_' + m + '_f0.nii.gz',
                         micro_path + 'mf/' + subject + '_mf_' + m + '_f1.nii.gz']
    
            metric_maps = np.stack((nib.load(map_files[0]).get_fdata(),
                                    nib.load(map_files[1]).get_fdata()),
                                   axis=3)
    
            if trajectory:
                mean, dev = get_metric_along_trajectory(fixel_weights, metric_maps,
                                                        roi_sections,
                                                        weighting=weighting)
                mean = mean.tolist()
                dev = dev.tolist()
            else:
                microstructure_map = get_microstructure_map(fixel_weights,
                                                            metric_maps)
                                                            
                # Create a NIfTI image
                nifti_img = nib.Nifti1Image(microstructure_map, nib.load(map_files[0]).affine)
                
                # Save the NIfTI image to a file
                #nib.save(nifti_img, output_path + f'{subject}_{m}.nii.gz')
                mean, dev = get_weighted_mean(microstructure_map, fixel_weights,
                                              weighting=weighting)
    
            mean_dic[m] = mean
            dev_dic[m] = dev
            
    else:
      for m in metric_list:
        mean_dic[m] = 0
        dev_dic[m] = 0
      

    return mean_dic, dev_dic


def get_mean_tracts_study(root: str, region_list: list,
                          output_path: str, subj_list: list = None,
                          trajectory: bool = False, method: str = 'ang',
                          weighting: str = 'tsl'):
    '''


    Parameters
    ----------
    root : str
        DESCRIPTION.
    selected_edges_path : str
        DESCRIPTION.

    Returns
    -------
    None.

    '''

    subjects_list = root + 'subjects/subj_list.json'

    if subj_list is None:
        with open(subjects_list, 'r') as read_file:
            subj_list = json.load(read_file)

    dic_tot = {}
    dic_tot['Mean'] = {}
    dic_tot['Dev'] = {}

    for sub in subj_list:

        micro_path = root + 'subjects/' + sub + '/dMRI/microstructure/'
        tract_path = root + 'subjects/' + sub + '/dMRI/tractography/tois/'

        dic_tot['Mean'][sub] = {}
        dic_tot['Dev'][sub] = {}

        eddy_qc_file = (root+'subjects/'+sub+'/dMRI/preproc/eddy/'+sub
                        + '_eddy_corr.qc/qc.json')

        if os.path.isfile(eddy_qc_file):
            print('File found for movement metrics')

            qc = json.load(open(eddy_qc_file))

            move = qc['qc_mot_rel']
            snr = qc['qc_cnr_avg'][0]

        for roi in region_list:

            try:
                trk_file = (tract_path + sub + '_' + roi + '.trk')

                mean_dic, dev_dic = get_mean_tracts(trk_file, micro_path,
                                                    trajectory=trajectory,
                                                    method=method,
                                                    weighting=weighting)

            except FileNotFoundError:
                print('.trk file or metrics not found for region ' + str(roi)
                      + ' in patient ' + sub + ' at '+trk_file)
                continue
            except IndexError:
                print('IndexError with subject ' + sub)
                continue
            except ValueError:
                print('Trajectory: Insufficient streamlines for region '
                      + str(roi) + ' in patient ' + sub)

            if os.path.isfile(eddy_qc_file):
                mean_dic['movement'] = move
                mean_dic['snr'] = snr

            dic_tot['Mean'][sub][roi] = mean_dic
            dic_tot['Dev'][sub][roi] = dev_dic

    if trajectory:
        dic_file = (output_path + 'unravel_trajectory_'+sub
                    + '_'+method+'_'+weighting+'.json')
    else:
        dic_file = output_path + 'unravel_'+sub+'_'+method+'_'+weighting+'.json'
    json.dump(dic_tot.copy(), open(dic_file, 'w'), default=to_float64)#+root[-3:-1]


def merge_json_dics(folder_path, trajectory: bool = False,
                    method: str = 'ang', weighting: str = 'tsl'):

    merged_dict = {}

    # Iterate through files in the directory
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the file is a JSON file
        if filename.endswith('.json'):
            if weighting in filename and method in filename:
                if trajectory:
                    if 'trajectory' not in filename:
                        continue
                else:
                    if 'trajectory' in filename:
                        continue
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)['Mean']
                        merged_dict.update(data)  # Merge dictionaries
                except Exception as e:
                    print(f"Error reading file '{file_path}': {e}")

    if trajectory:
        dic_file = output_path + 'unravel_trajectory.json'
    else:
        dic_file = output_path + 'unravel_mean.json'
    json.dump(merged_dict, open(dic_file, 'w'), default=to_float64)

    return merged_dict


if __name__ == '__main__':

    root = sys.argv[2]
    #root = "/globalscratch/users/d/u/dujardin/studies/study/"

    patient = sys.argv[1]
    #patient = "IRM_102202_E3"
    method = 'ang'
    weighting = 'tsl'#roi pondere par voxel et tsl par streamline
    trajectory = False


    region_list = ['cst_left', 'cst_right', 'cst_right_cross', 'cst_left_cross']

    output_path = sys.argv[4]
    #output_path = "/globalscratch/users/d/u/dujardin/out/"
    
    #output_path = get_unique_filename(output_path)
    
    #for i in range(21):
    #root = roott + f"studyr_{i}/"
    get_mean_tracts_study(root, region_list, output_path, subj_list=[patient],
                          trajectory=trajectory, method=method,
                          weighting=weighting)
    