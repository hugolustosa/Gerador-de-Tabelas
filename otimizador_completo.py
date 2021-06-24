import time
from pulp import *
import numpy as np
import pandas as pd
import math
import networkx as nx
import win32com.client as win32

antes = time.time()

########################################################### 
#DADOS DE ENTRADA

cenario_geral = 1
# 1 / 2 / 3 / 4 / 4.1 (SEM RESTRIÇÕES) / 5 / 6

cen_preco_qav = '5.00' # 5.00 / 4.50 / 4.00

cen_base_qav = 'todas_bases' # todas_bases / SBJR / SBMI / SBCB / todas_bases_sem_aerovias

cenario_qav = f'{cen_base_qav}_{cen_preco_qav}_reais'


cenario = f'Cenario_qav_{cen_preco_qav}_reais_{cen_base_qav}'

entrada = f'INPUT_para_tabelao_qav_{cen_preco_qav}_reais_{cen_base_qav}.xlsx'

arestas_df = pd.read_excel(entrada, sheet_name = 'arestas')

vertices_df = pd.read_excel(entrada, sheet_name = 'vertices')

output_df = pd.read_excel(entrada, sheet_name = 'aeronaves_roteiros')


DISPONIBILIDADE = 0.92
FATOR_DE_RECUPERACAO = 5 # DIAS
GIRO_MAXIMO_BASE1 = 3 # VOOS / DIA
GIRO_MAXIMO_BASE2 = 3 # VOOS / DIA
GIRO_MAXIMO_BASE3 = 3 # VOOS / DIA
GIRO_MAXIMO_BASE4 = 3 # VOOS / DIA

##################################

if cenario_geral == 1:
    base1_cap_mp = 20
    base2_cap_mp = 10
    base3_cap_mp = 20
    base4_cap_mp = 0
    
    base1_cap_gp = 15
    base2_cap_gp = 10
    base3_cap_gp = 15
    base4_cap_gp = 0
    
    base1_cap_total = 26
    base2_cap_total = 15
    base3_cap_total = 26
    base4_cap_total = 0
    
elif cenario_geral == 2:
    base1_cap_mp = 20
    base2_cap_mp = 0
    base3_cap_mp = 20
    base4_cap_mp = 0
    
    base1_cap_gp = 15
    base2_cap_gp = 0
    base3_cap_gp = 15
    base4_cap_gp = 0
    
    base1_cap_total = 26
    base2_cap_total = 0
    base3_cap_total = 26
    base4_cap_total = 0 

elif cenario_geral == 3:
    base1_cap_mp = 20
    base2_cap_mp = 10
    base3_cap_mp = 0
    base4_cap_mp = 0
    
    base1_cap_gp = 15
    base2_cap_gp = 10
    base3_cap_gp = 0
    base4_cap_gp = 0
    
    base1_cap_total = 26
    base2_cap_total = 15
    base3_cap_total = 0
    base4_cap_total = 0         

elif cenario_geral == 4:
    base1_cap_mp = 0
    base2_cap_mp = 10
    base3_cap_mp = 20
    base4_cap_mp = 0
    
    base1_cap_gp = 0
    base2_cap_gp = 10
    base3_cap_gp = 15
    base4_cap_gp = 0
    
    base1_cap_total = 0
    base2_cap_total = 15
    base3_cap_total = 26
    base4_cap_total = 0         
    
elif cenario_geral == 4.1: #igual ao cenário 4 mas sem restrições de capacidade
    base1_cap_mp = 0
    base2_cap_mp = 999
    base3_cap_mp = 999
    base4_cap_mp = 0
    
    base1_cap_gp = 0
    base2_cap_gp = 999
    base3_cap_gp = 999
    base4_cap_gp = 0
    
    base1_cap_total = 0
    base2_cap_total = 999
    base3_cap_total = 999
    base4_cap_total = 0   
    
elif cenario_geral == 5:
    base1_cap_mp = 20
    base2_cap_mp = 0
    base3_cap_mp = 0
    base4_cap_mp = 99
    
    base1_cap_gp = 15
    base2_cap_gp = 0
    base3_cap_gp = 0
    base4_cap_gp = 99
    
    base1_cap_total = 26
    base2_cap_total = 0
    base3_cap_total =0
    base4_cap_total = 99  

elif cenario_geral == 6:
    base1_cap_mp = 999
    base2_cap_mp = 999
    base3_cap_mp = 999
    base4_cap_mp = 0
    
    base1_cap_gp = 999
    base2_cap_gp = 999
    base3_cap_gp = 999
    base4_cap_gp = 0
    
    base1_cap_total = 999
    base2_cap_total = 999
    base3_cap_total = 999
    base4_cap_total = 0



########################################################### 

G = nx.from_pandas_edgelist(arestas_df, 
                            source='ORIGEM', 
                            target='DESTINO', 
                            edge_attr='DISTANCIA', 
                            create_using=nx.DiGraph())


for i in vertices_df.index:
    G.add_node(vertices_df['PONTO'][i], pos = (vertices_df['LONG'][i] , vertices_df['LAT'][i]))


for i in output_df.index:
    origem = output_df.loc[i]['ORIGEM']
    destino = output_df.loc[i]['DESTINO']
    pouso_final = output_df.loc[i]['POUSO_FINAL']
     
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

    TEMPO_SOLO = (output_df.loc[i]['TEMPO_ACIO_DECOL'] + output_df.loc[i]['TEMPO_POUSADOPLATAFORMA'] + output_df.loc[i]['TEMPO_POUSOCORTE']) / 60
    output_df.at[i, 'TEMPO_SOLO'] = TEMPO_SOLO

    TEMPO_SUBIDA = (output_df.loc[i]['TETO_CRUZEIRO'] / output_df.loc[i]['RAZAO_SUBIDA']) / 60
    output_df.at[i, 'TEMPO_SUBIDA'] = TEMPO_SUBIDA

    TEMPO_DESCIDA = (output_df.loc[i]['TETO_CRUZEIRO'] / output_df.loc[i]['RAZAO_DESCIDA']) / 60
    output_df.at[i, 'TEMPO_DESCIDA'] = TEMPO_DESCIDA

    ACELERACAO_SUBIDA = output_df.loc[i]['VELOCIDADE_CRUZEIRO'] / TEMPO_SUBIDA
    output_df.at[i, 'ACELERACAO_SUBIDA'] = ACELERACAO_SUBIDA

    ACELERACAO_DESCIDA = - (output_df.loc[i]['VELOCIDADE_CRUZEIRO'] / TEMPO_DESCIDA)
    output_df.at[i, 'ACELERACAO_DESCIDA'] = ACELERACAO_DESCIDA

    DISTANCIA_SUBIDA = ACELERACAO_SUBIDA * (TEMPO_SUBIDA ** 2 / 2)
    output_df.at[i, 'DISTANCIA_SUBIDA'] = DISTANCIA_SUBIDA

    DISTANCIA_DESCIDA = - ACELERACAO_DESCIDA * (TEMPO_DESCIDA ** 2 / 2)
    output_df.at[i, 'DISTANCIA_DESCIDA'] = DISTANCIA_DESCIDA

    DISTANCIA_CRUZEIRO = valor_medio_roteiro_total - DISTANCIA_SUBIDA - DISTANCIA_DESCIDA
    output_df.at[i, 'DISTANCIA_CRUZEIRO'] = DISTANCIA_CRUZEIRO

    TEMPO_CRUZEIRO = DISTANCIA_CRUZEIRO / output_df.loc[i]['VELOCIDADE_CRUZEIRO']
    output_df.at[i, 'TEMPO_CRUZEIRO'] = TEMPO_CRUZEIRO

    TEMPO_IDA = TEMPO_SUBIDA + TEMPO_DESCIDA + TEMPO_CRUZEIRO
    output_df.at[i, 'TEMPO_IDA'] = TEMPO_IDA

    TEMPO_VOLTA = TEMPO_IDA
    output_df.at[i, 'TEMPO_VOLTA'] = TEMPO_VOLTA

    TEMPO_VOO = TEMPO_IDA + TEMPO_VOLTA + output_df.loc[i]['TEMPO_CIRCUITO'] / 60
    output_df.at[i, 'TEMPO_VOO'] = TEMPO_VOO

    COMB_MISSAO = TEMPO_VOO * output_df.loc[i]['CONSUMO_VOO'] + TEMPO_SOLO * output_df.loc[i]['CONSUMO_SOLO']
    output_df.at[i, 'COMB_MISSAO'] = COMB_MISSAO

    TEMPO_MISSAO = TEMPO_VOO + TEMPO_SOLO
    output_df.at[i, 'TEMPO_MISSAO'] = TEMPO_MISSAO
    
    TEMPO_DECOLAGEM_POUSO = TEMPO_MISSAO - (output_df.loc[i]['TEMPO_ACIO_DECOL'] + output_df.loc[i]['TEMPO_POUSOCORTE'])/ 60
    output_df.at[i, 'TEMPO_DECOLAGEM_POUSO'] = TEMPO_DECOLAGEM_POUSO

    COMB_RESERVA = (max(0.5, 1/3 + 0.1 * TEMPO_MISSAO)) * output_df.loc[i]['CONSUMO_VOO']
    output_df.at[i, 'COMB_RESERVA'] = COMB_RESERVA    
    
    COMBUSTIVEL = COMB_MISSAO + COMB_RESERVA
    output_df.at[i, 'COMBUSTIVEL'] = COMBUSTIVEL    
    
    PAYLOAD = output_df.loc[i]['PMD'] - output_df.loc[i]['PBO'] - COMBUSTIVEL
    output_df.at[i, 'PAYLOAD'] = PAYLOAD    
    
    QUANT_PAX = math.floor(min(output_df.loc[i]['CAPACIDADE_PAX'], PAYLOAD / output_df.loc[i]['PESO_PAX']))
    output_df.at[i, 'QUANT_PAX'] = QUANT_PAX
    
    output_df.at[i, 'valor_medio_roteiro_total'] = valor_medio_roteiro_total 
       
    output_df.at[i, 'CUSTO_HORA_VOADA'] = output_df.loc[i]['PRECO_HORA_VOADA'] * output_df.loc[i]['TEMPO_VOO']
    
    output_df.at[i, 'CUSTO_QAV_CONSUMIDO'] = output_df.loc[i]['PRECO_QAV'] * output_df.loc[i]['COMB_MISSAO'] / 0.79 #PARA PASSAR DE KG PARA LITROS. O PREÇO DO QAV ADOTADO FOI EM R$ / LITROS   
    
    output_df.at[i, 'CUSTO_MISSAO'] = output_df.loc[i]['CUSTO_HORA_VOADA'] + output_df.loc[i]['CUSTO_QAV_CONSUMIDO']

