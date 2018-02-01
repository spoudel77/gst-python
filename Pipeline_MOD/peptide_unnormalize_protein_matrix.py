from pandas import *
import numpy as np
import sys

cruxDir = sys.argv[1]
ou1 = 'unnormalized_protein_matrix.csv'

in1 = cruxDir+'/final_peptide_matrix_count.txt'

new_px=pandas.read_csv(in1, sep = '\t', index_col=None)
a = new_px.groupby('protein').sum()
a.to_csv(ou1)
