'''
The script reads a similarity matrix file (tab separated) and a relevance vector
from files and run a the greedy algorithm XGAS from Gigli, Nardini, Lucchese, Perego
in order to select the n most relevant features which are less similar with each other.

It starts from the feature most correlated with y
Output: list of feature subsets
'''

#file paths
root='/home/asus/quickrank/data/Fold1/'
similarity_path=root+'spear_corr.txt'
relevance_path=root+'NDCG_single_feature.txt'

blacklist=[]

#set the number of feature to select
L=[7,14,27,41,54,68,102]
#L=[54]

lists=[]


#feature list will contain the feature number as int
#e.g. [99, 1, 2, 11, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 12, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 13, 121, 122, 123, 124]
#we assume feature will start from 0 and will be read as starting from 1, so 1 will be added to the output
c=0.05

for nr in L:
    
    corr_file=open(similarity_path,'r')
    
    #build a dictionary containing a similarity matrix
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
    
    #upload the relevance vector from the file

    r_file=open(relevance_path,'r')
    
    #build a dictionary containing the relevance vector
    R=dict()
    
    #skip head line
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
    
    #start from the most relevant feature
    temp=max(R, key=R.get)
    
    feature_list.append(int(temp.strip('feat')))
    
    R.pop(temp,0)
    
    while len(feature_list)<nr:
        
        param=max(1,int(round(c*len(D[temp]))))
        
        print nr, len(D[temp]), param
        
        fmin_list=sorted(D[temp], key=D[temp].get, reverse=False)[:param]
            
        for d in D:
            D[d].pop(temp,0)
        D.pop(temp,0)
        
        SubR=dict()
        for feat in fmin_list:
            SubR[feat]=R[feat]
        
        temp=max(SubR, key=SubR.get)
        feature_list.append(int(temp.strip('feat')))
        
        R.pop(temp,0)
    
    lists.append(feature_list)

print lists