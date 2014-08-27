'''
Created on Apr 7, 2014

@author: ehsan
'''
import pprint
import numpy as np
from numpy import random
import theano
import theano.tensor as T
from theano import function
import re
import Layers
from initialization import RandomInitialization
class NeuralNetworkFactory(object):
	#rng = random.RandomState(1234)
	def __init__(self,):
		self.regex = re.compile("-\d+$")
		
	
	def create(self, datapoint, n_dim,dep_weights,word_embeddings):
		
		pp = pprint.PrettyPrinter(indent=4)
		edges = self.parse(datapoint)
		
			
		''' 
		[ {president-6:[ (Obama-1,nsubj),(is-2, cop),(the-3, det), (black-5,amod),(USA-8,prep_of)  ],   ] 
		   black-5: [ (first-4,amod) ],
		   ROOT-0: [ (president-6:root)  ]
		'''
		#filteredEdges = self.__filter(edges, depArcs, arguments)
		pp.pprint(edges)
		
		network=self.__create_network ('ROOT-0',edges,datapoint, n_dim,dep_weights,word_embeddings)
		# filteredEdges = self.filter(edges) 
		# (arg1Dep, arg2Dep) = self.extract_arguments(filteredEdges)
		
		
		return network
		
	def __create_network (self,head_node,edges,datapoint, n_dim,dep_weights,word_embeddings):
		if head_node=='ROOT-0':
			edge = edges[head_node][0]
# 			print "edge",edge
			word=edge[1]
			dep_label = edge[0]
			#W =dep_weights[dep_label]
			layer = self.__create_network(word,edges,datapoint, n_dim, dep_weights,word_embeddings)
			#layer = Layers.HiddenLayer(self.__creat_network(word,edges,n_dim,dep_weights,word_embeddings).output,n_dim, n_dim, W,b=0, activation=T.tanh)
			return layer
		else:
			if edges.has_key(head_node):
				dependents = edges[head_node]
				dependent_layers =[]
				#make hidden layer
				#???
				#be careful about  args
				for dependent in dependents:
					word = dependent[1]
					dependent_layer = self.__create_network(word,edges,datapoint, n_dim, dep_weights,word_embeddings)
					dependent_weight = dep_weights[dependent[0]]
					dependent_layers.append(  (dependent_layer,dependent_weight,dependent[0]))
				#headword_layer = Layers.InputLayer(word_embeddings[self.__norm(head_node)],n_dim,self.__norm(head_node))
				#dependent_layers.append(  (headword_layer, headword_layer.W,"1"))
				direct_embedding_weights_tuple = (word_embeddings[self.__norm(head_node)],"identity","1")
				return Layers.HiddenLayer(dependent_layers,n_dim,self.__norm(head_node),extra_inputEmbedding_weight_tuple=[direct_embedding_weights_tuple])	
				
			else:
				#make input layer
				headword_layer = Layers.InputLayer(word_embeddings[self.__norm(head_node)],n_dim,name=self.__norm(head_node))
				return headword_layer
		
			
		
	def create2(self, datapoint, n_dim,weights,word2index_dict):
		pass
	
	def parse (self, datapoint):
		depGraph=datapoint["depGraph"]
		edges = depGraph.split('\n')
		edgeDict = dict()
		dep_labels=set()
		words=set()
		for edge in edges:
			tokens = edge.split('(')
			dep_label = tokens[0].strip()
			# filter aux and cop
			if (dep_label in ['cop', 'aux']):
				continue
			dep_labels.add(dep_label)
			nodes = tokens[1]
			nodes = nodes[0:len(nodes) - 1]
			node1, node2 = nodes.split(',')
			node1 = node1.strip()
			node2 = node2.strip()
			#??? refining arg1 and arg2 and exclude it 
			words.add(node1)
			words.add(node2)
			key = node1
			value = (dep_label, node2)
			if key in edgeDict.keys():
				values = edgeDict[key]
				
				values.append(value)
				edgeDict[key] = values
			else:
				edgeDict[key] = [value]
			

		return edgeDict
	
	def __norm(self, name):
# 		print "name",name
		name_se=self.regex.search(name)
# 		print "name",name,name_se
		return name[:name_se.start()]# 		print "name",name,nam# 		print "name",name,name_see_se
	
   	
		
		
if __name__ == "__main__":
 	
 	#dictionary_vector = { 'the':'the-rep', 'president':'president-rep', 'black':'black-rep', 'first':'first-rep', 'Obama':'obama-w', 'USA':'usa-w'}
 	#dictionary_w = {'det':'det-w' , 'amod':'amod-w', 'prep_of':'prep_of-w', 'id':'id-w', 'nsubj':'nsubj-w'}
 	
 	depGraph = "nsubj(president-6, Obama-1)\ncop(president-6, is-2)\ndet(president-6, the-3)\n \
 	amod(president-6, black-5)\namod(black-5, first-4)\nroot(ROOT-0, president-6)\n\
 	prep_of(president-6, USA-8)"
 	
 	datapoint1={"depGraph":depGraph, "head":"president", "arg1":"Obama" , "arg2":"USA"}
 	dataset=[datapoint1]
 	rng = random.RandomState(1234)
 	
 	r= RandomInitialization.RandomInitialization(rng)
 	(dep_weights,word_embeddings) = r.initialize(dataset, 10)
 	
 	factory = NeuralNetworkFactory()
 	 	
 	network = factory.create(datapoint1, 10,dep_weights,word_embeddings)
 	
 	print network.__str__()
 	#theano.printing.debugprint(network.output)
  	print theano.printing.pp(network.output)
