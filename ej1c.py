# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 15:25:02 2018

@author: noelp
"""

import networkx as nx
import matplotlib.pylab as plt
import pandas as pd
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
labels = ['louvain','fast_greedy','edge_betweenness','infomap']
#labels = ['infomap','fast_greedy']
info = np.zeros([len(labels),len(labels)])

for l in labels:
    for m in labels:
        info[labels.index(l)][labels.index(m)]=infomutual(dolphins,list(comunidades[l]),list(comunidades[m]))
        
caract = pd.DataFrame(info)
#print(caract)
print(caract.to_latex()) 

#%%

labels = ['louvain','fast_greedy','edge_betweenness','infomap']
#labels = ['infomap','fast_greedy']
preci = np.zeros([len(labels),len(labels)])

for l in labels:
    for m in labels:
        preci[labels.index(l)][labels.index(m)]=precision(dolphins,list(comunidades[l]),list(comunidades[m]))
        
caract = pd.DataFrame(preci)
#print(caract)
print(caract.to_latex()) 
            

        

        






    
    
