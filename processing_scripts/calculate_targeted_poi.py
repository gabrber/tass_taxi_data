#!/usr/bin/env python
import sys
sys.path.insert(0, '../')

import get_info
import pandas as pd
from shapely import wkt
from shapely.ops import nearest_points
import geopandas as gpd
from shapely import geometry


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
    poi_polygon = geometry.Polygon([[p.x, p.y] for p in poi_list])

    for taxi_drives_name in taxi_drives:
        # populate point for dropoff
        taxi_drives_dropoff_sql = "SELECT ST_AsText(ST_Transform(\"Dropoff_point\", 4326)) as newgeom,* FROM " + taxi_drives_name + " limit 5;"
        taxi_drives_dropoff_data = pd.read_sql(taxi_drives_dropoff_sql, conn)
        taxi_drives_dropoff_data['newgeom'] = taxi_drives_dropoff_data['newgeom'].apply(wkt.loads)

        for index, taxi_point in taxi_drives_dropoff_data[['newgeom', 'id']].iterrows():
            pol = nearest_points(taxi_point['newgeom'], poi_polygon)
            distance = pol[0].distance(pol[1])
            print(poi_data.loc[poi_data['newgeom'] == pol[1]])
            print(type(pol[1]))
            print(type(poi_data['newgeom'][1]))
            #print(distance)  # TRZEBA DODAĆ FUNKCJĘ KTÓRA BĘDZIE LICZYŁA DYSTANS>>!!<<

        conn.commit()

if __name__ == "__main__":
    conn = get_info.connect_to_db()

    curs = conn.cursor()

    calculate_zones_for_poi(conn, curs)