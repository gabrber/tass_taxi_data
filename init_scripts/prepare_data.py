#!/usr/bin/env python

import sys
import pandas as pd
import glob
import os

def prepare_poi(poifile):
  poi=pd.read_csv(poifile)
  keep_col = ['PLACEID','NAME','FACILITY_T','FACI_DOM','the_geom']
  tmp_poi = poi[keep_col]
  tmp_poi['POI_LONGITUDE'] = ""
  tmp_poi['POI_LATITUDE'] = ""

  for i, row in tmp_poi.iterrows():
    poi_point = str(row['the_geom']).split(" ")
    poi_longitude = str(poi_point[1]).replace("(","")
    poi_latitude = str(poi_point[2]).replace(")","")

    tmp_poi.at[i,'POI_LONGITUDE'] = poi_longitude
    tmp_poi.at[i,'POI_LATITUDE'] = poi_longitude

  new_poi = tmp_poi[['PLACEID','NAME','FACILITY_T','FACI_DOM','POI_LONGITUDE','POI_LATITUDE']]
  new_poi.to_csv("../data/poi.csv", index=False)
  #os.remove(poifile)

def prepare_green_taxi(green_csv, i):
  toedit = open(green_csv).read()
  toedit = toedit.replace(',,', '')
  edited = open(green_csv, 'w')
  edited.write(toedit)
  edited.close()

  keep_col = ['lpep_pickup_datetime','Lpep_dropoff_datetime','Pickup_longitude','Pickup_latitude','Dropoff_longitude','Dropoff_latitude', 'Passenger_count']
  taxi=pd.read_csv(green_csv,usecols=keep_col)

  new_taxi = taxi[keep_col]
  new_taxi['Pickup_znoe'] = ""
  new_taxi['Dropoff_zone'] = ""
  new_taxi['Dropoff_poi'] = ""

  filename = "../data/green-" + str(i)
  new_taxi.to_csv(filename, index=False)
  #os.remove(green_csv)

if __name__ == "__main__":

    poifile = "../data/rows.csv?accessType=DOWNLOAD"
    taxi_files = glob.glob('../data/green*')

    prepare_poi(poifile)
    for i, green_csv in enumerate(taxi_files):
      prepare_green_taxi(green_csv, i)