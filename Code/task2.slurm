#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=1
#SBATCH -p physical
#SBATCH -o 1n8c.out
echo 'Run jobs on 1 node 8 core '
module load Python/3.4.3-goolf-2015a
mpiexec  -n 8 python post.py

