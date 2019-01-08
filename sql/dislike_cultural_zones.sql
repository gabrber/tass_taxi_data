SELECT filter_weekday_evening."Pickup_zone", poi."poi_point", COUNT(*) AS counted
FROM filter_weekday_evening
INNER JOIN poi ON filter_weekday_evening."Dropoff_poi" = poi."PLACEID"
WHERE poi."FACILITY_T"=3
GROUP BY filter_weekday_evening."Pickup_zone", poi."poi_point"
ORDER BY counted;