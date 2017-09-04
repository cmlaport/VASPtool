#-------------------------------------------Introduction------------------------------------------------


#-------------------------------------------------------------------------------------------------------
import string
import numpy as np
import argparse
import sys
import VASPlib2
####this section creates a template to copy data from when we write our output file####

def main(args):
    new_file = args.new_file
    workingfiles = [args.POSCAR1,args.POSCAR2]
    change_step = args.change_step
    
    call = VASPlib2.per_change_bond([workingfiles],args.change_step)
    with open(new_file,'w') as f:
            for i, line in enumerate(VASPlib2.make_file(workingfiles[0]),-7):
                if i >= 1 and i <= VASPlib2.count_atom(workingfiles[1]):
                    f.writelines('  ' + call[i-1] + '\n')
                else:
                    f.writelines(line)
    return new_file

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