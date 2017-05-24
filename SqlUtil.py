import MySQLdb
import pickle

def GetAllAirline(dt, at):
    con = MySQLdb.connect('localhost', 'root', 'abc1234', 'ctrip')
    result = []
    with con:
        cur = con.cursor()
        sql_str = "SELECT id,dcity,acity,outbounddeparttime,outboundarrivaltime,saleprice,outboundticketairlines,outboundcabingroup FROM flight_order_t where outbounddeparttime >= '{0}' and outboundarrivaltime <= '{1}' and isoutboundtransfer = 0".format(dt, at)
        print sql_str
        cur.execute(sql_str)
        numrows = int(cur.rowcount)
        for i in range(numrows):
            row = cur.fetchone()
            result.append(row)
    print "Fetched All Airlines From MYSQL, {0} Records ".format(numrows)
    output = open('database.pkl', 'wb')
    pickle.dump(result, output)
    return result

def GetAll():
    con = MySQLdb.connect('localhost', 'root', 'abc1234', 'ctrip')
    result = []
    with con:
        cur = con.cursor()
        sql_str = "SELECT * FROM flight_order_transfer_t"
        cur.execute(sql_str)
        numrows = int(cur.rowcount)
        for i in range(numrows):
            row = cur.fetchone()
            result.append(row)
    print "Fetched All Airlines From MYSQL, {0} Records ".format(numrows)
    return result

def InsertData():
    db = MySQLdb.connect('localhost', 'root', 'abc1234', 'ctrip')
    cur = db.cursor()
    file = open('D:\\CitLab\\bysj\\1','r')
    line = file.readline()
    line = file.readline()
    count = 0
    while(line):
        sql = 'insert into global (dcity, acity, outbounddate, inbounddate, saleprice, salechannel, outboundflightgroup, outboundcabingroup, outboundclassgroup, outbounddeparttime, outboundarrivaltime, isoutboundtransfer, outboundtransfercities, outboundtransferminutes, outboundtransfercounts, inboundflightgroup, inboundcabingroup, inboundclassgroup, inbounddeparttime, inboundarrivaltime, isinboundtransfer, inboundtransfercities, inboundtransferminutes, inboundtransfercounts, adultcount, childcount, infantcount, requestclass, outboundticketairlines, inboundticketairlines, totalflightminutes, departureairports, departuretimes, arrivalairports,arrivaltimes, everysegmenttotalflightminutes) values '
        i = 0
        while(i<1000 and line):
            line = line.replace('\n',"")
            tmp = "('"+line.replace('\t',"','")+"')"
            sql = sql + tmp + ','
            line = file.readline()
            count = count + 1
            i = i+1
        sql = sql[:-1]
        if count%10000 == 0:
            print count
        cur.execute(sql)
        db.commit()
    cur.close()
    db.close()
    print count

def InsertFlightOrderData():
    db = MySQLdb.connect('localhost', 'root', 'abc1234', 'ctrip')
    cur = db.cursor()
    file = open('D:\\CitLab\\bysj\\flight_order','r')
    line = file.readline()
    line = file.readline()
    count = 0
    while(line):
        line = file.readline()
        sql = 'insert into flight_order_t (uid, orderid, dcity, acity, outbounddate, inbounddate, saleprice, salechannel, outboundflightgroup, outboundcabingroup, outboundclassgroup, outbounddeparttime, outboundarrivaltime, isoutboundtransfer, outboundtransfercities, outboundtransferminutes, outboundtransfercounts, inboundflightgroup, inboundcabingroup, inboundclassgroup, inbounddeparttime, inboundarrivaltime, isinboundtransfer, inboundtransfercities, inboundtransferminutes, inboundtransfercounts, adultcount, childcount, infantcount, requestclass, outboundticketairlines, inboundticketairlines, totalflightminutes, departureairports, departuretimes, arrivalairports,arrivaltimes, everysegmenttotalflightminutes) values '
        i = 0
        while(i<2000 and line):
            line = line.replace('\n',"")
            tmp = "('"+line.replace('\t',"','")+"')"
            sql = sql + tmp + ','
            line = file.readline()
            count = count + 1
            i = i+1
        sql = sql[:-1]
        if count%10000 == 0:
            print count
        cur.execute(sql)
        db.commit()
    cur.close()
    db.close()
    print count

def InsertOrderData():
    db = MySQLdb.connect('localhost', 'root', 'abc1234', 'ctrip')
    cur = db.cursor()
    file = open('D:\\CitLab\\bysj\\BYSJ_P\\flight_order_transfer.csv','r')
    line = file.readline()
    count = 0
    while(line):
        sql = 'insert into flight_order_transfer_t (id,uid, orderid,tripid, dcity, acity, dport, aport, dtime, atime, flight, cabin, class, price) values '
        i = 0
        while(i<5000 and line):
            line = line.replace('\n','')
            #line = ','.join(line.split(',')[1:])
            tmp = "('"+line.replace(',',"','")+"')"
            sql = sql + tmp + ','
            line = file.readline()
            count = count + 1
            i = i+1
        sql = sql[:-1]
        if count%10000 == 0:
            print count
        cur.execute(sql)
        db.commit()
    cur.close()
    db.close()
    print count

if __name__ == "__main__":
    #InsertOrderData()
    a = '123\t123\t123\t123\t456\t67\t'
    b = a.rstrip()
    print '"'+b.rstrip()+'"'
    print b.split('\t')
