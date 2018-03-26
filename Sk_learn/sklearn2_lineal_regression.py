import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

X = [[1],[2],[3],[4],[5],[6]]
y = [[1],[2.1],[2.9],[4.2],[5.1],[5.8]]
# X.reshape(-1,1)
model = LinearRegression()
model.fit(X,y)
prediction = model.predict([13])[0]
X2 = [[0],[2.5],[5.3],[9.1]]
y2 = model.predict(X2)
# print(prediction)

#plot the result
plt.figure()
plt.title('lineal regression')
plt.xlabel('x value')
plt.ylabel('y value')
plt.axis([0,10,0,10])
plt.grid(True)
plt.plot(X, y, 'k.')
plt.plot(X2, y2, 'g-')
plt.show()

