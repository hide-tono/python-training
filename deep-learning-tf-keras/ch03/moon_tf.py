import numpy as np
from sklearn import datasets
import tensorflow as tf
from sklearn.model_selection import train_test_split

N = 400
X,  y = datasets.make_moons(N, noise=0.3)
# print(X)
# print(y)
Y = y.reshape(N, 1)
# print(Y)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.8)
num_hidden = 2
x = tf.placeholder(tf.float32, shape=[None, 2])
t = tf.placeholder(tf.float32, shape=[None, 1])

w = tf.Variable(tf.truncated_normal([2, num_hidden]))
b = tf.Variable(tf.zeros([num_hidden]))
h = tf.nn.sigmoid(tf.matmul(x, W) + b)

V = tf.Variable(tf.truncated_normal([num_hidden], 1))
c = tf.Variable(tf.zeros([1]))
y = tf.nn.sigmoid(tf.matmul(h, V) + c)

cross_entropy = - tf.reduce_sum(t * tf.log(y) + (1 - t) * tf.log(1 - y))