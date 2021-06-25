import time
from pulp import *
import numpy as np
import pandas as pd
import math
import networkx as nx
import win32com.client as win32

'''inspirado em https://coin-or.github.io/pulp/CaseStudies/a_transportation_problem.html '''

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
print('')
###################################################################

print('##### OTIMIZADOR ####')
print('')

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
unidades_maritimas=['PMLZ_1','PMXL_1','FPSO_ANGRA_DOS_REIS','FPSO_ILHABELA','FPSO_ITAGUAI','FPSO_MANGARATIBA','FPSO_MARICA','FPSO_PARATY','FPSO_PIONEIRO_DE_LIBRA','FPSO_SANTOS','FPSO_SAO_PAULO','FPSO_SAQUAREMA','NS_31','NS_33','NS_38','NS_39','NS_40','NS_42','NS_43','NS_44','P_66','P_67','P_68','P_69','P_70','P_74','P_75','P_76','P_77','SS_75','UMMA','UMPA','UMTJ','UMVE','SRIO','SARU','SAJA','FASA','SECR','SAON','SKST','SKAU']

# Creates a dictionary for the number of units of demand for each demand node
demand = {'PMLZ_1':75,'PMXL_1':75,'FPSO_ANGRA_DOS_REIS':75,'FPSO_ILHABELA':75,'FPSO_ITAGUAI':75,'FPSO_MANGARATIBA':75,'FPSO_MARICA':75,'FPSO_PARATY':75,'FPSO_PIONEIRO_DE_LIBRA':75,'FPSO_SANTOS':75,'FPSO_SAO_PAULO':75,'FPSO_SAQUAREMA':75,'NS_31':87,'NS_33':87,'NS_38':87,'NS_39':87,'NS_40':87,'NS_42':87,'NS_43':87,'NS_44':87,'P_66':87,'P_67':87,'P_68':87,'P_69':87,'P_70':87,'P_74':87,'P_75':87,'P_76':87,'P_77':87,'SS_75':87,'UMMA':250,'UMPA':250,'UMTJ':250,'UMVE':250,'SRIO':30,'SARU':30,'SAJA':30,'FASA':30,'SECR':30,'SAON':30,'SKST':30,'SKAU':30}

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
prob += lpSum([vars[aero][UM]*costs[aero][UM] for (aero,UM) in Routes]), "Soma_dos_custos_de_transporte"


# The supply maximum constraints are added to prob for each supply node
#RESTRIÇÕES DE CAPACIDADE DOS AERÓDROMOS POR MODELO
for aero in aeroportos:
    prob += lpSum([vars[aero][UM] for UM in unidades_maritimas]) <= supply[aero] * 7, "Total_voos_base_e_modelo_%s"%aero   


#RESTRIÇÕES DE CAPACIDADE DE CADA AERÓDROMO COMO UM TODO
prob += lpSum([vars[aeroportos[0]][UM] + vars[aeroportos[1]][UM]  for UM in unidades_maritimas]) <= base1_cap_total * 7, "Total_voos_base1_%s"     
    
prob += lpSum([vars[aeroportos[2]][UM] + vars[aeroportos[3]][UM]  for UM in unidades_maritimas]) <= base2_cap_total * 7, "Total_voos_base2_%s"    

prob += lpSum([vars[aeroportos[4]][UM] + vars[aeroportos[5]][UM]  for UM in unidades_maritimas]) <= base3_cap_total * 7, "Total_voos_base3_%s"    

prob += lpSum([vars[aeroportos[6]][UM] + vars[aeroportos[7]][UM]  for UM in unidades_maritimas]) <= base4_cap_total * 7, "Total_voos_base4_%s"    
 

#RESTRIÇÃO DE ATENDIMENTO A DEMADA DE CADA PLATAFORMA 
# The demand minimum constraints are added to prob for each demand node
for UM in unidades_maritimas:
    prob += lpSum([vars[aero][UM]*assentos_uteis[aero][UM] for aero in aeroportos]) >= demand[UM], "Sum_of_Products_into_Bar%s"%UM


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

TOTAL_VOOS_MP_semanal = voos_MP_base1 + voos_MP_base2 + voos_MP_base3 + voos_MP_base4
TOTAL_VOOS_GP_semanal = voos_GP_base1 + voos_GP_base2 + voos_GP_base3 + voos_GP_base4
TOTAL_VOOS_semanal = TOTAL_VOOS_MP_semanal + TOTAL_VOOS_GP_semanal

print('TOTAL VOOS MP semanal = ', TOTAL_VOOS_MP_semanal)
print('TOTAL VOOS GP semanal = ', TOTAL_VOOS_GP_semanal)
print('TOTAL VOOS semanal = ', TOTAL_VOOS_semanal)
print('')

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

TOTAL_HORAS_VOADAS_MENSAL = HORAS_VOADAS_MP_MENSAL + HORAS_VOADAS_GP_MENSAL

print('')
print(f'HORAS VOADAS MP MENSAL = {HORAS_VOADAS_MP_MENSAL:.2f}')
print(f'HORAS VOADAS GP MENSAL = {HORAS_VOADAS_GP_MENSAL:.2f}')
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
# anexo1 = f'C:/Users/kk3f/Desktop/Gerador de Tabelas2.0/{OUTPUT_{cenario}.xlsx}'
# 
# email.Attachments.Add(anexo1)
# 
# email.Send()
# 
# print('E-mail enviado')
# =============================================================================





