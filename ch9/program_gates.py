from pyquil import Program
from pyquil.gates import *
program = Program()
program = program + X(0)
print(program)