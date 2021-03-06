#!/usr/bin/env python

import optparse
from sys import *
import os,sys,re
from optparse import OptionParser
import glob
import subprocess
from os import system
import linecache
import time


#=========================
def setupParserOptions():
        parser = optparse.OptionParser()
        parser.set_usage("%prog -i <stack.img> --num=[num. of particles] --radius=[radius] --sigma=[stdDev]")
        parser.add_option("-i",dest="stack",type="string",metavar="FILE",
                help="Particle stack in .img or .spi format")
        parser.add_option("--num",dest="numParts",type="int", metavar="INT",
                help="Number of particles in stack")
	parser.add_option("--radius",dest="radius",type="int", metavar="INT",
                help="Radius of particle for normalization (pixels)")
	parser.add_option("--sigma",dest="sigma",type="float", metavar="FLOAT",default="3.5",
                help="Standard deviation above which pixels are replaced by random values (default=3.5)")
	parser.add_option("-d", action="store_true",dest="debug",default=False,
                help="debug")
        options,args = parser.parse_args()

        if len(args) > 0:
                parser.error("Unknown commandline options: " +str(args))

        if len(sys.argv) < 4:
                parser.print_help()
                sys.exit()
        params={}
        for i in parser.option_list:
                if isinstance(i.dest,str):
                        params[i.dest] = getattr(options,i.dest)
        return params

#=============================
def checkConflicts(params):
        if not params['stack']:
                print "\nWarning: no untilted stack specified\n"
        elif not os.path.exists(params['stack']):
                print "\nError: stack file '%s' does not exist\n" % params['stack']
                sys.exit()
	if params['stack'][-4:] != '.img':
		if params['stack'][-4:] != '.spi':
			if params['stack'][-4:] != '.hed':
				print 'Stack extension %s is not recognized as .spi, .hed or .img file' %(params['stack'][-4:])
				sys.exit()

#==============================
def getXMIPPPath():
        xmipppath = subprocess.Popen("env | grep xmipp", shell=True, stdout=subprocess.PIPE).stdout.read().strip()
        if xmipppath: 
		return xmipppath
        print "XMIPP was not found, make sure XMIPP is in your path"
        sys.exit()

#==============================
def convertIMGtoSPI(params):

        #convert imagic stack to 3D mrc image stack using e2proc2d      

        cmd = 'proc2d %s %s.spi spiderswap' %(params['stack'],params['stack'][:-4])
        if params['debug'] is True:
                print cmd
        if os.path.exists('%s.spi' %(params['stack'][:-4])):
		print 'Output stack %s.spi already exists. Exiting.' %(params['stack'][:-4])
		sys.exit()
	subprocess.Popen(cmd,shell=True).wait()

#==============================
def spi2xmipp(params):
        print '\n'
	print 'Converting spider stack into individual images for XMIPP\n'
	print '\n'
	spifile = "currentSpiderScript.spi"
        if os.path.isfile(spifile):
                os.remove(spifile)
        spi=open(spifile,'w')
        spicmd="VM\n"
        spicmd+="mkdir data_temp\n" 
        spicmd+="do lb1 [part]=1,%s\n" %(params['numParts'])
	spicmd+="CP\n"
	spicmd+="%s@{********[part]}\n" %(params['stack'][:-4])
	spicmd+="data_temp/data{******[part]}\n"
	spicmd+="lb1\n"
	runSpider(spicmd)

#=============================
def runSpider(lines):
       spifile = "currentSpiderScript.spi"
       if os.path.isfile(spifile):
               os.remove(spifile)
       spi=open(spifile,'w')
       spi.write("MD\n")
       spi.write("TR OFF\n")
       spi.write("MD\n")
       spi.write("VB OFF\n")
       spi.write("MD\n")
       spi.write("SET MP\n")
       spi.write("(4)\n")
       spi.write("\n")
       spi.write(lines)

       spi.write("\nEN D\n")
       spi.close()
       spicmd = "spider spi @currentSpiderScript"
       spiout = subprocess.Popen(spicmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stderr.read()
       output = spiout.strip().split()
       if "ERROR" in output:
               print "Spider Error, check 'currentSpiderScript.spi'\n"
               sys.exit()
       # clean up
       os.remove(spifile)
       if os.path.isfile("LOG.spi"):
               os.remove("LOG.spi")
       resultf = glob.glob("results.spi.*")
       if resultf:
               for f in resultf:
                       os.remove(f)

#==============================
def xmipp_normalize(params):

	print '\n'
	print 'Running xmipp_normalize\n'
	print '\n'
	
	cmd = 'xmipp_normalize -i data_tmp.sel -method Ramp -background circle %s -remove_black_dust -thr_black_dust -%s -remove_white_dust -thr_white_dust %s' %(str(str(params['radius'])),str(params['sigma']),str(params['sigma']))
        print cmd
        subprocess.Popen(cmd,shell=True).wait()
	
#==============================
def xmipp_selfile_create():
	print '\n'
        print 'Creating xmipp selfile\n'
        print '\n'

	cmd = 'xmipp_selfile_create "data_temp/*.spi" > data_tmp.sel'
	print cmd
        subprocess.Popen(cmd,shell=True).wait()

#==============================
def xmipp2spi(params):
	print '\n'
        print 'Creating spider stack of XMIPP normalized particles\n'
        print '\n'

	if os.path.exists("%s_xnorm@{********[part]}\n" %(params['stack'][:-4])):
		print 'Stack %s_xnorm.spi already exists. Exiting.' %(params['stack'][:-4])
		sys.exit()
	spifile = "currentSpiderScript.spi"
        if os.path.isfile(spifile):
                os.remove(spifile)
        spi=open(spifile,'w')
        spicmd="do lb1 [part]=1,%s\n" %(params['numParts'])
        spicmd+="CP\n"
	spicmd+="data_temp/data{******[part]}\n"
        spicmd+="%s_xnorm@{********[part]}\n" %(params['stack'][:-4])
        spicmd+="lb1\n"
        runSpider(spicmd)

#==============================
if __name__ == "__main__":

	print '\n'
        print 'A single command to normalize an imagic or spider stack using xmipp_normalize'
	print '\n' 
	getXMIPPPath()
	params=setupParserOptions()
        checkConflicts(params)
       	if params['stack'][-4:] == '.img':
		if params['debug'] is True:
			print 'Imagic stack was provided'
		convertIMGtoSPI(params)
	if params['stack'][-4:] == '.hed':
                if params['debug'] is True:
                        print 'Imagic stack was provided'
                convertIMGtoSPI(params)
	spi2xmipp(params)
	xmipp_selfile_create()
	xmipp_normalize(params)
	xmipp2spi(params)	
	#Clean up
	if os.path.exists('%s_xnorm.spi' %(params['stack'][:-4])) is False:
		print 'Program crashed, exiting'
		sys.exit()
	cmd = 'rm -r data_temp/ data_tmp.sel'
	subprocess.Popen(cmd,shell=True).wait()		
