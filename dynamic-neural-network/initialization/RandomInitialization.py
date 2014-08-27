'''
Created on May 7, 2014

@author: ehsan
'''

import re
import theano
import numpy as np
import numpy.random
class RandomInitialization(object):
	'''
	classdocs
	'''


	def __init__(self,rng):
		'''
		Constructor
		'''
		self.regex = re.compile("-\d+$")
		self.rng=rng
		pass
	
	def initialize (self,dataset,dim_size):
		weights=dict()
		word_one_hot_dict=dict()
		for datapoint in dataset:
		 
			depGraph = datapoint["depGraph"]	
			(dep_labels,words) = self.parse(depGraph)
			for word in words:
				if not word_one_hot_dict.has_key(word):
					word_emb_values = np.asarray( self.rng.uniform(low=-10, high=10, size=(1,dim_size)  ) ,dtype=theano.config.floatX )
					#??? borrow
					word_one_hot_dict[word] = theano.shared(value=word_emb_values, name = word, borrow=True)
			for dep_label in dep_labels:
				if not weights.has_key(dep_label):
					weight = np.asarray( self.rng.uniform(low=-10, high=10, size=(dim_size,dim_size)  ) ,dtype=theano.config.floatX )
					weights[dep_label] = theano.shared(value=weight, name=dep_label, borrow=True)
		return (weights,word_one_hot_dict)
					
	def initialize_one_hot (self,dataset,dim_size):	
		dep_labels_set=set()
		words_set=set()
		index=0
		for datapoint in dataset:
			depGraph = datapoint["depGraph"]
			(dep_labels,words) = self.parse(depGraph)
			for word in words:
				words_set.add(word)
			for dep_label in dep_labels:
				dep_labels_set.add(dep_label)
		word2index_dict = dict( zip (words_set,range(len(words_set))) )
		weights= dict( zip(words_set, theano.shared(value=np.asarray( self.rng.uniform(low=-10, high=10, size=(len(words_set),dim_size)  ) ,dtype=theano.config.floatX ), name=word+"-W-1hot2emb", borrow=True) ) )
		weights.update( zip (dep_labels_set,theano.shared(value=np.asarray( self.rng.uniform(low=-10, high=10, size=(dim_size,dim_size)  ) ,dtype=theano.config.floatX ), name=dep_label, borrow=True)  )  )  
		
		return (weights,word2index_dict)
		
		
			
			
	
	@staticmethod
	def get_one_hot_vector(word,word2index_dict):
		#check for not being available
		index=word2index_dict[word]
		max_len= len(word2index_dict)
		tmp_vector = numpy.zeros((1,max_len),dtype = theano.config.floatX)
		tmp_vector[index]=1
		return tmp_vector
				
		
	def parse(self,depGraph):
		edges = depGraph.split('\n')
		dep_labels=set()
		words=set()
		for edge in edges:
			tokens = edge.split('(')
			dep_label = tokens[0].strip()
			# filter aux and cop
			if (dep_label in ['cop', 'aux','root']):
				continue
			dep_labels.add(dep_label)
			args = tokens[1]
			args = args[0:len(args) - 1]
			arg1, arg2 = args.split(',')
			arg1 = arg1.strip()
			arg2 = arg2.strip()
			print arg1,arg2
			
			arg1se=self.regex.search(arg1) if arg1!="ROOT" else None
			arg2se=self.regex.search(arg2) if arg2!="ROOT" else None
			if arg1se is not None:
				words.add(arg1[:arg1se.start()])
			if arg2se is not None:
				words.add(arg2[:arg2se.start()])
			
			
		return (dep_labels,words)
	
	
	
if __name__=='__main__':
	depGraph = "nsubj(president-6, Obama-1)\ncop(president-6, is-2)\ndet(president-6, the-3)\n \
 	amod(president-6, black-5)\namod(black-5, first-4)\nroot(ROOT-0, president-6)\n\
 	prep_of(president-6, USA-8)"
 	
 	datapoint1={"depGraph":depGraph, "head":"president", "arg1":"Obama" , "arg2":"USA"}
 	dataset=[datapoint1]
 	rng = numpy.random.RandomState(1234)
 	
 	r= RandomInitialization(rng)
 	(w1,w2) = r.initialize(dataset, 10)
 	
 	print w1['prep_of'].eval()
 	