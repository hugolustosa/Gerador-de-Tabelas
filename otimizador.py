import time
from pulp import *
import numpy as np
import pandas as pd
import math
import networkx as nx
import win32com.client as win32
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import optimize
import seaborn as sns


antes = time.time()
data_hora = time.strftime('%Y-%m-%d %Hh%Mm%Ss', time.localtime())

########################################################### 
#DADOS DE ENTRADA

cenario_geral = 1 # 1 / 2 / 3 / 4 / 5 / 6

cen_preco_qav = '5.00' # 5.00 / 4.50 / 4.00 / 0.00

cen_base_qav = 'todas_bases_aerovias_rev' # todas_bases_aerovias_rev / SBJR / SBMI / SBCB / todas_bases_sem_aerovias / cenario_estudo_reducao_sbjr / todas_bases_aerovias_rev_portoes_marica

cenario_qav = f'{cen_base_qav}_{cen_preco_qav}_reais'

cenario = f'CEN{cenario_geral}_{cen_preco_qav}_reais_{cen_base_qav}_{data_hora}'

entrada = f'INPUT_qav_{cen_preco_qav}_reais_{cen_base_qav}.xlsx'

arestas_df = pd.read_excel(entrada, sheet_name = 'arestas')

vertices_df = pd.read_excel(entrada, sheet_name = 'vertices')

unidades_df = pd.read_excel(entrada, sheet_name = 'unidades_maritimas')

output_df = pd.read_excel(entrada, sheet_name = 'aeronaves_roteiros')

DISPONIBILIDADE = 0.92 # 0.85 a 0.98 não alterou a frota
FATOR_DE_RECUPERACAO = 5 # DIAS - 4 a 7 não alterou a frota
GIRO_MAXIMO_BASE1 = 3 # VOOS / DIA  - 2.8 a 3.1 não alterou a frota
GIRO_MAXIMO_BASE2 = GIRO_MAXIMO_BASE1 # VOOS / DIA
GIRO_MAXIMO_BASE3 = GIRO_MAXIMO_BASE1 # VOOS / DIA
GIRO_MAXIMO_BASE4 = GIRO_MAXIMO_BASE1 # VOOS / DIA

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
    base2_cap_mp = 99 #10
    base3_cap_mp = 99 #20
    base4_cap_mp = 0
    
    base1_cap_gp = 0
    base2_cap_gp = 10 #10
    base3_cap_gp = 15 #15
    base4_cap_gp = 0
    
    base1_cap_total = 0
    base2_cap_total = 15 #15
    base3_cap_total = 26 #26
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

elif cenario_geral == 1.1:
    base1_cap_mp = 0
    base2_cap_mp = 0
    base3_cap_mp = 9999
    base4_cap_mp = 0
    
    base1_cap_gp = 0
    base2_cap_gp = 0
    base3_cap_gp = 9999
    base4_cap_gp = 0
    
    base1_cap_total = 0
    base2_cap_total = 0
    base3_cap_total = 9999
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

    TEMPO_MISSAO = TEMPO_VOO + TEMPO_SOLO #acionamento a corte
    output_df.at[i, 'TEMPO_MISSAO'] = TEMPO_MISSAO
    
    TEMPO_DECOLAGEM_POUSO = TEMPO_MISSAO - (output_df.loc[i]['TEMPO_ACIO_DECOL'] + output_df.loc[i]['TEMPO_POUSOCORTE']) / 60
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
       
    output_df.at[i, 'CUSTO_HORA_VOADA'] = output_df.loc[i]['PRECO_HORA_VOADA'] * output_df.loc[i]['TEMPO_DECOLAGEM_POUSO']
    
    output_df.at[i, 'CUSTO_QAV_CONSUMIDO'] = output_df.loc[i]['PRECO_QAV'] * output_df.loc[i]['COMB_MISSAO'] / 0.79 #PARA PASSAR DE KG PARA LITROS. O PREÇO DO QAV ADOTADO FOI EM R$ / LITROS   
    
    output_df.at[i, 'CUSTO_MISSAO'] = output_df.loc[i]['CUSTO_HORA_VOADA'] + output_df.loc[i]['CUSTO_QAV_CONSUMIDO']
    
    output_df.at[i, 'CUSTO_MISSAO_POR_PAX'] = output_df.at[i, 'CUSTO_MISSAO'] / (output_df.at[i, 'QUANT_PAX'] * 2)
    
output_df.to_excel(f"OUTPUT_{cenario}.xlsx")

print(f'# PLANILHA OUTPUT_{cenario}.xlsx SALVA NO DIRETORIO #')
print('')
###################################################################

print('##### OTIMIZADOR ####')
print('')

#inspirado em https://coin-or.github.io/pulp/CaseStudies/a_transportation_problem.html

# Creates a list of all the supply nodes
aeroportos = ["MP_SBJR", "GP_SBJR", "MP_SBMI", "GP_SBMI", "MP_SBCB", "GP_SBCB", "MP_SBME", "GP_SBME"]

