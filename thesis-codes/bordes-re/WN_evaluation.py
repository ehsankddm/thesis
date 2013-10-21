#! /usr/bin/python

from model import *
import scipy.sparse

def load_file(path):
    return scipy.sparse.csr_matrix(cPickle.load(open(path)),
            dtype=theano.config.floatX)


def convert2idx(spmat):
    rows, cols = spmat.nonzero()
    return rows[np.argsort(cols)]


def RankingEval(datapath='', dataset='test',
        loadmodel='best_valid_model.pkl', neval='all', Nsyn=40943, n=100):

    # Load model
    f = open(loadmodel)
    embeddings = cPickle.load(f)
    leftop = cPickle.load(f)
    rightop = cPickle.load(f)
    simfn = cPickle.load(f)
    f.close()
    ff= open('idx2synset.pkl') 
    idx2synset = cPickle.load(ff)
    ff.close()
    ff= open('info.pkl') 
    Nsyn = cPickle.load(ff)
    Nrel = cPickle.load(ff)
    Nent = cPickle.load(ff)
    Nreloffset = cPickle.load(ff)
    ff.close()	
    # Load data
    l = load_file(datapath + dataset + '-lhs.pkl')
    r = load_file(datapath + dataset + '-rhs.pkl')
    o = load_file(datapath + dataset + '-rel.pkl')
    if type(embeddings) is list:
        o = o[-embeddings[1].N:, :]

    # Convert sparse matrix to indexes
    if neval == 'all':
        idxl = convert2idx(l)
        idxr = convert2idx(r)
        idxo = convert2idx(o)
    else:
        idxl = convert2idx(l)[:neval]
        idxr = convert2idx(r)[:neval]
        idxo = convert2idx(o)[:neval]

#     ranklfunc = RankLeftFnIdx(simfn, embeddings, leftop, rightop,
#             subtensorspec=Nsyn)
#     rankrfunc = RankRightFnIdx(simfn, embeddings, leftop, rightop,
#             subtensorspec=Nsyn)
# 
#     res = RankingScoreIdx(ranklfunc, rankrfunc, idxl, idxr, idxo)
    rankrelfunc = RankRelFnIdx(simfn, embeddings, leftop, rightop, offset=Nreloffset,subtensorspec=Nent)
    res = RankingScoreRelIdx(rankrelfunc, idxl, idxr, idxo,offset=Nreloffset)
    dres = {}
    #dres.update({'microlmean': np.mean(res[0])})
    #dres.update({'microlmedian': np.median(res[0])})
    #dres.update({'microlr@n': np.mean(np.asarray(res[0]) <= n) * 100})
    #dres.update({'micrormean': np.mean(res[1])})
    #dres.update({'micrormedian': np.median(res[1])})
    #dres.update({'microrr@n': np.mean(np.asarray(res[1]) <= n) * 100})
    #resg = res[0] + res[1]
    #dres.update({'microgmean': np.mean(resg)})
    #dres.update({'microgmedian': np.median(resg)})
    #dres.update({'microgr@n': np.mean(np.asarray(resg) <= n) * 100})
    dres.update({'microgmean': np.mean(res)})
    dres.update({'microgmedian': np.median(res)})
    dres.update({'microgr@n': np.mean(np.asarray(res) <= n) * 100})

    print "### MICRO:"
