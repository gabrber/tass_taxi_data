#!/bin/bash

apt-get update
apt-get install -y python3 python3-pip
apt-get install -y postgresql postgresql-contrib pgadmin3

pip3 install pandas