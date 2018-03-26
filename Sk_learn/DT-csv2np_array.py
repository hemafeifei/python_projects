import numpy as np

def loadCSVfile2():
    tmp = np.loadtxt('train.csv', dtype = np.str, delimiter=',')
    df = tmp[1:,1:].astype(np.float)
    label = tmp[1:, 0]
    return df, label