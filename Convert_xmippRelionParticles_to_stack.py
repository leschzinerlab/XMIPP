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
        parser.set_usage("%prog -i <folder> -o <output stack> --num=[num. of particles] --name=<particle basename>")
        parser.add_option("-i",dest="folder",type="string",metavar="FILE",
                help="Folder containing the particles for analysis")
	parser.add_option("-o",dest="stack",type="string",metavar="FILE",
                help="Particle stack output name in .spi format")
        parser.add_option("--num",dest="numParts",type="int", metavar="INT",
                help="Number of particles in stack")
	parser.add_option("--name",dest="name",type="string", metavar="STR",
                help="Particle basename (e.g. data)")
	parser.add_option("-d", action="store_true",dest="debug",default=False,
                help="debug")
        options,args = parser.parse_args()

        if len(args) > 0:
                parser.error("Unknown commandline options: " +str(args))

        if len(sys.argv) < 5:
                parser.print_help()
                sys.exit()
        params={}
        for i in parser.option_list:
                if isinstance(i.dest,str):
                        params[i.dest] = getattr(options,i.dest)
        return params

#=============================
def checkConflicts(params):
        if not os.path.exists(params['folder']):
                print "\nError: folder '%s' does not exist\n" % params['folder']
                sys.exit()

	if os.path.exists(params['stack']):
		print "\nError: output stack already exists. Exiting.\n"
		sys.exit()

#==============================
def getXMIPPPath():
        xmipppath = subprocess.Popen("env | grep xmipp", shell=True, stdout=subprocess.PIPE).stdout.read().strip()
        if xmipppath: 
		return xmipppath
        print "XMIPP was not found, make sure XMIPP is in your path"
        sys.exit()

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
def xmipp2spi(params):
	print '\n'
        print 'Creating spider stack of XMIPP particles\n'
        print '\n'

	if os.path.exists("%s@{********[part]}\n" %(params['stack'][:-4])):
		print 'Stack %s.spi already exists. Exiting.' %(params['stack'][:-4])
		sys.exit()
	spifile = "currentSpiderScript.spi"
        if os.path.isfile(spifile):
                os.remove(spifile)
        spi=open(spifile,'w')
        spicmd="do lb1 [part]=1,%s\n" %(params['numParts'])
        spicmd+="CP\n"
	spicmd+="%s/%s{******[part]}\n" %(params['folder'],params['name'])
        spicmd+="%s@{********[part]}\n" %(params['stack'][:-4])
        spicmd+="lb1\n"
        runSpider(spicmd)

#==============================
if __name__ == "__main__":

	getXMIPPPath()
	params=setupParserOptions()
        checkConflicts(params)
	xmipp2spi(params)	
