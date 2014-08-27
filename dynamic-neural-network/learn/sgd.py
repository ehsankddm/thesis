'''
Created on Apr 17, 2014

@author: ehsan
'''
from layers.NeuralNetworkFactory import NeuralNetworkFactory
import theano
import theano.tensor as T
import numpy as np
from scipy import stats
from initialization import RandomInitialization
from numpy import random

def dot_product_similarity(num_vector,num_matrix_in_list):
	pass


	
def get_random_generator_freq_dist(probabilities):
	xk= np.arange(len(probabilities))
	custm = stats.rv_discrete(name='custm', values=(xk, probabilities))
	return custm
	
def train(dataset,n_dim,rng,learning_rate=0.01, L1_reg=0.00, L2_reg=0.0001, n_epochs=10,
              batch_size=20):
	
	r= RandomInitialization.RandomInitialization(rng)
 	(weights,word2index_dict) = r.initialize(dataset, n_dim)
 	
 	networkFactory = NeuralNetworkFactory()
 	
 	args2network_dict=dict()
 	#datapoint is a dict
 	#dataset is a list of datapoints
 	for idx,datapoint in enumerate(dataset):
 		arg1=datapoint["arg1"]
 		arg2=datapoint["arg2"]
 		network =networkFactory.create(datapoint, n_dim, weights, word2index_dict)
 		datapoint["network"]=network
 		if args2network_dict.has_key((arg1,arg2)):
 			args2network_dict[(arg1,arg2)].append( idx)
 		else:
 			args2network_dict[(arg1,arg2)]=[idx]
 	
 	args_based_freq=[]
 	sums=0.0
 	for key in  args2network_dict.iterkeys():
 		freq=len(args2network_dict[key])
 		args_based_freq.append(freq)
 		sums += freq
 	args2network_keys= args2network_dict.keys()
 	for i in range(0,len(args_based_freq)):
 		args_based_freq[i] = args_based_freq[i] /sums
 	   
 	args_dist_random_generator = get_random_generator_freq_dist(args_based_freq)
 	#arg1_arg2_dist_random_generator.rvs(size=100)  for negative sampling
 	#args_keys_probs=zip(arg1_arg2_keys,arg1_arg2_freq)
 	dataset_idx=range(0,len(dataset))
 	
 	for epoch in range(0,n_epochs):
 		random.shuffle(dataset_idx)
 		batch_max_iter = len(dataset_idx)/batch_size if batch_size%len(dataset_idx) ==0 else len(dataset_idx)/batch_size +1
 		
 	 	for batch_number in range(0,batch_max_iter):
 	 		subset_idx=dataset_idx[batch_number*batch_size  : min((batch_number+1)*batch_size,len(dataset_idx))]
 	 		positive_theta_list=[]
 	 		negative_theta_list=[]
 	 		batch = [dataset[i] for i in subset_idx]
 	 		
 	 		for datapoint in batch:
 	 			arg1 = datapoint["arg1"]
 	 			arg2 = datapoint["arg2"]
 	 			rel  = datapoint["head"]
 	 			pos_idx = args2network_dict[(arg1,arg2)]
 	 			pos_subset = [dataset[i] for i in pos_idx]
 	 			
 	 			#calculating sum(T.dot(datapoint.output, pos_subset_matrix))
 	 		 	#adding result to positiv_theta_list
 	 			positive_theta_list.append( sum([T.dot(datapoint.output,val) for val in pos_subset]))
 	 		 	
 	 		 	
 	 		 	#??? what can we do about number of negative samples?
 	 		  	neg_args_idxs=args_dist_random_generator.rvs(1)
 	 		  	neg_subset=[]
 	 		  	for neg_arg_idx in neg_args_idxs:
 	 		  		(neg_arg1,neg_arg2)=args2network_keys[neg_arg_idx]
 	 		  		neg_network_idx_list = args2network_dict[(neg_arg1,neg_arg2)]
 	 		  		for neg_network_idx in neg_network_idx_list:
 	 		  			neg_datapoint = dataset[neg_network_idx]
 	 		  			if neg_datapoint["head"]!=rel:
 	 		  					neg_subset.append(neg_datapoint)
 	 		  	
 	 		 	#calculating sum(T.dot(datapoint.output, neg_subset_matrix))
 	 		 	#adding result to negative_theta_list
 	 		 	negative_theta_list.append(sum([T.dot(datapoint.output,val) for val in neg_subset]))
 	 		 	#W is ok since we use all weights but what about Bias (bS)???
 	 		 	#Check by_ref or by_value of Ws stored in Dict--> checked, they change
 	 		 
 	 		cost = -1.0 * sum(T.log([1.0/(1+T.exp(theta_neg - theta_pos)) for theta_pos,theta_neg in zip(positive_theta_list,negative_theta_list)  ])) \
 	 		+ sum([w**2 for w in weights.values])
 	 		
 	 		#it 
 	 		params = [w for w in weights.values]
 	 	 	gparams=[]
	 	 	for param in params:
	 	 			# check internal theano algorithm of gradient
			 	 gparam=T.grad(cost,param)
				 gparams.append(gparam)
			updates=[]
			for param,gparam in zip (params,gparams):
				updates.append( (param,param-learning_rate*gparam) )
 			train_model = theano.function(inputs=[],outputs=cost,updates=updates)
 			train_model()
 			
 	
 	#compile a function get one vector and one matrix and return sum of dot product of this vector with all columns of the matrix
 		 
 		
 	
 	
if __name__ == '__main__':
	rng = random.RandomState(1234)