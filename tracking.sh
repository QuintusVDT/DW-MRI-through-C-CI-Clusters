#!/bin/bash
#
#SBATCH --job-name=$1
#
#SBATCH --ntasks=2
#SBATCH --time=8:00:00
#SBATCH --mem-per-cpu=20000
#SBATCH --mail-type='FAIL'
#SBATCH --mail-user=''

#SBATCH --output='$HOME/out/out.out'
#SBATCH --error='$HOME/out/out.err'

python $HOME/code/temp_tracking_from_rois.py $1 $2 $3 $4
python $HOME/code/OE_unravel.py $1 $2 $3 $4
python $HOME/code/merge_dic.py $1 $2 $3 $4
