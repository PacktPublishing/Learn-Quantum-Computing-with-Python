from pyquil import Program
from pyquil.gates import *
from pyquil.api import WavefunctionSimulator
from math import pi

state_preparation = Program(X(0))
dummy_qubits = Program(I(1), I(2))  

wavefunction_simulator = WavefunctionSimulator()
wavefunction = wavefunction_simulator.wavefunction(state_preparation + dummy_qubits)


def qft3(q0, q1, q2):
    program = Program()
    program = program +  [SWAP(q0, q2),
          H(q0),
          CPHASE(-pi / 2.0, q0, q1),
          H(q1),
          CPHASE(-pi / 4.0, q0, q2),
          CPHASE(-pi / 2.0, q1, q2),
          H(q2)]
    return program
qft_program = state_preparation + qft3(0, 1, 2)
wavefunction = wavefunction_simulator.wavefunction(qft_program)
print(wavefunction.amplitudes)    