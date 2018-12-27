# Latency Analysis

This project works with python. Uses pandas, numpy and several other graphing libraries (matplotlib, mplleaflet, geopandas) for analysis of latency data from latency log files over gps coordinates.

Antenna Data for South Korean Republic


Building height data for South Korean Republic

Statistical information can obtained from the South Korean National Spatial Data Infrastructure Portal Open Datasets at: http://www.nsdi.go.kr, more specifically from http://data.nsdi.go.kr/dataset/12623

The data is however extremelly big (>300MB) and in Shapefile format (.shp, .shx, .dbf). For familiarity reasons, the GeoJson format is preferred. To convert the shapefile files to GeoJson format, QGIS is used. For instructions on how to convert between formats using QGIS an online search gives the results.

Also, the information provided by the South Korean National Spatial Data Infrastructure Portal Open Datasets has an EPSG5174 Coordinate Reference System which corresponds to the Korean Central Belt (http://osgeo.kr/17). This CRS works for Korea but is not widely used. So when using with other applications converting the data to EPSG4326, which is basically latitude,longitude coordinates, is preferable. 

QGIS can handle both the Shapefile -> GeoJson conversion and the EPSG5174 -> EPSG4326 conversion. However it is necessary to follow instructions in http://www.osgeo.kr/252?category=413186  for QGIS to find the correct CRS. This instructions basically reduce to downloading the "src.db" file in

https://drive.google.com/file/d/15JKM75mSgjTcMD5sUHLGltRZTeSqPjOV/view

and overwriting the in the folder QGIS_HOME\apps\qgis\resources\ . Then when you import the shapefile files in QGIS and asked to define the CRS for the file, filter by "korea" and select ESPG5174 Korean Central Belt. Now QGIS will have all the information for later conversion to EPSG4326.

## Usage

This script will probably only run in Ubuntu. To run it, save logAnalysis.py, and the log files in a folder in the same directory. 

### Version 2

The scripts lAv2.py and wm2.py replace the previous scripts for generating graphs and web maps. To use them, it is necessary to use the adequate file format. Download the scripts lAV2.py and wm2.py and in a folder in the same download directory store the log files. Execute first lAv2.py like this

python lAv2.py -f [path_to_csv_file] -r [resolution] -t [test_name]  -x [file_format_number] -y 0 -b [number_of_bins_for_network_latency_histogram] -o [number_of_bins_for_encoding_latency_histogram] -p [name_of_place_of_test]

This will create all the graphs for the log file input in the f argument. Then use the wm2.py script for generating latency web maps like this:

python wm2.py -f [path_to_csv_file] -y [camera_number]

It is necessary to execute this script for every camera whose latency map you want to generate. 
Camera numbers from 0 - 10 will generate Encoding Latency map.
10-19 will generate Network Latency map.
20-29 will generate Total Latency map.

For example, -y 1  will generate Encoding Latency Map for camera 1. -y 12 will generate Network Latency map for Camera 2.  -y 23  will generate Total Latency Map for camera 3. You can think of the first number as the type of latency that will be drawn, and the second number as the camera number for which the map will be draw.

Important! You have to modify the mplleaflet library according to the next section in order to use wm2.py. 

#### Webmap screenshot automation

Taking a screenshot of every web latency map is a tedious an inefficient process. You can modify the mplleaflet library in order to automate taking this screenshot. In order to do so, follow the comment at https://github.com/jwass/mplleaflet/issues/37  

Although this process is not the best (compared to generating an image from the html file) is a reasonable solution.


### Version 1

First you need to run logAnalysis.py, which will generate all the graphs and several csv documents. Then you need to run web_map_draw.py to generate all the latency maps. This maps will be displayed in the web browser and you need to save one by one. 

Then use the following command:

python logAnalysis.py -f [path_to_log_file] -g [path_to_gpx_file] -r [video_resolution, eg 1280x720p] -t [Test_name] -a [path_to_track_image] -k [path_to_speed_image] -x [log_file_format(1,2 or 3)] -y [number_of_camera_to_draw_latency_map_for]

Example

First run:  

 python logAnalysis.py -f 20181214/20181214B/2018_12_14_07_10_42.txt -r 1280x720 -t 20181214_TestA -a route.jpg -k speed.png -x 3 -y 1

Then run 

python web_map_image.py -f 20181214/20181214B/2018_12_14_07_10_42.txt -y 0


The final parameter "y" indicates the camera number for which the latency map will be drawn. It goes from 0 to 11 where:


0-4  Latency for camera x

5    Latency All Cameras

6-10 PC Clock latency for camera X

11   PC Clock latency for all cameras

  
