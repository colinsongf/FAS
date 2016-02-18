import pandas as pd

L=[26,52,104,156,208,260,389]
#L=[208]
root='C:\Users\\t000524\Documents\data\Webscope_C14B\\'

blacklist=["feat3","feat4","feat5","feat13","feat14","feat15","feat16","feat19","feat24","feat35","feat38","feat40","feat42","feat49","feat50","feat51","feat52","feat54","feat57","feat59","feat61","feat63","feat65","feat68","feat72","feat73","feat84","feat90","feat92","feat93","feat94","feat95","feat103","feat105","feat109","feat112","feat113","feat115","feat116","feat118","feat119","feat130","feat134","feat136","feat142","feat148","feat156","feat171","feat180","feat183","feat184","feat185","feat188","feat194","feat198","feat200","feat203","feat207","feat209","feat210","feat211","feat213","feat214","feat217","feat218","feat221","feat237","feat249","feat250","feat252","feat258","feat263","feat269","feat270","feat272","feat273","feat278","feat280","feat293","feat296","feat303","feat306","feat307","feat310","feat314","feat315","feat318","feat327","feat328","feat334","feat336","feat343","feat346","feat351","feat357","feat360","feat365","feat368","feat370","feat371","feat373","feat380","feat386","feat396","feat402","feat403","feat406","feat407","feat409","feat411","feat413","feat415","feat419","feat420","feat422","feat424","feat449","feat460","feat462","feat464","feat466","feat467","feat471","feat482","feat484","feat490","feat491","feat496","feat501","feat503","feat506","feat509","feat510","feat516","feat520","feat522","feat523","feat524","feat526","feat530","feat536","feat543","feat547","feat549","feat551","feat552","feat553","feat560","feat567","feat573","feat576","feat577","feat582","feat584","feat588","feat593","feat597","feat599","feat601","feat609","feat617","feat619","feat626","feat630","feat632","feat635","feat646","feat649","feat651","feat652","feat653","feat655","feat662","feat667","feat668","feat672","feat673","feat675","feat679","feat684"]

rpath=root+'NDCG_single_feature.txt'

r_file=open(rpath,'r')

#build a dictionary containing corr(xi,y)
R=dict()

r_row=r_file.readline() #skip header

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

for slot in L:
        
    filename=root+"g_"+str(slot)+".txt"
    
    df=pd.read_csv(filename, sep=',',header=0,names=["mfeature", "mgroup"],skiprows=0)
    
    sublista=[]
    
    nr_to_select=slot
    
    for i in range(1,nr_to_select+1):
        temp=df[df["mgroup"]==i]["mfeature"].as_matrix()
        a={k: R[k] for k in temp}
        sublista.append(max(a, key=a.get))
    print sublista
    lista.append(sublista)
print lista