# Creates a dictionary for the number of units of supply for each supply node
supply = {"MP_SBJR": base1_cap_mp,
          "GP_SBJR": base1_cap_gp,
          "MP_SBMI": base2_cap_mp,
          "GP_SBMI": base2_cap_gp,
          "MP_SBCB": base3_cap_mp,
          "GP_SBCB": base3_cap_gp,
          "MP_SBME": base4_cap_mp,
          "GP_SBME": base4_cap_gp}


# Creates a list of all demand nodes
unidades_maritimas=['PMLZ','PMXL','FPAR','FPIB','FPIT','FPMA','FPMR','FPPA','FPPL','FPCS','FPSP','FPSA','NS31','NS33','NS38','NS39','NS40','NS42','NS43','NS44','P_66','P_67','P_68','P_69','P_70','P_74','P_75','P_76','P_77','SS75','UMMA','UMPA','UMTJ','UMVE','SRIO','SARU','SAJA','FASA','SECR','SAON','SKST','SKAU']

# Creates a dictionary for the number of units of demand for each demand node
demand = {'PMLZ':75,'PMXL':75,'FPAR':75,'FPIB':75,'FPIT':75,'FPMA':75,'FPMR':75,'FPPA':75,'FPPL':75,'FPCS':75,'FPSP':75,'FPSA':75,'NS31':87,'NS33':87,'NS38':87,'NS39':87,'NS40':87,'NS42':87,'NS43':87,'NS44':87,'P_66':87,'P_67':87,'P_68':87,'P_69':87,'P_70':87,'P_74':87,'P_75':87,'P_76':87,'P_77':87,'SS75':87,'UMMA':250,'UMPA':250,'UMTJ':250,'UMVE':250,'SRIO':30,'SARU':30,'SAJA':30,'FASA':30,'SECR':30,'SAON':30,'SKST':30,'SKAU':30}

# Creates a list of costs of each transportation path

                    #UM1, UM2, UM3....
costs = [list(output_df['CUSTO_MISSAO'][0:42]),         # MP_BASE1
         list(output_df['CUSTO_MISSAO'][168:210]),      # GP_BASE1
         list(output_df['CUSTO_MISSAO'][42:84]),        # MP_BASE2
         list(output_df['CUSTO_MISSAO'][210:252]),      # GP_BASE2
         list(output_df['CUSTO_MISSAO'][84:126]),       # MP_BASE3
         list(output_df['CUSTO_MISSAO'][252:294]),      # GP_BASE3
         list(output_df['CUSTO_MISSAO'][126:168]),      # MP_BASE4
         list(output_df['CUSTO_MISSAO'][294:336])]      # GP_BASE4

assentos_uteis = [list(output_df['QUANT_PAX'][0:42]),    # MP_BASE1
                  list(output_df['QUANT_PAX'][168:210]), # GP_BASE1
                  list(output_df['QUANT_PAX'][42:84]),   # MP_BASE2
                  list(output_df['QUANT_PAX'][210:252]), # GP_BASE2
                  list(output_df['QUANT_PAX'][84:126]),  # MP_BASE3
                  list(output_df['QUANT_PAX'][252:294]), # GP_BASE3
                  list(output_df['QUANT_PAX'][126:168]), # MP_BASE4
                  list(output_df['QUANT_PAX'][294:336])] # GP_BASE4

# =============================================================================

# The cost data is made into a dictionary
costs = makeDict([aeroportos,unidades_maritimas],costs,0)

assentos_uteis = makeDict([aeroportos,unidades_maritimas],assentos_uteis,0)

# Creates the 'prob' variable to contain the problem data
prob = LpProblem("Problema_de_Alocacao_Voos_Plataformas",LpMinimize)


# Creates a list of tuples containing all the possible routes for transport
Routes = [(aero,UM) for aero in aeroportos for UM in unidades_maritimas]


# A dictionary called 'Vars' is created to contain the referenced variables(the routes)
vars = LpVariable.dicts("Route",(aeroportos,unidades_maritimas),0,None,LpInteger)


# The objective function is added to 'prob' first
prob += lpSum([vars[aero][UM] * costs[aero][UM] for (aero,UM) in Routes]), "Soma_dos_custos_de_transporte"


# The supply maximum constraints are added to prob for each supply node
#RESTRIÇÕES DE CAPACIDADE DOS AERÓDROMOS POR MODELO
for aero in aeroportos:
    prob += lpSum([vars[aero][UM] for UM in unidades_maritimas]) <= supply[aero] * 7, "Total_voos_base_e_modelo_%s"%aero   


#RESTRIÇÕES DE CAPACIDADE DE CADA AERÓDROMO COMO UM TODO
prob += lpSum([vars[aeroportos[0]][UM] + vars[aeroportos[1]][UM]  for UM in unidades_maritimas]) <= base1_cap_total * 7, "Total_voos_base1"     
    
prob += lpSum([vars[aeroportos[2]][UM] + vars[aeroportos[3]][UM]  for UM in unidades_maritimas]) <= base2_cap_total * 7, "Total_voos_base2"    

prob += lpSum([vars[aeroportos[4]][UM] + vars[aeroportos[5]][UM]  for UM in unidades_maritimas]) <= base3_cap_total * 7, "Total_voos_base3"    

prob += lpSum([vars[aeroportos[6]][UM] + vars[aeroportos[7]][UM]  for UM in unidades_maritimas]) <= base4_cap_total * 7, "Total_voos_base4"    
 

