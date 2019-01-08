SELECT filter_work_traffic."Dropoff_zone", taxi_zones."geom", COUNT(*) AS counted
FROM filter_work_traffic
INNER JOIN taxi_zones ON filter_work_traffic."Dropoff_zone" = taxi_zones."gid"
GROUP BY filter_work_traffic."Dropoff_zone", taxi_zones."geom"
ORDER BY filter_work_traffic."Dropoff_zone";