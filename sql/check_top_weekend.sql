SELECT filter_weekend_day."Dropoff_poi", taxi_zones."geom", COUNT("Dropoff_poi") as counted
FROM filter_weekend_day
INNER JOIN poi ON filter_weekend_day."Dropoff_poi" = poi."PLACEID"
INNER JOIN taxi_zones ON filter_weekend_day."Dropoff_zone" = taxi_zones."gid"
WHERE poi."FACILITY_T"=4
GROUP BY filter_weekend_day."Dropoff_poi", taxi_zones."geom"
ORDER BY counted DESC;