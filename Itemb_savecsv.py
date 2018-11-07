#!/usr/bin/env python3
# -*- coding: utf-8 -*-

Label = 'infomap'
carac = ['Modularity','Silhouette']

dicts = dict()

dicts['Modularity'] = randMod
dicts['Silhouette'] = randSil


## Dejo los datos en el formato que los deseo guardar

lines_out1 = dict()

for c in carac:
    lines_out1[c]=[]
    for i in range(len(randMod[Label])):
        lines_out1[c].append('%.6f'%dicts[c][Label][i])      
    lines_out1[c] = ','.join(lines_out1[c])

f = open('ItemB'+Label+'.csv','w')
    
for c in carac:
    print(c+','+'%s' % lines_out1[c], file=f)

f.close()