#!/usr/bin/env python3
# -*- coding: utf-8 -*-

label = 'LITr'

entrada = open('ItemB'+label+'.csv')

lines = []

for line in entrada:
    lines.append(line.split(','))
    
for line in lines:
    for i in range(1,len(line)):
        line[i] = float(line[i])
i = 0
x = dict()
while i < len(lines):
    x[lines[i][0]] = lines[i][1:]
    i += 1

#%%



