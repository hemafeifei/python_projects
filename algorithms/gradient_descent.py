import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
import numpy as np
import argparse


# sigmoid function
def sigmoid_function(x):
    return 1.0/(1 + np.exp(-x))

