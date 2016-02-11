# Author: Pasan Fernando
# PhD student from University of South Dakota
# Written for the thesis project

#########################################################################################################
## this code takes a list of uberon terms as input and generates an png file showing its relationships
# Input file name: uberonlist.txt
# Is_a relationships are shown as black arrows and all other relationships are shown in red
# You need to install networkx and matplotlib packages in python to run this code

import itertools as it
import networkx as nx
import matplotlib.pyplot as plt
import re

G = nx.DiGraph()
uberon = {}
name = {}

#reading the uberon file
p = open('uberon.obo', 'r')

for line in p:
    if line.startswith('[Typedef]'):
        break

    if line.startswith('id:'):
        x = line.split()
        y = x[1]

        if G.has_node(y) == False:
            G.add_node(y)

    if line.startswith('name:'):
        k = re.sub('name: ','',line,1)
        z = k.strip()
        d = z.replace(" ","_")
        uberon[y] = d
        name[z] = y

    if line.startswith('is_a: '):
        z = line.split()
        k = z[1]
        # print k
        G.add_edge(k, y)

    elif line.startswith('relationship: ') or line.startswith('intersection_of:'):
        if 'UBERON:' in line:
            line = line.strip()
            m = 'UBERON:'+re.search('UBERON:(.+?) ', line).group(1)
            G.add_edge(m, y, color='red')

k = G.to_undirected()

#opening the uberon term list file and calculating the relationships
s = open('uberonlist.txt', 'r')
lis =[]
for line in s:
    if line!= '\n':
        x1 = line.strip()
        k1 = name[x1]
        lis.append(k1)
lis1 = []
s = []
for comb in it.combinations(lis,2):
    x,y = comb
    print x,y
    if nx.has_path(k,x,y):
        s = nx.shortest_path(k,x,y)
        lis1 =lis1+lis +s
f1 = list(set(lis1))

sub = nx.subgraph(G,f1)

for el in f1:
    sub.node[el]['label']=uberon[el]

for l in lis:
    sub.node[l]['style']='filled'
    sub.node[l]['fillcolor']='yellow'


A = nx.to_agraph(sub)
A.layout('dot')
A.draw('outputsubnetwork.png')
#print name['pectoral fin']
nx.write_dot(sub,'outputsubnetwork.dot')
