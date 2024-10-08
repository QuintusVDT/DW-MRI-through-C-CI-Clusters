import sys
import os
import shutil
import zipfile
import pydicom



def unzip_file(zip_file, extract_to):
    print(zip_file)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        
        
        
def conversion(filename, out):
    os.system('dcm2niix ' +
              '-f %f_%d_%t ' +
              '-b y ' +
              '-d 9 ' +
              '-p n ' +
              '-z y ' +
              '-ba y ' +
              '-w 2 ' +
              '-o ' + out + " " +
              filename + '/')
              
              
def contains_dicom_files(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            try:
                with pydicom.dcmread(filepath):
                    return True
            except pydicom.errors.InvalidDicomError:
                pass
    return False
              
   
   
def splitext_with_multiple_periods(filename, max_periods=1):
    """
    Splits the filename into name and extension, considering multiple periods.
    
    Parameters:
    - filename: The original filename.
    - max_periods: The maximum number of periods to consider as separators.
    
    Returns:
    - A tuple containing the name and the extension(s).
    """
    # Split the filename by periods, considering the max_periods parameter
    parts = filename.split('.', max_periods)
    
    # Join the last part(s) with a period to form the extension(s)
    extension = '.'.join(parts[-max_periods:])
    
    # Join the remaining parts to form the name
    name = '.'.join(parts[:-max_periods])
    
    return name, extension
    
               
              
def rename(old_name, new_name):
    try:
        # Split the file name and extension
        file_name, file_extension = splitext_with_multiple_periods(old_name)
        
        if 'nii.gz' in file_extension:
          file_extension = 'nii.gz'
          
        if 'json' in file_extension:
          file_extension = 'json'
          
        if 'bval' in file_extension:
          file_extension = 'bval'
          
        if 'bvec' in file_extension:
          file_extension = 'bvec'
        
        print(file_name)
        print(file_extension)
        
        # Concatenate the new name with the original extension
        new_file_name = new_name + file_extension
        
        # Rename the file
        os.rename(old_name, new_file_name)
        
        print(f"File '{old_name}' renamed to '{new_file_name}' successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")





def move_file(source, destination):
    try:
        shutil.move(source, destination)
        print(f"File moved successfully from '{source}' to '{destination}'.")
    except Exception as e:
        print(f"Error occurred: {e}")



patient =sys.argv[1]#'IRM_102401_E3' #sys.argv[1]#
root = sys.argv[2]#"/globalscratch/users/d/u/dujardin/studies/"#sys.argv[2]#
dicom_root = sys.argv[3]#"/globalscratch/users/d/u/dujardin/DICOM/"#sys.argv[3]#
unzip_root = sys.argv[4]#"/globalscratch/users/d/u/dujardin/UNZIP/"#sys.argv[4]#
niftii_root = sys.argv[5]#"/globalscratch/users/d/u/dujardin/NIFTI/"#sys.argv[5]#
study_path = sys.argv[6]#root + "/study/"#sys.argv[6]#




unzip_file(dicom_root + patient + ".zip", unzip_root + "/" + patient + "/")
with open(study_path + "/log.txt", "a") as file:
  file.write(patient + " unzip" + "\n")

        

p = os.listdir(unzip_root + patient + "/export/home1/sdc_image_pool/images/")[0]
p = os.path.join(unzip_root + patient + "/export/home1/sdc_image_pool/images/", p)
e = os.listdir(p)[0]
e = os.path.join(p, e)

conversion(e, niftii_root + patient)


#for root, dirs, files in os.walk(unzip_root + patient):
#    for direc in dirs:
#        file_path = os.path.join(root, direc)
#        if os.path.isdir(file_path) and contains_dicom_files(file_path):
#            conversion(file_path, niftii_root + patient)


DTI_files = []
DTI_size = []

fichiers = os.listdir(niftii_root + "/" + patient)
for fichier in fichiers:
    if 'T1' in fichier:
        move_file(niftii_root + patient + "/" + fichier, study_path + "/T1")
        rename(study_path + "/T1/" + fichier, study_path + "/T1/" + patient + "_T1.") 
        
    elif 'T2' in fichier:
        move_file(niftii_root + patient + "/" + fichier, study_path + "/T2")
        rename(study_path + "/T2/" + fichier, study_path + "/T2/" + patient + "_T2.")
        
    elif 'DTI' in fichier:
        DTI_files.append(fichier)
        DTI_size.append(os.path.getsize(niftii_root + patient + "/" + fichier))
        
        
print(DTI_files)
print(DTI_size)

with open(study_path + "/log.txt", "a") as file:
  file.write(patient + " list: ")
  for fichier in DTI_files:
    file.write(fichier)
    
  file.write("\n")
    
index_max_size = DTI_size.index(max(DTI_size)) 
nom, _ = DTI_files[index_max_size].split('.', 1)
print(nom)

a = 'a' in nom
b = 'b' in nom


print("a est ", str(a), " pour ", DTI_files[index_max_size] , " de taille ", index_max_size)
print("b est ", str(b), " pour ", DTI_files[index_max_size] , " de taille ", index_max_size)



for fichier in DTI_files:
    file_name, file_extension = fichier.split('.', 1)
    if 'a' in file_name:
      if a:
        move_file(niftii_root + patient + "/" + fichier, study_path + "/data_1")
        rename(study_path + "/data_1/" + fichier, study_path + "/data_1/" + patient + ".")
        
    elif 'b' in file_name:
      if b:
        move_file(niftii_root + patient + "/" + fichier, study_path + "/data_1")
        rename(study_path + "/data_1/" + fichier, study_path + "/data_1/" + patient + ".")
        
        
    elif not 'a' in file_name and not 'b' in file_name:
      if not a and not b:
        move_file(niftii_root + patient + "/" + fichier, study_path + "/data_1")
        rename(study_path + "/data_1/" + fichier, study_path + "/data_1/" + patient + ".")
        


""" 
directory = study_path + "T1"
for t in os.listdir(directory):
  print(t)
  parts = t.split(".")
  if len(parts) > 3:
    new_name = parts[0] + "." + parts[2] + "." +parts[3]
    
  elif len(parts) > 2:
    new_name = parts[0] + "." + parts[2]
    
  elif len(parts) > 1:
    new_name = parts[0] + "." + parts[1]
    
  else:
    new_name = part[0]
    

  new_path = os.path.join(directory, new_name)
  os.rename(os.path.join(directory, t), new_path)
  print(t, " changed to ", new_name)
  
  
  
directory = study_path + "T2"
for t in os.listdir(directory):
  print(t)
  parts = t.split(".")
  if len(parts) > 3:
    new_name = parts[0] + "." + parts[2] + "." +parts[3]
    
  elif len(parts) > 2:
    new_name = parts[0] + "." + parts[2]
    
  elif len(parts) > 1:
    new_name = parts[0] + "." + parts[1]
    
  else:
    new_name = part[0]
    

  new_path = os.path.join(directory, new_name)
  os.rename(os.path.join(directory, t), new_path)
  print(t, " changed to ", new_name)
      
"""