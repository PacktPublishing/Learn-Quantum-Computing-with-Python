from pyquil import Program
from pyquil.gates import *
from pyquil.api import WavefunctionSimulator


def ghz_state(qubits):
    prog = Program()
    prog = prog + H(qubits[0])
    for q1, q2 in zip(qubits, qubits[1:]):
        prog = prog + CNOT(q1, q2)
    return prog
    
prog = ghz_state(qubits=[0, 1, 2])
print(prog)

waveFunction = WavefunctionSimulator().wavefunction(prog)
print(waveFunction)