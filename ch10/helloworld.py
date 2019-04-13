from projectq import MainEngine  
from projectq.ops import H, Measure  

engine = MainEngine() 
qubit_allocated = engine.allocate_qubit()  

H | qubit_allocated  
Measure | qubit_allocated

engine.flush()  
print("Measure {}".format(int(qubit_allocated)))  