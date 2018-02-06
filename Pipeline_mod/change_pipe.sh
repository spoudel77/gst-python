#!/bin/bash
#PBS -V
### Set the job name
#PBS -N newjob
### Email for messaging
#PBS -M poudels@ornl.gov
### Node Spec, number of nodes and processors per node
###Two nodes and 32 cores per node in this case
###PBS -l nodes=2:ppn=32
### Tell PBS the anticipated run-time for your job, where walltime=HH:MM:S
#PBS -l walltime=00:10:20:0
### qos's available: std long burst devel
#PBS -l qos=burst
## Account specifier, from the account specifier in moab accounts.dat
## we can list if needed. in this case cades-ccsi
#PBS -A bsd-burst
### The ldap group list they need. In this case cades-user for burst
#PBS -W group_list=cades-user
### Base queueing stuff
### Switch to the working directory
cd $PBS_O_WORKDIR
pwd 
# Calculate the number of processors allocated to this run.
NPROCS=`wc -l < $PBS_NODEFILE`
# Calculate the number of nodes allocated.
NNODES=`uniq $PBS_NODEFILE | wc -l`
### Display the job context
module purge
module load python/2.7.12
module load gcc/5.3.0
module load anaconda2
source activate $5
#source activate spoudel
python $1/psmToNormalizeFDR.py $1/MOFF_OUTPUT $2 $1 $3 $4
python $1/peptide_matrix_experiment_08_03.py $1
