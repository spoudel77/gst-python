#!/bin/bash
#PBS -V
### Set the job name
#PBS -N newjob
### Email for messaging
#PBS -M pav@ornl.gov
### Node Spec, number of nodes and processors per node
### Tell PBS the anticipated run-time for your job, where walltime=HH:MM:S
#PBS -l walltime=1:00:0:0
### qos's available: std long burst devel
#PBS -l qos=std
## Account specifier, from the account specifier in moab accounts.dat
## we can list if needed. in this case cades-ccsi
#PBS -A bsd
### The ldap group list they need. In this case cades-user for burst
#PBS -W group_list=cades-bsd
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
source activate $9
python ${10}/Crux-Pipeline.py $1 $2 $3 
python ${10}/crux2moff.py $1 $2
python ${10}/moff_input.py $1 $4 $5 $6
python ${10}/psmToNormalizeFDR.py $1/MOFF_OUTPUT $2 $1 $7 $8
python ${10}/peptide_matrix_experiment.py $1
