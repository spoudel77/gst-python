'''
    CRUX And MOFF Fusion
    
    Convert the .raw and .mzML files (different fractions) obtained from Mass Spectrometry into single file containing petides and their intensity
    
    Created by Suresh Poudel on 02/15/2017
    Last modified 02/27/2017
    Copyright (c) 2017 Suresh Poudel (ORNL). All rights reserved.
    
    '''

## Parse mzML files, pulls
import sys
#sys.path.append('/home/pue/.conda/envs/spoudel/lib/python2.7/site-packages')
from pymzml import *
from os import path
import os.path
import glob
import os
import csv


## You will need to install pymzml and glob
## Make sure to pay attention to the file paths, including whether you are on a Linux or Windows based OS
## For simplicity, enter all file paths in Linux style. path.normpath() should handle these case if on
## Windows OS

mzML_Path = sys.argv[1]  #you should enter the command as script.py /path/to/mzml psmqvalCutoff

psmQvalue = sys.argv[2]

def parseMZML(a_file):
	
	msrun = run.Reader(a_file,extraAccessions=[('MS:1000042',['value']),("MS:1000016",['value']),("MS:1000504",["value"]),("MS:1000505",["value"])]) 
	
	dict1 = {} #empty dictionary to add MS2Scan, scan time and Selected ion mass to charge
	# File Path

	count = 0 			# This is just used to keep track of the scan number since they are ordered in the mzML files
	ms2_found = False	# When ms2 scan is found, this is switched to true
	ms1_scan = -1 		# Stores the ms1 scan value associated with a set of ms2 scans
	

	# Iterates through all of the scans within a run
	for spectrum in msrun:
		count+=1
		if spectrum["ms level"] == 1:
			if ms2_found == True:
				ms2_found = False	
				ms1_scan = -1       
		else:
			if ms1_scan == -1:
				ms1_scan = count - 1 		# since the ms1 scan precedes all ms2 scan associated with it
				ms2_found = True        	

			# PymzML tends to read in a scan that has no associated information with it.
			# This tends to occur at the end of the mzML file, so it might just be a bug in the library.
			# This try-except block is just meant to handle these situations. It will output
			# the corresponding scan number to the terminal so you can go look at it in the mzML file later.
			try:
				dict1[str(count).strip()] = "\t".join([str(spectrum["MS:1000016"]*60.0),str(spectrum["MS:1000744"])])
			except KeyError:
				print count
				continue
	return dict1	




def fileToSample(filelist):
	sample_List=[]
	for items in filelist:
		sample = items.split('/')[-1].split('.mzML')[0][0:-3]
		if sample not in sample_List:
			sample_List.append(sample)
	return sample_List

def openFile(key1, psm, filename, new_list, outfile, mz_dict):
	with open(filename,'r') as new_f, open(outfile,'w') as new_g:

		for line_r in new_f:
			temp_line = line_r.strip().split('\t')
			if 'file_idx' in line_r:
				new_g.write(line_r.strip()+'\trt\tmz\tpeptide\tprot\tmass\n')
			
			if temp_line[0] == key1 and float(temp_line[7]) <= float(psm):
				pep_id = temp_line[-3]+' (charge +'+ temp_line[2]+')'
				rt_mz = mz_dict[temp_line[1]].split('\t')
				if pep_id in new_list: 
					new_g.write(line_r.strip()+'\t'+rt_mz[0]+'\t'+rt_mz[1]+'\t'+pep_id+'\t'+temp_line[-2]+'\t'+temp_line[-8]+'\n')
	return outfile

mzml_lst = glob.glob(mzML_Path+'/*.mzML')
fold_list = fileToSample(mzml_lst)

file_id = {}


in_perc_id = mzML_Path+'/ConcatPerc/percolator.log.txt'
with open(in_perc_id,'r') as f:
	for line in f:
		if 'INFO: Assigning index' in line:
			te_line = line.strip().split()
			file_id[te_line[3]] = te_line[-1][0:-6]
cnt = 0
pep_list = []

in_perc = mzML_Path+'/ConcatPerc/percolator.target.peptides.txt'
in_perc2 = mzML_Path+'/ConcatPerc/percolator.target.psms.txt'

with open(in_perc, 'r') as csvfile:
	reader = csv.DictReader(csvfile, delimiter = '\t')
	for row in reader:
		if float(row['percolator q-value']) <= float(psmQvalue):
			new_peptide = row['sequence']+' (charge +'+ row['charge']+')'
			pep_list.append(new_peptide)



for key in file_id.keys():
	with open(in_perc2, 'r') as csvfile2:
		
		reader2 = csv.DictReader(csvfile2, delimiter = '\t')
		header=reader.fieldnames
		header+=['rt','mz','peptide','prot','mass']
		d1 = {}
		out_fil = file_id[key]+'.txt'
		#out_fil = file_id[key]+'.csv'  ## for csv files 

		mzml_file = file_id[key]+'.mzML'
		d1 = parseMZML(mzml_file)
		# for key in d1.keys():
		# 	print key
		out_fil = openFile(key, psmQvalue, in_perc2, pep_list, out_fil, d1)
		
				
		



