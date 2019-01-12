UPDATE all_stats2
SET weekday_evening_norm = weekday_evening/taxi_zones.shape_area
FROM taxi_zones
WHERE all_stats2.gid = taxi_zones.gid;

UPDATE all_stats2
SET work_traffic_norm = work_traffic/taxi_zones.shape_area
FROM taxi_zones
WHERE all_stats2.gid = taxi_zones.gid;

UPDATE all_stats2
SET weekend_day_norm = weekend_day_traffic/taxi_zones.shape_area
FROM taxi_zones
WHERE all_stats2.gid = taxi_zones.gid;