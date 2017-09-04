#-------------------------------------------Introduction------------------------------------------------
#In polaron modeling, we see a change in the bond lengths within a cystal structure when a charge is
# placed on an atom. We can use this idea to move an electron or hole from one atom to another in a 
# crystal.
#This is used in ab initio methods to determine charge mobility
#Here we use python to help model this behavior.
#We define simple functions to help us manipulate the position_vector file.
#This program is set up to use the POSCAR file in VASP.
#This program can manipulate the bond length of neighboring atoms around a central atom. This will create
# a new file with the adjusted structure so that we can move our hole or electron to or from that atom.
#This code is also designed to perform a linear interpolation between a initial and final state structure:
# This function requires initial state and final state position vector files
# The output file is a state inbetween the initial and final state.
#-------------------------------------------------------------------------------------------------------
import os
import math
import os
import numpy as np #for arrays
import heapq #for sorting
import argparse
import VASPlib2
#--------------------Part 1: Creating a file for an electron/hole transfer------------------------------

def polaroncalc(poscar_file,alpha,neighboring_ions,atom_serial_number, destination_file):

    with open(poscar_file,'r') as f:
        get_all=f.readlines()
        for i, line in enumerate(get_all,-7):
            if i==atom_serial_number:
                metal_ion=line.split( )
                metal_ion=[float(n) for n in metal_ion]


####This section calculates a new coordinate for each neighboring ion####
####Coordinates are converted back to string to write to file####
    for oxy in range(len(neighboring_ions)):
        with open(destination_file,'w') as f:
            for i, line in enumerate(get_all,-7):
                if i==neighboring_ions[oxy]:
                    oline=line.split( )
                    oline = [float(n) for n in oline]
                    o_coord_new=[]
                    for n, ocoord in enumerate(oline):
                        MO_old=(ocoord-metal_ion[n])
                        MO_o = VASPlib2.periodic_boundary(MO_old)
                        MO_new=alpha*MO_o
                        o_new=MO_new+metal_ion[n]
                        if MO_old > 0.5:
                            o_new = o_new + 1
                        if MO_old < -0.5:
                            o_new = o_new - 1
                        str_o=format(o_new, '.16f')
                        o_coord_new.append(str_o)
                    xyz="  ".join(o_coord_new)
                    f.writelines("  "+xyz+'\n')

                else:
                    f.writelines(line)
        with open(destination_file,'r') as f:
            get_all=f.readlines()
    return destination_file

def main (args):
    poscar_file = args.poscar
    site_num = args.atom_serial_number
    newfile = args.newfile
    coordinates = args.coordinates
    final_site = args.atom_final_site
    
    neighbors = VASPlib2.per_neighbor_finder(poscar_file,site_num,coordinates)
    neighborlist = neighbors.keys()
    polaroncalc(poscar_file,args.alpha,site_num,newfile)

    if final_site != None:
        neighbors = VASPlib2.per_neighbor_finder(poscar_file,final_site,coordinates)
        neighborlist = neighbors.keys()
        polaroncalc(newfile,args.beta,final_site,newfile)

if __name__=="__main__":  
    usage_str = "usage: %prog [options] arg"
 #   version_str = "%prog " + SCRIPT_VERSION
    parser = argparse.ArgumentParser(usage=usage_str)   
    parser = argparse.ArgumentParser(description='read the files')

    parser.add_argument('--POSCAR', '-i',
                        dest='POSCAR', 
                        type = str, 
                        default=None, 
                        help='Specifies the position card file')
    
    parser.add_argument('--alpha', '-a',
                        dest='alpha',
                        type = float,
                        default=0.95, 
                        help='Specifies a fraction that bonds will shrink by')
    
    parser.add_argument('--beta', '-b',
                        dest='beta',
                        type = float ,
                        default=1.05,
                        help = 'Specifies the fraction that bonds will grow by')
    
    parser.add_argument('--atom_initial', '-o',
                        dest='atom_serial_number',
                        type = int ,
                        default=1,
                        help = 'Initial defect site')
    
    parser.add_argument('--atom_final', '-f',
                        dest='atom_final_site',
                        type = int ,
                        default=None,
                        help = 'Final defect site')
 
    parser.add_argument('--coordinates', '-c',
                        dest='coordinates',
                        type = int ,
                        default=4,
                        help = 'Final defect site')
        
    parser.add_argument('--output',
                    dest='new_file',
                    type = str,
                    default='POSCAR.out',
                    help = 'name of file to output results to')

    args = parser.parse_args()
    print args
#    print sys.argv    
#    if len(sys.argv) < 2:
#        sys.exit("You tried to run grademaster without options. See --help for details.")
    main(args)