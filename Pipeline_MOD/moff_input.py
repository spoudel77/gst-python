import glob
import os
import sys
import time
import subprocess
from os import path


output1 = sys.argv[1]

rt_p = sys.argv[2]
rt_w = sys.argv[3]
tol = sys.argv[4]

os.chdir(output1)

for file2 in glob.glob('*.mzML'):
	out2 = output1+"/"+file2[0:-5]+'.txt'
	out3 = output1+"/"+file2[0:-5]+'.mzML'
	out_fol = output1+'/'+'MOFF_OUTPUT'
	subprocess.call(['python','moff_mzml.py','--inputtsv',out2,'--rt_p',rt_p,'--rt_w',rt_w,'--inputraw',out3,'--tol',tol,'--output_folder',out_fol])

