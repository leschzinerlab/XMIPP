#!/bin/csh

# Requested queue
#$ -q barcelona.q

# Name of job
#$ -N ml_tomo

# Use openmpi parallel environment; set number of slots
#$ -pe orte 16

# Max walltime for this job is X minutes
#$ -l h_rt=144:00:00

# Merge the standard out and standard error to one file
##$ -j y

# Run job through csh shell
#$ -S /bin/csh

# Use current working directory
#$ -cwd

# Change to current working directory
cd $SGE_O_WORKDIR

# The following is for reporting only. It is not needed
# to run the job. It will show up in your output file.
echo "Job starting `date`"
echo "Current working directory: $cwd"
echo "Got $NSLOTS slots."

set input = $1

# The job

mpirun -np $NSLOTS xmipp_mpi_ml_tomo -i data.sel -o run1_align/nref1_15deg -nref 2 -doc data.doc -iter 20 -ang 20 -dim 40 -perturb --thr=$NSLOTS

touch "ml tomo is done"
