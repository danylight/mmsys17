'''
Created on Mar 17, 2017
@author: Wonhee Cho
email : danylight@gmail.com
Web site: http://mediaq.usc.edu/mmsys17
Copyright 2017 Wonhee Cho
Function: Generate Graph
'''
import sys
import json
import numpy as np
import csv
from staticmap import StaticMap, CircleMarker
from motionless import LatLonMarker, DecoratedMap
from math import radians, cos, sin, asin, sqrt, atan2
import matplotlib.pyplot as plt
from matplotlib import mlab
from pylab import figure, axes, pie, title, show

#=========Generate Graph function =====================
def gen_graph(input_json_file_path,input_csv_file_path,output_graph_file_path):
    print(" graph, ",end="")
    json_data=open(input_json_file_path).read()
    data = json.loads(json_data)
    phone_os = data['device_properties']['OS']
    user_name = data['Username']

    fname = input_csv_file_path.split('\\')
    data = np.genfromtxt(input_csv_file_path, dtype=None, delimiter=',', names=True)
    if len(data)==0: return False
    max_range = len(data['speed']) + int(len(data['speed']) * 0.2)
    etime = int((data['accidx'][len(data['accidx'])-1])/5)
    dist = data['accdist'][len(data['accdist'])-1]/1000.0
    start_time = data['time'][0]
    mdist = dist * 0.621371
    grid, num = [], []
    if max_range > 20000:
        for i in range(max_range):
            if i%3000==0:
                grid.append(i)
                num.append(int(i/300))
    elif max_range > 1000:
        for i in range(max_range):
            if i%300==0:
                grid.append(i)
                num.append(int(i/300))
    elif max_range > 100:
        for i in range(max_range):
            if i%30==0:
                grid.append(i)
                num.append(int(i/5))
    else:
        for i in range(max_range):
            if i%5==0:
                grid.append(i)
                num.append(int(i/5))

    fig = plt.figure(figsize=(12,7))
    plt.subplot(511)
    if etime > 200: stime = "%.1f min" % (etime/60)
    else: stime = "%d sec" % (etime)
    str_title = "Filename : %s, start_time: %s \nTime = %s, Distance = %.3f km, %.3f mile, Phone_os=%s, User_name=%s" % \
                (fname[len(fname)-1], start_time.decode('UTF-8'), stime, dist, mdist, phone_os, user_name)
    plt.title(str_title,loc='left')
    plt.suptitle('MediaQ Sensor Data Analysis',fontsize=18,fontweight='bold')
    plt.grid(True)
    plt.plot(data['kacc_x'], 'b',label="kacc_x")
    plt.plot(data['kacc_y'], 'g',label="kacc_y")
    plt.xlabel('time')
    plt.ylabel('acceleration')
    plt.plot(data['kacc_z'],'r',label='kacc_z')
    plt.xticks(grid,num,fontsize=8)
    plt.yticks(fontsize=8)
    plt.legend(loc='upper right')

    plt.subplot(512)
    plt.grid(True)
    plt.plot(data['speed'], 'g',label="g speed")
    plt.plot(data['kspeed'], 'b',label="k speed")
    plt.plot(data['accSpeed'],'r',label='a speed')
    plt.ylabel('Speed')
    plt.xticks(grid,num,fontsize=8)
    plt.yticks(fontsize=8)
    plt.legend(loc='upper right')

    plt.subplot(513)
    plt.grid(True)
    plt.plot(data['azimuth'], 'r',label="azimuth")
    plt.plot(data['pitch'], 'g',label="pitch")
    plt.plot(data['roll'], 'b',label="roll")
    plt.ylabel('Orientation')
    plt.xticks(grid,num,fontsize=8)
    plt.yticks(range(-20, 360, 100), fontsize=8)
    plt.legend(loc='upper right')

    plt.subplot(514)
    plt.grid(True)
    plt.plot(data['gyro_x'], 'r',label="gyro_x")
    plt.plot(data['gyro_y'], 'g',label="gyro_y")
    plt.plot(data['gyro_z'], 'b',label="gyro_z")
    plt.ylabel('Gyroscope')
    plt.xticks(grid,num,fontsize=8)
    plt.yticks(fontsize=8)
    plt.legend(loc='upper right')

    plt.subplot(515)
    plt.tick_params(axis='both', which='both', bottom='off', top='off',
                    labelbottom='on', left='off', right='off', labelleft='on')
    plt.grid(True)
    plt.plot(data['mag_x'], 'r',label="mag_x")
    plt.plot(data['mag_y'], 'g',label="mag_y")
    plt.plot(data['mag_z'], 'b',label="mag_z")
    plt.xticks(grid,num,fontsize=8)
    plt.yticks(fontsize=8)
    plt.legend(loc='upper right')

    plt.ylabel('magnet')
    if max_range > 1000:
        plt.xlabel('time (minute)', fontsize=15)
    else:
        plt.xlabel('time (second)', fontsize=15)

    fig.savefig(output_graph_file_path)
    plt.close(fig)

    return True
