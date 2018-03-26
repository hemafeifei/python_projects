import numpy as np
import pandas as pd

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

iris = datasets.load_iris()
train_data = iris.data
train_target = iris.target

model = DecisionTreeClassifier()
scores = cross_val_score(model, train_data, train_target, cv=4)
print (scores, scores.mean())

X_train, X_test, y_train, y_test = train_test_split(train_data, train_target, test_size=0.2, random_state=0)
# model.fit(X_train, y_train)
# print X_train.shape, y_test.shape
# print model.fit(X_train,y_train).score(X_test, y_test)
# print metrics.confusion_matrix(y_test, model.predict(X_test))
# print metrics.classification_report(y_test, model.predict(X_test))

