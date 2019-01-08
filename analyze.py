#!/usr/bin/env python
import sys
import get_info
import pandas as pd

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
        curs.execute("SELECT geom FROM taxi_zones WHERE gid=" + str(traffic_stat[0]) + ";")
        dropoff = curs.fetchall()
        curs.execute("SELECT geom FROM taxi_zones WHERE gid=" + str(traffic_stat[1]) + ";")
        pickup = curs.fetchall()
        #TODO


if __name__ == "__main__":
    conn = get_info.connect_to_db()

    curs = conn.cursor()
    #zone_stats = dropoff_to_pickup(conn, curs, "filter_work_traffic")
    #print(zone_stats)
    count_zones_traffic(conn,curs)