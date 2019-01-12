WITH subquerry AS (SELECT filter_weekday_evening."Pickup_zone" as pickup_zone,  COUNT("Pickup_zone") as counted
FROM filter_weekday_evening
INNER JOIN poi ON filter_weekday_evening."Dropoff_poi" = poi."PLACEID"
WHERE poi."FACILITY_T" = 3 or poi."FACILITY_T" = 4 or poi."FACI_DOM" = 3 or poi."FACI_DOM" = 4
GROUP BY filter_weekday_evening."Pickup_zone"
ORDER BY counted DESC)
UPDATE all_stats2
SET weekday_evening = subquerry.counted
FROM subquerry
WHERE all_stats2.gid = subquerry.pickup_zone;