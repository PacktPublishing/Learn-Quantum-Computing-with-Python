from pyquil import get_qc, Program
from pyquil.gates import CNOT,H, Z
from pyquil.api import local_qvm

quantumvirtualmachine = get_qc('9q-square-qvm')
#prog = Program(Z(0), CNOT(0, 1))
program = Program(H(0), CNOT(0, 1))
with local_qvm():
    qvm_results = quantumvirtualmachine.run_and_measure(program, trials=10)
    
    print(qvm_results[0])
    print(qvm_results[1])