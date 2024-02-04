import math
from deprecated import deprecated
from typing import Optional
#import perceval as pcvl
from perceval import * 
import perceval as pcvl
from perceval.utils.algorithms.circuit_optimizer import CircuitOptimizer
import numpy as np
import perceval.components as comp
from perceval.utils.algorithms.simplification import simplify

def build_processor(modes, C, herald_indexes, change_basis = False, mode_basis_change=0):
    processor = pcvl.Processor("SLOS", modes)

    if change_basis:
        processor.add(mode_basis_change, pcvl.BS.H())
        processor.add(0,  comp.PERM([1, 0, 3, 2]))


    processor.add(0, C)
    for i in herald_indexes:
        processor.add_herald(i,1)

    if change_basis:
        processor.add(mode_basis_change, pcvl.BS.H())
        processor.add(0,  comp.PERM([1, 0, 3, 2]))
    return processor


def get_CCZ():
    # Return the processor's CCZ


    # Given array
    array = [
        [1.00050057e+00, -1.97125585e+00, 6.41240889e-01, 1.17478198e+00, -7.85131318e-02, 1.75119448e+00],
        [-1.42475437e+00, 1.50209773e+00, -5.86004693e-01, 1.46572683e+00, -7.39201837e-02, 2.37011908e+00],
        [3.38102724e-02, -1.45496088e+00, -4.94541751e-01, 1.71560691e+00, 1.06515694e-01, -4.98504150e-01],
        [2.21434090e-01, 1.18809853e+00, 3.03081108e+00, 1.31107407e+00, -1.35968060e-01, -6.99389255e-01],
        [2.83051274e+00, 1.43555626e+00, -4.56329083e-01, -4.56098445e-01, 1.42749749e-01, 9.88728256e-01],
        [-2.19669288e-01, 1.59550364e-03, 2.09581885e-01, -6.12932596e-02, 3.58386617e+00, 1.00339534e-01]
    ]

    # Create the numpy array
    matrix = np.array(array)
    matrix = matrix/np.linalg.norm(matrix,2)


    matrix = Matrix(matrix)

    def mzi(i):
        return Circuit(2) // PS(P(f"phi_1_{i}")) // BS() // PS(P(f"phi_2_{i}")) // BS()
    def ps(i):
        return PS(P(f"phi_3_{i}"))

    template = GenericInterferometer(6, mzi, phase_shifter_fun_gen=ps, phase_at_output=True)


    result_circuit, fidelity = CircuitOptimizer().optimize(matrix, template)
    pdisplay(result_circuit, recursive=True)

    pcvl.pdisplay(result_circuit, recursive=True)
    final = Circuit(9)
    final.add(0, comp.PERM([0, 3, 2, 4, 1, 5, 6, 7, 8]))
    final.add(3, result_circuit)
    final.add(0, comp.PERM([0, 4, 2, 1, 3, 5, 6, 7, 8]))
    pcvl.pdisplay(final, recursive=True)



    processor = build_processor(9, final, [6,7,8], change_basis=True, mode_basis_change=4)
    #pcvl.pdisplay(processor)


    states = {pcvl.BasicState('|1,0,1,0,1,0>'): '000',
                pcvl.BasicState('|1,0,1,0,0,1>'): '001',
                pcvl.BasicState('|1,0,0,1,1,0>'): '010',
                pcvl.BasicState('|1,0,0,1,0,1>'): '011',
                pcvl.BasicState('|0,1,1,0,1,0>'): '100',
                pcvl.BasicState('|0,1,1,0,0,1>'): '101',
                pcvl.BasicState('|0,1,0,1,1,0>'): '110',
                pcvl.BasicState('|0,1,0,1,0,1>'): '111'}

    return processor