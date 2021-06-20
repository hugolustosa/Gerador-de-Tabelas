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

tabelao = 'INPUT_para_tabelao_qav_5.00_reais_todas_bases.xlsx'

arestas_df = pd.read_excel(tabelao, sheet_name = 'arestas')

vertices_df = pd.read_excel(tabelao, sheet_name = 'vertices')

combinacoes_df = pd.read_excel(tabelao, sheet_name = 'aeronaves_roteiros')


origem = 'sbjr'
destino = 'fpso_itaguai'
pouso_final = 'sbjr'

########################################################### 

G = nx.from_pandas_edgelist(arestas_df, source='ORIGEM', target='DESTINO', edge_attr='DISTANCIA', create_using=nx.DiGraph())

#POSIÇÃO DOS NÓS NAS COORDENADAS
for i in vertices_df.index:
    G.add_node(vertices_df['PONTO'][i], pos = (vertices_df['LONG'][i] , vertices_df['LAT'][i]))


########################################################### 
#DADOS PARA CÁLCULO DE DISPONÍVEL, TEMPO E VOO E CONSUMO DE QAV
    
peso_pax = 107 # em kg

PMD_GP = 26500 # em lb considerado S92
PMD_SMP = 7800 # em kg considerado H175
PMD_MP = 7000 # em kg considerado AW139

PBO_GP = 18115 # em lb considerado S92
PBO_SMP = 4976 # em kg considerado H175
PBO_MP = 4680 # em kg considerado AW139

CONSUMO_VOO_GP = 1350 # em lb/h
CONSUMO_VOO_SMP = 450 # em kg/h (a confirmar)
CONSUMO_VOO_MP = 400 # em kg/h

CONSUMO_SOLO_GP = 675 # em lb/h
CONSUMO_SOLO_SMP = 380 # em kg/h (a confirmar)
CONSUMO_SOLO_MP = 320 # em kg/h

TEMPO_ACIO_DECOL_GP = 11 # em min
TEMPO_ACIO_DECOL_SMP = 11 # em min
TEMPO_ACIO_DECOL_MP = 11 # em min

TEMPO_POUSADOPLATAFORMA_GP = 10 # em min
TEMPO_POUSADOPLATAFORMA_SMP = 9 # em min
TEMPO_POUSADOPLATAFORMA_MP = 8 # em min

TEMPO_POUSOCORTE_GP = 6 # em min
TEMPO_POUSOCORTE_SMP = 6 # em min
TEMPO_POUSOCORTE_MP = 6 # em min

TEMPO_CIRCUITO_GP = 4 # em min
TEMPO_CIRCUITO_SMP = 4 # em min
TEMPO_CIRCUITO_MP = 4 # em min

TETO_CRUZEIRO_GP = 3000 # em pés
TETO_CRUZEIRO_SMP = 3000 # em pés
TETO_CRUZEIRO_MP = 3000 # em pés

RAZAO_SUBIDA_GP = 800 # em pés/min
RAZAO_SUBIDA_SMP = 800 # em pés/min
RAZAO_SUBIDA_MP = 800 # em pés/min

RAZAO_DESCIDA_GP = 500 # em pés/min
RAZAO_DESCIDA_SMP = 500 # em pés/min
RAZAO_DESCIDA_MP = 500 # em pés/min

VELOCIDADE_CRUZEIRO_GP = 145 # em nós
VELOCIDADE_CRUZEIRO_SMP = 150 # em nós
VELOCIDADE_CRUZEIRO_MP = 155 # em nós


########################################################### 

origem = origem.upper()
destino = destino.upper()
pouso_final = pouso_final.upper()


caminho_ida = nx.shortest_path(G, source = origem, target = destino, weight='DISTANCIA', method='dijkstra')

caminho_volta = nx.shortest_path(G, source = destino, target = pouso_final, weight='DISTANCIA', method='dijkstra')

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

roteiro_volta = []
valor_roteiro_volta = 0
subgrafo_volta = nx.DiGraph()
for i in range(len(caminho_volta) - 1):
    roteiro_volta.append((caminho_volta[i] , caminho_volta[i+1]))
    valor_roteiro_volta = valor_roteiro_volta + G[roteiro_volta[-1][0]][roteiro_volta[-1][1]]['DISTANCIA']
    subgrafo_volta.add_edge(caminho_volta[i] , caminho_volta[i+1])


