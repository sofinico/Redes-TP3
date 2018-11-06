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
                                        

def precision(graph,part1,part2):
    '''
    Graph:Networkx graph
    Part1,Part2: lista de particiones ['strings'] para comparar
    
    Matriz de precisión:
                    C(i,j)=C(i,j) C(i,j)!=C(i,j)
    C(i,j)=C(i,j)         a             b
    C(i,j)!=C(i,j)        c             d  
    
    Returns: Float33
    
    '''
    
    N = graph.number_of_nodes()
    idx = [ (part1[i],part2[i]) for i in range(N)]
    
    a = 0
    d = 0
    
    for i in range(N):
        for j in range(N):
            if i != j:
                if idx[i][0] == idx[j][0] and idx[i][1] == idx[j][1]:
                    a += 1
                elif idx[i][0] != idx[j][0] and idx[i][1] != idx[j][1]:
                    d += 1
   
    a = a/2
    d = d/2            
    pres = 2*(a+d)/(N*(N-1))
    return pres


def clust(graph,part):
    subGs = []
    for p in range(1,1+int(max(part))):
        subnodes=[]
        for n,idx in zip(graph.nodes,part):
            if idx == p:
                subnodes.append(n)
        subG = graph.subgraph(subnodes)
        subGs.append(subG)
    clustl = []
    number = sorted([g.number_of_nodes() for g in subGs])
    for g in subGs:       
        gn = g.number_of_nodes()
        if gn == number[-1]:
            clustl.append(nx.average_clustering(g))
        elif gn == number[:len(number)-2]:
            clustl.append(nx.average_clustering(g))
        elif gn == number[:len(number)-3]:
            clustl.append(nx.average_clustering(g))
    aveclust = np.average(clustl)
    return aveclust

    



################################ EJERCICIO D ##################################

"""
El cálculo de attribute_list puede ir adentro de bend, pero para optimizar
a la hora de hacer las iteraciones es mejor calcularla afuera y que vaya 
como parámetro.

attribute_list = []
for n in graph.nodes:
    attribute_list.append(graph.nodes[n][attribute]) 
"""    

def bend(graph, attribute_list, attribute = 'gender'):
    
    """
    Reasigna un atributo aleatoriamente manteniendo la proporción
    original del mismo.
    
    Out: 
        otro grafo idéntico pero con el atributo reasignado
    """
    
    np.random.shuffle(attribute_list)
    new = graph.copy()
    for n,g in zip(graph.nodes,attribute_list):
        new.nodes[n][attribute] = g               
    
    return new


def gendercount(graph, communities, method, it = 100):
    
    """
    Param: 
        graph: nx.Graph() al cual se le calcularon las comunidades
        communities: diccionario - key el método, values el array 
        comunidades de networkx
        method: string - el método de particiones que estamos utilizando 
        para los cálculos
        it: cantidad de iteraciones random
    
    Out:
        d: diccionario - keys las comunidades c
            d[c]['total']: la cantidad de individuos de la comunidad
            d[c]['f', 'm' o 'NA'][0] = cantidad real de ese género
            d[c]['f', 'm' o 'NA'][1:] = cantidades random      
    """ 
    
    def quantity(graph, total = False):
    
        quant = dict()
        if total:
            quant['total'] = 0
        for g in genders:
                quant[g] = 0
        for i in range(len(communities[method])):
                if communities[method][i] == c:
                    quant[graph.node[nodes[i]]['gender']] += 1
                    if total:
                        quant['total'] += 1
                
        return quant
    
    d = dict() 
    genders = ['f', 'm', 'NA']
    nodes = list(dolphins.nodes())
    
    for c in set(communities[method]):
        
        d[c] = dict()
        d[c]['total'] = 0         
        cant = quantity(graph, total = True)
        for g in genders:
            d[c][g] = []
            d[c][g].append(cant[g])
        d[c]['total'] = cant['total']
        
        attribute_list = []
        for n in graph.nodes:
            attribute_list.append(graph.nodes[n]['gender']) 
        
        new = graph
        for i in range(it):
            new = bend(new, attribute_list)
            cant = quantity(new)
            for g in genders:
                d[c][g].append(cant[g])
        
    return d


def pval(freq,bines,Tobs):
    
    """
    Calcula el pval para un cierto estadístico observado
    """
    
    bineslef = bines[:-1]
    cumprob = [sum(freq[0:i+1]) for i in range(len(freq))]
    i = 1
    if bineslef[0] >= Tobs:
        return 1
    elif bineslef[-1] < Tobs:
        return 1 - cumprob[-1]
    else:
        while bineslef[i] < Tobs:
            if i < len(bineslef)-1:
                i+=1
            else:
                break
            
        return 1 - cumprob[i-1] 
            
            
