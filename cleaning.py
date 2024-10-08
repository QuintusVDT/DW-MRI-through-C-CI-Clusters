import os
import shutil
import sys


def empty_directory(directory):
    try:
        # Recursively remove all files and directories within the specified directory
        for root, dirs, files in os.walk(directory, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))
        
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
        
        
        
patient =sys.argv[1]#'IRM_102401_E3' #
root = sys.argv[2]#"/globalscratch/users/d/u/dujardin/studies/"#
dicom_root = sys.argv[3]#"/globalscratch/users/d/u/dujardin/DICOM/"#sys.argv[3]
unzip_root = sys.argv[4]#"/globalscratch/users/d/u/dujardin/UNZIP/"#sys.argv[4]
niftii_root = sys.argv[5]#"/globalscratch/users/d/u/dujardin/NIFTI/"#sys.argv[5]


zipi = os.path.join(unzip_root, patient)
nift = os.path.join(niftii_root, patient)

empty_directory(zipi)
empty_directory(nift)