valor_roteiro_total = valor_roteiro_ida + valor_roteiro_volta
valor_medio_roteiro_total = 0.5 * valor_roteiro_total


print('-='*30)
print('Caminho mais curto ida:', caminho_ida)
print(f'Distancia do caminho ida = {valor_roteiro_ida:.2f} mn')

print('Caminho mais curto volta:', caminho_volta)
print(f'Distancia do caminho volta = {valor_roteiro_volta:.2f} mn')

print('Caminho mais curto ida e volta:', caminho_ida[0:-1] + caminho_volta)

print(f'Distancia do caminho ida e volta = {valor_roteiro_total:.2f} mn')
print(f'Distancia media do caminho = {valor_medio_roteiro_total:.2f} mn')


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

print('QUANT_PAX_GP = ', QUANT_PAX_GP)
print('QUANT_PAX_SMP = ', QUANT_PAX_SMP)
print('QUANT_PAX_MP = ', QUANT_PAX_MP)

print('TEMPO_MISSAO_GP = ', f'{TEMPO_MISSAO_GP:.2f} h')
print('TEMPO_MISSAO_SMP = ', f'{TEMPO_MISSAO_SMP:.2f} h')
print('TEMPO_MISSAO_MP = ', f'{TEMPO_MISSAO_MP:.2f} h')

########################################################### 
# draw graph

plt.axes([0.1, 0.1, 0.5, 0.83])

plt.axis("off")

plt.title(f'ROTEIRO: {origem} -> {destino} -> {pouso_final}', fontsize=5)

plt.text(-45, -21.8, '#### Planejamento deverá ser confirmado com a cia. aérea que utilizará os dados reais da aeronave ####', fontsize=3)

plt.text(-45, -23.2, f'Distancia total: {valor_roteiro_total:.2f} mn', fontsize=3)

plt.text(-45, -23.27, f'Distancia media: {valor_medio_roteiro_total:.2f} mn', fontsize=3)

plt.text(-45, -23.34, f'# pax embarque GP: {QUANT_PAX_GP:.1f} pax', fontsize=3)

plt.text(-45, -23.41, f'# pax embarque SMP: {QUANT_PAX_SMP:.1f} pax', fontsize=3)

plt.text(-45, -23.48, f'# pax embarque MP: {QUANT_PAX_MP:.1f} pax (PMD: {PMD_MP} kg)', fontsize=3)

plt.text(-45, -23.55, f'Tempo missão GP: {TEMPO_MISSAO_GP:.2f} h', fontsize=3)

plt.text(-45, -23.62, f'Tempo missão SMP: {TEMPO_MISSAO_SMP:.2f} h', fontsize=3)

plt.text(-45, -23.69, f'Tempo missão MP: {TEMPO_MISSAO_MP:.2f} h', fontsize=3)

plt.text(-45.2, -26.1, f'Ida: {caminho_ida} -> {valor_roteiro_ida:.2f} mn', fontsize=3)

plt.text(-45.2, -26.17, f'Volta: {caminho_volta} -> {valor_roteiro_volta:.2f} mn', fontsize=3)


nx.draw_networkx_nodes(G,
                       pos = nx.get_node_attributes(G, 'pos'),
                       node_size = 0.05,
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
                        font_size = 2,
                        alpha = 0.3)


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

nx.draw_networkx_labels(subgrafo_volta,
                        pos = nx.get_node_attributes(G, 'pos'),
                        font_size = 2,
                        alpha = 1)


plt.savefig(f'Roteiro {origem} - {destino} - {pouso_final}.pdf',
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

###########################################################
# enviar e-mail
# =============================================================================
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
# email.Subject = f'Planejamento Roteiro: {origem} -> {destino} -> {pouso_final}'
# 
# email.HTMLBody = f'''
# <p>Prezado(a) esta é uma mensagem automática do Gerador de Prévia de Voo OffshoreBS.</p>
# <p>Segue anexo o planejamento do Roteiro: <u>{origem} -> {destino} -> {pouso_final}</u>.</p>
# <p>Atenciosamente,</p>
# <p><b>Equipe Gerador de Prévia de Voo OffshoreBS</b></p>
# '''
# 
# anexo1 = f'C:/Users/kk3f/Desktop/Gerador de Tabelas/Roteiro {origem} - {destino} - {pouso_final}.pdf'
# 
# email.Attachments.Add(anexo1)
# 
# email.Send()
# 
# print('E-mail enviado')
# =============================================================================



