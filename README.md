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
 