#RESTRIÇÃO DE ATENDIMENTO A DEMADA DE CADA PLATAFORMA 
# The demand minimum constraints are added to prob for each demand node

for UM in unidades_maritimas:
    prob += lpSum([vars[aero][UM]*assentos_uteis[aero][UM] for aero in aeroportos]) >= demand[UM], "Demanda_atendida_de_cada_UM_%s"%UM


# Escreve o modelo no arquivo
prob.writeLP("otimizavoos.lp")

# Resolve o problema
prob.solve()

# Imprime o status da resolucao
print ("Status:", LpStatus[prob.status])

# Solucoes otimas das variaveis
for variable in prob.variables():
   if variable.varValue != 0:
       print(f'{variable.name} = {variable.varValue:.0f}')
       #print ("%s = %f" % (variable.name, variable.varValue))

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
# alocacao das unidades as bases

alocacao_sbjr_mp = []
alocacao_sbmi_mp = []
alocacao_sbcb_mp = []
alocacao_sbme_mp = []

alocacao_sbjr_gp = []
alocacao_sbmi_gp = []
alocacao_sbcb_gp = []
alocacao_sbme_gp = []

for variable in prob.variables():
    if "MP_SBJR" in variable.name and variable.varValue > 0:
        alocacao_sbjr_mp.append([variable.name[-4:], variable.varValue])
    elif "GP_SBJR" in variable.name and variable.varValue > 0:
        alocacao_sbjr_gp.append([variable.name[-4:], variable.varValue])
    elif "MP_SBMI" in variable.name and variable.varValue > 0:
        alocacao_sbmi_mp.append([variable.name[-4:], variable.varValue])
    elif "GP_SBMI" in variable.name and variable.varValue > 0:
        alocacao_sbmi_gp.append([variable.name[-4:], variable.varValue])
    elif "MP_SBCB" in variable.name and variable.varValue > 0:
        alocacao_sbcb_mp.append([variable.name[-4:], variable.varValue])
    elif "GP_SBCB" in variable.name and variable.varValue > 0:
        alocacao_sbcb_gp.append([variable.name[-4:], variable.varValue])
    elif "MP_SBME" in variable.name and variable.varValue > 0:
        alocacao_sbme_mp.append([variable.name[-4:], variable.varValue])
    elif "GP_SBME" in variable.name and variable.varValue > 0:
        alocacao_sbme_gp.append([variable.name[-4:], variable.varValue])


for i in unidades_df.index:
    for j in alocacao_sbjr_mp:
        if str(unidades_df.loc[i]["unidade"]) == str(j[0]):
            unidades_df.at[i, "SBJR_MP"] = j[1]  
    for j in alocacao_sbjr_gp:
        if str(unidades_df.loc[i]["unidade"]) == str(j[0]):
            unidades_df.at[i, "SBJR_GP"] = j[1]
    unidades_df.at[i, "SBJR"] = unidades_df.loc[i]["SBJR_MP"] + unidades_df.loc[i]["SBJR_GP"]
               
    for j in alocacao_sbmi_mp:
        if str(unidades_df.loc[i]["unidade"]) == str(j[0]):
            unidades_df.at[i, "SBMI_MP"] = j[1]
    for j in alocacao_sbmi_gp:
        if str(unidades_df.loc[i]["unidade"]) == str(j[0]):
            unidades_df.at[i, "SBMI_GP"] = j[1]
    unidades_df.at[i, "SBMI"] = unidades_df.loc[i]["SBMI_MP"] + unidades_df.loc[i]["SBMI_GP"]            
            
    for j in alocacao_sbcb_mp:
        if str(unidades_df.loc[i]["unidade"]) == str(j[0]):
            unidades_df.at[i, "SBCB_MP"] = j[1]
    for j in alocacao_sbcb_gp:
        if str(unidades_df.loc[i]["unidade"]) == str(j[0]):
            unidades_df.at[i, "SBCB_GP"] = j[1]  
    unidades_df.at[i, "SBCB"] = unidades_df.loc[i]["SBCB_MP"] + unidades_df.loc[i]["SBCB_GP"]            
            
    for j in alocacao_sbme_mp:
        if str(unidades_df.loc[i]["unidade"]) == str(j[0]):
            unidades_df.at[i, "SBME_MP"] = j[1]
    for j in alocacao_sbme_gp:
        if str(unidades_df.loc[i]["unidade"]) == str(j[0]):
            unidades_df.at[i, "SBME_GP"] = j[1]
    unidades_df.at[i, "SBME"] = unidades_df.loc[i]["SBME_MP"] + unidades_df.loc[i]["SBME_GP"]           
    
    if unidades_df.loc[i]["SBJR"] >= max(unidades_df.loc[i]["SBMI"], unidades_df.loc[i]["SBCB"], unidades_df.loc[i]["SBME"]):
        unidades_df.at[i, "base"] = str("SBJR")
    if unidades_df.loc[i]["SBMI"] >= max(unidades_df.loc[i]["SBJR"], unidades_df.loc[i]["SBCB"], unidades_df.loc[i]["SBME"]):
        unidades_df.at[i, "base"] = str("SBMI")
    if unidades_df.loc[i]["SBCB"] >= max(unidades_df.loc[i]["SBJR"], unidades_df.loc[i]["SBMI"], unidades_df.loc[i]["SBME"]):
        unidades_df.at[i, "base"] = str("SBCB")
    if unidades_df.loc[i]["SBME"] >= max(unidades_df.loc[i]["SBJR"], unidades_df.loc[i]["SBMI"], unidades_df.loc[i]["SBCB"]):
        unidades_df.at[i, "base"] = str("SBME")            
        
