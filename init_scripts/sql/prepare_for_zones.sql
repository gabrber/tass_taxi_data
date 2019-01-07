ALTER TABLE green_taxi ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE poi ADD COLUMN poi_area Integer;
ALTER TABLE green_taxi ADD COLUMN "Dropoff_area" Integer;
ALTER TABLE green_taxi ADD COLUMN "Pickup_area" Integer;

SELECT AddGeometryColumn('poi', 'poi_point', 4326, 'POINT', 2);
UPDATE poi SET poi_point = ST_SETSRID(ST_MakePoint("POI_LONGITUDE", "POI_LATITUDE"), 4326);
SELECT AddGeometryColumn('green_taxi', 'Dropoff_point', 4326, 'POINT', 2);
UPDATE green_taxi SET "Dropoff_point" = ST_SETSRID(ST_MakePoint("Dropoff_longitude", "Dropoff_latitude"), 4326);
SELECT AddGeometryColumn('green_taxi', 'Pickup_point', 4326, 'POINT', 2);
UPDATE green_taxi SET "Pickup_point" = ST_SETSRID(ST_MakePoint("Pickup_longitude", "Pickup_latitude"), 4326);