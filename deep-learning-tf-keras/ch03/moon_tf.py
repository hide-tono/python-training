import tensorflow as tf
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

N = 400
X, y = datasets.make_moons(N, noise=0.3)
# print(X)
# print(y)
Y = y.reshape(N, 1)
# print(Y)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.8)
num_hidden = 3
x = tf.placeholder(tf.float32, shape=[None, 2])
t = tf.placeholder(tf.float32, shape=[None, 1])

w = tf.Variable(tf.truncated_normal([2, num_hidden]))
b = tf.Variable(tf.zeros([num_hidden]))
h = tf.nn.sigmoid(tf.matmul(x, w) + b)

V = tf.Variable(tf.truncated_normal([num_hidden, 1]))
c = tf.Variable(tf.zeros([1]))
y = tf.nn.sigmoid(tf.matmul(h, V) + c)

cross_entropy = - tf.reduce_sum(t * tf.log(y) + (1 - t) * tf.log(1 - y))
train_step = tf.train.GradientDescentOptimizer(0.05).minimize(cross_entropy)
correct_prediction = tf.equal(tf.to_float(tf.greater(y, 0.5)), t)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# 学習
batch_size = 20
n_batches = N

init = tf.global_variables_initializer()
sess = tf.Session()

import os
LOG_DIR = os.path.join(os.path.dirname(__file__), 'log')
if os.path.exists(LOG_DIR) is False:
    os.mkdir(LOG_DIR)
tf.summary.FileWriter(LOG_DIR, sess.graph)
sess.run(init)

for epoch in range(500):
    if epoch % 10 == 0:
        print('epoch:', epoch)
    X_, Y_ = shuffle(X_train, Y_train)

    for i in range(n_batches):
        start = i * batch_size
        end = start + batch_size

        sess.run(train_step, feed_dict={
            x: X_[start:end],
            t: Y_[start:end]
        })

accuracy_rate = accuracy.eval(session=sess, feed_dict={
    x: X_test,
    t: Y_test
})

print('accuracy: ', accuracy_rate)
