from pyquil import Program
from pyquil.parameters import Parameter, quil_sin, quil_cos
from pyquil.quilbase import DefGate
from pyquil.gates import *
import numpy as np


thetaParameter = Parameter('theta')
controlledRx = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, quil_cos(thetaParameter / 2), -1j * quil_sin(thetaParameter / 2)],
    [0, 0, -1j * quil_sin(thetaParameter / 2), quil_cos(thetaParameter / 2)]
])

gate_definition = DefGate('CRX', controlledRx, [thetaParameter])
CONTROLRX = gate_definition.get_constructor()


program = Program()
program = program + gate_definition
program = program + H(0)
program = program + CONTROLRX(np.pi/2)(0, 1)

print(program)