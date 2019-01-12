# tass_taxi_data

### Steps1

1. ./install_postgress.sh
2. ./download_data.sh
3. python3 prepare_data.py
4. ./init_db.sh

### Steps2 - tworzenie tabeli taxi_zones
(1.)* ściągamy i rozpakowujemy do data folder .zip ze strony:
- http://www.nyc.gov/html/exit-page.html?url=https://s3.amazonaws.com/nyc-tlc/misc/taxi_zones.zip

(2.)* Tworzymy folder taxi_zones w folderze data i dodajemy tam pliki
- taxi_zones.shp
- taxi_zones.shx
- taxi_zones.dbf
3. uruchamiamy skrypt ./init_taxi_zones.sh

\* Tylko jeżeli dane nie są ściągnięte, defaultowo są już w repo

## Steps3 - filtracja tabeli
1. ./processing_scripts/filter_table.py 

## Steps4 - obliczenia na tabelach
1. ./processing_scripts/pre_exercise.py
2. ./processing_scripts/calculate_zone.py
3. ./processing_scripts/calculate_targeted_poi.py

## Steps5
1. ./results/init_stats_table.py 
2. ./last_stats.py


