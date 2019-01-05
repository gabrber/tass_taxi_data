#!/bin/bash

DATABASE="tass"

sudo -u postgres createdb $DATABASE
sudo -u postgres psql -d $DATABASE -f sql/create_tables.sql

cat ../data/green_tripdata_* | sudo -u postgres psql -d $DATABASE -c "COPY green_taxi FROM stdin WITH CSV HEADER;"
