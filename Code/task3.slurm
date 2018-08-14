#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH -p physical
#SBATCH -o 2n8c.out
echo 'Run jobs on 2 node 8 core '
module load Python/3.4.3-goolf-2015a
mpiexec  python  post.py