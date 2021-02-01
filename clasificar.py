# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 08:36:26 2021

@author: Jhoncone
"""

import re
import os
import codecs
import string
import nltk
import pandas as pd
#import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
#from sklearn.feature_extraction import text 
from textblob import TextBlob
from nltk.corpus import stopwords
bands=['dic1','dic2','dic3','dic4','dic5']

  
class clasificartextos:
    
    def __init__(self,ruta):
        
        self.rutafiles=ruta
        self.pands=self.generarpandas()
        self.editar=self.editar_pandas(self.pands)
        self.corpus=self.generarcorpus(self.editar)
        #corpus clean
        self.bagcorpus=self.bagofcorpus(self.corpus)
        self.data=self.datacorpus()
        self.wordbag=self.word_usos(self.data)
        self.newcorpus=self.corpus_new(self.data,self.wordbag)
        self.newbag=self.newbagcorpus(self.newcorpus)#con stopwords
        self.nubeword=self.nubeofwords(self.corpus,self.data,self.newbag)
        self.texblob=self.analisistex()
        #self.returow=self.retornar_rowdoc(self.retnomdoc)
    def generarpandas(self):
        filePath = []
        for file in os.listdir(self.rutafiles):
            filePath.append(os.path.join(self.rutafiles, file))   
        
        fileName = re.compile('\\\\(.*)\.yml')
    
        data = {}
        for file in filePath:
            #print("jgp")
            key = fileName.search(file)
            with codecs.open(file, "r", "utf-8-sig") as readFile:
                data[key[1]] = [readFile.read()]                
                #data[key[1]] = [file_to_terms[file]]#copia palabras separadas por comas
        dfs = pd.DataFrame(data).T.reset_index().rename(columns = {'index':'ymls', 0:'textos'})
    
        return dfs
    
    def editar_pandas(self,df):
        df.columns=['textos','transcript']
        df=df.sort_index()
        return df
    
    
    def clean_text_round1(self,text):
        '''Remueve text en square brackets, remueve puntuacion and remueve words que contienen numeros.'''
        text = text.lower()
        text = re.sub('\[.*?¿\]\%', ' ', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
        text = re.sub('\w*\d\w*', '', text)
        return text

    def clean_text_round2(self,text):
        '''Remueve signos de puntuacion adicionales.'''
        text = re.sub('[‘’“”…«»]', '', text)
        text = re.sub('\n', ' ', text)
        return text    

    def pre_procesado(self,texto):
        stopwords_sp = stopwords.words('spanish')
        texto = texto.lower()
        texto = re.sub(r"[\W\d_]+", " ", texto)
        texto = " ".join([palabra for palabra in texto.split() if palabra not in stopwords_sp])
        return texto.split()
    
    def generarcorpus(self,df):
        round1 = lambda x: self.clean_text_round1(x)

        data_clean = pd.DataFrame(df.transcript.apply(round1))



        round2 = lambda x: self.clean_text_round2(x)

        data_clean = pd.DataFrame(data_clean.transcript.apply(round2))
        df.to_pickle("corpus.pkl")
        df.to_csv("corpus.csv")#corpus formato csv
        return data_clean  

    def bagofcorpus(self,data_clean):
        # Creando  document-term matrix usando CountVectorizer, y excluyendo stopwords de spani
 
        cv = CountVectorizer(stop_words=nltk.corpus.stopwords.words('spanish'))
        data_cv = cv.fit_transform(data_clean.transcript)
        data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
        data_dtm.index = data_clean.index
 
        data_dtm.to_pickle("dtm.pkl")
        #  pickle a  cleaned data
        data_clean.to_pickle('data_clean.pkl')
        pickle.dump(cv, open("cv.pkl", "wb"))
 
        return data_dtm
        
    def datacorpus(self):
        #Analisis exploratorio
        data = pd.read_pickle('dtm.pkl')
        data = data.transpose()
        data.head()
        return data

    def word_usos(self,data):
        #Palabras mas usadas
        top_dict={}
        for c in data.columns:
            top = data[c].sort_values(ascending=False).head(30)
            top_dict[c]= list(zip(top.index, top.values))
        #print(top_dict)
        # Print the top 15 words por indice de texto
        for indx, top_words in top_dict.items():
            pass
            #print(indx)
            #print(', '.join([word for word, cont in top_words[0:14]]))
        return top_dict
    def corpus_new(self,data,top_dict):
        #Agregamos stop words
        # extrae el top 30 words para cada texto
        words = []
        for texto in data.columns:
             top = [word for (word, count) in top_dict[texto]]
        for t in top:
            words.append(t)
        #print(Counter(words).most_common())
        add_stop_words = [word for word, cont in Counter(words).most_common() if cont > 6]
        return add_stop_words
    def newbagcorpus(self,add_stop_words):
        # lee en cleaned data
        data_clean = pd.read_pickle('data_clean.pkl')
        stop_words=nltk.corpus.stopwords.words('spanish')
        for pal in add_stop_words:
            stop_words.append(pal)
        mas_stop_words=['tres','primer','primera','dos','uno','veces', 'así', 'luego', 'quizá','cosa','cosas','tan','asi','todas']
        for pal in mas_stop_words:
            stop_words.append(pal)
 
        # matrix de terminos
        cv = CountVectorizer(stop_words=stop_words)
        data_cv = cv.fit_transform(data_clean.transcript)
        data_stop = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
        data_stop.index = data_clean.index
 
        # Pickle para usar despues
        pickle.dump(cv, open("cv_stop.pkl", "wb"))
        data_stop.to_pickle("dtm_stop.pkl")
        return stop_words
    
    def nubeofwords(self,data_clean,data,stop_words):
        wc = WordCloud(stopwords=stop_words, background_color="white", colormap="Dark2",
        max_font_size=150, random_state=42)

        plt.rcParams['figure.figsize'] = [16,12]
 
        # Crea subplots  text
        for index, an in enumerate(data.columns):
            wc.generate(data_clean.transcript[an])
            plt.subplot(4, 3, index+1)
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.title(bands[index])#reemplza textos por bands
        #plt.show()
        return plt
   


    def analisistex(self):
        data = pd.read_pickle('corpus.pkl')
        #pol = lambda x: TextBlob(x).sentiment.polarity
        #pol2 = lambda x: x.sentiment.polarity
        #sub = lambda x: TextBlob(x).sentiment.subjectivity
        #sub2 = lambda x: x.sentiment.subjectivity
 
        #traducir = lambda x: TextBlob(x).translate(to="en")
 
        #data['blob_en'] = data['transcript'].apply(traducir)
        #data['polarity'] = data['blob_en'].apply(pol2)
        #data['subjectivity'] = data['blob_en'].apply(sub2)
        #data['new row']=data['transcript'].apply(word_tokenize)
        data['tokens']=data['transcript'].apply(lambda texto: self.pre_procesado(texto))#probando con la columna transcript
        return data
    
#q4=clasificartextos("./test")
#retorna los textos  en un dataframe de pandas
#q4.pands
