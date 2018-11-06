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
#%%
    
comunidades = dict()
labels = ['louvain','fast_greedy','edge_betweenness','infomap']

#%% Calculamos particiones mediante diferentes metodos

for label in labels:
    com = community(dolphins,label)
    comunidades[label]=com

#%% Caracterizo cada partición

labels = ['louvain','fast_greedy','edge_betweenness','infomap']

for l in labels: 
    print('Partición %s - Número de comunidades %s - Clustering Medio %s'
          % (l,max(comunidades[l]),round(clust(dolphins,comunidades[l]),2)))
  
#%%
'''
Ploteo

Cuidado al correr esta celda. Anda rarita
Corré cada label a manopla, si no, se traba.

'''
    
    
colors = ['darkred','salmon','olivedrab','lightgreen','deepskyblue',
          'darkblue','blueviolet'] 
#labels = ['louvain','fast_greedy','edge_betweenness','infomap']
l = 'infomap'

for n,c in zip(dolphins.nodes,comunidades[l]):
    dolphins.nodes[n]["comunidad"] = colors[int(c)]
plt.figure(labels.index(l))
nx.draw_networkx(dolphins,
        node_color= list(nx.get_node_attributes(dolphins,'comunidad').values()), 
        node_size=100, edge_color = 'grey', with_labels=False)
plt.title(l, loc='right',fontsize=12)
plt.axis('off')
plt.show(labels.index(l))

