SELECT filter_weekend_day."Pickup_zone", taxi_zones."geom",taxi_zones."zone", COUNT("Pickup_zone") as counted
FROM filter_weekend_day
INNER JOIN poi ON filter_weekend_day."Dropoff_poi" = poi."PLACEID"
INNER JOIN taxi_zones ON filter_weekend_day."Pickup_zone" = taxi_zones."gid"
WHERE poi."FACILITY_T"=4
GROUP BY filter_weekend_day."Pickup_zone", taxi_zones."geom", taxi_zones."zone"
ORDER BY counted DESC;