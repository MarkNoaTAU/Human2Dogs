#!/bin/bash
#SBATCH --job-name=noa_train_rf
#SBATCH --output=noa_train_rf.out
#SBATCH --error=noa_train_rf.err
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=5
#SBATCH --mem-per-cpu=16gb
#SBATCH --nodes=1
#SBATCH --open-mode=truncate
#SBATCH --export=NONE
#SBATCH --get-user-env=60L
#SBATCH --mail-user=marknoa1995@gmail.com
#SBATCH --mail-type=END
#SBATCH --signal=USR1@120 # how to end job when time’s up


# clear all loaded modules
module purge

# to load the latest version of Python
module load Python

# initialize the Python virtual environment
source noa_h2d/bin/activate

# check the Python version (useful for debugging)
python3 --version
# print the location of Python3 executable binary (also useful for debugging)
which python3

# run the Python command or in this case some custom Python script
/groups/umcg-lifelines/tmp01/projects/ov22_0666/personal_directories/noamark/Human2Dogs/noa_h2d/bin/python3 train_rf_v0.py
