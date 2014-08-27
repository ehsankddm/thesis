'''
Created on Apr 7, 2014

@author: ehsan
'''
import theano.tensor as T
from theano import function
import theano
import numpy as np
import pprint
from numpy import random
def test_theano_matrix():
	pp = pprint.PrettyPrinter(indent=3)
	W= T.matrix(dtype=theano.config.floatX)
	x=T.matrix(dtype=theano.config.floatX)
	b= T.matrix(dtype=theano.config.floatX)
	y = T.dot(W,x)+ b
	lin_func = function([W,x,b],y)
	dt = np.dtype(np.float64)
	w_inp = np.matrix('1 1;1 1',dtype=dt)
	print w_inp.dtype
	x_inp = np.matrix('2;1',dtype=dt)
	b_inp = np.matrix('1;1',dtype=dt)
	
	print lin_func(w_inp,x_inp,b_inp)

def lin_creator():
	W= T.matrix(dtype=theano.config.floatX)
	x=T.matrix(dtype=theano.config.floatX)
	b= T.matrix(dtype=theano.config.floatX)
	y = T.dot(W,x)+ b
	return y

def tanh_creator():
	W= T.matrix(dtype=theano.config.floatX)
	x=T.matrix(dtype=theano.config.floatX)
	b= T.matrix(dtype=theano.config.floatX)
	y = T.tanh(T.dot(W,x)+ b)
	lin_func = function([W,x,b],y)
	return lin_func
	
def sum_creator(input, ):
	pass
def test_update():
	rng = random.RandomState(1234)
	dim_size=10
	#x_values = np.asarray(rng.uniform(low=-10, high=10, size=(1,dim_size)  ) ,dtype=theano.config.floatX)
	x_values = np.asarray([0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]   ,dtype=theano.config.floatX)
	x=theano.shared(value=x_values, name='x', borrow=True)
	w_values = np.asarray(rng.uniform(low=-10, high=10, size=(dim_size,dim_size)),dtype=theano.config.floatX)
	w=theano.shared(value=w_values,name="w", borrow=True)
	
	b_values = np.asarray(rng.uniform(low=-10,high=10, size=(1,dim_size)),dtype=theano.config.floatX)
	b=theano.shared(value=b_values, name="b", borrow=True)
	test_dic={'w':w, 'b':b}
	y_hat = T.tanh(T.dot(x,w))+b
	y=np.asarray([0,0,0,0,0,1,1,1,1,1] ,dtype=theano.config.floatX)
	error = abs(y_hat - y).sum()
	params=[w,b]
	gparams=[]
	for param in params:
		gparam=T.grad(error,param)
		gparams.append(gparam)
	updates=[]
	for param,gparam in zip (params,gparams):
		updates.append( (param,param-0.05*gparam) )
	
	train_model = theano.function(inputs=[],outputs=error,updates=updates)
	perform=[]
	for i in range(1,1000):
		train_model()
		perform.append( error.eval())
		print "x",x.eval()
		print "y_hat",y_hat.eval()
		print "****"
# 		print test_dic['b'].eval()
		print "----------------------"
	print perform
def mu_test():
	y1=lin_creator()
	y2 = lin_creator()
	y3 = T.tanh(y1+y2)
def asho_test():
	import theano.tensor as T
	x = T.dmatrix('x')
	w = T.dmatrix('w')
	y = T.dot(x,w)

	f = function([x,w],y)	

def test_sum():
	pass

if __name__ == '__main__':
	#test_theano_matrix()
	#test_update()
	asho_test()
	print 'done'