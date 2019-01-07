#!/usr/bin/env bash

DATABASE="tass"

# create new table taxi zones
# here 2263 is spatial reference for POLYGON shape
sudo shp2pgsql -I -s 2263 ../data/taxi_zones/taxi_zones.shp taxi_zones | sudo -u postgres psql -d tass

sudo -u postgres psql -d $DATABASE -f sql/prepare_for_zones.sql