from pyquil import Program
from pyquil.api import WavefunctionSimulator
from pyquil.gates import *

wavefunction_simulator = WavefunctionSimulator()
program = Program()
program = program + X(0)
program = program + H(0)
program = program + H(1)
program = program + CNOT(1, 0)
program = program + H(0)
result = wavefunction_simulator.run_and_measure(program, trials=10)
print(result)