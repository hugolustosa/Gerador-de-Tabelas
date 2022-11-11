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

aeronaves_df = pd.read_excel(tabelao, sheet_name = 'aeronaves')

arestas_df = pd.read_excel(tabelao, sheet_name = 'arestas')

vertices_df = pd.read_excel(tabelao, sheet_name = 'vertices')

vertices2_df = pd.read_excel(tabelao, sheet_name = 'vertices')

portoes_quadriculas_df = pd.read_excel(tabelao, sheet_name = 'portoes_quadriculas') # quadriculas da bacia de santos

portoes_faixas_bc_df = pd.read_excel(tabelao, sheet_name = 'portoes_faixas_bc') # faixas da bacia de campos


########################################################### 
# ENTRADA DOS AERODROMOS, PLATAFORMAS E QTD. DE PASSAGEIROS

# Define the window's contents

sg.theme('DarkBlue3')

layout1 = [[sg.Text("PREFIXO_PROVISORIO:"), sg.Combo(list(aeronaves_df["PREFIXO_PROVISORIO"]), 'OHA', size=(10,1), key='-PREFIXO-')],
          [sg.Text("BASE ORIGEM:", size=(12,1)), sg.Combo(list(vertices_df.loc[vertices_df["TIPO"] == '1.BASE', "PONTO"]), 'SBJR', size=(12,1), key='-INPUT_ORIGEM-')],
          [sg.Text("UM1:", size=(3,1)), sg.Combo(list(vertices_df.loc[vertices_df["TIPO"] == '3.UM', "PONTO"]), size=(22,1), key='-INPUT_UM1-'), sg.Text("EMBARQUE:"), sg.Combo([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], 0, key='-BASE1_UM1-'), sg.Text("DESEMBARQUE:"), sg.Combo([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], 0, key='-UM1_BASE2-')],
          [sg.Text("UM2:", size=(3,1)), sg.Combo(list(vertices_df.loc[vertices_df["TIPO"] == '3.UM', "PONTO"]), size=(22,1), key='-INPUT_UM2-'), sg.Text("EMBARQUE:"), sg.Combo([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], 0, key='-BASE1_UM2-'), sg.Text("DESEMBARQUE:"), sg.Combo([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], 0, key='-UM2_BASE2-'), sg.Text("Caso não tenha UM 2 repita a UM 1")],
          [sg.Text("UM3:", size=(3,1)), sg.Combo(list(vertices_df.loc[vertices_df["TIPO"] == '3.UM', "PONTO"]), size=(22,1), key='-INPUT_UM3-'), sg.Text("EMBARQUE:"), sg.Combo([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], 0, key='-BASE1_UM3-'), sg.Text("DESEMBARQUE:"), sg.Combo([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], 0, key='-UM3_BASE2-'), sg.Text("Caso não tenha UM 3 repita a UM 2")],
          [sg.Text("UM4:", size=(3,1)), sg.Combo(list(vertices_df.loc[vertices_df["TIPO"] == '3.UM', "PONTO"]), size=(22,1), key='-INPUT_UM4-'), sg.Text("EMBARQUE:"), sg.Combo([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], 0, key='-BASE1_UM4-'), sg.Text("DESEMBARQUE:"), sg.Combo([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], 0, key='-UM4_BASE2-'), sg.Text("Caso não tenha UM 4 repita a UM 3")],
          [sg.Text("BASE DESTINO:", size=(12,1)), sg.Combo(list(vertices_df.loc[vertices_df["TIPO"] == '1.BASE', "PONTO"]), 'SBJR', size=(12,1), key='-INPUT_DESTINO-')],
          [sg.Button('CONFIRMAR DESTINOS')],
          [sg.Text(size=(80,2), key='-OUTPUT-')],
          [sg.HSep()],
          [sg.Text("TRANSBORDOS DE PAX", size=(80,2))],
          [sg.Combo([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], 0, key='-UM1_UM2-'), sg.Text("UM1=>UM2:", size=(50,1), key='-UM1=>UM2-')],
          [sg.Combo([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], 0, key='-UM1_UM3-'), sg.Text("UM1=>UM3:", size=(50,1), key='-UM1=>UM3-')],
          [sg.Combo([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], 0, key='-UM1_UM4-'), sg.Text("UM1=>UM4:", size=(50,1), key='-UM1=>UM4-')],
          [sg.Combo([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], 0, key='-UM2_UM3-'), sg.Text("UM2=>UM3:", size=(50,1), key='-UM2=>UM3-')],
          [sg.Combo([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], 0, key='-UM2_UM4-'), sg.Text("UM2=>UM4:", size=(50,1), key='-UM2=>UM4-')],
          [sg.Combo([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], 0, key='-UM3_UM4-'), sg.Text("UM3=>UM4:", size=(50,1), key='-UM3=>UM4-')],
          [sg.Button('ROTEIRIZAR')]]


