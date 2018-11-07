# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pylab as plt
from func import *
import numpy as np

#%% LOAD DATA

dolphins = nx.read_gml('TC03_data/dolphins.gml')
gender = ldata('TC03_data/dolphinsGender.txt')

for n in dolphins.nodes:
    for g in gender:
        if g[0] == n:
            dolphins.nodes[n]['gender'] = g[1]    

#%% Calculamos particiones mediante diferentes metodos
    
comunidades = dict()
labels = ['louvain','fast_greedy','edge_betweenness','infomap']

for label in labels:
    com = community(dolphins,label)
    comunidades[label]=com
    
#%% Función ploteo
    
def ploteo(metodo):  
    colors = ['darkred','salmon','olivedrab','lightgreen','deepskyblue',
              'darkblue','blueviolet']         
    for n,c in zip(dolphins.nodes,comunidades[metodo]):
        dolphins.nodes[n]["comunidad"] = colors[int(c)]
    plt.figure(labels.index(metodo))
    nx.draw_networkx(dolphins,
            node_color= list(nx.get_node_attributes(dolphins,'comunidad').values()), 
            node_size=100, edge_color = 'grey', with_labels=False)
    plt.title(metodo, loc='right',fontsize=12)
    plt.axis('off')
    plt.show(labels.index(metodo))

l = 'louvain'
fg = 'fast_greedy'
b = 'edge_betweenness'
im = 'infomap'

#%%

def applyHistoStyle(color = 'lightgrey'):
    pass
    

def histograma(d, c, g='f', plot=True, info=False,
               bins=12, color='lightgrey', loc_pval='left'):
    
    T = d[c]['total']
    real = d[c][g][0]/T
    frac = dict()
    
    for com in d.keys():
        frac[com] = []
        for i in range(len(d[1][g][1:])):
            frac[com].append(d[com][g][i]/T)
    
    freq, binedges = np.histogram(frac[c], bins=bins)
    norm = sum(freq)
    freq_normed = [i/norm for i in freq]
    bincenters = 0.5*(binedges[1:]+binedges[:-1])
    
    mean = np.mean(frac[c])
    stdev = np.std(frac[c])
    pvalue = pval(freq_normed, binedges, real)
    
    if plot:
        plt.axvline(real, color=color, linestyle='solid',
                    linewidth=2.5, label=g+' real')
        plt.axvline(mean, color=color, linestyle=(0, (1, 1)), 
                    linewidth=2, label=g+' prom')
        plt.bar(bincenters, freq_normed, color=color, alpha = 0.5,
                label=g+' random', width=np.diff(binedges)*0.8)
        plt.title('N = %s' %T, loc = 'right')
        plt.title('%s - pval: %s' %(g,round(pvalue,3)), loc = loc_pval)
        plt.legend(fontsize=6)
    
    if info:
        return real, mean, stdev, pvalue 
    
    
def major(d, cant=3):
    
    a = dict()    
    for i in d.keys():
        a[d[i]['total']] = i
    coms = sorted([a[x] for x in sorted(a.keys())[-cant:]])
    
    return coms
    
#%% 

''' Proporción de generos en las comunidades '''

d = gendercount(dolphins, comunidades, b, it = 3000)

N = dolphins.number_of_nodes()
Nf = 0
Nm = 0
for n in dolphins.nodes():
    if dolphins.nodes[n]['gender'] == 'f':
        Nf += 1
    elif dolphins.nodes[n]['gender'] == 'm':
        Nm += 1
    
#%%
        
''' Histogramas '''

com_grandes = major(d, cant=3)
    
for i in com_grandes:
    plt.figure(i)   
    plt.clf()

for i in com_grandes:
    plt.figure(i)
    plt.axvline(Nf/N, color='lightgrey', linestyle='solid',
                linewidth=1, label='f total')
    plt.axvline(Nm/N, color='lightgrey', linestyle='solid',
                linewidth=1, label='m total')
    histograma(d, c=i, g='m', bins=10, color='dodgerblue')
    histograma(d, c=i, g='f', bins=10, color='r', loc_pval='center')
    plt.legend(fontsize=6)
    plt.show()

#%% 

''' Cuantificación de la correlación género-comunidad 
    info: real, mean, stdev, pvalue (fracciones)
'''

# comunidades que voy a considerar para los cálculos
cant = 3
com_grandes = major(d, cant)

# listas con fracciones de genero sobre y sub respresentado de cada comunidad
sobre = []; sub = []; 
# el género al que corresponden esas fracciones
g_sobre = []; g_sub = []; 
# el pval de las fracciones sub y sobre representadas de cada comunidad
pval_sobre = []; pval_sub = [];
# el promedio de las tiradas random para cada comunidad y genero
mean_m = [[],[]]; mean_f = [[],[]];

for com in com_grandes:
    
    info_m = histograma(d, c=com, g='m', plot=False, info=True)
    info_f = histograma(d, c=com, g='f', plot=False, info=True)
    mean_m[0].append(info_m[1]); mean_m[1].append(info_m[2]); 
    mean_f[0].append(info_f[1]); mean_f[1].append(info_f[2]); 
    
    if info_m[1] < info_m[0]:
        sobre.append(info_m[0]); g_sobre.append('m');
        sub.append(info_f[0]); g_sub.append('f');
        pval_sobre.append(info_m[3]); pval_sub.append(info_f[3]);
              
    elif info_f[1] < info_f[0]: 
        sub.append(info_m[0]); g_sub.append('m');
        sobre.append(info_f[0]); g_sobre.append('f');
        pval_sub.append(info_m[3]); pval_sobre.append(info_f[3]);
    
    else: 
        print('algún problemilla')















