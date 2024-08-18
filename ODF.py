import elikopy
import json
import os
import sys

f_path=sys.argv[2]

study=elikopy.core.Elikopy(f_path, slurm=True, slurm_email=sys.argv[3],cuda=False)

patient_list=[sys.argv[1]]#study.patient_list(f_path)


study.odf_msmtcsd(patient_list_m=patient_list)
study.odf_csd(patient_list_m=patient_list)

#with open("/auto/home/users/d/u/dujardin/out_comparison/hello_world.txt", "a") as file:
#  file.write("odf" + sys.argv[1])