#gráfico de bolhas com coordenadas
sns.relplot(x="long", y="lat", hue="base", size="demanda",
            sizes=(30, 800), alpha=0.7, palette="muted",
            height=5, data=unidades_df)

plt.title(f'CEN {cenario_geral} QAV R$ {cen_preco_qav} BASE: {cen_base_qav}', fontsize=10)
plt.text(-43.37, -22.9875, 'SBJR', fontsize=10)
plt.text(-42.82888889, -22.91805556, 'SBMI', fontsize=10)
plt.text(-42.07138889, -22.92083333, 'SBCB', fontsize=10)
plt.text(-41.76166667, -22.33888889, 'SBME', fontsize=10)

plt.savefig(f'MAPA_{cenario}.jpeg',
            dpi = 300,
            facecolor = 'w',
            edgecolor = 'w',
            orientation = 'landscape',
            papertype = 'b0',
            format = 'jpeg',
            transparent = True,
            bbox_inches = 'tight',
            pad_inches = 0.1,
            frameon = None,
            metadata = None)

plt.show()

#################################################################
# quantidade de assentos por modelo de aeronave e base

assentos_SBJR_GP = 0
assentos_SBJR_MP = 0
assentos_SBMI_GP = 0
assentos_SBMI_MP = 0
assentos_SBCB_GP = 0
assentos_SBCB_MP = 0
assentos_SBME_GP = 0
assentos_SBME_MP = 0


for i in output_df.index:
    for j in range(len(alocacao_sbjr_gp)):
        if output_df.loc[i]['ORIGEM'] == "SBJR" and output_df.loc[i]['MODELO'] == "GP" and output_df.loc[i]['DESTINO'] == alocacao_sbjr_gp[j][0]:
            assentos_SBJR_GP = assentos_SBJR_GP + alocacao_sbjr_gp[j][1] * output_df.loc[i]['QUANT_PAX']
            
    for j in range(len(alocacao_sbjr_mp)):
        if output_df.loc[i]['ORIGEM'] == "SBJR" and output_df.loc[i]['MODELO'] == "MP" and output_df.loc[i]['DESTINO'] == alocacao_sbjr_mp[j][0]:
            assentos_SBJR_MP = assentos_SBJR_MP + alocacao_sbjr_mp[j][1] * output_df.loc[i]['QUANT_PAX']        

    for j in range(len(alocacao_sbmi_gp)):
        if output_df.loc[i]['ORIGEM'] == "SBMI" and output_df.loc[i]['MODELO'] == "GP" and output_df.loc[i]['DESTINO'] == alocacao_sbmi_gp[j][0]:
            assentos_SBMI_GP = assentos_SBMI_GP + alocacao_sbmi_gp[j][1] * output_df.loc[i]['QUANT_PAX']
            
    for j in range(len(alocacao_sbmi_mp)):
        if output_df.loc[i]['ORIGEM'] == "SBMI" and output_df.loc[i]['MODELO'] == "MP" and output_df.loc[i]['DESTINO'] == alocacao_sbmi_mp[j][0]:
            assentos_SBMI_MP = assentos_SBMI_MP + alocacao_sbmi_mp[j][1] * output_df.loc[i]['QUANT_PAX']           

    for j in range(len(alocacao_sbcb_gp)):
        if output_df.loc[i]['ORIGEM'] == "SBCB" and output_df.loc[i]['MODELO'] == "GP" and output_df.loc[i]['DESTINO'] == alocacao_sbcb_gp[j][0]:
            assentos_SBCB_GP = assentos_SBCB_GP + alocacao_sbcb_gp[j][1] * output_df.loc[i]['QUANT_PAX']
            
    for j in range(len(alocacao_sbcb_mp)):
        if output_df.loc[i]['ORIGEM'] == "SBCB" and output_df.loc[i]['MODELO'] == "MP" and output_df.loc[i]['DESTINO'] == alocacao_sbcb_mp[j][0]:
            assentos_SBCB_MP = assentos_SBCB_MP + alocacao_sbcb_mp[j][1] * output_df.loc[i]['QUANT_PAX']           

    for j in range(len(alocacao_sbme_gp)):
        if output_df.loc[i]['ORIGEM'] == "SBME" and output_df.loc[i]['MODELO'] == "GP" and output_df.loc[i]['DESTINO'] == alocacao_sbme_gp[j][0]:
            assentos_SBME_GP = assentos_SBME_GP + alocacao_sbme_gp[j][1] * output_df.loc[i]['QUANT_PAX']
            
    for j in range(len(alocacao_sbme_mp)):
        if output_df.loc[i]['ORIGEM'] == "SBME" and output_df.loc[i]['MODELO'] == "MP" and output_df.loc[i]['DESTINO'] == alocacao_sbme_mp[j][0]:
            assentos_SBME_MP = assentos_SBME_MP + alocacao_sbme_mp[j][1] * output_df.loc[i]['QUANT_PAX']   



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
for variavel in prob.variables():
    numero_voos.append(variavel.varValue)

