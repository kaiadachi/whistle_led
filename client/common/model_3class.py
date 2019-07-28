import tensorflow as tf

def weight_variable(shape):
  initial = tf.random.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

class Model:
    def __init__(self, data_len):
        self.input_size, self.output_size = data_len[0], data_len[1]

        # input
        self.x = tf.compat.v1.placeholder( tf.float32, [None, self.input_size] )

        # target
        self.labels = tf.compat.v1.placeholder(tf.int64,[None])
        self.y_ = tf.one_hot(self.labels, depth=self.output_size, dtype=tf.float32)
        self.init_model()

        # accuracy
        self.correct_prediction = tf.equal(tf.argmax(self.y_softmax,1), tf.argmax(self.y_,1))
        self.accuracy = tf.reduce_mean( tf.cast(self.correct_prediction, tf.float32) )

        self.loss = tf.reduce_mean(
            -tf.reduce_sum(self.y_ * tf.math.log(self.y_softmax), reduction_indices=[1])
        )

        # optimizer
        self.train_step = tf.compat.v1.train.AdamOptimizer(1e-4).minimize(self.loss)
        
        self.saver = tf.compat.v1.train.Saver(tf.compat.v1.global_variables())

        self.sess = tf.compat.v1.Session()
        
        self.sess.run(tf.compat.v1.global_variables_initializer())

    def init_model(self):
        num_fc1 = 128
        num_fc2 = 128
        num_fc3 = 128
        
        w_fc1 = weight_variable( [self.input_size, num_fc1] )
        b_fc1 = bias_variable([num_fc1])
        h_fc1 = tf.nn.relu( tf.matmul(self.x, w_fc1) + b_fc1 )

        w_fc2 = weight_variable( [num_fc1, num_fc2] )
        b_fc2 = bias_variable([num_fc2])
        h_fc2 = tf.nn.relu( tf.matmul(h_fc1, w_fc2) + b_fc2 )

        w_fc3 = weight_variable( [num_fc2, num_fc3] )
        b_fc3 = bias_variable([num_fc3])
        h_fc3 = tf.nn.relu( tf.matmul(h_fc2, w_fc3) + b_fc3 )

        w_fc4 = weight_variable( [num_fc3, self.output_size] )
        b_fc4 = bias_variable( [self.output_size] )
        
        self.y_softmax = tf.nn.softmax(tf.matmul(h_fc3, w_fc4) + b_fc4)

    def get_softmax(self, inp):
        output = self.sess.run( self.y_softmax, feed_dict={self.x:inp} )
        return output

    def get_pred(self, inp, label):
        pred = self.sess.run( tf.cast(self.correct_prediction, tf.float32), 
            feed_dict={self.x:inp, self.labels:label})
        return pred
    
    def get_maxindex(self,inp):
        return tf.argmax( self.get_softmax(inp),1)

    def update_model(self, inp, label):
        self.sess.run( self.train_step, feed_dict={self.x:inp, self.labels:label})

    def save_model(self, fname):
        self.saver.save(self.sess, fname)

    def load_model(self, fname):
        self.saver.restore(self.sess, fname)


