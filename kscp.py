import datetime
import pandas as pd
from sqlalchemy import create_engine
import Queue
from heapq import *
import dijkstra

def get_available_airline(s_time, a_time, read_csv = True):
    if (read_csv):
        return
    engine = create_engine("mysql://root:abc1234@localhost:3306/Ctrip")
    start = str(s_time.date())+" 00:00:00"
    arrive = str(a_time.date())+" 00:00:00"
    sql_query = "select * from crawlerdata where effectdate>='"+ start +"' and effectdate<='"+arrive+"' limit 200"
    print sql_query
    airlines = pd.read_sql_query(sql_query  ,engine)
    airlines["effectdate"] = pd.to_datetime(airlines.effectdate)
    airlines["dtime"] = pd.to_datetime(airlines.dtime)
    airlines["atime"] = pd.to_datetime(airlines.atime)
    return airlines

def validate_arr_time(row):
    d = row.effectdate.date()
    t = row.atime.time()
    real_time = datetime.datetime.combine(d,t)
    if(row.dtime>row.atime):
        return real_time + datetime.timedelta(days=1)
    else:
        return real_time

def validate_dep_time(row):
    d = row.effectdate.date()
    t = row.dtime.time()
    return datetime.datetime.combine(d,t)

def get_fixed_airlines(df, read_csv=True):
    if read_csv:
        df = pd.read_csv("1.csv", sep=";")
        df["dep_time"] = pd.to_datetime(df.dep_time)
        df["arr_time"] = pd.to_datetime(df.arr_time)
        return df
    df["dep_time"] = df.apply(lambda row: validate_dep_time(row), axis=1)
    df["arr_time"] = df.apply(lambda row: validate_arr_time(row), axis=1)
    df = df[["dcity","acity","dport","aport","airline","flight","dep_time","arr_time","ctripprice"]]
    #df.to_csv("1.csv",sep=";")
    return df

class Port:
    def __init__(self,i = 0, city="",time=""):
        self.index = i
        self.city = city
        self.time = time

class Airline:
    def __init__(self,s=0, t=0, dcity="",acity="",dtime="",atime="",flight="",price=""):
        self.s = s
        self.t = t
        self.dcity = dcity
        self.acity = acity
        self.dtime = dtime
        self.atime = atime
        self.flight = flight
        self.price = price

def create_graph(df, sp, tp, st, tt):
    index = 0
    point_list = []
    edges = []
    point_queue = Queue.Queue()
    port = Port(index, sp, st)
    point_queue.put(port)
    point_list.append(port)
    index = index + 1
    while(not point_queue.empty()):
        tmp_port = point_queue.get()
        if tmp_port.city == tp:
            continue
        tmp_df = df[df.dcity == tmp_port.city][df.dep_time>tmp_port.time]
        for idx,rows in tmp_df.iterrows():
            new_port = Port(index, rows.acity,rows.arr_time)
            new_airline = Airline(tmp_port.index,index,rows.dcity,rows.acity,rows.dep_time,rows.arr_time,rows.flight,rows.ctripprice)
            point_queue.put(new_port)
            point_list.append(new_port)
            edges.append(new_airline)
            index = index + 1
    return point_list,edges

def get_project_distance(source, destination, edges):
    cost,path = dijkstra.dijkstra(edges, source, destination)
    if cost == -1:
        cost = 9999
    return cost

def CSP_generator(vertex, edges, tp):
    print "Generator"
    MAX_COST = 2000
    v_num = len(vertex)
    edge_mat = []
    edge_idx_mat = []
    destination = []
    dij_edges = []
    for i in range(v_num):
        edge_mat.append([])
        edge_idx_mat.append([])
        edge_mat[i] = [9999]*v_num
        if vertex[i].city == tp:
            destination.append(i)
    for e in edges:
        edge_mat[e.s][e.t] = e.price
        edge_idx_mat[e.s].append(e.t)
        dij_edges.append((e.s,e.t,e.price))

    K = 5
    k = 0
    q = [(0,(0,()))]
    csp_list = []
    while(k<=K and len(q) > 0):
        print len(q)
        cost,path = heappop(q)
        u = path[0]
        if vertex[u].city == tp:
            csp_list.append(path)
            k = k+1
            continue
        else:
            out_points = edge_idx_mat[u]
            for out in out_points:
                tmp_path = (out, path)
                tmp_cost = cost + edge_mat[u][out]
                if (tmp_cost + get_project_distance(out, destination,dij_edges)) > MAX_COST:
                    continue
                else:
                    heappush(q,(tmp_cost,tmp_path))
    return csp_list

def decode_path(l,vertex):
    for p in l:
        tmp_path = []
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
        for port in tmp_path:
            a.append(vertex[port].city)
        print a
if __name__ == '__main__':
    start_time = datetime.datetime.strptime("2014-10-23 00:00:00", "%Y-%m-%d %H:%M:%S")
    arrive_time = datetime.datetime.strptime("2014-10-24 23:59:59", "%Y-%m-%d %H:%M:%S")
    start_point = "SHA"
    end_point = "BJS"
    airlines = get_available_airline(start_time,arrive_time)
    airlines = get_fixed_airlines(airlines)
    vertex,edges = create_graph(airlines,start_point,end_point,start_time,arrive_time)
    csp_list = CSP_generator(vertex,edges,end_point)
    print csp_list
    decode_path(csp_list,vertex)


