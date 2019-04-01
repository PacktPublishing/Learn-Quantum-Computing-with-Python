from pyquil.quilatom import QubitPlaceholder
from pyquil import Program
from pyquil.gates import *

qbit0 = QubitPlaceholder()
qbit1 = QubitPlaceholder()
program = Program(H(qbit0), CNOT(qbit0, qbit1))
print(program)