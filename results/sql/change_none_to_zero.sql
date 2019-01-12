UPDATE all_stats2
SET work_traffic_norm = work_traffic/taxi_zones.area
INNER JOIN taxi_zones on all_stats2.gid = taxi_zones.gid;

UPDATE all_stats2
SET weekday_evening = 0
WHERE weekday_evening IS NULL;

UPDATE all_stats2
SET weekend_day = 0
WHERE weekend_day IS NULL;