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

#%%

modularities = dict()
siluetas = dict() 
randMod = dict()
randSil = dict()

#%%

'''
Calculo la modularidad para cada particion obtenida.
Comparo ese valor con las modularidades obtenidas de las particiones generadas
en 1000 ('times') redes aleatorias 
'''
import datetime
from networkx.algorithms.community import modularity
import itertools
t0 = datetime.datetime.now()
times = 1000

#labels = ['louvain','fast_greedy','edge_betweenness','infomap']

l = 'louvain'

    
parts = partitions(dolphins,comunidades[l])
modularities[l] = modularity(dolphins, parts)

siluetas[l] = silhouette_graph(dolphins,parts)

random_sil = []
random_mode = []
for t in range(times):
    newG = dolphins.copy()
    newG = nx.double_edge_swap(dolphins, nswap=int(dolphins.number_of_nodes()/2), max_tries=500)
    com = community(newG,l)
    newP = partitions(dolphins,com)
    random_mode.append(modularity(newG, newP))
    random_sil.append(np.average(list(itertools.chain(*silhouette_graph(newG,newP)))))


randMod[l] = random_mode
randSil[l] = random_sil

aveSil = np.average(list(itertools.chain(*siluetas[l])))
print(datetime.datetime.now()-t0)


#%% 


'''
Ploteo

'''

#labels = ['louvain','fast_greedy','edge_betweenness','infomap']
    
l = 'louvain'

plt.figure(1)     
plt.hist(randMod[l], color='dodgerblue', normed=True, histtype='step')
plt.axvline(modularities[l],marker='d',color='c',markersize=7,label='$Modularidad$')
plt.show(1)

plt.figure(2)
plt.plot(randSil[l], marker='.', color='salmon')
plt.axhline(aveSil, color='pink', label=r'$Silhouette$')
plt.show(2)

    
#%%
