'''
Created on Mar 17, 2017
@author: Wonhee Cho
email : danylight@gmail.com
Web site: http://mediaq.usc.edu/mmsys17
Copyright 2017 Wonhee Cho
Function: Generate Map
'''
import sys
import json
import numpy as np
import csv
from staticmap import StaticMap, CircleMarker
from motionless import LatLonMarker, DecoratedMap
from math import radians, cos, sin, asin, sqrt, atan2, log
import matplotlib.pyplot as plt
from matplotlib import mlab
from pylab import figure, axes, pie, title, show
from GenCsv import distance

def gen_map(input_json_file_path, output_map_file_path):
    print(" gmap, ",end="")
    json_data=open(input_json_file_path).read()
    data = json.loads(json_data)
    gps = data['sensor_data'][0]['location_array_timestamp_lat_long_accuracy']
    m = StaticMap(600, 400, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')
    idx = 0
    if len(gps)<500: gps_interval = 1
    else: gps_interval = 15
    min_lat, min_lon, max_lat, max_lon = 90, 120, -90, -120
    for gpsdata in gps:
        gps_lat, gps_lon = gpsdata[2:4]
        if gps_lat==0 or gps_lon==0: continue
        if min_lat > gps_lat: min_lat = gps_lat
        if min_lon > gps_lon: min_lon = gps_lon
        if max_lat < gps_lat: max_lat = gps_lat
        if max_lon < gps_lon: max_lon = gps_lon
        if idx % gps_interval == 0:
            if not(gps_lat==0 or gps_lon==0):
                marker = CircleMarker((gps_lon, gps_lat), 'red', 7)
                m.add_marker(marker)
            else: continue
        idx += 1

    if idx <=3:
        print(" --> failed to generate because file contains less than 3 data... ")
        return False

    # calculate GPS trajectory distance using MBR(Most Boundary Rectangle)
    dist = ( distance(min_lon,min_lat,max_lon,max_lat) )/1000
    if dist > 50: level=8
    elif dist > 35 and dist <=50: level=9
    elif dist > 14 and dist <=35: level=10
    elif dist > 10 and dist <=14: level=11
    elif dist > 6 and dist <=10: level=12
    elif dist > 2 and dist <=6: level=13
    elif dist > 1 and dist <= 2: level=14
    elif dist > 0.5 and dist <=1 : level=15
    elif dist > 0.3 and dist <=0.5 : level=16
    elif dist <=0.3 : level=17
    else: level = 15
    image = m.render(zoom=level)
    image.save(output_map_file_path)

    return True
