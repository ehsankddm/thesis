'''
Created on Sep 29, 2013

@author: ehsan
'''
import riedel_parser
import tripleMaker
if __name__ == '__main__':
        
        parser = riedel_parser.RiedelParser()
        tmaker = tripleMaker.tripleMaker()
        f_train_out = open('train','w')
        f_test_out = open('test','w')
        
        opt=[]
        for res in parser.parse('/media/toothless/thesis_data/riedel_yao_univ/processed/train.positive.universal.txt'):
            for triple in tmaker.makeTriples(res, opt):
                f_train_out.write(triple[0].replace('\\s','#')+'\t\t'+ triple[1].replace('\\s','#')+'\t\t'+triple[2].replace('\\s','#')+'\n')
                f_train_out.flush()
        
        opt={'label':False,'hasNER':True, 'trigger':True, 'hasTrigger':False,'hasDependencyRole':True}
        for res in parser.parse('/media/toothless/thesis_data/riedel_yao_univ/processed/train.unlabeled.universal.txt'):
            for triple in tmaker.makeTriples(res, opt):
                f_train_out.write(triple[0].replace('\\s','#')+'\t\t'+ triple[1].replace('\\s','#')+'\t\t'+triple[2].replace('\\s','#')+'\n')
                f_train_out.flush()
        
        opt={'label':True,'hasNER':True, 'trigger':True, 'hasTrigger':True,'hasDependencyRole':True}
        for res in parser.parse('/media/toothless/thesis_data/riedel_yao_univ/processed/train.negative.universal.txt'):
            for triple in tmaker.makeTriples(res, opt):
                f_train_out.write(triple[0].replace('\\s','#')+'\t\t'+ triple[1].replace('\\s','#')+'\t\t'+triple[2].replace('\\s','#')+'\n')
                f_train_out.flush()
        
        opt={'label':False,'hasNER':True, 'trigger':True, 'hasTrigger':True,'hasDependencyRole':True}
        for res in parser.parse('/media/toothless/thesis_data/riedel_yao_univ/processed/test.positive.universal.txt'):
            for triple in tmaker.makeTriples(res, opt):
                f_train_out.write(triple[0].replace('\\s','#')+'\t\t'+ triple[1].replace('\\s','#')+'\t\t'+triple[2].replace('\\s','#')+'\n')
                f_train_out.flush()
        
        opt={'label':False,'hasNER':True, 'trigger':True, 'hasTrigger':True,'hasDependencyRole':True}
        for res in parser.parse('/media/toothless/thesis_data/riedel_yao_univ/processed/test.negative.universal.txt'):
            for triple in tmaker.makeTriples(res, opt):
                f_train_out.write(triple[0].replace('\\s','#')+'\t\t'+ triple[1].replace('\\s','#')+'\t\t'+triple[2].replace('\\s','#')+'\n')
                f_train_out.flush()
        f_train_out.close()
        
        opt={'label':True}
        for res in parser.parse('/media/toothless/thesis_data/riedel_yao_univ/processed/test.positive.universal.txt'):
            for triple in tmaker.makeTriples(res, opt):
                f_test_out.write(triple[0].replace('\\s','#')+'\t\t'+ triple[1].replace('\\s','#')+'\t\t'+triple[2].replace('\\s','#')+'\n')
                f_test_out.flush()
        
        opt={'label':True}
        for res in parser.parse('/media/toothless/thesis_data/riedel_yao_univ/processed/test.negative.universal.txt'):
            for triple in tmaker.makeTriples(res, opt):
                f_test_out.write(triple[0].replace('\\s','#')+'\t\t'+ triple[1].replace('\\s','#')+'\t\t'+triple[2].replace('\\s','#')+'\n')
                f_test_out.flush()
        
        f_test_out.close()   
        