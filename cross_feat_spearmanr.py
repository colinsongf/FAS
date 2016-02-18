from __future__ import division
from scipy import stats
import pandas as pd

root="/home/asus/quickrank/data/Fold1/"

#read train data
df=pd.read_csv(root+'sample_train_features.txt', sep='\t',header=0)#,nrows=90000)

#print df.describe()

#define Y as the label vector
Y=df['label']
#define X as the features matrix

X=df.loc[:,'feat1':'feat136']

#reset df to free space
df=0

#get a list of features names
names=list(X.columns.values)

spear_corr=[]

for i in range(len(names)):
    
    temp=[]
    #compute spearman for each pair of feature
    for j in range(len(names)):
        print "i,j: ",i,j
        if j > i:
            Xi=X.loc[:,names[i]].as_matrix()
            Xj=X.loc[:,names[j]].as_matrix()
            temp.append(stats.spearmanr(Xi,Xj)[0])
            
        elif j==i:
            temp.append(1.0)
        else:
            temp.append(spear_corr[j][i])
    
    #save spearman matrix in a file, tab separated
    with open(root+'spear_corr.txt', 'a') as f:
        for ele in temp:
            f.write("%f\t" % ele)
        f.write("\n")
    spear_corr.append(temp)