total_VD = len(numero_voos)
incremento = total_VD / 8

for i in range(total_VD): #verificar o ordenamento das variáveis de decisão (output em ordem alfabética)
    if i < incremento:
        voos_GP_base3 = voos_GP_base3 + numero_voos[i]

    if i >= incremento and i < incremento * 2:
        voos_GP_base1 = voos_GP_base1 + numero_voos[i]        

    if i >= incremento * 2 and i < incremento * 3:
        voos_GP_base4 = voos_GP_base4 + numero_voos[i]  

    if i >= incremento * 3 and i < incremento * 4:
        voos_GP_base2 = voos_GP_base2 + numero_voos[i]          

    if i >= incremento * 4 and i < incremento * 5:
        voos_MP_base3 = voos_MP_base3 + numero_voos[i]

    if i >= incremento * 5 and i < incremento * 6:
        voos_MP_base1 = voos_MP_base1 + numero_voos[i]        

    if i >= incremento * 6 and i < incremento * 7:
        voos_MP_base4 = voos_MP_base4 + numero_voos[i]  

    if i >= incremento * 7 and i < incremento * 8:
        voos_MP_base2 = voos_MP_base2 + numero_voos[i]          
              


TOTAL_VOOS_MP_semanal = voos_MP_base1 + voos_MP_base2 + voos_MP_base3 + voos_MP_base4
TOTAL_VOOS_GP_semanal = voos_GP_base1 + voos_GP_base2 + voos_GP_base3 + voos_GP_base4
TOTAL_VOOS_semanal = TOTAL_VOOS_MP_semanal + TOTAL_VOOS_GP_semanal



#################################################################
# CÁLCULO DAS HORAS VOADAS (DECOLAGEM A POUSO)

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
        if i < incremento and output_df['Route_MODELO_ORIGEM_DESTINO'][i] == variable.name:
            horas_voadas_dec_pouso_MP_base1 = horas_voadas_dec_pouso_MP_base1 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue  
            
        if i >= incremento and i < incremento * 2 and output_df['Route_MODELO_ORIGEM_DESTINO'][i] == variable.name:
            horas_voadas_dec_pouso_MP_base2 = horas_voadas_dec_pouso_MP_base2 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue         
    
        if i >= incremento * 2 and i < incremento * 3 and output_df['Route_MODELO_ORIGEM_DESTINO'][i] == variable.name:
            horas_voadas_dec_pouso_MP_base3 = horas_voadas_dec_pouso_MP_base3 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue        
    
        if i >= incremento * 3 and i < incremento * 4 and output_df['Route_MODELO_ORIGEM_DESTINO'][i] == variable.name:
            horas_voadas_dec_pouso_MP_base4 = horas_voadas_dec_pouso_MP_base4 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue       
    
        if i >= incremento * 4 and i < incremento * 5 and output_df['Route_MODELO_ORIGEM_DESTINO'][i] == variable.name:
            horas_voadas_dec_pouso_GP_base1 = horas_voadas_dec_pouso_GP_base1 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue          
    
        if i >= incremento * 5 and i < incremento * 6 and output_df['Route_MODELO_ORIGEM_DESTINO'][i] == variable.name:
            horas_voadas_dec_pouso_GP_base2 = horas_voadas_dec_pouso_GP_base2 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue  
    
        if i >= incremento * 6 and i < incremento * 7 and output_df['Route_MODELO_ORIGEM_DESTINO'][i] == variable.name:
            horas_voadas_dec_pouso_GP_base3 = horas_voadas_dec_pouso_GP_base3 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue         
    
        if i >= incremento * 7 and i < incremento * 8 and output_df['Route_MODELO_ORIGEM_DESTINO'][i] == variable.name:
            horas_voadas_dec_pouso_GP_base4 = horas_voadas_dec_pouso_GP_base4 + output_df['TEMPO_DECOLAGEM_POUSO'][i] * variable.varValue           
              


HORAS_VOADAS_MP_MENSAL = (horas_voadas_dec_pouso_MP_base1 + horas_voadas_dec_pouso_MP_base2 + horas_voadas_dec_pouso_MP_base3 + horas_voadas_dec_pouso_MP_base4) / 7 * 30

HORAS_VOADAS_GP_MENSAL = (horas_voadas_dec_pouso_GP_base1 + horas_voadas_dec_pouso_GP_base2 + horas_voadas_dec_pouso_GP_base3 + horas_voadas_dec_pouso_GP_base4) / 7 * 30

TOTAL_HORAS_VOADAS_MENSAL = HORAS_VOADAS_MP_MENSAL + HORAS_VOADAS_GP_MENSAL



# CALCULO DA FROTA
frota_MP_base1 = round(voos_MP_base1 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE1, 1)

frota_GP_base1 = round(voos_GP_base1 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE1, 1)

frota_MP_base2 = round(voos_MP_base2 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE2, 1)

frota_GP_base2 = round(voos_GP_base2 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE2, 1)

