#-------------------------------------------Introduction--------------------------------------------
#PROGRAM      = 'polaronmaker.py'
#AUTHOR       = "Christine LaPorte"
#VERSION      = 'v0.0.2'
#VERSION DATE = '6/16/2017'

#About this program:
#In small polaron modeling, we see a distortion in the crystal lattice structure around a small area
#such as around a single atom in the structure.

#This program is designed to simulate a polaron using given vectors/coordinates in a VASP POSCAR file.
#This version assumes fractional coordinates.
#you can do up to two polaron distortions per program run
#the user needs to know the coordinate number of the atom of interest. The default number is 4.


#------------------------------------------SYNTAX--------------------------------------------------
#-i input file
#-a alpha
#-b beta
#-o central atom
#-f 2nd central atom
#-c coordinates around central atom
#--output output file
#See -h for details on program sytax
#
#
#---------------------------------------------------------------------------------------------------
import os
import math
import os
import numpy as np
import heapq
import argparse
import VASPlib2
#---------------------------------------------PROGRAM BODY------------------------------------------

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
    poscar_file = args.POSCAR
    site_num = args.atom_serial_number
    newfile = args.new_file
    coordinates = args.coordinates
    final_site = args.atom_final_site
    
    neighbors = VASPlib2.per_neighbor_finder(poscar_file,site_num,coordinates)
    neighborlist = neighbors.keys()
    print site_num, neighborlist
    polaroncalc(poscar_file,args.alpha,neighborlist,site_num,newfile)

#    if final_site != None:
#        neighbors = VASPlib2.per_neighbor_finder(poscar_file,final_site,coordinates)
#        neighborlist = neighbors.keys()
#        print final_site,neighborlist
#        polaroncalc(newfile,args.beta,neighborlist,final_site,newfile)

#---------------------------------ARGUMENT SETTINGS------------------------------------------------
if __name__=="__main__":  
    usage_str = "usage: %prog [options] arg"
 #   version_str = "%prog " + SCRIPT_VERSION
    parser = argparse.ArgumentParser(usage=usage_str)   
    parser = argparse.ArgumentParser(description='read the files')

    parser.add_argument('--POSCAR', '-i',
                        dest='POSCAR', 
                        type = str, 
                        default='POSCAR', 
                        help="Specifies the position card file. Must be in fractional coordinates")
    
    parser.add_argument('--alpha', '-a',
                        dest='alpha',
                        type = float,
                        default=None, 
                        help="Specifies how the bond length will change, where 1 = no change")
    
    parser.add_argument('--beta', '-b',
                        dest='beta',
                        type = float ,
                        default=None,
                        help = "Specifies the fraction that secondary atom bonds change, where 1 = no change")
    
    parser.add_argument('--atom', '-o',
                        dest='atom_serial_number',
                        type = int ,
                        default=None,
                        help = "Site where the defect occurs, specified by the atom's serial number")
    
    parser.add_argument('--atom2', '-f',
                        dest='atom_final_site',
                        type = int ,
                        default=None,
                        help = "Secondary defect site, specified by the atom's serial number")
 
    parser.add_argument('--coordinates', '-c',
                        dest='coordinates',
                        type = int ,
                        default=None,
                        help = 'The number of bonds around the central atom of interest. This is manually input into the program')
        
    parser.add_argument('--output',
                    dest='new_file',
                    type = str,
                    default='POSCAR.out',
                    help = 'name of file to output results to')

    args = parser.parse_args()
#--------------------------------------------------------------------------------------------------
#
#
#------------------------------------------PROGRAM EXECUTE-----------------------------------------
    print args
    
    main(args)
#---------------------------------------------END PROGRAM------------------------------------------
