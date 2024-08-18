#!/bin/bash
#
#SBATCH --job-name=$1
#
#SBATCH --mem-per-cpu=20000
#SBATCH --time=4:00:00
#SBATCH --mail-type='FAIL'
#SBATCH --mail-user=''

#SBATCH --output='$HOME/out/out_conv.out'
#SBATCH --error='$HOME/out/out_conv.err'


python $HOME/code/cleaning.py $1 $2 $3 $4 $5 $6
python $HOME/code/conversion.py $1 $2 $3 $4 $5 $6