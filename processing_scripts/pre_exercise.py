#!/usr/bin/env python
import sys
sys.path.insert(0, '../')

import get_info

def create_point_column(table_name, new_point_column, conn):
    create_column = "SELECT AddGeometryColumn(\'" + table_name + "\',\'" + new_point_column + "\',4326,\'POINT\',2)"
    curs = conn.cursor()
    curs.execute(create_column)
    conn.commit()

def populate_point_column(table_name,lon_column, lat_column, new_point_column, conn):
    populate_column = "UPDATE " + table_name + " SET \"" + new_point_column + "\" = ST_SETSRID(ST_MakePoint(\"" + lon_column + "\", \"" + lat_column + "\"), 4326)"
    print(populate_column)
    curs = conn.cursor()
    curs.execute(populate_column)
    conn.commit()

def add_point_from_lon_lat(table_name,lon_column, lat_column, new_point_column, conn):
    create_point_column(table_name, new_point_column, conn)
    populate_point_column(table_name, lon_column, lat_column, new_point_column, conn)


if __name__ == "__main__":

    conn = get_info.connect_to_db()
    taxi_tables = get_info.get_tables_pattern("green", conn)
    poi_table = get_info.get_tables_pattern("poi", conn)

    #for poi_name in poi_table:
    #    add_point_from_lon_lat(poi_name,"POI_LONGITUDE","POI_LATITUDE",'poi_point',conn)

    for taxi_name in taxi_tables:
        add_point_from_lon_lat(taxi_name, "Pickup_longitude", "Pickup_latitude", "Pickup_point", conn)
        add_point_from_lon_lat(taxi_name, "Dropoff_longitude", "Dropoff_latitude", "Dropoff_point", conn)
