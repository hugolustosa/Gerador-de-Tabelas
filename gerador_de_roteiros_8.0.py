import networkx as nx
import random
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import collections
import pandas as pd
import math
import win32com.client as win32
import time
import folium
import requests
import json
import emoji
from shapely.geometry import Point, Polygon
import itertools
import PySimpleGUI as sg

########################################################### 
#DADOS DE ENTRADA DO GRAFO

tabelao = 'input.xlsx'

arestas_df = pd.read_excel(tabelao, sheet_name = 'arestas')

vertices_df = pd.read_excel(tabelao, sheet_name = 'vertices')

vertices2_df = pd.read_excel(tabelao, sheet_name = 'vertices')

portoes_quadriculas_df = pd.read_excel(tabelao, sheet_name = 'portoes_quadriculas') # quadriculas da bacia de santos

portoes_faixas_bc_df = pd.read_excel(tabelao, sheet_name = 'portoes_faixas_bc') # faixas da bacia de campos




########################################################### 
# ENTRADA DOS AERODROMOS E PLATAFORMAS

# Define the window's contents
layout = [[sg.Text("INFORME O ROTEIRO")],
          [sg.Text("ORIGEM"), sg.Combo(list(vertices_df.loc[vertices_df["TIPO"] == '1.BASE', "PONTO"]), key='-INPUT_ORIGEM-')],
          [sg.Text("UM 1"),sg.Combo(list(vertices_df.loc[vertices_df["TIPO"] == '3.UM', "PONTO"]),key='-INPUT_UM1-')],
          [sg.Text("UM 2"),sg.Combo(list(vertices_df.loc[vertices_df["TIPO"] == '3.UM', "PONTO"]),key='-INPUT_UM2-'), sg.Text("Caso não tenha UM 2 repita a UM 1")],
          [sg.Text("UM 3"),sg.Combo(list(vertices_df.loc[vertices_df["TIPO"] == '3.UM', "PONTO"]),key='-INPUT_UM3-'), sg.Text("Caso não tenha UM 3 repita a UM 2")],
          [sg.Text("UM 4"),sg.Combo(list(vertices_df.loc[vertices_df["TIPO"] == '3.UM', "PONTO"]),key='-INPUT_UM4-'), sg.Text("Caso não tenha UM 4 repita a UM 3")],
          [sg.Text("DESTINO"),sg.Combo(list(vertices_df.loc[vertices_df["TIPO"] == '1.BASE', "PONTO"]),key='-INPUT_DESTINO_FINAL-')],
          [sg.Text(size=(60,5), key='-OUTPUT-')],
          [sg.Button('CONFIRMAR DESTINOS'), sg.Button('ROTEIRIZAR')]]


