#!/bin/bash

DATABASE="tass"

sudo -u postgres psql -d $DATABASE -c "DROP SCHEMA public CASCADE;"
sudo -u postgres psql -d $DATABASE -c "CREATE SCHEMA public;"
sudo -u postgres psql -d $DATABASE -c "GRANT ALL ON SCHEMA public TO postgres;"
sudo -u postgres psql -d $DATABASE -c "GRANT ALL ON SCHEMA public TO public;"