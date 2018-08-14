#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH -p physical
#SBATCH -o 1n1c.out
echo 'Run jobs on 1 node 1 core '
module load Python/3.4.3-goolf-2015a
mpiexec  python  post.py

