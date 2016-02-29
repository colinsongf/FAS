from __future__ import division

from sklearn.cross_validation import cross_val_score
from sklearn.tree import DecisionTreeRegressor

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import ensemble
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error

###############################################################################
# Load data

path='/home/asus/quickrank/data/Fold1/sample_train_features.txt'
df = pd.read_csv(path, sep="\t",nrows=1)
columns=df.columns.tolist()
colstouse=range(2,len(columns)-1)
y=pd.read_csv(path,
               sep="\t",
               skiprows=0,
               usecols=[0],
               nrows=150000).values

X=pd.read_csv(path,
               sep="\t",
               skiprows=0,
               usecols=colstouse,
               nrows=150000).values

offset = int(X.shape[0] * 0.8)
X_train, y_train = X[:offset], y[:offset]
X_test, y_test = X[offset:], y[offset:]

###############################################################################
# Fit regression model


params = {'n_estimators': 100, 'max_depth': 3, 'min_samples_split': 1,
          'learning_rate': 0.01, 'max_leaf_nodes': 6,'loss': 'ls'}
clf = ensemble.GradientBoostingRegressor(**params)

clf.fit(X_train, np.ravel(y_train))

mse = mean_squared_error(y_test, clf.predict(X_test))

print("MSE: %.4f" % mse)

###############################################################################
# Plot training deviance

# compute test set deviance

test_score = np.zeros((params['n_estimators'],), dtype=np.float64)

for i, y_pred in enumerate(clf.staged_predict(X_test)):
    test_score[i] = clf.loss_(y_test, y_pred)

plt.figure(figsize=(18, 36))
plt.subplot(1, 2, 1)
plt.title('Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, clf.train_score_, 'b-',
         label='Training Set Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-',
         label='Test Set Deviance')
plt.legend(loc='upper right')
plt.xlabel('Boosting Iterations')
plt.ylabel('Deviance')

###############################################################################
# Plot feature importance

feature_importance = clf.feature_importances_
# make importances relative to max importance
feature_importance = 100.0 * (feature_importance / feature_importance.max())
for i in feature_importance:
    print i
    
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + .5
plt.subplot(1, 2, 2)
plt.barh(pos, feature_importance[sorted_idx], align='center')
mynames=list(df)[2:138]
orderednames=[ mynames[i] for i in sorted_idx]
plt.yticks(pos, orderednames)
plt.xlabel('Relative Importance')
plt.title('Variable Importance')
plt.show()
'''
from sklearn.ensemble import RandomForestClassifier
clf= RandomForestClassifier(n_estimators=10)
clf.fit(X_train, y_train)
mse = mean_squared_error(y_test, clf.predict(X_test))
feature_importance = clf.feature_importances_
'''
