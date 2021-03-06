#adaptated from https://github.com/discobot/LambdaMart/blob/acb8329ab63a45d2bcb43055fa54f14b8c6725c1/mart.py 

import math
import numpy as np
import csv
from optparse import OptionParser
from sklearn.tree import DecisionTreeRegressor
from multiprocessing import Pool
from itertools import chain
import pandas as pd

class Ensemble:
    def __init__(self, rate):
        self.trees = []
        self.rate = rate

    def __len__(self):
        return len(self.trees)

    def add(self, tree):
        self.trees.append(tree)

    def eval_one(self, object):
        return self.eval([object])[0]

    def eval(self, objects):
        results = np.zeros(len(objects))
        for tree in self.trees:
            results += tree.predict(objects) * self.rate
        return results

    def remove(self, number):
        self.trees = self.trees[:-number]


def groupby(score, query):
    result = []
    this_query = None
    this_list = -1
    for s, q in zip(score, query):
        if q != this_query:
            result.append([])
            this_query = q
            this_list += 1
        result[this_list].append(s)
    result = map(np.array, result)
    return result


def compute_point_dcg(arg):
    rel, i = arg
    return (2 ** rel - 1) / math.log(i + 2, 2)


def compute_point_dcg2(arg):
    rel, i = arg
    if i == 0:
        return rel
    else:
        return rel / (math.log(1 + i, 2))
    return


def compute_dcg(array):
    dcg = map(compute_point_dcg, zip(array, range(len(array))))
    return sum(dcg)


def compute_ndcg(page, k=10):
    idcg = compute_dcg(np.sort(page)[::-1][:k])
    dcg = compute_dcg(page[:k])

    if idcg == 0:
        return 1

    return dcg / idcg


def ndcg(prediction, true_score, query, k=10):
    true_pages = groupby(true_score, query)
    pred_pages = groupby(prediction, query)

    total_ndcg = []
    for q in range(len(true_pages)):
        total_ndcg.append(compute_ndcg(true_pages[q][np.argsort(pred_pages[q])[::-1]], k))
    return sum(total_ndcg) / len(total_ndcg)


def query_lambdas(page):
    true_page, pred_page = page
    worst_order = np.argsort(true_page)
    true_page = true_page[worst_order]
    pred_page = pred_page[worst_order]

    page = true_page[np.argsort(pred_page)]
    idcg = compute_dcg(np.sort(page)[::-1])
    position_score = np.zeros((len(true_page), len(true_page)))

    for i in xrange(len(true_page)):
        for j in xrange(len(true_page)):
            position_score[i, j] = compute_point_dcg((page[i], j))

    lambdas = np.zeros(len(true_page))

    for i in xrange(len(true_page)):
        for j in xrange(len(true_page)):
                if page[i] > page[j]:

                    delta_dcg = position_score[i][j] - position_score[i][i]
                    delta_dcg += position_score[j][i] - position_score[j][j]

                    delta_ndcg = abs(delta_dcg / idcg)

                    rho = 1 / (1 + math.exp(page[i] - page[j]))
                    lam = rho * delta_ndcg

                    lambdas[i] -= lam
                    lambdas[j] += lam
    return lambdas


def compute_lambdas(prediction, true_score, query, k=10):
    true_pages = groupby(true_score, query)
    pred_pages = groupby(prediction, query)

    print len(true_pages), "pages"

    pool = Pool()
    lambdas = pool.map(query_lambdas, zip(true_pages, pred_pages))
    return list(chain(*lambdas))


def mart_responces(prediction, true_score):
    return true_score - prediction


def learn(train_file, validation_file, n_trees=10, learning_rate=0.1, k=10):
    print "Loading train file"
    print train_file
    print validation_file
    train = np.loadtxt(train_file, delimiter="\t", skiprows=0)
    validation = np.loadtxt(validation_file, delimiter="\t", skiprows=0)

    scores = train[:, 0]
    val_scores = validation[:, 0]

    queries = train[:, 1]
    val_queries = validation[:, 1]

    features = train[:, 2:]
    val_features = validation[:, 2:]

    ensemble = Ensemble(learning_rate)

    print "Training starts..."
    model_output = np.array([float(0)] * len(features))
    val_output = np.array([float(0)] * len(validation))

    
    #time.clock()
    
    for i in range(n_trees):
        print " Iteration: " + str(i + 1)

        # Compute psedo responces (lambdas)
        # witch act as training label for document
        
        #start = time.clock()
        print "  --generating labels"
        #lambdas = compute_lambdas(model_output, scores, queries, k)
        lambdas = mart_responces(model_output, scores)
        #print "  --done", str(time.clock() - start) + "sec"

        # create tree and append it to the model
        print "  --fitting tree"
        #start = time.clock()
        tree = DecisionTreeRegressor(max_depth=2)
        
        #print "Distinct lambdas", set(lambdas)
        tree.fit(features, lambdas)

        #print "  ---done", str(time.clock() - start) + "sec"
        print "  --adding tree to ensemble"
        ensemble.add(tree)

        # update model score
        print "  --generating step prediction"
        prediction = tree.predict(features)

        print "  --updating full model output"
        model_output += learning_rate * prediction

        # train_score
        print "  --scoring on train"
        train_score = ndcg(model_output, scores, queries, 10)
        print "  --iteration train score " + str(train_score) 
        
        # validation score
        print "  --scoring on validation"
        val_output += learning_rate * tree.predict(val_features)
        val_score = ndcg(val_output, val_scores, val_queries, 10)

        print "  --iteration validation score " + str(val_score)


    print "Finished successfully."
    print "------------------------------------------------"
    return ensemble


