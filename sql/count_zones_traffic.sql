SELECT "Pickup_zone", "Dropoff_zone", COUNT(*) AS counted
FROM filter_work_traffic
GROUP BY "Pickup_zone", "Dropoff_zone"
ORDER BY counted DESC;