output_df.to_excel(f"OUTPUT_{cenario}.xlsx")

print(f'# PLANILHA OUTPUT_{cenario}.xlsx SALVA NO DIRETORIO #')

###################################################################
print('')
print('##### OTIMIZADOR ####')
print('')

# Cria o problema
prob = LpProblem("Otimizacao_Atendimento_Aereo", LpMinimize)

# Cria as variaveis (número de voos semanais decolando da base(i) para a UM(j) utilizando aeronave(k)). Lowerbound = 0
x1 = LpVariable("MP_PMLZ_1_base1", 0, cat='Integer')
x2 = LpVariable("MP_PMXL_1_base1", 0, cat='Integer')
x3 = LpVariable("MP_FPSO_ANGRA_DOS_REIS_base1", 0, cat='Integer')
x4 = LpVariable("MP_FPSO_ILHABELA_base1", 0, cat='Integer')
x5 = LpVariable("MP_FPSO_ITAGUAI_base1", 0, cat='Integer')
x6 = LpVariable("MP_FPSO_MANGARATIBA_base1", 0, cat='Integer')
x7 = LpVariable("MP_FPSO_MARICA_base1", 0, cat='Integer')
x8 = LpVariable("MP_FPSO_PARATY_base1", 0, cat='Integer')
x9 = LpVariable("MP_FPSO_PIONEIRO_DE_LIBRA_base1", 0, cat='Integer')
x10 = LpVariable("MP_FPSO_SANTOS_base1", 0, cat='Integer')
x11 = LpVariable("MP_FPSO_SAO_PAULO_base1", 0, cat='Integer')
x12 = LpVariable("MP_FPSO_SAQUAREMA_base1", 0, cat='Integer')
x13 = LpVariable("MP_NS_31_base1", 0, cat='Integer')
x14 = LpVariable("MP_NS_33_base1", 0, cat='Integer')
x15 = LpVariable("MP_NS_38_base1", 0, cat='Integer')
x16 = LpVariable("MP_NS_39_base1", 0, cat='Integer')
x17 = LpVariable("MP_NS_40_base1", 0, cat='Integer')
x18 = LpVariable("MP_NS_42_base1", 0, cat='Integer')
x19 = LpVariable("MP_NS_43_base1", 0, cat='Integer')
x20 = LpVariable("MP_NS_44_base1", 0, cat='Integer')
x21 = LpVariable("MP_P_66_base1", 0, cat='Integer')
x22 = LpVariable("MP_P_67_base1", 0, cat='Integer')
x23 = LpVariable("MP_P_68_base1", 0, cat='Integer')
x24 = LpVariable("MP_P_69_base1", 0, cat='Integer')
x25 = LpVariable("MP_P_70_base1", 0, cat='Integer')
x26 = LpVariable("MP_P_74_base1", 0, cat='Integer')
x27 = LpVariable("MP_P_75_base1", 0, cat='Integer')
x28 = LpVariable("MP_P_76_base1", 0, cat='Integer')
x29 = LpVariable("MP_P_77_base1", 0, cat='Integer')
x30 = LpVariable("MP_SS_75_base1", 0, cat='Integer')
x31 = LpVariable("MP_UMMA_base1", 0, cat='Integer')
x32 = LpVariable("MP_UMPA_base1", 0, cat='Integer')
x33 = LpVariable("MP_UMTJ_base1", 0, cat='Integer')
x34 = LpVariable("MP_UMVE_base1", 0, cat='Integer')
x35 = LpVariable("MP_SRIO_base1", 0, cat='Integer')
x36 = LpVariable("MP_SARU_base1", 0, cat='Integer')
x37 = LpVariable("MP_SAJA_base1", 0, cat='Integer')
x38 = LpVariable("MP_FASA_base1", 0, cat='Integer')
x39 = LpVariable("MP_SECR_base1", 0, cat='Integer')
x40 = LpVariable("MP_SAON_base1", 0, cat='Integer')
x41 = LpVariable("MP_SKST_base1", 0, cat='Integer')
x42 = LpVariable("MP_SKAU_base1", 0, cat='Integer')
x43 = LpVariable("MP_PMLZ_1_base2", 0, cat='Integer')
x44 = LpVariable("MP_PMXL_1_base2", 0, cat='Integer')
x45 = LpVariable("MP_FPSO_ANGRA_DOS_REIS_base2", 0, cat='Integer')
x46 = LpVariable("MP_FPSO_ILHABELA_base2", 0, cat='Integer')
x47 = LpVariable("MP_FPSO_ITAGUAI_base2", 0, cat='Integer')
x48 = LpVariable("MP_FPSO_MANGARATIBA_base2", 0, cat='Integer')
x49 = LpVariable("MP_FPSO_MARICA_base2", 0, cat='Integer')
x50 = LpVariable("MP_FPSO_PARATY_base2", 0, cat='Integer')
x51 = LpVariable("MP_FPSO_PIONEIRO_DE_LIBRA_base2", 0, cat='Integer')
x52 = LpVariable("MP_FPSO_SANTOS_base2", 0, cat='Integer')
x53 = LpVariable("MP_FPSO_SAO_PAULO_base2", 0, cat='Integer')
x54 = LpVariable("MP_FPSO_SAQUAREMA_base2", 0, cat='Integer')
x55 = LpVariable("MP_NS_31_base2", 0, cat='Integer')
x56 = LpVariable("MP_NS_33_base2", 0, cat='Integer')
x57 = LpVariable("MP_NS_38_base2", 0, cat='Integer')
x58 = LpVariable("MP_NS_39_base2", 0, cat='Integer')
x59 = LpVariable("MP_NS_40_base2", 0, cat='Integer')
x60 = LpVariable("MP_NS_42_base2", 0, cat='Integer')
x61 = LpVariable("MP_NS_43_base2", 0, cat='Integer')
x62 = LpVariable("MP_NS_44_base2", 0, cat='Integer')
x63 = LpVariable("MP_P_66_base2", 0, cat='Integer')
x64 = LpVariable("MP_P_67_base2", 0, cat='Integer')
x65 = LpVariable("MP_P_68_base2", 0, cat='Integer')
x66 = LpVariable("MP_P_69_base2", 0, cat='Integer')
x67 = LpVariable("MP_P_70_base2", 0, cat='Integer')
x68 = LpVariable("MP_P_74_base2", 0, cat='Integer')
x69 = LpVariable("MP_P_75_base2", 0, cat='Integer')
x70 = LpVariable("MP_P_76_base2", 0, cat='Integer')
x71 = LpVariable("MP_P_77_base2", 0, cat='Integer')
x72 = LpVariable("MP_SS_75_base2", 0, cat='Integer')
x73 = LpVariable("MP_UMMA_base2", 0, cat='Integer')
x74 = LpVariable("MP_UMPA_base2", 0, cat='Integer')
x75 = LpVariable("MP_UMTJ_base2", 0, cat='Integer')
x76 = LpVariable("MP_UMVE_base2", 0, cat='Integer')
x77 = LpVariable("MP_SRIO_base2", 0, cat='Integer')
x78 = LpVariable("MP_SARU_base2", 0, cat='Integer')
x79 = LpVariable("MP_SAJA_base2", 0, cat='Integer')
x80 = LpVariable("MP_FASA_base2", 0, cat='Integer')
x81 = LpVariable("MP_SECR_base2", 0, cat='Integer')
x82 = LpVariable("MP_SAON_base2", 0, cat='Integer')
x83 = LpVariable("MP_SKST_base2", 0, cat='Integer')
x84 = LpVariable("MP_SKAU_base2", 0, cat='Integer')
x85 = LpVariable("MP_PMLZ_1_base3", 0, cat='Integer')
x86 = LpVariable("MP_PMXL_1_base3", 0, cat='Integer')
x87 = LpVariable("MP_FPSO_ANGRA_DOS_REIS_base3", 0, cat='Integer')
x88 = LpVariable("MP_FPSO_ILHABELA_base3", 0, cat='Integer')
x89 = LpVariable("MP_FPSO_ITAGUAI_base3", 0, cat='Integer')
x90 = LpVariable("MP_FPSO_MANGARATIBA_base3", 0, cat='Integer')
x91 = LpVariable("MP_FPSO_MARICA_base3", 0, cat='Integer')
x92 = LpVariable("MP_FPSO_PARATY_base3", 0, cat='Integer')
x93 = LpVariable("MP_FPSO_PIONEIRO_DE_LIBRA_base3", 0, cat='Integer')
x94 = LpVariable("MP_FPSO_SANTOS_base3", 0, cat='Integer')
x95 = LpVariable("MP_FPSO_SAO_PAULO_base3", 0, cat='Integer')
x96 = LpVariable("MP_FPSO_SAQUAREMA_base3", 0, cat='Integer')
x97 = LpVariable("MP_NS_31_base3", 0, cat='Integer')
x98 = LpVariable("MP_NS_33_base3", 0, cat='Integer')
x99 = LpVariable("MP_NS_38_base3", 0, cat='Integer')
x100 = LpVariable("MP_NS_39_base3", 0, cat='Integer')
x101 = LpVariable("MP_NS_40_base3", 0, cat='Integer')
x102 = LpVariable("MP_NS_42_base3", 0, cat='Integer')
x103 = LpVariable("MP_NS_43_base3", 0, cat='Integer')
x104 = LpVariable("MP_NS_44_base3", 0, cat='Integer')
x105 = LpVariable("MP_P_66_base3", 0, cat='Integer')
x106 = LpVariable("MP_P_67_base3", 0, cat='Integer')
x107 = LpVariable("MP_P_68_base3", 0, cat='Integer')
x108 = LpVariable("MP_P_69_base3", 0, cat='Integer')
x109 = LpVariable("MP_P_70_base3", 0, cat='Integer')
x110 = LpVariable("MP_P_74_base3", 0, cat='Integer')
x111 = LpVariable("MP_P_75_base3", 0, cat='Integer')
x112 = LpVariable("MP_P_76_base3", 0, cat='Integer')
x113 = LpVariable("MP_P_77_base3", 0, cat='Integer')
x114 = LpVariable("MP_SS_75_base3", 0, cat='Integer')
x115 = LpVariable("MP_UMMA_base3", 0, cat='Integer')
x116 = LpVariable("MP_UMPA_base3", 0, cat='Integer')
x117 = LpVariable("MP_UMTJ_base3", 0, cat='Integer')
x118 = LpVariable("MP_UMVE_base3", 0, cat='Integer')
x119 = LpVariable("MP_SRIO_base3", 0, cat='Integer')
x120 = LpVariable("MP_SARU_base3", 0, cat='Integer')
x121 = LpVariable("MP_SAJA_base3", 0, cat='Integer')
x122 = LpVariable("MP_FASA_base3", 0, cat='Integer')
x123 = LpVariable("MP_SECR_base3", 0, cat='Integer')
x124 = LpVariable("MP_SAON_base3", 0, cat='Integer')
x125 = LpVariable("MP_SKST_base3", 0, cat='Integer')
x126 = LpVariable("MP_SKAU_base3", 0, cat='Integer')
x127 = LpVariable("MP_PMLZ_1_base4", 0, cat='Integer')
x128 = LpVariable("MP_PMXL_1_base4", 0, cat='Integer')
x129 = LpVariable("MP_FPSO_ANGRA_DOS_REIS_base4", 0, cat='Integer')
x130 = LpVariable("MP_FPSO_ILHABELA_base4", 0, cat='Integer')
x131 = LpVariable("MP_FPSO_ITAGUAI_base4", 0, cat='Integer')
x132 = LpVariable("MP_FPSO_MANGARATIBA_base4", 0, cat='Integer')
x133 = LpVariable("MP_FPSO_MARICA_base4", 0, cat='Integer')
x134 = LpVariable("MP_FPSO_PARATY_base4", 0, cat='Integer')
x135 = LpVariable("MP_FPSO_PIONEIRO_DE_LIBRA_base4", 0, cat='Integer')
x136 = LpVariable("MP_FPSO_SANTOS_base4", 0, cat='Integer')
x137 = LpVariable("MP_FPSO_SAO_PAULO_base4", 0, cat='Integer')
x138 = LpVariable("MP_FPSO_SAQUAREMA_base4", 0, cat='Integer')
x139 = LpVariable("MP_NS_31_base4", 0, cat='Integer')
x140 = LpVariable("MP_NS_33_base4", 0, cat='Integer')
x141 = LpVariable("MP_NS_38_base4", 0, cat='Integer')
x142 = LpVariable("MP_NS_39_base4", 0, cat='Integer')
x143 = LpVariable("MP_NS_40_base4", 0, cat='Integer')
x144 = LpVariable("MP_NS_42_base4", 0, cat='Integer')
x145 = LpVariable("MP_NS_43_base4", 0, cat='Integer')
x146 = LpVariable("MP_NS_44_base4", 0, cat='Integer')
x147 = LpVariable("MP_P_66_base4", 0, cat='Integer')
x148 = LpVariable("MP_P_67_base4", 0, cat='Integer')
x149 = LpVariable("MP_P_68_base4", 0, cat='Integer')
x150 = LpVariable("MP_P_69_base4", 0, cat='Integer')
x151 = LpVariable("MP_P_70_base4", 0, cat='Integer')
x152 = LpVariable("MP_P_74_base4", 0, cat='Integer')
x153 = LpVariable("MP_P_75_base4", 0, cat='Integer')
x154 = LpVariable("MP_P_76_base4", 0, cat='Integer')
x155 = LpVariable("MP_P_77_base4", 0, cat='Integer')
x156 = LpVariable("MP_SS_75_base4", 0, cat='Integer')
x157 = LpVariable("MP_UMMA_base4", 0, cat='Integer')
x158 = LpVariable("MP_UMPA_base4", 0, cat='Integer')
x159 = LpVariable("MP_UMTJ_base4", 0, cat='Integer')
x160 = LpVariable("MP_UMVE_base4", 0, cat='Integer')
x161 = LpVariable("MP_SRIO_base4", 0, cat='Integer')
x162 = LpVariable("MP_SARU_base4", 0, cat='Integer')
x163 = LpVariable("MP_SAJA_base4", 0, cat='Integer')
x164 = LpVariable("MP_FASA_base4", 0, cat='Integer')
x165 = LpVariable("MP_SECR_base4", 0, cat='Integer')
x166 = LpVariable("MP_SAON_base4", 0, cat='Integer')
x167 = LpVariable("MP_SKST_base4", 0, cat='Integer')
x168 = LpVariable("MP_SKAU_base4", 0, cat='Integer')
x169 = LpVariable("GP_PMLZ_1_base1", 0, cat='Integer')
x170 = LpVariable("GP_PMXL_1_base1", 0, cat='Integer')
x171 = LpVariable("GP_FPSO_ANGRA_DOS_REIS_base1", 0, cat='Integer')
x172 = LpVariable("GP_FPSO_ILHABELA_base1", 0, cat='Integer')
x173 = LpVariable("GP_FPSO_ITAGUAI_base1", 0, cat='Integer')
x174 = LpVariable("GP_FPSO_MANGARATIBA_base1", 0, cat='Integer')
x175 = LpVariable("GP_FPSO_MARICA_base1", 0, cat='Integer')
x176 = LpVariable("GP_FPSO_PARATY_base1", 0, cat='Integer')
x177 = LpVariable("GP_FPSO_PIONEIRO_DE_LIBRA_base1", 0, cat='Integer')
x178 = LpVariable("GP_FPSO_SANTOS_base1", 0, cat='Integer')
x179 = LpVariable("GP_FPSO_SAO_PAULO_base1", 0, cat='Integer')
x180 = LpVariable("GP_FPSO_SAQUAREMA_base1", 0, cat='Integer')
x181 = LpVariable("GP_NS_31_base1", 0, cat='Integer')
x182 = LpVariable("GP_NS_33_base1", 0, cat='Integer')
x183 = LpVariable("GP_NS_38_base1", 0, cat='Integer')
x184 = LpVariable("GP_NS_39_base1", 0, cat='Integer')
x185 = LpVariable("GP_NS_40_base1", 0, cat='Integer')
x186 = LpVariable("GP_NS_42_base1", 0, cat='Integer')
x187 = LpVariable("GP_NS_43_base1", 0, cat='Integer')
x188 = LpVariable("GP_NS_44_base1", 0, cat='Integer')
x189 = LpVariable("GP_P_66_base1", 0, cat='Integer')
x190 = LpVariable("GP_P_67_base1", 0, cat='Integer')
x191 = LpVariable("GP_P_68_base1", 0, cat='Integer')
x192 = LpVariable("GP_P_69_base1", 0, cat='Integer')
x193 = LpVariable("GP_P_70_base1", 0, cat='Integer')
x194 = LpVariable("GP_P_74_base1", 0, cat='Integer')
x195 = LpVariable("GP_P_75_base1", 0, cat='Integer')
x196 = LpVariable("GP_P_76_base1", 0, cat='Integer')
x197 = LpVariable("GP_P_77_base1", 0, cat='Integer')
x198 = LpVariable("GP_SS_75_base1", 0, cat='Integer')
x199 = LpVariable("GP_UMMA_base1", 0, cat='Integer')
x200 = LpVariable("GP_UMPA_base1", 0, cat='Integer')
x201 = LpVariable("GP_UMTJ_base1", 0, cat='Integer')
x202 = LpVariable("GP_UMVE_base1", 0, cat='Integer')
x203 = LpVariable("GP_SRIO_base1", 0, cat='Integer')
x204 = LpVariable("GP_SARU_base1", 0, cat='Integer')
x205 = LpVariable("GP_SAJA_base1", 0, cat='Integer')
x206 = LpVariable("GP_FASA_base1", 0, cat='Integer')
x207 = LpVariable("GP_SECR_base1", 0, cat='Integer')
x208 = LpVariable("GP_SAON_base1", 0, cat='Integer')
x209 = LpVariable("GP_SKST_base1", 0, cat='Integer')
x210 = LpVariable("GP_SKAU_base1", 0, cat='Integer')
x211 = LpVariable("GP_PMLZ_1_base2", 0, cat='Integer')
x212 = LpVariable("GP_PMXL_1_base2", 0, cat='Integer')
x213 = LpVariable("GP_FPSO_ANGRA_DOS_REIS_base2", 0, cat='Integer')
x214 = LpVariable("GP_FPSO_ILHABELA_base2", 0, cat='Integer')
x215 = LpVariable("GP_FPSO_ITAGUAI_base2", 0, cat='Integer')
x216 = LpVariable("GP_FPSO_MANGARATIBA_base2", 0, cat='Integer')
x217 = LpVariable("GP_FPSO_MARICA_base2", 0, cat='Integer')
x218 = LpVariable("GP_FPSO_PARATY_base2", 0, cat='Integer')
x219 = LpVariable("GP_FPSO_PIONEIRO_DE_LIBRA_base2", 0, cat='Integer')
x220 = LpVariable("GP_FPSO_SANTOS_base2", 0, cat='Integer')
x221 = LpVariable("GP_FPSO_SAO_PAULO_base2", 0, cat='Integer')
x222 = LpVariable("GP_FPSO_SAQUAREMA_base2", 0, cat='Integer')
x223 = LpVariable("GP_NS_31_base2", 0, cat='Integer')
x224 = LpVariable("GP_NS_33_base2", 0, cat='Integer')
x225 = LpVariable("GP_NS_38_base2", 0, cat='Integer')
x226 = LpVariable("GP_NS_39_base2", 0, cat='Integer')
x227 = LpVariable("GP_NS_40_base2", 0, cat='Integer')
x228 = LpVariable("GP_NS_42_base2", 0, cat='Integer')
x229 = LpVariable("GP_NS_43_base2", 0, cat='Integer')
x230 = LpVariable("GP_NS_44_base2", 0, cat='Integer')
x231 = LpVariable("GP_P_66_base2", 0, cat='Integer')
x232 = LpVariable("GP_P_67_base2", 0, cat='Integer')
x233 = LpVariable("GP_P_68_base2", 0, cat='Integer')
x234 = LpVariable("GP_P_69_base2", 0, cat='Integer')
x235 = LpVariable("GP_P_70_base2", 0, cat='Integer')
x236 = LpVariable("GP_P_74_base2", 0, cat='Integer')
x237 = LpVariable("GP_P_75_base2", 0, cat='Integer')
x238 = LpVariable("GP_P_76_base2", 0, cat='Integer')
x239 = LpVariable("GP_P_77_base2", 0, cat='Integer')
x240 = LpVariable("GP_SS_75_base2", 0, cat='Integer')
x241 = LpVariable("GP_UMMA_base2", 0, cat='Integer')
x242 = LpVariable("GP_UMPA_base2", 0, cat='Integer')
x243 = LpVariable("GP_UMTJ_base2", 0, cat='Integer')
x244 = LpVariable("GP_UMVE_base2", 0, cat='Integer')
x245 = LpVariable("GP_SRIO_base2", 0, cat='Integer')
x246 = LpVariable("GP_SARU_base2", 0, cat='Integer')
x247 = LpVariable("GP_SAJA_base2", 0, cat='Integer')
x248 = LpVariable("GP_FASA_base2", 0, cat='Integer')
x249 = LpVariable("GP_SECR_base2", 0, cat='Integer')
x250 = LpVariable("GP_SAON_base2", 0, cat='Integer')
x251 = LpVariable("GP_SKST_base2", 0, cat='Integer')
x252 = LpVariable("GP_SKAU_base2", 0, cat='Integer')
x253 = LpVariable("GP_PMLZ_1_base3", 0, cat='Integer')
x254 = LpVariable("GP_PMXL_1_base3", 0, cat='Integer')
x255 = LpVariable("GP_FPSO_ANGRA_DOS_REIS_base3", 0, cat='Integer')
x256 = LpVariable("GP_FPSO_ILHABELA_base3", 0, cat='Integer')
x257 = LpVariable("GP_FPSO_ITAGUAI_base3", 0, cat='Integer')
x258 = LpVariable("GP_FPSO_MANGARATIBA_base3", 0, cat='Integer')
x259 = LpVariable("GP_FPSO_MARICA_base3", 0, cat='Integer')
x260 = LpVariable("GP_FPSO_PARATY_base3", 0, cat='Integer')
x261 = LpVariable("GP_FPSO_PIONEIRO_DE_LIBRA_base3", 0, cat='Integer')
x262 = LpVariable("GP_FPSO_SANTOS_base3", 0, cat='Integer')
x263 = LpVariable("GP_FPSO_SAO_PAULO_base3", 0, cat='Integer')
x264 = LpVariable("GP_FPSO_SAQUAREMA_base3", 0, cat='Integer')
x265 = LpVariable("GP_NS_31_base3", 0, cat='Integer')
x266 = LpVariable("GP_NS_33_base3", 0, cat='Integer')
x267 = LpVariable("GP_NS_38_base3", 0, cat='Integer')
x268 = LpVariable("GP_NS_39_base3", 0, cat='Integer')
x269 = LpVariable("GP_NS_40_base3", 0, cat='Integer')
x270 = LpVariable("GP_NS_42_base3", 0, cat='Integer')
x271 = LpVariable("GP_NS_43_base3", 0, cat='Integer')
x272 = LpVariable("GP_NS_44_base3", 0, cat='Integer')
x273 = LpVariable("GP_P_66_base3", 0, cat='Integer')
x274 = LpVariable("GP_P_67_base3", 0, cat='Integer')
x275 = LpVariable("GP_P_68_base3", 0, cat='Integer')
x276 = LpVariable("GP_P_69_base3", 0, cat='Integer')
x277 = LpVariable("GP_P_70_base3", 0, cat='Integer')
x278 = LpVariable("GP_P_74_base3", 0, cat='Integer')
x279 = LpVariable("GP_P_75_base3", 0, cat='Integer')
x280 = LpVariable("GP_P_76_base3", 0, cat='Integer')
x281 = LpVariable("GP_P_77_base3", 0, cat='Integer')
x282 = LpVariable("GP_SS_75_base3", 0, cat='Integer')
x283 = LpVariable("GP_UMMA_base3", 0, cat='Integer')
x284 = LpVariable("GP_UMPA_base3", 0, cat='Integer')
x285 = LpVariable("GP_UMTJ_base3", 0, cat='Integer')
x286 = LpVariable("GP_UMVE_base3", 0, cat='Integer')
x287 = LpVariable("GP_SRIO_base3", 0, cat='Integer')
x288 = LpVariable("GP_SARU_base3", 0, cat='Integer')
x289 = LpVariable("GP_SAJA_base3", 0, cat='Integer')
x290 = LpVariable("GP_FASA_base3", 0, cat='Integer')
x291 = LpVariable("GP_SECR_base3", 0, cat='Integer')
x292 = LpVariable("GP_SAON_base3", 0, cat='Integer')
x293 = LpVariable("GP_SKST_base3", 0, cat='Integer')
x294 = LpVariable("GP_SKAU_base3", 0, cat='Integer')
x295 = LpVariable("GP_PMLZ_1_base4", 0, cat='Integer')
x296 = LpVariable("GP_PMXL_1_base4", 0, cat='Integer')
x297 = LpVariable("GP_FPSO_ANGRA_DOS_REIS_base4", 0, cat='Integer')
x298 = LpVariable("GP_FPSO_ILHABELA_base4", 0, cat='Integer')
x299 = LpVariable("GP_FPSO_ITAGUAI_base4", 0, cat='Integer')
x300 = LpVariable("GP_FPSO_MANGARATIBA_base4", 0, cat='Integer')
x301 = LpVariable("GP_FPSO_MARICA_base4", 0, cat='Integer')
x302 = LpVariable("GP_FPSO_PARATY_base4", 0, cat='Integer')
x303 = LpVariable("GP_FPSO_PIONEIRO_DE_LIBRA_base4", 0, cat='Integer')
x304 = LpVariable("GP_FPSO_SANTOS_base4", 0, cat='Integer')
x305 = LpVariable("GP_FPSO_SAO_PAULO_base4", 0, cat='Integer')
x306 = LpVariable("GP_FPSO_SAQUAREMA_base4", 0, cat='Integer')
x307 = LpVariable("GP_NS_31_base4", 0, cat='Integer')
x308 = LpVariable("GP_NS_33_base4", 0, cat='Integer')
x309 = LpVariable("GP_NS_38_base4", 0, cat='Integer')
x310 = LpVariable("GP_NS_39_base4", 0, cat='Integer')
x311 = LpVariable("GP_NS_40_base4", 0, cat='Integer')
x312 = LpVariable("GP_NS_42_base4", 0, cat='Integer')
x313 = LpVariable("GP_NS_43_base4", 0, cat='Integer')
x314 = LpVariable("GP_NS_44_base4", 0, cat='Integer')
x315 = LpVariable("GP_P_66_base4", 0, cat='Integer')
x316 = LpVariable("GP_P_67_base4", 0, cat='Integer')
x317 = LpVariable("GP_P_68_base4", 0, cat='Integer')
x318 = LpVariable("GP_P_69_base4", 0, cat='Integer')
x319 = LpVariable("GP_P_70_base4", 0, cat='Integer')
x320 = LpVariable("GP_P_74_base4", 0, cat='Integer')
x321 = LpVariable("GP_P_75_base4", 0, cat='Integer')
x322 = LpVariable("GP_P_76_base4", 0, cat='Integer')
x323 = LpVariable("GP_P_77_base4", 0, cat='Integer')
x324 = LpVariable("GP_SS_75_base4", 0, cat='Integer')
x325 = LpVariable("GP_UMMA_base4", 0, cat='Integer')
x326 = LpVariable("GP_UMPA_base4", 0, cat='Integer')
x327 = LpVariable("GP_UMTJ_base4", 0, cat='Integer')
x328 = LpVariable("GP_UMVE_base4", 0, cat='Integer')
x329 = LpVariable("GP_SRIO_base4", 0, cat='Integer')
x330 = LpVariable("GP_SARU_base4", 0, cat='Integer')
x331 = LpVariable("GP_SAJA_base4", 0, cat='Integer')
x332 = LpVariable("GP_FASA_base4", 0, cat='Integer')
x333 = LpVariable("GP_SECR_base4", 0, cat='Integer')
x334 = LpVariable("GP_SAON_base4", 0, cat='Integer')
x335 = LpVariable("GP_SKST_base4", 0, cat='Integer')
x336 = LpVariable("GP_SKAU_base4", 0, cat='Integer')



