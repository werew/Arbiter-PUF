import numpy as np
from sklearn.linear_model import LogisticRegression
from arbiterPUF import ArbiterPUF
from XorPUF import XorPUF
import random

def into_features_vect(chall):
    "Transforms a challenge into a feature vector"
    phi = []
    for i in range(1,len(chall)):
        s = sum(chall[i:])
        if s % 2 == 0:
            phi.append(1)
        else:
            phi.append(-1)
    phi.append(1)
    return phi

############################################################
#                   Arbiter PUF 
############################################################
N  = 32     # Size of the PUF
LS = 100    # Size learning set
TS = 10000  # Size testing set
apuf = ArbiterPUF(N)

# Creating training suite
learningX = [[random.choice([0,1]) for _ in range(N)] for _ in range(LS)] # Challenges
learningY = [apuf.get_output(chall) for chall in learningX] # Outputs PUF

# Creating testing suite
testingX = [[random.choice([0,1]) for _ in range(N)] for _ in range(TS)] 
testingY = [apuf.get_output(chall) for chall in testingX]

# Convert challenges into feature vectors
learningX = [into_features_vect(c) for c in learningX]
testingX = [into_features_vect(c) for c in testingX]

# Prediction
lr = LogisticRegression()
lr.fit(learningX,learningY)
print "Score arbiter PUF (%d stages): %f" % (N,lr.score(testingX,testingY))


############################################################
#                   XOR Arbiter PUF (3 PUFs)
############################################################
N  = 8      # Size of the PUF
LS = 100    # Size learning set
TS = 10000  # Size testing set
apuf = XorPUF(N,3)

# Creating training suite
learningX = [[random.choice([0,1]) for _ in range(N)] for _ in range(LS)] # Challenges
learningY = [apuf.get_output(chall) for chall in learningX] # Outputs PUF

# Creating testng suite
testingX = [[random.choice([0,1]) for _ in range(N)] for _ in range(TS)] 
testingY = [apuf.get_output(chall) for chall in testingX]

# Convert challenges into feature vectors
learningX = [into_features_vect(c) for c in learningX]
testingX = [into_features_vect(c) for c in testingX]

# Prediction 
lr = LogisticRegression()
lr.fit(learningX,learningY)
print "XOR PUF (%d stages): %f" % (N,lr.score(testingX,testingY))
