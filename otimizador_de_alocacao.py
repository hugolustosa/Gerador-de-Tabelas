import time
antes = time.time()
from pulp import *
import numpy as np
import pandas as pd
import math

###################################
cenario_geral = 1
# 1 / 2 / 3 / 4 / 4.1 (SEM RESTRIÇÕES) / 5 / 6

cenario_qav = 'todas_bases_5_reais'
# todas_bases_5_reais / base1_4.5reais / base1_4reais / base2_4.5reais / base2_4reais
# base3_4.5reais / base3_4reais

DISPONIBILIDADE = 0.92
FATOR_DE_RECUPERAÇÃO = 5 #DIAS
GIRO_MÁXIMO_BASE1 = 3 # VOOS / DIA
GIRO_MÁXIMO_BASE2 = 3 # VOOS / DIA
GIRO_MÁXIMO_BASE3 = 3 # VOOS / DIA
GIRO_MÁXIMO_BASE4 = 3 # VOOS / DIA

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
    
elif cenario_geral == 4.1:
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
    base4_cap_mp = 999
    
    base1_cap_gp = 999
    base2_cap_gp = 999
    base3_cap_gp = 999
    base4_cap_gp = 999
    
    base1_cap_total = 999
    base2_cap_total = 999
    base3_cap_total = 999
    base4_cap_total = 999

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


VD=[x1,	x2,	x3,	x4,	x5,	x6,	x7,	x8,	x9,	x10,	x11,	x12,	x13,	x14,	x15,	x16,	x17,	x18,	x19,	x20,	x21,	x22,	x23,	x24,	x25,	x26,	x27,	x28,	x29,	x30,	x31,	x32,	x33,	x34,	x35,	x36,	x37,	x38,	x39,	x40,	x41,	x42,	x43,	x44,	x45,	x46,	x47,	x48,	x49,	x50,	x51,	x52,	x53,	x54,	x55,	x56,	x57,	x58,	x59,	x60,	x61,	x62,	x63,	x64,	x65,	x66,	x67,	x68,	x69,	x70,	x71,	x72,	x73,	x74,	x75,	x76,	x77,	x78,	x79,	x80,	x81,	x82,	x83,	x84,	x85,	x86,	x87,	x88,	x89,	x90,	x91,	x92,	x93,	x94,	x95,	x96,	x97,	x98,	x99,	x100,	x101,	x102,	x103,	x104,	x105,	x106,	x107,	x108,	x109,	x110,	x111,	x112,	x113,	x114,	x115,	x116,	x117,	x118,	x119,	x120,	x121,	x122,	x123,	x124,	x125,	x126,	x127,	x128,	x129,	x130,	x131,	x132,	x133,	x134,	x135,	x136,	x137,	x138,	x139,	x140,	x141,	x142,	x143,	x144,	x145,	x146,	x147,	x148,	x149,	x150,	x151,	x152,	x153,	x154,	x155,	x156,	x157,	x158,	x159,	x160,	x161,	x162,	x163,	x164,	x165,	x166,	x167,	x168,	x169,	x170,	x171,	x172,	x173,	x174,	x175,	x176,	x177,	x178,	x179,	x180,	x181,	x182,	x183,	x184,	x185,	x186,	x187,	x188,	x189,	x190,	x191,	x192,	x193,	x194,	x195,	x196,	x197,	x198,	x199,	x200,	x201,	x202,	x203,	x204,	x205,	x206,	x207,	x208,	x209,	x210,	x211,	x212,	x213,	x214,	x215,	x216,	x217,	x218,	x219,	x220,	x221,	x222,	x223,	x224,	x225,	x226,	x227,	x228,	x229,	x230,	x231,	x232,	x233,	x234,	x235,	x236,	x237,	x238,	x239,	x240,	x241,	x242,	x243,	x244,	x245,	x246,	x247,	x248,	x249,	x250,	x251,	x252,	x253,	x254,	x255,	x256,	x257,	x258,	x259,	x260,	x261,	x262,	x263,	x264,	x265,	x266,	x267,	x268,	x269,	x270,	x271,	x272,	x273,	x274,	x275,	x276,	x277,	x278,	x279,	x280,	x281,	x282,	x283,	x284,	x285,	x286,	x287,	x288,	x289,	x290,	x291,	x292,	x293,	x294,	x295,	x296,	x297,	x298,	x299,	x300,	x301,	x302,	x303,	x304,	x305,	x306,	x307,	x308,	x309,	x310,	x311,	x312,	x313,	x314,	x315,	x316,	x317,	x318,	x319,	x320,	x321,	x322,	x323,	x324,	x325,	x326,	x327,	x328,	x329,	x330,	x331,	x332,	x333,	x334,	x335,	x336]

# Importa a matriz de custos dos voos
data_custos = pd.read_excel('custos.xlsx', sheet_name = cenario_qav)

