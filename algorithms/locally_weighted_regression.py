import numpy as np
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot


# Algorithm
def local_regression(x0, X, y, tau):
    # add bias term
    x0 = np.r_[1, x0]
    X = np.c_[np.ones(len(X)), X]

    # fit model
    xw = X.T * radial_kernel(x0, X, tau)
    beta = np.linalg.pinv(xw @ X) @ xw @ y

    # predict value
    return x0 @ beta


def radial_kernel(x0, X, tau):
    return np.exp(np.sum((X - x0)**2, axis=1)/(-2 * tau ** 2))

# make some data
n = 1000
X = np.linspace(-3, 3, num=n)
y = np.log(np.abs(X ** 2 -1) + .5)
# jitter X
X += np.random.normal(scale=.1, size=n)

# use bokeh plot data
def plot_lwr(tau):
    domain = np.linspace(-3, 3, num=300)
    prediction = [local_regression(x0, X, y, tau) for x0 in domain]

    plot = figure(plot_width=400, plot_height=400)
    plot.title.text = 'tau=%g' %tau
    plot.scatter(X, y, alpha=.3)
    plot.line(domain, prediction, line_width=2, color='red')
    return plot

show(gridplot([
    [plot_lwr(10.), plot_lwr(1.)],
    [plot_lwr(0.1), plot_lwr(0.01)]
]))