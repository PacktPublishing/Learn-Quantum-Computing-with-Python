from projectq.ops import All, CNOT, H, Measure, Rz, X, Z
from projectq import MainEngine
from projectq.meta import Dagger, Control


def GetBellPair(eng):
    b1 = eng.allocate_qubit()
    b2 = eng.allocate_qubit()

    H | b1
    CNOT | (b1, b2)

    return b1, b2


def ExecuteTeleport(eng, state_creation_function, verbose=False):

    b1, b2 = GetBellPair(eng)

    psi = eng.allocate_qubit()
    if verbose:
        print("Alice : state creation")
    state_creation_function(eng, psi)

    CNOT | (psi, b1)
    if verbose:
        print("Alice : entangled qubit")

    H | psi
    Measure | psi
    Measure | b1
    messageToBob = [int(psi), int(b1)]
    if verbose:
        print("Alice : message {} : Bob.".format(messageToBob))

    with Control(eng, b1):
        X | b2
    with Control(eng, psi):
        Z | b2

    if verbose:
        print("Bob is trying to uncompute the state.")
    with Dagger(eng):
        state_creation_function(eng, b2)

    del b2
    eng.flush()

    if verbose:
        print("Bob successfully arrived at |0>")


if __name__ == "__main__":
    engine = MainEngine()

    def GetState(engine, qubit):
        H | qubit
        Rz(1.21) | qubit

    ExecuteTeleport(engine, GetState, verbose=True)