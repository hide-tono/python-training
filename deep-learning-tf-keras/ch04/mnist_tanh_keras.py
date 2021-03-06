import numpy as np
from keras.callbacks import TensorBoard
from keras.layers.core import Dense, Activation
from keras.models import Sequential
from keras.optimizers import SGD
from sklearn import datasets
from sklearn.model_selection import train_test_split

np.random.seed(0)

mnist = datasets.fetch_mldata('MNIST original', data_home='.')

n = len(mnist.data)
N = 10000

indices = np.random.permutation(range(n))[:N]

X = mnist.data[indices]
y = mnist.target[indices]
Y = np.eye(10)[y.astype(int)]

print(y.astype(int))
print('length of Y:', len(Y))

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.8)

n_in = len(X[0])
n_hidden = 200
n_out = len(Y[0])

model = Sequential()
model.add(Dense(n_hidden, input_dim=n_in))
model.add(Activation('tanh'))

model.add(Dense(n_hidden))
model.add(Activation('tanh'))

model.add(Dense(n_hidden))
model.add(Activation('tanh'))

model.add(Dense(n_out))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer=SGD(lr=0.01),
              metrics=['accuracy'])

epochs = 100
batch_size = 200

model.fit(X_train, Y_train, epochs=epochs, batch_size=batch_size, callbacks=[TensorBoard(log_dir="log", histogram_freq=1)])

loss_and_metrics = model.evaluate(X_test, Y_test)
print(loss_and_metrics)
