#!/bin/bash
#PBS -V
### Set the job name
#PBS -N newjob
### Email for messaging
#PBS -M pav@ornl.gov
### Node Spec, number of nodes and processors per node
#PBS -l nodes=1:ppn=32
### Tell PBS the anticipated run-time for your job, where walltime=HH:MM:S
#PBS -l walltime=00:10:0:0
### qos's available: std long burst level
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
/lustre/or-hydra/cades-bsd/pav/crux percolator --test-fdr 0.01 --train-fdr 0.01 --protein-report-duplicates T --protein-report-fragments T --search-input concatenated --overwrite T --output-dir percolator_test /lustre/or-hydra/cades-bsd/pav/ConcatPerc/tide-search.txt 