# LISTA COM AS VARIAVEIS DE DECISÃO (VD) - (1 LINHA x 336 COLUNAS)
VD = [x1,	x2,	x3,	x4,	x5,	x6,	x7,	x8,	x9,	x10,	x11,	x12,	x13,	x14,	
      x15,	x16,	x17,	x18,	x19,	x20,	x21,	x22,	x23,	x24,	
      x25,	x26,	x27,	x28,	x29,	x30,	x31,	x32,	x33,	x34,	
      x35,	x36,	x37,	x38,	x39,	x40,	x41,	x42,	x43,	x44,	
      x45,	x46,	x47,	x48,	x49,	x50,	x51,	x52,	x53,	x54,	
      x55,	x56,	x57,	x58,	x59,	x60,	x61,	x62,	x63,	x64,	
      x65,	x66,	x67,	x68,	x69,	x70,	x71,	x72,	x73,	x74,	
      x75,	x76,	x77,	x78,	x79,	x80,	x81,	x82,	x83,	x84,	
      x85,	x86,	x87,	x88,	x89,	x90,	x91,	x92,	x93,	x94,	
      x95,	x96,	x97,	x98,	x99,	x100,	x101,	x102,	x103,	x104,	
      x105,	x106,	x107,	x108,	x109,	x110,	x111,	x112,	x113,	x114,	
      x115,	x116,	x117,	x118,	x119,	x120,	x121,	x122,	x123,	x124,	
      x125,	x126,	x127,	x128,	x129,	x130,	x131,	x132,	x133,	x134,	
      x135,	x136,	x137,	x138,	x139,	x140,	x141,	x142,	x143,	x144,	
      x145,	x146,	x147,	x148,	x149,	x150,	x151,	x152,	x153,	x154,	
      x155,	x156,	x157,	x158,	x159,	x160,	x161,	x162,	x163,	x164,	
      x165,	x166,	x167,	x168,	x169,	x170,	x171,	x172,	x173,	x174,	
      x175,	x176,	x177,	x178,	x179,	x180,	x181,	x182,	x183,	x184,	
      x185,	x186,	x187,	x188,	x189,	x190,	x191,	x192,	x193,	x194,	
      x195,	x196,	x197,	x198,	x199,	x200,	x201,	x202,	x203,	x204,	
      x205,	x206,	x207,	x208,	x209,	x210,	x211,	x212,	x213,	x214,	
      x215,	x216,	x217,	x218,	x219,	x220,	x221,	x222,	x223,	x224,	
      x225,	x226,	x227,	x228,	x229,	x230,	x231,	x232,	x233,	x234,	
      x235,	x236,	x237,	x238,	x239,	x240,	x241,	x242,	x243,	x244,	
      x245,	x246,	x247,	x248,	x249,	x250,	x251,	x252,	x253,	x254,	
      x255,	x256,	x257,	x258,	x259,	x260,	x261,	x262,	x263,	x264,	
      x265,	x266,	x267,	x268,	x269,	x270,	x271,	x272,	x273,	x274,	
      x275,	x276,	x277,	x278,	x279,	x280,	x281,	x282,	x283,	x284,	
      x285,	x286,	x287,	x288,	x289,	x290,	x291,	x292,	x293,	x294,	
      x295,	x296,	x297,	x298,	x299,	x300,	x301,	x302,	x303,	x304,	
      x305,	x306,	x307,	x308,	x309,	x310,	x311,	x312,	x313,	x314,	
      x315,	x316,	x317,	x318,	x319,	x320,	x321,	x322,	x323,	x324,	
      x325,	x326,	x327,	x328,	x329,	x330,	x331,	x332,	x333,	x334,	
      x335,	x336]

