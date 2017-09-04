#!/usr/bin/env python2.7
#--------------------------------------
# Script to Convert .cif files to VASP Poscar
# Depends on argparse, ase and os libraries
#
# Version:  1.0
# Date:     12th May 2015
# Author:   Nicholas Hamilton
# Email:    n.hamilton@unsw.edu.au
#--------------------------------------

from ase import io
import argparse, os

#Set up the arguments and parse
parser = argparse.ArgumentParser(description="Convert CIF File to VASP POSCAR, in Either Direct or Cartesian Coordinates")

#argument values
parser.add_argument("-i",dest="input", default="input.cif",type=str, help='Name of Input FIle (CIF)')
parser.add_argument("-o",dest="output",default="POSCAR",   type=str, help='Name of Output File')
parser.add_argument("-c","--cartesian", dest='cartesian', action='store_true',help='Output in Cartesian Coordinates')


#Get the variables from the parsed arguments.
args = parser.parse_args()
fileInput = args.input
fileOutput= args.output
cartesian = args.cartesian

#Check the input file exists
if not os.path.isfile(fileInput):
	print "ERROR: Input FIle %s Doesn't Exist..." % fileInput
	quit()

#Run the Procedure
try:
	atoms = io.read(fileInput)
	atoms.write(fileOutput, format = 'vasp',direct=(not cartesian))
except Exception, e:
	print "ERROR: %s" % str(e)
	quit()

#Done
print "Success, output written to %s" % fileOutput
