import random
import math
import numpy as np
import scipy.sparse as sp
import cPickle
from WN_exp import *
from WN_evaluation import *

print "\n##### EVALUATION #####\n"

ClassifEval(datapath='', loadmodel='best_valid_model.pkl')
RankingEval(datapath='', loadmodel='best_valid_model.pkl')
