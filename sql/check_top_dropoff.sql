SELECT filter_weekday_evening."Dropoff_poi", poi."poi_point", COUNT("Dropoff_poi") as counted
FROM filter_weekday_evening
INNER JOIN poi ON filter_weekday_evening."Dropoff_poi" = poi."PLACEID"
GROUP BY filter_weekday_evening."Dropoff_poi", poi."poi_point"
ORDER BY counted DESC;