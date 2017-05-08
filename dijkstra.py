from collections import defaultdict
from heapq import *

M =9999
M_topo = [
[M, 1,1,M,10,M, 1,1,6,M,M, M,M,M,M,M, M,M,M,M,M],
[1, M,1,M,M,1, M,M,M,M,M, M,M,M,M,M, M,M,M,M,M],
[1, 1,M,1,M,M, M,M,M,M,M, M,M,M,M,M, M,M,M,M,M],
[M, M,1,M,1,M, M,M,M,M,M, M,M,M,M,M, M,M,M,M,M],
[1, M,M,1,M,M, M,M,M,1,1, 1,M,M,M,M, M,M,M,M,M],
[M, 1,M,M,M,M, 1,M,M,M,M, M,M,M,M,M, M,M,M,M,M],
[1, M,M,M,M,1, M,1,M,M,M, M,M,M,M,M, M,M,M,M,M],
[1, M,M,M,M,M, 1,M,1,M,M, M,M,M,M,M, M,M,M,M,M],
[1, M,M,M,M,M, M,1,M,1,M, M,1,M,M,M, M,M,M,M,M],
[M, M,M,M,1,M, M,M,1,M,M, 1,M,M,M,M, M,M,M,M,M],
[M, M,M,M,1,M, M,M,M,M,M, 1,M,1,M,M, M,M,M,M,M],
[M, M,M,M,1,M, M,M,M,1,1, M,M,1,1,M, M,M,M,M,M],
[M, M,M,M,M,M, M,M,1,M,M, M,M,M,1,M, M,M,M,M,M],
[M, M,M,M,M,M, M,M,M,M,1, 1,M,M,1,M, M,1,1,M,M],
[M, M,M,M,M,M, M,M,M,M,M, 1,1,1,M,1, 1,M,M,M,M],
[M, M,M,M,M,M, M,M,M,M,M, M,M,M,1,M, 1,M,1,1,M],
[M, M,M,M,M,M, M,M,M,M,M, M,M,M,1,1, M,M,M,M,1],
[M, M,M,M,M,M, M,M,M,M,M, M,M,1,M,M, M,M,1,M,M],
[M, M,M,M,M,M, M,M,M,M,M, M,M,1,M,1, M,1,M,1,M],
[M, M,M,M,M,M, M,M,M,M,M, M,M,M,M,1, M,M,1,M,1],
[M, M,M,M,M,M, M,M,M,M,M, M,M,M,M,M, 1,M,M,1,M]
]

def dijkstra_raw(edges, from_node, to_node):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))
    q, seen = [(0,from_node,())], set()
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 in to_node:
                return cost,path
            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost+c, v2, path))
    return float("inf"),[]

def dijkstra(edges, from_node, to_node):
    len_shortest_path = -1
    ret_path=[]
    length,path_queue = dijkstra_raw(edges, from_node, to_node)
    if len(path_queue)>0:
        len_shortest_path = length      ## 1. Get the length firstly;
        ## 2. Decompose the path_queue, to get the passing nodes in the shortest path.
        left = path_queue[0]
        ret_path.append(left)       ## 2.1 Record the destination node firstly;
        right = path_queue[1]
        while len(right)>0:
            left = right[0]
            ret_path.append(left)   ## 2.2 Record other nodes, till the source-node.
            right = right[1]
        ret_path.reverse()  ## 3. Reverse the list finally, to make it be normal sequence.
    return len_shortest_path,ret_path

def dij_mat(vertexes, edges, to_node):
    print "Calculating DIJ"
    maxnum = len(vertexes)
    dij_cost = []
    for i in range(maxnum):
        dij_cost.append(999999)
    g = defaultdict(list)
    for l, r, c in edges:
        g[l].append((c, r))
    for i in range(maxnum):
        q, seen = [(0, i)], set()
        while q:
            (cost, v1) = heappop(q)
            if v1 not in seen:
                seen.add(v1)
            if v1 in to_node:
                dij_cost[i] = cost
                break
            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost + c, v2))
    return dij_cost

if __name__ == "__main__":
    edges = []
    for i in range(len(M_topo)):
        for j in range(len(M_topo[0])):
            if i!=j and M_topo[i][j]!=M:
                edges.append((i,j,M_topo[i][j]))### (i,j) is a link

    print "=== Dijkstra ==="
    print "Let's find the shortest-path from 0 to 9:"
    length,Shortest_path = dijkstra(edges, 0, 9)
    print 'length = ',length
    print 'The shortest path is ',Shortest_path