# Cria a funcao objetivo (numeros de voos (por porte e origem/destino) * custo dos voos)
prob+= np.dot(VD,data_custos['custos']),"Total custos"

#RESTRIÇÕES DE ATENDIMENTO À DEMANDA (a demand da UM(j) deve ser atendida)
#os numeros multiplicados pelas variáveis de decisão são as respectivas capacidades das aeronaves (numero de pax)
#numero zero multiplicando a variável de decisão significa que a unidade marítima não recebe aeronave daquele porte
prob+= x1*7+x169*0+x43*5+x211*0+x85*4+x253*0+x127*2+x295*0>=75,  "demanda atendida PMLZ_1"
prob+= x2*10+x170*0+x44*9+x212*0+x86*7+x254*0+x128*5+x296*0>=75,  "demanda atendida PMXL_1"
prob+= x3*7+x171*16+x45*7+x213*16+x87*7+x255*15+x129*5+x297*12>=75,  "demanda atendida FPSO_ANGRA_DOS_REIS"
prob+= x4*7+x172*15+x46*6+x214*15+x88*6+x256*14+x130*4+x298*11>=75,  "demanda atendida FPSO_ILHABELA"
prob+= x5*9+x173*18+x47*8+x215*18+x89*8+x257*18+x131*6+x299*14>=75,  "demanda atendida FPSO_ITAGUAI"
prob+= x6*8+x174*18+x48*8+x216*17+x90*8+x258*17+x132*6+x300*14>=75,  "demanda atendida FPSO_MANGARATIBA"
prob+= x7*7+x175*17+x49*7+x217*16+x91*7+x259*16+x133*5+x301*13>=75,  "demanda atendida FPSO_MARICA"
prob+= x8*8+x176*17+x50*7+x218*16+x92*7+x260*16+x134*5+x302*13>=75,  "demanda atendida FPSO_PARATY"
prob+= x9*9+x177*18+x51*9+x219*18+x93*10+x261*18+x135*8+x303*18>=75,  "demanda atendida FPSO_PIONEIRO_DE_LIBRA"
prob+= x10*11+x178*18+x52*11+x220*18+x94*11+x262*18+x136*9+x304*18>=75,  "demanda atendida FPSO_SANTOS"
prob+= x11*7+x179*15+x53*6+x221*15+x95*6+x263*14+x137*4+x305*10>=75,  "demanda atendida FPSO_SAO_PAULO"
prob+= x12*7+x180*16+x54*7+x222*16+x96*7+x264*16+x138*5+x306*13>=75,  "demanda atendida FPSO_SAQUAREMA"
prob+= x13*10+x181*18+x55*10+x223*18+x97*10+x265*18+x139*8+x307*18>=87,  "demanda atendida NS_31"
prob+= x14*10+x182*18+x56*10+x224*18+x98*10+x266*18+x140*8+x308*17>=87,  "demanda atendida NS_33"
prob+= x15*9+x183*18+x57*9+x225*18+x99*10+x267*18+x141*8+x309*17>=87,  "demanda atendida NS_38"
prob+= x16*9+x184*18+x58*9+x226*18+x100*10+x268*18+x142*8+x310*18>=87,  "demanda atendida NS_39"
prob+= x17*9+x185*18+x59*9+x227*18+x101*10+x269*18+x143*8+x311*18>=87,  "demanda atendida NS_40"
prob+= x18*9+x186*18+x60*8+x228*18+x102*8+x270*18+x144*6+x312*15>=87,  "demanda atendida NS_42"
prob+= x19*9+x187*18+x61*8+x229*18+x103*8+x271*18+x145*6+x313*14>=87,  "demanda atendida NS_43"
prob+= x20*9+x188*18+x62*8+x230*18+x104*9+x272*18+x146*7+x314*15>=87,  "demanda atendida NS_44"
prob+= x21*7+x189*16+x63*7+x231*15+x105*7+x273*15+x147*5+x315*12>=87,  "demanda atendida P_66"
prob+= x22*8+x190*17+x64*8+x232*17+x106*8+x274*17+x148*6+x316*13>=87,  "demanda atendida P_67"
prob+= x23*9+x191*18+x65*8+x233*18+x107*8+x275*18+x149*6+x317*15>=87,  "demanda atendida P_68"
prob+= x24*7+x192*16+x66*7+x234*15+x108*6+x276*15+x150*4+x318*12>=87,  "demanda atendida P_69"
prob+= x25*9+x193*18+x67*8+x235*18+x109*9+x277*18+x151*7+x319*16>=87,  "demanda atendida P_70"
prob+= x26*10+x194*18+x68*10+x236*18+x110*10+x278*18+x152*8+x320*17>=87,  "demanda atendida P_74"
prob+= x27*9+x195*18+x69*9+x237*18+x111*9+x279*18+x153*7+x321*16>=87,  "demanda atendida P_75"
prob+= x28*10+x196*18+x70*9+x238*18+x112*10+x280*18+x154*8+x322*17>=87,  "demanda atendida P_76"
prob+= x29*10+x197*18+x71*9+x239*18+x113*10+x281*18+x155*8+x323*18>=87,  "demanda atendida P_77"
prob+= x30*7+x198*15+x72*6+x240*15+x114*6+x282*14+x156*4+x324*11>=87,  "demanda atendida SS_75"
prob+= x31*10+x199*18+x73*10+x241*18+x115*10+x283*18+x157*8+x325*17>=250,  "demanda atendida UMMA"
prob+= x32*7+x200*16+x74*7+x242*15+x116*7+x284*15+x158*5+x326*12>=250,  "demanda atendida UMPA"
prob+= x33*10+x201*18+x75*9+x243*18+x117*10+x285*18+x159*8+x327*17>=250,  "demanda atendida UMTJ"
prob+= x34*10+x202*18+x76*10+x244*18+x118*11+x286*18+x160*8+x328*18>=250,  "demanda atendida UMVE"
prob+= x35*10+x203*0+x77*9+x245*0+x119*10+x287*0+x161*8+x329*0>=30,  "demanda atendida SRIO"
prob+= x36*8+x204*0+x78*7+x246*0+x120*7+x288*0+x162*5+x330*0>=30,  "demanda atendida SARU"
prob+= x37*7+x205*0+x79*6+x247*0+x121*6+x289*0+x163*4+x331*0>=30,  "demanda atendida SAJA"
prob+= x38*9+x206*0+x80*9+x248*0+x122*10+x290*0+x164*8+x332*0>=30,  "demanda atendida FASA"
prob+= x39*7+x207*0+x81*7+x249*0+x123*7+x291*0+x165*5+x333*0>=30,  "demanda atendida SECR"
prob+= x40*8+x208*0+x82*8+x250*0+x124*8+x292*0+x166*6+x334*0>=30,  "demanda atendida SAON"
prob+= x41*8+x209*0+x83*7+x251*0+x125*7+x293*0+x167*5+x335*0>=30,  "demanda atendida SKST"
prob+= x42*7+x210*0+x84*7+x252*0+x126*7+x294*0+x168*5+x336*0>=30,  "demanda atendida SKAU"

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

