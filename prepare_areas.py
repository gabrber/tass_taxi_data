areas_count = 10

min_longitude = -74.2589
min_latitude = 40.4774
max_longitude = -73.7004
max_latitude = 40.9176

diff_NS = max_longitude - min_longitude
diff_EW = max_latitude - min_latitude

areas = [[0 for x in range(areas_count)] for y in range(areas_count)]

start_NS = min_longitude
start_ES = min_latitude

for i in range(areas_count):
  ends_NS = start_NS + diff_NS

  for j in range(areas_count):

    ends_ES = start_ES + diff_EW
    areas[i][j] = (start_NS, start_ES, ends_NS, ends_ES)
    start_ES = ends_ES

  start_NS = ends_NS
  start_ES = min_latitude