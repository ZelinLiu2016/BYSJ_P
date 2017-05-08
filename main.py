import SqlUtil
import K_SCP
import datetime
import Personalize
import pickle
import networkx as nx
import matplotlib

def Get_Airline_Dict(path):
    airlines = open(path,'r')
    all = airlines.read().split('\n')
    return all


if __name__ == "__main__":
    start_point = 'TYO'
    end_point = 'SHA'
    start_time_str = '2017-04-27 00:00:00'
    end_time_str = '2017-04-27 20:00:00'
    start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

    airline_dict = Get_Airline_Dict('airlines')
    #all_airlines = SqlUtil.GetAllAirline(start_time, end_time)
    all_airlines = pickle.load(open('database.pkl', 'rb'))
    airline_mat = Personalize.airline_mat("CA")
    cabin_mat = Personalize.cabin_mat("Premium")

    Graph,vertexes,edges = K_SCP.create_graph(all_airlines,start_point,end_point,start_time)
    print len(vertexes)
    csp_list = K_SCP.Generator(50, vertexes, edges, start_point, end_point, airline_mat,cabin_mat,5000,4000,Graph)
    K_SCP.decode_path(csp_list,vertexes,edges,Graph)