# Create the window 1
window1 = sg.Window('ROTEIRIZADOR AEREO (by LOFF/OPTA) - Versao 1.0', layout1)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window1.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'ROTEIRIZAR':
        break
    # Output a message to the window
    window1['-OUTPUT-'].update(f"O roteiro escolhido foi: {values['-INPUT_ORIGEM-']} => {values['-INPUT_UM1-']} => {values['-INPUT_UM2-']} => {values['-INPUT_UM3-']} => {values['-INPUT_UM4-']} => {values['-INPUT_DESTINO-']}.")
    window1['-UM1=>UM2-'].update(f"{values['-INPUT_UM1-']} => {values['-INPUT_UM2-']}")
    window1['-UM1=>UM3-'].update(f"{values['-INPUT_UM1-']} => {values['-INPUT_UM3-']}")
    window1['-UM1=>UM4-'].update(f"{values['-INPUT_UM1-']} => {values['-INPUT_UM4-']}")
    window1['-UM2=>UM3-'].update(f"{values['-INPUT_UM2-']} => {values['-INPUT_UM3-']}")
    window1['-UM2=>UM4-'].update(f"{values['-INPUT_UM2-']} => {values['-INPUT_UM4-']}")
    window1['-UM3=>UM4-'].update(f"{values['-INPUT_UM3-']} => {values['-INPUT_UM4-']}")
    

########################################################### 

antes = time.time()
data_hora = time.strftime('%Y-%m-%d %Hh%Mm%S', time.localtime())

########################################################### 
    
prefixo = values['-PREFIXO-']
origem = values['-INPUT_ORIGEM-']
destino1 = values['-INPUT_UM1-']
destino2 = values['-INPUT_UM2-']
destino3 = values['-INPUT_UM3-']
destino4 = values['-INPUT_UM4-']
pouso_final = values['-INPUT_DESTINO-']

pax_base1_um1 = values['-BASE1_UM1-']
pax_base1_um2 = values['-BASE1_UM2-']
pax_base1_um3 = values['-BASE1_UM3-']
pax_base1_um4 = values['-BASE1_UM4-']

pax_um1_um2 = values['-UM1_UM2-']
pax_um1_um3 = values['-UM1_UM3-']
pax_um1_um4 = values['-UM1_UM4-']
pax_um1_base2 = values['-UM1_BASE2-']

pax_um2_um1 = 0
pax_um2_um3 = values['-UM2_UM3-']
pax_um2_um4 = values['-UM2_UM4-']
pax_um2_base2 = values['-UM2_BASE2-']

pax_um3_um1 = 0
pax_um3_um2 = 0
pax_um3_um4 = values['-UM3_UM4-']
pax_um3_base2 = values['-UM3_BASE2-']

pax_um4_um1 = 0
pax_um4_um2 = 0
pax_um4_um3 = 0
pax_um4_base2 = values['-UM4_BASE2-']


dicionario_sobe_desce = {(origem, destino1):pax_base1_um1,
                         (origem, destino2):pax_base1_um2,
                         (origem, destino3):pax_base1_um3,
                         (origem, destino4):pax_base1_um4,
                         (destino1, destino2):pax_um1_um2,
                         (destino1, destino3):pax_um1_um3,
                         (destino1, destino4):pax_um1_um4,
                         (destino1, pouso_final):pax_um1_base2,
                         (destino2, destino1):pax_um2_um1,
                         (destino2, destino3):pax_um2_um3,
                         (destino2, destino4):pax_um2_um4,
                         (destino2, pouso_final):pax_um2_base2,
                         (destino3, destino1):pax_um3_um1,
                         (destino3, destino2):pax_um3_um2,
                         (destino3, destino4):pax_um3_um4,
                         (destino3, pouso_final):pax_um3_base2,
                         (destino4, destino1):pax_um4_um1,
                         (destino4, destino2):pax_um4_um2,
                         (destino4, destino3):pax_um4_um3,
                         (destino4, pouso_final):pax_um4_base2}

########################################################### 

lista_destinos = [destino1, destino2, destino3, destino4]

num_pousos = 1
for i in range(1, len(lista_destinos)):
    if lista_destinos[i] != lista_destinos[i-1]:
        num_pousos = num_pousos + 1


lista_permutacoes_total = list(itertools.permutations(lista_destinos))

lista_permutacoes_unicas = []

