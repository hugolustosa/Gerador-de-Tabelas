import networkx as nx
import random
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import collections
import pandas as pd
import math
import win32com.client as win32

########################################################### 

#DADOS DE ENTRADA

cen_preco_qav = '5.00'
cen_base_qav = 'todas_bases' #quando não especificado o preço do qav da base será R$ 5.00 por litro

cenario = f'Cenario_qav_{cen_preco_qav}_reais_{cen_base_qav}'

tabelao = f'INPUT_para_tabelao_qav_{cen_preco_qav}_reais_{cen_base_qav}.xlsx'

arestas_df = pd.read_excel(tabelao, sheet_name = 'arestas')

vertices_df = pd.read_excel(tabelao, sheet_name = 'vertices')

combinacoes_df = pd.read_excel(tabelao, sheet_name = 'aeronaves_roteiros')


########################################################### 

G = nx.from_pandas_edgelist(arestas_df, source='ORIGEM', target='DESTINO', edge_attr='DISTANCIA', create_using=nx.DiGraph())


for i in vertices_df.index:
    G.add_node(vertices_df['PONTO'][i], pos = (vertices_df['LONG'][i] , vertices_df['LAT'][i]))


for i in combinacoes_df.index:
    origem = combinacoes_df.loc[i]['ORIGEM']
    destino = combinacoes_df.loc[i]['DESTINO']
    pouso_final = combinacoes_df.loc[i]['POUSO_FINAL']
     
    caminho_ida = nx.shortest_path(G, source = origem, target = destino, weight='DISTANCIA', method='dijkstra')
    caminho_volta = nx.shortest_path(G, source = destino, target = pouso_final, weight='DISTANCIA', method='dijkstra')
        
    pares_ordenados_ida = []
    valor_roteiro_ida = 0
    subgrafo_ida = nx.DiGraph()
    for j in range(len(caminho_ida) - 1):
        pares_ordenados_ida.append((caminho_ida[j] , caminho_ida[j+1]))
        valor_roteiro_ida = valor_roteiro_ida + G[pares_ordenados_ida[-1][0]][pares_ordenados_ida[-1][1]]['DISTANCIA']
        subgrafo_ida.add_edge(caminho_ida[j] , caminho_ida[j+1])
    
    pares_ordenados_volta = []
    valor_roteiro_volta = 0
    subgrafo_volta = nx.DiGraph()
    for j in range(len(caminho_volta) - 1):
        pares_ordenados_volta.append((caminho_volta[j] , caminho_volta[j+1]))
        valor_roteiro_volta = valor_roteiro_volta + G[pares_ordenados_volta[-1][0]][pares_ordenados_volta[-1][1]]['DISTANCIA']
        subgrafo_volta.add_edge(caminho_volta[j] , caminho_volta[j+1])
    
    valor_roteiro_total = valor_roteiro_ida + valor_roteiro_volta
    valor_medio_roteiro_total = 0.5 * valor_roteiro_total

    TEMPO_SOLO = (combinacoes_df.loc[i]['TEMPO_ACIO_DECOL'] + combinacoes_df.loc[i]['TEMPO_POUSADOPLATAFORMA'] + combinacoes_df.loc[i]['TEMPO_POUSOCORTE']) / 60
    combinacoes_df.at[i, 'TEMPO_SOLO'] = TEMPO_SOLO

    TEMPO_SUBIDA = (combinacoes_df.loc[i]['TETO_CRUZEIRO'] / combinacoes_df.loc[i]['RAZAO_SUBIDA']) / 60
    combinacoes_df.at[i, 'TEMPO_SUBIDA'] = TEMPO_SUBIDA

    TEMPO_DESCIDA = (combinacoes_df.loc[i]['TETO_CRUZEIRO'] / combinacoes_df.loc[i]['RAZAO_DESCIDA']) / 60
    combinacoes_df.at[i, 'TEMPO_DESCIDA'] = TEMPO_DESCIDA

    ACELERACAO_SUBIDA = combinacoes_df.loc[i]['VELOCIDADE_CRUZEIRO'] / TEMPO_SUBIDA
    combinacoes_df.at[i, 'ACELERACAO_SUBIDA'] = ACELERACAO_SUBIDA

    ACELERACAO_DESCIDA = - (combinacoes_df.loc[i]['VELOCIDADE_CRUZEIRO'] / TEMPO_DESCIDA)
    combinacoes_df.at[i, 'ACELERACAO_DESCIDA'] = ACELERACAO_DESCIDA

    DISTANCIA_SUBIDA = ACELERACAO_SUBIDA * (TEMPO_SUBIDA ** 2 / 2)
    combinacoes_df.at[i, 'DISTANCIA_SUBIDA'] = DISTANCIA_SUBIDA

    DISTANCIA_DESCIDA = - ACELERACAO_DESCIDA * (TEMPO_DESCIDA ** 2 / 2)
    combinacoes_df.at[i, 'DISTANCIA_DESCIDA'] = DISTANCIA_DESCIDA

    DISTANCIA_CRUZEIRO = valor_medio_roteiro_total - DISTANCIA_SUBIDA - DISTANCIA_DESCIDA
    combinacoes_df.at[i, 'DISTANCIA_CRUZEIRO'] = DISTANCIA_CRUZEIRO

    TEMPO_CRUZEIRO = DISTANCIA_CRUZEIRO / combinacoes_df.loc[i]['VELOCIDADE_CRUZEIRO']
    combinacoes_df.at[i, 'TEMPO_CRUZEIRO'] = TEMPO_CRUZEIRO

    TEMPO_IDA = TEMPO_SUBIDA + TEMPO_DESCIDA + TEMPO_CRUZEIRO
    combinacoes_df.at[i, 'TEMPO_IDA'] = TEMPO_IDA

    TEMPO_VOLTA = TEMPO_IDA
    combinacoes_df.at[i, 'TEMPO_VOLTA'] = TEMPO_VOLTA

    TEMPO_VOO = TEMPO_IDA + TEMPO_VOLTA + combinacoes_df.loc[i]['TEMPO_CIRCUITO'] / 60
    combinacoes_df.at[i, 'TEMPO_VOO'] = TEMPO_VOO

    COMB_MISSAO = TEMPO_VOO * combinacoes_df.loc[i]['CONSUMO_VOO'] + TEMPO_SOLO * combinacoes_df.loc[i]['CONSUMO_SOLO']
    combinacoes_df.at[i, 'COMB_MISSAO'] = COMB_MISSAO

    TEMPO_MISSAO = TEMPO_VOO + TEMPO_SOLO
    combinacoes_df.at[i, 'TEMPO_MISSAO'] = TEMPO_MISSAO

    COMB_RESERVA = (max(0.5, 1/3 + 0.1 * TEMPO_MISSAO)) * combinacoes_df.loc[i]['CONSUMO_VOO']
    combinacoes_df.at[i, 'COMB_RESERVA'] = COMB_RESERVA    
    
    COMBUSTIVEL = COMB_MISSAO + COMB_RESERVA
    combinacoes_df.at[i, 'COMBUSTIVEL'] = COMBUSTIVEL    
    
    PAYLOAD = combinacoes_df.loc[i]['PMD'] - combinacoes_df.loc[i]['PBO'] - COMBUSTIVEL
    combinacoes_df.at[i, 'PAYLOAD'] = PAYLOAD    
    
    QUANT_PAX = math.ceil(min(combinacoes_df.loc[i]['CAPACIDADE_PAX'], PAYLOAD / combinacoes_df.loc[i]['PESO_PAX']))
    combinacoes_df.at[i, 'QUANT_PAX'] = QUANT_PAX
    
    combinacoes_df.at[i, 'valor_medio_roteiro_total'] = valor_medio_roteiro_total 
       
    combinacoes_df.at[i, 'CUSTO_HORA_VOADA'] = combinacoes_df.loc[i]['PRECO_HORA_VOADA'] * combinacoes_df.loc[i]['TEMPO_VOO']
    
    combinacoes_df.at[i, 'CUSTO_QAV_CONSUMIDO'] = combinacoes_df.loc[i]['PRECO_QAV'] * combinacoes_df.loc[i]['COMB_MISSAO'] / 0.79 #PARA PASSAR DE KG PARA LITROS. O PREÇO DO QAV ADOTADO FOI EM R$ / LITROS   
    
    combinacoes_df.at[i, 'CUSTO_MISSAO'] = combinacoes_df.loc[i]['CUSTO_HORA_VOADA'] + combinacoes_df.loc[i]['CUSTO_QAV_CONSUMIDO']

