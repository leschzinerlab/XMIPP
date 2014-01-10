#!/bin/csh

# Requested queue
#$ -q himem.q

# Name of job
#$ -N ML3D

# Use openmpi parallel environment; set number of slots
#$ -pe orte 36

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

set num=$1

# The job

mpirun -np $NSLOTS xmipp_mpi_ml_refine3d -i subset_${num}.sel -vol filtered_reference.vol -iter 1 -o GenerateSeed_${num}/seeds_split_${num}

touch Generate_Seed_Done