# Importa a matriz de custos dos voos
data_custos = output_df['CUSTO_MISSAO']

# Cria a funcao objetivo (numeros de voos (por porte e origem/destino) * custo dos voos)
prob+= np.dot(VD,data_custos),"Total custos"

#RESTRIÇÕES DE ATENDIMENTO À DEMANDA (a demand da UM(j) deve ser atendida)

#COM AEROVIAS
prob+= x1 * output_df['QUANT_PAX'][0] + x169 * output_df['QUANT_PAX'][168] + x43*  output_df['QUANT_PAX'][42] + x211 * output_df['QUANT_PAX'][210] + x85 * output_df['QUANT_PAX'][84] + x253 * output_df['QUANT_PAX'][252] + x127 * output_df['QUANT_PAX'][126] + x295 * output_df['QUANT_PAX'][294] >= 75,  "demanda atendida PMLZ_1"

prob+= x2 * output_df['QUANT_PAX'][1] + x170 * output_df['QUANT_PAX'][169] + x44*  output_df['QUANT_PAX'][43] + x212 * output_df['QUANT_PAX'][211] + x86 * output_df['QUANT_PAX'][85] + x254 * output_df['QUANT_PAX'][253] + x128 * output_df['QUANT_PAX'][127] + x296 * output_df['QUANT_PAX'][295] >= 75,  "demanda atendida PMXL_1"

