from pyquil.api import WavefunctionSimulator
from pyquil import Program
from pyquil.gates import *
prog = Program(
    H(0),
    CNOT(0, 1),
)
print(prog)
wavefunction = WavefunctionSimulator().wavefunction(prog)
print(wavefunction)