import dipy.io.gradients as dipigrad
import os


path = "/globalscratch/users/d/u/dujardin/studies/study/data_1/"


bval_path = []
bvec_path = []

for files in os.listdir(path):

  # Replace 'path_to_bval_file' and 'path_to_bvec_file' with the actual paths to your files
  if ".bval" in files:
    bval_path.append(os.path.join(path, files))
  if ".bvec" in files:
    bvec_path.append(os.path.join(path, files))
    
    
for i in range(0, min(len(bval_path), len(bvec_path))):
  
  # Read the b-values and b-vectors
  bvals, bvecs = dipigrad.read_bvals_bvecs(bval_path[i], bvec_path[i])
  
  # Count the number of b-values and vectors
  num_bvalues = len(bvals)
  num_vectors = len(bvecs)
  
  print(f"Number of b-values: {num_bvalues}")
  print(f"Number of vectors: {num_vectors}")
