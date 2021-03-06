'''
Created on Sep 29, 2013

@author: ehsan
'''
class TripleParser(object):
    def parse(self, line):
        tokens = line.strip().split('\t\t')
        assert len(tokens)==3
        
        return (tokens[0], tokens[1],tokens[2])
            
    
class RiedelParser(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
    
    
    def parse(self, file_addr):
        #parsedLines = []
        for line in open(file_addr, 'r'):
            yield self.__parseLine(line)
#              parsedLines.append(self.__parseLine(line))
             
        #return parsedLines
    def __parseLine(self, line):
        tokens = line.split("\t");
        
        
        rels = []
        paths = []
        posl = []
        nerl = []
        triggers=[]
        lexs=[]
        for token in tokens:
            if 'REL$' in token:
                s=token.strip()
                s = s[len('REL$'):]
                rels.append(s)
            elif 'pos#' in token:
                s=token.strip()
                s = s[len('pos#'):]
                posl.append(s)
            
            elif "path#" in token:             
                s=token.strip()
                s = s[len('path#'):]
                paths.append(s)
            
            elif 'ner#' in token:
                s=token.strip()
                s = s[len('ner#'):]
                nerl.append(s)
            
            elif 'trigger#' in token:
                s=token.strip()
                s = s[len('trigger#'):]
                triggers.append(s)
            
            elif 'lex#' in token:
                s=token.strip()
                s = s[len('lex#'):]
                lexs.append(s)
        
        
        res={'label':tokens[0].strip()}
        res['lhs']=tokens[1].strip()
        res['rhs']=tokens[2].strip()
        res['rel'] = rels
        res['path'] = paths
        res['pos'] = posl
        res['ner']= nerl
        res['trigger'] = triggers
        res['lemma']=lexs
        return res
        '''  
        print line
        print tokens
        print 'label: ', tokens[0]
        print 'lhs: ', tokens[1]
        print 'rhs:  ', tokens[2]
        print 'rels: ', len(rels), rels
        print 'path: ', len(paths), paths
        print 'pos: ', len(posl), posl
        print 'trigger: ', len(triggers), triggers
        print 'lemma: ', len(lexs), lexs
        print 'ner: ', len(nerl), nerl  
        print
        print
       '''
        

    
        

