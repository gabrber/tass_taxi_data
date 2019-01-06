#!/bin/bash

apt-get update
apt-get install -y python3 python3-pip
apt-get install -y postgresql postgresql-contrib pgadmin3

pip3 install pandas psycopg2 simpledbf

# download Postgis scripts (you could already have it)
sudo apt-get install -y postgresql-10-postgis-2.4-scripts postgis