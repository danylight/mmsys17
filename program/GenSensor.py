'''
Created on Mar 17, 2017
@author: Wonhee Cho
email : danylight@gmail.com
Web site: http://mediaq.usc.edu/mmsys17
Copyright 2017 Wonhee Cho
Function: main module
'''
import os
import json

from PIL import Image
from resizeimage import resizeimage
import cv2

from GenCsv import gen_csv
from GenMap import gen_map
from GenGraph import gen_graph
from GenPhoto import gen_photo

# file path: change your file path in your computer
json_path = "C:\\data\\mmsys17_2\\sensordata\\json\\"
movie_path = "C:\\data\\mmsys17_2\\sensordata\\movie\\"
out_path = "C:\\data\\mmsys17_2\\generated\\"

filecnt = 0
for filename in os.listdir(json_path):
    if '.json' in filename:
        print("=====> Start Sensor Data Generation (", filecnt, ") \n json file : ",filename)
        outfilename = filename.replace(".json", '')
        input_filepath_json = json_path+filename
        json_data=open(input_filepath_json).read()
        try:
            data = json.loads(json_data)
        except ValueError as err:
            print("========> json parsing error :", err)
            continue
        user_name = data['Username']
        phone_os = data['device_properties']['OS']
        if not os.path.exists(out_path + "csv\\"): os.makedirs(out_path + "csv\\")
        if not os.path.exists(out_path + "image\\"): os.makedirs(out_path + "image\\")
        output_filepath_csv = out_path + "csv\\"+ outfilename+".csv"
        output_filepath_graph = out_path + "image\\" + outfilename + "_graph.png"
        output_filepath_gmap = out_path + "image\\" + outfilename + "_gmap.png"
        output_filepath_merge = out_path + "image\\" + outfilename + "_photo.png"
        output_filepath_temp = out_path + "image\\" + outfilename + "_photo2.jpg"
        if phone_os == "android":
            output_filepath_movie = movie_path + outfilename+".mp4"
        else:
            output_filepath_movie = movie_path + outfilename+".mov"
        print(" movie file : ",output_filepath_movie)

        check = gen_csv(input_filepath_json,output_filepath_csv)
        if not check:
            print("========> csv generation error :",outfilename)
            continue
        check = gen_map(input_filepath_json,output_filepath_gmap)
        if not check:
            print("========> map generation error :",outfilename)
            continue
        check = gen_graph(input_filepath_json,output_filepath_csv,output_filepath_graph)
        if not check:
            print("========> graph generation error :",outfilename)
            continue

        check = gen_photo(output_filepath_movie,output_filepath_temp)

        # merge three images - graph, gmap, movie first screen shot
        loadfilename = []
        loadfilename.append(output_filepath_graph)
        loadfilename.append(output_filepath_gmap)
        loadfilename.append(output_filepath_temp)
        newimg=Image.new("RGBA",(1200,1100 ) )
        image = Image.open(loadfilename[1])
        newimg.paste(image,(0,0))
        if check:
            image = Image.open(loadfilename[2])
            image2 = resizeimage.resize_cover(image, [720, 480])
            newimg.paste(image2,(600,0))
        image = Image.open(loadfilename[0])
        newimg.paste(image,(0,400))
        newimg.save(output_filepath_merge,"PNG")

        # remove temporal files
        if os.path.exists(output_filepath_graph): os.remove(output_filepath_graph)
        if os.path.exists(output_filepath_gmap): os.remove(output_filepath_gmap)
        if os.path.exists(output_filepath_temp): os.remove(output_filepath_temp)

        filecnt += 1
        print("===> (",filecnt,") files generated..")

print("==========> Finish generation : total ", filecnt, " files generated.")
