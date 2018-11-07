#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pylab as plt
from func import *
import numpy as np
from networkx.algorithms.community import modularity
import itertools

#%% LOAD DATA

dolphins = nx.read_gml('TC03_data/dolphins.gml')
gender = ldata('TC03_data/dolphinsGender.txt')


for n in dolphins.nodes:
    for g in gender:
        if g[0] == n:
            dolphins.nodes[n]['gender'] = g[1]

#%%
    
comunidades = dict()
l = 'infomap'

#%%
def plotH(data,c, bins=12, color='lightgrey'):
    freq, binedges = np.histogram(data, bins=bins)
    norm = sum(freq)
    freq_normed = [i/norm for i in freq]
    bincenters = 0.5*(binedges[1:]+binedges[:-1])
    
    mean = np.mean(data)
    stdev = np.std(data)

    plt.axvline(mean, color=color, linestyle='dotted', 
                linewidth=2)
    plt.bar(bincenters, freq_normed, color=color, alpha = 0.5, width=np.diff(binedges)*0.8)
    plt.title('%s' %c, loc = 'right',weight = 'bold')
    plt.legend(fontsize=6)
    
#%%


entrada = open('ItemB'+l+'.csv')

lines = []

for line in entrada:
    lines.append(line.split(','))
    
for line in lines:
    for i in range(1,len(line)):
        line[i] = float(line[i])

randMod = lines[0][1:]
randSil = lines[1][1:]


#%% #### Correr y plotear esto solo si hay valores muy cercanos a +-1.0
filteredSil = []
for i in range(len(randSil)):
    if randSil[i] <= 0.9 and randSil[i] >= -0.9:
        filteredSil.append(randSil[i])



#%% Calculamos particiones mediante diferentes metodos

com = community(dolphins,l)
comunidades[l]=com

parts = partit(dolphins,comunidades[l])
measured_mod = modularity(dolphins, parts)
measured_sil = np.average(list(itertools.chain(*silhouette_graph(dolphins,parts))))




#%%


plt.figure(107)
plotH(data=filteredSil,c=l, bins=12, color='dodgerblue', )
plt.axvline(measured_sil, color='dodgerblue', linestyle='solid',
            linewidth=2, label='Observado')
plt.ylabel('Frecuencia',fontsize=12)
plt.xlabel('Silouhette',fontsize=12)
plt.show()
#weight = 'bold'






















