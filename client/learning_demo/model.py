import tensorflow as tf

def weight_variable(shape):
  initial = tf.random.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

class Model:
    def __init__(self, data_len):
        # self.in_h, self.in_w, self.in_c = input_shape[0], input_shape[1], input_shape[2]
        self.input_size = data_len
        # input
        self.x = tf.compat.v1.placeholder( tf.float32, [None, self.input_size] )
        # self.x = tf.placeholder( tf.float32, [None, self.in_h, self.in_w, self.in_c], name="input")

        # target
        self.y_ = tf.compat.v1.placeholder( tf.float32, [None,1] )
        self.init_model()

        # accuracy
        self.correct_prediction = tf.equal(tf.round(self.y_sig), self.y_)
        self.accuracy = tf.reduce_mean( tf.cast(self.correct_prediction, tf.float32) )

        self.loss = tf.reduce_mean(
            tf.nn.sigmoid_cross_entropy_with_logits(labels=self.y_, logits=self.y_fc)
        )

        # optimizer
        self.train_step = tf.compat.v1.train.AdamOptimizer(1e-4).minimize(self.loss)
        
        self.saver = tf.compat.v1.train.Saver(tf.compat.v1.global_variables())

        self.sess = tf.compat.v1.Session()
        
        self.sess.run(tf.compat.v1.global_variables_initializer())

    def init_model(self):
        num_fc1 = 256
        num_fc2 = 256
        num_fc3 = 256
        
        w_fc1 = weight_variable( [self.input_size, num_fc1] )
        b_fc1 = bias_variable([num_fc1])
        h_fc1 = tf.nn.relu( tf.matmul(self.x, w_fc1) + b_fc1 )

        w_fc2 = weight_variable( [num_fc1, num_fc2] )
        b_fc2 = bias_variable([num_fc2])
        h_fc2 = tf.nn.relu( tf.matmul(h_fc1, w_fc2) + b_fc2 )

        w_fc3 = weight_variable( [num_fc2, num_fc3] )
        b_fc3 = bias_variable([num_fc3])
        h_fc3 = tf.nn.relu( tf.matmul(h_fc2, w_fc3) + b_fc3 )

        w_fc4 = weight_variable( [num_fc3, 1] )
        b_fc4 = bias_variable( [1] )
        
        self.y_fc = tf.matmul(h_fc3, w_fc4) + b_fc4
        self.y_sig = tf.nn.sigmoid(self.y_fc)

    def get_sigout(self, inp):
        output = self.sess.run( self.y_sig, feed_dict={self.x:inp} )
        return output

    def get_pred(self, inp, label):
        pred = self.sess.run( tf.cast(self.correct_prediction, tf.float32), 
            feed_dict={self.x:inp, self.y_:label})
        return pred
    
    def update_model(self, inp, label):
        self.sess.run( self.train_step, feed_dict={self.x:inp, self.y_:label})

    def save_model(self, fname):
        self.saver.save(self.sess, fname)

    def load_model(self, fname):
        self.saver.restore(self.sess, fname)


