import numpy as np
import operator as op
from functools import reduce

epsilon = 0.000001
class utils:
    def __init__(self):
        self.epsilon = epsilon

    def add(self , x1, x2):
        return (x1 + x2) / (1 + (x1 * x2) + epsilon)

    def subtract(self ,x1, x2):
        return (x1 - x2) / (1 - (x1 * x2) + epsilon)

    def mult(self ,lamda, x):
        nom = ((1 + x) ** lamda) - ((1 - x) ** lamda)
        denom = ((1 + x) ** lamda) + ((1 - x) ** lamda)
        return nom / (denom+epsilon )

    def fai(self ,x):
        return 0.5 * np.log((1 + x) / (1 - x + epsilon) )

    def norm(self ,x):
        return np.abs(utils.fai(self,x))

    def comb(self ,n, r):
        r = min(r, n - r)
        numer = reduce(op.mul, range(n, n - r, -1), 1)
        denom = reduce(op.mul, range(1, r + 1), 1)
        return numer / denom

    def colorAdd(self , q1,q2):
        res = []
        res.append(self.add(q1[0] , q2[0]))
        res.append(self.add(q1[1] , q2[1]))
        res.append(self.add(q1[2] , q2[2]))
        return res


    def colorSub(self , q1,q2):
        res = []
        res.append(self.subtract(q1[0] , q2[0]))
        res.append(self.subtract(q1[1] , q2[1]))
        res.append(self.subtract(q1[2] , q2[2]))
        return res

    def colorMult(self,lamda,q):
        res = []
        res.append(self.mult(lamda, q[0]))
        res.append(self.mult(lamda, q[1]))
        res.append(self.mult(lamda, q[2]))
        return res

    def colorNorm(self,q):
        res = 0
        res += self.fai(q[0])**2
        res += self.fai(q[1])**2
        res += self.fai(q[2])**2
        return np.sqrt(res)