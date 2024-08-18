import elikopy
import json
import os
import sys

f_path=sys.argv[2]

study=elikopy.core.Elikopy(f_path, slurm=True, slurm_email='',cuda=False)

patient_list=[sys.argv[1]]
#[sys.argv[1]]#study.patient_list(f_path)

#with open("/auto/globalscratch/users/d/u/dujardin/out/hello_world.txt", "a") as file:
#  file.write("preproc" + sys.argv[0] + " " + sys.argv[1] + " "+ sys.argv[2] + " "+ sys.argv[3] + "\n")

study.preproc(eddy=True, denoising=True,reslice=False,gibbs=True,forceSynb0DisCo=True,topup=True,patient_list_m=patient_list,cpus=2)