#PARA DIMINUIR A LISTA DE PERMUTAÇÕES EM CASO DE UNIDADES IGUAIS
for i in lista_permutacoes_total:
    if i not in lista_permutacoes_unicas:
        lista_permutacoes_unicas.append(i)

listas_permutacoes_inviaveis = []

for i in lista_permutacoes_unicas:
    if i[0]==i[2] and i[0]!=i[1]:
        listas_permutacoes_inviaveis.append(i)
    
    if i[0]==i[3] and (i[0]!=i[1] or i[0]!=i[2]):
        listas_permutacoes_inviaveis.append(i)
    
    if i[1]==i[3] and i[1]!=i[2]:
        listas_permutacoes_inviaveis.append(i)
    
lista_permutacoes = []

for i in lista_permutacoes_unicas:
    if i not in listas_permutacoes_inviaveis:
        lista_permutacoes.append(i)
        
lista_permutacoes_restritas = {}

###########################################################
# dados das poligonais da BS e ES

'''https://automating-gis-processes.github.io/CSC18/lessons/L4/point-in-polygon.html'''

poligono_coords_BS = Polygon([(-23.7108916666667,-43.6677416666667),(-23.5687611111111,-43.1358916666667),(-23,1775611111111,-42.7796305555556),(-23,1029444444444,-42.4989027777778),(-23,5058833333333,-42.4989),(-23,5058805555556,-41.9987138888889),(-24,3333333333333,-41.6666666666667),(-25,-41.6666666666667),(-25.6666666666667,-42.3333333333333),(-26.333325,-43.3333138888889),(-26.333325,-43.6666472222222)])

poligono_coords_ES = Polygon([(-20.9083333333333,-40.1103333333333),(-20.8578333333333,-39.967),(-20.2108333333333,-39.5775),(-19.9575,-39.6528333333333),	(-19.564465,-39.253961),(-19.6012,-38.3478),(-21.4019,-39.2816),(-21.4058,-40.453)])

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

# quadrantes fictícios na bacia do ES (OS 4 QUADRANDOS DO ES SÃO IDENTICOS, FORAM CRIADOS ASSIM PARA CRIAR TODOS AS ARESTAS POSSÍVEIS PARA OS 4 WAYPOITS FINAIS)

coord_ES01 = ['ES01', Polygon([(-20.9083333333333,-40.1103333333333),(-20.8578333333333,-39.967),(-20.2108333333333,-39.5775),(-19.9575,-39.6528333333333),	(-19.564465,-39.253961),(-19.6012,-38.3478),(-21.4019,-39.2816),(-21.4058,-40.453)])]

coord_ES02 = ['ES02', Polygon([(-20.9083333333333,-40.1103333333333),(-20.8578333333333,-39.967),(-20.2108333333333,-39.5775),(-19.9575,-39.6528333333333),	(-19.564465,-39.253961),(-19.6012,-38.3478),(-21.4019,-39.2816),(-21.4058,-40.453)])]

coord_ES03 = ['ES03', Polygon([(-20.9083333333333,-40.1103333333333),(-20.8578333333333,-39.967),(-20.2108333333333,-39.5775),(-19.9575,-39.6528333333333),	(-19.564465,-39.253961),(-19.6012,-38.3478),(-21.4019,-39.2816),(-21.4058,-40.453)])]

coord_ES04 = ['ES04', Polygon([(-20.9083333333333,-40.1103333333333),(-20.8578333333333,-39.967),(-20.2108333333333,-39.5775),(-19.9575,-39.6528333333333),	(-19.564465,-39.253961),(-19.6012,-38.3478),(-21.4019,-39.2816),(-21.4058,-40.453)])]

coord_ES05 = ['ES05', Polygon([(-20.9083333333333,-40.1103333333333),(-20.8578333333333,-39.967),(-20.2108333333333,-39.5775),(-19.9575,-39.6528333333333),	(-19.564465,-39.253961),(-19.6012,-38.3478),(-21.4019,-39.2816),(-21.4058,-40.453)])]

lista_quadrantes = [coord_QDA4, coord_QDA5, coord_QDA6, coord_QDA7, coord_QDA8, coord_QDA9, coord_QDB4, coord_QDB5, coord_QDB6, coord_QDB7, coord_QDB8, coord_QDB9, coord_QDC4, coord_QDC5, coord_QDC6, coord_QDC7, coord_QDC8, coord_QDC9, coord_QDD4, coord_QDD5, coord_QDD6, coord_QDD7, coord_QDD8, coord_QDD9, coord_QDE0, coord_QDE1, coord_QDE2, coord_QDE3, coord_QDF0, coord_QDF1, coord_QDF2, coord_QDF3, coord_QDG0, coord_QDG1, coord_QDG2, coord_QDG3, coord_QDH0, coord_QDH1, coord_QDH2, coord_QDH3, coord_ES01, coord_ES02, coord_ES03, coord_ES04, coord_ES05]

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
    return 3440 * math.acos(math.cos((90-lat1)*0.017453) * math.cos((90-lat2)*0.017453) + math.sin((90-lat1)*0.017453) * math.sin((90-lat2)*0.017453) * math.cos((long1-long2)*0.017453))
    
