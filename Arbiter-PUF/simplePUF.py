# coding: utf-8

import numpy as np
from sklearn.linear_model import LogisticRegression


def randbool(shape):
    a = 2 * (np.random.rand(shape) > .5).astype(int) - 1
    a[shape-1] = 1
    return a

############################################################
#                   Arbiter PUF 
############################################################
N = 32      # PUF Size
tr = 100    # Training Set Size
ts = 10000  # Test Set Size 

# Weight vector
w = np.random.randn(N+1)

# Training Set
trsetX = np.array([randbool(N+1) for i in range(tr)])
trsetY = np.array([np.dot(p,w) for p in trsetX]) > 0

# Test Set
tssetX = np.array([randbool(N+1) for i in range(ts)])
tssetY = np.array([np.dot(p,w) for p in tssetX]) > 0


lr = LogisticRegression(fit_intercept=False,dual=False)
lr.fit(trsetX, trsetY) 

print "Score arbiter PUF (%d stages): %f" % (N,lr.score(tssetX,tssetY))



############################################################
#                   XOR Arbiter PUF (3 PUFs)
############################################################
N = 8      # PUF Size
tr = 100    # Training Set Size
ts = 10000  # Test Set Size 

# Weight vector
w1 = np.random.randn(N+1)
w2 = np.random.randn(N+1)
w3 = np.random.randn(N+1)

# Training Set
trsetX = np.array([randbool(N+1) for i in range(tr)])
res_1 = np.array([np.dot(p,w1) for p in trsetX]) > 0
res_2 = np.array([np.dot(p,w2) for p in trsetX]) > 0
res_3 = np.array([np.dot(p,w3) for p in trsetX]) > 0
trsetY = np.array([r1 ^ r2 ^ r3 for r1,r2,r3 in zip(res_1,res_2,res_3)])

# Test Set
tssetX = np.array([randbool(N+1) for i in range(ts)])
res_1 = np.array([np.dot(p,w1) for p in tssetX]) > 0
res_2 = np.array([np.dot(p,w2) for p in tssetX]) > 0
res_3 = np.array([np.dot(p,w3) for p in tssetX]) > 0
tssetY = np.array([r1 ^ r2 ^ r3 for r1,r2,r3 in zip(res_1,res_2,res_3)])


lr = LogisticRegression(fit_intercept=False,dual=False)
lr.fit(trsetX, trsetY) 

print "Score XOR PUF (%d stages): %f" % (N,lr.score(tssetX,tssetY))
