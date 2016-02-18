'''
Input: The script takes a relevance vector and a list of files. Each file contain the clustering of the feature set
accordingly to a cutting level.
Output: list of feature subsets
'''

import pandas as pd

L=[7,14,27,41,54,68,102]
#L=[54]

root='C:\Users\\t000524\Documents\data\Fold1\\'
relevance_path=root+'NDCG_single_feature.txt'

blacklist=[]

r_file=open(relevance_path,'r')

#build a dictionary containing relevance(feature(i),y)
R=dict()

#skip header
r_row=r_file.readline() 

r_row=r_file.readline()

r_row=r_row.strip()
r_row_fields=r_row.split('\t')

j=1
lista=[]

while (r_row != ""):
    
    feat=j
    r_row=r_row.strip()
    r_row_fields=r_row.split('\t')
    
    if feat not in blacklist:
        R[feat]=float(r_row_fields[1])
        
    j+=1
    r_row=r_file.readline()


for l in L:
    
    #leggo i file contenenti due colonne separate da virgola
    #la prima contiene il ref della feature la seconda il cluster di appartenenza
    
    '''
    ,x
    feature1,cluster(feature1)
    feature12,cluster(feature1)
    feature1,cluster(feature1)
    ...
    
    '''
    filename=root+"g"+str(l)+".txt"
    
    df=pd.read_csv(filename, sep=',',header=0,names=["mfeature", "mgroup"],skiprows=0)

    sublista=[]
    
    nr_to_select=l
    
    for i in range(1,nr_to_select+1):

        temp=df[df["mgroup"]==i]["mfeature"].as_matrix()

        a={k: R[k] for k in temp}
        sublista.append(max(a, key=a.get))
        
    print sublista
    
    lista.append(sublista)
print lista
