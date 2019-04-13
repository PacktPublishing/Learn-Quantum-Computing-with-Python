import math

from projectq import MainEngine
from projectq.ops import H, Z, X, Measure, All
from projectq.meta import Loop, Compute, Uncompute, Control


def ExecuteGrover(engine, n, oracle):
    x = engine.allocate_qureg(n)

    All(H) | x

    num_it = int(math.pi/4.*math.sqrt(1 << n))

    oracle_out = engine.allocate_qubit()
    X | oracle_out
    H | oracle_out

    with Loop(engine, num_it):
        oracle(engine, x, oracle_out)
        with Compute(engine):
            All(H) | x
            All(X) | x

        with Control(engine, x[0:-1]):
            Z | x[-1]

        Uncompute(engine)

    All(Measure) | x
    Measure | oracle_out

    engine.flush()
    return [int(qubit) for qubit in x]


def GetAlternatingBitsOracle(engine, qubits, output):
    with Compute(engine):
        All(X) | qubits[1::2]
    with Control(engine, qubits):
        X | output
    Uncompute(engine)

engine = MainEngine()  
print(ExecuteGrover(engine, 7, GetAlternatingBitsOracle))
