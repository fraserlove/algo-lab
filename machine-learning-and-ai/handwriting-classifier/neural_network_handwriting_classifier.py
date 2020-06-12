import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot = True)

# Network hyperparameters
learning_rate = 0.0001 # 1.95 for sigmoid activation function
batch_size = 10
update_step = 10

input_nodes = 784 # 28x38 images as input
layer_1_nodes = 500
layer_2_nodes = 500
layer_3_nodes = 500
output_nodes = 10

network_input = tf.placeholder(tf.float32, [None, input_nodes])
target_output = tf.placeholder(tf.float32, [None, output_nodes])

# Network model, weights and biases
layer_1 = tf.Variable(tf.random_normal([input_nodes, layer_1_nodes]))
layer_2 = tf.Variable(tf.random_normal([layer_1_nodes, layer_2_nodes]))
layer_3 = tf.Variable(tf.random_normal([layer_2_nodes, layer_3_nodes]))
output_layer = tf.Variable(tf.random_normal([layer_3_nodes, output_nodes]))

layer_1_bias = tf.Variable(tf.random_normal([layer_1_nodes]))
layer_2_bias = tf.Variable(tf.random_normal([layer_2_nodes]))
layer_3_bias = tf.Variable(tf.random_normal([layer_3_nodes]))
output_layer_bias = tf.Variable(tf.random_normal([output_nodes]))

# Feedforward calculations
layer_1_out = tf.nn.relu(tf.matmul(network_input, layer_1) + layer_1_bias)
layer_2_out = tf.nn.relu(tf.matmul(layer_1_out, layer_2) + layer_2_bias)
layer_3_out = tf.nn.relu(tf.matmul(layer_2_out, layer_3) + layer_3_bias)
network_out_1 = tf.matmul(layer_3_out, output_layer) + output_layer_bias
network_out_2 = tf.nn.softmax(network_out_1)

cost_function = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = network_out_1, labels = target_output))
training_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost_function)
predicitions = tf.equal(tf.argmax(network_out_2, 1), tf.argmax(target_output, 1))
accuracy = tf.reduce_mean(tf.cast(predicitions, tf.float32))

# Running the neural network
with tf.Session() as session:
    session.run(tf.global_variables_initializer())
    no_epochs = 10
    for epoch in range(no_epochs):
        total_cost = 0
        no_batches = int(mnist.train.num_examples / batch_size)
        for batch in range(no_batches):
            input_data, labels = mnist.train.next_batch(batch_size)
            step, cost = session.run([training_step, cost_function], feed_dict = {network_input: input_data, target_output: labels})
            total_cost += cost
        print('Epoch {} out of {} completed, loss: {}'.format(epoch, no_epochs, total_cost))
    print('Accuracy: {}'.format(accuracy.eval({network_input: mnist.test.images, target_output: mnist.test.labels})))
