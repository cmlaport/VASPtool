
#--------------------Part 1: Creating a file for an electron/hole transfer------------------------------
import numpy as np

class POSCAR(object):
    def __init__(self,name,filename):
        self.name = name
        self.filename = filename
        #self.coordinates = coordinates
        #self.selectiveflag = selectiveflag
        #self.directory = directory
        #self.description = description;
        #self.cell_lattice = cell_lattice;
        #self.basis = basis;
        #self.num_atoms = num_atoms;
        #self.total_atoms = total_atoms
        #self.atomtypeflag = atomtypeflag;
        #self.filetype =;
#coordinates,selectiveflag,directory,description,cell_lattice,basis,num_atoms,total_atoms,atomtypeflag):

    def file_contents(self):
        with open(self.filename,'r') as f:
            file_contents=f.readlines()

            #atomtypeflag = get_all[5]
            #num_atoms = get_all[6]
            
        return (file_contents)  
    
    def description(self):
        with open(self.filename,'r') as f:
            file_contents=f.readlines()
        description = file_contents[0]
        return description

    def basis(self):
        with open(self.filename,'r') as f:
            file_contents=f.readlines()
        basis = file_contents[1]
        return basis  

    def lattice(self):
    
        with open(self.filename,'r') as f:
            file_contents=f.readlines()
        
        cell_lattice = file_contents[2:5]
        for i,line in enumerate(cell_lattice):
            cell_lattice[i] = line.strip()
            cell_lattice[i] = line.split()
            cell_lattice[i] =  [float(n) for n in cell_lattice[i]]
        cell_lattice = np.array(cell_lattice)
            
        return cell_lattice
    
    
    def atomtypeflag(self):
        with open(self.filename,'r') as f:
            file_contents=f.readlines()
        atomtype = file_contents[5]
        atomtype = atomtype.strip()
        atomtype = atomtype.split()
        return atomtype
     
    def num_atomtype(self):
        with open(self.filename,'r') as f:
            file_contents=f.readlines()
        atomtype = file_contents[6]
        atomtype = atomtype.strip()
        atomtype = atomtype.split()
        atomtype = [int(n) for n in atomtype]
        return atomtype
    
    def total_atom(self):
        with open(self.filename,'r') as f:
            file_contents=f.readlines()
        atomtype = file_contents[6]
        atomtype = atomtype.strip()
        atomtype = atomtype.split()
        atomtype = [int(n) for n in atomtype]
        count = 0
        for n in atomtype:
            count = count + n
        return count

    
    def vector(self):
        with open(self.filename,'r') as f:  ##with funtion to open and close a file
            file_content=f.readlines()  ##reads all lines of file
            vector=[]
            total_atom = POSCAR.total_atom(self)
            for i, line in enumerate(file_content,-7):
                if i >= 1 and i<= total_atom:  ##for loop over the coordinates of BiVO3 supercell with 0 velocity
                    coordinates=line.split( )  
                    coordinates=[float(n) for n in coordinates]
                    vector.append(coordinates)  ##now each atom is a list of its coodinates (list of lists)
            vector = np.array(vector)
        
        return vector 

