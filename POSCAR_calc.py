
#--------------------Part 1: Creating a file for an electron/hole transfer------------------------------
import numpy as np

class POSCAR(object):
    def __init__(self,name,filename):
        self.name = name
        self.file = filename
        self.coordinates = ' '
        self.selectiveflag = ' '
        self.directory = ' '
        self.description = "";
        self.cell_lattice = 0;
        self.basis;
        self.num_atoms = 0;
        self.total_atoms = 0
        self.atomtypeflag = "";
        self.filetype;

    def read_poscar(self):

        with open(self.file,'r') as f:
            get_all=f.readlines()
        
        for i,line in enumerate(get_all):
            self.description = i[0]
            self.basis = i[1]
            self.cell_lattice = i[2:5]
            self.
            
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
                            o_new=alpha*ocoord+metal_ion[n]*(1-alpha)
                            str_o=format(o_new, '.16f')
                            o_coord_new.append(str_o)
                        xyz="  ".join(o_coord_new)
                        f.writelines("  "+xyz+'\n')
                        print xyz
                    else:
                        f.writelines(line)
            with open(destination_file,'r') as f:
                get_all=f.readlines()
        return destination_file 

BVO3=POSCAR('BVO','POSCAR_ini')
print BVO3.file
BVO3.polaroncalc(0.95,neighboring_ions=[12,48,35,39], atom_serial_number=1, destination_file='POSCAR_new')
'''
####Use distance formula to find the nearest neighbors.####
####Verify coordinates with Vesta, Avogadro or other structure modeling software####
####distances are calculated in direct coordinates, not angstroms####
####This can be used as input into polaroncalc for oxygen neighbors if desired####
####Compare the bondlenths of neighboring atoms####
def neighbor_finder(poscar_file, atom_serial_number,coordination_number):
####poscar_file: input vector file####
####atom_serial_number: serial number coorsponding to central atom of interest####
####coordination number: number of bonded neighbors####
    import heapq #for sorting
    distances=[]
    a_vectorT=[]
####This section opens the position vector file, reads the file into get_all.####
####Then the atom serial number is place into an array####
   
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
                np.array(a_vectorT)
        print a_vectorT


####This section references get_vector function (see Part 2) to create a list of arrays.####
####we calculate the magnitude of the distance between the central atom and all the atoms in
# the get_vector array####
####then we sort by distances using heapq.nsmallest, but return the index number instead####
####because the origen is included we sort for coordination number +1, then remove the origin point####
####finally we a dictionary containing the indices in terms of the serial number convention (starts at 1 instead of 0)####
    for n, line in enumerate(get_vector(poscar_file)):
        neighbor_array=np.array(line)
        dist = np.linalg.norm(ion_array*a_vectorT-neighbor_array*a_vectorT)
        distances.append(dist)
    ksmall=heapq.nsmallest((coordination_number+1), range(len(distances)),distances.__getitem__)
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
    return neighbor_table '''