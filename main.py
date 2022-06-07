'''
Script de ajuste de base de dados para a importação para uso no Power BI

Autor: Lucas de Melo Jurema Guimarães
'''


''' 
1-) Importação de bibliotecas e leitura de arquivos csv e excel'''

import pandas as pd
from haversine import haversine
import numpy as np

dist = pd.read_csv('distancia.csv', sep = ';')
base = pd.read_excel('base_franquias.xlsx')
demo = pd.read_excel('demograficas.xlsx')

''' 
2-) Ajuste da Base de Franquias para organização e exportação para csv para uso em Power BI'''

base = base.sort_values(by = ['franquia', 'referencia'], ascending = False)
base.to_csv('base_franquia.csv', index=False)

'''
3-) Limpeza da base de dados de Distância para a solução do desafio e criação de um novo índice'''

dist = dist.dropna()
vendedor = dist['vendedor']
index = list(range(len(vendedor)))
index = pd.DataFrame(index)
dist = pd.concat([dist,index], ignore_index = True)
dist = dist.drop(columns=0)
dist = dist.dropna()

'''
4-) Separação do dataframe em series para cálculo da distância'''

vendedor = dist['vendedor']
print(type(vendedor))
data = dist['data_visita']
latitude = dist['lat']
longitude = dist['lon']
distancia = np.zeros(len(longitude))

'''
5-) Fase de cálculo da distância através da biblioteca Haversine '''

i = 0
while i in range(0, len(longitude)-1):#
    if vendedor[i] == vendedor[i+1]:
        if data[i] == data[i+1]:
            pontoA = (float(str(latitude[i]).replace(',','.')), float(str(longitude[i]).replace(',','.')))
            pontoB = (float(str(latitude[i+1]).replace(',','.')), float(str(longitude[i+1]).replace(',','.')))
            distancia[i] = haversine(pontoB, pontoA)
    else:
        distancia[i] = 0
    i += 1

'''
6-) Converção e adição do array de distância percorrida pelos entregadores calculada ao Dataframe para exportação
'''
distancia = pd.DataFrame(distancia)
dist = pd.concat([dist, distancia], ignore_index = True, axis = 1)
dist.columns = ['vendedor', 'latitude', 'longitude', 'data_visita', 'distancia']
dist.to_excel('distancias_novo.xlsx', index = False)


