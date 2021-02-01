# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 08:26:09 2021

@author: Jhoncone
"""
from preprocesamiento import Preprocesar
from parsear import ParserConsulta
import re
import os
import yaml
import nltk
#from nltk.stem import PorterStemmer 
import math
import codecs



class procesar:
    b = 0.75
    k = 1.2
    #Frases_coincide=1
    def __init__(self,ruta):
        Frases_coincide=1
        self.tf = {}
        self.df = {}
        self.rutafiles=ruta
        self.ymls=self.pasaryml()
        self.textos=self.sintoken()
        
        self.file_a_terms=self.procesar_file()
        self.indice=self.indice_doc(self.file_a_terms)
        self.reindx=self.regular_indx(self.file_a_terms)
        self.invertedIndx=self.inverted_indx()
        self.dltabla=self.docLtabla()
        self.dl=self.docLongi()
        self.avgdl=self.avgdoc()
        self.N=self.n_doc()
        self.idf=self.invers_df()

        qry=self.retornar_query()#retorna el primer elemento de la lista que es la consulta
        #q= ParserConsulta(input("Digite una pregunta "))
        q=ParserConsulta(qry)
        #q=set(tokenize(input("Consulta: ")))# con el set convierte una expresion que esta entre [] a {}
        query=list(q.tokens)#convirtiendo a lista
        #self.p=q#el argumento inici  que entra a self.coincide es de tipo lista sino cambiarlo
        self.p=query
        
        self.totalscore=self.BM25scores(query)
        self.clasiDocs=self.clasific_doc()
        self.retnomdoc=self.retornar_nom(query)
        self.retordoc=self.retornar_doc(self.retnomdoc)#dentro de esta variable esta el contenido que corresponde a la key anterior buscada
        self.docmayu=self.doc_mayus(self.retordoc)#convirtiendo a mayuscula el texto de la key
        self.inversed=self.calcular_idfs(self.file_a_terms)
        #passage retrievel
        self.passages=self.separar_frases(self.retordoc)     
        #calculando idfs del documento top
        self.idfsdoc=self.calcular_idfs(self.passages)
        #determinado las frases top
        self.coincide=self.top_frases(self.p,self.passages,self.idfsdoc,n=Frases_coincide)
        self.retrieve=self.informes(self.coincide)
        
        self.pregun=self.buscar_preg(self.retrieve)#contiene el indice de la pregunta
        
        self.retyml=self.retor_yml(self.retnomdoc)
        
        self.retpre,self.retolu=self.lista_pre_olu(self.retyml)
        self.retexto=self.retorn_texto(self.retyml)
        self.retresp=self.procesar_res(self.retyml,self.pregun,self.retpre,self.retolu)


        
    def retornar_query(self):
        listPre=[]
        q= (input("Digite una pregunta: "))
        a=input("Digite la alternativa A: ")
        b=input("Digite la alternativa B: ")
        c=input("Digite la alternativa C: ")
        d=input("Digite la alternativa D: ")
        e=input("Digite la alternativa E: ")
        listPre.append(q)
        listPre.append(a)
        listPre.append(b)
        listPre.append(c)
        listPre.append(d)
        listPre.append(e)
        print(listPre)
        return listPre[0]

    
    def pasaryml(self):
 
        filePath = []
        for file in os.listdir(self.rutafiles):
            filePath.append(os.path.join(self.rutafiles, file))   
       
        fileName = re.compile('\\\\(.*)\.yml')

        file_a_terms={}

        for file in filePath:
            key = fileName.search(file)
           
            with codecs.open(file, "r", "utf-8-sig") as file:
                texto_list = yaml.load(file, Loader=yaml.FullLoader)

                file_a_terms[key[1]]=texto_list
                texto=file_a_terms[key[1]]
                file_a_terms[key[1]]=texto
        return file_a_terms
        
    
    def sintoken(self):#pasar a diccionario sin tokenizar

 
        filePath = []
        for file in os.listdir(self.rutafiles):
            filePath.append(os.path.join(self.rutafiles, file))   
       
        fileName = re.compile('\\\\(.*)\.yml')

        file_a_terms={}

        for file in filePath:
            key = fileName.search(file)
            with codecs.open(file, "r", "utf-8-sig") as readFile:#codecs para poder abrir con modo utf8
                file_a_terms[key[1]]=readFile.read()
                textos=file_a_terms[key[1]]
                file_a_terms[key[1]]=textos
        return file_a_terms

    
    def procesar_file(self):

        filePath = []
        for file in os.listdir(self.rutafiles):
            filePath.append(os.path.join(self.rutafiles, file)) 

        fileName = re.compile('\\\\(.*)\.yml')

        file_a_terms={}

        for file in filePath:
            key = fileName.search(file)
            with codecs.open(file, "r", "utf-8-sig") as readFile:#codecs para poder abrir con modo utf8    
                file_a_terms[key[1]]=readFile.read()
                texto=file_a_terms[key[1]]
                #wordsintextos=self.normaliz(texto)
                proc=Preprocesar(texto)
                wordsintextos=proc.prep
                wordsintextos=nltk.word_tokenize(wordsintextos)
                file_a_terms[key[1]]=wordsintextos
        return file_a_terms

    
    def n_doc(self):
        return len(self.procesar_file())
    
    def indice_doc(self,listater):
        fileIndex = {}
        for index,word in enumerate(listater):
            if word in fileIndex.keys():
                
                fileIndex[word].append(index)
            else:
                fileIndex[word] = [index]

        return fileIndex
    
    def regular_indx(self,listaterm):
        regdex = {}

        for filenombre in listaterm.keys():
            regdex[filenombre] = self.indice_doc(listaterm[filenombre])

        return regdex
    
    def inverted_indx(self):
        total_index = {}
        regdex = self.reindx
        
        for filenombre in regdex.keys():
            self.tf[filenombre] = {}
            
            for word in regdex[filenombre].keys():
                
                self.tf[filenombre][word] = len(regdex[filenombre][word])
                
                if word in self.df.keys():
                  
                    self.df[word] += 1
                else:
                    self.df[word] = 1

                if word in total_index.keys():
                    if filenombre in total_index[word].keys():
                        total_index[word][filenombre].extend(regdex[filenombre][word])
                    else:
                        total_index[word][filenombre] = regdex[filenombre][word]
                else:
                    total_index[word] = {filenombre: regdex[filenombre][word]}

        return total_index
    
    def docLtabla(self):
        dltable = {}
        for w in self.invertedIndx.keys():
            total_freq = 0
            for file in self.invertedIndx[w].keys():
                total_freq += len(self.invertedIndx[w][file])
                
            dltable[w] = {len(self.invertedIndx[w].keys()):total_freq}
                
        return dltable

    def docLongi(self):
        dl = {}
        for file in self.file_a_terms.keys():
            dl[file]=len(self.file_a_terms[file])
        return dl
    def avgdoc(self):
        sum = 0
        for file in self.dl.keys():
            sum += self.dl[file]
            avgdl = sum/len(self.dl.keys())
        return avgdl
     
    def invers_df(self):
        idf = {}
        for w in self.df.keys():
            # idf[w] = math.log((self.N - self.df[w] + 0.5)/(self.df[w] + 0.5))
            idf[w] = math.log((self.N +1 )/self.df[w])
        return idf
    def obtener_score(self,nombrefile,qlista):
        score = 0
        for w in self.file_a_terms[nombrefile]:
            if w not in qlista:
                continue
            wc = len(self.invertedIndx[w][nombrefile])
            score += self.idf[w] * ((wc)* (self.k+1)) / (wc + self.k * 
                                                         (1 - self.b + self.b * self.dl[nombrefile] / self.avgdl))
        return score
    def BM25scores(self,qlista):
        total_score = {}#los diccionarios se tienen que declarar
        for doc in self.file_a_terms.keys():
            total_score[doc] = self.obtener_score(doc,qlista)
        return total_score
    def clasific_doc(self):
        ranked_docs = sorted(self.totalscore.items(), key=lambda x: x[1], reverse=True)
        return ranked_docs    
    
    def retornar_nom(self,qlistas):

        orde=self.clasiDocs[0]
            #orde=docu
        vari=str(orde)
        
        #regex = re.compile('[a-z][a-z][a-z] [0-9][.][t][x][t]')
        #regex = re.compile('[a-z][a-z][a-z] [0-9]')
        regex=re.compile('[A-Z][0-9][_][0-9][0-9][0-9][0-9][_][A-Z][0-9][A-Z][_][A-Z][0-9]')
        m=regex.findall(vari)
        #print(m)
        listString = ' '.join([str(elem) for elem in m])   
        #print(listString) 
        nom=listString
        return nom
        
    def retornar_doc(self,nom):
        total_nom={}
        key=nom
        total_nom[key]=self.file_a_terms.get(nom)#cambiando a diccionario asignando como key al nom 
        return total_nom
    
    def doc_mayus(self,doc):
        
        texto = ""
        #almacenando el texto en una variable
        for linea in doc:
            #linea = linea.strip()
            texto = texto + " " + linea
        return texto.upper()
        #return docmayu
    
    def separar_frases(self,filenames):
            frases = dict()
            for filenombre in filenames:
                for passage in self.textos[filenombre].split("\n"):#probando con otra forma de dividir el texto /n cada salto de linea o cada :
                    for frase in nltk.sent_tokenize(passage):
                        token=ParserConsulta(frase)
                        tokens=token.tokens
                        if tokens:
                            frases[frase] = tokens
            return frases
    
    def calcular_idfs(self,documents):
        
        inverse_doc = {}
        unique_doc =[]
        num_dic = len(documents)
        #print(num_dic)
        for k,v in documents.items():
            documents[k] = set(v)
            unique_doc.append(documents[k])
        for k,v in documents.items():
            for word in v:
                cont = 0
                for ud in unique_doc: 
                    if word in ud:
                        cont += 1
                if word not in inverse_doc.keys():
                    inverse_doc[word] = num_dic/cont
        
        return inverse_doc
    
    
    def top_frases(self,query, sentences, idfs, n):

        q_c_f = {}
        for k,v in sentences.items():
            for q in query:
                if q in v:
                    if k not in q_c_f:
                        q_c_f[k] = idfs[q]
                    else:
                        q_c_f[k] += idfs[q]
        q_c_f = {k: v for k, v in sorted(q_c_f.items(), key=lambda item: item[1],reverse=True)}
        #print(q_c_f)
        #confirma si hay mas de una coincidencia
        highest = max(q_c_f.values())
        match_frase = [k for k, v in q_c_f.items() if v == highest]
        densidad_term = {}
        if len(match_frase) > 1:
            for sentence in match_frase:
                intersec = set(sentence).interseccion(query)
                densidad_term[sentence] = len(intersec)
            densidad_term = {k: v for k, v in sorted(densidad_term.items(), key=lambda item: item[1],reverse=True)}
            fs = []
            for k in q_c_f:
                fs.append(k)
            td = fs[:n]
            return td
        #print(match_frase)
        fs = []
        for k in q_c_f:
            fs.append(k)
        sen = fs[:n]
        #print(tf)
        return sen
    
    def informes(self,frase):
        for fr in frase:
            infor=fr
        return fr
    
    def buscar_preg(self,consulta):
        pretok=nltk.word_tokenize(consulta)
        #print(pretok)
        #obteniendo con el primer elemento de la lista
        preel=pretok[0]
        return preel
    
    def retor_yml(self,nombreyml):
        texto_list=self.ymls.get(nombreyml)
        #tokens=texto_list
        return texto_list
        
    def lista_pre_olu(self,tokens):
        lispreg=[]
        regex = re.compile('[p][r][e][g][u][n][t][a][0-9]')

        for dics in tokens:
            if regex.findall(dics)!=None:
                m=regex.findall(dics)
                listString = ' '.join([str(elem) for elem in m]) 
                nom=listString
                lispreg.append(nom)
            else:
                pass

        listafil=['',' ','  ']
        #print(lispreg)
        b=[]
        for lis in lispreg:
            if lis not in listafil:
                 b.append(lis)
    
        #print(b)


        #obteniendo la lista de soluciones en el texto
        lisolu=[]
        regex = re.compile('[s][o][l][u][c][i][o][n][0-9]')

        for dics in tokens:
            if regex.findall(dics)!=None:
                m=regex.findall(dics)
                listString = ' '.join([str(elem) for elem in m]) 
                olu=listString
                lisolu.append(olu)
            else:
                pass
                #print("no token pregunta")



        s=[]
        for olu in lisolu:
            if olu not in listafil:
                s.append(olu)
        
        return b,s
    
    def retorn_texto(self,texto_list):
        texto=texto_list.get('texto')
        #print(texto)
        return texto
    
    def procesar_res(self,texto_list,preel,b,s):
        longi=len(b)
        #print(longi)
        i=0

        for pre in enumerate(b):
            if preel in b:
                pregun=preel

        for i in range(longi):
            if b[i]==pregun:
                pos=i
        
        #print("pos ",pos,"val ",pregun)
        pregun=texto_list.get(pregun)

        #print(pos)
        olu=s[pos]
        #print(olu)

        #obteniendo la solucion 

        luc=texto_list.get(olu)

        #print(luc)
        luc2=list(luc.values())
        alt=luc2[0]
        #print(alt)
        #imprimiendo la solucion
        dic=texto_list.get('alternativas'+str(pos+1))
        dic2=dic.get(alt)
        #print(dic)
        ans=alt+':'+dic2
        #print(ans)
        #print("ol")
        return ans
    
    
'''    
q3=procesar("./test")
#print(q3.ymls)
#print(q3.textos)
#print(q3.file_a_terms)


#print(q3.file_a_terms.keys())

#print(q3.indice)
#print(q3.reindx)
#print(q3.invertedIndx)



#print(q3.dltabla)
#print(q3.dl)
#print(q3.avgdl)
#print(q3.N)
#print(q2.idf)
#print(q3.totalscore)

#grafico de scores

#print(q3.clasiDocs)
#print("proban")
#print(q3.retnomdoc)
#print(q3.retordoc)
#print(q3.docmayu)

#print(q3.inversed)
#print(q3.p)
#print(q3.passages)
#print(q3.idfsdoc)

#testeado con el archivo new2 .txt de la carpeta blo  sucess
#en el texto 3 al reducir la pregunta 2 sin sostener si encuentra la respuesta
print(q3.retrieve)
#retornando el archivo yml donde esta la pregunta
#print(q3.retyml)
#retorna la lista de preguntas que hay en el archivo
#print(q3.retpre)
#retorna la lista de soluciones de la pregunta
#print(q3.retolu)
#retorna el texto donde esta la pregunta
#print(q3.retexto)

#retorna la respuesta
print(q3.retresp)
'''    