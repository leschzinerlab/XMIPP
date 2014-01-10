#!/usr/bin/env python

import os
from optparse import OptionParser
import sys
import glob
import subprocess
from os import system

#Usage section

def parseCommandLine():
        arglist = []
        for arg in sys.argv:
                arglist.append( arg )
        progname = os.path.basename(arglist[0])
        usage = progname + " xmippBasename(e.g. ml2d_iter00009) OutputStackName"
	parser=OptionParser(usage)
	(options, args) = parser.parse_args(arglist[1:])
	if len(args) < 2:
                print "usage: " + usage
                

#Function section

def main():
	arglist = []
	for arg in sys.argv:
                arglist.append( arg )
	parser=OptionParser()
	(options, args) = parser.parse_args(arglist[1:])
	if len(args)>1:
		
		file=sys.argv[1]
		
		out=sys.argv[2]
		
		output="%s.hed" %(out)
		
		list=glob.glob("%s*xmp"%file) 	
			
		for file in list:
			
			cmd="proc2d %s %s" %(file,output)
			#system("proc2d %s.xmp %s.img"%(file,file))
			subprocess.Popen(cmd,shell=True).wait()
		
#Need this at the end for the parse commands
if __name__ == "__main__":
        main()
	parseCommandLine()