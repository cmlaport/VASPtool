import math
import numpy as np
from itertools import product

def make_file(inputfile):
    with open(inputfile,'r') as f:
        outputfile=f.readlines()
        return outputfile


def count_atom(inputfile):

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


def get_vector(workingfile):

    try:
        with open(workingfile,'r') as f:  ##with funtion to open and close a file
            whole_file=f.readlines()  ##reads all lines of file
            vector=[]
            for i, line in enumerate(whole_file,-7):
                if i >= 1 and i<=count_atom(workingfile):  ##for loop over the coordinates of BiVO3 supercell with 0 velocity
                    coordinates=line.split( )  
                    coordinates=[float(n) for n in coordinates]
                    vector.append(coordinates)  ##now each atom is a list of its coodinates (list of lists)
            vector = np.array(vector)
        return vector
    except:
        print "Not a valid position vector file!"
        print """Position vector file requires format:'\n' atom line 5'\n' #of atoms line 6'\n' begin position coordinates line 9 """


def vect_dist(array1,array2):
    vector1 = array1
    vector2 = get_vector(array2)
    dist = np.copy(vector2)
    for n, atom in enumerate(dist):
        for i,xyz in enumerate(atom):
            dist[n][i] = xyz - vector1[i]
    
    return dist 


def periodic_boundary(dist):    
    
    if dist > 0.5:
        dist = dist - 1
        dist = format(dist,'.16f')
               
    elif dist < -0.5:
        dist = dist + 1
        dist = format(dist,'.16f')
               
    return dist 

def return_periodic(dist_array,array2):
    dist = np.copy(dist_array)
    for n, atom in enumerate(dist_array):
        for i,xyz in enumerate(atom):
            dist_array[n][i] = xyz + vector2[n][i]
    
    return dist_array    

       
def p_mag_distance(dist):
    return math.sqrt(dist[0]**2 + dist[1]**2 + dist[2]**2)

def per_neighbor_finder(poscar_file, atom_serial_number,coordination_number):

    import heapq
    distances=[]
    a_vectorT=[]
   
    with open(poscar_file,'r') as f:
        get_all=f.readlines()
        for i, line in enumerate(get_all,-7):
            if i==atom_serial_number:
                metal_ion=line.split(   )
                metal_ion=[float(n) for n in metal_ion]
                ion_array=np.array(metal_ion)
            if i <=-3 and i >=-5:
                a_vectT=line.split( )
                a_vectT=[float(n) for n in a_vectT]
                a_vectorT.append(a_vectT)
    a_vectorT = np.array(a_vectorT)
    


    abc = vect_dist(ion_array,poscar_file)
    
    num_atoms = len(abc)
    distance = np.zeros(num_atoms)
    for i,atom in enumerate(abc):
        for j,xyz in enumerate(atom):
            atom[j] = periodic_boundary(xyz)
            
            
        atom = np.dot(atom,a_vectorT.T)
        distance[i] = p_mag_distance(atom)

    distances = distance.tolist()

    ksmall=heapq.nsmallest((coordination_number+1), range(len(distances)),distance.__getitem__)
    kdist=heapq.nsmallest((coordination_number+1), distances)
    n = 0
    while n < len(ksmall): #change numbering to start at 1
        ksmall[n]=ksmall[n] + 1
        n=n+1

    neighbor_table={}
    for i in range(len(ksmall)):
        neighbor_table[ksmall[i]]=kdist[i]
    for key, item in neighbor_table.items():
        if key is atom_serial_number:
            del neighbor_table[key]
    return neighbor_table

print per_neighbor_finder('init_POSCAR', 9, 4)