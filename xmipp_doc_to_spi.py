#!/usr/bin/env python

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
        parser.set_usage("%prog -d <XMIPP doc file> -s <XMIPP select filek> -o <output>")
        parser.add_option("-d",dest="doc",type="string",metavar="FILE",
                help="XMIPP doc file")
        parser.add_option("-s",dest="sel",type="string",metavar="FILE",
                help="Xmipp select file")
	parser.add_option("-o",dest="out",type="string",metavar="FILE",
                help="Output document file")
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
	doc = params['doc']
        out = open(params['out'],'w')

	s = open(sel,'r')

        for line in s:

                l = line.split()
                part = l[0]
                partNum = part[:-4]
                partNum = partNum[-5:]

		lineNum = int(2*float(partNum)+1) 

		lineDoc = linecache.getline(doc,lineNum)

		out.write(lineDoc)
	
	out.close()	

if __name__ == "__main__":     
	params=setupParserOptions()     
	main2(params)
