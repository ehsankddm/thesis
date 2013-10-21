#!/usr/bin/python

#number of relations  = db.Features1.distinct("relation").length
#number of unique lefthandside+righthand side = db.Features1_externalRef.count()
#db.Features1.count()


import random
import math
import numpy as np
import scipy.sparse as sp
import cPickle
from WN_exp import *
from WN_evaluation import *
from my_parse import *



file_name='RE_'
(nbsyn,nbrel,nbent,nbreloffset) = parse(file_name)


launch(op='SME_bil',dataset='', Nent=nbent, Nsyn=nbsyn, Nrel=nbrel,Nreloffset=nbreloffset
       , simfn='Dot', ndim=2, nhid=2, marge=1., lremb=0.01,
    lrparam=1., nbatches=2, totepochs=5, test_all=2, savepath='.',
    datapath='')

print "\n##### EVALUATION #####\n"

ClassifEval(datapath='', loadmodel='best_valid_model.pkl')
RankingEval(datapath='', loadmodel='best_valid_model.pkl')
            
        
        


     







