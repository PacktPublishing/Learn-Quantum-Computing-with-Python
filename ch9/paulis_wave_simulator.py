from pyquil import Program
from pyquil.gates import *
from pyquil.paulis import sZ
from pyquil.api import QVMConnection

prog = Program(
    H(0),
    CNOT(0, 1),
)


zoper0 = (1-sZ(0))*0.5
zoper1 = (1-sZ(1))*0.5
xoroper = (1-sZ(0)*sZ(1))*0.5

print(zoper0,zoper1,xoroper)



for observable in [zoper0, zoper1, xoroper]:
    expect = QVMConnection().pauli_expectation(prep_prog=prog, pauli_terms=observable)
    print(observable, '\t', expect)