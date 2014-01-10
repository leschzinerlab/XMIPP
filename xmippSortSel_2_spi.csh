#!/bin/bash 

#How to convert an xmipp sorted select file into a spider select file:

#To run: 

#	 xmippSortSel_2_spi.csh < sort_junk.sel | awk '$1 {printf("%s\n",$1)}' | sed 's/data//' | sed 's/data//' | sed -e 's/.spi//' | gawk '{printf ("%5d %1d  %-6.2f \n",NR,1,$0)}' >> sort_junk_sel.spi

while read file; do

	basename "$file"
done