#     print "\t-- left   >> mean: %s, median: %s, r@%s: %s%%" % (
#             round(dres['microlmean'], 5), round(dres['microlmedian'], 5),
#             n, round(dres['microlr@n'], 3))
#     print "\t-- right  >> mean: %s, median: %s, r@%s: %s%%" % (
#             round(dres['micrormean'], 5), round(dres['micrormedian'], 5),
#             n, round(dres['microrr@n'], 3))
#     print "\t-- global >> mean: %s, median: %s, r@%s: %s%%" % (
#             round(dres['microgmean'], 5), round(dres['microgmedian'], 5),
#             n, round(dres['microgr@n'], 3))
	
    print "\t-- relation >> mean: %s, median: %s, r@%s: %s%%" % ( round(dres['microgmean'], 5), round(dres['microgmedian'], 5), n, round(dres['microgr@n'], 3))

    listrel = set(idxo)
    print 'number of relations in test set', len(listrel)
    dictrelres = {}
    dictrelmean = {}
    dictrelmedian = {}
    dictreln = {}

    for i in listrel:
        dictrelres.update({i: []})

    for i, j in enumerate(res):
        dictrelres[idxo[i]] += [j]

    for i in listrel:
        dictrelmean[i] = np.mean(dictrelres[i])
        dictrelmedian[i] = np.median(dictrelres[i])
        dictreln[i] = np.mean(np.asarray(dictrelres[i]) <= n) * 100

    dres.update({'dictrelres': dictrelres})
    dres.update({'dictrelmean': dictrelmean})
    dres.update({'dictrelmedian': dictrelmedian})
    dres.update({'dictreln': dictreln}) 
    print 'dictrelmean: ', dictrelmean, dictrelmean.values()
    print 'dictrelmedian: ', dictrelmedian, dictrelmedian.values()
    dres.update({'macrorelmean': np.mean(dictrelmean.values())})
    dres.update({'macrorelmedian': np.mean(dictrelmedian.values())})
    dres.update({'macrorel@n': np.mean(dictreln.values())})

    print "\n### MACRO:"
    print "\t-- relation   >> mean: %s, median: %s, r@%s: %s%%" % (
            round(dres['macrorelmean'], 5), round(dres['macrorelmedian'], 5),
            n, round(dres['macrorel@n'], 3))
   
    
    offset = 0
    if type(embeddings) is list:
        o = o[-embeddings[1].N:, :]
        offset = l.shape[0] - embeddings[1].N
    for i in np.sort(list(listrel)):
        print "\n### RELATION %s:" % idx2synset[offset + i]
        print "\t-- stat>> mean: %s, median: %s, r@%s: %s%%, N: %s" % (
                round(dictrelmean[i], 5), round(dictrelmedian[i], 5),
                n, round(dictreln[i], 3), len(dictrelres[i]))
       

    return dres


def ClassifEval(datapath='', validset='valid', testset='test',
        loadmodel='best_valid_model.pkl', seed=647):

    # Load model
    f = open(loadmodel)
    embeddings = cPickle.load(f)
    leftop = cPickle.load(f)
    rightop = cPickle.load(f)
    simfn = cPickle.load(f)
    f.close()

    np.random.seed(seed)

    # Load data
    # linked list sparse matrix directly from train test valid dataset
    # inpl = sp.lil_matrix((np.max(synset2idx.values()) + 1, len(dat)),
    #        dtype='float32')
    
    # inpl.tocsr()
    
    
    # what is lvn? list valid negative????
    
    lv = load_file(datapath + validset + '-lhs.pkl')
    lvn = lv[:, np.random.permutation(lv.shape[1])]
    rv = load_file(datapath + validset + '-rhs.pkl')
    rvn = rv[:, np.random.permutation(lv.shape[1])]
    ov = load_file(datapath + validset + '-rel.pkl')
    ovn = ov[:, np.random.permutation(lv.shape[1])]
    if type(embeddings) is list:
        ov = ov[-embeddings[1].N:, :]
        ovn = ovn[-embeddings[1].N:, :]

    # Load data
    lt = load_file(datapath + testset + '-lhs.pkl')
    ltn = lt[:, np.random.permutation(lv.shape[1])]
    rt = load_file(datapath + testset + '-rhs.pkl')
    rtn = rt[:, np.random.permutation(lv.shape[1])]
    ot = load_file(datapath + testset + '-rel.pkl')
    otn = ot[:, np.random.permutation(lv.shape[1])]
    if type(embeddings) is list:
        ot = ot[-embeddings[1].N:, :]
        otn = otn[-embeddings[1].N:, :]
    #ref:
    #leftop = LayerMat('lin', state.ndim, state.nhid)
    #rightop = LayerMat('lin', state.ndim, state.nhid)
    # see SimFn
    simfunc = SimFn(simfn, embeddings, leftop, rightop)


    # what is output in resv and resvn ?????? format ? how many numbers? should be similarity
    resv = simfunc(lv, rv, ov)[0]
    resvn = simfunc(lvn, rvn, ovn)[0]
    rest = simfunc(lt, rt, ot)[0]
    restn = simfunc(ltn, rtn, otn)[0]

    # Threshold
    perf = 0
    T = 0
    for val in list(np.concatenate([resv, resvn])):
        tmpperf = (resv > val).sum() + (resvn <= val).sum()
        if tmpperf > perf:
            perf = tmpperf
            T = val
    testperf = ((rest > T).sum() + (restn <= T).sum()) / float(2 * len(rest))
    print "### Classification performance : %s%%" % round(testperf * 100, 3)

    return testperf


if __name__ == '__main__':
    ClassifEval()
    RankingEval()
