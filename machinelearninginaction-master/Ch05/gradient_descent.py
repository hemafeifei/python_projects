import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
import numpy as np
import argparse


def sigmoid_activation(x):
    return 1.0/(1 + np.exp(-x))


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--epochs", type=float, default=100,
                help='# of epochs')
ap.add_argument("-a", "--alpha", type=float, default=0.01,
                help="learning rate")
args = vars(ap.parse_args())


# generate data
(X, y) = make_blobs(n_samples=250, n_features=2, centers=2,
                    cluster_std=1.05, random_state=42)
# add x0=1 to X data
X = np.c_[np.ones((X.shape[0])), X]

print("[INFO] starting training...")
W = np.zeros((X.shape[1],))


# initialize a list to store the loss value for each epoch
loss_history = []
for epoch in np.arange(0, args["epochs"]):
    preds = sigmoid_activation(X.dot(W))

    error = preds - y

    loss = np.sum(error ** 2)/(2*X.shape[0])
    loss_history.append(loss)
    print("[INFO] epoch # {}, loss={:.7f}".format(epoch +1, loss))

    gradient = X.transpose().dot(error)/X.shape[0]

    W += -args['alpha']* gradient
print(W)

# take some sample data to see the result
for i in np.random.choice(250, 10):
    activation = sigmoid_activation(X[i].dot(W))

    label = 0 if activation < 0.5 else 1

    print("activation = {:.2f}, predoction_label = {}, true_label = {}".format(activation, label, y[i]))

# Visualizing
Y = (-W[0] - (W[1]*X)) / W[2]

plt.figure()
plt.scatter(X[:, 1], X[:, 2], marker="o", c=y)
plt.plot(X, Y, "r--")


# construct a figure that plots the loss over time
fig = plt.figure()
plt.plot(np.arange(0, args["epochs"]), loss_history)
fig.suptitle("Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.show()