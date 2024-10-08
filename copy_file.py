import os
import shutil

def copytree_overwrite(src, dst):
    # If the destination directory exists, remove it
    if os.path.exists(dst):
        shutil.rmtree(dst)
    
    # Copy the source directory to the destination
    shutil.copytree(src, dst)

def copy_subdirectory(src_dir, des_dir, num_copies):
    """
    Copies a subdirectory and its contents, appending a number to the name of each new copy.
    
    :param src_dir: The path of the subdirectory to be copied.
    :param num_copies: The number of copies to be made.
    """
    if not os.path.isdir(src_dir):
        raise ValueError(f"The source directory '{src_dir}' does not exist or is not a directory.")
    
    # Get the parent directory and the name of the source directory
    parent_dir = os.path.dirname(src_dir)
    base_name = os.path.basename(src_dir)
    base_name = base_name[:-2]
    print(base_name)
    
    for i in range(1, num_copies):
        new_dir_name = f"{base_name}_{i}/"
        new_dir_path = os.path.join(des_dir, new_dir_name)
        
        # Copy the directory
        shutil.copytree(src_dir, new_dir_path)
        print(f"Copied {src_dir} to {new_dir_path}")

# Example usage:
#copy_subdirectory('/globalscratch/users/d/u/dujardin/studies/studyr', 20)

#for i in range(21, 51):
copy_subdirectory("/globalscratch/users/d/u/dujardin/studies/study_0", f"/globalscratch/users/d/u/dujardin/studies/", 6)
#shutil.rmtree(f"/globalscratch/users/d/u/dujardin/studies/studyr_{i}/subjects/IRM_101001_E2/dMRI/tractography/")