prob+= x3 * output_df['QUANT_PAX'][2] + x171 * output_df['QUANT_PAX'][170] + x45*  output_df['QUANT_PAX'][44] + x213 * output_df['QUANT_PAX'][212] + x87 * output_df['QUANT_PAX'][86] + x255 * output_df['QUANT_PAX'][254] + x129 * output_df['QUANT_PAX'][128] + x297 * output_df['QUANT_PAX'][296] >= 75,  "demanda atendida FPSO_ANGRA_DOS_REIS"

prob+= x4 * output_df['QUANT_PAX'][3] + x172 * output_df['QUANT_PAX'][171] + x46*  output_df['QUANT_PAX'][45] + x214 * output_df['QUANT_PAX'][213] + x88 * output_df['QUANT_PAX'][87] + x256 * output_df['QUANT_PAX'][255] + x130 * output_df['QUANT_PAX'][129] + x298 * output_df['QUANT_PAX'][297] >= 75,  "demanda atendida FPSO_ILHABELA"

prob+= x5 * output_df['QUANT_PAX'][4] + x173 * output_df['QUANT_PAX'][172] + x47*  output_df['QUANT_PAX'][46] + x215 * output_df['QUANT_PAX'][214] + x89 * output_df['QUANT_PAX'][88] + x257 * output_df['QUANT_PAX'][256] + x131 * output_df['QUANT_PAX'][130] + x299 * output_df['QUANT_PAX'][298] >= 75,  "demanda atendida FPSO_ITAGUAI"

prob+= x6 * output_df['QUANT_PAX'][5] + x174 * output_df['QUANT_PAX'][173] + x48*  output_df['QUANT_PAX'][47] + x216 * output_df['QUANT_PAX'][215] + x90 * output_df['QUANT_PAX'][89] + x258 * output_df['QUANT_PAX'][257] + x132 * output_df['QUANT_PAX'][131] + x300 * output_df['QUANT_PAX'][299] >= 75,  "demanda atendida FPSO_MANGARATIBA"

prob+= x7 * output_df['QUANT_PAX'][6] + x175 * output_df['QUANT_PAX'][174] + x49*  output_df['QUANT_PAX'][48] + x217 * output_df['QUANT_PAX'][216] + x91 * output_df['QUANT_PAX'][90] + x259 * output_df['QUANT_PAX'][258] + x133 * output_df['QUANT_PAX'][132] + x301 * output_df['QUANT_PAX'][300] >= 75,  "demanda atendida FPSO_MARICA"

prob+= x8 * output_df['QUANT_PAX'][7] + x176 * output_df['QUANT_PAX'][175] + x50*  output_df['QUANT_PAX'][49] + x218 * output_df['QUANT_PAX'][217] + x92 * output_df['QUANT_PAX'][91] + x260 * output_df['QUANT_PAX'][259] + x134 * output_df['QUANT_PAX'][133] + x302 * output_df['QUANT_PAX'][301] >= 75,  "demanda atendida FPSO_PARATY"

prob+= x9 * output_df['QUANT_PAX'][8] + x177 * output_df['QUANT_PAX'][176] + x51*  output_df['QUANT_PAX'][50] + x219 * output_df['QUANT_PAX'][218] + x93 * output_df['QUANT_PAX'][92] + x261 * output_df['QUANT_PAX'][260] + x135 * output_df['QUANT_PAX'][134] + x303 * output_df['QUANT_PAX'][302] >= 75,  "demanda atendida FPSO_PIONEIRO_DE_LIBRA"

prob+= x10 * output_df['QUANT_PAX'][9] + x178 * output_df['QUANT_PAX'][177] + x52*  output_df['QUANT_PAX'][51] + x220 * output_df['QUANT_PAX'][219] + x94 * output_df['QUANT_PAX'][93] + x262 * output_df['QUANT_PAX'][261] + x136 * output_df['QUANT_PAX'][135] + x304 * output_df['QUANT_PAX'][303] >= 75,  "demanda atendida FPSO_SANTOS"

prob+= x11 * output_df['QUANT_PAX'][10] + x179 * output_df['QUANT_PAX'][178] + x53*  output_df['QUANT_PAX'][52] + x221 * output_df['QUANT_PAX'][220] + x95 * output_df['QUANT_PAX'][94] + x263 * output_df['QUANT_PAX'][262] + x137 * output_df['QUANT_PAX'][136] + x305 * output_df['QUANT_PAX'][304] >= 75,  "demanda atendida FPSO_SAO_PAULO"

prob+= x12 * output_df['QUANT_PAX'][11] + x180 * output_df['QUANT_PAX'][179] + x54*  output_df['QUANT_PAX'][53] + x222 * output_df['QUANT_PAX'][221] + x96 * output_df['QUANT_PAX'][95] + x264 * output_df['QUANT_PAX'][263] + x138 * output_df['QUANT_PAX'][137] + x306 * output_df['QUANT_PAX'][305] >= 75,  "demanda atendida FPSO_SAQUAREMA"

prob+= x13 * output_df['QUANT_PAX'][12] + x181 * output_df['QUANT_PAX'][180] + x55*  output_df['QUANT_PAX'][54] + x223 * output_df['QUANT_PAX'][222] + x97 * output_df['QUANT_PAX'][96] + x265 * output_df['QUANT_PAX'][264] + x139 * output_df['QUANT_PAX'][138] + x307 * output_df['QUANT_PAX'][306] >= 87,  "demanda atendida NS_31"

prob+= x14 * output_df['QUANT_PAX'][13] + x182 * output_df['QUANT_PAX'][181] + x56*  output_df['QUANT_PAX'][55] + x224 * output_df['QUANT_PAX'][223] + x98 * output_df['QUANT_PAX'][97] + x266 * output_df['QUANT_PAX'][265] + x140 * output_df['QUANT_PAX'][139] + x308 * output_df['QUANT_PAX'][307] >= 87,  "demanda atendida NS_33"

prob+= x15 * output_df['QUANT_PAX'][14] + x183 * output_df['QUANT_PAX'][182] + x57*  output_df['QUANT_PAX'][56] + x225 * output_df['QUANT_PAX'][224] + x99 * output_df['QUANT_PAX'][98] + x267 * output_df['QUANT_PAX'][266] + x141 * output_df['QUANT_PAX'][140] + x309 * output_df['QUANT_PAX'][308] >= 87,  "demanda atendida NS_38"

prob+= x16 * output_df['QUANT_PAX'][15] + x184 * output_df['QUANT_PAX'][183] + x58*  output_df['QUANT_PAX'][57] + x226 * output_df['QUANT_PAX'][225] + x100 * output_df['QUANT_PAX'][99] + x268 * output_df['QUANT_PAX'][267] + x142 * output_df['QUANT_PAX'][141] + x310 * output_df['QUANT_PAX'][309] >= 87,  "demanda atendida NS_39"

