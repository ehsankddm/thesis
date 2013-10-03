'''
Created on Sep 29, 2013

@author: ehsan
'''
import riedel_parser
import tripleMaker
import random
import re

class Experiment(object):
    def __init__(self):
        pass
    
    @staticmethod
    def parseAndMake(file_addr_in, file_addr_out, opt):
        parser = riedel_parser.RiedelParser()
        tmaker = tripleMaker.tripleMaker()
        pattern = re.compile(r'\s')
        file_out = open (file_addr_out,'a')
        for res in parser.parse(file_addr_in):
            for triple in tmaker.makeTriples(res, opt):
                file_out.write(re.sub(pattern,'#',triple[0])+'\t\t'+ re.sub(pattern,'#',triple[1])+'\t\t'+re.sub(pattern,'#',triple[2])+'\n')
                file_out.flush()
        
        file_out.close()
    
    @staticmethod
    def sample(file_addr_in ,file_addr_out,number_of_samples):
        import tempfile
        
        random.seed(2013)
        with open(file_addr_in,'r') as file_in:
            population_length = sum (1 for line in file_in)
        if number_of_samples < population_length:    
            sample_index = random.sample(range(population_length),number_of_samples)
            
            with open (file_addr_out,'w') as file_out:        
                with open(file_addr_in,'r') as file_in:
                    [file_out.write(v) for k,v in enumerate(file_in) if k in sample_index] 
        else:
            with open (file_addr_out,'w') as file_out:        
                with open(file_addr_in,'r') as file_in:
                    [file_out.write(line) for line in file_in]
    @staticmethod 
    def statistics(file_addr_in):
        import collections
        import operator
        parser = riedel_parser.TripleParser()
        counts = collections.defaultdict(int)
        rels = collections.defaultdict(int)
        number_of_triples=0
        with open(file_addr_in,'r') as f_in:
            for line in f_in:
                (lhs,rel,rhs) = parser.parse(line)
                number_of_triples +=1
                counts[lhs] +=1
                counts[rhs] +=1
                counts[rel] +=1
                rels[rel] +=1
        '''for i in sorted(counts.iteritems(), key=operator.itemgetter(1)):
            print i
        '''
        threshold = 3
        gt_thresh=0
        le_thresh=0
        
        for k,v in counts.iteritems():
            if v>threshold:
                gt_thresh+=1.0
            else:
                le_thresh+=1.0
        for i in sorted(rels.iteritems(), key=operator.itemgetter(1)):
            print i
        print 'number of triples: ', number_of_triples
        print 'number of entities: ',len(counts)
        print 'number of Freebase relations: ', len(rels)
        print 'threshold: ', threshold
        print 'percent of entities occurred more than threshold: ',gt_thresh/len(counts) * 100.0
        print 'percent of entities occurred less than threshold: ',le_thresh/len(counts) * 100.0
        
    @staticmethod
    def experiment1():
       
        
        train_positive_addr_orig = '/media/toothless/thesis_data/riedel_yao_univ/processed/train.positive.universal.txt'
        train_unlabeled_addr_orig = '/media/toothless/thesis_data/riedel_yao_univ/processed/train.unlabeled.universal.txt'
        train_negative_addr_orig = '/media/toothless/thesis_data/riedel_yao_univ/processed/train.negative.universal.txt'
        
        test_positive_addr_orig ='/media/toothless/thesis_data/riedel_yao_univ/processed/test.positive.universal.txt'
        test_negative_addr_orig = '/media/toothless/thesis_data/riedel_yao_univ/processed/test.negative.universal.txt'
        
        train_positive_addr_in = 'sample.train.positive'
        train_unlabeled_addr_in = 'sample.train.unlabeled'
        train_negative_addr_in = 'sample.train.negative'
        
        test_positive_addr_in ='sample.test.positive'
        test_negative_addr_in = 'sample.test.negative'
        
        validation_positive_addr_in = 'sample.validation.positive'
        validation_negative_addr_in = 'sample.validation.negative'
        
        train_addr_out = 'train_sample'
        test_addr_out = 'test_sample'
        validation_addr_out = 'validation_sample'
        
        Experiment.sample(train_positive_addr_orig,train_positive_addr_in, 8409)
        Experiment.sample(train_negative_addr_orig,train_negative_addr_in, 20000)
        
        Experiment.sample(test_positive_addr_orig,test_positive_addr_in, 2500)
        Experiment.sample(test_negative_addr_orig,test_negative_addr_in, 4000)
        
        Experiment.sample(test_positive_addr_in,validation_positive_addr_in, 1000)
        Experiment.sample(test_negative_addr_in,validation_negative_addr_in, 1000)
        
        
        opt={'label':True,'hasNER':True, 'trigger':True, 'hasTrigger':True,'hasDependencyRole':True}
        Experiment.parseAndMake(train_positive_addr_in, train_addr_out, opt)
        
        opt={'label':True,'hasNER':True, 'trigger':True, 'hasTrigger':True,'hasDependencyRole':True}
        Experiment.parseAndMake(train_negative_addr_in, train_addr_out, opt)
        
                
        opt={'label':False,'hasNER':True, 'trigger':True, 'hasTrigger':True,'hasDependencyRole':True}
        Experiment.parseAndMake(test_positive_addr_in, train_addr_out, opt)
               
        opt={'label':False,'hasNER':True, 'trigger':True, 'hasTrigger':True,'hasDependencyRole':True}
        Experiment.parseAndMake(test_negative_addr_in, train_addr_out, opt) 


        opt={'label':True}
        Experiment.parseAndMake(test_positive_addr_in, test_addr_out, opt)
            
        opt={'label':True}
        Experiment.parseAndMake(test_negative_addr_in, test_addr_out, opt)
        
        opt={'label':True}
        Experiment.parseAndMake(validation_positive_addr_in, validation_addr_out, opt)
            
        opt={'label':True}
        Experiment.parseAndMake(validation_negative_addr_in, validation_addr_out, opt)            
        
if __name__ == '__main__':
        
        
        Experiment.experiment1()
        
        train_addr_out = 'train_sample'
        test_addr_out = 'test_sample'
        validation_addr_out = 'validation_sample'
        Experiment.statistics(train_addr_out)
        
        #Experiment.experiment1() 
        #Experiment.statistics(test_addr_out)
        #Experiment.statistics(validation_addr_out)
        
       
            