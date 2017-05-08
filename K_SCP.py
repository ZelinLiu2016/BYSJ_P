import datetime
import Queue
import dijkstra
from heapq import *
import Personalize
import networkx as nx
import math

class Port:
    def __init__(self,i, city, time):
        self.index = i
        self.city = city
        self.time = time

class Airline:
    def __init__(self,s=0, t=0, dcity="",acity="",dtime="",atime="",flight="",price="",cabin="",idx=""):
        self.s = s
        self.t = t
        self.dcity = dcity
        self.acity = acity
        self.dtime = dtime
        self.atime = atime
        self.flight = flight
        self.price = price
        self.cabin = cabin
        self.idx = idx

def create_graph(all_airlines, sp, ep, st):
    airways = Personalize.get_airways(sp, ep)
    index = 0
    edge_index = 0
    vertexes = []
    edges = []
    G = nx.DiGraph()
    point_queue = Queue.Queue()
    port = Port(index, sp, st)
    vertexes.append(port)
    G.add_node(index)
    index = index + 1
    for airway in airways:
        point_queue.put(vertexes[0])
        while(not point_queue.empty()):
            tmp_port = point_queue.get()
            if tmp_port.city == ep:
                continue
            tmp_airlines = [x for x in all_airlines if ((x[1] == tmp_port.city) and (x[2]==airway[x[1]])and (x[3]>=tmp_port.time))]
            for airline in tmp_airlines:
                new_port = Port(index, airline[2],airline[4])
                new_airline = Airline(tmp_port.index,index,airline[1],airline[2],airline[3],airline[4],airline[6],airline[5],airline[7],airline[0])
                point_queue.put(new_port)
                vertexes.append(new_port)
                G.add_node(index)
                edges.append(new_airline)
                G.add_edge(tmp_port.index,index,index = edge_index)
                index = index + 1
                edge_index = edge_index + 1
    return G,vertexes,edges

def get_cost_edges(edges):
    return [(x.s,x.t,x.price)for x in edges]

def get_cost_mark(cost,avg_cost):
    return 1/(1+pow(math.e,-abs(cost-avg_cost)/avg_cost))

def Generator(K,vertexes,edges,sc,ec, airline_mat,cabin_mat, MAX_COST,AVG_COST,Graph):
    q = [(0,0,0,(0, ()))]
    csp_list = []
    cost_edges = get_cost_edges(edges)
    to_nodes = [x.index for x in vertexes if x.city==ec]
    cost_dij = dijkstra.dij_mat(vertexes,cost_edges,to_nodes)
    max_score = 0
    print "KCSP"
    while ( len(q) > 0):
        score,cost,transist,path = heappop(q)
        u = path[0]
        if vertexes[u].city == ec:
            if(len(csp_list)<K):
                heappush(csp_list,(-1 * score,path))
            else:
                if score>-1*max_score:
                    heappop(csp_list)
                    heappush(csp_list, (-1 * score, path))
                    s = nsmallest(1,csp_list)
                    max_score = -1*s[0][0]
        else:
            out_points = Graph[u]
            for out in out_points:
                attributes = out_points[out]
                airline = edges[attributes["index"]]
                tmp_path = (out, path)
                tmp_cost = cost + airline.price
                if (tmp_cost + cost_dij[out]) > MAX_COST:
                    continue
                tmp_score = float(score*transist-airline_mat[airline.flight]-cabin_mat[airline.cabin]-get_cost_mark(tmp_cost,AVG_COST))/(transist+1)
                tmp_score_up = float(tmp_score*(transist+1)-3)/(transist+2)
                if tmp_score_up > max_score:
                    continue
                else:
                    heappush(q, (tmp_score,tmp_cost,transist+1, tmp_path))
    return csp_list

def decode_path(l,vertex,edges,Graph):
    print "decoding"
    while(len(l)>0):
        q = heappop(l)
        tmp_path = []
        p = q[1]
        if len(p)>0:
            left = p[0]
            right = p[1]
            tmp_path.append(left)
            while(len(right)>0):
                left = right[0]
                tmp_path.append(left)
                right = right[1]
        tmp_path.reverse()
        a = []
        b = []
        for port in tmp_path:
            a.append(vertex[port].city)
            b.append(vertex[port].index)
        c = []
        for i in range(len(b)-1):
            c.append(edges[Graph.edge[b[i]][b[i+1]]["index"]].idx)
        print a,c,q[0]