prob+= x17 * output_df['QUANT_PAX'][16] + x185 * output_df['QUANT_PAX'][184] + x59*  output_df['QUANT_PAX'][58] + x227 * output_df['QUANT_PAX'][226] + x101 * output_df['QUANT_PAX'][100] + x269 * output_df['QUANT_PAX'][268] + x143 * output_df['QUANT_PAX'][142] + x311 * output_df['QUANT_PAX'][310] >= 87,  "demanda atendida NS_40"

prob+= x18 * output_df['QUANT_PAX'][17] + x186 * output_df['QUANT_PAX'][185] + x60*  output_df['QUANT_PAX'][59] + x228 * output_df['QUANT_PAX'][227] + x102 * output_df['QUANT_PAX'][101] + x270 * output_df['QUANT_PAX'][269] + x144 * output_df['QUANT_PAX'][143] + x312 * output_df['QUANT_PAX'][311] >= 87,  "demanda atendida NS_42"

prob+= x19 * output_df['QUANT_PAX'][18] + x187 * output_df['QUANT_PAX'][186] + x61*  output_df['QUANT_PAX'][60] + x229 * output_df['QUANT_PAX'][228] + x103 * output_df['QUANT_PAX'][102] + x271 * output_df['QUANT_PAX'][270] + x145 * output_df['QUANT_PAX'][144] + x313 * output_df['QUANT_PAX'][312] >= 87,  "demanda atendida NS_43"

prob+= x20 * output_df['QUANT_PAX'][19] + x188 * output_df['QUANT_PAX'][187] + x62*  output_df['QUANT_PAX'][61] + x230 * output_df['QUANT_PAX'][229] + x104 * output_df['QUANT_PAX'][103] + x272 * output_df['QUANT_PAX'][271] + x146 * output_df['QUANT_PAX'][145] + x314 * output_df['QUANT_PAX'][313] >= 87,  "demanda atendida NS_44"

prob+= x21 * output_df['QUANT_PAX'][20] + x189 * output_df['QUANT_PAX'][188] + x63*  output_df['QUANT_PAX'][62] + x231 * output_df['QUANT_PAX'][230] + x105 * output_df['QUANT_PAX'][104] + x273 * output_df['QUANT_PAX'][272] + x147 * output_df['QUANT_PAX'][146] + x315 * output_df['QUANT_PAX'][314] >= 87,  "demanda atendida P_66"

prob+= x22 * output_df['QUANT_PAX'][21] + x190 * output_df['QUANT_PAX'][189] + x64*  output_df['QUANT_PAX'][63] + x232 * output_df['QUANT_PAX'][231] + x106 * output_df['QUANT_PAX'][105] + x274 * output_df['QUANT_PAX'][273] + x148 * output_df['QUANT_PAX'][147] + x316 * output_df['QUANT_PAX'][315] >= 87,  "demanda atendida P_67"

prob+= x23 * output_df['QUANT_PAX'][22] + x191 * output_df['QUANT_PAX'][190] + x65*  output_df['QUANT_PAX'][64] + x233 * output_df['QUANT_PAX'][232] + x107 * output_df['QUANT_PAX'][106] + x275 * output_df['QUANT_PAX'][274] + x149 * output_df['QUANT_PAX'][148] + x317 * output_df['QUANT_PAX'][316] >= 87,  "demanda atendida P_68"

prob+= x24 * output_df['QUANT_PAX'][23] + x192 * output_df['QUANT_PAX'][191] + x66*  output_df['QUANT_PAX'][65] + x234 * output_df['QUANT_PAX'][233] + x108 * output_df['QUANT_PAX'][107] + x276 * output_df['QUANT_PAX'][275] + x150 * output_df['QUANT_PAX'][149] + x318 * output_df['QUANT_PAX'][317] >= 87,  "demanda atendida P_69"

prob+= x25 * output_df['QUANT_PAX'][24] + x193 * output_df['QUANT_PAX'][192] + x67*  output_df['QUANT_PAX'][66] + x235 * output_df['QUANT_PAX'][234] + x109 * output_df['QUANT_PAX'][108] + x277 * output_df['QUANT_PAX'][276] + x151 * output_df['QUANT_PAX'][150] + x319 * output_df['QUANT_PAX'][318] >= 87,  "demanda atendida P_70"

prob+= x26 * output_df['QUANT_PAX'][25] + x194 * output_df['QUANT_PAX'][193] + x68*  output_df['QUANT_PAX'][67] + x236 * output_df['QUANT_PAX'][235] + x110 * output_df['QUANT_PAX'][109] + x278 * output_df['QUANT_PAX'][277] + x152 * output_df['QUANT_PAX'][151] + x320 * output_df['QUANT_PAX'][319] >= 87,  "demanda atendida P_74"

prob+= x27 * output_df['QUANT_PAX'][26] + x195 * output_df['QUANT_PAX'][194] + x69*  output_df['QUANT_PAX'][68] + x237 * output_df['QUANT_PAX'][236] + x111 * output_df['QUANT_PAX'][110] + x279 * output_df['QUANT_PAX'][278] + x153 * output_df['QUANT_PAX'][152] + x321 * output_df['QUANT_PAX'][320] >= 87,  "demanda atendida P_75"

prob+= x28 * output_df['QUANT_PAX'][27] + x196 * output_df['QUANT_PAX'][195] + x70*  output_df['QUANT_PAX'][69] + x238 * output_df['QUANT_PAX'][237] + x112 * output_df['QUANT_PAX'][111] + x280 * output_df['QUANT_PAX'][279] + x154 * output_df['QUANT_PAX'][153] + x322 * output_df['QUANT_PAX'][321] >= 87,  "demanda atendida P_76"

prob+= x29 * output_df['QUANT_PAX'][28] + x197 * output_df['QUANT_PAX'][196] + x71*  output_df['QUANT_PAX'][70] + x239 * output_df['QUANT_PAX'][238] + x113 * output_df['QUANT_PAX'][112] + x281 * output_df['QUANT_PAX'][280] + x155 * output_df['QUANT_PAX'][154] + x323 * output_df['QUANT_PAX'][322] >= 87,  "demanda atendida P_77"

prob+= x30 * output_df['QUANT_PAX'][29] + x198 * output_df['QUANT_PAX'][197] + x72*  output_df['QUANT_PAX'][71] + x240 * output_df['QUANT_PAX'][239] + x114 * output_df['QUANT_PAX'][113] + x282 * output_df['QUANT_PAX'][281] + x156 * output_df['QUANT_PAX'][155] + x324 * output_df['QUANT_PAX'][323] >= 87,  "demanda atendida SS_75"

prob+= x31 * output_df['QUANT_PAX'][30] + x199 * output_df['QUANT_PAX'][198] + x73*  output_df['QUANT_PAX'][72] + x241 * output_df['QUANT_PAX'][240] + x115 * output_df['QUANT_PAX'][114] + x283 * output_df['QUANT_PAX'][282] + x157 * output_df['QUANT_PAX'][156] + x325 * output_df['QUANT_PAX'][324] >= 250,  "demanda atendida UMMA"

prob+= x32 * output_df['QUANT_PAX'][31] + x200 * output_df['QUANT_PAX'][199] + x74*  output_df['QUANT_PAX'][73] + x242 * output_df['QUANT_PAX'][241] + x116 * output_df['QUANT_PAX'][115] + x284 * output_df['QUANT_PAX'][283] + x158 * output_df['QUANT_PAX'][157] + x326 * output_df['QUANT_PAX'][325] >= 250,  "demanda atendida UMPA"

prob+= x33 * output_df['QUANT_PAX'][32] + x201 * output_df['QUANT_PAX'][200] + x75*  output_df['QUANT_PAX'][74] + x243 * output_df['QUANT_PAX'][242] + x117 * output_df['QUANT_PAX'][116] + x285 * output_df['QUANT_PAX'][284] + x159 * output_df['QUANT_PAX'][158] + x327 * output_df['QUANT_PAX'][326] >= 250,  "demanda atendida UMTJ"

prob+= x34 * output_df['QUANT_PAX'][33] + x202 * output_df['QUANT_PAX'][201] + x76*  output_df['QUANT_PAX'][75] + x244 * output_df['QUANT_PAX'][243] + x118 * output_df['QUANT_PAX'][117] + x286 * output_df['QUANT_PAX'][285] + x160 * output_df['QUANT_PAX'][159] + x328 * output_df['QUANT_PAX'][327] >= 250,  "demanda atendida UMVE"

prob+= x35 * output_df['QUANT_PAX'][34] + x203 * output_df['QUANT_PAX'][202] + x77*  output_df['QUANT_PAX'][76] + x245 * output_df['QUANT_PAX'][244] + x119 * output_df['QUANT_PAX'][118] + x287 * output_df['QUANT_PAX'][286] + x161 * output_df['QUANT_PAX'][160] + x329 * output_df['QUANT_PAX'][328] >= 30,  "demanda atendida SRIO"

prob+= x36 * output_df['QUANT_PAX'][35] + x204 * output_df['QUANT_PAX'][203] + x78*  output_df['QUANT_PAX'][77] + x246 * output_df['QUANT_PAX'][245] + x120 * output_df['QUANT_PAX'][119] + x288 * output_df['QUANT_PAX'][287] + x162 * output_df['QUANT_PAX'][161] + x330 * output_df['QUANT_PAX'][329] >= 30,  "demanda atendida SARU"

prob+= x37 * output_df['QUANT_PAX'][36] + x205 * output_df['QUANT_PAX'][204] + x79*  output_df['QUANT_PAX'][78] + x247 * output_df['QUANT_PAX'][246] + x121 * output_df['QUANT_PAX'][120] + x289 * output_df['QUANT_PAX'][288] + x163 * output_df['QUANT_PAX'][162] + x331 * output_df['QUANT_PAX'][330] >= 30,  "demanda atendida SAJA"

prob+= x38 * output_df['QUANT_PAX'][37] + x206 * output_df['QUANT_PAX'][205] + x80*  output_df['QUANT_PAX'][79] + x248 * output_df['QUANT_PAX'][247] + x122 * output_df['QUANT_PAX'][121] + x290 * output_df['QUANT_PAX'][289] + x164 * output_df['QUANT_PAX'][163] + x332 * output_df['QUANT_PAX'][331] >= 30,  "demanda atendida FASA"

