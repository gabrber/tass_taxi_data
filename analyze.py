#!/usr/bin/env python
import sys
import get_info
import pandas as pd

def check_top_dropoff(conn,curs):

    curs.execute(open("sql/check_top_dropoff.sql", "r").read())
    top_dropoff = curs.fetchall()

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

def check_dislike_culture(conn,curs):
    curs.execute(open("sql/dislike_cultural_zones.sql", "r").read())
    dislike_culture = curs.fetchall()

    return dislike_culture

def check_like_culture(conn,curs):
    curs.execute(open("sql/start_cultural_zones.sql", "r").read())
    like_culture = curs.fetchall()

    return like_culture


if __name__ == "__main__":
    conn = get_info.connect_to_db()

    curs = conn.cursor()
    #zone_stats = dropoff_to_pickup(conn, curs, "filter_work_traffic")
    #print(zone_stats)
    traffic_zones = count_zones_traffic(conn,curs)
    print(traffic_zones)
    #top_dropoff = check_top_dropoff(conn,curs)
    #like_culture = check_like_culture(conn,curs)
    #dislike_culture = check_dislike_culture(conn,curs)
    #dislike_culture = like_culture[::-1]