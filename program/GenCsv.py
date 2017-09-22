# -*- coding: utf-8 -*-
'''
Created on Mar 17, 2017
@author: Wonhee Cho
email : danylight@gmail.com
Web site: http://mediaq.usc.edu/mmsys17
Copyright 2017 Wonhee Cho
Function: Generate CSV File
'''
import sys
import json
import time
import datetime
from dateutil import tz
from pytz import timezone
from pprint import pprint
from math import radians, cos, sin, asin, sqrt, atan2

accArrayCnt = 0
ARRAY_SIZE = 50
AccArray = []
SpeedArray = []
avgAccValue = 0

class Kalman:
    """
    simplified version Kalman filtering logic
    Conversion from java to Python by Wonhee Cho
    source : https://trandi.wordpress.com/2011/05/16/kalman-filter-simplified-version/
    """
    Q = 0.00001
    R = 0.001
    P = 1
    X = 0
    K = 0

    def __init__(self, initValue, initR):
        self.X = initValue
        self.R = initR

    def setInit(self, newInit):
        X = newInit

    def measurementUpdate(self):
        self.K = (self.P + self.Q) / (self.P + self.Q + self.R)
        self.P = self.R * (self.P + self.Q) / (self.P + self.Q + self.R)

    def update(self, measurement):
        self.measurementUpdate()
        self.X = self.X + (measurement - self.X) * self.K
        return self.X


def distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    https://gist.github.com/rochacbruno/2883505
    """
    if lon1 == 0 or lat1 == 0 or lon2 == 0 or lat2 == 0: return 0
    radius = 6371  # km

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) \
                                        * cos(radians(lat2)) * sin(dlon / 2) * sin(dlon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = radius * c * 1000
    return d

# calculate average acc for getting acc speed
def get_acc_mean(sdata):
    sumacc = 0
    cnt = 0
    for i in sdata:
        if i[1] == 0:
            continue
        sumacc += i[8]
        cnt += 1
    avgacc = sumacc / cnt
    return (avgacc)

def get_diff_sec(befhour, befmin, befsec, chour, cmin, csec):
    bef_count = befhour * 3600 + befmin * 60 + befsec
    cur_count = chour * 3600 + cmin * 60 + csec
    return (cur_count - bef_count)

def add_acc(acc, speed):
    global accArrayCnt
    global ARRAY_SIZE
    global AccArray
    global SpeedArray
    if accArrayCnt > ARRAY_SIZE:
        del AccArray[:]
        del SpeedArray[:]
        accArrayCnt = 0
    AccArray.insert(accArrayCnt, acc)
    SpeedArray.insert(accArrayCnt, speed)
    accArrayCnt += 1

def get_acc_speed(phone_os,avgAccValue):
    global accArrayCnt
    global ARRAY_SIZE
    global AccArray
    sumAcc = 0
    if accArrayCnt < ARRAY_SIZE:
        j = accArrayCnt
    else:
        j = ARRAY_SIZE
    for i in range(0, j):
        if phone_os == "android":
            sumAcc += -(AccArray[i] - avgAccValue) / 2.2
        else:
            sumAcc += (AccArray[i] - avgAccValue) * 15

    resultSpeed = SpeedArray[0] + sumAcc
    return resultSpeed

# --------------- generate csv file -------------
def gen_csv(input_file_path,output_file_path):
    global accArrayCnt
    global ARRAY_SIZE
    global AccArray
    global SpeedArray
    global avgAccValue

    print(" gen csv, ",end="")
    json_data = open(input_file_path).read()
    try:
        data = json.loads(json_data)
    except ValueError as err:
        print("json error :", err)
        return False

    accArrayCnt = 0
    gpsspeed = 0
    distFromStart = 0
    phone_os = data['device_properties']['OS']
    user_name = data['Username']
    print("phone_os=", phone_os, " user_name=", user_name)
    gps = data['sensor_data'][0]['location_array_timestamp_lat_long_accuracy']
    sensor = data['sensor_data'][1]['sensor_array_timestamp_x_y_z']
    outfile = open(output_file_path, 'w')
    outfile.write(
        "gpsidx,accidx,date,time,speed,kspeed,accSpeed,d_sec,accdist,sentime," +
        "azimuth,pitch,roll,light,gps_lat,gps_lon,alti,accuracy,acc_x,acc_y,acc_z," +
        "kacc_x,kacc_y,kacc_z,mag_x,mag_y,mag_z,gyro_x,gyro_y,gyro_z,user_name\n")

    # ----------- calculate accmean for acc speed gen -------------
    avgAccValue = get_acc_mean(sensor)

    # ----------- Kalman filter instance gen
    filteredSpeed = Kalman(0, 0.0001)
    filteredAccX = Kalman(0, 0.0001)
    filteredAccY = Kalman(0, 0.0001)
    filteredAccZ = Kalman(0, 0.0001)
    gpsidx = 0
    accidx = 0
    bef_gpstimesec = 0
    bef_gpsspeed = 0
    bef_accuracy = 0
    # ------------ Read GPS dataset
    for gpsdata in gps:
        gpsdtime = int(gpsdata[0])
        gpsrtime = gpsdtime / 1000
        gpsttime = datetime.datetime.fromtimestamp(gpsrtime)
        gpsntime = gpsttime.strftime('%Y-%m-%d %H:%M:%S')
        gpsdate = gpsntime[0:10]
        gpstime = gpsntime[11:19]
        gpshour = int(gpstime[0:2])
        gpsmin = int(gpstime[3:5])
        gpssec = int(gpstime[6:8])
        gpstimesec = gpshour * 3600 + gpsmin * 60 + gpssec
        gps_lat,gps_lon,alti = gpsdata[2:5]
        accuracy = int(gpsdata[5])
        if gps_lat == 0 or gps_lon == 0: continue
        if gpsidx == 0:
            d_sec = 0
            distFromGps = 0
            gpsspeed = 0
        else:
            d_sec = gpstimesec - bef_gpstimesec
            if accuracy > 10:
                gpsspeed = bef_gpsspeed
                gps_lon = bef_gps_lon
                gps_lat = bef_gps_lat
                distFromGps = 0
            else:
                distFromGps = distance(gps_lon, gps_lat, bef_gps_lon, bef_gps_lat)
                gpsspeed = distFromGps * 3.6 # GPS speed calculate
                if abs( gpsspeed - bef_gpsspeed) > 50: gpsspeed = bef_gpsspeed
                if bef_accuracy > 10: gpsspeed = bef_gpsspeed
        if gpsidx == 1: # Actual gps speed is generated after 1 sec. To start the base speed value from 1 second.
            del AccArray[:]
            del SpeedArray[:]
            accArrayCnt = 0
        distFromStart += distFromGps
        gpsspeedMph = gpsspeed * 0.621371 # convert km/h to mph
        kfilterdSpeed = filteredSpeed.update(gpsspeedMph)

        # -- process merging sensor data
        for j in range(accidx, len(sensor)):
            sendata = sensor[j]
            if sendata[1] == 0:
                accidx += 1
                continue
            sendtime = int(sendata[0])
            senrtime = sendtime / 1000
            senttime = datetime.datetime.fromtimestamp(senrtime)
            senntime = senttime.strftime('%Y-%m-%d %H:%M:%S')
            sendate = senntime[0:10]
            sentime = senntime[11:19]
            senhour = int(sentime[0:2])
            senmin = int(sentime[3:5])
            sensec = int(sentime[6:8])
            sentimesec = senhour * 3600 + senmin * 60 + sensec

            if gpstimesec < sentimesec: break
            azimuth,pitch,roll,light,acc_x,acc_y,acc_z,mag_x,mag_y,mag_z,gyro_x,gyro_y,gyro_z = sendata[2:15]
            if acc_x == 0 and acc_y == 0 and acc_z == 0.0: continue
            if accidx == 0:
                filteredAccX.setInit(acc_x)
                filteredAccY.setInit(acc_y)
                filteredAccZ.setInit(acc_z)
                fAccX = acc_x
                fAccY = acc_y
                fAccZ = acc_z
            else:
                fAccX = filteredAccX.update(acc_x)
                fAccY = filteredAccY.update(acc_y)
                fAccZ = filteredAccZ.update(acc_z)
            if (gpsidx < 3 and gpsspeed != 0) or gpsidx >= 3:
                add_acc(acc_z, gpsspeedMph)
            else:
                add_acc(acc_z, 0)
            acc_speed = get_acc_speed(phone_os,avgAccValue)
            accidx += 1
            buff = "%d,%d,%s,%s,%f,%f,%f,%d,%f,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (
            gpsidx, accidx, gpsdate, gpstime, gpsspeedMph, kfilterdSpeed, acc_speed, d_sec, distFromStart, sentime,
            azimuth, pitch, roll, light, gps_lat, gps_lon, alti, accuracy, acc_x, acc_y, acc_z, fAccX, fAccY, fAccZ, mag_x,
            mag_y, mag_z, gyro_x, gyro_y, gyro_z, user_name)
            outfile.write(buff)

        bef_gpstimesec = gpstimesec
        bef_gps_lat = gps_lat
        bef_gps_lon = gps_lon
        bef_gpsspeed = gpsspeed
        bef_accuracy = accuracy
        gpsidx += 1
        #if gpsidx > 120: break
    if gpsidx <=2 or accidx <=2 : return False
    else: return True
