SELECT filter_weekday_evening."Pickup_zone", taxi_zones."geom" ,poi."poi_point", taxi_zones."zone", COUNT(*) AS counted
FROM filter_weekday_evening
INNER JOIN poi ON filter_weekday_evening."Dropoff_poi" = poi."PLACEID"
INNER JOIN taxi_zones ON filter_weekday_evening."Dropoff_zone" = taxi_zones."gid"
WHERE poi."FACILITY_T"=3
GROUP BY filter_weekday_evening."Pickup_zone", taxi_zones."geom", poi."poi_point", taxi_zones."zone"
ORDER BY counted DESC;