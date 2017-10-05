import numpy as np
import tensorflow as tf

# orゲートを学習するときの
x1 = np.array([0, 0])
x2 = np.array([1, 0])
x3 = np.array([0, 1])
x4 = np.array([1, 1])

y1 = np.array([0])
y2 = np.array([1])
y3 = np.array([1])
y4 = np.array([1])

w = tf.Variable(tf.zeros([2, 1]))
b = tf.Variable(tf.zeros([1]))
# をtensorflowで表すと
x = tf.placeholder(tf.float32, shape=[None, 2])
t = tf.placeholder(tf.float32, shape=[None, 1])
y = tf.nn.sigmoid(tf.matmul(x, w) + b)
# (placeholderという名前はデータを格納する入れ物)を示す
# 実際にこのplaceholderに値を入れるときは
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
Y = np.array([[0], [1], [1], [1]])

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

print('w:', sess.run(w))
print('b:', sess.run(b))

# x,t,yはあとから値を入れるplaceholderなので、
# 中身を確認するときはfeed_dictで値を入れる
print('x', sess.run(x, feed_dict={
    x: X
}))
print('t', sess.run(t, feed_dict={
    t: Y
}))
print('y',  sess.run(y, feed_dict={
    x: X,
    t: Y
}))

cross_entropy = - tf.reduce_sum(t * tf.log(y) + (1 - t) * tf.log(1 - y))
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(cross_entropy)

# 実際に訓練を回して重みとバイアスの変化、nnの出力内容変化を確認

for epoch in range(10):
    sess.run(train_step, feed_dict={
        x: X,
        t: Y
    })

print('10回回す')
print('w:', sess.run(w))
print('b:', sess.run(b))
print('y',  sess.run(y, feed_dict={
    x: X,
    t: Y
}))


for epoch in range(100):
    sess.run(train_step, feed_dict={
        x: X,
        t: Y
    })

print('100回回す')
print('w:', sess.run(w))
print('b:', sess.run(b))
print('y',  sess.run(y, feed_dict={
    x: X,
    t: Y
}))

for epoch in range(1000):
    sess.run(train_step, feed_dict={
        x: X,
        t: Y
    })

print('1000回回す')
print('w:', sess.run(w))
print('b:', sess.run(b))
print('y',  sess.run(y, feed_dict={
    x: X,
    t: Y
}))