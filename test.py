# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 08:55:00 2021

@author: Jhoncone
"""
import codecs
from procesamiento import procesar
from clasificar import clasificartextos
class test:
      if __name__ == '__main__':
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
          
          
          q4=clasificartextos("./test")
          #retorna los textos  en un dataframe de pandas
          #q4.pands
          #retorna el dataframe editado
          #q4.editar
          #q4.bagcorpus
          #q4.nubeword
          q4.texblob