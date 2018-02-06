'''
    CRUX And MOFF Fusion
    
    Convert the .raw and .mzML files (different fractions) obtained from Mass Spectrometry into single file containing petides and their intensity
    
    Created by Suresh Poudel on 03/13/2017
    Last modified 02/27/2017
    Copyright (c) 2017 Suresh Poudel (ORNL). All rights reserved.
    
    '''

import glob
import os
import sys
import time
import subprocess
from os import path

print "The user need to have mzML files, fasta file and .params file in order to execute this script"

output1 = sys.argv[1]

PSMqval = sys.argv[2]

crux = sys.argv[3]
#IndexFile = sys.argv[3]


def waitUntilFinish(cnt,n):
	a = 0
	while a!=1: 
		if len(glob.glob(output1+'/'+'tide_output*/*.txt')) == cnt*n:
			a = 1
		else:
			time.sleep(300)
	time.sleep(120)
	return 

def submitJob(filenames):
	for files in glob.glob(filenames):
		subprocess.call(['qsub',files])
	return

def fileToSample(filelist):
	sample_List=[]
	for items in filelist:
		sample = items.split('/')[-1].split('.mzML')[0][0:-3]
		if sample not in sample_List:
			sample_List.append(sample)
	return sample_List

# os.chdir(output1)
mzml_lst = glob.glob(output1+'/*.mzML')
fasta_list = glob.glob(output1+'/*.fasta')
tide_search_files = []


if len(mzml_lst)!=0:
	
	#os.chdir(output1)
	#crux = '/home/pue/crux-3.1.Linux.x86_64/bin/crux'
	for fasta_file in fasta_list:
		code_Decoy = 'removeNewLIneDecoyDatabase.py'
		new_Fasta_in = fasta_file.split('.fasta')
		new_Fasta_file = new_Fasta_in[0]+'_New.fasta'
		Index = output1+'/Index_'+new_Fasta_in[0]
		IndexFile = output1+'/IndexFile_'+new_Fasta_in[0]
		mod = 'C+57.02146,2M+15.9949'
		# /data/home/spoudel/crux-3.1.Linux.x86_64/bin/crux tide-index --output-dir Index --decoy-format protein-reverse --mods-spec C+57.02146,2M+15.9949 --clip-nterm-methionine T /lustre/projects/spoudel/proteomics/prot_projects/projects/Ppoly_NCBI_F.fasta IndexFile
		subprocess.call(['python',code_Decoy,'-i',fasta_file,'-o', new_Fasta_file])
		subprocess.call([crux,'tide-index','--output-dir',Index,'--decoy-format','protein-reverse','--missed-cleavages','2','--mods-spec',mod,'--clip-nterm-methionine','T',fasta_file,IndexFile])

	#samples = fileToSample(mzml_lst)
	tide_input = ' '.join(mzml_lst)
	#crux = '/home/pue/crux-3.1.Linux.x86_64/bin/crux'
	new_out = output1+'/ConcatPerc'
	test =[crux,'tide-search','--compute-sp','T','--concat','T','--precursor-window','10','--precursor-window-type','ppm','--output-dir',new_out]
	test.append(tide_input)
	#NewIndex = 'IndexFile'+samp.split('_')[1]+samp.split('_')[2]
	test+=[IndexFile]
	new_test = ' '.join(test)
	os.system(new_test)
	# print 'test'
	# os.chdir(samp)
	#fold = output1+'/Tide'
	#file1 = fold+'/tide-search.txt'
	#tide_search_files.append(file1)
		# print tide_search_files
			# subprocess.call(['crux','percolator','--test-fdr','0.05','--train-fdr','0.05','--only-psms','T','--search-input','concatenated','--overwrite','T','--output-dir',fold,file1])
	perc_folder = output1+'/ConcatPerc'
	concat_tide = output1+'/ConcatPerc/tide-search.txt'	
	subprocess.call([crux,'percolator','--test-fdr','0.01','--train-fdr','0.01','--search-input','concatenated','--overwrite','T','--output-dir',perc_folder,concat_tide])

			
