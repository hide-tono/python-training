from keras.callbacks import TensorBoard
from keras.layers import *
from keras.models import *
from keras.optimizers import *
from sklearn import datasets
from sklearn.model_selection import train_test_split

N = 400
X, y = datasets.make_moons(N, noise=0.3)
# print(X)
# print(y)
# Y = y.reshape(N, 1)
# print(Y)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)

model = Sequential()
model.add(Dense(3, input_dim=2))
model.add(Activation('sigmoid'))
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.compile(loss='binary_crossentropy',
              optimizer=SGD(lr=0.05),
              metrics=['accuracy'])

model.fit(X_train, y_train, epochs=500, batch_size=20, callbacks=[TensorBoard(log_dir="log", histogram_freq=1)])
loss_and_metrics = model.evaluate(X_test, y_test)
print(loss_and_metrics)
