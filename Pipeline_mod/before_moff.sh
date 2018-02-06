#!/bin/bash
#PBS -V
### Set the job name
#PBS -N newjob
### Email for messaging
#PBS -M pue@ornl.gov
### Node Spec, number of nodes and processors per node
### Tell PBS the anticipated run-time for your job, where walltime=HH:MM:S
#PBS -l walltime=1:00:0:0
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
source activate $2
#python ${10}/new_merge_script_Paul.py $1 $2 $3 
#python ${10}/crux2moff_FileID_ConcatPerc.py $1 $2
#python $9/moff_input.py $1 $3 $4 $5
#python $9/psmToNormalizeFDR.py $1/MOFF_OUTPUT $2 $1 $6 $7
python $3/peptide_matrix_experiment_08_03.py $1
#python ${10}/peptide_unnormalize_protein_matrix.py $1 
