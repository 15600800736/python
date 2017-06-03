# encoding=UTF-8

def connect_with(node1, node2):
    node1.neighbor.append(node2.index)
    node2.neighbor.append(node1.index)

    node1.indegree = node1.indegree + 1
    node1.outdegree = node1.outdegree + 1
    node1.degree = node1.degree + 2

    node2.indegree = node1.indegree + 1
    node2.outdegree = node2.outdegree + 1
    node2.degree = node2.degree + 2


def connect_to(node1, node2):
    node1.neighbor.append(node2.index)
    node1.indegree = node1.indegree + 1
    node1.outdegree = node1.outdegree + 1
    node1.degree = node1.degree + 2
