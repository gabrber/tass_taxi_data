#!/usr/bin/env python
import sys
sys.path.insert(0, '../')

import get_info
import shapely.wkt
from shapely.geometry import shape
import pandas as pd
from geoalchemy2.shape import to_shape
from shapely.geometry import Point
from shapely import wkt


if __name__ == "__main__":

    conn = get_info.connect_to_db()

    #we get name of tables for taxi drives and taxi zones
    taxi_zones = get_info.get_tables_pattern("zones", conn)
    taxi_drives = get_info.get_tables_pattern("green", conn)

    #we have only one taxi_zones file
    taxi_zone_name = taxi_zones[0]

    #Add id to our green_taxi table
    add_id = "ALTER TABLE green_taxi ADD COLUMN id SERIAL PRIMARY KEY"

    curs = conn.cursor()

    # select polygon from taxi_zones
    taxi_zone_sql = "SELECT ST_AsText(ST_Transform(ST_Transform(geom, 2263), 4326)) as newgeom,* FROM " + taxi_zone_name + ";"
    taxi_zone_data = pd.read_sql(taxi_zone_sql, conn)
    taxi_zone_data['newgeom'] = taxi_zone_data['newgeom'].apply(wkt.loads)

    #print(taxi_zone_data['newgeom'])

    for taxi_drives_name in taxi_drives:
        # populate point for pickup
        taxi_drives_pickup_sql = "SELECT ST_AsText(ST_Transform(\"Pickup_point\", 4326)) as newgeom,* FROM " + taxi_drives_name + ";"
        taxi_drives_pickup_data = pd.read_sql(taxi_drives_pickup_sql, conn)
        taxi_drives_pickup_data['newgeom'] = taxi_drives_pickup_data['newgeom'].apply(wkt.loads)

        #print(taxi_drives_pickup_data['newgeom'])

        for index1, zone in taxi_zone_data[['newgeom','gid']].iterrows():
            for index2, point in taxi_drives_pickup_data[['newgeom', 'id']].iterrows():
                if zone['newgeom'].contains(point['newgeom']) == True:
                    sql = "UPDATE " + taxi_drives_name + " SET \"Pickup_area\" = " + str(zone['gid']) + " WHERE id = " + str(point['id']) + " limit 5;"
                    curs.execute(sql)
                    print('Done pickup'+str(point['id']))
                    #print("UPDATE " + taxi_drives_name + " SET \"Pickup_area\" = " + str(zone['gid']) + " WHERE id = " + str(point['id']) + ";")
                    break

        conn.commit()

        # populate point for dropoff
        taxi_drives_dropoff_sql = "SELECT ST_AsText(ST_Transform(\"Dropoff_point\", 4326)) as newgeom,* FROM " + taxi_drives_name + ";"
        taxi_drives_dropoff_data = pd.read_sql(taxi_drives_dropoff_sql, conn)
        taxi_drives_dropoff_data['newgeom'] = taxi_drives_dropoff_data['newgeom'].apply(wkt.loads)

        for index1, zone in taxi_zone_data[['newgeom','gid']].iterrows():
            for index2, point in taxi_drives_dropoff_data[['newgeom', 'id']].iterrows():
                if zone['newgeom'].contains(point['newgeom']) == True:
                    sql = "UPDATE " + taxi_drives_name + " SET \"Dropoff_area\" = " + str(zone['gid']) + " WHERE id = " + str(point['id']) + " limit 5;"
                    curs.execute(sql)
                    print('Done dropoff' + str(point['id']))
                    #print("UPDATE " + taxi_drives_name + " SET \"Dropoff_area\" = " + str(zone['gid']) + " WHERE id = " + str(point['id']) + ";")
                    break

        conn.commit()
