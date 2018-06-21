from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import sklearn
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV


def loadCSV(fname):
    X = []
    for line in open(fname):
        line = line.strip()
        data = list(map(float,line.split(' ')))
        X.append(data[:])
    return np.asarray(X)

X = loadCSV("traces_50_HW.csv")
Y = loadCSV("model_HW.csv")

X_train = X[0:6000,]
Y_train = np.ravel(Y[0:6000,])
print np.ravel(Y[0:6,])
Y_train = np.ravel(Y[0:6000,])
X_test = X[6000:10000,]
Y_test= np.ravel(Y[6000:10000,])

parameters = {'n_estimators':[200]}
RF = RandomForestClassifier()
clf = GridSearchCV(RF,parameters,cv=5,n_jobs=1,scoring='accuracy')
clf.fit(X_train,Y_train)
Y_pred_rf = clf.predict(X_test)
print(accuracy_score(Y_test,Y_pred_rf))


