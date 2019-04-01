from pyquil import Program, get_qc
from pyquil.gates import *
from pyquil.api import local_qvm
import numpy as np

def ansatz(theta):
    prog = Program()
    prog = prog + RY(theta, 0)
    return prog


quantumCircuit = get_qc("9q-square-qvm")

thetaValues = np.linspace(0, 2*np.pi, 21)
results = []
for thetaValue in thetaValues:
     prog = ansatz(thetaValue)
     with local_qvm():
         bitstrs = quantumCircuit.run_and_measure(prog, trials=1000)
         results.append(np.mean(bitstrs[0]))
print(results)    