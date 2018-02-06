#!/bin/bash

python $9/new_merge_script_Paul.py $1 $2 $3 
python $9/crux2moff_FileID_ConcatPerc.py $1 $2
python $9/moff_input.py $1 $4 $5 $6
python $9/psmToNormalizeFDR.py $1/MOFF_OUTPUT $2 $1 $7 $8
python $9/peptide_matrix_experiment_08_03.py $1
#python ${10}/peptide_unnormalize_protein_matrix.py $1 
