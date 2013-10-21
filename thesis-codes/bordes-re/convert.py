#!/usr/bin/python
import pprint
from model import *
import scipy.sparse
from WN_evaluation import *

def convert2idx(spmat):
    rows, cols = spmat.nonzero()
    return rows[np.argsort(cols)]
def print_set(data, name):
    with open( name + ".txt", "w+") as handle:
        print >>handle, "# type(python)", type(data)
        print >>handle, "# type(theano)", data.type
        print >>handle, "# dimensions  ", data.ndim
        if data.ndim == 2:
            print >>handle, "# rows(numpy) ", len(data.get_value())
            print >>handle, "# cols(numpy) ", len(data.get_value()[0])
            for row in theano.function([], data)():
                for val in row:
                    print >>handle, "%0.6f" % val,
                print >>handle
        elif data.ndim == 1:
            for row in theano.function([], data)():
                print >>handle, "%d" % row
        elif data.ndim == 3:
            print >>handle, "# Tensor" 
        else:
            return
def convert_set2(data):
        
        if data.ndim == 2:
           s='' 
	   for row in data:
                for val in row:
                    s= s +  "%0.6f" % val + ','
           return s[0:-1]
      
        elif data.ndim == 1:
            for row in data:
                print "%d" % row
        elif data.ndim == 3:
            print "# Tensor" 
        else:
            return
def convertArrayToString(arr):
	arr=arr[0]
	s=''
	for elm in arr:
		s=s+str(elm)+','
	return s[0:-1]
	
if __name__ == '__main__':
    loadmodel='.best_valid_model.pkl'
    # Load model
    f = open(loadmodel) 
    embeddings = cPickle.load(f)
    leftop = cPickle.load(f)
    rightop = cPickle.load(f)
    simfn = cPickle.load(f)
    f.close()
    ff= open('idx2synset.pkl') 
    idx2synset = cPickle.load(ff)
    #print len(idx2synset)
    ff.close()
    ff= open('info.pkl') 
    Nsyn = cPickle.load(ff)
    Nrel = cPickle.load(ff)
    #print Nsyn, Nrel
    ff.close()	
    #print type(embeddings),type(leftop), type(rightop)
    embedding, relationl, relationr = parse_embeddings(embeddings)
#     print(dir(embedding.E))
#     pprint.pprint(dir(embedding.E))
    pprint.pprint(embedding.D)
    pprint.pprint(embedding.N)
    for i in range (0,Nsyn):
	    #print  idx2synset[i], convertArrayToString(embedding.E[:,i].reshape((1, embedding.D)).eval())
	    print  idx2synset[i], convert_set2(embedding.E.get_value()[:,i].reshape((1, embedding.D)))
    #pprint.pprint(relationl.D)
    #pprint.pprint(relationr.D)
    #print type(embedding)
    
    #idxo = T.iscalar('idxo')
    #idxr = T.iscalar('idxr')
    #idxl = T.iscalar('idxl')
    # Graph
    #lhs = (embedding.E[:, idxl]).reshape((1, embedding.D))
    #rhs = (embedding.E[:, idxr]).reshape((1, embedding.D))
    #rell = (relationl.E[:, idxo]).reshape((1, relationl.D))
    #relr = (relationr.E[:, idxo]).reshape((1, relationr.D))
    #simi = simfn(leftop(lhs, rell), rightop(rhs, relr))
#     print_set(embedding.E, "embedding")
#     print_set(relationl.E, "relationl")
#     print_set(relationr.E, "relationr")
    #print type(lhs)
    #print type(rhs)
    #print type(rell)
    #print type(relr)
