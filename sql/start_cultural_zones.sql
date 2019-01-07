SELECT "Pickup_zone", COUNT(*) AS counted
FROM filter_weekday_evening
INNER JOIN poi ON filter_weekday_evening."Dropoff_poi" = poi."PLACEID"
WHERE poi."FACILITY_T"=3
GROUP BY "Pickup_zone", "Dropoff_zone"
ORDER BY counted DESC;