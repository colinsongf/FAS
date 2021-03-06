'''
The script reads a tab separated file representing features similarity and a file 
containing a relevance vector. Then it runs GAS in order to select the n 
most relevant features which are less similar with each other.

It starts from the feature most correlated with y.

Output: list of feature subsets containing the feature number as int
e.g. [99, 1, 2, 11, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 12, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 13, 121, 122, 123, 124]

'''
#################      INPUT      ##########################

#file path
root='/home/asus/quickrank/data/Fold1/' #change this

#similarity matrix file path
similarity_path=root+'spear_corr.txt'
#relevance vector file path
relevance_path=root+'NDCG_single_feature.txt'

#hyperparameter
c=0.01

#feature subsets to be produced, corresponding to 5%, 10%, 20%, 30%, 40%, 50%, 75% of the whole
#feature set (for MSN1 136 features)

L=[7,14,27,41,54,68]

#list of features to be excluded
blacklist=[]

############################################################

#initialize a void list
lists=[]

for nr_feat in L:
    
    print nr_feat
   
    corr_file=open(similarity_path,'r')
    
    #build a dictionary of dictionaries containing the correlation matrix
    
    '''
    D={feat1: {feat1: corr(x1,x1), feat2: corr(x1,x2),...featn:corr(x1,xn)},
       feat2: {feat1: corr(x2,x1), feat2: corr(x2,x2),...featn:corr(x2,xn)},
       ...
       featn: {feat1: corr(x2,x1), feat2: corr(x2,x2),...featn:corr(x2,xn)}}
    '''
    
    D=dict()
    
    corr_row=corr_file.readline()
    corr_row=corr_row.strip()
    
    #the similarity matrix format is tab separated
    corr_row_fields=corr_row.split('\t')
    
    #build a dictionary for every feature which is not in the blacklist
    for i in range(1,len(corr_row_fields)+1):
            feat="feat"+str(i)
            if feat not in blacklist:
                D[feat]=dict()
    
    j=1
    
    #fill the dictionary of dictionaries
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
    
    #build a dictionary containing relevance(feature(i),y)
    R=dict()
    
    #skip headline
    r_row=r_file.readline()
    
    #read the first informative line
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
     
    #initialize the feature subset list
    feature_list=[]
    
    #start from the most y-correlated feature
    temp=max(R, key=R.get)
    
    #add to the feature subset list
    feature_list.append(int(temp.strip('feat')))
    
    while len(feature_list)<nr_feat:

        #spread penalities over the remaining features through the hyperparameter
        for d in D[temp]:
            R[d]=R[d]-2*c*D[temp][d]+0
        
        #remove selected from Relevance Vector
        R.pop(temp,0)
        
        #remove selected from dictionary of dictionaries
        for d in D:
            D[d].pop(temp,0)
        D.pop(temp,0)
        
        #select the new feature to be added
        temp=max(R, key=R.get)
        
        feature_list.append(int(temp.strip('feat')))
            
    print feature_list
    lists.append(feature_list)
    
print lists