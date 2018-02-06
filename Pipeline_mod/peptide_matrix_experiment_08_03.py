import sys
import glob
from collections import defaultdict
from os import path
import os
cruxDir = sys.argv[1]

def peptToDict(filename):
	d1 = {}
	with open(filename,'r') as f:
		for line in f:
			if 'specCnt' not in line.strip():

				temp_line=line.strip().split('\t')
				d1[temp_line[0].strip()+'_'+temp_line[1].strip()] = temp_line[-1].strip()
	return d1


def pepfilesToList(file_col):
	peptList = []
	for filename in file_col:
		with open(filename,'r') as f:
			for line in f:
				if 'specCnt' not in line.strip():
					temp_line=line.strip().split('\t')
					val = temp_line[0].strip()+'_'+temp_line[1].strip()
					if val not in peptList:
						peptList.append(val)

	return peptList

pept_Reports = glob.glob(cruxDir+'/'+'*_sample_pep_report.txt')

pept_list = pepfilesToList(pept_Reports)
# print pept_list

dd = defaultdict(list)
for f1 in pept_Reports:
	dct = f1.split('.txt')
	dct[0]={}
	dct[0] = peptToDict(f1)
	dct[0].setdefault('peptide_protein', f1.strip().split('_sample_pep_report.txt')[0].split('/')[-1])

	for key in pept_list:
		dct[0].setdefault(key, '')
	
	for key, value in dct[0].iteritems():
		# if 'peptide_protein' not in key:
		dd[key].append(value)


header = '\t'.join(dd['peptide_protein'])
# print header
os.chdir(cruxDir)
with open('final_peptide_matrix_count.txt','a') as g:
	g.write('peptide\tprotein\t'+header+'\n')
for key in dd.keys():
	with open('final_peptide_matrix_count.txt','a') as g:
		if 'peptide_protein' not in key:
			value_row = '\t'.join(dd[key])
			new_key = key.split(')_')
			# print new_key[0]+')\t'+new_key[1]+'\t'+str(value_row)
			
			g.write(new_key[0]+')\t'+new_key[1]+'\t')
			g.write(str(value_row))
			g.write('\n') 

