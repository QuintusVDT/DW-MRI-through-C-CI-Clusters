import os
import json
import numpy as np


def compute_global_stats(means, stds, ns):
    """
    Compute the global mean, standard deviation, and sample size given lists of means, standard deviations, and sample sizes.

    Parameters:
    means (list of float): List of means of the groups.
    stds (list of float): List of standard deviations of the groups.
    ns (list of int): List of sample sizes of the groups.

    Returns:
    tuple: global_mean (float), global_std (float), global_n (int)
    """
    
    # Convert input lists to numpy arrays for easier manipulation
    means = np.array(means)
    stds = np.array(stds)
    ns = np.array(ns)
    
    # Compute global sample size
    global_n = np.sum(ns)
    
    # Compute global mean
    global_mean = np.sum(ns * means) / global_n
    
    # Compute global variance
    sum_squares_within = np.sum((ns - 1) * (stds ** 2))
    sum_squares_between = np.sum(ns * (means - global_mean) ** 2)
    global_variance = (sum_squares_within + sum_squares_between) / (global_n - 1)
    
    # Compute global standard deviation
    global_std = np.sqrt(global_variance)
    
    return global_mean, global_std, global_n

def to_float64(val):
    """
    Used if *val* is an instance of numpy.float32.
    """

    return np.float64(val)


mean_file = "/globalscratch/users/d/u/dujardin/unravel_mean.json"
dev_file = "/globalscratch/users/d/u/dujardin/unravel_dev.json"

root = "/globalscratch/users/d/u/dujardin/"

out_list = [root + "out"]
for i in range(1, 6):
  out_list.append(root + f"out_{i}")
  
print(out_list)

metrics = ["stream_count", "voxel_count", "FA_DTI", "AD_DTI", "MD_DTI", "RD_DTI", "fextra", "fintra", "fiso", "odi", "n", "frac_dmd", "hei", "FA", "MD", "RD", "AD", "fvf", "frac", "DIFF_ex", "movement", "snr"]
cotes = ["cst_left", "cst_right", "cst_left_cross", "cst_right_cross"]

patient_list = os.listdir("/globalscratch/users/d/u/dujardin/NIFTI/")

#mean

mean_dic = {}
dev_dic = {}

for patient in patient_list:
  data = {patient : {}}
  data1 = {patient : {}}
  mean_dic.update(data)
  dev_dic.update(data1)
  for cote in cotes:
    data = {cote : {}}
    data1 = {cote : {}}
    mean_dic[patient].update(data)
    dev_dic[patient].update(data1)
    for metric in metrics:
      data = {metric : 0}
      data1 = {metric : 0}
      mean_dic[patient][cote].update(data)
      dev_dic[patient][cote].update(data1)
      
 
 
metrics = ["movement", "snr", "stream_count", "voxel_count", "FA_DTI", "AD_DTI", "MD_DTI", "RD_DTI", "fextra", "fintra", "fiso", "odi", "frac_dmd", "hei", "FA", "MD", "RD", "AD", "fvf", "frac", "DIFF_ex"]     
      
for patient in patient_list:
  for cote in cotes:
    for metric in metrics:
      m = []
      s = []
      n = []
      for out in out_list:
        with open(out + "/unravel_mean.json", 'r') as file:
          u_mean = json.load(file)
        with open(out + "/unravel_dev.json", 'r') as file:
          u_dev = json.load(file)
          
        if patient in u_mean.keys():
          if cote in u_mean[patient].keys():
            if metric in u_mean[patient][cote].keys():
              if metric in u_dev[patient][cote].keys():
                m.append(u_mean[patient][cote][metric])
                s.append(u_dev[patient][cote][metric])
                n.append(u_mean[patient][cote]["n"])
              else:
                m.append(u_mean[patient][cote][metric])
                s.append(0)
                n.append(1)
              
        
      #global_mean, global_std, global_n = compute_global_stats(m, s, n)
      mean_dic[patient][cote][metric] = m
      mean_dic[patient][cote]["n"] = n
      dev_dic[patient][cote][metric] = s
      

json.dump(mean_dic, open(root + "unravel_mean_merged.json", 'w'), default=to_float64)
json.dump(dev_dic, open(root + "unravel_dev_merged.json", 'w'), default=to_float64)      
      

print(mean_dic)









