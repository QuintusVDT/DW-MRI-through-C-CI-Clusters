import numpy as np
import nibabel as nb
import os


metrics = ["FA", "MD", "AD", "RD"]

for metric in metrics:

    # Assuming file_paths is a list of paths to your NIfTI files
    file_paths = []
    
    for i in range(0, 21):
      if os.path.exists(f"/globalscratch/users/d/u/dujardin/studies/studyr_{i}/subjects/IRM_101001_E1/dMRI/microstructure/diamond/IRM_101001_E1_diamond_{metric}_t0.nii.gz"):
        file_paths.append(f"/globalscratch/users/d/u/dujardin/studies/studyr_{i}/subjects/IRM_101001_E1/dMRI/microstructure/diamond/IRM_101001_E1_diamond_{metric}_t0.nii.gz")
      if os.path.exists(f"/globalscratch/users/d/u/dujardin/studies/studyr_{i}/subjects/IRM_101001_E1/dMRI/microstructure/diamond/IRM_101001_E1_diamond_{metric}_t1.nii.gz"):
        file_paths.append(f"/globalscratch/users/d/u/dujardin/studies/studyr_{i}/subjects/IRM_101001_E1/dMRI/microstructure/diamond/IRM_101001_E1_diamond_{metric}_t1.nii.gz")
      
    
    
    
    # Load all images
    images = [nb.load(fp) for fp in file_paths]
    
    # Get dimensions of the images
    dims = images[0].shape
    
    # Initialize an empty array to hold the voxel values
    voxel_values = np.empty((len(images), dims[0], dims[1], dims[2]))
    
    # Fill the voxel_values array with data from each image
    for i, img in enumerate(images):
        #voxel_values[i] = np.asarray(img.dataobj)
        voxel_values[i] = img.get_fdata()
        
        
    print("max: ", np.max(voxel_values))
    
    # Initialize arrays to store non-null voxel indices and their values
    non_null_indices = []
    non_null_values = []
    
    # Find non-null voxels across all slices
    for x in range(dims[0]):
        for y in range(dims[1]):
            for z in range(dims[2]):
                if np.any(voxel_values[:, x, y, z] != 0):
                    non_null_indices.append((x, y, z))
                    non_null_values.append(voxel_values[:, x, y, z])
    
    # Convert lists to NumPy arrays
    non_null_indices = np.array(non_null_indices)
    non_null_values = np.array(non_null_values)
    
    # Reshape non_null_values to match the structure of non_null_indices
    non_null_values = non_null_values.reshape(-1, len(file_paths))
    
    ndims = non_null_values.shape
    print("dim: ", ndims)
    n = ndims[0]*ndims[1]
    
    # Compute standard deviation for each voxel
    std_dev = np.std(non_null_values, axis=1)
    
    # Compute mean for each voxel
    mean = np.mean(non_null_values, axis=1)
    
    # Compute coefficient of variation (CV) for each voxel
    cv = std_dev / mean
    
    
    
    
    #print("std: ", std_dev)
    
    std_mean = np.mean(std_dev)
    CV = np.mean(cv)
    std_std = np.std(std_dev)
    print(metric)
    print("mean of std: ", std_mean)
    print("std of std: ", std_std)
    print("n: ", n)
    print("CV: ", CV)
    
    # Save the result as a new NIfTI image
    #std_dev_img = nb.Nifti1Image(std_dev[..., np.newaxis], images[0].affine)
    #nb.save(std_dev_img, f'/globalscratch/users/d/u/dujardin/out/standard_deviation_{metric}_DTI.nii.gz')