def distancia_cartesiana(lat1, long1, lat2, long2):
    '''função que retorna a distancia em milhas náuticas a partir das coordenadas geográficas de dois pontos. Não leva em consideração a curvatura da Terra'''
    return (((lat1 - lat2) ** 2 + (long1 - long2) ** 2) ** 0.5) * 60


###########################################################
    
#DADOS PARA CÁLCULO DE DISPONÍVEL, TEMPO E VOO E CONSUMO DE QAV
   
peso_pax = 107
PMD = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "PMD"])
PBO = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "PBO"])
CONSUMO_VOO = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "CONSUMO_VOO"])
CONSUMO_SOLO = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "CONSUMO_SOLO"])
TEMPO_ACIO_DECOL = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "TEMPO_ACIO_DECOL"])
TEMPO_POUSADOPLATAFORMA = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "TEMPO_POUSADOPLATAFORMA"]) * num_pousos
TEMPO_POUSOCORTE = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "TEMPO_POUSOCORTE"])
TEMPO_CIRCUITO = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "TEMPO_CIRCUITO"]) * num_pousos
TETO_CRUZEIRO = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "TETO_CRUZEIRO"])
RAZAO_SUBIDA = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "RAZAO_SUBIDA"])
RAZAO_DESCIDA = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "RAZAO_DESCIDA"])
VELOCIDADE_CRUZEIRO = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "VELOCIDADE_CRUZEIRO"])
numero_tripulantes = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "NUM_TRIPULANTES"])
numero_pax = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "NUM_PAX"])
capacidade_tanque_qav = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "CAP_TANQUE"])
preco_hora_voada = float(aeronaves_df.loc[aeronaves_df["PREFIXO_PROVISORIO"] == prefixo, "PRECO_HV"])


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

dicionario_pax_milhas = {}

