#!/usr/bin/env python

import sys
import psycopg2

def connect_to_db():
  conn = None
  try:
    conn = psycopg2.connect("dbname = 'tass' user = 'postgres' host = 'localhost' password = 'postgres'")
  except psycopg2.DatabaseError as ex:
    print("Error connectiong to database: " + ex.args)
    sys.exit(1)
  return conn

#
# get_top_dropoff returns ordered list of (dropoff_poi, count(dropoff_poi))

def get_top_dropoff(conn):
  dropoff_rank = []
  curs = conn.cursor()
  curs.execute(open("sql/check_top_dropoff.sql", "r").read())
  for row in curs:
     dropoff_rank.append(row)
  return dropoff_rank

if __name__ == "__main__":

    conn = connect_to_db()
    top_dropoff = get_top_dropoff(conn)