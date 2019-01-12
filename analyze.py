#!/usr/bin/env python
import sys
import get_info
import pandas as pd
import numpy as np
from collections import defaultdict

def check_top_dropoff(conn,curs):

    curs.execute(open("sql/check_top_dropoff.sql", "r").read())
    top_dropoff = curs.fetchall()
    i = 0
    for top in top_dropoff:
        print(str(top[4])+"\t"+str(top[2]))

    return top_dropoff


def dropoff_to_pickup(conn,curs,table):

    get_zones = "SELECT gid FROM taxi_zones;"
    curs.execute(get_zones)
    zones = curs.fetchall()
    #print(zones)

    zone_stats =[]
    for zone in zones:
        sql_dropoff = "SELECT COUNT(*) FROM " + table + " WHERE \"Dropoff_zone\"=" + str(zone[0]) + ";"
        sql_pickup = "SELECT COUNT(*) FROM " + table + " WHERE \"Pickup_zone\"=" + str(zone[0]) +";"

        curs.execute(sql_dropoff)
        #curs.execute(open("sql/count_dropoff.sql", "r").read())
        count_dropoff = curs.fetchall()
        curs.execute(sql_pickup)
        #curs.execute(open("sql/count_pickup.sql", "r").read())
        count_pickup = curs.fetchall()

        if count_pickup[0][0] != 0:
            count = float(count_dropoff[0][0])/float(count_pickup[0][0])
            if ( count > 1):
                curs.execute("SELECT geom FROM taxi_zones WHERE gid=" + str(zone[0]) + ";")
                zone_geom = curs.fetchall()[0]
                zone_stats.append((zone[0],zone_geom,count))

    sorted_zone_stats = sorted(zone_stats, key=lambda stat: stat[2], reverse=True)
    return(sorted_zone_stats)

def count_zones_traffic(conn,curs):

    curs.execute(open("sql/count_zones_traffic.sql", "r").read())
    traffic = curs.fetchall()
    #print(traffic)
    new_traffic = []
    for traffic_stat in traffic:
        if not ((traffic_stat[0] is None) or (traffic_stat[1] is None)):
            curs.execute("SELECT geom FROM taxi_zones WHERE gid=" + str(traffic_stat[0]) + ";")
            dropoff = curs.fetchall()
            curs.execute("SELECT geom FROM taxi_zones WHERE gid=" + str(traffic_stat[1]) + ";")
            pickup = curs.fetchall()
            data = (traffic_stat[0],pickup,traffic_stat[1],dropoff,traffic_stat[2])
            new_traffic.append(data)

    return new_traffic

def count_zones_traffic_2(conn,curs):

    curs.execute(open("sql/count_zones_traffic.sql", "r").read())
    traffic = curs.fetchall()
    #print(traffic)
    new_traffic = np.zeros([264, 264])
    max_list = []
    for t in traffic:
        if t[0] == None or t[1] == None:
            continue
        elif t[0] > t[1]:
            new_traffic[t[0]][t[1]] += t[2]
        else:
            new_traffic[t[1]][t[0]] += t[2]

    for i in range(264):
        for k in range(264):
            max_list.append([i,k,new_traffic[i][k]])

    max_list = sorted(max_list, key=lambda x: x[2], reverse = True)[0:10]
    for m in max_list:
        sql = "INSERT INTO \"result_weekday\"(\"first_area\", \"second_area\",\"counted\") VALUES (" + str(m[0]) + "," + str(m[1]) + "," + str(m[2]) +")"
        curs.execute(sql)
    conn.commit()

    return max_list[0:10]

def check_dislike_culture(conn,curs):
    curs.execute(open("sql/dislike_cultural_zones.sql", "r").read())
    dislike_culture = curs.fetchall()

    return dislike_culture

def check_like_culture(conn,curs):
    curs.execute(open("sql/check_top_weekend.sql", "r").read())
    like_culture = curs.fetchall()
    like_culture = sorted(like_culture, key = lambda x: x[3], reverse=True)[0:10]
    for l in like_culture:
        print("{: >6} {: >30}".format(l[3], l[2]))

    return like_culture


if __name__ == "__main__":
    conn = get_info.connect_to_db()

    curs = conn.cursor()
    #zone_stats = dropoff_to_pickup(conn, curs, "filter_work_traffic")
    #print(zone_stats)
    #check_top_dropoff(conn, curs)
    #top_dropoff = check_top_dropoff(conn,curs)
    like_culture = check_like_culture(conn,curs)
    #dislike_culture = check_dislike_culture(conn,curs)
    #dislike_culture = like_culture[::-1]
    #print(count_zones_traffic_2(conn,curs))
    # sql = "SELECT *  from result_weekday;"
    # curs.execute(sql)
    # zone = curs.fetchall()
    # zone = sorted(zone, key = lambda x: x[2], reverse=True)
    # for z in zone:
    #     print("{: > 6} {: >20} {: >20}".format(z[2], z[5], z[6]))