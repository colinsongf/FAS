
from __future__ import division
from scipy import histogram, digitize, stats, mean
from collections import defaultdict

import pandas as pd
import scipy as sc
import numpy as np

from math import log
log2 = lambda x:log(x,2)

def mutual_information(x,y):
    ce, hx=conditional_entropy(x,y)
    hy=entropy(y)
    return hy - ce

def norm_mutual_information(x,y):
    ce, hx=conditional_entropy(x,y)
    hy=entropy(y)
    return (hy - ce)/sc.sqrt(hx*hy)
    
def conditional_entropy(x, y):
    """
    x: vettore di numeri reali
    y: vettore di interi
    calcola H(Y|X)
    """
    # discretizzazione di X
    
    hx, bx= histogram(x, bins=x.size/10, density=True)

    Py= compute_distribution(y)
    
    Px= compute_distribution(digitize(x,bx))
    
    res= 0
    for ey in set(y):
        # P(X | Y)
        x1 = x[y==ey]
        condPxy= compute_distribution(digitize(x1,bx))

        for k, v in condPxy.iteritems():
            res+= (v*Py[ey]*(log2(Px[k]) - log2(v*Py[ey])))
    
    en_x=entropy(digitize(x,bx))
    
    return res, en_x
        
def entropy(y):
    """
    Calcola l'entropia di un vettore di discreti
    """
    # P(Y)
    Py= compute_distribution(y)
    res=0.0
    for k, v in Py.iteritems():
        res+=v*log2(v)
    return -res

def compute_distribution(v):
    """
    v: vettore di interi
    
    ottengo un dictionary con chiave pari all'intero e valore pari alla probabilità 
    """
    d= defaultdict(int)
    for e in v: d[e]+=1
    s= float(sum(d.values()))
    return dict((k, v/s) for k, v in d.items())


root="/home/asus/quickrank/data/Webscope_C14B/" #Data directory

print "Reading from ", root

df=pd.read_csv(root+'sample_train.txt', sep='\t',header=0)#,nrows=400000)
print len(df)

Y=df['label']
X=df.loc[:,'feat1':'feat699'] #le feature dioendono dal dataset

names=list(X.columns.values)

Y0=Y.as_matrix()
norm_miscore=[]
kendall_score=[]
spearman_score=[]

for i in range(len(names)):
    print "Spear,NMI,Ken",i
    X0=X.loc[:,names[i]].as_matrix()
    spearman_score.append(stats.spearmanr(X0,Y0)[0])
    norm_miscore.append(norm_mutual_information(X0, Y0))
    #kendall_score.append(0)
    kendall_score.append(stats.kendalltau(X0,Y0)[0])

AGvar=[]

#calcolo i gruppi

nrs=set(Y0)
idx=[]
for i in range(len(nrs)):
    idx.append(Y[Y == float(i)].index.tolist())


for i in range(len(names)):
    print "ag", i
    N=len(X.loc[:,names[i]].as_matrix())
    
    feature_mean=mean(X.loc[:,names[i]].as_matrix())
    
    TSS=sum([(xx-feature_mean)**2 for xx in X.loc[:,names[i]].as_matrix()])
    SSDX=0    

    for j in range(len(nrs)):
        Ng=len(X.loc[idx[j],names[i]].as_matrix())
        # variation between groups (X for 'cross')
        SSDX+=Ng*(mean(X.loc[idx[j],names[i]].as_matrix())-feature_mean)**2
    AGvar.append(1-SSDX/TSS)
    
with open(root+'feature_rank.txt','w') as wfile:
    wfile.write("label\tNMI\tAG1\tKen\tSpea\n")
    for i in range(len(names)):
        wfile.write("%s\n" % (str(names[i])+
                              "\t"+str(norm_miscore[i])+
                              "\t"+str(-log(AGvar[i]))+
                              "\t"+ str(np.abs(kendall_score[i]))+
                              "\t"+ str(np.abs(spearman_score[i]))
                              )
                    )
wfile.close()


from matplotlib.pyplot import barh,plot,yticks,show,xlabel,figure

figure(figsize=(8,35))
wscores = zip(names,norm_miscore)
wmi = sorted(wscores,key=lambda x:x[1]) 
topmi = zip(*wmi[-len(names):])
x = range(len(topmi[1]))
labels = topmi[0]
barh(x,topmi[1],align='center',alpha=.2,color='g')
plot(topmi[1],x,'-o',markersize=2,alpha=.8,color='g')
yticks(x,labels)
xlabel('Normalized Mutual Information')
show()

figure(figsize=(8,35))
wscores = zip(names,np.abs(kendall_score))
wmi = sorted(wscores,key=lambda x:x[1]) 
topmi = zip(*wmi[-len(names):])
x = range(len(topmi[1]))
labels = topmi[0]
barh(x,topmi[1],align='center',alpha=.2,color='g')
plot(topmi[1],x,'-o',markersize=2,alpha=.8,color='g')
yticks(x,labels)
xlabel('Kendall\'s tau')
show()

figure(figsize=(8,35))
wscores = zip(names,np.abs(spearman_score))
wmi = sorted(wscores,key=lambda x:x[1]) 
topmi = zip(*wmi[-len(names):])
x = range(len(topmi[1]))
labels = topmi[0]
barh(x,topmi[1],align='center',alpha=.2,color='g')
plot(topmi[1],x,'-o',markersize=2,alpha=.8,color='g')
yticks(x,labels)
xlabel('spearman_score')
show()

figure(figsize=(8,35))
wscores = zip(names,[-log(x) for x in AGvar])
wmi = sorted(wscores,key=lambda x:x[1]) 
topmi = zip(*wmi[-len(names):])
x = range(len(topmi[1]))
labels = topmi[0]
barh(x,topmi[1],align='center',alpha=.2,color='g')
plot(topmi[1],x,'-o',markersize=2,alpha=.8,color='g')
yticks(x,labels)
xlabel('-log(1-SSDX/TSS)')
show()