frota_MP_base3 = round(voos_MP_base3 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE3, 1)

frota_GP_base3 = round(voos_GP_base3 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE3, 1)

frota_MP_base4 = round(voos_MP_base4 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE4, 1)

frota_GP_base4 = round(voos_GP_base4 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERACAO) / GIRO_MAXIMO_BASE4, 1)



###########################################################
#GERACAO DE GRAFICOS

def best_fit(eixo_x, eixo_y):
    '''funcao para gerar equacao da reta
    inspirado em https://scipy-cookbook.readthedocs.io/items/FittingData.html'''      
    # Define function for calculating
    eq_reta = lambda a , x , b : a * x + b        
    ##########
    # Generate data points with noise
    ##########        
    num_points = len(eixo_x)
    
    # Note: all positive, non-zero data
        
    xdata = np.array(eixo_x)
    ydata = np.array(eixo_y)
    yerr = 0.0001 * ydata         # simulated errors (0%)
        
    ##########
    # Fitting the data -- Least Squares Method
    ##########
    #
    #  y = a * x + b
    #  
    logyerr = yerr / ydata
    
    # define our (line) fitting function
    fitfunc = lambda p, x: p[0] + p[1] * x
    errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err
    
    pinit = [1.0, -1.0]
    out = optimize.leastsq(errfunc, pinit,
                           args=(xdata, ydata, logyerr), full_output=1)
       
    coef_a = out[0][1]
    coef_b = out[0][0]
   
    return f'y = {coef_a:.4f}x + {coef_b:.2f}'

##########################################################################

distancia = output_df['valor_medio_roteiro_total'][:int(len(output_df)/2)]

payload_mp = output_df['PAYLOAD'][:int(len(output_df)/2)]
payload_gp = output_df['PAYLOAD'][int(len(output_df)/2):]

tempo_dec_pouso_mp = output_df['TEMPO_DECOLAGEM_POUSO'][:int(len(output_df)/2)]
tempo_dec_pouso_gp = output_df['TEMPO_DECOLAGEM_POUSO'][int(len(output_df)/2):]

pax_mp = output_df['QUANT_PAX'][:int(len(output_df)/2)]
pax_gp = output_df['QUANT_PAX'][int(len(output_df)/2):]

custo_pax_mp = output_df['CUSTO_MISSAO_POR_PAX'][:int(len(output_df)/2)]
custo_pax_gp = output_df['CUSTO_MISSAO_POR_PAX'][int(len(output_df)/2):]


fig1, axes = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=False, squeeze=True, subplot_kw=None, gridspec_kw=None, figsize=(12,4))

best_fit_payload_mp = best_fit(distancia, payload_mp)
best_fit_payload_gp = best_fit(distancia, payload_gp)
best_fit_tempo_voo_mp = best_fit(distancia, tempo_dec_pouso_mp)
best_fit_tempo_voo_gp = best_fit(distancia, tempo_dec_pouso_gp)

axes[0].plot(distancia, payload_gp, 'k-')
axes[0].plot(distancia, payload_gp, 'r.', label = 'payload large')
axes[0].plot(distancia, payload_mp, 'k-')
axes[0].plot(distancia, payload_mp, 'b.', label = 'payload medium')
axes[0].set_xlim(80, 200)
axes[0].set_ylim(0, 2500)
axes[0].set_title('(a) distance x payload')
axes[0].set_xlabel('half distance (nautical miles)')
axes[0].set_ylabel('payload in kg')
axes[0].text(105, 750, best_fit_payload_mp, fontsize = 9)
axes[0].text(105, 2350, best_fit_payload_gp, fontsize = 9)
axes[0].grid(False)
axes[0].legend()

axes[1].plot(distancia, tempo_dec_pouso_gp, 'k-')
axes[1].plot(distancia, tempo_dec_pouso_gp, 'r.', label = 'large flight time')
axes[1].plot(distancia, tempo_dec_pouso_mp, 'k-')
axes[1].plot(distancia, tempo_dec_pouso_mp, 'b.', label = 'medium flight time')
axes[1].set_xlim(80, 200)
axes[1].set_ylim(0, 3.5)
axes[1].set_title('(b) distance x flight time')
axes[1].set_xlabel('half distance (nautical miles)')
axes[1].set_ylabel('flight time in hours')
axes[1].text(125, 1.6, best_fit_tempo_voo_mp, fontsize = 9)
axes[1].text(85, 2.3, best_fit_tempo_voo_gp, fontsize = 9)
axes[1].grid(False)
axes[1].legend()

plt.savefig(f'parametrizacao_{cenario}.jpg',
            dpi = 300,
            facecolor = 'w',
            edgecolor = 'w',
            orientation = 'landscape',
            papertype = 'b0',
            format = 'jpg',
            transparent = True,
            bbox_inches = 'tight',
            pad_inches = 0.1,
            frameon = None,
            metadata = None)


plt.show()

###########################################################
# gráfico boxplot das meias distancias

bases = ['SBJR', 'SBMI', 'SBCB', 'SBME']

distancias_sbjr = []
distancias_sbmi = []
distancias_sbcb = []
distancias_sbme = []

