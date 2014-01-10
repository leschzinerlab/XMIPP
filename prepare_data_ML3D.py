#!/usr/bin/env python

import sys
import subprocess
import os 

#To run: ./prepare_data_ML3D.py [selFile].sel [volume].vol [pixelSize] [number of seed models]

sel=sys.argv[1]
vol=sys.argv[2]
pix=float(sys.argv[3])
num=float(sys.argv[4])

print("Correcting absolute greyscale of initial reference volume\n")

os.mkdir('CorrectGreyscale')

doc=sel.strip('.sel')
doc=("%s.doc" %(doc))

print ("Making blank header file %s\n" %(doc))
cmd="xmipp_header_extract -i %s -o %s" %(sel,doc)
subprocess.Popen(cmd,shell=True).wait()

print ("Projecting volume %s\n" %(vol))
cmd="xmipp_angular_project_library  -i %s -experimental_images %s -o CorrectGreyscale/ref -sampling_rate 15 -sym c1h -compute_neighbors -angular_distance -1" %(vol,doc)
subprocess.Popen(cmd,shell=True).wait()

print ("Aligning particles to reference\n")
cmd="xmipp_angular_projection_matching  -i %s -o CorrectGreyscale/corrected_reference -ref CorrectGreyscale/ref" %(doc)
subprocess.Popen(cmd,shell=True).wait()

cmd="xmipp_angular_class_average  -i CorrectGreyscale/corrected_reference.doc -lib CorrectGreyscale/ref_angles.doc -o CorrectGreyscale/corrected_reference"
subprocess.Popen(cmd,shell=True).wait()

cmd="xmipp_reconstruct_wbp  -i CorrectGreyscale/corrected_reference_classes.sel -o corrected_reference.vol -threshold 0.02 -sym c1  -use_each_image -weight"
subprocess.Popen(cmd,shell=True).wait()

print ("Low pass filtering greyscale corrected model\n")
cmd="xmipp_fourier_filter -i corrected_reference.vol -o filtered_reference.vol -low_pass 80 -sampling %s" %(pix)
subprocess.Popen(cmd,shell=True).wait()

print ("Creating %s seed models" %(num))
cmd="xmipp_selfile_split -i %s -n %s -o subset" %(sel,num) 
subprocess.Popen(cmd,shell=True).wait()

if num == 2:

	os.mkdir('GenerateSeed_1')
	os.mkdir('GenerateSeed_2')


if num == 3:

        os.mkdir('GenerateSeed_1')
        os.mkdir('GenerateSeed_2')
	os.mkdir('GenerateSeed_3')



if num == 4:

        os.mkdir('GenerateSeed_1')
        os.mkdir('GenerateSeed_2')
        os.mkdir('GenerateSeed_3')
	os.mkdir('GenerateSeed_4')



