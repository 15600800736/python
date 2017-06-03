# encoding=UTF-8

class Node:
    index = None
    indegree = 0
    outdegree = 0
    degree = 0
    neighbor = []
    def __int__(self, indegree, outdegree, index):
        self.index = index
        self.indegree = indegree
        self.outdegree = outdegree
        degree = self.indegree + self.outdegree

def comparation(node1,node2):
    return cmp(node1.degree, node2.degree)