prob+= x39 * output_df['QUANT_PAX'][38] + x207 * output_df['QUANT_PAX'][206] + x81*  output_df['QUANT_PAX'][80] + x249 * output_df['QUANT_PAX'][248] + x123 * output_df['QUANT_PAX'][122] + x291 * output_df['QUANT_PAX'][290] + x165 * output_df['QUANT_PAX'][164] + x333 * output_df['QUANT_PAX'][332] >= 30,  "demanda atendida SECR"

prob+= x40 * output_df['QUANT_PAX'][39] + x208 * output_df['QUANT_PAX'][207] + x82*  output_df['QUANT_PAX'][81] + x250 * output_df['QUANT_PAX'][249] + x124 * output_df['QUANT_PAX'][123] + x292 * output_df['QUANT_PAX'][291] + x166 * output_df['QUANT_PAX'][165] + x334 * output_df['QUANT_PAX'][333] >= 30,  "demanda atendida SAON"

prob+= x41 * output_df['QUANT_PAX'][40] + x209 * output_df['QUANT_PAX'][208] + x83*  output_df['QUANT_PAX'][82] + x251 * output_df['QUANT_PAX'][250] + x125 * output_df['QUANT_PAX'][124] + x293 * output_df['QUANT_PAX'][292] + x167 * output_df['QUANT_PAX'][166] + x335 * output_df['QUANT_PAX'][334] >= 30,  "demanda atendida SKST"

prob+= x42 * output_df['QUANT_PAX'][41] + x210 * output_df['QUANT_PAX'][209] + x84*  output_df['QUANT_PAX'][83] + x252 * output_df['QUANT_PAX'][251] + x126 * output_df['QUANT_PAX'][125] + x294 * output_df['QUANT_PAX'][293] + x168 * output_df['QUANT_PAX'][167] + x336 * output_df['QUANT_PAX'][335] >= 30,  "demanda atendida SKAU"



#RESTRIÇÕES DE CAPACIDADE DOS AERÓDROMOS
#avaliada as capacidades por porte de aeronaves e capacidades totais dos aerodromos (voos por semana)
prob+= x1+	x2+	x3+	x4+	x5+	x6+	x7+	x8+	x9+	x10+	x11+	x12+	x13+	x14+	x15+	x16+	x17+	x18+	x19+	x20+	x21+	x22+	x23+	x24+	x25+	x26+	x27+	x28+	x29+	x30+	x31+	x32+	x33+	x34+	x35+	x36+	x37+	x38+	x39+	x40+	x41+	x42 <= 7 * base1_cap_mp, "capacidade de voos semanal MP base1"

prob+=x169+	x170+	x171+	x172+	x173+	x174+	x175+	x176+	x177+	x178+	x179+	x180+	x181+	x182+	x183+	x184+	x185+	x186+	x187+	x188+	x189+	x190+	x191+	x192+	x193+	x194+	x195+	x196+	x197+	x198+	x199+	x200+	x201+	x202+	x203+	x204+	x205+	x206+	x207+	x208+	x209+	x210 <= 7 * base1_cap_gp, "capacidade de voos semanal GP base1"

prob+=x43+	x44+	x45+	x46+	x47+	x48+	x49+	x50+	x51+	x52+	x53+	x54+	x55+	x56+	x57+	x58+	x59+	x60+	x61+	x62+	x63+	x64+	x65+	x66+	x67+	x68+	x69+	x70+	x71+	x72+	x73+	x74+	x75+	x76+	x77+	x78+	x79+	x80+	x81+	x82+	x83+	x84 <= 7 * base2_cap_mp, "capacidade de voos semanal MP base2"

prob+=x211+	x212+	x213+	x214+	x215+	x216+	x217+	x218+	x219+	x220+	x221+	x222+	x223+	x224+	x225+	x226+	x227+	x228+	x229+	x230+	x231+	x232+	x233+	x234+	x235+	x236+	x237+	x238+	x239+	x240+	x241+	x242+	x243+	x244+	x245+	x246+	x247+	x248+	x249+	x250+	x251+	x252 <= 7 * base2_cap_gp, "capacidade de voos semanal GP base2"

prob+=x85+	x86+	x87+	x88+	x89+	x90+	x91+	x92+	x93+	x94+	x95+	x96+	x97+	x98+	x99+	x100+	x101+	x102+	x103+	x104+	x105+	x106+	x107+	x108+	x109+	x110+	x111+	x112+	x113+	x114+	x115+	x116+	x117+	x118+	x119+	x120+	x121+	x122+	x123+	x124+	x125+	x126 <= 7 * base3_cap_mp, "capacidade de voos semanal MP base3"

prob+=x253+	x254+	x255+	x256+	x257+	x258+	x259+	x260+	x261+	x262+	x263+	x264+	x265+	x266+	x267+	x268+	x269+	x270+	x271+	x272+	x273+	x274+	x275+	x276+	x277+	x278+	x279+	x280+	x281+	x282+	x283+	x284+	x285+	x286+	x287+	x288+	x289+	x290+	x291+	x292+	x293+	x294 <= 7 * base3_cap_gp,"capacidade de voos semanal GP base3"

prob+=x127+	x128+	x129+	x130+	x131+	x132+	x133+	x134+	x135+	x136+	x137+	x138+	x139+	x140+	x141+	x142+	x143+	x144+	x145+	x146+	x147+	x148+	x149+	x150+	x151+	x152+	x153+	x154+	x155+	x156+	x157+	x158+	x159+	x160+	x161+	x162+	x163+	x164+	x165+	x166+	x167+	x168 <= 7 * base4_cap_mp, "capacidade de voos semanal MP base4"

prob+=x295+	x296+	x297+	x298+	x299+	x300+	x301+	x302+	x303+	x304+	x305+	x306+	x307+	x308+	x309+	x310+	x311+	x312+	x313+	x314+	x315+	x316+	x317+	x318+	x319+	x320+	x321+	x322+	x323+	x324+	x325+	x326+	x327+	x328+	x329+	x330+	x331+	x332+	x333+	x334+	x335+	x336 <= 7 * base4_cap_gp, "capacidade de voos semanal GP base4"

prob+=x1+	x2+	x3+	x4+	x5+	x6+	x7+	x8+	x9+	x10+	x11+	x12+	x13+	x14+	x15+	x16+	x17+	x18+	x19+	x20+	x21+	x22+	x23+	x24+	x25+	x26+	x27+	x28+	x29+	x30+	x31+	x32+	x33+	x34+	x35+	x36+	x37+	x38+	x39+	x40+	x41+	x42+	x169+	x170+	x171+	x172+	x173+	x174+	x175+	x176+	x177+	x178+	x179+	x180+	x181+	x182+	x183+	x184+	x185+	x186+	x187+	x188+	x189+	x190+	x191+	x192+	x193+	x194+	x195+	x196+	x197+	x198+	x199+	x200+	x201+	x202+	x203+	x204+	x205+	x206+	x207+	x208+	x209+	x210 <= 7 * base1_cap_total, "capacidade de voos semanal total base1"

prob+=x43+	x44+	x45+	x46+	x47+	x48+	x49+	x50+	x51+	x52+	x53+	x54+	x55+	x56+	x57+	x58+	x59+	x60+	x61+	x62+	x63+	x64+	x65+	x66+	x67+	x68+	x69+	x70+	x71+	x72+	x73+	x74+	x75+	x76+	x77+	x78+	x79+	x80+	x81+	x82+	x83+	x84+	x211+	x212+	x213+	x214+	x215+	x216+	x217+	x218+	x219+	x220+	x221+	x222+	x223+	x224+	x225+	x226+	x227+	x228+	x229+	x230+	x231+	x232+	x233+	x234+	x235+	x236+	x237+	x238+	x239+	x240+	x241+	x242+	x243+	x244+	x245+	x246+	x247+	x248+	x249+	x250+	x251+	x252 <= 7 * base2_cap_total, "capacidade de voos semanal total base2"

prob+=x85+	x86+	x87+	x88+	x89+	x90+	x91+	x92+	x93+	x94+	x95+	x96+	x97+	x98+	x99+	x100+	x101+	x102+	x103+	x104+	x105+	x106+	x107+	x108+	x109+	x110+	x111+	x112+	x113+	x114+	x115+	x116+	x117+	x118+	x119+	x120+	x121+	x122+	x123+	x124+	x125+	x126+	x253+	x254+	x255+	x256+	x257+	x258+	x259+	x260+	x261+	x262+	x263+	x264+	x265+	x266+	x267+	x268+	x269+	x270+	x271+	x272+	x273+	x274+	x275+	x276+	x277+	x278+	x279+	x280+	x281+	x282+	x283+	x284+	x285+	x286+	x287+	x288+	x289+	x290+	x291+	x292+	x293+	x294 <= 7 * base3_cap_total, "capacidade de voos semanal total base3"

prob+=x127+	x128+	x129+	x130+	x131+	x132+	x133+	x134+	x135+	x136+	x137+	x138+	x139+	x140+	x141+	x142+	x143+	x144+	x145+	x146+	x147+	x148+	x149+	x150+	x151+	x152+	x153+	x154+	x155+	x156+	x157+	x158+	x159+	x160+	x161+	x162+	x163+	x164+	x165+	x166+	x167+	x168+	x295+	x296+	x297+	x298+	x299+	x300+	x301+	x302+	x303+	x304+	x305+	x306+	x307+	x308+	x309+	x310+	x311+	x312+	x313+	x314+	x315+	x316+	x317+	x318+	x319+	x320+	x321+	x322+	x323+	x324+	x325+	x326+	x327+	x328+	x329+	x330+	x331+	x332+	x333+	x334+	x335+	x336 <= 7 * base4_cap_total, "capacidade de voos semanal total base4"

# Escreve o modelo no arquivo
prob.writeLP("otimizavoos.lp")

# Resolve o problema
prob.solve()

# Imprime o status da resolucao
print ("Status:", LpStatus[prob.status])


# Solucoes otimas das variaveis
for variable in prob.variables():
   print ("%s = %f" % (variable.name, variable.varValue))

# Objetivo otimizado
print (f'Custo total semanal dos atendimentos: R$ {value(prob.objective):.0f}')

print(f'CENARIO GERAL: {cenario_geral}')
print('')

print(f'QAV: {cenario_qav}')
print('')

