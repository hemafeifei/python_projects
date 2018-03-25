# The difference between vanilla gradient descent and SGD is the addition of
# the 'next_training_batch' function. Instead of computing our gradient over
# the entire dataset, we instead sample our data, yielding a 'batch'.
# The batch size can be 32, 64, 128, 256...(power of 2)
# In gerneral, you basically determine how many training examples weill fit
# on your GPU/main memory and the use the nearest power of 2 as the batch size.

import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
import numpy as np
import argparse


def sigmoid_function(x):
    return 1.0 / (1 + np.exp(-x))


def next_batch(X, y, batchsize):
    # loop over our dataset 'X' in mini-batches of size
    for i in np.arange(0, X.shape[0], batchsize):
        # yield a tuple of the current batched data and labels
        yield (X[i:i + batchsize], y[i: i + batchsize])


# Construct the argument parse
ap = argparse.ArgumentParser()
ap.add_argument('-e', '--epochs', type=float, default=10,
                help='# of epochs')
ap.add_argument('-a', '--alpha', type=float, default=0.01,
                help='learning rate')
ap.add_argument('-b', '--batch_size', type=int, default=32,
                help='size of SGD mini-batches')
args = vars(ap.parse_args())


# Generate dataset
(X, y) = make_blobs(n_samples=400, n_features=2, centers=2,
                    cluster_std=2.5, random_state=42)
X = np.c_[np.ones((X.shape[0])), X]
print("[INFO] starting training...")
W = np.random.uniform(size=(X.shape[1],))

# Initialize a loss list
loss_his = []

# Loop over the desired number of epochs
for epoch in np.arange(0, args['epochs']):
    epoch_loss = []

    for (batch_x, batch_y) in next_batch(X, y, args['batch_size']):
        preds = sigmoid_function(batch_x.dot(W))
        error = preds - batch_y

        loss = np.sum(error ** 2)
        epoch_loss.append(loss)

        gradient = np.dot(batch_x.T, error)/batch_x.shape[0]
        W += -args['alpha'] * gradient

    loss_his.append(np.average(epoch_loss))

Y = (-W[0] - (W[1]*X)) / W[2]

# Plot the orginial data along with our line of best fit
plt.figure()
plt.scatter(X[:, 1], X[:, 2], marker='o', c=y)
plt.plot(X, Y , 'r--')

# Plot the loss-training epochs curve
fig = plt.figure()
plt.plot(np.arange(0, args['epochs']), loss_his)
fig.suptitle("Training Loss")
plt.xlabel("Epoch of #")
plt.ylabel("Loss")
plt.show()

