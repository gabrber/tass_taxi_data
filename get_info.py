#!/usr/bin/env python

import sys
import psycopg2

def connect_to_db():
  conn = None
  try:
    #gab
    #conn = psycopg2.connect("dbname = 'tass' user = 'postgres' host = 'localhost' password = 'postgres'")
    #krzysiek
    conn = psycopg2.connect("dbname = 'tass' user = 'postgres' host = 'localhost' password = 'psql'")
  except psycopg2.DatabaseError as ex:
    print("Error connectiong to database: " + ex.args)
    sys.exit(1)
  return conn

def disconnect_from_db(conn):
  conn.close()
#
# get_tables_pattern return list of tables containing string(pattern)
#
def get_tables_pattern(pattern, conn):
  pattern_tables = []
  curs = conn.cursor()
  curs.execute("""SELECT * FROM information_schema.tables
               WHERE table_schema = 'public'""")
  for table in curs:
    if(pattern in table[2]):
      pattern_tables.append(table[2])

  return pattern_tables
#
# get_top_dropoff returns ordered list of (dropoff_poi, count(dropoff_poi))
#
def get_top_dropoff(conn):
  dropoff_rank = []
  curs = conn.cursor()
  curs.execute(open("sql/check_top_dropoff.sql", "r").read())
  for row in curs:
     dropoff_rank.append(row)
  return dropoff_rank

if __name__ == "__main__":

    conn = connect_to_db()
    #top_dropoff = get_top_dropoff(conn)
    taxi_tables = get_tables_pattern("taxi", conn)