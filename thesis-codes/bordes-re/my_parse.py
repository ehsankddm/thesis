import os
import cPickle

import numpy as np
import scipy.sparse as sp


def parseline(line):
    lhs, rel, rhs = line.split('\t\t')
    lhs = lhs.split(' ')
    rhs = rhs.split(' ')
    rel = rel.split(' ')
    return lhs, rel, rhs

#################################################
# ## Creation of the synset/indices dictionnaries
def parse (file_name):
	np.random.seed(753)

	synlist = []
	rellist = []

	for datatyp in ['train', 'valid', 'test']:
		f = open(file_name + '%s' % datatyp, 'r')
		dat = f.readlines()
		f.close()
		for i in dat:
		          lhs, rel, rhs = parseline(i[:-1])
		          synlist += [lhs[0], rhs[0]]
		          rellist += [rel[0]]

	synset = list(set(synlist))
	synset.sort(reverse=True)
	try:
		synset.remove('NA')
		synset.append('NA')
	except ValueError:
		pass
	
	relset = list(set(rellist))
	relset.sort(reverse=True)

	synset2idx = {}
	idx2synset = {}

	idx = 0
	nbfbrel=0
	for i in synset:
	    synset2idx[i] = idx
	    idx2synset[idx] = i
	    idx += 1
	    if i.startswith('/') or i == 'NA':
	    	nbfbrel+=1
	nbsyn = idx
	print "Number of synsets in the dictionary: ", nbsyn
	print "Number of real synsets in the dictionary: ", nbsyn - nbfbrel
	nbreloffset =  nbsyn - nbfbrel
	# add relations at the end of the dictionary
	for i in relset:
            if not synset2idx.has_key(i):  
	           synset2idx[i] = idx
	           idx2synset[idx] = i
	           idx += 1
            else:
                continue
	nbent = idx
        nbrel = len(relset)
	print "Number of relations in the dictionary: ", nbrel
	
        print "Number of entities in the dictionary: ", nbent
	h = open('info.pkl', 'w')
	f = open('synset2idx.pkl', 'w')
	g = open('idx2synset.pkl', 'w')
	cPickle.dump(synset2idx, f, -1)
	cPickle.dump(idx2synset, g, -1)
	cPickle.dump(nbsyn, h, -1)
	cPickle.dump(nbrel, h, -1)
        cPickle.dump(nbent, h, -1)
        cPickle.dump(nbreloffset, h, -1)
	f.close()
	g.close()
	h.close()


	#################################################
	# ## Creation of the dataset files

	for datatyp in ['train', 'valid', 'test']:
	    f = open(file_name + '%s' % datatyp, 'r')
	    dat = f.readlines()
	    f.close()

	    # Declare the dataset variables
	    inpl = sp.lil_matrix((np.max(synset2idx.values()) + 1, len(dat)),
		    dtype='float32')
	    inpr = sp.lil_matrix((np.max(synset2idx.values()) + 1, len(dat)),
		    dtype='float32')
	    inpo = sp.lil_matrix((np.max(synset2idx.values()) + 1, len(dat)),
		    dtype='float32')
	    # Fill the sparse matrices
	    ct = 0
	    for i in dat:
		lhs, rel, rhs = parseline(i[:-1])
		inpl[synset2idx[lhs[0]], ct] = 1
		inpr[synset2idx[rhs[0]], ct] = 1
		inpo[synset2idx[rel[0]], ct] = 1
		ct += 1
	    # Save the datasets

	    f = open('%s-lhs.pkl' % datatyp, 'w')
	    g = open('%s-rhs.pkl' % datatyp, 'w')
	    h = open('%s-rel.pkl' % datatyp, 'w')
	    cPickle.dump(inpl.tocsr(), f, -1)
	    cPickle.dump(inpr.tocsr(), g, -1)
	    cPickle.dump(inpo.tocsr(), h, -1)
	    f.close()
	    g.close()
	    h.close()
	return (nbsyn, nbrel, nbent,nbreloffset)

