'''
Created on Apr 7, 2014

@author: ehsan
'''

import theano
import theano.tensor as T
import numpy
from numpy import random

		
class HiddenLayer(object):
	
	def __init__(self, list_of_inputLayer_weight_tuple, n_dim,name,b=None, activation=T.tanh, extra_inputEmbedding_weight_tuple=None):
		self.list_of_inputLayer_weight_tuple = list_of_inputLayer_weight_tuple
		self.name=name
		self.rng =  numpy.random.RandomState(1234)
		if b is None:
			b_values = numpy.zeros((1,n_dim), dtype=theano.config.floatX)
			b = theano.shared(value=b_values, name='b', borrow=True)
		self.b=b
		self.activation = activation
		self.params=[]
		
		
		temp_output=self.b
		self.params = [self.b]
		for inputLayer_weight_tuple in self.list_of_inputLayer_weight_tuple:
				input_layer = inputLayer_weight_tuple[0]
				W = inputLayer_weight_tuple[1]
				temp_output += T.dot(input_layer.output, W)
				self.params=self.params+ input_layer.params
				
		if extra_inputEmbedding_weight_tuple is not None:
			self.extra_embeddings_weight_tuple = extra_inputEmbedding_weight_tuple
			for emb_weight_tuple in extra_inputEmbedding_weight_tuple:
				input_emb = emb_weight_tuple[0]
				W_string = emb_weight_tuple[1]
							
				if W_string=="identity":
					W_values = numpy.identity(n_dim,dtype=theano.config.floatX )
					W=theano.shared(value=W_values, name=self.name+'-identity', borrow=True)
				else:
					W_values = np.asarray( self.rng.uniform(low=-10, high=10, size=(n_dim, n_dim)  ) ,dtype=theano.config.floatX )
					W = theano.shared(value=W_values, name=self.name+"W", borrow=True)
				
				temp_output += T.dot(input_emb, W)
				self.params += W
					
		self.output = (temp_output if activation is None else activation(temp_output))
		
		
		
		
	def __str__(self):
		s=" "+ self.name+":["
		
		for child in self.list_of_inputLayer_weight_tuple:
			s=s+" ("+child[2]+"*"+child[0].__str__()+") "
		for child in self.extra_embeddings_weight_tuple:
			s=s+" ("+child[2]+"*"+self.name+") "
		s=s+"] "
		return s
	
	def output_test(self):
		return self.activation+'('+self.W+'*'+input+'+'+self.b+')'
	
	
class InputLayer(object):
	def __init__(self,word_embedding,n_dim,name):
		self.name=name
		W_values = numpy.identity(n_dim,dtype=theano.config.floatX )
		self.W=theano.shared(value=W_values, name="identity", borrow=True)
		self.output=T.dot(word_embedding,self.W)
		self.params=[]
	def __str__(self):
		return self.name+":[(1*"+self.name+")]"		