# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 17:36:31 2018

@author: noelp
"""

import networkx as nx
import matplotlib.pylab as plt
from func import *
import numpy as np

#%%


## Load data

dolphins = nx.read_gml('TC03_data/dolphins.gml')
gender = ldata('TC03_data/dolphinsGender.txt')
gender = [gender[n][1] for n in range(len(gender))]

for n,g in zip(dolphins.nodes,gender):
    dolphins.nodes[n]["gender"] = g

#%%
comunidades = dict()
labels = ['louvain','fast_greedy','edge_betweenness','infomap']

#%%

'''
ITEM A 


Encuentro las particiones a partir de los diferentes métodos

'''


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

#%%

'''
ITEM B

Falta escribir el script para silhouettes
'''   

modularities = dict()
#silhouettes = dict()  ##Todavía no hice esta parte del script
randMod = dict()


#%%

'''
Calculo la modularidad para cada particion obtenida.
Comparo ese valor con las modularidades obtenidas de las particiones generadas
en 1000 ('times') redes aleatorias 
'''

from networkx.algorithms.community import modularity

times = 1000


for l in labels:    
    for n,c in zip(dolphins.nodes,comunidades[l]):
        dolphins.nodes[n]["comunidad"] = int(c)
        
    partitions = [set(grupo(dolphins,attribute='comunidad',kind=i)) for i in
                  range(1,int(max(comunidades[l]))+1)]
    modularities[l] = modularity(dolphins, partitions)

    random_mode = []
    for t in range(times):
        newG = dolphins.copy()
        newG = nx.double_edge_swap(dolphins, nswap=int(dolphins.number_of_nodes()/2), max_tries=500)
        com = community(newG,label)
        for n,c in zip(newG.nodes,com):
            newG.nodes[n]["comunidad"] = int(c)
        partitions = [set(grupo(newG,attribute='comunidad',kind=i)) for i in
                      range(1,int(max(com))+1)]
        random_mode.append(modularity(newG, partitions))
    
    randMod[l] = random_mode
    
#%% 


'''
Ploteo

Corré cada label a manopla, si no, se traba.
'''
#labels = ['louvain','fast_greedy','edge_betweenness','infomap']
    
l = 'louvain'

plt.figure(labels.index(l))     
plt.hist(randMod[l], color='dodgerblue', normed=True, histtype='step')
plt.axvline(modularities[l],marker='d',color='c',markersize=7,label=r'$Modularidad$')
plt.show(labels.index(l))
    

#%%
    







