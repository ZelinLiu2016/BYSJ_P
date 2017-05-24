import pandas as pd

def get_port_city_dict():
    path = 'data\\city_port.csv'
    f = open(path,'r')
    port_city_dict = {}
    line = f.readline()
    line = f.readline()
    while(line):
        line = line.replace('\n','')
        info = line.split(',')
        port_city_dict[info[3]] = info[1]
        line = f.readline()
    f.close()
    return port_city_dict

def GetAllFlight():
    path = 'flight_order_transfer.csv'
    column = ['id','userid','orderid','tripid','dcity','acity','dport','aport','dtime','atime','flight','cabin','class','price']
    result = pd.read_csv(path,sep=',',names=column)
    return result

def shape_time(date_time):
    date = date_time.split(' ')[0]
    time = date_time.split(' ')[1]
    d = date.split('-')
    d_list = []
    d_list.append(d[0])
    d_list.append("%02d" % (int(d[1])))
    d_list.append("%02d" % (int(d[2])))
    new_d = '-'.join(d_list)
    t = time.split(':')
    t_list = []
    t_list.append('%02d' % (int(t[0])))
    t_list.append('%02d' % (int(t[1])))
    t_list.append('%02d' % (int(t[2])))
    new_t = ':'.join(t_list)
    return ' '.join([new_d,new_t])



def refine_data(path):
    f = open(path,'r')
    w = open('aaa', 'w')
    result = []
    column = ['id','userid','tripid','orderid','dcity','acity']
    line = f.readline()
    line_num = 0
    id_num = 1
    print line
    while(line):
        line_num = line_num + 1
        line = f.readline()
        data = line.replace('\n','').split('\t')
        if (len(data) != 38):
            print "Error! "
            print line
            continue
        uid = data[0]
        orderid = data[1]
        dcity = data[2]
        acity = data[3]
        isout = data[4]
        isin = data[5]
        price = float(data[6])
        outflightgroup = data[8]
        outcabingroup = data[9]
        outclassgroup = data[10]
        outdeptime = data[11]
        outarvtime = data[12]
        isouttransfer = data[13]
        outtransfercity = data[14]
        outtransfertime = data[15]
        outtransfercount = int(data[16])
        inflightgroup = data[17]
        incabingroup = data[18]
        inclassgroup = data[19]
        indeptime = data[20]
        inarvtime = data[21]
        intransfer = data[22]
        intransfercity = data[23]
        intransfertime = data[24]
        intransfercount = int(data[25])
        adult = data[26]
        child = data[27]
        infant = data[28]
        outairlines = data[30]
        inairlines = data[31]
        depports = data[33]
        deptimes = data[34]
        arvports = data[35]
        arvtimes = data[36]

        a = 0 if isout=='NULL' else 1
        b = 0 if isin=='NULL' else 1
        px = price/(a+b)
        if(isout != 'NULL'):
            #outcount = outtransfercount + 1
            outcities = [] if (outtransfercity == 'NULL') else outtransfercity.split(',')
            outdeptimes = deptimes.split(';')[0].split(',')
            outarvtimes = arvtimes.split(';')[0].split(',')
            outdepports = depports.split(';')[0].split(',')
            outarvports = arvports.split(';')[0].split(',')

            outclasses = outclassgroup.split(',')
            outcabins = outcabingroup.split(',')
            outflights = outflightgroup.split(',')

            outcount = len(outcities) + 1
            if (len(outdeptimes) != len(outarvtimes) or len(outdeptimes) != len(outdepports)):
                print "Out Time Not Match    "
                print line
                outcount = 0
            if (len(outcities)+1 != len(outdepports)):
                print "Out Transfer Not Match    "
                print line
                outcount = 0
            if(outcount>2):
                print "Transfer Count > 2    "
            for i in range(outcount):
                fromcity = dcity if (i == 0) else outcities[i-1]
                tocity =  acity if (i == (outcount - 1)) else outcities[i]
                fromtime = shape_time(outdeptimes[i])
                totime = shape_time(outarvtimes[i])
                fromport = outdepports[i]
                toport = outarvports[i]
                outclass = outclasses[i]
                outcabin = outcabins[i]
                outflight = outflights[i]
                info = [str(id_num),uid,orderid,str(line_num),fromcity,tocity,fromport,toport,fromtime,totime,outflight,outcabin,outclass,str(px)]
                id_num = id_num + 1
                w.write(','.join(info) + '\n')
                #result.append(info)
        if (isin != 'NULL'):
            #incount = intransfercount + 1
            incities = [] if (intransfercity == 'NULL') else intransfercity.split(',')
            indeptimes = deptimes.split(';')[1].split(',')
            inarvtimes = arvtimes.split(';')[1].split(',')
            indepports = depports.split(';')[1].split(',')
            inarvports = arvports.split(';')[1].split(',')

            inclasses = inclassgroup.split(',')
            incabins = incabingroup.split(',')
            inflights = inflightgroup.split(',')
            incount = len(incities) + 1
            if (len(indeptimes) != len(inarvtimes) or len(indeptimes) != len(indepports)):
                print "In Time Not Match    "
                print line
                incount = 0
            if (len(incities)+1 != len(indepports)):
                print "In Transfer Not Match    "
                print line
                incount = 0
            if (incount > 2):
                print "Transfer Count > 2    "
            for i in range(incount):
                fromcity = acity if (i == 0) else incities[i - 1]
                tocity = dcity if (i == (incount - 1)) else incities[i]
                fromtime = shape_time(indeptimes[i])
                totime = shape_time(inarvtimes[i])
                fromport = indepports[i]
                toport = inarvports[i]
                inclass = inclasses[i]
                incabin = incabins[i]
                inflight = inflights[i]
                info = [str(id_num), uid, orderid,str(line_num), fromcity, tocity, fromport, toport, fromtime, totime, inflight, incabin,inclass, str(px)]
                id_num = id_num + 1
                w.write(','.join(info) + '\n')
                #result.append(info)
            print id_num,line_num
    w.close()

def trial(path):
    f = open(path,'r')
    line = f.readline()
    write = open('aaa','w')
    while(line):
        data = line.split('\t')
        if (data[4] == 'NULL' or data[5] == 'NULL'):
            write.write(line)
        line = f.readline()

def readNline(path,n):
    f = open(path,'r')
    for i in range(n+1):
        line = f.readline()
    print line.split('\t')

if __name__ == "__main__":
    path = "D:\\CitLab\\bysj\\BYSJ_P\\flight_order_transfer.csv"
    #refine_data(path)
    #trial(path)
    readNline(path,19657907)
    # print shape_time('2017-1-4 2:12:9')