from projectq import MainEngine
from projectq.backends import CircuitDrawer
from projectq.ops import All, CNOT, H, Measure, Rz, X, Z


def getBellPair(engine):
    bit1 = engine.allocate_qubit()
    bit2 = engine.allocate_qubit()

    H | bit1
    CNOT | (bit1, bit2)

    return bit1, bit2

circuit_drawer = CircuitDrawer()
engine = MainEngine(circuit_drawer)

getBellPair(engine)

engine.flush()
print(circuit_drawer.get_latex())