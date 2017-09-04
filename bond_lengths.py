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
    print args
#    print sys.argv    
#    if len(sys.argv) < 2:
#        sys.exit("You tried to run grademaster without options. See --help for details.")
    main(args)