for permutacao in range(len(lista_permutacoes)):
    destino1 = lista_permutacoes[permutacao][0]
    destino2 = lista_permutacoes[permutacao][1]
    destino3 = lista_permutacoes[permutacao][2]
    destino4 = lista_permutacoes[permutacao][3]
    
    lista_destinos_permutacao_i = [destino1, destino2, destino3, destino4]
  
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
   
    #verificação se o destino está no espaço aéreo da BS, ES ou BC, verifica qual quadrícula ou faixa e encontra e acrescenta as arestas de chegada e saida da plataforma
    
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
        
    if coord_destino1.within(poligono_coords_BS) == True or coord_destino1.within(poligono_coords_ES) == True: #verifica se o destino1 está dentro da poligonal da BS ou ES
        for i in lista_quadrantes:
            if i[1].contains(coord_destino1) == True: #verifica se está dentro dos quadrantes da BS ou ES
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
                        
                              
    # CASO PLATAFORMA 1 ESTEJA FORA DA ÁREA DO ESPAÇO AÉREO DA BS, ES E BC       
            
    if coord_destino1.within(poligono_coords_BS) == False and coord_destino1.within(poligono_coords_BC) == False and coord_destino1.within(poligono_coords_ES) == False: 
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
    
    if coord_destino4.within(poligono_coords_BS) == True or coord_destino4.within(poligono_coords_ES) == True: #verifica se o destino4 está dentro da poligonal da BS ou ES
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
            
    if coord_destino4.within(poligono_coords_BS) == False and coord_destino4.within(poligono_coords_BC) == False and coord_destino4.within(poligono_coords_ES) == False: #verifica se está fora da poligonal da BS, ES e BC
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
    
    mapa = folium.Map(location=[-24.010991, -43.087035], zoom_start=6)   
    
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
        
    mapa.save(f"{origem} - {destino1} - {destino2} - {destino3} - {destino4} - {pouso_final}_{data_hora}.html")
    
    #####################################################
    #CÁLCULO DA QUANTIDADE DE PAX NO EMBARQUE
    
    TEMPO_SOLO = (TEMPO_ACIO_DECOL + TEMPO_POUSADOPLATAFORMA + TEMPO_POUSOCORTE) / 60
    
    TEMPO_SUBIDA = (TETO_CRUZEIRO / RAZAO_SUBIDA) / 60
    
    TEMPO_DESCIDA = (TETO_CRUZEIRO / RAZAO_DESCIDA) / 60
    
    ACELERACAO_SUBIDA = VELOCIDADE_CRUZEIRO / TEMPO_SUBIDA
    
    ACELERACAO_DESCIDA = - (VELOCIDADE_CRUZEIRO / TEMPO_DESCIDA)
    
    DISTANCIA_SUBIDA = ACELERACAO_SUBIDA * (TEMPO_SUBIDA ** 2 / 2)
    
    DISTANCIA_DESCIDA = - ACELERACAO_DESCIDA * (TEMPO_DESCIDA ** 2 / 2)
    
    DISTANCIA_CRUZEIRO = valor_medio_roteiro_total - DISTANCIA_SUBIDA - DISTANCIA_DESCIDA
    
    TEMPO_CRUZEIRO = DISTANCIA_CRUZEIRO / VELOCIDADE_CRUZEIRO
    
    TEMPO_IDA = TEMPO_SUBIDA + TEMPO_DESCIDA + TEMPO_CRUZEIRO
    
    TEMPO_VOLTA = TEMPO_IDA
    
    TEMPO_VOO = TEMPO_IDA + TEMPO_VOLTA + TEMPO_CIRCUITO / 60 #CONSIDERA OS TEMPOS DE TODAS AS PLATAFORMAS
    
    COMB_MISSAO = TEMPO_VOO * CONSUMO_VOO + TEMPO_SOLO * CONSUMO_SOLO
    
    TEMPO_MISSAO = TEMPO_VOO + TEMPO_SOLO
    
    COMB_RESERVA = (max(0.5, 1/3 + 0.1 * TEMPO_MISSAO)) * CONSUMO_VOO
    
    COMBUSTIVEL = COMB_MISSAO + COMB_RESERVA
    
    PAYLOAD = PMD - PBO - COMBUSTIVEL
    
    QUANT_PAX = min(numero_pax, PAYLOAD / peso_pax)

    qav_necessario = COMBUSTIVEL

    TEMPO_VOO_PAGO = TEMPO_VOO + TEMPO_POUSADOPLATAFORMA / 60 #CONSIDERA OS TEMPOS DE TODAS AS PLATAFORMAS
    
    CUSTO_HORA_VOADA = TEMPO_VOO_PAGO * preco_hora_voada
    
    ########################################################### 
    #API REDEMET
    
    hora_zulu = str(int(data_hora[11:13])+3)
    data_resumida = data_hora[:4] + data_hora[5:7] + data_hora[8:10] + hora_zulu
    chave_api = 'colar chave API redemet aqui'
    
    try:
        informacao_origem = requests.get(f"https://api-redemet.decea.mil.br/aerodromos/info?api_key={chave_api}&localidade={origem}&datahora={data_resumida}")
         
        informacao_origem = informacao_origem.json()
        informacao_origem_metar = informacao_origem['data']['metar']
        informacao_origem_teto = informacao_origem['data']['teto']
        informacao_origem_visibilidade = informacao_origem['data']['visibilidade']
        informacao_origem_ceu = informacao_origem['data']['ceu']
        informacao_origem_condicoes_tempo = informacao_origem['data']['condicoes_tempo']
    except:
        informacao_origem = 'sem informação METAR'
        informacao_origem_metar = 'sem informação METAR'
        informacao_origem_teto = 'sem informação METAR'
        informacao_origem_visibilidade = 'sem informação METAR'
        informacao_origem_ceu = 'sem informação METAR'
        informacao_origem_condicoes_tempo = 'sem informação METAR'       
    
    try:
        informacao_pouso_final = requests.get(f"https://api-redemet.decea.mil.br/aerodromos/info?api_key={chave_api}&localidade={pouso_final}&datahora={data_resumida}")
         
        informacao_pouso_final = informacao_pouso_final.json()
        informacao_pouso_final_metar = informacao_pouso_final['data']['metar']
        informacao_pouso_final_teto = informacao_pouso_final['data']['teto']
        informacao_pouso_final_visibilidade = informacao_pouso_final['data']['visibilidade']
        informacao_pouso_final_ceu = informacao_pouso_final['data']['ceu']
        informacao_pouso_final_condicoes_tempo = informacao_pouso_final['data']['condicoes_tempo']
    except:        
        informacao_pouso_final = 'sem informação METAR'
        informacao_pouso_final_metar = 'sem informação METAR'
        informacao_pouso_final_teto = 'sem informação METAR'
        informacao_pouso_final_visibilidade = 'sem informação METAR'
        informacao_pouso_final_ceu = 'sem informação METAR'
        informacao_pouso_final_condicoes_tempo = 'sem informação METAR'        
     

    try: 
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
    except:
        cor_farol_origem = 'sem informação status'
        cor_farol_pouso_final = 'sem informação status'
    
    
    lista_destinos_permutacao_i = [destino1, destino2, destino3, destino4]
    
       
    for i in dicionario_sobe_desce:
        if origem == i[0] and destino1 == i[1]:
            pax_base1_um1 = dicionario_sobe_desce[i]
        
        if origem == i[0] and destino2 == i[1]:
            pax_base1_um2 = dicionario_sobe_desce[i]
        
        if origem == i[0] and destino3 == i[1]:
            pax_base1_um3 = dicionario_sobe_desce[i]
        
        if origem == i[0] and destino4 == i[1]:
            pax_base1_um4 = dicionario_sobe_desce[i]
        
        if destino1 == i[0] and destino2 == i[1]:
            pax_um1_um2 = dicionario_sobe_desce[i]
        
        if destino1 == i[0] and destino3 == i[1]:
            pax_um1_um3 = dicionario_sobe_desce[i]
        
        if destino1 == i[0] and destino4 == i[1]:
            pax_um1_um4 = dicionario_sobe_desce[i]
        
        if destino1 == i[0] and pouso_final == i[1]:
            pax_um1_base2 = dicionario_sobe_desce[i]
        
        if destino2 == i[0] and destino1 == i[1]:
            pax_um2_um1 = dicionario_sobe_desce[i]
        
        if destino2 == i[0] and destino3 == i[1]:
            pax_um2_um3 = dicionario_sobe_desce[i]
        
        if destino2 == i[0] and destino4 == i[1]:
            pax_um2_um4 = dicionario_sobe_desce[i]
        
        if destino2 == i[0] and pouso_final == i[1]:
            pax_um2_base2 = dicionario_sobe_desce[i]
        
        if destino3 == i[0] and destino1 == i[1]:
            pax_um3_um1 = dicionario_sobe_desce[i]
        
        if destino3 == i[0] and destino2 == i[1]:
            pax_um3_um2 = dicionario_sobe_desce[i]
        
        if destino3 == i[0] and destino4 == i[1]:
            pax_um3_um4 = dicionario_sobe_desce[i]
        
        if destino3 == i[0] and pouso_final == i[1]:
            pax_um3_base2 = dicionario_sobe_desce[i]
        
        if destino4 == i[0] and destino1 == i[1]:
            pax_um4_um1 = dicionario_sobe_desce[i]
        
        if destino4 == i[0] and destino2 == i[1]:
            pax_um4_um2 = dicionario_sobe_desce[i]
        
        if destino4 == i[0] and destino3 == i[1]:
            pax_um4_um3 = dicionario_sobe_desce[i]
        
        if destino4 == i[0] and pouso_final == i[1]:
            pax_um4_base2 = dicionario_sobe_desce[i]

    if destino2 == destino1:
        pax_base1_um2 = 0
        pax_um2_base2 = 0
        pax_um1_um2 = 0
        pax_um2_um3 = 0
        pax_um2_um4 = 0

        
    if destino3 == destino2:
        pax_base1_um3 = 0
        pax_um3_base2 = 0
        pax_um1_um3 = 0  
        pax_um2_um3 = 0
        pax_um3_um4 = 0
          
    
    if destino4 == destino3:
        pax_base1_um4 = 0
        pax_um4_base2 = 0
        pax_um1_um4 = 0        
        pax_um2_um4 = 0
        pax_um3_um4 = 0
        
    
    pax_trecho1 = numero_tripulantes + pax_base1_um1 + pax_base1_um2 + pax_base1_um3 + pax_base1_um4
    
    pax_trecho2 = numero_tripulantes + pax_um1_base2 + pax_um1_um2 + pax_um1_um3 + pax_um1_um4 + pax_base1_um2 + pax_base1_um3 + pax_base1_um4
    
    pax_trecho3 = numero_tripulantes + pax_um1_um4 + pax_um1_base2 + pax_um2_base2 + pax_um2_um3 + pax_um1_um3 + pax_um2_um4 + pax_base1_um3 + pax_base1_um4
    
    pax_trecho4 = numero_tripulantes + pax_um1_um4 + pax_um3_um4 + pax_um1_base2 + pax_um2_base2 + pax_um3_base2 + pax_base1_um4
    
    pax_trecho5 = numero_tripulantes + pax_um1_base2 + pax_um2_base2 + pax_um3_base2 + pax_um4_base2
                                    
    pax_milhas = valor_roteiro_ida * pax_trecho1 + valor_roteiro_intermediario1 * pax_trecho2 + valor_roteiro_intermediario2 * pax_trecho3 + valor_roteiro_intermediario3 * pax_trecho4 + valor_roteiro_volta * pax_trecho5
    
    ########################################################### 
    # análise de viabilidade do roteiro
    
    if (numero_pax + numero_tripulantes) >= max(pax_trecho1, pax_trecho2, pax_trecho3, pax_trecho4, pax_trecho5) and capacidade_tanque_qav >= qav_necessario and QUANT_PAX >= (pax_base1_um1 + pax_base1_um2 + pax_base1_um3 + pax_base1_um4):
        dicionario_resultado[lista_permutacoes[permutacao]] = round(valor_roteiro_total, 1)  
        dicionario_pax_milhas[lista_permutacoes[permutacao]] = round(pax_milhas, 1)
        viabilidade = 'ROTEIRO VIÁVEL'
    else:
        viabilidade = 'ROTEIRO INVIÁVEL'
  
    
    ########################################################### 
    # draw graph
        
    plt.axes([0.1, 0.1, 0.5, 0.83])
    
    #plt.axis("off")
        
    plt.axis([-45.4, -37, -26.8, -19.50])
    
    plt.title(f'{origem} -> {destino1} -> {destino2} -> {destino3} -> {destino4} -> {pouso_final}', fontsize=5)
    
    plt.text(-45.3, -19.60, f'{viabilidade}: {destino1}({pax_base1_um1}/{pax_um1_base2}) -> {destino2}({pax_base1_um2}/{pax_um2_base2}) -> {destino3}({pax_base1_um3}/{pax_um3_base2}) -> {destino4}({pax_base1_um4}/{pax_um4_base2})', fontsize=2.5)
    
    
    plt.text(-45.3, -19.70, f'Transbordos:{destino1}=>{destino2}({pax_um1_um2})', fontsize=2.5) 
    
    plt.text(-45.3, -19.80, f'Transbordos:{destino1}=>{destino3}({pax_um1_um3})', fontsize=2.5)     
    
    plt.text(-45.3, -19.90, f'Transbordos:{destino1}=>{destino4}({pax_um1_um4})', fontsize=2.5)     
    
    plt.text(-45.3, -20.00, f'Transbordos:{destino2}=>{destino3}({pax_um2_um3})', fontsize=2.5)

    plt.text(-45.3, -20.10, f'Transbordos:{destino2}=>{destino4}({pax_um2_um4})', fontsize=2.5)     
    
    plt.text(-45.3, -20.20, f'Transbordos:{destino3}=>{destino4}({pax_um3_um4})', fontsize=2.5) 
    
    
    plt.text(-45.3, -20.30, f'trecho1: {int(pax_trecho1 - numero_tripulantes)} pax; trecho2: {int(pax_trecho2 - numero_tripulantes)} pax; trecho3: {int(pax_trecho3 - numero_tripulantes)} pax; trecho4: {int(pax_trecho4 - numero_tripulantes)} pax; trecho5: {int(pax_trecho5 - numero_tripulantes)} pax', fontsize=2.5)
    
    plt.text(-45.3, -20.40, f'Pax x milhas: {pax_milhas:.1f} pax.mn', fontsize=2.5)
    
    plt.text(-45.3, -20.50, f'Distancia total: {valor_roteiro_total:.2f} mn', fontsize=2.5)
    
    plt.text(-45.3, -20.60, f'Distancia media: {valor_medio_roteiro_total:.2f} mn', fontsize=2.5)
    
    plt.text(-45.3, -20.70, f'Prefixo aeronave: {prefixo}', fontsize=2.5)
    
    plt.text(-45.3, -20.80, f'# pax máximo no embarque: {QUANT_PAX:.1f} pax', fontsize=2.5)
    
    plt.text(-45.3, -20.90, f'Tempo missão: {TEMPO_MISSAO:.2f} h', fontsize=2.5)
    
    plt.text(-45.3, -21.00, f'Custo estimado horas voada: R$ {CUSTO_HORA_VOADA:.2f}', fontsize=2.5)
    
      
    plt.text(-45.3, -21.20, f'{informacao_origem_metar}', fontsize=2.5)
    
    plt.text(-45.3, -21.30, f'TETO ORIGEM: {informacao_origem_teto}', fontsize=2.5)
    
    plt.text(-45.3, -21.40, f'VISIBILIDADE ORIGEM: {informacao_origem_visibilidade}', fontsize=2.5)
    
    plt.text(-45.3, -21.50, f'CEU ORIGEM: {informacao_origem_ceu}', fontsize=2.5)
    
    plt.text(-45.3, -21.60, f'CONDICOES TEMPO ORIGEM: {informacao_origem_condicoes_tempo}', fontsize=2.5)
    
    plt.text(-45.3, -21.70, f'BOLINHA REDEMET ORIGEM: {cor_farol_origem}', fontsize=2.5)
    
    plt.text(-45.3, -21.90, f'{informacao_pouso_final_metar}', fontsize=2.5)
    
    plt.text(-45.3, -22.00, f'TETO POUSO FINAL: {informacao_pouso_final_teto}', fontsize=2.5)
    
    plt.text(-45.3, -22.10, f'VISIBILIDADE POUSO FINAL: {informacao_pouso_final_visibilidade}', fontsize=2.5)
    
    plt.text(-45.3, -22.20, f'CEU POUSO FINAL: {informacao_pouso_final_ceu}', fontsize=2.5)
    
    plt.text(-45.3, -22.30, f'CONDICOES TEMPO POUSO FINAL: {informacao_pouso_final_condicoes_tempo}', fontsize=2.5)
    
    plt.text(-45.3, -22.40, f'BOLINHA REDEMET POUSO FINAL: {cor_farol_pouso_final}', fontsize=2.5)    
    
     
    plt.text(-45.3, -26.10, f'Ida: {caminho_ida} -> {valor_roteiro_ida:.2f} mn', fontsize=2.5)
    
    plt.text(-45.3, -26.20, f'Inter1: {caminho_intermediario1} -> {valor_roteiro_intermediario1:.2f} mn', fontsize=2.5)
    
    plt.text(-45.3, -26.30, f'Inter2: {caminho_intermediario2} -> {valor_roteiro_intermediario2:.2f} mn', fontsize=2.5)
    
    plt.text(-45.3, -26.40, f'Inter3: {caminho_intermediario3} -> {valor_roteiro_intermediario3:.2f} mn', fontsize=2.5)
    
    plt.text(-45.3, -26.50, f'Volta: {caminho_volta} -> {valor_roteiro_volta:.2f} mn', fontsize=2.5)   

    plt.text(-45, -26.60, '#### Planejamento deverá ser confirmado com a cia. aérea que utilizará os dados reais da aeronave ####', fontsize=2.5)
    
    plt.text(-45, -26.70, f'IMPRESSO EM: {data_hora}', fontsize=2.5)


    
    nx.draw_networkx_nodes(G,
                           pos = nx.get_node_attributes(G, 'pos'),
                           node_size = 0.01,
                           node_color = 'b',
                           alpha = 0.3,
                           node_shape = 'o')
    
    nx.draw_networkx_edges(G,
                           pos = nx.get_node_attributes(G, 'pos'),
                           edgelist = None,
                           width = 0.01,
                           edge_color = 'k',
                           style = 'solid',
                           alpha = 0.03,
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
                            alpha = 0.2)
    
    
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
                           arrows = None,
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
    
    plt.savefig(f'{origem} - {destino1} - {destino2} - {destino3} - {destino4} - {pouso_final}_{data_hora}.pdf',
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


# Finish up by removing from the screen
window1.close()

print('#####################')  
print('')
print('RANKING EM MILHAS NÁUTICAS:')

try:
    for i in sorted(dicionario_resultado, key = dicionario_resultado.get):
        print(i,' => ', dicionario_resultado[i])
    
    resultado_milhas = sorted(dicionario_resultado, key = dicionario_resultado.get)[0]
except:
    print('nenhum roteiro viável')


print('#####################')  
print('')
print('RANKING EM PAX x MILHAS NÁUTICAS:')


try:
    for i in sorted(dicionario_pax_milhas, key = dicionario_pax_milhas.get):
        print(i,' => ', dicionario_pax_milhas[i])
    
    resultado_pax_milhas = sorted(dicionario_pax_milhas, key = dicionario_pax_milhas.get)[0]
    
    print('')
    depois = time.time()
    print(f'Tempo de processamento = {depois - antes:.1f} segundos')
    print('')
    
    print('### FINALIZADO ###')
    
    
    layout2 = [[sg.Text("RESULTADO. RANKING EM MILHAS NÁUTICAS:")],
              [sg.Text(resultado_milhas), sg.Text("=>"), sg.Text(dicionario_resultado[resultado_milhas])],
              [sg.Text("RESULTADO. RANKING EM PAX x MILHAS NÁUTICAS:")],
              [sg.Text(resultado_pax_milhas), sg.Text("=>"), sg.Text(dicionario_pax_milhas[resultado_pax_milhas])],
              [sg.Button('FECHAR')]]
    
    
    # Create the window 2
    window2 = sg.Window('ROTEIRIZADOR AEREO (by LOFF/OPTA) - Versao 1.0', layout2)
    
    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window2.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'FECHAR':
            break
    
    
    # Finish up by removing from the screen
    window2.close()
except:
    print('nenhum roteiro viável')
########################################################### 