depois=time.time()
print(f'Tempo de processamento igual a {depois-antes:.3f} segundos')
print('')

print(f'CENARIO: {cenario_geral}')
print('')

print(f'QAV: {cenario_qav}')
print('')

valor_anual = value(prob.objective) / 7 *365
print('custo anual R$:')
print(f'{valor_anual:.0f}')

#################################################################

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
print('voos_MP_base1 = ', voos_MP_base1)
print('voos_GP_base1 = ', voos_GP_base1)

print('voos_MP_base2 = ', voos_MP_base2)
print('voos_GP_base2 = ', voos_GP_base2)

print('voos_MP_base3 = ', voos_MP_base3)
print('voos_GP_base3 = ', voos_GP_base3)

print('voos_MP_base4 = ', voos_MP_base4)
print('voos_GP_base4 = ', voos_GP_base4)
print('')

# CALCULO DA FROTA
frota_MP_base1 = math.ceil(voos_MP_base1 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERAÇÃO) / GIRO_MÁXIMO_BASE1)

frota_GP_base1 = math.ceil(voos_GP_base1 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERAÇÃO) / GIRO_MÁXIMO_BASE1)

frota_MP_base2 = math.ceil(voos_MP_base2 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERAÇÃO) / GIRO_MÁXIMO_BASE2)

frota_GP_base2 = math.ceil(voos_GP_base2 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERAÇÃO) / GIRO_MÁXIMO_BASE2)

frota_MP_base3 = math.ceil(voos_MP_base3 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERAÇÃO) / GIRO_MÁXIMO_BASE3)

frota_GP_base3 = math.ceil(voos_GP_base3 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERAÇÃO) / GIRO_MÁXIMO_BASE3)

frota_MP_base4 = math.ceil(voos_MP_base4 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERAÇÃO) / GIRO_MÁXIMO_BASE4)

frota_GP_base4 = math.ceil(voos_GP_base4 / 7 / DISPONIBILIDADE * (1 + 1 / FATOR_DE_RECUPERAÇÃO) / GIRO_MÁXIMO_BASE4)


print('frota_MP_base1 = ', frota_MP_base1)
print('frota_GP_base1 = ', frota_GP_base1)

print('frota_MP_base2 = ', frota_MP_base2)
print('frota_GP_base2 = ', frota_GP_base2)

print('frota_MP_base3 = ', frota_MP_base3)
print('frota_GP_base3 = ', frota_GP_base3)

print('frota_MP_base4 = ', frota_MP_base4)
print('frota_GP_base4 = ', frota_GP_base4)








