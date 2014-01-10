#!/bin/csh 
#$ -N ML2D
#$ -S /bin/tcsh
#$ -cwd
#$ -V
#$ -pe ompi 32

# The job

set input = $1
set refs = $2

mpirun -np $NSLOTS xmipp_mpi_ml_align2d -i $input -nref $refs -iter 40 -o RunML2D_phaseFlip2/ml2d -mirror
