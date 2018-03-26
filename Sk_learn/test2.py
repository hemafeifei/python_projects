import numpy as np
from sklearn import datasets, svm
digits = datasets.load_digits()
X_data = digits.data
y_data = digits.target
svc = svm.SVC( kernel='linear')
svc.fit(X_data[:-500], y_data[:-500])
score = svc.score(X_data[-500:], y_data[-500:])
print (score)

# # use np.array_split to create n-fold validation
# X_fold = np.array_split(X_data,3)
# y_fold = np.array_split(y_data,3)
# scores = list()
# for k in range(3):
#     X_train = list(X_fold)
#     X_test = X_train.pop(k)
#     X_train = np.concatenate(X_train)
#
#     y_train =list(y_fold)
#     y_test = y_train.pop(k)
#     y_train = np.concatenate(y_train)
#     scores.append(svc.fit(X_train, y_train).score(X_test, y_test))
# print scores

from sklearn.model_selection import KFold, cross_val_score
kfold = KFold(n_splits=3)
[svc.fit(X_data[train], y_data[train]).score(X_data[test], y_data[test]) for train, test in kfold.split(X_data)]

print (cross_val_score(svc, X_data, y_data,cv=kfold, n_jobs=1))
