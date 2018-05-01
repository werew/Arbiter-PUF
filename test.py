import numpy as np
from sklearn.linear_model import LogisticRegression
from arbiterPUF import ArbiterPUF
import random

N  = 65     # Size of the PUF
LS = 300    # Size learning set
TS = 10000  # Size testing set

apuf = ArbiterPUF(N)

learningX = [[random.choice([0,1]) for _ in range(N)] for _ in range(LS)] # Challenges
learningY = [apuf.get_output(chall) for chall in learningX] # Outputs PUF

testingX = [[random.choice([0,1]) for _ in range(N)] for _ in range(TS)] 
testingY = [apuf.get_output(chall) for chall in testingX]

#lr = LogisticRegression()
#lr.fit(learningX,learningY)
#print(lr.score(learningX,learningY))
#print(lr.score(testingX,testingY))

def into_features_vect(chall):
    phi = []
    for i in range(1,len(chall)):
        s = sum(chall[i:])
        if s % 2 == 0:
            phi.append(1)
        else:
            phi.append(-1)
    phi.append(1)
    return phi

learningX = [into_features_vect(c) for c in learningX]
testingX = [into_features_vect(c) for c in testingX]
lr = LogisticRegression()
lr.fit(learningX,learningY)
#print(lr.score(learningX,learningY))
print(lr.score(testingX,testingY))

# Some debugging
#print apuf._delays
#for i in range(LS):
#    print(learningX[i])
#    print(lX[i])
#    v = 0
#    for b,d in zip(lX[i],apuf._delays):
#        print b,"*",d,"+",
#        v += b*d
#        
#    print "= ",v

#print learningY
