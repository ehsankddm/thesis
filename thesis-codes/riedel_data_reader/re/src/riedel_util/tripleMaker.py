'''
Created on Sep 29, 2013

@author: ehsan
'''

class tripleMaker(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def __makeFreeBaseRel(self, res):
        triples = []
        for rel in res['rel']:
            triples.append((res['lhs'] , rel , res ['rhs']))
        return triples    
   
    def __makeHasNER(self, res):
        triples = []
        for ner in res['ner']:
            ner_list = ner.split('->')
            if len(ner_list) == 2:
                triples.append((res['lhs'] , 'HAS_TYPE' , ner_list[0]))
                triples.append((res['rhs'] , 'HAS_TYPE' , ner_list[1]))
        return triples  
    
    def __makeTrigger(self, res):
        triples = []
        for trigger in res['trigger']:
            triples.append((res['lhs'] , trigger , res ['rhs']))
        return triples
    
    def __makeHasTigger(self, res):
        triples = []
        for rel in res['rel']:
            for trigger in res['trigger']:
                triples.append((rel , 'HAS_TRIGGER' , trigger))
        return triples  
    
    def __makeHasDependencyRole(self, res):
        triples = []
        for path in res['path']:
            path_tokens = path.split('|')
            if len(path_tokens) == 3:
                triples.append((res['lhs'] , 'HAS_DEP_ROLE' , path_tokens[0]))
                triples.append((res['rhs'] , 'HAS_DEP_ROLE' , path_tokens[2]))
        return triples
    
    def makeTriples(self, res, opt):
        
        if isinstance(opt, dict):
            triples = []
            if opt.has_key('label') and opt['label'] == True:
                for triple in self.__makeFreeBaseRel(res):
                    triples.append(triple)
            if opt.has_key('hasNER') and opt['hasNER'] == True:
                for triple in self.__makeHasNER(res):
                    triples.append(triple)
            if opt.has_key('trigger') and opt['trigger'] == True:
                for triple in self.__makeTrigger(res):
                    triples.append(triple)
            if opt.has_key('hasTrigger') and opt['hasTrigger'] == True:
                for triple in self.__makeHasTigger(res):
                    triples.append(triple)
            if opt.has_key('hasDependencyRole') and opt['hasDependencyRole'] == True:
                for triple in self.__makeHasDependencyRole(res):
                    triples.append(triple)
            return triples
        
        else:
            return self.__makeFreeBaseRel(res) + self.__makeHasNER(res) + self.__makeTrigger(res) + self.__makeHasTigger(res) + self.__makeHasDependencyRole(res)
        
   
        
    
