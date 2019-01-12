#!/usr/bin/env bash

DATABASE="tass"

#sudo -u postgres createdb $DATABASE
sudo -u postgres psql -d $DATABASE -f sql\create_stats_table.sql
sudo -u postgres psql -d $DATABASE -f sql\copy_from_zones.sql
sudo -u postgres psql -d $DATABASE -f sql\weekday_evening_querry.sql
sudo -u postgres psql -d $DATABASE -f sql\work_traffic_querry.sql
sudo -u postgres psql -d $DATABASE -f sql\weekend_day_querry.sql