from scipy import linalg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import colors
from sklearn.discriminant_analysis import LinearClassifierMixin, QuadraticDiscriminantAnalysis
import pandas as pd

#设定一个可线性变化的colormap
cmap = colors.LinearSegmentedColormap(
    'red_blue_classes', {'red': [(0,1,1), (1,0.7,0.7)],
                         'green': [(0,0.7,0.7), (1,0.7,0.7)],
                         'blue': [(0,0.7,0.7),(1,1,1)]})
plt.cm.register_cmap(cmap=cmap)

values = np.arange(0,1.1,0.1)
cmap_values = mpl.cm.get_cmap('red_blue_classes')(values)

pd.set_option('precision',2)
df = pd.DataFrame(np.hstack((values.reshape(11,1), cmap_values)))
df.columns = ['Value', 'R', 'G', 'B', 'Alpha']
# print(df)