for i in output_df.index:
    if output_df['ORIGEM'][i] == 'SBJR':
        distancias_sbjr.append(output_df['valor_medio_roteiro_total'][i])
    if output_df['ORIGEM'][i] == 'SBMI':
        distancias_sbmi.append(output_df['valor_medio_roteiro_total'][i])
    if output_df['ORIGEM'][i] == 'SBCB':
        distancias_sbcb.append(output_df['valor_medio_roteiro_total'][i])
    if output_df['ORIGEM'][i] == 'SBME':
        distancias_sbme.append(output_df['valor_medio_roteiro_total'][i])


distancia_bases = np.array(distancias_sbjr), np.array(distancias_sbmi), np.array(distancias_sbcb), np.array(distancias_sbme)

fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(7, 5))



# rectangular box plot
bplot1 = ax1.boxplot(distancia_bases,
                     vert=True,
                     patch_artist=False, # vertical box alignment
                     labels=bases)  # will be used to label x-ticks

bplot1 = ax1.violinplot(distancia_bases,
                  showmeans=False,
                  showmedians=False)

# add x-tick labels
plt.setp(ax1, xticks=[y + 1 for y in range(len(distancia_bases))],
         xticklabels=['SBJR', 'SBMI', 'SBCB', 'SBME'])

ax1.yaxis.grid(False)
ax1.set_ylabel('half distance (nm)')
ax1.set_ylim([0,300])

plt.savefig(f'boxplot.jpg',
            dpi = 300,
            facecolor = 'w',
            edgecolor = 'w',
            orientation = 'landscape',
            papertype = 'b0',
            format = 'jpg',
            transparent = True,
            bbox_inches = 'tight',
            pad_inches = 0.1,
            frameon = None,
            metadata = None)

plt.show()

##########################################################################
# quadro resumo

quadro_resumo = pd.DataFrame({"BASE": ["SBJR", "SBMI", "SBCB", "SBME"],
                              "FROTA_MP": [frota_MP_base1, frota_MP_base2, frota_MP_base3, frota_MP_base4],
                              "FROTA_GP": [frota_GP_base1, frota_GP_base2, frota_GP_base3, frota_GP_base4],
                              "VOOS_MP": [voos_MP_base1, voos_MP_base2, voos_MP_base3, voos_MP_base4],
                              "VOOS_GP": [voos_GP_base1, voos_GP_base2, voos_GP_base3, voos_GP_base4],
                              "HORAS_VOADAS_MP": [horas_voadas_dec_pouso_MP_base1 / 7 * 30, horas_voadas_dec_pouso_MP_base2 / 7 * 30, horas_voadas_dec_pouso_MP_base3 / 7 * 30, horas_voadas_dec_pouso_MP_base4 / 7 * 30],
                              "HORAS_VOADAS_GP": [horas_voadas_dec_pouso_GP_base1 / 7 * 30, horas_voadas_dec_pouso_GP_base2 / 7 * 30, horas_voadas_dec_pouso_GP_base3 / 7 * 30, horas_voadas_dec_pouso_GP_base4 / 7 * 30],
                              "ASSENTOS_MP": [assentos_SBJR_MP, assentos_SBMI_MP, assentos_SBCB_MP, assentos_SBME_MP],
                              "ASSENTOS_GP": [assentos_SBJR_GP, assentos_SBMI_GP, assentos_SBCB_GP, assentos_SBME_GP]})




##########################################################################
# graficos de barras (frota, voos, horas voadas e assentos))

fig2, ax = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False, squeeze=True, subplot_kw=None, gridspec_kw=None, figsize=(9,8))

labels = quadro_resumo["BASE"]

frota_mp = quadro_resumo["FROTA_MP"]
frota_gp = quadro_resumo["FROTA_GP"]

voos_mp = quadro_resumo["VOOS_MP"]
voos_gp = quadro_resumo["VOOS_GP"]

horas_voadas_mp = quadro_resumo["HORAS_VOADAS_MP"]
horas_voadas_gp = quadro_resumo["HORAS_VOADAS_GP"]

assentos_mp = quadro_resumo["ASSENTOS_MP"]
assentos_gp = quadro_resumo["ASSENTOS_GP"]


x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

rects1 = ax[0, 0].bar(x - width/2, frota_mp, width, label='medium')
rects2 = ax[0, 0].bar(x + width/2, frota_gp, width, label='large')
ax[0, 0].set_title(f'(a) Fleet - CEN {cenario_geral}')
ax[0, 0].set_xticks(x)
ax[0, 0].set_xticklabels(labels)
ax[0, 0].text(-width/1.5, frota_mp[0], frota_mp[0], fontsize = 12)
ax[0, 0].text(width/3, frota_gp[0], frota_gp[0], fontsize = 12)
ax[0, 0].text(1-width/1.5, frota_mp[1], frota_mp[1], fontsize = 12)
ax[0, 0].text(1+width/3, frota_gp[1], frota_gp[1], fontsize = 12)
ax[0, 0].text(2-width/1.5, frota_mp[2], frota_mp[2], fontsize = 12)
ax[0, 0].text(2+width/3, frota_gp[2], frota_gp[2], fontsize = 12)
ax[0, 0].text(3-width/1.5, frota_mp[3], frota_mp[3], fontsize = 12)
ax[0, 0].text(3+width/3, frota_gp[3], frota_gp[3], fontsize = 12)
ax[0, 0].legend()

