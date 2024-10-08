import os
import shutil
import subprocess
              



def empty_directory(directory):
    try:
        # Recursively remove all files and directories within the specified directory
        for root, dirs, files in os.walk(directory, topdown=False):
            for filee in files:
                os.remove(os.path.join(root, filee))
            for dire in dirs:
                shutil.rmtree(os.path.join(root, dire))
        
        # Check if the directory is empty
        if not os.listdir(directory):
            print(f"Directory '{directory}' emptied successfully.")
        else:
            print(f"Directory '{directory}' is not empty.")
        
        # Check permission to delete files
        test_file = os.path.join(directory, ".test_file")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        print("Permission to delete files: Yes")
        
    except PermissionError:
        print("Permission denied to delete files.")
    except Exception as e:
        print(f"Error occurred: {e}")
              
              
def create_directory(directory):
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist. Creating it.")
        makedirs(directory)
    else:
        print(f"Directory '{directory}' already exists.")
        # Optionally, create a new directory within the existing directory
        new_directory = os.path.join(directory, "new_directory")
        if not os.path.exists(new_directory):
            print(f"Creating a new directory '{new_directory}'.")
            makedirs(new_directory)
        else:
            print(f"New directory '{new_directory}' already exists.")
            
    return directory + "/"
        
        
        
        
def list_subdirectories(directory):
    subdirectories = []
    # List all files and directories in the specified directory
    for item in os.listdir(directory):
        item = item.replace(".zip", "")
        subdirectories.append(item)
    return subdirectories


if __name__ == "__main__":



    home = os.path.realpath(__file__)
    path_components = home.split(os.path.sep)  # Split the path using the separator appropriate for the platform

    # Remove the last two components
    new_path_components = path_components[:-2]
    home = os.path.sep.join(new_path_components)
    print(home)
    globalscratch = home.replace("home", "globalscratch")
    print(globalscratch)


    root = globalscratch + "/studies/"
    dicom_root = globalscratch + "/DICOM/"
    unzip_root = globalscratch + "/UNZIP/"
    niftii_root = globalscratch + "/NIFTI/"
    out = globalscratch + "/out/"
    empti = False
    
    
    if not os.path.exists(root):
      os.makedirs(root)
    elif empti:
      empty_directory(root)
      
    if not os.path.exists(unzip_root):
      os.makedirs(unzip_root)
    elif empti:
      empty_directory(unzip_root)
      
    if not os.path.exists(niftii_root):
      os.makedirs(niftii_root)
    elif empti:
      empty_directory(niftii_root)
      
    if not os.path.exists(out):
      os.makedirs(out)
    elif empti:
      empty_directory(out)
      
    print(dicom_root) 
    if not os.path.exists(dicom_root):
      print("DICOM file missing")
    
    
    for filename in os.listdir(dicom_root):
        # Check if the file is a zip file
        if filename.endswith(".zip"):
            # Construct the full path to the file
            old_name = os.path.join(dicom_root, filename)
            
            base_name, _ = os.path.splitext(filename)
            
            # Generate the new base name by replacing "T" with "E" and removing all other dots
            new_base_name = base_name.replace("T", "E").replace(".", "").replace("zip", "")
            
            # Ensure the new base name ends with ".zip"
            if not new_base_name.endswith(".zip"):
                new_base_name += ".zip"
            
            # Construct the full path for the new name
            new_name = os.path.join(dicom_root, new_base_name)
            
            # Rename the file
            os.rename(old_name, new_name)
            print(f"Renamed '{old_name}' to '{new_name}'")
    
    patient_list=list_subdirectories(dicom_root)
    patient_list = ['IRM_000000_E0']
    #patient_list = ["IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1",     "IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1", "IRM_101001_E1"]
    #patient_list = [s.replace(".", "").replace("T", "E") for s in patient_dicom]
    print(patient_list)
    study_path = root + "study/"
    if not os.path.exists(study_path):
      os.makedirs(study_path)
    elif empti:
      empty_directory(study_path)
  

    print("study directory")
    if not os.path.exists(study_path + "/data_1"):
      os.makedirs(study_path + "/data_1")
    elif empti:
      empty_directory(study_path + "/data_1")
      
    if not os.path.exists(study_path + "/T1"):
      os.makedirs(study_path + "/T1")
    elif empti:
      empty_directory(study_path + "/T1")
      
    if not os.path.exists(study_path + "/T2"):
      os.makedirs(study_path + "/T2")
    elif empti:
      empty_directory(study_path + "/T2")
      
    if not os.path.exists(study_path + "/subjects"):
      os.makedirs(study_path + "/subjects")
      
    
      
      
    print("all subdirectories")
      
    
    for patient in patient_list:#patients directory 
        print(patient)
        if not os.path.exists(study_path + "/subjects/" + patient):
          os.makedirs(study_path + "/subjects/" + patient)
        if not os.path.exists(niftii_root + "/" + patient):
          os.makedirs(niftii_root + "/" + patient)
        if not os.path.exists(unzip_root + "/" + patient):
          os.makedirs(unzip_root + "/" + patient)
        
        
    print("patient directories")

    for patient in patient_list:
      os.system('sbatch -J '+patient+' code/conversion.sh ' + patient+" "+root+" "+dicom_root+" "+unzip_root+" "+niftii_root+" "+study_path)

      