combinacoes_df.to_excel(f"OUTPUT_{cenario}.xlsx")

print('- = - PLANILHA SALVA NO DIRETORIO - = - ')

###########################################################
# =============================================================================
# # enviar e-mail
# 
# # criar a integração com o Outlook
# outlook = win32.Dispatch('outlook.application')
# 
# # criar um e-mail
# email = outlook.CreateItem(0)
# 
# # configurar as informações do seu e-mail
# 
# email.To = 'seuemail@xxxxx.com.br; seuemail@xxxxx.com.br'
# 
# email.CC = 'seuemail@xxxxx.com.br; seuemail@xxxxx.com.br'
# 
# email.BCC = 'seuemail@xxxxx.com.br; seuemail@xxxxx.com.br'
# 
# email.Subject = f'Planejamento Tabelão'
# 
# email.HTMLBody = f'''
# <p>Prezado(a) esta é uma mensagem automática do Gerador de Prévia de Voo OffshoreBS.</p>
# <p>Segue anexo o planejamento Tabelão.</p>
# <p>Atenciosamente,</p>
# <p><b>Equipe Gerador de Prévia de Voo OffshoreBS</b></p>
# '''
# 
# anexo1 = f'C:/Users/kk3f/Desktop/Gerador de Tabelas/{OUTPUT_{cenario}.xlsx}'
# 
# email.Attachments.Add(anexo1)
# 
# email.Send()
# 
# print('E-mail enviado')
# =============================================================================



