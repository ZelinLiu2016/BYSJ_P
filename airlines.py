def get_ways_dict(dcity,acity,airline_dict):
    return



if __name__ == "__main__":
    path = "data\\search\\city"
    f = open(path,'r')
    city_count = {}
    line = f.readline()
    count = 0
    while(line):
        count = count + 1
        if(count%50000 == 0):
            print count
        cities = line.replace('\n','').split()
        city = (cities[0]+' ' + cities[1]) if cities[0]<cities[1] else (cities[1]+' '+cities[0])
        if city in city_count:
            city_count[city] = city_count[city] + 1
        else:
            city_count[city] = 1
        line = f.readline()
    l = sorted(city_count.items(), key=lambda d: d[1])
    l.reverse()
    f2 = open("data\\search\\city_count",'w')
    for i in range(len(l)):
        f2.write(l[i][0]+'\t'+str(l[i][1])+'\n')
    f2.close()