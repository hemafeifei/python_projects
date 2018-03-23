import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
import numpy as np
import argparse
plt.style.use('fivethirtyeight')


# sigmoid function
def sigmoid_function(x):
    return 1.0/(1 + np.exp(-x))

# set the argument parse
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--epochs", type=float, default=200,
                help="# of epochs")
ap.add_argument("-a", "--alpha", type=float, default=0.01,
                help="learning rate")
args = vars(ap.parse_args())

# make data
(X, y) = make_blobs(n_samples=300, n_features=2, centers=2,
                    cluster_std=1.1, random_state=42)
X = np.c_[np.ones((X.shape[0])), X]
# initialize our weight matrix
print("[INFO] starting training...")
W = np.random.uniform(size=(X.shape[1],))

# initialize a list to store the loss value to PLT
loss_history = []

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.scatter(X[:, 1], X[:, 2], marker='o', c=y)
plt.ion()
plt.show()
# loop over the epochs
for epoch in np.arange(0, args['epochs']):
    preds = sigmoid_function(X.dot(W))
    error = preds -y
    loss = np.sum(error**2)/X.shape[0]
    loss_history.append(loss)
    # print("[INFO] epoch #{}, loss={:.5f}".format(epoch+1, loss))

    gradient = np.dot(X.transpose(), error)/X.shape[0]
    W += -args['alpha']*gradient

    # Draw the boundary
    Y = (-W[0] - (W[1] * X)) / W[2]
    # if 'lines' in locals().keys():
    #     ax.lines.remove(lines[0])
    if epoch % 20 == 0:
        try:
            ax.lines.remove(lines[0])
        except Exception:
            pass

        lines = ax.plot(X, Y, 'r--')
        plt.pause(0.5)

# # Take 10 sample data to show the prediction
# for i in np.random.choice(300, 10):
#     activation = sigmoid_function(X[i].dot(W))
#     label = 0 if activation < 0.5 else 1
#     print("activation={:.4f}, prediction={}, true_label={}".format(activation, label, y[i]))


# # Plot the loss-learning curve
# fig = plt.figure()
# plt.plot(np.arange(0, args['epochs']), loss_history)
# fig.suptitle("Training Loss")
# plt.xlabel("Epoch #")
# plt.ylabel("Loss")
# plt.show()