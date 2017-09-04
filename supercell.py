import ase.io.vasp
cell = ase.io.vasp.read_vasp("POSCAR")
ase.io.vasp.write_vasp("POSCAR.2x2x2",cell*(2,2,2), label='222supercell',direct=True,sort=True)