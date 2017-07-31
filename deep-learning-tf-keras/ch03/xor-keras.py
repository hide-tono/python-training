# 線形でXORの分類に失敗する例
import numpy as np
from keras.layers import Dense, Activation
from keras.models import Sequential
from keras.optimizers import SGD

np.random.seed(0)

# XOR
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
Y = np.array([[0], [1], [1], [0]])

model = Sequential([Dense(input_dim=2, units=1),
                    Activation('sigmoid')])
model.compile(loss='binary_crossentropy', optimizer=SGD(lr=0.1))
model.fit(X, Y, epochs=200, batch_size=1)
prob = model.predict_proba(X, batch_size=1)
print('-------失敗例------')
print(prob)
print('-------------')

# keras XOR
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
Y = np.array([[0], [1], [1], [0]])

model = Sequential()
model.add(Dense(input_dim=2, units=2))
model.add(Activation('sigmoid'))
model.add(Dense(units=1))
model.add(Activation('sigmoid'))
model.compile(loss='binary_crossentropy', optimizer=SGD(lr=0.1))

model.fit(X, Y, epochs=6000, batch_size=4)

classes = model.predict_classes(X, batch_size=4)
prob = model.predict_proba(X, batch_size=4)

print('classified:')
print(np.argmax(model.predict(X), axis=1) == classes)
print()
print('output probability:')
print(prob)
