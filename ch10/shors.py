from __future__ import print_function

import math
import random
import sys
from fractions import Fraction
try:
    from math import gcd
except ImportError:
    from fractions import gcd

from builtins import input

import projectq.libs.math
import projectq.setups.decompositions
from projectq.backends import Simulator, ResourceCounter
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               MainEngine, TagRemover)
from projectq.libs.math import (AddConstant, AddConstantModN,
                                MultiplyByConstantModN)
from projectq.meta import Control
from projectq.ops import (All, BasicMathGate, get_inverse, H, Measure, QFT, R,
                          Swap, X)


def ExecuteShorAlgorithm(eng, N, a, verbose=False):
    n = int(math.ceil(math.log(N, 2)))

    x = eng.allocate_qureg(n)

    X | x[0]

    measurements = [0] * (2 * n)  
    ctrl_qubit = eng.allocate_qubit()

    for k in range(2 * n):
        current_a = pow(a, 1 << (2 * n - 1 - k), N)
        H | ctrl_qubit
        with Control(eng, ctrl_qubit):
            MultiplyByConstantModN(current_a, N) | x

        for i in range(k):
            if measurements[i]:
                R(-math.pi/(1 << (k - i))) | ctrl_qubit
        H | ctrl_qubit

        Measure | ctrl_qubit
        eng.flush()
        measurements[k] = int(ctrl_qubit)
        if measurements[k]:
            X | ctrl_qubit

        if verbose:
            print("\033[95m{}\033[0m".format(measurements[k]), end="")
            sys.stdout.flush()

    All(Measure) | x
    y = sum([(measurements[2 * n - 1 - i]*1. / (1 << (i + 1)))
             for i in range(2 * n)])

    r = Fraction(y).limit_denominator(N-1).denominator

    return r


def GetHighLevelGates(eng, cmd):
    g = cmd.gate
    if g == QFT or get_inverse(g) == QFT or g == Swap:
        return True
    if isinstance(g, BasicMathGate):
        return False
        if isinstance(g, AddConstant):
            return True
        elif isinstance(g, AddConstantModN):
            return True
        return False
    return eng.next_engine.is_available(cmd)


if __name__ == "__main__":
    resourceCounter = ResourceCounter()
    rule_set = DecompositionRuleSet(modules=[projectq.libs.math,projectq.setups.decompositions])
    compilerengines = [AutoReplacer(rule_set),
                       InstructionFilter(GetHighLevelGates),
                       TagRemover(),
                       LocalOptimizer(3),
                       AutoReplacer(rule_set),
                       TagRemover(),
                       LocalOptimizer(3),
                       resourceCounter]

    engine = MainEngine(Simulator(), compilerengines)

    print(" Shor's Algorithm")
         
    Number = int(input('Input Number to be Factored '))
    print("\n\tFactoring the number Number = {}: \033[0m".format(Number), end="")

    aRand = int(random.random()*Number)
    if not gcd(aRand, Number) == 1:
        print("non relative prime by accident")
        
        print("Factors: ",gcd(aRand, Number))
    else:
        remainder = ExecuteShorAlgorithm(engine, Number, aRand, True)

        if remainder % 2 != 0:
            remainder *= 2
        apowrhalf = pow(aRand, remainder >> 1, Number)
        factor1 = gcd(apowrhalf + 1, Number)
        factor2 = gcd(apowrhalf - 1, Number)
        if ((not factor1 * factor2 == Number) and factor1 * factor2 > 1 and
                int(1. * N / (factor1 * factor2)) * factor1 * factor2 == N):
            factor1, factor2 = factor1*factor2, int(Number/(factor1*factor2))
        if factor1 * factor2 == Number and factor1 > 1 and factor2 > 1:
            print("Factors are : {} * {} = {}"
                  .format(factor1, factor2, Number))
        else:
            print("No Luck Found the factors {} and {}".format(factor1,factor2))

        print(resourceCounter)  
