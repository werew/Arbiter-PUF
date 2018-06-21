
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import scipy
from scipy.stats import multivariate_normal
from sklearn.metrics import accuracy_score


# ## HW model

# In[2]:


# Let's first load the data
mhw = pd.read_csv("lab/model_HW.csv",header=None)
thw = pd.read_csv("lab/traces_50_HW.csv",header=None,sep='\s+')

trainsize = 25000
y_train = mhw.iloc[:trainsize]
x_train = thw.iloc[:trainsize]
y_test  = mhw.iloc[trainsize:50000]
x_test  = thw.iloc[trainsize:50000]


# In[3]:


# Build pdf for each HW
pdfs = []
for hw in range(0,9):
    mean_matrix = x_train[y_train[0] == hw].mean()
    cov_matrix  = scipy.cov(x_train[y_train[0] == hw],rowvar=False)
    pdfs.append(multivariate_normal(mean_matrix,cov_matrix))


# In[4]:


# Try to predict HW using a single trace (we just pick the best guess)
predict = lambda trace: np.argmax(map(lambda p: p.pdf(trace), pdfs))
y_pred  = x_test.apply(predict,axis=1)
print accuracy_score(y_test,y_pred)


# In[5]:


# Try to predict HW using a using multiple traces (see https://wiki.newae.com/Template_Attacks "Combining the Results")
y_pred = []
for hw in range(0,9):
    tmp = []
    for p in pdfs:
        probs = p.pdf(x_test[y_test[0] == hw])
        tmp.append(reduce(lambda x,y: x+np.log(y), probs,0))
    y_pred.append(np.argmax(tmp))
    
print accuracy_score(range(0,9),y_pred)


# ## Value model

# In[6]:


# Let's first load the data
mhw = pd.read_csv("lab/model_value.csv",header=None)
thw = pd.read_csv("lab/traces_50_Value.csv",header=None,sep='\s+')


trainsize = 25000
y_train = mhw.iloc[:trainsize]
x_train = thw.iloc[:trainsize]
y_test  = mhw.iloc[trainsize:50000]
x_test  = thw.iloc[trainsize:50000]


# In[7]:


# Build pdf for each value
pdfs = []
for value in range(0,255):
    mean_matrix = x_train[y_train[0] == value].mean()
    cov_matrix  = scipy.cov(x_train[y_train[0] == value],rowvar=False)
    pdfs.append(multivariate_normal(mean_matrix,cov_matrix))


# In[8]:


# Try to predict values using a single trace (we just pick the best guess)
predict = lambda trace: np.argmax(map(lambda p: p.pdf(trace), pdfs))
y_pred = x_test.apply(predict,axis=1)
print accuracy_score(y_test,y_pred)


# In[9]:


# Try to predict values using a using multiple traces (see https://wiki.newae.com/Template_Attacks "Combining the Results")
y_pred = []
for value in range(0,255):
    tmp = []
    for p in pdfs:
        probs = p.pdf(x_test[y_test[0] == value])
        if isinstance(probs,np.float64): probs = [probs]
        tmp.append(reduce(lambda x,y: x+np.log(y), probs,0))
    y_pred.append(np.argmax(tmp))

print accuracy_score(range(0,255),y_pred)

