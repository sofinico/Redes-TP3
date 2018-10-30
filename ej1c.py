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
gender = [gender[n][1] for n in range(len(gender))]

for n,g in zip(dolphins.nodes,gender):
    dolphins.nodes[n]['gender'] = g

#%%
    
comunidades = dict()
labels = ['louvain','fast_greedy','edge_betweenness','infomap']

#%% Calculamos particiones mediante diferentes metodos

for label in labels:
    com = community(dolphins,label)
    comunidades[label]=com

#%%
#labels = ['louvain','fast_greedy','edge_betweenness','infomap']
labels = ['infomap','fast_greedy']
acuerdo = np.zeros([len(labels),len(labels)])

for l in labels:
    for m in labels:
        acuerdo[labels.index(l)][labels.index(m)]=mutual(dolphins,list(comunidades[l]),list(comunidades[m]))
        
caract = pd.DataFrame(acuerdo)
print(caract)
#print(caract.to_latex()) 


            

        

        






    
    
