import time
antes = time.time()
from pulp import *
import numpy as np
import pandas as pd

###################################
cenario_geral = 1
# 1 / 2 / 3 / 4 / 5 / 6

cenario_qav = 'todas_bases_5_reais'
# todas_bases_5_reais / base1_4.5reais / base1_4reais / base2_4.5reais / base2_4reais
# base3_4.5reais / base3_4reais

##################################

if cenario_geral == 1:
    base1_cap_mp = 20
    base2_cap_mp = 7
    base3_cap_mp = 20
    base4_cap_mp = 0
    
    base1_cap_gp = 15
    base2_cap_gp = 7
    base3_cap_gp = 15
    base4_cap_gp = 0
    
    base1_cap_total = 26
    base2_cap_total = 14
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
    base2_cap_mp = 7
    base3_cap_mp = 0
    base4_cap_mp = 0
    
    base1_cap_gp = 15
    base2_cap_gp = 7
    base3_cap_gp = 0
    base4_cap_gp = 0
    
    base1_cap_total = 26
    base2_cap_total = 14
    base3_cap_total = 0
    base4_cap_total = 0         

elif cenario_geral == 4:
    base1_cap_mp = 0
    base2_cap_mp = 7
    base3_cap_mp = 20
    base4_cap_mp = 0
    
    base1_cap_gp = 0
    base2_cap_gp = 7
    base3_cap_gp = 15
    base4_cap_gp = 0
    
    base1_cap_total = 0
    base2_cap_total = 14
    base3_cap_total = 26
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
prob+= x1*8+x169*0+x43*6+x211*0+x85*5+x253*0+x127*3+x295*0>=75,  "demanda atendida PMLZ_1"
prob+= x2*11+x170*0+x44*10+x212*0+x86*8+x254*0+x128*6+x296*0>=75,  "demanda atendida PMXL_1"
prob+= x3*8+x171*17+x45*8+x213*17+x87*8+x255*16+x129*6+x297*13>=75,  "demanda atendida FPSO_ANGRA_DOS_REIS"
prob+= x4*8+x172*16+x46*7+x214*16+x88*7+x256*15+x130*5+x298*12>=75,  "demanda atendida FPSO_ILHABELA"
prob+= x5*10+x173*18+x47*9+x215*18+x89*9+x257*18+x131*7+x299*15>=75,  "demanda atendida FPSO_ITAGUAI"
prob+= x6*9+x174*18+x48*9+x216*18+x90*9+x258*18+x132*7+x300*15>=75,  "demanda atendida FPSO_MANGARATIBA"
prob+= x7*8+x175*18+x49*8+x217*17+x91*8+x259*17+x133*6+x301*14>=75,  "demanda atendida FPSO_MARICA"
prob+= x8*9+x176*18+x50*8+x218*17+x92*8+x260*17+x134*6+x302*14>=75,  "demanda atendida FPSO_PARATY"
prob+= x9*10+x177*18+x51*10+x219*18+x93*11+x261*18+x135*9+x303*18>=75,  "demanda atendida FPSO_PIONEIRO_DE_LIBRA"
prob+= x10*12+x178*18+x52*12+x220*18+x94*12+x262*18+x136*10+x304*18>=75,  "demanda atendida FPSO_SANTOS"
prob+= x11*8+x179*16+x53*7+x221*16+x95*7+x263*15+x137*5+x305*11>=75,  "demanda atendida FPSO_SAO_PAULO"
prob+= x12*8+x180*17+x54*8+x222*17+x96*8+x264*17+x138*6+x306*14>=75,  "demanda atendida FPSO_SAQUAREMA"
prob+= x13*11+x181*18+x55*11+x223*18+x97*11+x265*18+x139*9+x307*18>=87,  "demanda atendida NS_31"
prob+= x14*11+x182*18+x56*11+x224*18+x98*11+x266*18+x140*9+x308*18>=87,  "demanda atendida NS_33"
prob+= x15*10+x183*18+x57*10+x225*18+x99*11+x267*18+x141*9+x309*18>=87,  "demanda atendida NS_38"
prob+= x16*10+x184*18+x58*10+x226*18+x100*11+x268*18+x142*9+x310*18>=87,  "demanda atendida NS_39"
prob+= x17*10+x185*18+x59*10+x227*18+x101*11+x269*18+x143*9+x311*18>=87,  "demanda atendida NS_40"
prob+= x18*10+x186*18+x60*9+x228*18+x102*9+x270*18+x144*7+x312*16>=87,  "demanda atendida NS_42"
prob+= x19*10+x187*18+x61*9+x229*18+x103*9+x271*18+x145*7+x313*15>=87,  "demanda atendida NS_43"
prob+= x20*10+x188*18+x62*9+x230*18+x104*10+x272*18+x146*8+x314*16>=87,  "demanda atendida NS_44"
prob+= x21*8+x189*17+x63*8+x231*16+x105*8+x273*16+x147*6+x315*13>=87,  "demanda atendida P_66"
prob+= x22*9+x190*18+x64*9+x232*18+x106*9+x274*18+x148*7+x316*14>=87,  "demanda atendida P_67"
prob+= x23*10+x191*18+x65*9+x233*18+x107*9+x275*18+x149*7+x317*16>=87,  "demanda atendida P_68"
prob+= x24*8+x192*17+x66*8+x234*16+x108*7+x276*16+x150*5+x318*13>=87,  "demanda atendida P_69"
prob+= x25*10+x193*18+x67*9+x235*18+x109*10+x277*18+x151*8+x319*17>=87,  "demanda atendida P_70"
prob+= x26*11+x194*18+x68*11+x236*18+x110*11+x278*18+x152*9+x320*18>=87,  "demanda atendida P_74"
prob+= x27*10+x195*18+x69*10+x237*18+x111*10+x279*18+x153*8+x321*17>=87,  "demanda atendida P_75"
prob+= x28*11+x196*18+x70*10+x238*18+x112*11+x280*18+x154*9+x322*18>=87,  "demanda atendida P_76"
prob+= x29*11+x197*18+x71*10+x239*18+x113*11+x281*18+x155*9+x323*18>=87,  "demanda atendida P_77"
prob+= x30*8+x198*16+x72*7+x240*16+x114*7+x282*15+x156*5+x324*12>=87,  "demanda atendida SS_75"
prob+= x31*11+x199*18+x73*11+x241*18+x115*11+x283*18+x157*9+x325*18>=250,  "demanda atendida UMMA"
prob+= x32*8+x200*17+x74*8+x242*16+x116*8+x284*16+x158*6+x326*13>=250,  "demanda atendida UMPA"
prob+= x33*11+x201*18+x75*10+x243*18+x117*11+x285*18+x159*9+x327*18>=250,  "demanda atendida UMTJ"
prob+= x34*11+x202*18+x76*11+x244*18+x118*12+x286*18+x160*9+x328*18>=250,  "demanda atendida UMVE"
prob+= x35*11+x203*0+x77*10+x245*0+x119*11+x287*0+x161*9+x329*0>=30,  "demanda atendida SRIO"
prob+= x36*9+x204*0+x78*8+x246*0+x120*8+x288*0+x162*6+x330*0>=30,  "demanda atendida SARU"
prob+= x37*8+x205*0+x79*7+x247*0+x121*7+x289*0+x163*5+x331*0>=30,  "demanda atendida SAJA"
prob+= x38*10+x206*0+x80*10+x248*0+x122*11+x290*0+x164*9+x332*0>=30,  "demanda atendida FASA"
prob+= x39*8+x207*0+x81*8+x249*0+x123*8+x291*0+x165*6+x333*0>=30,  "demanda atendida SECR"
prob+= x40*9+x208*0+x82*9+x250*0+x124*9+x292*0+x166*7+x334*0>=30,  "demanda atendida SAON"
prob+= x41*9+x209*0+x83*8+x251*0+x125*8+x293*0+x167*6+x335*0>=30,  "demanda atendida SKST"
prob+= x42*8+x210*0+x84*8+x252*0+x126*8+x294*0+x168*6+x336*0>=30,  "demanda atendida SKAU"


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

print('custo anual R$:')

valor_anual = value(prob.objective) / 7 *365

print(f'{valor_anual:.0f}')

