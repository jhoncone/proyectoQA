# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 08:16:04 2021

@author: Jhoncone
"""
import re
import string
import nltk

class Preprocesar:
    def __init__(self,words):
        self.frases=words
        self.prep=self.procesarwords(self.frases)
    def procesarwords(self,word):
        word=self.clean_texto_round1(word)
        word=self.clean_texto_round2(word)
        return word          
        
     #normalizacion
    def clean_texto_round1(self,text):
        '''Remueve puntuacion .'''
        text = text.lower()
        text = re.sub('\[.*?¿\]\%', ' ', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
        text = re.sub('\w*\d\w*', '', text)
        return text

    def clean_texto_round2(self,text):
        '''Remueve signos de puntuacion adicionales.'''
        text = re.sub('[‘’“”…«»]', '', text)
        text = re.sub('\n', ' ', text)
        text = re.sub('\r', ' ', text)
        return text
    
#texto="La ubicación de cada peruano no depende necesariamente del color, sino de los diversos espacios que se ocupan cada día en la sociedad."   
#prep=Preprocesar(texto)
#pr=nltk.word_tokenize(prep.prep)

#print(pr)