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
                    linewidth=2, label=g+' real')
        plt.axvline(mean, color=color, linestyle='dotted', 
                    linewidth=2, label=g+' prom')
        plt.bar(bincenters, freq_normed, color=color, alpha = 0.5,
                label=g+' random', width=np.diff(binedges)*0.8)
        plt.title('N = %s' %T, loc = 'right')
        plt.title('%s - pval: %s' 
                  %(g,round(pvalue,3)), 
                  loc = loc_pval)
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

d = gendercount(dolphins, comunidades, fg, it = 3000)

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
    histograma(d, c=i, g='m', bins=12, color='dodgerblue')
    histograma(d, c=i, g='f', bins=12, color='r', loc_pval='center')
    plt.axvline(Nf/N, color='r', linestyle='solid',
                linewidth=1, label='f total')
    plt.axvline(Nm/N, color='dodgerblue', linestyle='solid',
                linewidth=1, label='m total')
    plt.legend(fontsize=6)
    plt.show()

#%% ESTO ES LOS QUE ESTOY HACIENDO RIGHT NOW

''' Cuantificación de la correlación género-comunidad '''

com_grandes = major(d, cant=3)
prom_sobre = 0; prom_sub = 0;
pval_sobre = 0; pval_sub = 0;

for com in com_grandes:
    info_m = histograma(d, c=com, g='m', plot=False, info=True)
    info_f = histograma(d, c=com, g='f', plot=False, info=True)
    
    if info_m[1] < info_m[0]:
        prom_sobre += info_m[0]
    elif 
        prom_sub += info_m
        
        


