rects1 = ax[0, 1].bar(x - width/2, voos_mp, width, label='medium')
rects2 = ax[0, 1].bar(x + width/2, voos_gp, width, label='large')
ax[0, 1].set_title(f'(b) Weekly flights - CEN {cenario_geral}')
ax[0, 1].set_xticks(x)
ax[0, 1].set_xticklabels(labels)
ax[0, 1].text(-width/1.5, voos_mp[0], int(voos_mp[0]), fontsize = 12)
ax[0, 1].text(width/5, voos_gp[0], int(voos_gp[0]), fontsize = 12)
ax[0, 1].text(1-width/1.5, voos_mp[1], int(voos_mp[1]), fontsize = 12)
ax[0, 1].text(1+width/5, voos_gp[1], int(voos_gp[1]), fontsize = 12)
ax[0, 1].text(2-width/1.5, voos_mp[2], int(voos_mp[2]), fontsize = 12)
ax[0, 1].text(2+width/5, voos_gp[2], int(voos_gp[2]), fontsize = 12)
ax[0, 1].text(3-width/1.5, voos_mp[3], int(voos_mp[3]), fontsize = 12)
ax[0, 1].text(3+width/5, voos_gp[3], int(voos_gp[3]), fontsize = 12)
ax[0, 1].legend()

rects1 = ax[1, 0].bar(x - width/2, horas_voadas_mp, width, label='medium')
rects2 = ax[1, 0].bar(x + width/2, horas_voadas_gp, width, label='large')
ax[1, 0].set_title(f'(c) Monthly flown hours - CEN {cenario_geral}')
ax[1, 0].set_xticks(x)
ax[1, 0].set_xticklabels(labels)
ax[1, 0].text(-width, horas_voadas_mp[0], int(horas_voadas_mp[0]), fontsize = 12)
ax[1, 0].text(width/5, horas_voadas_gp[0], int(horas_voadas_gp[0]), fontsize = 12)
ax[1, 0].text(1-width, horas_voadas_mp[1], int(horas_voadas_mp[1]), fontsize = 12)
ax[1, 0].text(1+width/5, horas_voadas_gp[1], int(horas_voadas_gp[1]), fontsize = 12)
ax[1, 0].text(2-width, horas_voadas_mp[2], int(horas_voadas_mp[2]), fontsize = 12)
ax[1, 0].text(2+width/5, horas_voadas_gp[2], int(horas_voadas_gp[2]), fontsize = 12)
ax[1, 0].text(3-width, horas_voadas_mp[3], int(horas_voadas_mp[3]), fontsize = 12)
ax[1, 0].text(3+width/5, horas_voadas_gp[3], int(horas_voadas_gp[3]), fontsize = 12)
ax[1, 0].legend()

rects1 = ax[1, 1].bar(x - width/2, assentos_mp, width, label='medium')
rects2 = ax[1, 1].bar(x + width/2, assentos_gp, width, label='large')
ax[1, 1].set_title(f'(d) Weekly boarding seats - CEN {cenario_geral}')
ax[1, 1].set_xticks(x)
ax[1, 1].set_xticklabels(labels)
ax[1, 1].text(-width, assentos_mp[0], int(assentos_mp[0]), fontsize = 12)
ax[1, 1].text(width/5, assentos_gp[0], int(assentos_gp[0]), fontsize = 12)
ax[1, 1].text(1-width, assentos_mp[1], int(assentos_mp[1]), fontsize = 12)
ax[1, 1].text(1+width/5, assentos_gp[1], int(assentos_gp[1]), fontsize = 12)
ax[1, 1].text(2-width, assentos_mp[2], int(assentos_mp[2]), fontsize = 12)
ax[1, 1].text(2+width/5, assentos_gp[2], int(assentos_gp[2]), fontsize = 12)
ax[1, 1].text(3-width, assentos_mp[3], int(assentos_mp[3]), fontsize = 12)
ax[1, 1].text(3+width/5, assentos_gp[3], int(assentos_gp[3]), fontsize = 12)
ax[1, 1].legend()



plt.savefig(f'frota_voos_horas_assentos_{cenario}.jpg',
            dpi = 300,
            facecolor = 'w',
            edgecolor = 'w',
            orientation = 'landscape',
            papertype = 'b0',
            format = 'jpg',
            transparent = True,
            bbox_inches = 'tight',
            pad_inches = 0.1,
            frameon = None,
            metadata = None)

plt.show()

###########################################################

print('')
depois=time.time()
print(f'Tempo de processamento = {depois-antes:.3f} segundos')
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
# #email.To = 'seuemail@petrobras.com.br'
# 
# #email.CC = 'seuemail@xxxxx.com.br; seuemail@xxxxx.com.br'
# 
# #email.BCC = 'seuemail@xxxxx.com.br; seuemail@xxxxx.com.br'
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
# anexo1 = f'C:/Users/kk3f/OneDrive - PETROBRAS/Desktop/Gerador de Tabelas 2.0/OUTPUT_{cenario}.xlsx'
# 
# email.Attachments.Add(anexo1)
# 
# email.Send()
# 
# print('E-mail enviado')
# =============================================================================





