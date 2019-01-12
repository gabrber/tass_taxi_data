SELECT filter_weekday_evening."Dropoff_poi", poi."poi_point", poi."NAME", poi."poi_area", COUNT("Dropoff_poi") as counted
FROM filter_weekday_evening
INNER JOIN poi ON filter_weekday_evening."Dropoff_poi" = poi."PLACEID"
WHERE poi."FACILITY_T" = 3
GROUP BY filter_weekday_evening."Dropoff_poi", poi."poi_point", poi."NAME", poi."poi_area"
ORDER BY counted DESC;