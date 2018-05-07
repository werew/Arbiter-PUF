# Source: https://gist.github.com/gabisurita/f315ae49f781bde8c626dc350df5ea7f
# coding: utf-8

# In[146]:

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

# PUF Size
N = 65
# Training Set Size
tr = 100
# Test Set Size 
ts = 10000

def randbool(shape):
    a = 2 * (np.random.rand(shape) > .5).astype(int) - 1
    a[shape-1] = 1
    return a


# In[147]:

# Weight vector
w = np.random.randn(N+1)
print w

# Training Set
trsetX = np.array([randbool(N+1) for i in range(tr)])
trsetY = np.array([np.dot(p,w) for p in trsetX]) > 0

print trsetX
print trsetY

# Test Set
tssetX = np.array([randbool(N+1) for i in range(ts)])
tssetY = np.array([np.dot(p,w) for p in tssetX]) > 0


wn = np.zeros(N+1)

# Parity Predictor
for p, y in zip(trsetX, trsetY):    
    
    # Invert challenge vector
    if not y:
        p = -p
    
    # Sum vector plane
    wn += p

# Parity predictor geom fit
wn /= max(wn)
fwn = wn.copy()
fwn[wn >=  0.75] =  1.
fwn[wn <= -0.75] = -1.
fwn[np.logical_and(wn >=  0.625 ,wn <  0.75)] =  .75
fwn[np.logical_and(wn <= -0.625 ,wn > -0.75)] = -.75
fwn[np.logical_and(wn >=  0.375 ,wn <  0.625)] =  .5
fwn[np.logical_and(wn <= -0.375 ,wn > -0.625)] = -.5
fwn[np.logical_and(wn >=  0.125 ,wn <  0.375)] =  .25
fwn[np.logical_and(wn <= -0.125 ,wn > -0.375)] = -.25
fwn[np.abs(wn) < .125] = 0

# In[149]:

lr = LogisticRegression(fit_intercept=False,dual=False)
lr.fit(trsetX, trsetY) 
lr.fit(-trsetX, ~trsetY)

# In[150]:

svm = LinearSVC(fit_intercept=False, dual=False)
svm.fit(trsetX, trsetY)
#svm.fit(-trsetX, ~trsetY)


# In[151]:

# Test parity predictior
pred = np.array([np.dot(p,wn) for p in tssetX]) > 0
print "Parity Vector", 1-sum(np.logical_xor(tssetY, pred))/float(ts)

pred = np.array([np.dot(p,fwn) for p in tssetX]) > 0
print "Fitted Parity Vector", 1-sum(np.logical_xor(tssetY, pred))/float(ts)

pred = lr.predict(tssetX)
print "Logistic Regression", 1-sum(np.logical_xor(tssetY, pred))/float(ts)

pred = svm.predict(tssetX)
print "Linear SVM", 1-sum(np.logical_xor(tssetY, pred))/float(ts)

