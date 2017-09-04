#-------------------------------------------Introduction------------------------------------------------


#-------------------------------------------------------------------------------------------------------
import string
import numpy as np
import argparse
import sys
import VASPlib
####this section creates a template to copy data from when we write our output file####
def make_file(inputfile):
####inputfile: use initial POSCAR file as input for most cases####
    with open(inputfile,'r') as f:
        outputfile=f.readlines()
        return outputfile


####this counts the number of atoms in the POSCAR file so that we can make a list of coordinates for any 
# size structure####
def count_atom(inputfile):
####inputfile: use initial POSCAR file as input for most cases#### 
    for i, line in enumerate(make_file(inputfile)):
        total=0
        if i ==6:
            atom_count=line.split()
            atom_count=[int(n) for n in atom_count]
            count=0
            while count < len(atom_count):
                total=total+atom_count[count]
                count = count +1
            return total

        
####this section reads intial and final position of atoms from the initial and final state 
# position vector files####
####we input files that represent the atom on one atom(initial) and a neighbor atom (final)####
####the result is a nested list of atom coordinates, the values are floating points:
# list[atom1[coordinate_x,coordinate_y,coordinate_z]
####we also make a dictionary that can be used as a quick reference for each of the position vector files####     
####if the file format is incorrect an error message will appear (try, expect)
def get_vector(workingfile):
####workingfile: initial and final state position vector files. Usually a list of two files####
    try:
        with open(workingfile,'r') as f:  ##with funtion to open and close a file
            whole_file=f.readlines()  ##reads all lines of file
            vector=[]
            for i, line in enumerate(whole_file,-7):
                if i >= 1 and i<=count_atom(workingfile):  ##for loop over the coordinates of BiVO3 supercell with 0 velocity
                    coordinates=line.split( )  
                    coordinates=[float(n) for n in coordinates]
                    vector.append(coordinates)  ##now each atom is a list of its coodinates (list of lists)
        return vector
    except:
        print "Not a valid position vector file!"
        print """Position vector file requires format:'\n' atom line 5'\n' #of atoms line 6'\n' begin position coordinates line 9 """


####This section does the calculation that we want to do to the POSCAR coordinates####
####It returns the values as a nested list, where each sublist is a set of string values####
def change_bond(workingfiles,change_step):
####workingfiles: initial and final state position vector files. Usually a list of two files####
####changestep: a number between 0 and 1, where 0 is the initial state and 1 is the final state position####
    output_coordinates=[]
    initial_state=get_vector(str(workingfiles[0]))
    initial_state= np.array(initial_state)
    final_state=get_vector(str(workingfiles[1]))
    final_state=np.array(final_state)
    periodic_check = np.copy(final_state)
    for n,lst in enumerate(final_state):
        for i in range(len(lst)):
            periodic_check = lst[i] - initial_state[n][i]
    final_p = VASPlib.periodic_boundary(periodic_check)
    
    
    output_position=((1-change_step)*initial_state+final_p*change_step)
    if periodic_check > 0.5:
        output_position = output_position + 1
    if periodic_check < -0.5:
        output_position = output_position -1
    output_position=output_position.tolist()
    for lst in output_position:
        for i in range(len(lst)):
            lst[i]=format(lst[i],'.16f')
           
    for lst in output_position:
        for i in range(len(lst)):
            if lst[i][0] !='-':
                lst[i]=' '+ lst[i]
        output_line=' '.join(lst)
        output_coordinates.append(output_line)
    
    return output_coordinates

def main(args):
    new_file = args.new_file
    workingfiles = [args.POSCAR1,args.POSCAR2]
    change_step = args.change_step
    
    call=change_bond([args.POSCAR1,args.POSCAR2],args.change_step)
    with open(args.new_file,'w') as f:
            for i, line in enumerate(make_file(args.POSCAR1),-7):
                if i >= 1 and i <= count_atom(args.POSCAR2):
                    f.writelines('  ' + call[i-1] + '\n')
                else:
                    f.writelines(line)
    return args.new_file

if __name__=="__main__":  
    usage_str = "usage: %prog [options] arg"
 #   version_str = "%prog " + SCRIPT_VERSION
    parser = argparse.ArgumentParser(usage=usage_str)   
    parser = argparse.ArgumentParser(description='read the files')

    parser.add_argument('--p1', 
                        dest='POSCAR1', 
                        type = str, 
                        default=None, 
                        help='Specifies the position card file')
    
    parser.add_argument('--p2',
                        dest='POSCAR2',
                        type = str,
                        default=None, 
                        help='Specifies a second position card file')
    
    parser.add_argument('--step',
                        dest='change_step',
                        type = float ,
                        default=None,
                        help = 'The interpolation is represented as a fraction of the final state')
    
    parser.add_argument('--output',
                    dest='new_file',
                    type = str,
                    default=None,
                    help = 'name of file to output results to')

    args = parser.parse_args()
    print args
#    print sys.argv    
#    if len(sys.argv) < 2:
#        sys.exit("You tried to run grademaster without options. See --help for details.")
    main(args)