def evaluate(model, fn,i):
    predict = np.loadtxt(fn, delimiter="\t", skiprows=1)
    
    true_label=predict[:, 0]
    queries = predict[:, 1]
    features = predict[:, 2:]

    results = model.eval(features)
    ndcg_at_k=ndcg(results,true_label,queries,10)
    
    path='C:\Users\\t000524\Documents\data\Fold1\\results_'+i+'.txt'
    
    with open(path,'w') as csvfile:
        writer = csv.writer(csvfile)
        for line in zip(queries, results, true_label):
            writer.writerow(line)
    csvfile.close()

    return ndcg_at_k


def feat_ranker(feat_number,measure_name):
    
    feat_rank_path='C:\Users\\t000524\Documents\data\Fold1\\feature_rank.txt'
    
    df=pd.read_csv(feat_rank_path,
                   sep="\t",
                   skiprows=0,
                   usecols=[measure_name],
                   header=0)

    df["feat_nr"]=range(1,len(df)+1)
    
    result = df.sort([measure_name], ascending=False)
    
    return result['feat_nr'].head(n=feat_number).tolist()


def average_ndcg(rpath,k):
    #mean absolut error macroaveraging
    
    df=pd.read_csv(rpath,sep=",",skiprows=0,header=0)
    
    cases=set(df.iloc[:,0].tolist())

    ndcg=[]
    
    for i in cases:
        subdf = df[(df.iloc[:,0] == i)]
    
    maem=[]
    print "MAEM: ", maem
    return maem


def get_selected_features(feature_list, train_path, vali_path, test_path):
    
    feature_labels=["label","query"]
    
    for i in feature_list:
        feature_labels.append(str(i))
    
    print train_path
    print feature_list
    
    print "Leggo train..."
    
    df=pd.read_csv(train_path,
                   sep="\t",
                   skiprows=0,
                   usecols=feature_labels,
                   header=0)
    
    
    print "Salvo train..."
    df.to_csv("C:\Users\\t000524\Documents\data\Fold1\\selected_train_features.txt",sep="\t",header=False,index=False)
    
    print "Leggo vali..."
    df=pd.read_csv(vali_path,
                   sep="\t",
                   skiprows=0,
                   usecols=feature_labels,
                   header=0)
    
    print "Salvo vali..."
    df.to_csv("C:\Users\\t000524\Documents\data\Fold1\\selected_validation_features.txt",sep="\t",header=False,index=False)
    
    print "Leggo test..."
    df=pd.read_csv(test_path,
                   sep="\t",
                   skiprows=0,
                   usecols=feature_labels,
                   header=0)
    
    print "Salvo test..."
    df.to_csv("C:\Users\\t000524\Documents\data\Fold1\\selected_test_features.txt",sep="\t",header=False,index=False)

if __name__ == "__main__":
    
    parser = OptionParser()
    
    parser.add_option("-t", "--train", action="store", type="string", dest="train_file")
    parser.add_option("-v", "--validation", action="store", type="string", dest="val_file")
    parser.add_option("-p", "--predict", action="store", type="string", dest="predict_file")

    options, args = parser.parse_args()
    
    learning_rate = 0.1
    ndcg_at_k_matrix=[]
    
    #trials=range(1,137)
    measures=["NDCG"]
    
    trials=[]
    
    for i in range(1,137):
        feat="feat"+str(i)
        print "includo ", feat
        trials.append(feat)
    
    for measure in measures:
        
        ndcg_at_k_list=[]
        
        for nr_feat_to_select in trials:
            
            feat_list=[]
            feat_list.append(nr_feat_to_select)
            
            print feat_list

            get_selected_features(feat_list, options.train_file, options.val_file, options.predict_file)
            print "Learning..."
            model = learn("C:\Users\\t000524\Documents\data\Fold1\\selected_train_features.txt", "C:\Users\\t000524\Documents\data\Fold1\\selected_validation_features.txt", n_trees=100)
            print "Evaluating..."
            ndcg_at_k=evaluate(model, "C:\Users\\t000524\Documents\data\Fold1\\selected_test_features.txt",str(nr_feat_to_select))
            ndcg_at_k_list.append(ndcg_at_k)

        print ndcg_at_k_list
        
        ndcg_at_k_matrix.append(ndcg_at_k_list)
        
    print ndcg_at_k_matrix
