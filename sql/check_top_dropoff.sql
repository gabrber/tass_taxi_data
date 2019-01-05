SELECT "Dropoff_poi", COUNT("Dropoff_poi") as counted
FROM green_taxi
GROUP BY "Dropoff_poi"
ORDER BY counted DESC;