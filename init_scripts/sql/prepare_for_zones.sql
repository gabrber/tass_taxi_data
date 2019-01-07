ALTER TABLE green_taxi ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE poi ADD COLUMN poi_area Integer;
SELECT AddGeometryColumn('poi', 'poi_point', 4326, 'POINT', 2);
UPDATE poi SET poi_point = ST_SETSRID(ST_MakePoint("POI_LONGITUDE", "POI_LATITUDE"), 4326);
