import SqlUtil
import pandas as pd
import K_SCP
import datetime
import Personalize
import pickle
import networkx as nx
import matplotlib
import LoadData
def Get_Airline_Dict(path):
    airlines = open(path,'r')
    all = airlines.read().split('\n')
    return all

def Get_Recommend_Result(all_flights,sp,ep,st,et,airline,cabin,money,span=1):
    #airline_dict = Get_Airline_Dict('airlines')
    # all_airlines = pickle.load(open('database.pkl', 'rb'))
    airline_mat = Personalize.airline_mat(airline)
    cabin_mat = Personalize.cabin_mat(cabin)

    Graph, vertexes, edges = K_SCP.create_graph(all_flights, sp, ep, st, et, span)
    #print len(vertexes)
    csp_list = K_SCP.Generator(50, vertexes, edges, start_point, end_point, airline_mat, cabin_mat, 2*money, money, Graph)
    result = K_SCP.decode_path(csp_list, vertexes, edges, Graph)
    return result

def Get_Rank(ret,df,answer):
    for i in range(len(ret)):
        idx = int(ret[i][1][0])
        flight = df[df.id==idx]
        if ((flight.dtime.values[0] == answer[13]) and (flight.atime.values[0] == answer[14]) and (flight.flight.values[0] == answer[5]) and (flight.dtime.values[0] == answer[13])):
            return (i+1)
    return 100

if __name__ == "__main__":
    all_flights = LoadData.GetAllFlight()
    check = 'D:\\CitLab\\bysj\\BYSJ_P\\data\\search\\order_detail.csv'
    f = open(check,'r')
    line = f.readline()
    line = f.readline()
    f2 = open("D:\\CitLab\\bysj\\BYSJ_P\\data\\search\\airport_city.csv",'r')
    line1 = f2.readline()
    line1 = f2.readline()
    airport_city = {}
    Ranks = []
    while(line1):
        line1 = line1.replace('\n','')
        tmp = line1.split('\t')
        airport_city[tmp[0]] = tmp[1]
        line1 = f2.readline()
    for i in range(50):
        #print line
        line = line.replace('\n','')
        line = line.rstrip()
        test = line.split('\t')
        if (len(test) != 16):
            line = f.readline()
            continue
        start_point = airport_city[test[11]]
        end_point = airport_city[test[12]]
        start_time_str = test[13]
        end_time_str = test[14]
        start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
        if (start_time_str == 'NULL' or end_time_str == 'NULL'):
            line = f.readline()
            continue
        if(test[7]=='0'):
            line = f.readline()
            continue
        result = Get_Recommend_Result(all_flights,start_point,end_point,start_time,end_time,test[5][:2],'Economy',float(test[7]))
        Ranks.append(Get_Rank(result,all_flights,test))
        line = f.readline()
    print Ranks
