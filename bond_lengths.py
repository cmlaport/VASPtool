#--------------------------------------------INTRODUCTION------------------------------------------
#PROGRAM:  bond_lengths
#AUTHOR:   Christine LaPorte
#Revision: Version 0.1.1
#Date:     6/25/2017
#
#About this program: This program calculates the closest neighbors to a selected atom. User inputs
#VASP POSCAR file, atom of interest, and number of closest neighbors to locate.
#------------------------------------------SYNTAX--------------------------------------------------
#
#-f filename
#-a atom of interest
#-n number of atoms near atom a
#
#------------------------------------------PROGRAM BODY--------------------------------------------
import string
import numpy as np
import argparse
import sys
import VASPlib2
import os

def main(args):
    print VASPlib2.per_neighbor_finder(args.file,args.atom_num,args.coordinates)


if __name__=="__main__":  
    usage_str = "usage: %prog [options] arg"
 #   version_str = "%prog " + SCRIPT_VERSION
    parser = argparse.ArgumentParser(usage=usage_str)   
    parser = argparse.ArgumentParser(description='read the files')

    parser.add_argument('--file', '-f', 
                        dest='file', 
                        type = str, 
                        default=None, 
                        help='Specifies the position card file')
    
    parser.add_argument('--atom', '-a',
                        dest='atom_num',
                        type = int,
                        default=None,
                        help = 'Specifies the central atom by serial number')
    
    parser.add_argument('--num', '-n',
                    dest='coordinates',
                    type = int,
                    default=None,
                    help = 'number of atoms to search for')

    args = parser.parse_args()
#--------------------------------------EXECUTE PROGRAM---------------------------------------------
    print args
    main(args)
