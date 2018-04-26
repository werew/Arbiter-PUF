import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from arbiterPUF import ArbiterPUF
import random

N  = 65     # Size of PUF
LS = 200    # Size learning set
TS = 1000   # Size testing set

apuf = ArbiterPUF(N)

learningX = [[random.choice([0,1]) for _ in range(N)] for _ in range(LS)]
learningY = [apuf.get_output(chall) for chall in learningX]

testingX = [[random.choice([0,1]) for _ in range(N)] for _ in range(TS)]
testingY = [apuf.get_output(chall) for chall in testingX]

lr = LogisticRegression()
lr.fit(lX,lY)
print(lr.score(lX,lY))
print(lr.score(tX,tY))

"""
lX = 2*np.array(learningX) - 1
lY = 2*np.array(learningY) - 1
tX = 2*np.array(testingX) - 1
tY = 2*np.array(testingY) - 1

print(lX[:1])
lr = LogisticRegression()
lr.fit(learningX,learningY)
print(lr.score(learningX,learningY))
print(lr.score(testingX,testingY))
"""
