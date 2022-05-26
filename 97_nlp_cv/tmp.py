import numpy as np

def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

def _cross_entrophy(y_hat, y):
    if y == 1:
        return - np.log(y_hat)
    else:
        return - np.log(1 - y_hat)