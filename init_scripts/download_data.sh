#!/bin/bash

while read -r data_url; do
    wget "$data_url" -c -P ../data/
done < ../data/data_url.txt