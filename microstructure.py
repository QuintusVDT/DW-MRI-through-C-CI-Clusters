import elikopy
import json
import os
import sys

f_path=sys.argv[2]

study=elikopy.core.Elikopy(f_path, slurm=True, slurm_email=sys.argv[3],cuda=False)

patient_list=[sys.argv[1]]#study.patient_list(f_path)

study.dti(patient_list_m=patient_list)
study.noddi(patient_list_m=patient_list,slurm_timeout="20:00:00")
study.diamond(patient_list_m=patient_list,customDiamond=" --ntensors 2 --automose aicu --fascicle diamondcyl --waterfraction 1 --waterDiff 0.003 --verbose 1 --log")


#with open("/auto/home/users/d/u/dujardin/out_comparison/hello_world.txt", "a") as file:
#  file.write("micro" + sys.argv[1])