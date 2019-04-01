from pyquil import Program
from pyquil.gates import *
from pyquil import get_qc
from pyquil.api import local_qvm



quantumCircuit = get_qc('1q-qvm')  

program = Program()
program =  program + X(0)

with local_qvm():

   result = quantumCircuit.run_and_measure(program,trials=1)
   print(result)
