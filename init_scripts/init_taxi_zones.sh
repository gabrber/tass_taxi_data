#!/usr/bin/env bash

# download Postgis scripts (you could already have it)
sudo apt-get install postgresql-10-postgis-2.4-scripts

# create new table taxi zones
# here 2263 is spatial reference for POLYGON shape
sudo shp2pgsql -I -s 2263 ../data/taxi_zones/taxi_zones.shp taxi_zones | psql -U postgres -d tass
