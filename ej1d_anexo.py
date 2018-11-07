
"""
ANEXO ej1d.py para realizar las figuras y tablas del informe
"""

#%% HISTOGRAMAS

def histo_informe(d, c, g, bins=12, color='lightgrey', loc_pval='left'):
    
    T = d[c]['total']
    real = d[c][g][0]/T
    frac = dict()
    
    for com in d.keys():
        frac[com] = []
        for i in range(len(d[1][g][1:])):
            frac[com].append(d[com][g][i]/T)
    
    freq, binedges = np.histogram(frac[c], bins=bins)
    norm = sum(freq)
    freq_normed = [i/norm for i in freq]
    bincenters = 0.5*(binedges[1:]+binedges[:-1])
    
    mean = np.mean(frac[c])
    stdev = np.std(frac[c])
    pvalue = pval(freq_normed, binedges, real)
    
    plt.axvline(real, color=color, linestyle='solid',
                linewidth=2.5)
    plt.axvline(mean, color=color, linestyle=(0, (1, 1)), 
                linewidth=2)
    plt.bar(bincenters, freq_normed, color=color, alpha = 0.5,
            width=np.diff(binedges)*0.8)
    plt.title('Louvain', loc = 'left',
              weight='bold',fontsize=12)
    plt.title('N = %s' %T, loc = 'right',
              weight='bold',fontsize=12)
    #plt.title('%s - pval: %s' %(g,round(pvalue,3)), loc = loc_pval)

plt.figure(107)   
plt.clf()

plt.figure(107) 
plt.axvline(Nf/N, color='lightgrey', linestyle='solid',
            linewidth=1)
plt.axvline(Nm/N, color='lightgrey', linestyle='solid',
            linewidth=1)

histo_informe(d, c=3, g='m', bins=12, color='dodgerblue')
histo_informe(d, c=3, g='f', bins=12, color='r')

plt.ylabel('Frecuencia', fontsize=12)
plt.xlabel('Fracción de hembras/machos',fontsize=12)
plt.legend(fontsize=6)
plt.show()

#%% TABLA

import pandas as pd

N = dolphins.number_of_nodes()
Nf = 0
Nm = 0
for n in dolphins.nodes():
    if dolphins.nodes[n]['gender'] == 'f':
        Nf += 1
    elif dolphins.nodes[n]['gender'] == 'm':
        Nm += 1

l = 'louvain'
fg = 'fast_greedy'
b = 'edge_betweenness'
im = 'infomap'

D = dict()
metodos = [b, im, fg, l]
for met in metodos:
    d = gendercount(dolphins, comunidades, met, it = 3000)
    D[met] = d

#%%

met = im
cant = 3
com_grandes = major(D[met], cant)

sobre = []; sub = []; 
g_sobre = []; g_sub = []; 
pval_sobre = []; pval_sub = [];
mean_m = [[],[]]; mean_f = [[],[]];

for com in com_grandes:
    
    info_m = histograma(D[met], c=com, g='m', plot=False, info=True)
    info_f = histograma(D[met], c=com, g='f', plot=False, info=True)
    mean_m[0].append(info_m[1]); mean_m[1].append(info_m[2]); 
    mean_f[0].append(info_f[1]); mean_f[1].append(info_f[2]); 
    
    if info_m[1] < info_m[0]:
        sobre.append(info_m[0]); g_sobre.append('m');
        sub.append(info_f[0]); g_sub.append('f');
        pval_sobre.append(info_m[3]); pval_sub.append(info_f[3]);
              
    elif info_f[1] < info_f[0]: 
        sub.append(info_m[0]); g_sub.append('m');
        sobre.append(info_f[0]); g_sobre.append('f');
        pval_sub.append(info_m[3]); pval_sobre.append(info_f[3]);
    
    else: 
        print('algún problemilla')

despl = list()
for i in range(cant):
    if g_sobre[i] == 'm':
        despl.append((sobre[i]-mean_m[0][i])/mean_m[1][i])
    else:
        despl.append((sobre[i]-mean_f[0][i])/mean_f[1][i])

N_com_grandes = list()
for i in range(cant):
    N_com_grandes.append(D[met][com_grandes[i]]['total'])
    
media = list()
for i in range(cant):
    if g_sobre[i] == 'm':
        media.append((mean_m[0][i],mean_m[1][i]))
    else:
        media.append((mean_f[0][i],mean_f[1][i]))

        
com = 1
print('metodo', met)
print('comunidad', com)
print('total:', D[met][com]['total'])
print('real machos:', D[met][com]['m'][0])
print('real hembras:', D[met][com]['f'][0])


#%%


    
caract_im = pd.DataFrame({ 'N': N_com_grandes,
                         'media_sobre':media,
                         'fracc_sobre': sobre,                        
                         'gen_sobre': g_sobre,
                         'desplaz_resp_media': despl,
                         'p_value': pval_sobre
                        })
    
caract_im = caract_im[['N','gen_sobre','media_sobre','fracc_sobre',
                   'desplaz_resp_media','p_value']]

print(caract_im)

















