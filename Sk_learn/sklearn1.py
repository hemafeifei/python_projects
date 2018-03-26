#2017.06
from sklearn import svm
from sklearn import datasets
from sklearn.linear_model import LassoCV
from sklearn.linear_model import Lasso
from sklearn.model_selection import KFold
k_fold = KFold(3)
iris = datasets.load_iris()
digits = datasets.load_digits()

# print (digits.data)

clf = svm.SVC(gamma=0, C=100)
clf.fit(digits.data[:-1], digits.target[:-1])

clf.predict(digits.data[-1:])


#function1
lasso_cv = LassoCV(alphas = alphas, random_state=0)
for k, (train, test) in enumerate(k_fold.split(X,y)):
    lasso_cv.fit(X[train], y[train])
    print("[fold{0} alpha:{1:5f}, score: {2:5f}]".format(k, lasso_cv.alpha_, lasso_cv.score(X[test], y[test])))

for train_idx, test_idx in k_fold.split(X):
    print ("Train: %s | test: %s" % (train_idx, test_idx))