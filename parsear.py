# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 08:21:40 2021

@author: Jhoncone
"""

import nltk
from preprocesamiento import  Preprocesar

class ParserConsulta:
    def __init__(self,files):
        self.nombrefile=files
        self.tokens =self.obtenerConsulta()
 
    
    def obtenerConsulta(self):
        texto=self.nombrefile
        token=Preprocesar(texto)
        tokens=token.prep
        tokens=nltk.word_tokenize(tokens)        
        #delete stopwords
        #stopwords = nltk.corpus.stopwords.words("spanish")
        tokens.sort()
        #print(tokens)       
        return set(tokens)
    
    
#q=ParserConsulta(input("ingrese una consulta: "))
#print(q.tokens)