#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 19:45:47 2018

@author: sofinico
"""

import networkx as nx
import os
import rpy2.robjects as robjects
import numpy as np


def ldata(archive):
    f = open(archive)
    data = []
    for line in f:
        line = line.strip()
        col = line.split()
        data.append(col)	
    return data


def degrees(grafo, node = 'All'):
    if node == 'All':
        lista = list(dict(grafo.degree).values())
    else:
        lista = grafo.degree(node)
    return lista

def community(nxG, algorithm, fig_name = "G"):
    """
    In:
        nxG: grafo de networkx.
        algorithm: string, entre las siguientes opciones: 
            fast_greedy
            edge_betweenness
            louvain
            infomap
        fig_name: nombre de la figura que se genera al clsuterizar. Le agrega automaticamente el nombre del algoritmo usado y el nombre del grafo si lo tuviere
    Out:
        labels: numpy array con la pertenencia de cada nodo al cluster.
    
    """
    gml_file_name = "G.gml"
    fig_name += "_"+nxG.name+"_"+algorithm+".svg"
    nx.write_gml(nxG, gml_file_name)
    
    igG = robjects.r('''
        f <- function(file, algorithm, fig_name){
            require("igraph")     
            
            G <- read_graph(file, "gml")
            #format = c("edgelist", "pajek", "ncol", "lgl", "graphml","dimacs", "graphdb", "gml", "dl"), ...)
            
            if(algorithm == "fast_greedy"){
                c <- cluster_fast_greedy(G, 
                    merges = TRUE, 
                    modularity = TRUE, 
                    membership = TRUE)
            }
            
            if(algorithm == "edge_betweenness"){
                c <- cluster_edge_betweenness(G,directed = FALSE,edge.betweenness = TRUE)
            }
            
            if(algorithm == "louvain"){
                c <- cluster_louvain(G)
            }
            
            if(algorithm == "infomap"){
                c <- cluster_infomap(G)
            }
            
            svg(fig_name)
            plot(c, G)
            dev.off()
            
            return(membership(c))
        }
    ''')
    
    labels = igG(gml_file_name, algorithm, fig_name)
    os.remove(gml_file_name)
    return np.array(labels)


def grupo(graph,attribute='gender', kind='f'):
    
    '''
    Devuelve una lista de los nodos con un cierto atributo 
    '''
    
    nodes = list(dict(graph.nodes))
    group = []
    for n in nodes:
        if graph.nodes[n][attribute] == kind:
            group.append(n)
    return group


def partitions(graph, comunidades):
    part = [ [] for i in range(int(max(comunidades))+1) ]
    for a in list(zip(graph.nodes,comunidades)):
        i = int(a[1])
        part[i].append(a[0])
    return part[1:]
        


def silhouette(graph, partitions, node):
    '''
    Medida de silhouette para un nodo
    
    Graph: networkx.graph
    Partitions: iterable
    Node: Name of node.
    '''

    bs = []
    for p in partitions:
        if node in p:
            amigues = p
        
            acum = 0
            for a in amigues:
                acum += nx.shortest_path_length(graph, source=node, target=a, weight=None)   
            ai = acum/len(amigues)
            
        if node not in p:
            if len(list(nx.connected_component_subgraphs(graph))) == 1: 
                enemigues = p
                
                bcum= 0 
                for b in enemigues:
                    bcum += nx.shortest_path_length(graph, source=node, target=b, weight=None)   
                bis = bcum/len(enemigues)
                bs.append(bis)
            else:
                for g in nx.connected_component_subgraphs(graph): 
                    if node in list(g.nodes):
                        enemigues = p
                        bcum = 0 
                        for b in enemigues:
                            if b in list(g.nodes):
                                bcum += nx.shortest_path_length(g, source=node, target=b, weight=None) 
                        bis = bcum/len(enemigues)
                        bs.append(bis)
    bi = min(bs)
    M = max([ai,bi])
    sil = (bi-ai)/M
    return sil


def silhouette_graph(graph, particiones):
    siluetas = [[] for i in range(len(particiones))]
    i=0
    for p in particiones:
        siluetas[i] = [ silhouette(graph,particiones, n) for n in p ] 
        i+=1
    return siluetas
    
    

#def mutual(graph, part1, part2):
#    '''
#    Graph: Networkx graph
#    part1, part2, lista de particiones para comparar
#    '''
#    
#    pC1 = [ part1.count(i)/graph.number_of_nodes()  for i in
#              range(1,int(max(part1))+1)]
#    pC2 = [ part2.count(i)/graph.number_of_nodes()  for i in
#              range(1,int(max(part2))+1)]
#        
#    pC12 = np.zeros([len(pC1),len(pC2)])
#    sumN12 = 0
#    for a in list(zip(graph.nodes,part1)):
#        for b in list(zip(graph.nodes,part2)):
#            if a[1] == b[1]:
#                pC12[int(a[1])-1][int(b[1])-1] += 1
#                sumN12 += 1
#    pC12 = [i/sumN12 for i in pC12]
#    
#    hC1= -np.sum([i*np.log(i) for i in pC1]); hC2= -np.sum([i*np.log(i) for i in pC2])
#    
#    I = 0
#    
#    for i in range(len(pC1)-1):
#        for j in range(len(pC12)-1):
#            I += pC12[i][j] * np.log(pC12[i][j]/(pC1[i]*pC2[j]))
#            
#    In = 2*I/(hC1+hC2)
#    return In
#    
def infomutual(graph, part1, part2):
    '''
    Graph:Networkx graph
    Part1,Part2: lista de particiones ['strings'] para comparar
    '''
    N = graph.number_of_nodes()
    idx = [ (part1[i],part2[i]) for i in range(N)]
    
    pC1 = [ part1.count(i)/graph.number_of_nodes()  for i in
              range(1,int(max(part1))+1)]
    pC2 = [ part2.count(i)/graph.number_of_nodes()  for i in
              range(1,int(max(part2))+1)]
  
    pC12 = np.zeros([len(pC1),len(pC2)]) 
    for i in idx:
        pC12[int(i[0])-1][int(i[1])-1] += 1
    
    pC12 = [i/N for i in pC12 ]

    hC1= -np.sum([i*np.log(i) for i in pC1])
    hC2= -np.sum([i*np.log(i) for i in pC2])
    
    I = 0
    
    for j in range(len(pC1)):
        for k in range(len(pC2)):
            if pC12[j][k] != 0:
                I += pC12[j][k] * np.log(pC12[j][k]/(pC1[j]*pC2[k]))
    
    In = 2*I/(hC1+hC2)
    In
    return In
                                        

















