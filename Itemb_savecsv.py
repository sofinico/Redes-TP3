#!/usr/bin/env python3
# -*- coding: utf-8 -*-


labels = ['louvain','fast_greedy','edge_betweenness','infomap']


## Dejo los datos en el formato que los deseo guardar

lines_out1 = dict()


for c in labels:
    lines_out1[c]=[]
    for i in range(len(removed_nodes[c])):
        lines_out1[c].append('%.6f'%randMod[c][i])
    lines_out1[c] = ','.join(lines_out1[c])


f = open('ItemB'+'.csv','w')
    
for c in labels:
    print(c+','+'%s' % lines_out1[c], file=f)

f.close()