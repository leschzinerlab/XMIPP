#!/usr/bin/env python

import optparse
from sys import *
import os,sys,re
from optparse import OptionParser
import glob
import subprocess
from os import system
import linecache

def setupParserOptions():
        parser = optparse.OptionParser()
        parser.set_usage("%prog -i <imagic particle stack> -s <XMIPP select filek>")
        parser.add_option("-i",dest="stack",type="string",metavar="FILE",
                help="Imagic particle stack")
        parser.add_option("-s",dest="sel",type="string",metavar="FILE",
                help="Xmipp select file")
        parser.add_option("-d", action="store_true",dest="debug",default=False,
                help="debug")
        options,args = parser.parse_args()

        if len(args) > 0:
                parser.error("Unknown commandline options: " +str(args))

        if len(sys.argv) < 2:
                parser.print_help()
		sys.exit()
        params={}
        for i in parser.option_list:
                if isinstance(i.dest,str):
                        params[i.dest] = getattr(options,i.dest)
        return params

def main2(params):
		
	sel = params['sel']
	stack = params['stack']

	s = open(sel,'r')

	if os.path.exists('tmp.txt'):
		os.remove('tmp.txt')
	tmp = open('tmp.txt','w')

	for line in s:

		l = line.split()
		part = l[0]
		partNum = part[:-4]
		partNum = partNum[-5:]

		#Switch to eman numbering convention

		partNum = float(partNum) - 1

		tmp.write('%s\n'  %(str(partNum)))

	tmp.close()

	cmd = 'proc2d %s %s_sel.img list=tmp.txt' %(stack,stack[:-4])
	subprocess.Popen(cmd,shell=True).wait()	


if __name__ == "__main__":     
	params=setupParserOptions()     
	main2(params)
