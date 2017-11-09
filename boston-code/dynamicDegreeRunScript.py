#!/bin/bash


#PBS -N dynamicDegree
#PBS -l select=1:ncpus=20:mem=64gb,walltime=48:00:00


cd $PBS_O_WORKDIR


module add anaconda/2.3.0

python dynamicDegree.py 
