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

  
