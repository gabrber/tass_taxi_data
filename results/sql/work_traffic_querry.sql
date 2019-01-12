WITH subquerry AS (SELECT pickup_zone count(pickup_zone) as counted
FROM filter_work_traffic)
UPDATE all_stats2
SET all_stats2.work_traffic = subquerry.counted
FROM subquerry
WHERE all_stats2.gid = subquerry.pickup_zone;