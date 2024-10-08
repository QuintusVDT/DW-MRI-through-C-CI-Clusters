import nibabel as nib
import numpy as np

m = "frac"
subject = "IRM_100302_E1"

# Run the command and capture its output
#subprocess.run("mkdir -p $HOME/coucou", shell=True, capture_output=True, text=True)
map_files = [f"/globalscratch/users/d/u/dujardin/studies/study/subjects/IRM_100302_E1/dMRI/microstructure/diamond/IRM_100302_E1_{m}_t0.nii.gz", f"/globalscratch/users/d/u/dujardin/studies/study/subjects/IRM_100302_E1/dMRI/microstructure/diamond/IRM_100302_E1_{m}_t1.nii.gz"]


img1 = nib.load(map_files[0]).get_fdata()
print(np.shape(img1))
print(img1[55, 55, 34])
img2 = nib.load(map_files[1]).get_fdata()
print(np.shape(img2))
print(img2[55, 55, 34])

#img2 = nib.load(map_files[1]).get_fdata()
img3 = img1 + img2

sh = np.shape(img3)
print(sh)



# Create a NIfTI image
nifti_img = nib.Nifti1Image(img3, nib.load(map_files[0]).affine)

# Save the NIfTI image to a file

nib.save(nifti_img, f'/globalscratch/users/d/u/dujardin/studies/study/subjects/IRM_100302_E1/dMRI/microstructure/diamond/{subject}_diamond_{m}_t0t1.nii.gz')
