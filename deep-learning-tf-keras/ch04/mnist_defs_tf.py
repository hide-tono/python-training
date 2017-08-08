import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

np.random.seed(0)
tf.set_random_seed(1234)


def inference(x, keep_prob, n_in, n_hiddens, n_out):
    def weight_variable(shape):
        initial = tf.truncated_normal(shape, stddev=0.01)
        return tf.Variable(initial)

    def bias_variable(shape):
        initial = tf.zeros(shape)
        return tf.Variable(initial)

    for i, n_hidden in enumerate(n_hiddens):
        if i == 0:
            input = x
            input_dim = n_in
        else:
            input = output
            input_dim = n_hiddens[i - 1]

        W = weight_variable([input_dim, n_hidden])
        b = bias_variable(n_hidden)

        h = tf.nn.relu(tf.matmul(input, W) + b)
        output = tf.nn.dropout(h, keep_prob)

    W_out = weight_variable([n_hiddens[-1], n_out])
    b_out = bias_variable([n_out])
    y = tf.nn.softmax(tf.matmul(output, W_out) + b_out)
    return y


def loss(y, t):
    cross_entropy = \
        tf.reduce_mean(-tf.reduce_sum(
            t * tf.log(tf.clip_by_value(y, 1e-10, 1.0)),
            reduction_indices=[1]
        ))
    return cross_entropy


def training(loss):
    optimizer = tf.train.GradientDescentOptimizer(0.01)
    train_step = optimizer.minimize(loss)
    return train_step


def accuracy(y, t):
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.arg_max(t, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    return accuracy


if __name__ == '__main__':
    mnist = datasets.fetch_mldata('MNIST original', data_home='.')
    n = len(mnist.data)
    N = 30000
    N_train = 20000
    N_validation = 4000
    indices = np.random.permutation(range(n))[:N]

    X = mnist.data[indices]
    y = mnist.target[indices]
    Y = np.eye(10)[y.astype(int)]

    X_train, X_test, Y_train, Y_test = \
        train_test_split(X, Y, train_size=N_train)

    X_train, X_validation, Y_train, Y_validation = \
        train_test_split(X_train, Y_train, test_size=N_validation)

    n_in = len(X[0])
    n_hiddens = [200, 200, 200]
    n_out = len(Y[0])
    p_keep = 0.5

    x = tf.placeholder(tf.float32, shape=[None, n_in])
    t = tf.placeholder(tf.float32, shape=[None, n_out])
    keep_prob = tf.placeholder(tf.float32)

    y = inference(x, keep_prob, n_in=n_in, n_hiddens=n_hiddens, n_out=n_out)
    loss = loss(y, t)
    train_step = training(loss)

    accuracy = accuracy(y, t)

    history = {
        'val_loss': [],
        'val_acc': []
    }

    epochs = 50
    batch_size = 200

    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)

    n_batches = N_train // batch_size

    for epoch in range(epochs):
        X_, Y_ = shuffle(X_train, Y_train)

        for i in range(n_batches):
            start = i * batch_size
            end = start + batch_size

            sess.run(train_step, feed_dict={
                x: X_[start:end],
                t: Y_[start:end],
                keep_prob: p_keep
            })

        val_loss = loss.eval(session=sess, feed_dict={
            x: X_validation,
            t: Y_validation,
            keep_prob: 1.0
        })
        val_acc = accuracy.eval(session=sess, feed_dict={
            x: X_validation,
            t: Y_validation,
            keep_prob: 1.0
        })

        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)

        print('epoch:', epoch, ' validation loss:', val_loss, ' validation accuracy:', val_acc)

        plt.rc('font', family='serif')
        fig = plt.figure()
        ax_acc = fig.add_subplot(111)
        ax_acc.plot(range(epochs), history['val_acc'],
                    label='acc', color='black')
        ax_loss = ax_acc.twinx()
        ax_loss.plot(range(epochs), history['val_loss'],
                     label='loss', color='gray')
        plt.xlabel('epochs')
        plt.savefig('mnist_tensorflow.eps')

        accuracy_rate = accuracy.eval(session=sess, feed_dict={
            x: X_test,
            t: Y_test,
            keep_prob: 1.0
        })
        print('accuracy: ', accuracy_rate)
