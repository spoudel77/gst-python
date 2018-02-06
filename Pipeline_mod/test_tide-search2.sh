#!/bin/bash
#PBS -V
### Set the job name
#PBS -N newjob
### Email for messaging
#PBS -M pav@ornl.gov
### Node Spec, number of nodes and processors per node
#PBS -l nodes=1:ppn=32
### Tell PBS the anticipated run-time for your job, where walltime=HH:MM:S
#PBS -l walltime=00:03:0:0
### qos's available: std long burst level
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
source activate $9
/lustre/or-hydra/cades-bsd/pav/crux tide-search --compute-sp T --concat T --precursor-window 10.0 --precursor-window-type ppm --output-dir tide-search_test /lustre/or-hydra/cades-bsd/pav/Easy_nLC_5uL_EP04_StageTip_AC30cm_Rep1_01.mzML /lustre/or-hydra/cades-bsd/pav/Easy_nLC_5uL_EP04_StageTip_AC30cm_Rep2_01.mzML /lustre/or-hydra/cades-bsd/pav/Easy_nLC_5uL_EP04_StageTip_AC30cm_Rep3_01.mzML /lustre/or-hydra/cades-bsd/pav/Kfedtschenkoi_382_v1dot1_chloro_mito_CRAPs_nobreaks_FR.fasta
