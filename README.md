----------------------------------------------------------------------
Title : Multimedia Sensor Dataset for the Analysis of Vehicle Movement
----------------------------------------------------------------------
URL : http://mediaq.usc.edu/mmsys17

We would like to provide datasets and programs used in this study.
One group of collected dataset consists of sensor data and matching
videos captured from smartphones, and the other group of
generated dataset is the files that were created through the data
processing. It also contains the Python program source used in 
the processing.

<The detailed description of the folders and files>

Folder Name 		Description
------------------------------------------------
/sensordata/json/ 	Json File
/sensordata/movie/ 	mp4 movie clip
/generated/csv/ 	csv merged (GPS and Sensor data merged data 
                        by 200ms unit)
/generated/image/ 	png (Sensor data temporal chart with map and 
                        first seen captured photo)
/program/ 		Python Program

==============================
<Dataset>
==============================

Data Size
------------------------------------------
  Type 			Size
------------------------------------------
Driving Time 		22.4 hours
Driving Distance 	731.6 miles
Video Size 		50.2 Gbyte
------------------------------------------

Json file is the sensor data file collected from smartphones. 
GPS and sensor data are included in the Json files. The movie folder 
has video files collected by smartphones.
The Android video format is "mp4" and iPhone’s is "mov". In the
CSV folder, there are files in which GPS and sensor data are merged
in time series sequence, and the generated and corrected data are
stored in csv format. There are images in the image folder that
combine three images which are the GPS trajectory image drawn
on the map, the first screen of video, and the sensor chart drawn in
time sequence.

We also collected some data while driving a long distance, mainly
freeways. In the selection of roads, we considered different sections
such as commuting residential streets, urban city roads, high speed
freeways, and traffic congested area

* Some data include abnormal movement pattern data generated arbitrarily.
  The 'PatternExamples.txt' file is an example of movement patterns.
  Note that these are just examples in this study.

** Some of the data includes data collected at the same place, 
  same time, same vehicle with iPhone and Android phone.
  It can be compared the sensor data patterns between Android and iOS.
  However, because the smartphone mount state and time do not match exactly
  Please refer to it just for reference.

    Android				iOS
    --------------------------------------------------------------------------------
    2017_3_3_Videotake_1488556872958	A970968C14_2017_3_03_Videotake_1488557028675
    2017_3_3_Videotake_1488557397346	A970968C14_2017_3_03_Videotake_1488557500967
    2017_3_3_Videotake_1488557830135	A970968C14_2017_3_03_Videotake_1488557926797
    2017_3_3_Videotake_1488557962102	A970968C14_2017_3_03_Videotake_1488558048007
    2017_3_3_Videotake_1488558118372	A970968C14_2017_3_03_Videotake_1488558217615
    2017_3_3_Videotake_1488558276211	A970968C14_2017_3_03_Videotake_1488558383391
    2017_3_3_Videotake_1488558407856	A970968C14_2017_3_03_Videotake_1488558461154
    2017_3_3_Videotake_1488906270623	A970968C14_2017_3_03_Videotake_1488906469876
    
==============================
<Program>
==============================

Python folder has five files. The main program is GenSensor.py.
GenCsv.py contains CSV file generation module, and GenGraph.py
contains graph image generation module. GenMap.py has a module
that draws the GPS trajectory on the map, and GenPhoto.py
has a module that captures the first screen of the moving video.
GenSensor.py program needs to set the Json, movie and output file
path.
In order to run the program, download it to a folder on your PC
and set the Json, movie, and output file paths in your GenSensor.py
(* If you did not install the relevant packages used by Import, 
 first install the packages using the pip install command.)

Program & Module description
--------------------------------
GenSensor.py 	Main Program - Import call module GenCsv, Graph, Map, Photo.
GenCsv.py 	CSV file generation - Speed Generation, Kalman Filtering
GenGraph.py 	Draw Sensor signal graph using matplotlib.pyplot library
GenMap.py 	GPS trajectory image generation on the Map
GenPhoto.py 	Generation First photo screen shot of movie

Download to a folder on your PC and set the json, movie, and output 
file paths in your GenSensor.py program.
An example of executing a python program in the cmd prompt Windows OS 
environment is as follows.

   c:\myfolder> python GenSensor.py
   
When you run GenSensor.py, it automatically generates csv and image folder 
and files under the output file path.

Wonhee Cho, Seon Ho Kim
Integrated Media Systems Center, University of Southern California, Los Angeles, CA 90089

---------------------------------------------------------------
Copyright (2017) by Wonhee Cho(danylight@gmail.com)

