UPDATE result_weekday
SET first_area_geom = taxi_zones."geom"
FROM  taxi_zones
WHERE taxi_zones."gid" = result_weekday."first_area";

UPDATE result_weekday
SET second_area_geom = taxi_zones."geom"
FROM  taxi_zones
WHERE taxi_zones."gid" = result_weekday."second_area";