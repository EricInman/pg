import numpy as np
import networkx as nx
import time
import sys

# cleans ill-formatted file contents
def cleanStuff(words):
    words = words[:4]
    for i in range(len(words)):
        words[i] = words[i].strip().replace('"', "")
        if words[i].isnumeric():
            words[i] = int(words[i])
    return words


# builds a directed or undirected graph from the csv files (or gmls)
def createGraphFromCsv(filename, directed=False):
    if filename.endswith(".gml"):
        G = nx.read_gml(filename)
        sparse = nx.to_scipy_sparse_matrix(G)
        return G, sparse
    
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    
    edges = []
    with open(filename, "r") as f:
        line = f.readline()
        while line:
            thing = line.split(',')
            words = cleanStuff(thing)
            if not directed:
                edges.append((words[0], words[2]))
            else:
                if words[1] > words[3]:
                    edges.append((words[2], words[0]))
                else:
                    edges.append((words[0], words[2]))
            line = f.readline()
            
    G.add_edges_from(edges)
    sparse = nx.to_scipy_sparse_matrix(G)
    sparse = sparse.transpose()
    
    # fixes sinks, only for NCAA dataset
    if directed:
        sparseCopy = sparse.tocoo()
        colIndex = set(sparseCopy.col)
        allCols = set(np.arange(0, len(G.nodes)))
        sinkset = allCols - colIndex
        nodes = list(G.nodes)
        for index in sinkset:
            G.add_edge(nodes[index], nodes[index])
        sparse = nx.to_scipy_sparse_matrix(G)
        sparse = sparse.transpose()
        return G, sparse
    
    return G, sparse


# builds a directed graph from the txt files, which are much larger
def createGraphFromTxt(filename):
    G = nx.DiGraph()
    
    edges = []
    with open(filename, "r") as f:
        line = f.readline()
        while line:
            if not line.startswith('#'):
                nodes = line.strip().split("\t")
                edges.append((nodes[0], nodes[1]))
            line = f.readline()
    
    G.add_edges_from(edges)
    sparse = nx.to_scipy_sparse_matrix(G)
    sparse = sparse.transpose()
    sparseCopy = sparse.tocoo()
    cols = set(sparseCopy.col)
    allNodes = set(G.nodes)
    sinkset = allNodes - cols
    for node in sinkset:
        G.add_edge(node, node)
    sparse = nx.to_scipy_sparse_matrix(G)
    sparse = sparse.transpose()

    return G, sparse


# computes page rank and iterations
def pageRank(G, sparse):
    d = 0.85
    epsilon = 1e-05
    sumDiff = float("inf")
    V = G.number_of_nodes()
    curRanks = np.array([1/V] * sparse.shape[0])
    outEdges = sparse.sum(axis=0).A1
    
    iterations = 0
    while sumDiff >= epsilon:
        dividedRanks = curRanks / outEdges
        nextRanks = (1-d)/V + d * (sparse.dot(dividedRanks))
        diffs = nextRanks - curRanks
        diffs = np.abs(diffs)
        sumDiff = diffs.sum()
        curRanks = nextRanks
        iterations += 1
        
    return curRanks, iterations

# show the top nodes with their ranks
def evaluate(ranks, graph, big=False):
    order = {i: ranks[i] for i in range(len(ranks))}
    order = sorted(order.items(), key=lambda x: x[1], reverse=True)
    nodes = list(graph.nodes)
    i = 0
    for index, rank in order:
        if big and i == 30:
            break
        print(nodes[index], "with pagerank:", rank)
        i += 1

        
# driver method
if __name__ == "__main__":
    big = False
    if len(sys.argv) < 3:
        print("Error: missing arguments.")
        print("Usage: python3 pageRank.py <filename> <directed [T | F]> [big [T | F]]")
        exit(1)
    elif len(sys.argv) == 3:
        file = sys.argv[1]
        directed = sys.argv[2]
    elif len(sys.argv) == 4:
        file = sys.argv[1]
        directed = True if sys.argv[2] == "T" else False
        big = True if sys.argv[3] == "T" else False
        
    
    G = None
    sparse = None
    
    start = time.time()
    if big:
        G, sparse = createGraphFromTxt(file)
    else:
        G, sparse = createGraphFromCsv(file, directed)
    end = time.time()
    
    graphCreationTime = end - start
        
    start = time.time()
    ranks, iterations = pageRank(G, sparse)
    end = time.time()
    pageRankTime = end - start
    
    print()
    print("Graph Creation Time: ", graphCreationTime)
    print("PageRank Time: ", pageRankTime)
    print()
    evaluate(ranks, G, big)
    print()
        