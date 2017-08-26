import tensorflow as tf

class VariableLengthModel:
    constIntermediateSize = 30
    variableIntermediateSize = 300

    def __init__(self, constPartSize, variablePartSize, targetSize):
        #create the data holding variables
        self.constInputs = tf.placeholder(tf.float32, [None, constPartSize])
        self.variableInputs = tf.placeholder(tf.float32, [None, None, variablePartSize])
        self.targets = tf.placeholder(tf.float32, [None, targetSize])
        #network for the constant part
        self.constNet = self._makeNet(self.constInputs, 
                            [constPartSize, 50, constIntermediateSize])
        #network for the variable part
        self.variableNet = self._maxPoolingLayer(self._makeNet(self.variableInputs, 
                            [variablePartSize, 50, variableIntermediateSize]))
        #intermediate values from the two preprocessing networks
        self.intermediateRepr = tf.concat(concat_dim, [self.constNet,self.variableNet], name='concat')
        
        self.outputNet = self._makeNet(self.intermediateRepr,
                    [self.constIntermediateSize+self.variableIntermediateSize, 50, targetSize])
    
    def _makeHiddenLayer(self, inData, inputs, outputs):
        W = tf.Variable(tf.random_uniform([inputs, outputs],0.,1./inputs**0.5))
        b = tf.Variable(tf.zeros([outputs]))
        return tf.nn.elu(tf.matmul(inData, W) + b)
    
    def _makeOutputLayer(self, inData, inputs, outputs):
        W = tf.Variable(tf.random_uniform([inputs, outputs],0.,1./inputs**0.5))
        b = tf.Variable(tf.zeros([outputs]))
        return tf.nn.softmax(tf.matmul(inData, W) + b)
    
    def _maxPoolingLayer(self, inData):
        return tf.reduce_max(inData, reduction_indices=[1])
    
    def _makeNet(self, inData, layerData):
        d = inData
        for i in range(len(layerData)-1):
            d = self._makeHiddenLayer(d, layerData[i],layerData[i]+1)
        return d
    
    def _formatVariableBatch(self, data):
        """
        TODO: transform the variable sized data into const data padded by 0's?
        """
        pass
        
    def saveModel(self, fname):
        """
        TODO: implement save/load
        """
        pass
    
    def loadModel(self, fname):
        """
        TODO: implement save/load
        """
        pass
    
            
    def train(self, constValues, variableValues, targetValues):
        """
        constValues is a list of same-sized 1d vectors (ie a matrix)
        variableValues is a list of matrices with the last dimension same-sized
        targetValues is similar in format to constValues
        """
        cross_entropy = tf.reduce_mean(-tf.reduce_sum(self.targets * tf.log(self.outputNet), reduction_indices=[1]))
        """
        TODO: cross entropy is wrong for this kind fo training
        """
        train_step = tf.train.AdamOptimizer(0.5).minimize(cross_entropy)
        self.sess = tf.InteractiveSession()
        tf.global_variables_initializer().run()
        for _ in range(1000):
            """
            TODO: rewrite batching - we may need batches of 1?
            """
            batch_xs, batch_ys = mnist.train.next_batch(100)
            self.sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
        correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print(self.sess.run(accuracy, feed_dict={
                    self.constInputs: constValues,
                    self.variableInputs: self._formatVariableBatch(variableValues),
                    self.targets: targetValues}))
    
    def evaluate(self, constValues, variableValues):
        """
        TODO: validate this
        """
        return self.sess.run(self.outputNet, feed_dict={
                    self.constInputs: constValues,
                    self.variableInputs: variableValues.reshape(1,
                                                    variableValues.shape[0],
                                                    variableValues.shape[1])})
