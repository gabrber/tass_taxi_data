WITH subquerry AS (SELECT filter_weekend_day."Pickup_zone" as pickup_zone,  COUNT("Pickup_zone") as counted
FROM filter_weekend_day
INNER JOIN poi ON filter_weekend_day."Dropoff_poi" = poi."PLACEID"
WHERE poi."FACILITY_T" = 9 or poi."FACI_DOM" = 9
GROUP BY filter_weekend_day."Pickup_zone"
ORDER BY counted DESC)
UPDATE all_stats2
SET weekend_day = subquerry.counted
FROM subquerry
WHERE all_stats2.gid = subquerry.pickup_zone;