# Create the window
window = sg.Window('ROTEIRIZADOR AEREO (by LOFF/OPTA) - Versao 1.0', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'ROTEIRIZAR':
        break
    # Output a message to the window
    window['-OUTPUT-'].update(f"O roteiro escolhido foi: {values['-INPUT_ORIGEM-']}=>{values['-INPUT_UM1-']}=>{values['-INPUT_UM2-']}=>{values['-INPUT_UM3-']}=>{values['-INPUT_UM4-']}=>{values['-INPUT_DESTINO_FINAL-']}. Obrigado por utilizar o Roteirizador! Aperte ROTEIRIZAR para verificar os resultados no diretório.")


origem = values['-INPUT_ORIGEM-']
destino1 = values['-INPUT_UM1-']
destino2 = values['-INPUT_UM2-']
destino3 = values['-INPUT_UM3-']
destino4 = values['-INPUT_UM4-']
pouso_final = values['-INPUT_DESTINO_FINAL-']
 
########################################################### 

antes = time.time()
data_hora = time.strftime('%Y-%m-%d %Hh%Mm%S', time.localtime())


lista_destinos = [destino1, destino2, destino3, destino4]

num_pousos = 1
for i in range(1, len(lista_destinos)):
    if lista_destinos[i] != lista_destinos[i-1]:
        num_pousos = num_pousos + 1


lista_permutacoes_total = list(itertools.permutations(lista_destinos))

lista_permutacoes = []

for i in lista_permutacoes_total:
    if i not in lista_permutacoes:
        lista_permutacoes.append(i)


###########################################################
# dados das poligonais da BS 

'''https://automating-gis-processes.github.io/CSC18/lessons/L4/point-in-polygon.html'''

poligono_coords_BS = Polygon([(-23.7108916666667,-43.6677416666667),(-23.5687611111111,-43.1358916666667),(-23,1775611111111,-42.7796305555556),(-23,1029444444444,-42.4989027777778),(-23,5058833333333,-42.4989),(-23,5058805555556,-41.9987138888889),(-24,3333333333333,-41.6666666666667),(-25,-41.6666666666667),(-25.6666666666667,-42.3333333333333),(-26.333325,-43.3333138888889),(-26.333325,-43.6666472222222)])


coord_QDA4 = ['QDA4', Polygon([(-25,-43.3333333333333),(-25,-43.1666666666667),(-25.1666666666667,-43.1666666666667),(-25.1666666666667,-43.3333333333333)])]

coord_QDA5 = ['QDA5', Polygon([(-25.1666666666667,-43.3333333333333),(-25.1666666666667,-43.1666666666667),(-25.3333333333333,-43.1666666666667),(-25.3333333333333,-43.3333333333333)])]

coord_QDA6 = ['QDA6', Polygon([(-25.3333333333333,-43.3333333333333),(-25.3333333333333,-43.1666666666667),(-25.5,-43.1666666666667),(-25.5,-43.3333333333333)])]

coord_QDA7 = ['QDA7', Polygon([(-25.5,-43.3333333333333),(-25.5,-43.1666666666667),(-25.6666666666667,-43.1666666666667),(-25.6666666666667,-43.3333333333333)])]

coord_QDA8 = ['QDA8', Polygon([(-25.6666666666667,-43.3333333333333),(-25.6666666666667,-43.1666666666667),(-25.8333333333333,-43.1666666666667),(-25.8333333333333,-43.3333333333333)])]

coord_QDA9 = ['QDA9', Polygon([(-25.8333333333333,-43.3333333333333),(-25.8333333333333,-43.1666666666667),(-26,-43.1666666666667),(-26,-43.3333333333333)])]

coord_QDB4 = ['QDB4', Polygon([(-25,-43.1666666666667),(-25,-43),(-25.1666666666667,-43),(-25.1666666666667,-43.1666666666667)])]

coord_QDB5 = ['QDB5', Polygon([(-25.1666666666667,-43.1666666666667),(-25.1666666666667,-43),(-25.3333333333333,-43),(-25.3333333333333,-43.1666666666667)])]

coord_QDB6 = ['QDB6', Polygon([(-25.3333333333333,-43.1666666666667),(-25.3333333333333,-43),(-25.5,-43),(-25.5,-43.1666666666667)])]

coord_QDB7 = ['QDB7', Polygon([(-25.5,-43.1666666666667),(-25.5,-43),(-25.6666666666667,-43),(-25.6666666666667,-43.1666666666667)])]

coord_QDB8 = ['QDB8', Polygon([(-25.6666666666667,-43.1666666666667),(-25.6666666666667,-43),(-25.8333333333333,-43),(-25.8333333333333,-43.1666666666667)])]

coord_QDB9 = ['QDB9', Polygon([(-25.8333333333333,-43.1666666666667),(-25.8333333333333,-43),(-26,-43),(-26,-43.1666666666667)])]

coord_QDC4 = ['QDC4', Polygon([(-25,-43),(-25,-42.8333333333333),(-25.1666666666667,-42.8333333333333),(-25.1666666666667,-43)])]

coord_QDC5 = ['QDC5', Polygon([(-25.1666666666667,-43),(-25.1666666666667,-42.8333333333333),(-25.3333333333333,-42.8333333333333),(-25.3333333333333,-43)])]

coord_QDC6 = ['QDC6', Polygon([(-25.3333333333333,-43),(-25.3333333333333,-42.8333333333333),(-25.5,-42.8333333333333),(-25.5,-43)])]

coord_QDC7 = ['QDC7', Polygon([(-25.5,-43),(-25.5,-42.8333333333333),(-25.6666666666667,-42.8333333333333),(-25.6666666666667,-43)])]

coord_QDC8 = ['QDC8', Polygon([(-25.6666666666667,-43),(-25.6666666666667,-42.8333333333333),(-25.8333333333333,-42.8333333333333),(-25.8333333333333,-43)])]

coord_QDC9 = ['QDC9', Polygon([(-25.8333333333333,-43),(-25.8333333333333,-42.8333333333333),(-26,-42.8333333333333),(-26,-43)])]

coord_QDD4 = ['QDD4', Polygon([(-25,-42.8333333333333),(-25,-42.6666666666667),(-25.1666666666667,-42.6666666666667),(-25.1666666666667,-42.8333333333333)])]

coord_QDD5 = ['QDD5', Polygon([(-25.1666666666667,-42.8333333333333),(-25.1666666666667,-42.6666666666667),(-25.3333333333333,-42.6666666666667),(-25.3333333333333,-42.8333333333333)])]

coord_QDD6 = ['QDD6', Polygon([(-25.3333333333333,-42.8333333333333),(-25.3333333333333,-42.6666666666667),(-25.5,-42.6666666666667),(-25.5,-42.8333333333333)])]

coord_QDD7 = ['QDD7', Polygon([(-25.5,-42.8333333333333),(-25.5,-42.6666666666667),(-25.6666666666667,-42.6666666666667),(-25.6666666666667,-42.8333333333333)])]

coord_QDD8 = ['QDD8', Polygon([(-25.6666666666667,-42.8333333333333),(-25.6666666666667,-42.6666666666667),(-25.8333333333333,-42.6666666666667),(-25.8333333333333,-42.8333333333333)])]

coord_QDD9 = ['QDD9', Polygon([(-25.8333333333333,-42.8333333333333),(-25.8333333333333,-42.6666666666667),(-26,-42.6666666666667),(-26,-42.8333333333333)])]

coord_QDE0 = ['QDE0', Polygon([(-24.3333333333333,-42.6666666666667),(-24.3333333333333,-42.5),(-24.5,-42.5),(-24.5,-42.6666666666667)])]

coord_QDE1 = ['QDE1', Polygon([(-24.5,-42.6666666666667),(-24.5,-42.5),(-24.6666666666667,-42.5),(-24.6666666666667,-42.6666666666667)])]

coord_QDE2 = ['QDE2', Polygon([(-24.6666666666667,-42.6666666666667),(-24.6666666666667,-42.5),(-24.8333333333333,-42.5),(-24.8333333333333,-42.6666666666667)])]

coord_QDE3 = ['QDE3', Polygon([(-24.8333333333333,-42.6666666666667),(-24.8333333333333,-42.5),(-26,-42.5),(-26,-42.6666666666667)])]

coord_QDF0 = ['QDF0', Polygon([(-24.3333333333333,-42.5),(-24.3333333333333,-42.3333333333333),(-24.5,-42.3333333333333),(-24.5,-42.5)])]

coord_QDF1 = ['QDF1', Polygon([(-24.5,-42.5),(-24.5,-42.3333333333333),(-24.6666666666667,-42.3333333333333),(-24.6666666666667,-42.5)])]

coord_QDF2 = ['QDF2', Polygon([(-24.6666666666667,-42.5),(-24.6666666666667,-42.3333333333333),(-24.8333333333333,-42.3333333333333),(-24.8333333333333,-42.5)])]

coord_QDF3 = ['QDF3', Polygon([(-24.8333333333333,-42.5),(-24.8333333333333,-42.3333333333333),(-26,-42.3333333333333),(-26,-42.5)])]

coord_QDG0 = ['QDG0', Polygon([(-24.3333333333333,-42.3333333333333),(-24.3333333333333,-42.1666666666667),(-24.5,-42.1666666666667),(-24.5,-42.3333333333333)])]

coord_QDG1 = ['QDG1', Polygon([(-24.5,-42.3333333333333),(-24.5,-42.1666666666667),(-24.6666666666667,-42.1666666666667),(-24.6666666666667,-42.3333333333333)])]

coord_QDG2 = ['QDG2', Polygon([(-24.6666666666667,-42.3333333333333),(-24.6666666666667,-42.1666666666667),(-24.8333333333333,-42.1666666666667),(-24.8333333333333,-42.3333333333333)])]

coord_QDG3 = ['QDG3', Polygon([(-24.8333333333333,-42.3333333333333),(-24.8333333333333,-42.1666666666667),(-26,-42.1666666666667),(-26,-42.3333333333333)])]

coord_QDH0 = ['QDH0', Polygon([(-24.3333333333333,-42.1666666666667),(-24.3333333333333,-42),(-24.5,-42),(-24.5,-42.1666666666667)])]

coord_QDH1 = ['QDH1', Polygon([(-24.5,-42.1666666666667),(-24.5,-42),(-24.6666666666667,-42),(-24.6666666666667,-42.1666666666667)])]

coord_QDH2 = ['QDH2', Polygon([(-24.6666666666667,-42.1666666666667),(-24.6666666666667,-42),(-24.8333333333333,-42),(-24.8333333333333,-42.1666666666667)])]

coord_QDH3 = ['QDH3', Polygon([(-24.8333333333333,-42.1666666666667),(-24.8333333333333,-42),(-26,-42),(-26,-42.1666666666667)])]

lista_quadrantes = [coord_QDA4, coord_QDA5, coord_QDA6, coord_QDA7, coord_QDA8, coord_QDA9, coord_QDB4, coord_QDB5, coord_QDB6, coord_QDB7, coord_QDB8, coord_QDB9, coord_QDC4, coord_QDC5, coord_QDC6, coord_QDC7, coord_QDC8, coord_QDC9, coord_QDD4, coord_QDD5, coord_QDD6, coord_QDD7, coord_QDD8, coord_QDD9, coord_QDE0, coord_QDE1, coord_QDE2, coord_QDE3, coord_QDF0, coord_QDF1, coord_QDF2, coord_QDF3, coord_QDG0, coord_QDG1, coord_QDG2, coord_QDG3, coord_QDH0, coord_QDH1, coord_QDH2, coord_QDH3]

###########################################################
# dados das poligonais da BC 

poligono_coords_BC = Polygon([(-23.0085,-41.2133333333333),	(-22.907,-41.1161666666667),	(-22.7985,-41.0125),	(-22.7311666666667,-40.9101666666667),	(-22.6836666666667,-40.8098333333333),	(-22.5881666666667,-40.7028333333333),	(-22.4898333333333,-40.6283333333333),	(-22.379,-40.5826666666667),	(-22.2428333333333,-40.5698333333333),	(-22.1201666666667,-40.5531666666667),	(-21.9931666666667,-40.5511666666667),	(-21.7093333333333,-39.595),	(-21.9413333333333,-39.6218333333333),	(-22.1575,-39.6403333333333),	(-22.3995,-39.6658333333333),	(-22.5975,-39.7355),	(-22.79,-39.9646666666667),	(-22.976,-39.9646666666667),	(-23.0913333333333,-40.0955),	(-23.2485,-40.2511666666667),	(-23.3963333333333,-40.5418333333333),	(-23.2098333333333,-41.0435)])


coord_faixaBC1 = ['faixaBC1', Polygon([(-23.2098333333333,-41.0435),	(-23.0085,-41.2133333333333),	(-22.907,-41.1161666666667),	(-23.3963333333333,-40.5418333333333)])]

coord_faixaBC2 = ['faixaBC2', Polygon([(-23.3963333333333,-40.5418333333333),	(-22.907,-41.1161666666667),	(-22.7985,-41.0125),	(-23.2485,-40.2511666666667)])]

coord_faixaBC3 = ['faixaBC3', Polygon([(-23.2485,-40.2511666666667),	(-22.7985,-41.0125),	(-22.7311666666667,-40.9101666666667),	(-23.0913333333333,-40.0955)])]

coord_faixaBC4 = ['faixaBC4', Polygon([(-23.0913333333333,-40.0955),	(-22.7311666666667,-40.9101666666667),	(-22.6836666666667,-40.8098333333333),	(-22.976,-39.9646666666667)])]

coord_faixaBC5 = ['faixaBC5', Polygon([(-22.976,-39.9646666666667),	(-22.6836666666667,-40.8098333333333),	(-22.5881666666667,-40.7028333333333),	(-22.79,-39.9646666666667)])]

coord_faixaBC6 = ['faixaBC6', Polygon([(-22.79,-39.9646666666667),	(-22.5881666666667,-40.7028333333333),	(-22.4898333333333,-40.6283333333333),	(-22.5975,-39.7355)])]

coord_faixaBC7 = ['faixaBC7', Polygon([(-22.5975,-39.7355),	(-22.4898333333333,-40.6283333333333),	(-22.379,-40.5826666666667),	(-22.3995,-39.6658333333333)])]

coord_faixaBC8 = ['faixaBC8', Polygon([(-22.3995,-39.6658333333333),	(-22.379,-40.5826666666667),	(-22.2428333333333,-40.5698333333333),	(-22.1575,-39.6403333333333)])]

coord_faixaBC9 = ['faixaBC9', Polygon([(-22.1575,-39.6403333333333),	(-22.2428333333333,-40.5698333333333),	(-22.1201666666667,-40.5531666666667),	(-21.9413333333333,-39.6218333333333)])]

coord_faixaBC10 = ['faixaBC10', Polygon([(-21.9413333333333,-39.6218333333333),	(-22.1201666666667,-40.5531666666667),	(-21.9931666666667,-40.5511666666667),	(-21.7093333333333,-39.595)])]

lista_faixasBC = [coord_faixaBC1, coord_faixaBC2, coord_faixaBC3, coord_faixaBC4, coord_faixaBC5, coord_faixaBC6, coord_faixaBC7, coord_faixaBC8, coord_faixaBC9, coord_faixaBC10]

########################################################### 

for v1 in vertices_df.index:
    if vertices_df.loc[v1]['PONTO'] == origem:
        lat_origem = vertices_df.loc[v1]['LAT']
        long_origem = vertices_df.loc[v1]['LONG']

    if vertices_df.loc[v1]['PONTO'] == pouso_final:
        lat_pouso_final = vertices_df.loc[v1]['LAT']
        long_pouso_final = vertices_df.loc[v1]['LONG']


coord_origem = Point(lat_origem, long_origem)
coord_pouso_final = Point(lat_pouso_final, long_pouso_final)


def distancia_geodesica(lat1, long1, lat2, long2):
    '''função que retorna a distancia em milhas náuticas a partir das coordenadas geográficas de dois pontos. Leva em consideração a curvatura da Terra'''
    return 3440 * math.acos(math.cos((90-lat1)*0.017453292519943295) * math.cos((90-lat2)*0.017453292519943295) + math.sin((90-lat1)*0.017453292519943295) * math.sin((90-lat2)*0.017453292519943295) * math.cos((long1-long2)*0.017453292519943295))
    
########################################################### 

#GERAR TODOS OS CENÁRIOS DE ROTEIROS

lat_destino1 = 0
long_destino1 = 0
lat_destino2 = 0
long_destino2 = 0
lat_destino3 = 0
long_destino3 = 0
lat_destino4 = 0
long_destino4 = 0

dicionario_resultado = {}

for permutacao in range(len(lista_permutacoes)):
    destino1 = lista_permutacoes[permutacao][0]
    destino2 = lista_permutacoes[permutacao][1]
    destino3 = lista_permutacoes[permutacao][2]
    destino4 = lista_permutacoes[permutacao][3]
    
    
    arestas_df = pd.read_excel(tabelao, sheet_name = 'arestas')
    vertices2_df = pd.read_excel(tabelao, sheet_name = 'vertices')
   
    for v2 in vertices2_df.index:
 
          
        if vertices2_df.loc[v2]['PONTO'] == destino1:
            lat_destino1 = vertices2_df.loc[v2]['LAT']
            long_destino1 = vertices2_df.loc[v2]['LONG']
            
        if vertices2_df.loc[v2]['PONTO'] == destino2:
            lat_destino2 = vertices2_df.loc[v2]['LAT']
            long_destino2 = vertices2_df.loc[v2]['LONG']    
            
        if vertices2_df.loc[v2]['PONTO'] == destino3:
            lat_destino3 = vertices2_df.loc[v2]['LAT']
            long_destino3 = vertices2_df.loc[v2]['LONG'] 
    
        if vertices2_df.loc[v2]['PONTO'] == destino4:
            lat_destino4 = vertices2_df.loc[v2]['LAT']
            long_destino4 = vertices2_df.loc[v2]['LONG'] 
            

    coord_destino1 = Point(lat_destino1, long_destino1)
    coord_destino2 = Point(lat_destino2, long_destino2)
    coord_destino3 = Point(lat_destino3, long_destino3)
    coord_destino4 = Point(lat_destino4, long_destino4)

    
    ###########################################################  
   
    #verificação se o destino está no espaço aéreo da BS ou BC, verifica qual quadrícula ou faixa e encontra e acrescenta as arestas de chegada e saida da plataforma
    
    #para BS:
    lat_portao_entrada_quadricula = 0
    long_portao_entrada_quadricula = 0
    tamanho_aresta_ida = 0
    tamanho_aresta_volta = 0
    contador = 0
    
    #para BC:
    lat_portao_entrada_faixa = 0
    long_portao_entrada_faixa = 0
    lat_portao_saida_faixa = 0
    long_portao_saida_faixa = 0   
    lat_limite_entrada = 0
    long_limite_entrada = 0
    lat_limite_saida = 0
    long_limite_saida = 0
        
    lat_traves_ida = 0
    long_traves_ida = 0
    lat_traves_volta = 0
    long_traves_volta = 0
  
            
    ########################################################### 
    
    # conferencia do destino1 (1ª PLATAFORMA)
        
    if coord_destino1.within(poligono_coords_BS) == True: #verifica se o destino1 está dentro da poligonal da BS
        for i in lista_quadrantes:
            if i[1].contains(coord_destino1) == True: #verifica se está dentro dos quadrantes da BS
                contador = contador + 1
                quadrante_destino1 = i[0]
                for j in portoes_quadriculas_df.index:
                    if portoes_quadriculas_df.loc[j]['QUADRICULA'] == quadrante_destino1:
                        portao_entrada_quadricula = portoes_quadriculas_df.loc[j]['ENTRADA']
                        portao_saida_quadricula = portoes_quadriculas_df.loc[j]['SAIDA']
                       
                        for k in vertices2_df.index:
                            if vertices2_df.loc[k]['PONTO'] == portao_entrada_quadricula:
                                lat_portao_entrada_quadricula = vertices2_df.loc[k]['LAT']
                                long_portao_entrada_quadricula = vertices2_df.loc[k]['LONG']
                                tamanho_aresta_ida = coord_destino1.distance(Point(lat_portao_entrada_quadricula, long_portao_entrada_quadricula)) * 60
                                indice_aresta_1 = -random.random()
                                arestas_df.at[indice_aresta_1, 'ORIGEM'] = portao_entrada_quadricula
                                arestas_df.at[indice_aresta_1, 'DESTINO'] = destino1
                                arestas_df.at[indice_aresta_1, 'DISTANCIA'] = tamanho_aresta_ida                        
                                                                                          
                           
                            if vertices2_df.loc[k]['PONTO'] == portao_saida_quadricula:
                                lat_portao_saida_quadricula = vertices2_df.loc[k]['LAT']
                                long_portao_saida_quadricula = vertices2_df.loc[k]['LONG']    
                                tamanho_aresta_volta = coord_destino1.distance(Point(lat_portao_saida_quadricula, long_portao_saida_quadricula)) * 60
                                indice_aresta_2 = -random.random()
                                arestas_df.at[indice_aresta_2, 'ORIGEM'] = destino1
                                arestas_df.at[indice_aresta_2, 'DESTINO'] = portao_saida_quadricula
                                arestas_df.at[indice_aresta_2, 'DISTANCIA'] = tamanho_aresta_volta
        
        if contador == 0: # para o caso de estar dentro da poligonal da BS, porém fora das quadrículas

            waypoint_entrada = ''
            waypoint_saida = ''
            distancia_waypoint_entrada = 99999999
            distancia_waypoint_saida = 99999999
            
            for m in vertices_df.index:
                if (vertices_df['SENTIDO'][m] == 'IN' or vertices_df['SENTIDO'][m] == 'IN_OUT') and vertices_df['LAT'][m] > lat_destino1:
                    lat_waypoint_entrada = vertices_df.loc[m]['LAT']
                    long_waypoint_entrada = vertices_df.loc[m]['LONG']
                    distancia_waypont_entrada_prov = coord_destino1.distance(Point(lat_waypoint_entrada, long_waypoint_entrada)) * 60
                    if distancia_waypont_entrada_prov < distancia_waypoint_entrada:
                        distancia_waypoint_entrada = distancia_waypont_entrada_prov
                        waypoint_entrada = vertices_df['PONTO'][m]
                    
                if (vertices_df['SENTIDO'][m] == 'OUT' or vertices_df['SENTIDO'][m] == 'IN_OUT') and vertices_df['LAT'][m] > lat_destino1:
                    lat_waypoint_saida = vertices_df.loc[m]['LAT']
                    long_waypoint_saida = vertices_df.loc[m]['LONG']
                    distancia_waypont_saida_prov = coord_destino1.distance(Point(lat_waypoint_saida, long_waypoint_saida)) * 60
                    if distancia_waypont_saida_prov < distancia_waypoint_saida:
                        distancia_waypoint_saida = distancia_waypont_saida_prov
                        waypoint_saida = vertices_df['PONTO'][m]                    
           
            # cria a aresta do waypoint de entrada para a plataforma    
            indice_aresta_3 = -random.random()
            arestas_df.at[indice_aresta_3, 'ORIGEM'] = waypoint_entrada
            arestas_df.at[indice_aresta_3, 'DESTINO'] = destino1
            arestas_df.at[indice_aresta_3, 'DISTANCIA'] = distancia_waypoint_entrada                
                    
            # cria a aresta da plataforma para o waypoint de saída   
            indice_aresta_4 = -random.random()
            arestas_df.at[indice_aresta_4, 'ORIGEM'] = destino1
            arestas_df.at[indice_aresta_4, 'DESTINO'] = waypoint_saida
            arestas_df.at[indice_aresta_4, 'DISTANCIA'] = distancia_waypoint_saida             
                        
                              
    # CASO PLATAFORMA 1 ESTEJA FORA DA ÁREA DO ESPAÇO AÉREO DA BS E BC       
            
    if coord_destino1.within(poligono_coords_BS) == False and coord_destino1.within(poligono_coords_BC) == False: 
        indice_aresta_5 = -random.random()
        arestas_df.at[indice_aresta_5, 'ORIGEM'] = origem
        arestas_df.at[indice_aresta_5, 'DESTINO'] = destino1
        arestas_df.at[indice_aresta_5, 'DISTANCIA'] = distancia_geodesica(lat_origem, long_origem, lat_destino1, long_destino1)                    
        
        indice_aresta_6 = -random.random()
        arestas_df.at[indice_aresta_6, 'ORIGEM'] = destino1
        arestas_df.at[indice_aresta_6, 'DESTINO'] = pouso_final
        arestas_df.at[indice_aresta_6, 'DISTANCIA'] = distancia_geodesica(lat_destino1, long_destino1, lat_pouso_final, long_pouso_final)   
      
    
    # CASO PLATAFORMA 1 ESTEJA DENTRO DA ÁREA DO ESPAÇO AÉREO DA BC 
    
    portao_entrada_faixa = ''
    portao_saida_faixa = ''
    vetor_u_in = np.array([0, 0]) # vetor que liga o portão de entrada da faixa a plataforma
    vetor_u_out = np.array([0, 0]) # vetor que liga o extremo da saida da faixa a platarforma
    vetor_v_in = np.array([0, 0]) # vetor que liga o portão de entrada da faixa ao limite do segmento de reta da entrada
    vetor_v_out = np.array([0, 0]) # vetor que liga o limite extremo da faixa sentido saida para portão de saida da faixa
    modulo_vetor_v_in = 0
    modulo_vetor_v_out = 0
    proj_of_u_in_on_v_in = np.array([0, 0])
    proj_of_u_out_on_v_out = np.array([0, 0])
    
        
    if coord_destino1.within(poligono_coords_BC) == True: # verifica se está dentro da poligonal BC   
        for faixa1 in lista_faixasBC:
            if faixa1[1].contains(coord_destino1) == True: # verifica se está dentro das faixas
                faixa_destino1 = faixa1[0]
                for jj in portoes_faixas_bc_df.index:
                    if portoes_faixas_bc_df.loc[jj]['faixa'] == faixa_destino1:                       
                        portao_entrada_faixa = portoes_faixas_bc_df.loc[jj]['point_in']
                        portao_saida_faixa = portoes_faixas_bc_df.loc[jj]['point_out']
                        lat_portao_entrada_faixa = portoes_faixas_bc_df.loc[jj]['lat_point_in']
                        long_portao_entrada_faixa = portoes_faixas_bc_df.loc[jj]['long_point_in']
                        lat_portao_saida_faixa = portoes_faixas_bc_df.loc[jj]['lat_point_out']
                        long_portao_saida_faixa = portoes_faixas_bc_df.loc[jj]['long_point_out']
                        lat_limite_entrada = portoes_faixas_bc_df.loc[jj]['lat_point_limit_in']
                        long_limite_entrada = portoes_faixas_bc_df.loc[jj]['long_point_limit_in']
                        lat_limite_saida = portoes_faixas_bc_df.loc[jj]['lat_point_limit_out']
                        long_limite_saida = portoes_faixas_bc_df.loc[jj]['long_point_limit_out']
                        
                        vetor_u_in = np.array([long_destino1 - long_portao_entrada_faixa, lat_destino1 - lat_portao_entrada_faixa])
                        vetor_u_out = np.array([long_destino1 - long_limite_saida, lat_destino1 - lat_limite_saida])
                        
                        vetor_v_in = np.array([long_limite_entrada - long_portao_entrada_faixa, lat_limite_entrada - lat_portao_entrada_faixa])
                        vetor_v_out = np.array([long_portao_saida_faixa - long_limite_saida, lat_portao_saida_faixa - lat_limite_saida])
                        
                        modulo_vetor_v_in = np.sqrt(sum(vetor_v_in**2))
                        modulo_vetor_v_out = np.sqrt(sum(vetor_v_out**2))
                        
                        proj_of_u_in_on_v_in = (np.dot(vetor_u_in, vetor_v_in)/modulo_vetor_v_in**2)*vetor_v_in
                        proj_of_u_out_on_v_out = (np.dot(vetor_u_out, vetor_v_out)/modulo_vetor_v_out**2)*vetor_v_out
                        
                        lat_traves_ida = lat_portao_entrada_faixa + proj_of_u_in_on_v_in[1]
                        long_traves_ida = long_portao_entrada_faixa + proj_of_u_in_on_v_in[0]
                        
                        lat_traves_volta = lat_limite_saida + proj_of_u_out_on_v_out[1]
                        long_traves_volta = long_limite_saida + proj_of_u_out_on_v_out[0]
                        
                        # criação dos 2 vertices de través 
                        
                        vertices2_df = vertices2_df.reset_index()
                                                
                        indice_vertice_1 = -random.random()
                        vertices2_df.at[indice_vertice_1, 'PONTO'] = f'TRV_IN_{indice_vertice_1:.3f}'
                        vertices2_df.at[indice_vertice_1, 'LAT'] = lat_traves_ida
                        vertices2_df.at[indice_vertice_1, 'LONG'] = long_traves_ida
                        
                        indice_vertice_2 = -random.random()
                        vertices2_df.at[indice_vertice_2, 'PONTO'] = f'TRV_OUT_{indice_vertice_2:.3f}'
                        vertices2_df.at[indice_vertice_2, 'LAT'] = lat_traves_volta
                        vertices2_df.at[indice_vertice_2, 'LONG'] = long_traves_volta
                     
                        # cria aresta portão de entrada para o través entrada    
                        indice_aresta_7 = -random.random()
                        arestas_df.at[indice_aresta_7, 'ORIGEM'] = portao_entrada_faixa
                        arestas_df.at[indice_aresta_7, 'DESTINO'] = f'TRV_IN_{indice_vertice_1:.3f}'
                        arestas_df.at[indice_aresta_7, 'DISTANCIA'] = distancia_geodesica(lat_portao_entrada_faixa, long_portao_entrada_faixa, lat_traves_ida, long_traves_ida)
                        
                        # cria aresta traves entrada para a plataforma1    
                        indice_aresta_8 = -random.random()
                        arestas_df.at[indice_aresta_8, 'ORIGEM'] = f'TRV_IN_{indice_vertice_1:.3f}'
                        arestas_df.at[indice_aresta_8, 'DESTINO'] = destino1
                        arestas_df.at[indice_aresta_8, 'DISTANCIA'] = distancia_geodesica(lat_traves_ida, long_traves_ida, lat_destino1, long_destino1)
                        
                        # cria aresta plataforma para o traves de saida    
                        indice_aresta_9 = -random.random()
                        arestas_df.at[indice_aresta_9, 'ORIGEM'] = destino1
                        arestas_df.at[indice_aresta_9, 'DESTINO'] = f'TRV_OUT_{indice_vertice_2:.3f}'
                        arestas_df.at[indice_aresta_9, 'DISTANCIA'] = distancia_geodesica(lat_destino1, long_destino1, lat_traves_volta, long_traves_volta)
                        
                        # cria aresta traves de saida para portão de saida 
                        indice_aresta_10 = -random.random()
                        arestas_df.at[indice_aresta_10, 'ORIGEM'] = f'TRV_OUT_{indice_vertice_2:.3f}'
                        arestas_df.at[indice_aresta_10, 'DESTINO'] = portao_saida_faixa
                        arestas_df.at[indice_aresta_10, 'DISTANCIA'] = distancia_geodesica(lat_traves_volta, long_traves_volta, lat_portao_saida_faixa, long_portao_saida_faixa)                        
                        
                        
       
    ########################################################### 			
    
    # conferencia do último (quarto) destino
    
    lat_portao_entrada_quadricula = 0
    long_portao_entrada_quadricula = 0
    tamanho_aresta_ida = 0
    tamanho_aresta_volta = 0
    contador = 0
    
    if coord_destino4.within(poligono_coords_BS) == True: #verifica se o destino4 está dentro da poligonal da BS
        for i in lista_quadrantes:
            if i[1].contains(coord_destino4) == True: #verifica se está dentro dos quadrantes
                contador = contador + 1
                quadrante_destino4 = i[0]
                for j in portoes_quadriculas_df.index:
                    if portoes_quadriculas_df.loc[j]['QUADRICULA'] == quadrante_destino4:
                        portao_entrada_quadricula = portoes_quadriculas_df.loc[j]['ENTRADA']
                        portao_saida_quadricula = portoes_quadriculas_df.loc[j]['SAIDA']
                       
                        for k in vertices2_df.index:
                            if vertices2_df.loc[k]['PONTO'] == portao_entrada_quadricula:
                                lat_portao_entrada_quadricula = vertices2_df.loc[k]['LAT']
                                long_portao_entrada_quadricula = vertices2_df.loc[k]['LONG']
                                tamanho_aresta_ida = coord_destino4.distance(Point(lat_portao_entrada_quadricula, long_portao_entrada_quadricula)) * 60
                                indice_aresta_11 = -random.random()
                                arestas_df.at[indice_aresta_11, 'ORIGEM'] = portao_entrada_quadricula
                                arestas_df.at[indice_aresta_11, 'DESTINO'] = destino4
                                arestas_df.at[indice_aresta_11, 'DISTANCIA'] = tamanho_aresta_ida                        
                                                                                          
                           
                            if vertices2_df.loc[k]['PONTO'] == portao_saida_quadricula:
                                lat_portao_saida_quadricula = vertices2_df.loc[k]['LAT']
                                long_portao_saida_quadricula = vertices2_df.loc[k]['LONG']    
                                tamanho_aresta_volta = coord_destino4.distance(Point(lat_portao_saida_quadricula, long_portao_saida_quadricula)) * 60
                                indice_aresta_12 = -random.random()
                                arestas_df.at[indice_aresta_12, 'ORIGEM'] = destino4
                                arestas_df.at[indice_aresta_12, 'DESTINO'] = portao_saida_quadricula
                                arestas_df.at[indice_aresta_12, 'DISTANCIA'] = tamanho_aresta_volta
        
        if contador == 0: # para o caso de estar dentro da poligonal da BS, porém fora das quadrículas

            waypoint_entrada = ''
            waypoint_saida = ''
            distancia_waypoint_entrada = 99999999
            distancia_waypoint_saida = 99999999
            
            for m in vertices_df.index:
                if (vertices_df['SENTIDO'][m] == 'IN' or vertices_df['SENTIDO'][m] == 'IN_OUT') and vertices_df['LAT'][m] > lat_destino4:
                    lat_waypoint_entrada = vertices_df.loc[m]['LAT']
                    long_waypoint_entrada = vertices_df.loc[m]['LONG']
                    distancia_waypont_entrada_prov = coord_destino4.distance(Point(lat_waypoint_entrada, long_waypoint_entrada)) * 60
                    if distancia_waypont_entrada_prov < distancia_waypoint_entrada:
                        distancia_waypoint_entrada = distancia_waypont_entrada_prov
                        waypoint_entrada = vertices_df['PONTO'][m]
                    
                if (vertices_df['SENTIDO'][m] == 'OUT' or vertices_df['SENTIDO'][m] == 'IN_OUT') and vertices_df['LAT'][m] > lat_destino4:
                    lat_waypoint_saida = vertices_df.loc[m]['LAT']
                    long_waypoint_saida = vertices_df.loc[m]['LONG']
                    distancia_waypont_saida_prov = coord_destino4.distance(Point(lat_waypoint_saida, long_waypoint_saida)) * 60
                    if distancia_waypont_saida_prov < distancia_waypoint_saida:
                        distancia_waypoint_saida = distancia_waypont_saida_prov
                        waypoint_saida = vertices_df['PONTO'][m]                    
            
            # cria a aresta do waypoint de entrada para a plataforma    
            indice_aresta_13 = -random.random()
            arestas_df.at[indice_aresta_13, 'ORIGEM'] = waypoint_entrada
            arestas_df.at[indice_aresta_13, 'DESTINO'] = destino4
            arestas_df.at[indice_aresta_13, 'DISTANCIA'] = distancia_waypoint_entrada                
                    
            # cria a aresta da plataforma para o waypoint de saída   
            indice_aresta_14 = -random.random()
            arestas_df.at[indice_aresta_14, 'ORIGEM'] = destino4
            arestas_df.at[indice_aresta_14, 'DESTINO'] = waypoint_saida
            arestas_df.at[indice_aresta_14, 'DISTANCIA'] = distancia_waypoint_saida             
                        
                              
    # CASO A 4ª PLATAFORMA ESTEJA FORA DA ÁREA DO ESPAÇO AÉREO DA BS e BC        
            
    if coord_destino4.within(poligono_coords_BS) == False and coord_destino4.within(poligono_coords_BC) == False: #verifica se está fora da poligonal da BS e BC
        indice_aresta_15 = -random.random()
        arestas_df.at[indice_aresta_15, 'ORIGEM'] = origem
        arestas_df.at[indice_aresta_15, 'DESTINO'] = destino4
        arestas_df.at[indice_aresta_15, 'DISTANCIA'] = distancia_geodesica(lat_origem, long_origem, lat_destino4, long_destino4)                    
        indice_aresta_16 = -random.random()
        arestas_df.at[indice_aresta_16, 'ORIGEM'] = destino4
        arestas_df.at[indice_aresta_16, 'DESTINO'] = pouso_final
        arestas_df.at[indice_aresta_16, 'DISTANCIA'] = distancia_geodesica(lat_destino4, long_destino4, lat_pouso_final, long_pouso_final)  
    

    # CASO PLATAFORMA 4 ESTEJA DENTRO DA ÁREA DO ESPAÇO AÉREO DA BC 

    portao_entrada_faixa = ''
    portao_saida_faixa = ''
    vetor_u_in = np.array([0, 0]) # vetor que liga o portão de entrada da faixa a plataforma
    vetor_u_out = np.array([0, 0]) # vetor que liga o extremo da saida da faixa a platarforma
    vetor_v_in = np.array([0, 0]) # vetor que liga o portão de entrada da faixa ao limite do segmento de reta da entrada
    vetor_v_out = np.array([0, 0]) # vetor que liga o limite extremo da faixa sentido saida para portão de saida da faixa
    modulo_vetor_v_in = 0
    modulo_vetor_v_out = 0
    proj_of_u_in_on_v_in = np.array([0, 0])
    proj_of_u_out_on_v_out = np.array([0, 0])

    
    if coord_destino4.within(poligono_coords_BC) == True: # verifica se está dentro da poligonal BC   
        for faixa4 in lista_faixasBC:
            if faixa4[1].contains(coord_destino4) == True: # verifica se está dentro das faixas
                faixa_destino4 = faixa4[0]
                for kk in portoes_faixas_bc_df.index:
                    if portoes_faixas_bc_df.loc[kk]['faixa'] == faixa_destino4:
                        
                        portao_entrada_faixa = portoes_faixas_bc_df.loc[kk]['point_in']
                        portao_saida_faixa = portoes_faixas_bc_df.loc[kk]['point_out']
                        lat_portao_entrada_faixa = portoes_faixas_bc_df.loc[kk]['lat_point_in']
                        long_portao_entrada_faixa = portoes_faixas_bc_df.loc[kk]['long_point_in']
                        lat_portao_saida_faixa = portoes_faixas_bc_df.loc[kk]['lat_point_out']
                        long_portao_saida_faixa = portoes_faixas_bc_df.loc[kk]['long_point_out']
                        lat_limite_entrada = portoes_faixas_bc_df.loc[kk]['lat_point_limit_in']
                        long_limite_entrada = portoes_faixas_bc_df.loc[kk]['long_point_limit_in']
                        lat_limite_saida = portoes_faixas_bc_df.loc[kk]['lat_point_limit_out']
                        long_limite_saida = portoes_faixas_bc_df.loc[kk]['long_point_limit_out']
                        
                        vetor_u_in = np.array([long_destino4 - long_portao_entrada_faixa, lat_destino4 - lat_portao_entrada_faixa])
                        vetor_u_out = np.array([long_destino4 - long_limite_saida, lat_destino4 - lat_limite_saida])
                        
                        vetor_v_in = np.array([long_limite_entrada - long_portao_entrada_faixa, lat_limite_entrada - lat_portao_entrada_faixa])
                        vetor_v_out = np.array([long_portao_saida_faixa - long_limite_saida, lat_portao_saida_faixa - lat_limite_saida])
                        
                        modulo_vetor_v_in = np.sqrt(sum(vetor_v_in**2))
                        modulo_vetor_v_out = np.sqrt(sum(vetor_v_out**2))
                        
                        proj_of_u_in_on_v_in = (np.dot(vetor_u_in, vetor_v_in)/modulo_vetor_v_in**2)*vetor_v_in
                        proj_of_u_out_on_v_out = (np.dot(vetor_u_out, vetor_v_out)/modulo_vetor_v_out**2)*vetor_v_out
                        
                        lat_traves_ida = lat_portao_entrada_faixa + proj_of_u_in_on_v_in[1]
                        long_traves_ida = long_portao_entrada_faixa + proj_of_u_in_on_v_in[0]
                        
                        lat_traves_volta = lat_limite_saida + proj_of_u_out_on_v_out[1]
                        long_traves_volta = long_limite_saida + proj_of_u_out_on_v_out[0]
                        
                        # criação dos 2 vertices de través
                        
                        vertices2_df = vertices2_df.reset_index()
                        
                        indice_vertice_3 = -random.random()
                        vertices2_df.at[indice_vertice_3, 'PONTO'] = f'TRV_IN_{indice_vertice_3:.3f}'
                        vertices2_df.at[indice_vertice_3, 'LAT'] = lat_traves_ida
                        vertices2_df.at[indice_vertice_3, 'LONG'] = long_traves_ida                        

                        indice_vertice_4  = -random.random()
                        vertices2_df.at[indice_vertice_4, 'PONTO'] = f'TRV_OUT_{indice_vertice_4:.3f}'
                        vertices2_df.at[indice_vertice_4, 'LAT'] = lat_traves_volta
                        vertices2_df.at[indice_vertice_4, 'LONG'] = long_traves_volta
                     
                        # cria aresta portão de entrada para o través entrada    
                        indice_aresta_17 = -random.random()
                        arestas_df.at[indice_aresta_17, 'ORIGEM'] = portao_entrada_faixa
                        arestas_df.at[indice_aresta_17, 'DESTINO'] = f'TRV_IN_{indice_vertice_3:.3f}'
                        arestas_df.at[indice_aresta_17, 'DISTANCIA'] = distancia_geodesica(lat_portao_entrada_faixa, long_portao_entrada_faixa, lat_traves_ida, long_traves_ida)
                        
                        # cria aresta traves entrada para a plataforma4   
                        indice_aresta_18 = -random.random()
                        arestas_df.at[indice_aresta_18, 'ORIGEM'] = f'TRV_IN_{indice_vertice_3:.3f}'
                        arestas_df.at[indice_aresta_18, 'DESTINO'] = destino4
                        arestas_df.at[indice_aresta_18, 'DISTANCIA'] = distancia_geodesica(lat_traves_ida, long_traves_ida, lat_destino4, long_destino4)
                        
                        # cria aresta plataforma4 para o traves de saida    
                        indice_aresta_19 = -random.random()
                        arestas_df.at[indice_aresta_19, 'ORIGEM'] = destino4
                        arestas_df.at[indice_aresta_19, 'DESTINO'] = f'TRV_OUT_{indice_vertice_4:.3f}'
                        arestas_df.at[indice_aresta_19, 'DISTANCIA'] = distancia_geodesica(lat_destino4, long_destino4, lat_traves_volta, long_traves_volta)
                        
                        # cria aresta traves de saida para portão de saida 
                        indice_aresta_20 = -random.random()
                        arestas_df.at[indice_aresta_20, 'ORIGEM'] = f'TRV_OUT_{indice_vertice_4:.3f}'
                        arestas_df.at[indice_aresta_20, 'DESTINO'] = portao_saida_faixa
                        arestas_df.at[indice_aresta_20, 'DISTANCIA'] = distancia_geodesica(lat_traves_volta, long_traves_volta, lat_portao_saida_faixa, long_portao_saida_faixa)                        
                        
                        
   
    ########################################################### 
    # incluir as arestas entre plataformas
    indice_aresta_21 = -random.random()
    arestas_df.at[indice_aresta_21, 'ORIGEM'] = destino1
    arestas_df.at[indice_aresta_21, 'DESTINO'] = destino2
    arestas_df.at[indice_aresta_21, 'DISTANCIA'] = distancia_geodesica(lat_destino1, long_destino1, lat_destino2, long_destino2)                    
    
    indice_aresta_22 = -random.random()
    arestas_df.at[indice_aresta_22, 'ORIGEM'] = destino2
    arestas_df.at[indice_aresta_22, 'DESTINO'] = destino3
    arestas_df.at[indice_aresta_22, 'DISTANCIA'] = distancia_geodesica(lat_destino2, long_destino2, lat_destino3, long_destino3)                    
    
    indice_aresta_23 = -random.random()
    arestas_df.at[indice_aresta_23, 'ORIGEM'] = destino3
    arestas_df.at[indice_aresta_23, 'DESTINO'] = destino4
    arestas_df.at[indice_aresta_23, 'DISTANCIA'] = distancia_geodesica(lat_destino3, long_destino3, lat_destino4, long_destino4)                    
    
    
    ########################################################### 
    #MODELAGEM DO ESPAÇO AÉREO COMO GRAFO
    
    G = nx.from_pandas_edgelist(arestas_df, source='ORIGEM', target='DESTINO', edge_attr='DISTANCIA', create_using=nx.DiGraph())
    
    #POSIÇÃO DOS NÓS NAS COORDENADAS
    for i in vertices2_df.index:
        G.add_node(vertices2_df['PONTO'][i], pos = (vertices2_df['LONG'][i] , vertices2_df['LAT'][i]))
    
    
    ########################################################### 
    #DADOS PARA CÁLCULO DE DISPONÍVEL, TEMPO E VOO E CONSUMO DE QAV
        
    peso_pax = 107 # em kg
    
    PMD_GP = 26500 # em lb considerado S92
    PMD_SMP = 7800 # em kg considerado H175
    PMD_MP = 7000 # em kg considerado AW139
    
    PBO_GP = 18115 # em lb considerado S92
    PBO_SMP = 4949 # em kg considerado H175 4976
    PBO_MP = 4680 # em kg considerado AW139
    
    CONSUMO_VOO_GP = 1350 # em lb/h
    CONSUMO_VOO_SMP = 490 # em kg/h 420
    CONSUMO_VOO_MP = 400 # em kg/h
    
    CONSUMO_SOLO_GP = 675 # em lb/h
    CONSUMO_SOLO_SMP = 270 # 220 em kg/h
    CONSUMO_SOLO_MP = 320 # em kg/h
    
    TEMPO_ACIO_DECOL_GP = 10 # em min 11
    TEMPO_ACIO_DECOL_SMP = 10 # em min 11 min
    TEMPO_ACIO_DECOL_MP = 10 # em min 11
    
    TEMPO_POUSADOPLATAFORMA_GP = 10 * num_pousos # em min
    TEMPO_POUSADOPLATAFORMA_SMP = 10 * num_pousos # em min
    TEMPO_POUSADOPLATAFORMA_MP = 8 * num_pousos # em min
    
    TEMPO_POUSOCORTE_GP = 5 # em min 6
    TEMPO_POUSOCORTE_SMP = 5 # em min 6
    TEMPO_POUSOCORTE_MP = 5 # em min 6
    
    TEMPO_CIRCUITO_GP = 4 * num_pousos # em min
    TEMPO_CIRCUITO_SMP = 4 * num_pousos # em min
    TEMPO_CIRCUITO_MP = 4 * num_pousos # em min
    
    TETO_CRUZEIRO_GP = 3000 # em pés
    TETO_CRUZEIRO_SMP = 3000 # em pés
    TETO_CRUZEIRO_MP = 3000 # em pés
    
    RAZAO_SUBIDA_GP = 800 # em pés/min
    RAZAO_SUBIDA_SMP = 800 # em pés/min
    RAZAO_SUBIDA_MP = 800 # em pés/min
    
    RAZAO_DESCIDA_GP = 500 # em pés/min
    RAZAO_DESCIDA_SMP = 500 # em pés/min
    RAZAO_DESCIDA_MP = 500 # em pés/min
    
    VELOCIDADE_CRUZEIRO_GP = 145 # em nós 145
    VELOCIDADE_CRUZEIRO_SMP = 145 # em nós 145
    VELOCIDADE_CRUZEIRO_MP = 155 # em nós 155
    
    
    ###########################################################  
    
    caminho_ida = nx.shortest_path(G, source = origem, target = destino1, weight='DISTANCIA', method='dijkstra')
    
    caminho_intermediario1 = nx.shortest_path(G, source = destino1, target = destino2, weight='DISTANCIA', method='dijkstra')
    
    caminho_intermediario2 = nx.shortest_path(G, source = destino2, target = destino3, weight='DISTANCIA', method='dijkstra')
    
    caminho_intermediario3 = nx.shortest_path(G, source = destino3, target = destino4, weight='DISTANCIA', method='dijkstra')
    
    caminho_volta = nx.shortest_path(G, source = destino4, target = pouso_final, weight='DISTANCIA', method='dijkstra')
    
    ########################################################### 
    
    def custo_caminho(G, weights_edges, caminho):
        custo_caminho = 0
        pares_ordenados_caminho = []
        for i in range(len(caminho)-1):
            pares_ordenados_caminho.append((caminho[i],caminho[i+1]))
            custo_caminho = custo_caminho + G[pares_ordenados_caminho[-1][0]][pares_ordenados_caminho[-1][1]][str(weights_edges)]
        retorna = [custo_caminho , pares_ordenados_caminho]
        return retorna  
    
    roteiro_ida = []
    valor_roteiro_ida = 0
    subgrafo_ida = nx.DiGraph()
    for i in range(len(caminho_ida) - 1):
        roteiro_ida.append((caminho_ida[i] , caminho_ida[i+1]))
        valor_roteiro_ida = valor_roteiro_ida + G[roteiro_ida[-1][0]][roteiro_ida[-1][1]]['DISTANCIA']
        subgrafo_ida.add_edge(caminho_ida[i] , caminho_ida[i+1])
    
    roteiro_intermediario1 = []
    valor_roteiro_intermediario1 = 0
    subgrafo_intermediario1 = nx.DiGraph()
    for i in range(len(caminho_intermediario1) - 1):
        roteiro_intermediario1.append((caminho_intermediario1[i] , caminho_intermediario1[i+1]))
        valor_roteiro_intermediario1 = valor_roteiro_intermediario1 + G[roteiro_intermediario1[-1][0]][roteiro_intermediario1[-1][1]]['DISTANCIA']
        subgrafo_intermediario1.add_edge(caminho_intermediario1[i] , caminho_intermediario1[i+1])
    
    roteiro_intermediario2 = []
    valor_roteiro_intermediario2 = 0
    subgrafo_intermediario2 = nx.DiGraph()
    for i in range(len(caminho_intermediario2) - 1):
        roteiro_intermediario2.append((caminho_intermediario2[i] , caminho_intermediario2[i+1]))
        valor_roteiro_intermediario2 = valor_roteiro_intermediario2 + G[roteiro_intermediario2[-1][0]][roteiro_intermediario2[-1][1]]['DISTANCIA']
        subgrafo_intermediario2.add_edge(caminho_intermediario2[i] , caminho_intermediario2[i+1])
    
    roteiro_intermediario3 = []
    valor_roteiro_intermediario3 = 0
    subgrafo_intermediario3 = nx.DiGraph()
    for i in range(len(caminho_intermediario3) - 1):
        roteiro_intermediario3.append((caminho_intermediario3[i] , caminho_intermediario3[i+1]))
        valor_roteiro_intermediario3 = valor_roteiro_intermediario3 + G[roteiro_intermediario3[-1][0]][roteiro_intermediario3[-1][1]]['DISTANCIA']
        subgrafo_intermediario3.add_edge(caminho_intermediario3[i] , caminho_intermediario3[i+1])
    
    roteiro_volta = []
    valor_roteiro_volta = 0
    subgrafo_volta = nx.DiGraph()
    for i in range(len(caminho_volta) - 1):
        roteiro_volta.append((caminho_volta[i] , caminho_volta[i+1]))
        valor_roteiro_volta = valor_roteiro_volta + G[roteiro_volta[-1][0]][roteiro_volta[-1][1]]['DISTANCIA']
        subgrafo_volta.add_edge(caminho_volta[i] , caminho_volta[i+1])
    
    
    valor_roteiro_total = valor_roteiro_ida + valor_roteiro_intermediario1 + valor_roteiro_intermediario2 + valor_roteiro_intermediario3 + valor_roteiro_volta
    valor_medio_roteiro_total = 0.5 * valor_roteiro_total
    
    print('-='*30)
    print(f'{destino1} => {destino2} => {destino3} => {destino4}')    
    print(f'Distancia do caminho completo = {valor_roteiro_total:.2f} mn')

    
    #####################################################
    # MAPA FOLIUM
    
    vertices2_df = vertices2_df.set_index('PONTO')
    
    mapa = folium.Map(location=[-24.010991, -43.087035], zoom_start=8)
    
    
    for vertice in vertices2_df.index:
        folium.CircleMarker([vertices2_df.loc[vertice]['LAT'], vertices2_df.loc[vertice]['LONG']], radius=0.5, popup=vertice, tooltip=vertice, color="#848c82", fill=False, fill_color="#848c82").add_to(mapa)
    
    lista_polyline_ida = []
    lista_polyline_intermediario1 = []
    lista_polyline_intermediario2 = []
    lista_polyline_intermediario3 = []
    lista_polyline_volta = []
    
    for vertice in caminho_ida:
        lista_polyline_ida.append([vertices2_df.loc[vertice]['LAT'], vertices2_df.loc[vertice]['LONG']])
    
    for vertice in caminho_intermediario1:
        lista_polyline_intermediario1.append([vertices2_df.loc[vertice]['LAT'], vertices2_df.loc[vertice]['LONG']])
        
    for vertice in caminho_intermediario2:
        lista_polyline_intermediario2.append([vertices2_df.loc[vertice]['LAT'], vertices2_df.loc[vertice]['LONG']])
    
    for vertice in caminho_intermediario3:
        lista_polyline_intermediario3.append([vertices2_df.loc[vertice]['LAT'], vertices2_df.loc[vertice]['LONG']])    
        
    for vertice in caminho_volta:
        lista_polyline_volta.append([vertices2_df.loc[vertice]['LAT'], vertices2_df.loc[vertice]['LONG']])
    
    
    for vertice in caminho_ida:
        folium.CircleMarker([vertices2_df.loc[vertice]['LAT'], vertices2_df.loc[vertice]['LONG']], radius=2, popup=vertice, tooltip=vertice, color="#000000", fill=True, fill_color="#000000").add_to(mapa)
    
    for vertice in caminho_intermediario1:
        folium.CircleMarker([vertices2_df.loc[vertice]['LAT'], vertices2_df.loc[vertice]['LONG']], radius=2, popup=vertice, tooltip=vertice, color="#000000", fill=True, fill_color="#000000").add_to(mapa)
    
    for vertice in caminho_intermediario2:
        folium.CircleMarker([vertices2_df.loc[vertice]['LAT'], vertices2_df.loc[vertice]['LONG']], radius=2, popup=vertice, tooltip=vertice, color="#000000", fill=True, fill_color="#000000").add_to(mapa)
        
    for vertice in caminho_intermediario3:
        folium.CircleMarker([vertices2_df.loc[vertice]['LAT'], vertices2_df.loc[vertice]['LONG']], radius=2, popup=vertice, tooltip=vertice, color="#000000", fill=True, fill_color="#000000").add_to(mapa)    
    
    for vertice in caminho_volta:
        folium.CircleMarker([vertices2_df.loc[vertice]['LAT'], vertices2_df.loc[vertice]['LONG']], radius=2, popup=vertice, tooltip=vertice, color="#000000", fill=True, fill_color="#000000").add_to(mapa)
        
    folium.vector_layers.PolyLine(lista_polyline_ida, popup=None, tooltip=None, color="#ff0400").add_to(mapa)
    
    folium.vector_layers.PolyLine(lista_polyline_intermediario1, popup=None, tooltip=None, color="#00ff44").add_to(mapa)
    
    folium.vector_layers.PolyLine(lista_polyline_intermediario2, popup=None, tooltip=None, color="#00ff44").add_to(mapa)
    
    folium.vector_layers.PolyLine(lista_polyline_intermediario3, popup=None, tooltip=None, color="#00ff44").add_to(mapa)
        
    folium.vector_layers.PolyLine(lista_polyline_volta, popup=None, tooltip=None, color="#1100ff").add_to(mapa)    
    
    mapa.add_child(folium.LatLngPopup())
        
    mapa.save(f"Roteiro {origem} - {destino1} - {destino2} - {destino3} - {destino4} - {pouso_final}_{data_hora}.html")
    
    #####################################################
    #CÁLCULO DA QUANTIDADE DE PAX NO EMBARQUE
    
    TEMPO_SOLO_GP = (TEMPO_ACIO_DECOL_GP + TEMPO_POUSADOPLATAFORMA_GP + TEMPO_POUSOCORTE_GP) / 60
    TEMPO_SOLO_SMP = (TEMPO_ACIO_DECOL_SMP + TEMPO_POUSADOPLATAFORMA_SMP + TEMPO_POUSOCORTE_SMP) / 60
    TEMPO_SOLO_MP = (TEMPO_ACIO_DECOL_MP + TEMPO_POUSADOPLATAFORMA_MP + TEMPO_POUSOCORTE_MP) / 60
    
    TEMPO_SUBIDA_GP = (TETO_CRUZEIRO_GP / RAZAO_SUBIDA_GP) / 60
    TEMPO_SUBIDA_SMP = (TETO_CRUZEIRO_SMP / RAZAO_SUBIDA_SMP) / 60
    TEMPO_SUBIDA_MP = (TETO_CRUZEIRO_MP / RAZAO_SUBIDA_MP) / 60
    
    TEMPO_DESCIDA_GP = (TETO_CRUZEIRO_GP / RAZAO_DESCIDA_GP) / 60
    TEMPO_DESCIDA_SMP = (TETO_CRUZEIRO_SMP / RAZAO_DESCIDA_SMP) / 60
    TEMPO_DESCIDA_MP = (TETO_CRUZEIRO_MP / RAZAO_DESCIDA_MP) / 60
    
    ACELERACAO_SUBIDA_GP = VELOCIDADE_CRUZEIRO_GP / TEMPO_SUBIDA_GP
    ACELERACAO_SUBIDA_SMP = VELOCIDADE_CRUZEIRO_SMP / TEMPO_SUBIDA_SMP
    ACELERACAO_SUBIDA_MP = VELOCIDADE_CRUZEIRO_MP / TEMPO_SUBIDA_MP
    
    ACELERACAO_DESCIDA_GP = - (VELOCIDADE_CRUZEIRO_GP / TEMPO_DESCIDA_GP)
    ACELERACAO_DESCIDA_SMP = - (VELOCIDADE_CRUZEIRO_SMP / TEMPO_DESCIDA_SMP)
    ACELERACAO_DESCIDA_MP = - (VELOCIDADE_CRUZEIRO_MP / TEMPO_DESCIDA_MP)
    
    DISTANCIA_SUBIDA_GP = ACELERACAO_SUBIDA_GP * (TEMPO_SUBIDA_GP ** 2 / 2)
    DISTANCIA_SUBIDA_SMP = ACELERACAO_SUBIDA_SMP * (TEMPO_SUBIDA_SMP ** 2 / 2)
    DISTANCIA_SUBIDA_MP = ACELERACAO_SUBIDA_MP * (TEMPO_SUBIDA_MP ** 2 / 2)
    
    DISTANCIA_DESCIDA_GP = - ACELERACAO_DESCIDA_GP * (TEMPO_DESCIDA_GP ** 2 / 2)
    DISTANCIA_DESCIDA_SMP = - ACELERACAO_DESCIDA_SMP * (TEMPO_DESCIDA_SMP ** 2 / 2)
    DISTANCIA_DESCIDA_MP = - ACELERACAO_DESCIDA_MP * (TEMPO_DESCIDA_MP ** 2 / 2)
    
    DISTANCIA_CRUZEIRO_GP = valor_medio_roteiro_total - DISTANCIA_SUBIDA_GP - DISTANCIA_DESCIDA_GP
    DISTANCIA_CRUZEIRO_SMP = valor_medio_roteiro_total - DISTANCIA_SUBIDA_SMP - DISTANCIA_DESCIDA_SMP
    DISTANCIA_CRUZEIRO_MP = valor_medio_roteiro_total - DISTANCIA_SUBIDA_MP - DISTANCIA_DESCIDA_MP
    
    TEMPO_CRUZEIRO_GP = DISTANCIA_CRUZEIRO_GP / VELOCIDADE_CRUZEIRO_GP
    TEMPO_CRUZEIRO_SMP = DISTANCIA_CRUZEIRO_SMP / VELOCIDADE_CRUZEIRO_SMP
    TEMPO_CRUZEIRO_MP = DISTANCIA_CRUZEIRO_MP / VELOCIDADE_CRUZEIRO_MP
    
    TEMPO_IDA_GP = TEMPO_SUBIDA_GP + TEMPO_DESCIDA_GP + TEMPO_CRUZEIRO_GP
    TEMPO_IDA_SMP = TEMPO_SUBIDA_SMP + TEMPO_DESCIDA_SMP + TEMPO_CRUZEIRO_SMP
    TEMPO_IDA_MP = TEMPO_SUBIDA_MP + TEMPO_DESCIDA_MP + TEMPO_CRUZEIRO_MP
    
    TEMPO_VOLTA_GP = TEMPO_IDA_GP
    TEMPO_VOLTA_SMP = TEMPO_IDA_SMP
    TEMPO_VOLTA_MP = TEMPO_IDA_MP
    
    TEMPO_VOO_GP = TEMPO_IDA_GP + TEMPO_VOLTA_GP + TEMPO_CIRCUITO_GP / 60
    TEMPO_VOO_SMP = TEMPO_IDA_SMP + TEMPO_VOLTA_SMP + TEMPO_CIRCUITO_SMP / 60
    TEMPO_VOO_MP = TEMPO_IDA_MP + TEMPO_VOLTA_MP + TEMPO_CIRCUITO_MP / 60
    
    COMB_MISSAO_GP = TEMPO_VOO_GP * CONSUMO_VOO_GP + TEMPO_SOLO_GP * CONSUMO_SOLO_GP
    COMB_MISSAO_SMP = TEMPO_VOO_SMP * CONSUMO_VOO_SMP + TEMPO_SOLO_SMP * CONSUMO_SOLO_SMP
    COMB_MISSAO_MP = TEMPO_VOO_MP * CONSUMO_VOO_MP + TEMPO_SOLO_MP * CONSUMO_SOLO_MP
    
    TEMPO_MISSAO_GP = TEMPO_VOO_GP + TEMPO_SOLO_GP
    TEMPO_MISSAO_SMP = TEMPO_VOO_SMP + TEMPO_SOLO_SMP
    TEMPO_MISSAO_MP = TEMPO_VOO_MP + TEMPO_SOLO_MP
    
    COMB_RESERVA_GP = (max(0.5, 1/3 + 0.1 * TEMPO_MISSAO_GP)) * CONSUMO_VOO_GP
    COMB_RESERVA_SMP = (max(0.5, 1/3 + 0.1 * TEMPO_MISSAO_SMP)) * CONSUMO_VOO_SMP
    COMB_RESERVA_MP = (max(0.5, 1/3 + 0.1 * TEMPO_MISSAO_MP)) * CONSUMO_VOO_MP
    
    COMBUSTIVEL_GP = COMB_MISSAO_GP + COMB_RESERVA_GP
    COMBUSTIVEL_SMP = COMB_MISSAO_SMP + COMB_RESERVA_SMP
    COMBUSTIVEL_MP = COMB_MISSAO_MP + COMB_RESERVA_MP
    
    PAYLOAD_GP = PMD_GP - PBO_GP - COMBUSTIVEL_GP
    PAYLOAD_SMP = PMD_SMP - PBO_SMP - COMBUSTIVEL_SMP
    PAYLOAD_MP = PMD_MP - PBO_MP - COMBUSTIVEL_MP
    
    QUANT_PAX_GP = min(18, PAYLOAD_GP / (2.20462 * peso_pax)) # passar de lb para kg
    QUANT_PAX_SMP = min(16, PAYLOAD_SMP / peso_pax)
    QUANT_PAX_MP = min(12, PAYLOAD_MP / peso_pax)
    
    
    ########################################################### 
    #API REDEMET
    
    hora_zulu = str(int(data_hora[11:13])+3)
    data_resumida = data_hora[:4] + data_hora[5:7] + data_hora[8:10] + hora_zulu
    chave_api = 'coloca a chave api redemet aqui'
    # 
    informacao_origem = requests.get(f"https://api-redemet.decea.mil.br/aerodromos/info?api_key={chave_api}&localidade={origem}&datahora={data_resumida}")
     
    informacao_origem = informacao_origem.json()
    informacao_origem_metar = informacao_origem['data']['metar']
    informacao_origem_teto = informacao_origem['data']['teto']
    informacao_origem_visibilidade = informacao_origem['data']['visibilidade']
    informacao_origem_ceu = informacao_origem['data']['ceu']
    informacao_origem_condicoes_tempo = informacao_origem['data']['condicoes_tempo']

    informacao_pouso_final = requests.get(f"https://api-redemet.decea.mil.br/aerodromos/info?api_key={chave_api}&localidade={pouso_final}&datahora={data_resumida}")
     
    informacao_pouso_final = informacao_pouso_final.json()
    informacao_pouso_final_metar = informacao_pouso_final['data']['metar']
    informacao_pouso_final_teto = informacao_pouso_final['data']['teto']
    informacao_pouso_final_visibilidade = informacao_pouso_final['data']['visibilidade']
    informacao_pouso_final_ceu = informacao_pouso_final['data']['ceu']
    informacao_pouso_final_condicoes_tempo = informacao_pouso_final['data']['condicoes_tempo']

     
    status = requests.get(f"https://api-redemet.decea.mil.br/aerodromos/status?api_key={chave_api}")
    status = status.json()
    status_aeroporto = status['data']
    
    cor_farol_origem = ''
    cor_farol_pouso_final = ''
    
    for i in range(len(status_aeroporto)):
         if status_aeroporto[i][0] == origem:
             cor_farol_origem = status_aeroporto[i][4]
             if cor_farol_origem == 'g':
                 cor_farol_origem = (emoji.emojize("VERDE :green_circle:"))
             elif cor_farol_origem == 'y':
                 cor_farol_origem = (emoji.emojize("AMARELA :yellow_circle:"))
             elif cor_farol_origem == 'r':
                 cor_farol_origem = (emoji.emojize("VERMELHA :red_circle:"))
             elif cor_farol_origem == 'gw':
                 cor_farol_origem = (emoji.emojize("VERDE :green_circle:"))
             elif cor_farol_origem == 'yw':
                 cor_farol_origem = (emoji.emojize("AMARELA :yellow_circle:"))
             elif cor_farol_origem == 'rw':
                 cor_farol_origem = (emoji.emojize("VERMELHA :red_circle:"))
         if status_aeroporto[i][0] == pouso_final:
             cor_farol_pouso_final = status_aeroporto[i][4]
             if cor_farol_pouso_final == 'g':
                 cor_farol_pouso_final = (emoji.emojize('VERDE :green_circle:'))
             elif cor_farol_pouso_final == 'y':
                 cor_farol_pouso_final = (emoji.emojize('AMARELA :yellow_circle:'))
             elif cor_farol_pouso_final == 'r':
                 cor_farol_pouso_final = (emoji.emojize('VERMELHA :red_circle:'))
             elif cor_farol_pouso_final == 'gw':
                 cor_farol_pouso_final = (emoji.emojize('VERDE :green_circle:'))
             elif cor_farol_pouso_final == 'yw':
                 cor_farol_pouso_final = (emoji.emojize('AMARELA :yellow_circle:'))
             elif cor_farol_pouso_final == 'rw':
                 cor_farol_pouso_final = (emoji.emojize('VERMELHA :red_circle:'))
       
    
    ########################################################### 
    # draw graph
        
    plt.axes([0.1, 0.1, 0.5, 0.83])
    
    plt.axis("off")
    
    plt.title(f'ROTEIRO: {origem} -> {destino1} -> {destino2} -> {destino3} -> {destino4} -> {pouso_final}', fontsize=5)
    
    
    plt.text(-45, -21.20, f'Distancia total: {valor_roteiro_total:.2f} mn', fontsize=2.5)
    
    plt.text(-45, -21.27, f'Distancia media: {valor_medio_roteiro_total:.2f} mn', fontsize=2.5)
    
    plt.text(-45, -21.37, f'# pax embarque GP: {QUANT_PAX_GP:.1f} pax', fontsize=2.5)
    
    plt.text(-45, -21.44, f'# pax embarque SMP: {QUANT_PAX_SMP:.1f} pax', fontsize=2.5)
    
    plt.text(-45, -21.51, f'# pax embarque MP: {QUANT_PAX_MP:.1f} pax (PMD: {PMD_MP} kg)', fontsize=2.5)
    
    plt.text(-45, -21.61, f'Tempo missão GP: {TEMPO_MISSAO_GP:.2f} h', fontsize=2.5)
    
    plt.text(-45, -21.68, f'Tempo missão SMP: {TEMPO_MISSAO_SMP:.2f} h', fontsize=2.5)
    
    plt.text(-45, -21.75, f'Tempo missão MP: {TEMPO_MISSAO_MP:.2f} h', fontsize=2.5)
    
    plt.text(-45, -21.85, f'{informacao_origem_metar}', fontsize=2.5)
    
    plt.text(-45, -21.92, f'TETO ORIGEM: {informacao_origem_teto}', fontsize=2.5)
    
    plt.text(-45, -21.99, f'VISIBILIDADE ORIGEM: {informacao_origem_visibilidade}', fontsize=2.5)
    
    plt.text(-45, -22.06, f'CEU ORIGEM: {informacao_origem_ceu}', fontsize=2.5)
    
    plt.text(-45, -22.13, f'CONDICOES TEMPO ORIGEM: {informacao_origem_condicoes_tempo}', fontsize=2.5)
    
    plt.text(-45, -22.20, f'BOLINHA REDEMET ORIGEM: {cor_farol_origem}', fontsize=2.5)
    
    plt.text(-45, -22.30, f'{informacao_pouso_final_metar}', fontsize=2.5)
    
    plt.text(-45, -22.37, f'TETO POUSO FINAL: {informacao_pouso_final_teto}', fontsize=2.5)
    
    plt.text(-45, -22.43, f'VISIBILIDADE POUSO FINAL: {informacao_pouso_final_visibilidade}', fontsize=2.5)
    
    plt.text(-45, -22.50, f'CEU POUSO FINAL: {informacao_pouso_final_ceu}', fontsize=2.5)
    
    plt.text(-45, -22.57, f'CONDICOES TEMPO POUSO FINAL: {informacao_pouso_final_condicoes_tempo}', fontsize=2.5)
    
    plt.text(-45, -22.63, f'BOLINHA REDEMET POUSO FINAL: {cor_farol_pouso_final}', fontsize=2.5)    
    
     
    plt.text(-45.2, -26.10, f'Ida: {caminho_ida} -> {valor_roteiro_ida:.2f} mn', fontsize=2.5)
    
    plt.text(-45.2, -26.17, f'Inter1: {caminho_intermediario1} -> {valor_roteiro_intermediario1:.2f} mn', fontsize=2.5)
    
    plt.text(-45.2, -26.24, f'Inter2: {caminho_intermediario2} -> {valor_roteiro_intermediario2:.2f} mn', fontsize=2.5)
    
    plt.text(-45.2, -26.31, f'Inter3: {caminho_intermediario3} -> {valor_roteiro_intermediario3:.2f} mn', fontsize=2.5)
    
    plt.text(-45.2, -26.38, f'Volta: {caminho_volta} -> {valor_roteiro_volta:.2f} mn', fontsize=2.5)   

    plt.text(-45, -26.45, '#### Planejamento deverá ser confirmado com a cia. aérea que utilizará os dados reais da aeronave ####', fontsize=2.5)
    
    plt.text(-45, -26.52, f'IMPRESSO EM: {data_hora}', fontsize=2.5)


    
    nx.draw_networkx_nodes(G,
                           pos = nx.get_node_attributes(G, 'pos'),
                           node_size = 0.01,
                           node_color = 'b',
                           alpha = 0.2,
                           node_shape = 'o')
    
    nx.draw_networkx_edges(G,
                           pos = nx.get_node_attributes(G, 'pos'),
                           edgelist = None,
                           width = 0.01,
                           edge_color = 'k',
                           style = 'solid',
                           alpha = 0.01,
                           edge_cmap = None,
                           edge_vmin = None,
                           edge_vmax = None,
                           ax = None,
                           arrows = False,
                           label = None,
                           arrowsize = 1)
    
    nx.draw_networkx_labels(G,
                            pos = nx.get_node_attributes(G, 'pos'),
                            font_size = 1,
                            alpha = 0.1)
    
    
    nx.draw_networkx_edges(subgrafo_ida,
                           pos = nx.get_node_attributes(G, 'pos'),
                           edgelist = None,
                           width = 0.4,
                           edge_color = 'r',
                           style = 'solid',
                           alpha = 1,
                           edge_cmap = None,
                           edge_vmin = None,
                           edge_vmax = None,
                           ax = None,
                           arrows = False,
                           label = None,
                           arrowsize = 1)
    
    nx.draw_networkx_edges(subgrafo_intermediario1,
                           pos = nx.get_node_attributes(G, 'pos'),
                           edgelist = None,
                           width = 0.4,
                           edge_color = 'g',
                           style = 'solid',
                           alpha = 1,
                           edge_cmap = None,
                           edge_vmin = None,
                           edge_vmax = None,
                           ax = None,
                           arrows = False,
                           label = None,
                           arrowsize = 1)
    
    nx.draw_networkx_edges(subgrafo_intermediario2,
                           pos = nx.get_node_attributes(G, 'pos'),
                           edgelist = None,
                           width = 0.4,
                           edge_color = 'g',
                           style = 'solid',
                           alpha = 1,
                           edge_cmap = None,
                           edge_vmin = None,
                           edge_vmax = None,
                           ax = None,
                           arrows = False,
                           label = None,
                           arrowsize = 1)
    
    nx.draw_networkx_edges(subgrafo_intermediario3,
                           pos = nx.get_node_attributes(G, 'pos'),
                           edgelist = None,
                           width = 0.4,
                           edge_color = 'g',
                           style = 'solid',
                           alpha = 1,
                           edge_cmap = None,
                           edge_vmin = None,
                           edge_vmax = None,
                           ax = None,
                           arrows = False,
                           label = None,
                           arrowsize = 1)
    
    nx.draw_networkx_edges(subgrafo_volta,
                           pos = nx.get_node_attributes(G, 'pos'),
                           edgelist = None,
                           width = 0.4,
                           edge_color = 'b',
                           style = 'solid',
                           alpha = 1,
                           edge_cmap = None,
                           edge_vmin = None,
                           edge_vmax = None,
                           ax = None,
                           arrows = False,
                           label = None,
                           arrowsize = 1)
    
    nx.draw_networkx_labels(subgrafo_ida,
                            pos = nx.get_node_attributes(G, 'pos'),
                            font_size = 2,
                            alpha = 1)
    
    nx.draw_networkx_labels(subgrafo_intermediario1,
                            pos = nx.get_node_attributes(G, 'pos'),
                            font_size = 2,
                            alpha = 1)
    
    nx.draw_networkx_labels(subgrafo_intermediario2,
                            pos = nx.get_node_attributes(G, 'pos'),
                            font_size = 2,
                            alpha = 1)
    
    nx.draw_networkx_labels(subgrafo_intermediario3,
                            pos = nx.get_node_attributes(G, 'pos'),
                            font_size = 2,
                            alpha = 1)
    
    nx.draw_networkx_labels(subgrafo_volta,
                            pos = nx.get_node_attributes(G, 'pos'),
                            font_size = 2,
                            alpha = 1)
    
    plt.savefig(f'Roteiro {origem} - {destino1} - {destino2} - {destino3} - {destino4} - {pouso_final}_{data_hora}.pdf',
                dpi = 300,
                facecolor = 'w',
                edgecolor = 'w',
                orientation = 'landscape',
                papertype = 'b0',
                format = 'pdf',
                transparent = True,
                bbox_inches = 'tight',
                pad_inches = 0.1,
                frameon = None,
                metadata = None)
    

    plt.close()
    
    ###########################################################    
    
    # incluir valor do percurso no dicionario de resultados
    
    dicionario_resultado[lista_permutacoes[permutacao]] = round(valor_roteiro_total, 1)

    
    ###########################################################


print('#####################')  
print('')

for i in sorted(dicionario_resultado, key = dicionario_resultado.get):
    print(i,' => ', dicionario_resultado[i])


print('')
depois = time.time()
print(f'Tempo de processamento = {depois - antes:.1f} segundos')
print('')


print('### FINALIZADO ###')

# Finish up by removing from the screen
window.close()

########################################################### 

