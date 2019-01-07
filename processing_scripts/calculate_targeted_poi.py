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
    taxi_drives = get_info.get_tables_pattern("filter", conn)

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
        # populate point for dropoff
        taxi_drives_dropoff_sql = "SELECT ST_AsText(ST_Transform(\"Dropoff_point\", 4326)) as newgeom,* FROM " + taxi_drives_name + ";"
        taxi_drives_dropoff_data = pd.read_sql(taxi_drives_dropoff_sql, conn)
        taxi_drives_dropoff_data['newgeom'] = taxi_drives_dropoff_data['newgeom'].apply(wkt.loads)

        #this is variable for assigning poi to taxi_data
        for index, taxi_point in taxi_drives_dropoff_data[['newgeom', 'id']].iterrows():
            pol = nearest_points(taxi_point['newgeom'], poi_polygon)

            for index, poi_d in poi_data[['newgeom', 'PLACEID']].iterrows():

                if poi_d['newgeom'] == pol[1]:
                    distance = function_measure(poi_d['newgeom'].y, poi_d['newgeom'].x, taxi_point['newgeom'].y, taxi_point['newgeom'].x)
                    if distance > 50:
                        out_poi = 0
                    else:
                        out_poi = poi_d["PLACEID"]
                    sql_poi = "UPDATE " + taxi_drives_name + " SET \"Dropoff_poi\" = " + str(out_poi) + " WHERE \"id\" = " + str(taxi_point['id']) + ";"
                    curs.execute(sql_poi)
                    print(taxi_point['id'])
                    break

        conn.commit()

if __name__ == "__main__":
    conn = get_info.connect_to_db()

    curs = conn.cursor()
    calculate_zones_for_poi(conn, curs)