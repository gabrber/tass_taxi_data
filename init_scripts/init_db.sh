#!/bin/bash

DATABASE="tass"

#sudo -u postgres createdb $DATABASE
sudo -u postgres psql -d $DATABASE -f sql/create_tables.sql
sudo -u postgres psql -d $DATABASE -c "ALTER USER postgres WITH PASSWORD 'psql';"

cat ../data/green-* | sudo -u postgres psql -d $DATABASE -c "COPY green_taxi FROM stdin WITH CSV HEADER;"
cat ../data/poi* | sudo -u postgres psql -d $DATABASE -c "COPY poi FROM stdin WITH CSV HEADER;"
