#!/usr/bin/env python
import sys
sys.path.insert(0, '../')

import get_info
import pandas as pd
from shapely import wkt
from shapely.ops import nearest_points
import geopandas as gpd
from shapely import geometry
import math

def function_measure(lat1, lon1, lat2, lon2):
    R = 6378.137 #Radius of earth in KM
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) *\
        math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000


def calculate_zones_for_poi(conn,curs):
    poi = get_info.get_tables_pattern("poi", conn)
    taxi_drives = get_info.get_tables_pattern("filter_weekday_evening", conn)

    # we have only one taxi_zones file
    poi_name = poi[0]

    # populate point for dropoff
    poi_sql = "SELECT ST_AsText(ST_Transform(\"poi_point\", 4326)) as newgeom,* FROM " + poi_name + ";"
    poi_data = pd.read_sql(poi_sql, conn)
    poi_data['newgeom'] = poi_data['newgeom'].apply(wkt.loads)

    poi_data_copy = poi_data.copy()
    poi_list = poi_data_copy['newgeom'].tolist()
    poi_polygon = geometry.MultiPoint([[p.x, p.y] for p in poi_list])

    for taxi_drives_name in taxi_drives:
        print(taxi_drives_name + " started")
        # populate point for dropoff
        taxi_drives_dropoff_sql = "SELECT ST_AsText(ST_Transform(\"Dropoff_point\", 4326)) as newgeom,* FROM " + taxi_drives_name + " limit 50;"
        taxi_drives_dropoff_data = pd.read_sql(taxi_drives_dropoff_sql, conn)
        taxi_drives_dropoff_data['newgeom'] = taxi_drives_dropoff_data['newgeom'].apply(wkt.loads)

        #this is variable for assigning poi to taxi_data
        flag = False

        for index, taxi_point in taxi_drives_dropoff_data[['newgeom', 'id', 'Dropoff_zone']].iterrows():


            for index, poi_d in poi_data[['newgeom', 'PLACEID', 'poi_area']].iterrows():
                #print(poi_d)

                if poi_d['poi_area'] != taxi_point['Dropoff_zone']:
                    continue
                else:
                    pol = nearest_points(taxi_point['newgeom'], poi_polygon)
                    if poi_d['newgeom'] == pol[1]:
                        #distance = function_measure(poi_d['newgeom'].y, poi_d['newgeom'].x, taxi_point['newgeom'].y, taxi_point['newgeom'].x)
                        distance = math.sqrt(pow(poi_d['newgeom'].y-taxi_point['newgeom'].y,2) + pow(poi_d['newgeom'].x-taxi_point['newgeom'].x,2))
                        distance *= 111000
                        if distance > 50:
                            out_poi = 0
                        else:
                            out_poi = poi_d["PLACEID"]
                        sql_poi = "UPDATE " + taxi_drives_name + " SET \"Dropoff_poi\" = " + str(out_poi) + " WHERE \"id\" = " + str(taxi_point['id']) + ";"
                        curs.execute(sql_poi)
                        print(str(taxi_point['id']) + " - " + str(out_poi))
                        flag = True
                if flag == True:
                    flag = False
                    break

        conn.commit()


def calculate_poi_for_dropoff(conn,curs):
    poi = get_info.get_tables_pattern("poi", conn)
    taxi_drives = get_info.get_tables_pattern("filter_weekday_evening", conn)

    # we have only one taxi_zones file
    poi_name = poi[0]

    # populate point for dropoff
    poi_sql = "SELECT \"POI_LONGITUDE\",\"POI_LATITUDE\", \"poi_area\", \"PLACEID\" FROM " + poi_name + ";"
    curs.execute(poi_sql)
    poi_data = curs.fetchall()

    for taxi_drives_name in taxi_drives:
        print(taxi_drives_name + " started")
        # populate point for dropoff
        taxi_drives_dropoff_sql = "SELECT \"Dropoff_longitude\",\"Dropoff_latitude\", \"Dropoff_zone\", \"id\" FROM " + taxi_drives_name + " limit 50;"
        curs.execute(taxi_drives_dropoff_sql)
        taxi_drives_dropoff_data = curs.fetchall()

        for taxi_point in taxi_drives_dropoff_data:
            out_poi = 0
            last_best = 50
            for poi_d in poi_data:
                #print(poi_d)
                #print(taxi_point)

                if poi_d[2] != taxi_point[2]:
                    continue
                else:
                    distance = math.sqrt(pow(poi_d[0]-taxi_point[0],2) + pow(poi_d[1]-taxi_point[1],2))
                    distance *= 111000
                    if (distance < 50) and (distance < last_best):
                        out_poi = poi_d[3]
                        last_best = distance
            sql_poi = "UPDATE " + taxi_drives_name + " SET \"Dropoff_poi\" = " + str(out_poi) + " WHERE \"id\" = " + str(taxi_point[3]) + ";"
            curs.execute(sql_poi)
            print(str(taxi_point[3]) + " - " + str(out_poi))
        conn.commit()

if __name__ == "__main__":
    conn = get_info.connect_to_db()

    curs = conn.cursor()
    calculate_poi_for_dropoff(conn, curs)