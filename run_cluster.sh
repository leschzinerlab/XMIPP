#!/bin/csh 
#$ -N ML2D
#$ -S /bin/tcsh
#$ -cwd
#$ -V
#$ -pe ompi 39

mpirun -np 39 xmipp_mpi_ml_align2d -i data.sel -nref 40 -iter 40 -o RunML2D/ml2d -fast --mirror