valor_anual = value(prob.objective) / 7 * 365
print('custo anual R$:')
print(f'{valor_anual:.0f}')

#################################################################
# CÁLCULO DO NUMERO DE VOOS

voos_MP_base1 = 0
voos_MP_base2 = 0
voos_MP_base3 = 0
voos_MP_base4 = 0

voos_GP_base1 = 0
voos_GP_base2 = 0
voos_GP_base3 = 0
voos_GP_base4 = 0


numero_voos = []
for variavel in VD:
    numero_voos.append(variavel.varValue)

total_VD = len(numero_voos)
incremento = total_VD / 8

for i in range(total_VD):
    if i < incremento:
        voos_MP_base1 = voos_MP_base1 + numero_voos[i]

    if i >= incremento and i < incremento * 2:
        voos_MP_base2 = voos_MP_base2 + numero_voos[i]        

    if i >= incremento * 2 and i < incremento * 3:
        voos_MP_base3 = voos_MP_base3 + numero_voos[i]  

    if i >= incremento * 3 and i < incremento * 4:
        voos_MP_base4 = voos_MP_base4 + numero_voos[i]          

    if i >= incremento * 4 and i < incremento * 5:
        voos_GP_base1 = voos_GP_base1 + numero_voos[i]

    if i >= incremento * 5 and i < incremento * 6:
        voos_GP_base2 = voos_GP_base2 + numero_voos[i]        

    if i >= incremento * 6 and i < incremento * 7:
        voos_GP_base3 = voos_GP_base3 + numero_voos[i]  

    if i >= incremento * 7 and i < incremento * 8:
        voos_GP_base4 = voos_GP_base4 + numero_voos[i]          
              
print('')    
print('voos_MP_base1 semanal = ', voos_MP_base1)
print('voos_GP_base1 semanal = ', voos_GP_base1)

print('voos_MP_base2 semanal = ', voos_MP_base2)
print('voos_GP_base2 semanal = ', voos_GP_base2)

print('voos_MP_base3 semanal = ', voos_MP_base3)
print('voos_GP_base3 semanal = ', voos_GP_base3)

print('voos_MP_base4 semanal = ', voos_MP_base4)
print('voos_GP_base4 semanal = ', voos_GP_base4)
print('')
print('TOTAL VOOS MP semanal = ', voos_MP_base1 + voos_MP_base2 + voos_MP_base3 + voos_MP_base4)
print('TOTAL VOOS GP semanal = ', voos_GP_base1 + voos_GP_base2 + voos_GP_base3 + voos_GP_base4)
print('TOTAL VOOS semanal = ', voos_MP_base1 + voos_MP_base2 + voos_MP_base3 + voos_MP_base4 + voos_GP_base1 + voos_GP_base2 + voos_GP_base3 + voos_GP_base4)
print('')

#################################################################
# CÁLCULO DAS HORAS VOADAS (DCOLAGEM A POUSO)

horas_voadas_dec_pouso_MP_base1 = 0
horas_voadas_dec_pouso_MP_base2 = 0
horas_voadas_dec_pouso_MP_base3 = 0
horas_voadas_dec_pouso_MP_base4 = 0

horas_voadas_dec_pouso_GP_base1 = 0
horas_voadas_dec_pouso_GP_base2 = 0
horas_voadas_dec_pouso_GP_base3 = 0
horas_voadas_dec_pouso_GP_base4 = 0


for i in range(len(output_df)):
    for variable in prob.variables(): 
        if i < incremento and output_df['MODELO_DESTINO_base'][i] == variable.name:
            horas_voadas_dec_pouso_MP_base1 = horas_voadas_dec_pouso_MP_base1 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue  
            
        if i >= incremento and i < incremento * 2 and output_df['MODELO_DESTINO_base'][i] == variable.name:
            horas_voadas_dec_pouso_MP_base2 = horas_voadas_dec_pouso_MP_base2 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue         
    
        if i >= incremento * 2 and i < incremento * 3 and output_df['MODELO_DESTINO_base'][i] == variable.name:
            horas_voadas_dec_pouso_MP_base3 = horas_voadas_dec_pouso_MP_base3 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue        
    
        if i >= incremento * 3 and i < incremento * 4 and output_df['MODELO_DESTINO_base'][i] == variable.name:
            horas_voadas_dec_pouso_MP_base4 = horas_voadas_dec_pouso_MP_base4 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue       
    
        if i >= incremento * 4 and i < incremento * 5 and output_df['MODELO_DESTINO_base'][i] == variable.name:
            horas_voadas_dec_pouso_GP_base1 = horas_voadas_dec_pouso_GP_base1 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue          
    
        if i >= incremento * 5 and i < incremento * 6 and output_df['MODELO_DESTINO_base'][i] == variable.name:
            horas_voadas_dec_pouso_GP_base2 = horas_voadas_dec_pouso_GP_base2 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue  
    
        if i >= incremento * 6 and i < incremento * 7 and output_df['MODELO_DESTINO_base'][i] == variable.name:
            horas_voadas_dec_pouso_GP_base3 = horas_voadas_dec_pouso_GP_base3 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue         
    
        if i >= incremento * 7 and i < incremento * 8 and output_df['MODELO_DESTINO_base'][i] == variable.name:
            horas_voadas_dec_pouso_GP_base4 = horas_voadas_dec_pouso_GP_base4 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue           
              
print('')    
print(f'Horas voadas dec_pouso MP base1 mensal = {(horas_voadas_dec_pouso_MP_base1 / 7 * 30):.2f}')
print(f'Horas voadas dec_pouso GP base1 mensal = {(horas_voadas_dec_pouso_GP_base1 / 7 * 30):.2f}')

print(f'Horas voadas dec_pouso MP base2 mensal = {(horas_voadas_dec_pouso_MP_base2 / 7 * 30):.2f}')
print(f'Horas voadas dec_pouso GP base2 mensal = {(horas_voadas_dec_pouso_GP_base2 / 7 * 30):.2f}')

print(f'Horas voadas dec_pouso MP base3 mensal = {(horas_voadas_dec_pouso_MP_base3 / 7 * 30):.2f}')
print(f'Horas voadas dec_pouso GP base3 mensal = {(horas_voadas_dec_pouso_GP_base3 / 7 * 30):.2f}')

print(f'Horas voadas dec_pouso MP base4 mensal = {(horas_voadas_dec_pouso_MP_base4 / 7 * 30):.2f}')
print(f'Horas voadas dec_pouso GP base4 mensal = {(horas_voadas_dec_pouso_GP_base4 / 7 * 30):.2f}')

HORAS_VOADAS_MP_MENSAL = (horas_voadas_dec_pouso_MP_base1 + horas_voadas_dec_pouso_MP_base2 + horas_voadas_dec_pouso_MP_base3 + horas_voadas_dec_pouso_MP_base4) / 7 * 30

HORAS_VOADAS_GP_MENSAL = (horas_voadas_dec_pouso_GP_base1 + horas_voadas_dec_pouso_GP_base2 + horas_voadas_dec_pouso_GP_base3 + horas_voadas_dec_pouso_GP_base4) / 7 * 30

print('')
print(f'HORAS VOADAS MP MENSAL = {HORAS_VOADAS_MP_MENSAL:.2f}')
print(f'HORAS VOADAS GP MENSAL = {HORAS_VOADAS_MP_MENSAL:.2f}')

TOTAL_HORAS_VOADAS_MENSAL = HORAS_VOADAS_MP_MENSAL + HORAS_VOADAS_GP_MENSAL

print(f'TOTAL HORAS VOADAS MENSAL = {TOTAL_HORAS_VOADAS_MENSAL:.2f}')
print('')

# CALCULO DA FROTA
frota_MP_base1 = math.ceil(voos_MP_base1 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE1)

frota_GP_base1 = math.ceil(voos_GP_base1 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE1)

frota_MP_base2 = math.ceil(voos_MP_base2 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE2)

frota_GP_base2 = math.ceil(voos_GP_base2 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE2)

frota_MP_base3 = math.ceil(voos_MP_base3 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE3)

frota_GP_base3 = math.ceil(voos_GP_base3 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE3)

frota_MP_base4 = math.ceil(voos_MP_base4 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE4)

frota_GP_base4 = math.ceil(voos_GP_base4 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE4)

print('frota_MP_base1 = ', frota_MP_base1)
print('frota_GP_base1 = ', frota_GP_base1)

print('frota_MP_base2 = ', frota_MP_base2)
print('frota_GP_base2 = ', frota_GP_base2)

print('frota_MP_base3 = ', frota_MP_base3)
print('frota_GP_base3 = ', frota_GP_base3)

print('frota_MP_base4 = ', frota_MP_base4)
print('frota_GP_base4 = ', frota_GP_base4)
print('')

FROTA_TOTAL_MP = frota_MP_base1 + frota_MP_base2 + frota_MP_base3 + frota_MP_base4
FROTA_TOTAL_GP = frota_GP_base1 + frota_GP_base2 + frota_GP_base3 + frota_GP_base4
FROTA_TOTAL = FROTA_TOTAL_MP + FROTA_TOTAL_GP

print('FROTA TOTAL MP = ', FROTA_TOTAL_MP)
print('FROTA TOTAL GP = ', FROTA_TOTAL_GP)
print('FROTA TOTAL = ', FROTA_TOTAL)
print('')

MEDIA_HORAS_VOADAS_MP = HORAS_VOADAS_MP_MENSAL / FROTA_TOTAL_MP
MEDIA_HORAS_VOADAS_GP = HORAS_VOADAS_GP_MENSAL / FROTA_TOTAL_GP
MEDIA_HORAS_VOADAS_TOTAL = TOTAL_HORAS_VOADAS_MENSAL / FROTA_TOTAL

print(f'MEDIA HORAS VOADAS MP MENSAL = {MEDIA_HORAS_VOADAS_MP:.2f}')
print(f'MEDIA HORAS VOADAS GP MENSAL = {MEDIA_HORAS_VOADAS_GP:.2f}')
print(f'MEDIA HORAS VOADAS TOTAL MENSAL = {MEDIA_HORAS_VOADAS_TOTAL:.2f}')

print('')
depois=time.time()
print(f'Tempo de processamento igual a {depois-antes:.3f} segundos')
print('')


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




