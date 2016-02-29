#!/usr/bin/python

import os,sys

def parse(filename):
    inddict={}
    countdict = {}
    for l in open(filename, 'r'):
        features=l.rstrip().split(' ')
        dataline = [0] * 701;
        for (i,f) in enumerate(features):
            if i==0:
                dataline[0] = int(f);
            elif i==1:
                indfeat = f.split(':')
                dataline[1] = int(indfeat[1]);
            else:
                indfeat = f.split(':')
                dataline[int(indfeat[0])+1] = indfeat[1];
    
        print ",".join(map(str,dataline))
        
if len(sys.argv)<2:
    print "Usage: python txt2csv.py train/set1.train.txt"
else:
    parse(sys.argv[1])