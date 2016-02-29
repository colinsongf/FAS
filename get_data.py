#read train data file from MSN dataset and produce 3 array structures for future analyses. (one for label, one for query id, one for feature)

root='C:\Users\\t000524\Documents\ex reuters\Learning to rank\FeatSel\Fold1\\'
#n=600000

#line_train_to_be_read=n
label_array=[]
query_array=[]
feat_array=[]
rpath=root+'train.txt'

feat_file=open(rpath,'r')
counter=0

feat_row=feat_file.readline()

while (feat_row!=""):
    
    feat_row=feat_row.strip()
    
    feat_row_fields=feat_row.split(':')
    
    for i in range(len(feat_row_fields)):
        #print feat_row_fields[i]
        feat_row_fields[i]=float(feat_row_fields[i].split(' ')[0])
        #print feat_row_fields[i],"\n"
    #print feat_row_fields
    
    label_array.append(feat_row_fields[0])
    query_array.append(feat_row_fields[1])
    feat_array.append(feat_row_fields[2:len(feat_row_fields)])
    counter+=1
    feat_row=feat_file.readline()

print counter

#salvo un campione di dati su un file per esplorarne le caratteristiche

with open(root+'sample_train_features.txt','w') as wfile:
    
    wfile.write("label\t")
    wfile.write("query\t")
    
    for element in range(1,len(feat_row_fields)-1):
        wfile.write("feat%s\t" % str(element))
    wfile.write("\n")
    
    for i in range(len(feat_array)):
        wfile.write("%s\t" % str(label_array[i]))
        wfile.write("%s\t" % str(query_array[i]))
        for element in range(len(feat_array[i])-1):
            wfile.write("%s\t" % str(feat_array[i][element]))
        wfile.write("%s\n" % str(feat_array[i][element+1]))
wfile.close()


n=235000
line_validation_to_be_read=n
label_array=[]
query_array=[]
feat_array=[]

rpath=root+'vali.txt'

feat_file=open(rpath,'r')
counter=0

feat_row=feat_file.readline()

while (feat_row!=""):
    
    feat_row=feat_row.strip()
    
    feat_row_fields=feat_row.split(':')
    
    for i in range(len(feat_row_fields)):
        #print feat_row_fields[i]
        feat_row_fields[i]=float(feat_row_fields[i].split(' ')[0])
        #print feat_row_fields[i],"\n"
    #print feat_row_fields
    
    label_array.append(feat_row_fields[0])
    query_array.append(feat_row_fields[1])
    feat_array.append(feat_row_fields[2:len(feat_row_fields)])
    counter+=1
    feat_row=feat_file.readline()

print counter

#print "\n\n", feat_array, "\n", query_array, "\n", label_array, "\n\n"

#salvo un campione di dati su un file per esplorarne le caratteristiche

with open(root+'sample_validation_features.txt','w') as wfile:
    
    wfile.write("label\t")
    wfile.write("query\t")
    
    for element in range(1,len(feat_row_fields)-1):
        wfile.write("feat%s\t" % str(element))
    wfile.write("\n")
    
    for i in range(len(feat_array)):
        
        wfile.write("%s\t" % str(label_array[i]))
        wfile.write("%s\t" % str(query_array[i]))

        for element in range(len(feat_array[i])-1):
            wfile.write("%s\t" % str(feat_array[i][element]))
            
        wfile.write("%s\n" % str(feat_array[i][element+1]))
        
wfile.close()

line_test_to_be_read=n
label_array=[]
query_array=[]
feat_array=[]
rpath=root+'test.txt'

feat_file=open(rpath,'r')
counter=0

feat_row=feat_file.readline()
while (feat_row!=""):

    
    feat_row=feat_row.strip()
    
    feat_row_fields=feat_row.split(':')
    
    for i in range(len(feat_row_fields)):
        #print feat_row_fields[i]
        feat_row_fields[i]=float(feat_row_fields[i].split(' ')[0])
        #print feat_row_fields[i],"\n"
    #print feat_row_fields
    
    label_array.append(feat_row_fields[0])
    query_array.append(feat_row_fields[1])
    feat_array.append(feat_row_fields[2:len(feat_row_fields)])
    counter+=1
    feat_row=feat_file.readline()

print counter
#print "\n\n", feat_array, "\n", query_array, "\n", label_array, "\n\n"

#salvo un campione di dati su un file per esplorarne le caratteristiche

with open(root+'sample_test_features.txt','w') as wfile:
    
    wfile.write("label\t")
    wfile.write("query\t")
    
    for element in range(1,len(feat_row_fields)-1):
        wfile.write("feat%s\t" % str(element))
    wfile.write("\n")
    
    for i in range(len(feat_array)):
        
        wfile.write("%s\t" % str(label_array[i]))
        wfile.write("%s\t" % str(query_array[i]))
        
        for element in range(len(feat_array[i])-1):
            wfile.write("%s\t" % str(feat_array[i][element]))
            
        wfile.write("%s\n" % str(feat_array[i][element+1]))
        
wfile.close()
