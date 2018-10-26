# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pylab as plt
from func import *
import numpy as np

#%% LOAD DATA

dolphins = nx.read_gml('TC03_data/dolphins.gml')
gender = ldata('TC03_data/dolphinsGender.txt')
gender = [gender[n][1] for n in range(len(gender))]

for n,g in zip(dolphins.nodes,gender):
    dolphins.nodes[n]["gender"] = g

#%%
    
comunidades = dict()
labels = ['louvain','fast_greedy','edge_betweenness','infomap']

#%% Calculamos particiones mediante diferentes metodos

for label in labels:
    com = community(dolphins,label)
    comunidades[label]=com

#%%
    
'''
Ploteo

Cuidado al correr esta celda. Anda rarita
Corré cada label a manopla, si no, se traba.

'''
    
    
colors = ['darkred','salmon','olivedrab','lightgreen','deepskyblue',
          'darkblue','blueviolet'] 
#labels = ['louvain','fast_greedy','edge_betweenness','infomap']
l = 'louvain'

for n,c in zip(dolphins.nodes,comunidades[l]):
    dolphins.nodes[n]["comunidad"] = colors[int(c)]
plt.figure(labels.index(l))
nx.draw_networkx(dolphins,
        node_color= list(nx.get_node_attributes(dolphins,'comunidad').values()), 
        node_size=100, edge_color = 'grey', with_labels=False)
plt.title(l, loc='right',fontsize=12)
plt.axis('off')
plt.show(labels.index(l))

