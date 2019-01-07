#!/usr/bin/env python
import sys
sys.path.insert(0, '../')

import get_info
import shapely.wkt


def create_new_filtered_table(conn, curs, new_table, days, hours):

    taxies = get_info.get_tables_pattern("green", conn)
    new_table_check = get_info.get_tables_pattern(new_table, conn)
    taxi_table = taxies[0]

    if not new_table_check:
        sql = "SELECT * INTO " + new_table + " FROM " + taxi_table + " WHERE (\"Day_of_week\" BETWEEN " + str(days[0]) + " AND " +  str(days[1]) + ") AND " + " (\"Pickup_hour\" BETWEEN " + str(hours[0]) + " AND " + str(hours[1]) + ");"
    else:
        sql = "INSERT INTO " + new_table + " SELECT * FROM " + taxi_table + " WHERE (\"Day_of_week\" BETWEEN " + str(days[0]) + " AND " +  str(days[1]) + ") AND " + " (\"Pickup_hour\" BETWEEN " + str(hours[0]) + " AND " + str(hours[1]) + ");"

    curs.execute(sql)
    conn.commit()


if __name__ == "__main__":

    conn = get_info.connect_to_db()
    curs = conn.cursor()

    # Monday is 0, Sunday is 6

    # weekday envenings
    create_new_filtered_table(conn,curs,"filter_weekday_evening",(0,4),(18,23))

    # work traffic hours
    create_new_filtered_table(conn,curs,"filter_work_traffic",(0,4),(8,10))
    create_new_filtered_table(conn,curs,"filter_work_traffic",(0,4),(16,18))

    # weekend chill
    create_new_filtered_table(conn,curs,"filter_weekend_day",(5,6),(8,20))