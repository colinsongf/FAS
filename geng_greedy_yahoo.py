'''
The script reads a similarity matrix file (tab separated) and a relevance vector
from files and run a greedy algorithm from GENG et al.  in order to select the n 
most relevant features which are less similar with each other.
It starts from the feature most correlated with y

Output: list of feature subsets
'''

#################      INPUT      ##########################

#files path
root='/home/asus/quickrank/data/Webscope_C14B/'

#similarity matrix file path
similarity_path=root+'spear_corr.txt'
#relevance vector file path
relevance_path=root+'NDCG_single_feature.txt'

#hyperparameter
c=0.01

#feature subsets to be produced, corresponding to 5%, 10%, 20%, 30%, 40%, 50%, 75% of the whole
#feature set (for yahoo 519 features)

L=[26,52,104,156,208,260,389]

blacklist=["feat3","feat4","feat5","feat13","feat14","feat15","feat16","feat19","feat24","feat35","feat38","feat40","feat42","feat49","feat50","feat51","feat52","feat54","feat57","feat59","feat61","feat63","feat65","feat68","feat72","feat73","feat84","feat90","feat92","feat93","feat94","feat95","feat103","feat105","feat109","feat112","feat113","feat115","feat116","feat118","feat119","feat130","feat134","feat136","feat142","feat148","feat156","feat171","feat180","feat183","feat184","feat185","feat188","feat194","feat198","feat200","feat203","feat207","feat209","feat210","feat211","feat213","feat214","feat217","feat218","feat221","feat237","feat249","feat250","feat252","feat258","feat263","feat269","feat270","feat272","feat273","feat278","feat280","feat293","feat296","feat303","feat306","feat307","feat310","feat314","feat315","feat318","feat327","feat328","feat334","feat336","feat343","feat346","feat351","feat357","feat360","feat365","feat368","feat370","feat371","feat373","feat380","feat386","feat396","feat402","feat403","feat406","feat407","feat409","feat411","feat413","feat415","feat419","feat420","feat422","feat424","feat449","feat460","feat462","feat464","feat466","feat467","feat471","feat482","feat484","feat490","feat491","feat496","feat501","feat503","feat506","feat509","feat510","feat516","feat520","feat522","feat523","feat524","feat526","feat530","feat536","feat543","feat547","feat549","feat551","feat552","feat553","feat560","feat567","feat573","feat576","feat577","feat582","feat584","feat588","feat593","feat597","feat599","feat601","feat609","feat617","feat619","feat626","feat630","feat632","feat635","feat646","feat649","feat651","feat652","feat653","feat655","feat662","feat667","feat668","feat672","feat673","feat675","feat679","feat684"]

############################################################

#initialize a void list
lists=[]

for nr_feat in L:
    print nr_feat
    
    corr_file=open(similarity_path,'r')
    
    #build a dictionary containing correlation matrix
    D=dict()
    
    corr_row=corr_file.readline()
    corr_row=corr_row.strip()
    corr_row_fields=corr_row.split('\t')
        
    for i in range(1,len(corr_row_fields)+1):
            feat="feat"+str(i)
            if feat not in blacklist:
                D[feat]=dict()
    
    j=1
    
    while (corr_row != ""):
        corr_row=corr_row.strip()
        corr_row_fields=corr_row.split('\t')
        for i in range(0,len(corr_row_fields)):
            feat1="feat"+str(j)
            feat2="feat"+str(i+1)
            if (feat1 not in blacklist) and (feat2 not in blacklist):
                if feat1!=feat2:
                    D[feat1][feat2]=abs(float(corr_row_fields[i]))
        j+=1
        corr_row=corr_file.readline()

    '''
    get D={feat1: {feat1: corr(x1,x1), feat2: corr(x1,x2),...featn:corr(x1,xn)},
           feat2: {feat1: corr(x2,x1), feat2: corr(x2,x2),...featn:corr(x2,xn)},
           ...
           featn: {feat1: corr(x2,x1), feat2: corr(x2,x2),...featn:corr(x2,xn)}}
    
    example:
    In [26]: D['feat1']['feat2']
    Out[26]: '0.041894'
    '''

    #upload (Xi,Y) correlation vector saved in a file
    r_file=open(relevance_path,'r')
    
    #build a dictionary containing corr(xi,y)
    R=dict()
    
    #skip first line
    r_row=r_file.readline()
    
    r_row=r_file.readline()
        
    r_row=r_row.strip()
    r_row_fields=r_row.split('\t')
    
    j=1
    
    while (r_row != ""):
        feat="feat"+str(j)
        r_row=r_row.strip()
        r_row_fields=r_row.split('\t')
        if feat not in blacklist:
            R[feat]=abs(float(r_row_fields[1]))
        j+=1
        r_row=r_file.readline()
    
    
    feature_list=[]
    
    #start from the most y-correlated feature
    temp=max(R, key=R.get)
    feature_list.append(int(temp.strip('feat')))
    
    while len(feature_list)<nr_feat:
        
        for d in D[temp]:
            R[d]=R[d]-2*c*D[temp][d]
                
        R.pop(temp,0)
        
        for d in D:
            D[d].pop(temp,0)

        D.pop(temp,0)
        
        temp=max(R, key=R.get)
        
        feature_list.append(int(temp.strip('feat')))
            
    lists.append(feature_list)
    
print lists