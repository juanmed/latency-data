#!/usr/bin/env python
# -*- coding: cp949 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import argparse
from datetime import timedelta
from datetime import datetime
from dateutil import parser     # 
import json                    
import geopandas as gpd
import geojsonio				# sudo pip install geojsonio		
from geojsonio import display   
from shapely.geometry import Point, Polygon
import contextily as ctx    # sudo pip install contextily, pip install cartopy, pip install mercantile,
# pip install rasterio, 
from mpl_toolkits.axes_grid1 import make_axes_locatable

#import descartes   #pip install descartes

# for working with gpx file
import gpxpy
import gpxpy.gpx

# creating web map, with mplleaflet
import mplleaflet

# to work with hangul
import codecs
from io import open

import math
import time
import cv2

import google_streetview.api

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA as sklearnPCA

from mpl_toolkits.mplot3d import Axes3D

import re

key = "AIzaSyCLfa54Y6BLEVS8NQNgZPU8GTtDvEphiwA"


# disable pandas warning
pd.options.mode.chained_assignment = None

# Calculate drop rate 
def getDropRate(a):
	# get number of normaly received frame
	c = a.dropna(how='any')
	n = len(c)
	#print ("n: "+str(n))
	# get number of "drop frame : old frame"
	d = len(a[ a['id'] == 'drop frame : old frame' ])
	#print ("d: "+str(d))
	# get m = no of cameras 'k' * (max(seq) - min(seq))
	k = len(c.groupby('id'))
	#print ("k: "+str(k))
	c['seq'] = c['seq'].str.extract('(\d+)', expand=True).astype(int)
	minseq = min(c['seq'])
	maxseq = max(c['seq'])
	#print ("min seq: "+str(minseq)+" max seq: "+str(maxseq))
	m = k*(maxseq-minseq+1)
	#print("m: "+str(m))
	# get droprate
	dr = (1.0-(n+d)*1.0/m)*100.0
	print("drop rate: "+str(dr)+"%")
	return dr

# Clean imported data
def cleanData(data):
	data = data.dropna(how='any')
	data = data[ ~data.loc[:,:].isnull() ]
	#print ("Clean log shape: "+str(data.shape)+" Type: "+str(type(data))+" Types: "+str(data.dtypes))
	return data

# Convert imported data to correct data types
def convertData(data, types=[] ):
	columns = data.columns
	#datatypes = [type(k) for k in types]
	for (datatype, col) in zip(types, columns):
		if ( datatype == int ):
			data[col] = data[col].str.extract('(\d+)', expand=True)	.astype(int)
			#data[col] = map(lambda x: x.str.extract('(\d+)', expand=True), data[col])
		if ( datatype == datetime ):
			#data[col] = map(lambda x: datetime.strptime(x[8:len(x)-2],"%y/%m/%d %H:%M:%S %z"), data[col])
			#data[col] = datetime.strptime(data[col][8: len(data[col]) - 2], "%y/%m/%e %H:%M:%S %z")
			# for now exclude UTC offset
			data[col]= map(lambda x: parser.parse(x[8:len(x)-7] ,yearfirst = True), data[col])
		if (datatype == str):
			data[col] = str(data[col])
		if (datatype == "dms"):
			data[col] = map(lambda x: dms2dd(x), data[col])
		if ( datatype ==  "ignore" ):
			continue
		if (datatype == float):
			#data[col] = data[col].str.extract('\d+\.\d+', expand=True).astype(float)
			data[col]= map(lambda x: float(re.findall("\d+\.\d+",x)[0]), data[col])
			#data[col] = str(data[col])
	return data

# Create a parser for the command line arguments
def createCommandLineParser():
	parser1 = argparse.ArgumentParser(description='Code for Analyzing log files.')
	parser1.add_argument('-f', help='Path to log file.', default='log201811071627_1080p_0.txt')
	parser1.add_argument('-b', help='Histogram bin size', default=200)
	parser1.add_argument('-g', help='Path to gpx file.', default='20181112/2018._11._12._noon_5_09_18.gpx')
	parser1.add_argument('-r', help='Video Resolution', default='1280*720.gpx')
	parser1.add_argument('-t', help='Test Name', default='20180101 TestA')
	parser1.add_argument('-a', help='Name of GPS Track image', default='GPS Track image file name with extension')
	parser1.add_argument('-k', help='Name of GPS Data image', default='GPS Data image file name with extension')
	parser1.add_argument('-x', help='LOG File format: 1: oldest , 2: new  3:newest ', default="old")
	parser1.add_argument('-y', help='Number of camera for which latency map will be draw, 5 = all cameras', default="5")
	parser1.add_argument('-q', help='Colormap to be used [viridis_r, magma_r, inferno_r]', default="inferno_r")

	#parser.add_argument('-w', help='Path to rotated image', default='r1.jpg')
	args = parser1.parse_args()
	return args

# draw a Latency Graph
def drawLatencyGraph(data,ax,stats,camnumber,col,data_dic):

	#cam0.plot(x = 'seq', y ='latency', label = 'Camera 0' , legend = True)
	ax.plot(data['seq'],data['latency'], color = col)
	ax.set_xlabel('Sequence ')
	ax.set_ylabel('Latency {ms}')
	minlat = stats.loc['min','latency']
	maxlat = stats.loc['max','latency']
	avg = stats.loc['mean','latency']
	std = stats.loc['std','latency']
	ax.set_title('Camera '+str(camnumber)+" min: {:.2f}".format(minlat)+", max: {:.2f}".format(maxlat)+", mean: {:.2f}".format(avg)+" std: {:.2f}".format(std))

	#draw line on mean
	meanline = np.ones_like(data['seq'])*avg
	ax.plot(data['seq'],meanline, color = 'c')

	# fill data for md file creation later
	key = "cam"+str(camnumber)+"_avg"
	data_dic[key]=avg
	key = "cam"+str(camnumber)+"_min"
	data_dic[key] = minlat
	key = "cam"+str(camnumber)+"_max"
	data_dic[key] = maxlat
	key = "cam"+str(camnumber)+"_std"
	data_dic[key] = std
	return data_dic

# draw a Latency Graph
def drawrawLatencyGraph(data,ax,stats,camnumber,col,data_dic):

	#cam0.plot(x = 'seq', y ='latency', label = 'Camera 0' , legend = True)
	ax.plot(data['seq'],data['raw_UTC_latency'], color = col)
	ax.set_xlabel('Sequence ')
	ax.set_ylabel('Raw Latency {ms}')
	minlat = stats.loc['min','raw_UTC_latency']
	maxlat = stats.loc['max','raw_UTC_latency']
	avg = stats.loc['mean','raw_UTC_latency']
	std = stats.loc['std','raw_UTC_latency']
	ax.set_title(" Min: {:.2f}".format(minlat)+", max: {:.2f}".format(maxlat)+", mean: {:.2f}".format(avg)+" std: {:.2f}".format(std))

	#draw line on mean
	meanline = np.ones_like(data['seq'])*avg
	ax.plot(data['seq'],meanline, color = 'c')

	# fill data for md file creation later
	key = "cam"+str(camnumber)+"_raw_avg"
	data_dic[key]=avg
	key = "cam"+str(camnumber)+"_raw_min"
	data_dic[key] = minlat
	key = "cam"+str(camnumber)+"_raw_max"
	data_dic[key] = maxlat
	key = "cam"+str(camnumber)+"_raw_std"
	data_dic[key] = std
	return data_dic

# draw PC Network Latency minus Latency Graph
def draw_PCNetworkLatency_Latency_Diff_Graph(data,ax,stats,camnumber,col,data_dic):

	#cam0.plot(x = 'seq', y ='latency', label = 'Camera 0' , legend = True)
	a = data['pc_network_latency'] - data['latency']
	ax.plot(data['seq'],a, color = col)
	ax.set_xlabel('Sequence ')
	ax.set_ylabel('PC Network Latency - Latency (Difference)  {ms}')
	minlat = min(a)
	maxlat = max(a)
	avg = a.mean()
	std = a.std()
	ax.set_title(" Min: {:.2f}".format(minlat)+", max: {:.2f}".format(maxlat)+", mean: {:.2f}".format(avg)+" std: {:.2f}".format(std))

	#draw line on mean
	meanline = np.ones_like(data['seq'])*avg
	ax.plot(data['seq'],meanline, color = 'c')

	# fill data for md file creation later
	# pnlml = pc clock latency minus latency
	key = "cam"+str(camnumber)+"_pnlml_raw_avg"
	data_dic[key]=avg
	key = "cam"+str(camnumber)+"_pnlml_raw_min"
	data_dic[key] = minlat
	key = "cam"+str(camnumber)+"_pnlml_raw_max"
	data_dic[key] = maxlat
	key = "cam"+str(camnumber)+"_pnlml_raw_std"
	data_dic[key] = std
	return data_dic

# draw PC Clock Network Latency Graph
def draw_PCClock_Network_LatencyGraph(data,ax,stats,camnumber,col,data_dic):

	#cam0.plot(x = 'seq', y ='latency', label = 'Camera 0' , legend = True)
	ax.plot(data['seq'],data['pc_network_latency'], color = col)
	ax.set_xlabel('Sequence ')
	ax.set_ylabel('PC Clock Network Latency {ms}')
	minlat = stats.loc['min','pc_network_latency']
	maxlat = stats.loc['max','pc_network_latency']
	avg = stats.loc['mean','pc_network_latency']
	std = stats.loc['std','pc_network_latency']
	ax.set_title(" Min: {:.2f}".format(minlat)+", max: {:.2f}".format(maxlat)+", mean: {:.2f}".format(avg)+" std: {:.2f}".format(std))

	#draw line on mean
	meanline = np.ones_like(data['seq'])*avg
	ax.plot(data['seq'],meanline, color = 'c')

	# fill data for md file creation later
	key = "cam"+str(camnumber)+"_pc_network_avg"
	data_dic[key]=avg
	key = "cam"+str(camnumber)+"_pc_network_min"
	data_dic[key] = minlat
	key = "cam"+str(camnumber)+"_pc_network_max"
	data_dic[key] = maxlat
	key = "cam"+str(camnumber)+"_pc_network_std"
	data_dic[key] = std
	return data_dic

# draw a Latency Graph
def drawSatelliteGraph(data,ax,stats,camnumber,col,data_dic):

	#cam0.plot(x = 'seq', y ='latency', label = 'Camera 0' , legend = True)
	ax.plot(data['seq'],data['sat'], color = col)
	ax.set_xlabel('Sequence ')
	ax.set_ylabel('Satellite Count')
	minlat = stats.loc['min','sat']
	maxlat = stats.loc['max','sat']
	avg = stats.loc['mean','sat']
	std = stats.loc['std','sat']
	ax.set_title("Min: {:.2f}".format(minlat)+", max: {:.2f}".format(maxlat)+", mean: {:.2f}".format(avg)+" std: {:.2f}".format(std))

	#draw line on mean
	meanline = np.ones_like(data['seq'])*avg
	ax.plot(data['seq'],meanline, color = 'c')

	# fill data for md file creation later
	key = "cam"+str(camnumber)+"_sat_avg"
	data_dic[key]=avg
	key = "cam"+str(camnumber)+"_sat_min"
	data_dic[key] = minlat
	key = "cam"+str(camnumber)+"_sat_max"
	data_dic[key] = maxlat
	key = "cam"+str(camnumber)+"_sat_std"
	data_dic[key] = std
	return data_dic

# draw a Latency Graph
def drawpcLatencyGraph(data,ax,stats,camnumber,col,data_dic):

	#cam0.plot(x = 'seq', y ='latency', label = 'Camera 0' , legend = True)
	ax.plot(data['seq'],data['pc_latency'], color = col)
	ax.set_xlabel('Sequence ')
	ax.set_ylabel('PC Latency {ms}')
	minlat = stats.loc['min','pc_latency']
	maxlat = stats.loc['max','pc_latency']
	avg = stats.loc['mean','pc_latency']
	std = stats.loc['std','pc_latency']
	ax.set_title('Camera '+str(camnumber)+" min: {:.2f}".format(minlat)+", max: {:.2f}".format(maxlat)+", mean: {:.2f}".format(avg)+" std: {:.2f}".format(std))

	#draw line on mean
	meanline = np.ones_like(data['seq'])*avg
	ax.plot(data['seq'],meanline, color = 'c')

	# fill data for md file creation later
	key = "cam"+str(camnumber)+"_avg_pc"
	data_dic[key]=avg
	key = "cam"+str(camnumber)+"_min_pc"
	data_dic[key] = minlat
	key = "cam"+str(camnumber)+"_max_pc"
	data_dic[key] = maxlat
	key = "cam"+str(camnumber)+"_std_pc"
	data_dic[key] = std
	return data_dic

# draw combined a Latency Graph
def drawCombinedLatencyGraph(data,ax,stats,camnumber,col,data_dic):

	#cam0.plot(x = 'seq', y ='latency', label = 'Camera 0' , legend = True)
	ax.plot(data['seq'],data['pc_latency'], color = 'k', label = 'PC Clock Latency', linestyle = '--')
	ax.plot(data['seq'],data['latency'], color = col, label = 'GPS Latency')
	ax.set_xlabel('Sequence ')
	ax.set_ylabel('Latency {ms}')
	ax.legend(loc='upper right', shadow=True, fontsize='large')
	ax.set_title('Camera '+str(camnumber)+" PC Clock Latency and GPS Latency")

	#draw line on mean
	meanline = np.ones_like(data['seq'])*data['latency'].mean()
	ax.plot(data['seq'],meanline, color = 'c')
	meanline2 = np.ones_like(data['seq'])*data['pc_latency'].mean()
	ax.plot(data['seq'],meanline2, color = 'k', linestyle = '--')

	return data_dic

# draw combined a Latency Graph and PC Network Graph
def drawCombinedLatency_PCNetworkLatency_Graph(data,ax,stats,camnumber,col,data_dic):

	#cam0.plot(x = 'seq', y ='latency', label = 'Camera 0' , legend = True)
	ax.plot(data['seq'],data['latency'], color = 'k', label = 'Latency')
	ax.plot(data['seq'],data['pc_network_latency'], color = col, label = 'PC Clock Network Latency')
	ax.set_xlabel('Sequence ')
	ax.set_ylabel('Latency {ms}')
	ax.legend(loc='upper right', shadow=True, fontsize='large')
	ax.set_title("PC Clock Network Latency, Latency vs Sequence")

	#draw line on mean
	meanline = np.ones_like(data['seq'])*data['latency'].mean()
	ax.plot(data['seq'],meanline, color = 'k')
	meanline2 = np.ones_like(data['seq'])*data['pc_network_latency'].mean()
	ax.plot(data['seq'],meanline2, color = col, linestyle = '--')

	return data_dic


# draw Difference a Latency Graph
def drawDifferenceLatencyGraph(data,ax,stats,camnumber,col,data_dic):

	#cam0.plot(x = 'seq', y ='latency', label = 'Camera 0' , legend = True)
	ax.plot(data['seq'],data['dif_latency'], color = col, label = 'PC_Clock Latency - GPS Latency')
	ax.set_xlabel('Sequence ')
	ax.set_ylabel(' Latency Difference {ms}')
	ax.legend(loc='upper right', shadow=True, fontsize='large')
	minlat = stats.loc['min','dif_latency']
	maxlat = stats.loc['max','dif_latency']
	avg = stats.loc['mean','dif_latency']
	std = stats.loc['std','dif_latency']
	ax.set_title('Camera '+str(camnumber)+" min: {:.2f}".format(minlat)+", max: {:.2f}".format(maxlat)+", mean: {:.2f}".format(avg)+" std: {:.2f}".format(std))

	#draw line on mean
	meanline = np.ones_like(data['seq'])*avg
	ax.plot(data['seq'],meanline, color = 'c', linestyle = '--')
	return data_dic


# draw a Histogram
def drawHistogram(data,ax,stats,camnumber, bins,col):
	bins = np.arange(stats.loc['min','latency'],stats.loc['max','latency'],bins	)
	ax.hist(data['latency'], bins, [stats.loc['min','latency'],stats.loc['max','latency']], color = col)
	ax.set_title("Camera "+str(camnumber))
	ax.set_xlabel("Latency {ms}")
	ax.set_ylabel("Count")
	ax.set_xticks(bins)

# draw a Histogram
def drawpcHistogram(data,ax,stats,camnumber, bins,col):
	bins = np.arange(stats.loc['min','pc_latency'],stats.loc['max','pc_latency'],bins	)
	ax.hist(data['pc_latency'], bins, [stats.loc['min','pc_latency'],stats.loc['max','pc_latency']], color = col)
	ax.set_title("Camera "+str(camnumber))
	ax.set_xlabel("PC Latency {ms}")
	ax.set_ylabel("Count")
	ax.set_xticks(bins)

# draw and save all latency and histogram graphs for all cameras
def drawGraphs(data_dic):
	if(doplot):

		#print cam1.tail(15)						

		print (" *************** DRAWING LATENCY 0 **********************")																																																																																	
		fig0 = plt.figure(figsize=(20,10))
		fig0.suptitle('Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig0ax1 = fig0.add_subplot(1,1,1)																										
		data_dic = drawLatencyGraph(cam0,fig0ax1, cam0stats,0,'r',data_dic)
		print (" *************** DRAWING LATENCY 1 **********************") 
		fig1 = plt.figure(figsize=(20,10))
		fig1.suptitle('Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig1ax1 = fig1.add_subplot(1,1,1)
		data_dic = drawLatencyGraph(cam1,fig1ax1, cam1stats,1,'g', data_dic)
		print (" *************** DRAWING LATENCY 2 **********************") 
		fig2 = plt.figure(figsize=(20,10))
		fig2.suptitle('Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig2ax1 = fig2.add_subplot(1,1,1)
		data_dic = drawLatencyGraph(cam2,fig2ax1, cam2stats,2,'b', data_dic)
		print (" *************** DRAWING LATENCY 3 **********************") 
		fig3 = plt.figure(figsize=(20,10))
		fig3.suptitle('Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig3ax1 = fig3.add_subplot(1,1,1)
		data_dic = drawLatencyGraph(cam3,fig3ax1, cam3stats,3,'m', data_dic)
		print (" *************** DRAWING LATENCY 4 **********************") 
		fig4 = plt.figure(figsize=(20,10))
		fig4.suptitle('Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig4ax1 = fig4.add_subplot(1,1,1)
		data_dic = drawLatencyGraph(cam4,fig4ax1, cam4stats,4,'c', data_dic)

		plt.close('all')

		print (" *************** DRAWING PC LATENCY 0 **********************")																																																																																	
		fig20 = plt.figure(figsize=(20,10))
		fig20.suptitle('PC Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig20ax1 = fig20.add_subplot(1,1,1)																										
		data_dic = drawpcLatencyGraph(cam0,fig20ax1, cam0stats,0,'r',data_dic)
		print (" *************** DRAWING PC LATENCY 1 **********************") 
		fig21 = plt.figure(figsize=(20,10))
		fig21.suptitle('PC Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig21ax1 = fig21.add_subplot(1,1,1)
		data_dic = drawpcLatencyGraph(cam1,fig21ax1, cam1stats,1,'g', data_dic)
		print (" *************** DRAWING PC LATENCY 2 **********************") 
		fig22 = plt.figure(figsize=(20,10))
		fig22.suptitle('PC Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig22ax1 = fig22.add_subplot(1,1,1)
		data_dic = drawpcLatencyGraph(cam2,fig22ax1, cam2stats,2,'b', data_dic)
		print (" *************** DRAWING PC LATENCY 3 **********************") 
		fig23 = plt.figure(figsize=(20,10))
		fig23.suptitle('PC Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig23ax1 = fig23.add_subplot(1,1,1)
		data_dic = drawpcLatencyGraph(cam3,fig23ax1, cam3stats,3,'m', data_dic)
		print (" *************** DRAWING PC LATENCY 4 **********************") 
		fig24 = plt.figure(figsize=(20,10))
		fig24.suptitle('PC Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig24ax1 = fig24.add_subplot(1,1,1)
		data_dic = drawpcLatencyGraph(cam4,fig24ax1, cam4stats,4,'c', data_dic)	


		plt.close('all')
		print (" *************** DRAWING COMBINED LATENCY 0 **********************")																																																																																	
		fig30 = plt.figure(figsize=(20,10))
		fig30.suptitle('PC Clock Latency and GPS Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig30ax1 = fig30.add_subplot(1,1,1)																										
		data_dic = drawCombinedLatencyGraph(cam0,fig30ax1, cam0stats,0,'r',data_dic)
		print (" *************** DRAWING COMBINED LATENCY 1 **********************") 
		fig31 = plt.figure(figsize=(20,10))
		fig31.suptitle('PC Clock Latency and GPS Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig31ax1 = fig31.add_subplot(1,1,1)
		data_dic = drawCombinedLatencyGraph(cam1,fig31ax1, cam1stats,1,'g', data_dic)
		print (" *************** DRAWING COMBINED LATENCY 2 **********************") 
		fig32 = plt.figure(figsize=(20,10))
		fig32.suptitle('PC Clock Latency and GPS Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig32ax1 = fig32.add_subplot(1,1,1)
		data_dic = drawCombinedLatencyGraph(cam2,fig32ax1, cam2stats,2,'b', data_dic)
		print (" *************** DRAWING COMBINED LATENCY 3 **********************") 
		fig33 = plt.figure(figsize=(20,10))
		fig33.suptitle('PC Clock Latency and GPS Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig33ax1 = fig33.add_subplot(1,1,1)
		data_dic = drawCombinedLatencyGraph(cam3,fig33ax1, cam3stats,3,'m', data_dic)
		print (" *************** DRAWING COMBINED LATENCY 4 **********************") 
		fig34 = plt.figure(figsize=(20,10))
		fig34.suptitle('PC Clock Latency and GPS Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig34ax1 = fig34.add_subplot(1,1,1)
		data_dic = drawCombinedLatencyGraph(cam4,fig34ax1, cam4stats,4,'c', data_dic)

		plt.close('all')

		print (" *************** DRAWING DIFFERENCE LATENCY 0 **********************")																																																																																	
		fig40 = plt.figure(figsize=(20,10))
		fig40.suptitle('PC Clock Latency and GPS Latency Difference vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig40ax1 = fig40.add_subplot(1,1,1)																										
		data_dic = drawDifferenceLatencyGraph(cam0,fig40ax1, cam0stats,0,'r',data_dic)
		print (" *************** DRAWING DIFFERENCE LATENCY 1 **********************") 
		fig41 = plt.figure(figsize=(20,10))
		fig41.suptitle('PC Clock Latency and GPS Latency Difference vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig41ax1 = fig41.add_subplot(1,1,1)
		data_dic = drawDifferenceLatencyGraph(cam1,fig41ax1, cam1stats,1,'g', data_dic)
		print (" *************** DRAWING DIFFERENCE LATENCY 2 **********************") 
		fig42 = plt.figure(figsize=(20,10))
		fig42.suptitle('PC Clock Latency and GPS Latency Difference vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig42ax1 = fig42.add_subplot(1,1,1)
		data_dic = drawDifferenceLatencyGraph(cam2,fig42ax1, cam2stats,2,'b', data_dic)
		print (" *************** DRAWING DIFFERENCE LATENCY 3 **********************") 
		fig43 = plt.figure(figsize=(20,10))
		fig43.suptitle('PC Clock Latency and GPS Latency Difference vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig43ax1 = fig43.add_subplot(1,1,1)
		data_dic = drawDifferenceLatencyGraph(cam3,fig43ax1, cam3stats,3,'m', data_dic)
		print (" *************** DRAWING DIFFERENCE LATENCY 4 **********************") 
		fig44 = plt.figure(figsize=(20,10))
		fig44.suptitle('PC Clock Latency and GPS Latency Difference vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig44ax1 = fig44.add_subplot(1,1,1)
		data_dic = drawDifferenceLatencyGraph(cam4,fig44ax1, cam4stats,4,'c', data_dic)


		plt.close('all')

		print (" *************** DRAWING RAW LATENCY ALL **********************")																																																																																	
		fig50 = plt.figure(figsize=(20,10))
		fig50.suptitle('Raw Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig50ax1 = fig50.add_subplot(1,1,1)																										
		data_dic = drawDifferenceLatencyGraph(clog,fig50ax1, clogstats,0,'r',data_dic)

		print (" *************** DRAWING SATELLITE ALL **********************")																																																																																	
		fig60 = plt.figure(figsize=(20,10))
		fig60.suptitle('Satellite Count vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig60ax1 = fig60.add_subplot(1,1,1)																										
		data_dic = drawSatelliteGraph(clog,fig60ax1, clogstats,0,'r',data_dic)

		print (" *************** DRAWING PC CLOCK NETWORK LATENCY ALL **********************")																																																																																	
		fig61 = plt.figure(figsize=(20,10))
		fig61.suptitle('PC Clock Network Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig61ax1 = fig61.add_subplot(1,1,1)																										
		data_dic = draw_PCClock_Network_LatencyGraph(clog,fig61ax1, clogstats,0,'r',data_dic)

		print (" *************** DRAWING PC CLOCK NETWORK LATENCY & LATENCY  ALL **********************")																																																																																	
		fig62 = plt.figure(figsize=(20,10))
		fig62.suptitle('PC Clock Network Latency and Latency vs Sequence from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig62ax1 = fig62.add_subplot(1,1,1)																										
		data_dic = drawCombinedLatency_PCNetworkLatency_Graph(clog,fig62ax1, clogstats,0,'r',data_dic)

		print (" *************** DRAWING PC CLOCK NETWORK LATENCY - LATENCY (DIFFERENCE)  ALL **********************")																																																																																	
		fig63 = plt.figure(figsize=(20,10))
		fig63.suptitle('PC Clock Network Latency - Latency from file: '+file_name+" \n drop rate: {:.2f}".format(drop_rate) + "%")
		fig63ax1 = fig63.add_subplot(1,1,1)																										
		data_dic = draw_PCNetworkLatency_Latency_Diff_Graph(clog,fig63ax1, clogstats,0,'r',data_dic)

		
		plt.close('all')


	if(dohist):

		bins1 = int(args.b)
		print (" *************** DRAWING HISTOGRAM 0 **********************") 
		fig5 = plt.figure(figsize=(20,10))
		fig5.suptitle("Latency Histograms \n "+"file: "+file_name)
		fig5ax1 = fig5.add_subplot(1,1,1)
		drawHistogram(cam0,fig5ax1,cam0stats,0, bins1,'r')
		print (" *************** DRAWING HISTOGRAM 1 **********************") 
		fig6 = plt.figure(figsize=(20,10))
		fig6.suptitle("Latency Histograms \n "+"file: "+file_name)
		fig6ax1 = fig6.add_subplot(1,1,1)
		drawHistogram(cam1,fig6ax1,cam1stats,1, bins1,'g')
		print (" *************** DRAWING HISTOGRAM 2 **********************") 
		fig7 = plt.figure(figsize=(20,10))
		fig7.suptitle("Latency Histograms \n "+"file: "+file_name)
		fig7ax1 = fig7.add_subplot(1,1,1)
		drawHistogram(cam2,fig7ax1,cam2stats,2, bins1,'b')
		print (" *************** DRAWING HISTOGRAM 3 **********************") 
		fig8 = plt.figure(figsize=(20,10))
		fig8.suptitle("Latency Histograms \n "+"file: "+file_name)
		fig8ax1 = fig8.add_subplot(1,1,1)
		drawHistogram(cam3,fig8ax1,cam3stats,3, bins1,'m')
		print (" *************** DRAWING HISTOGRAM 4 **********************") 
		fig9 = plt.figure(figsize=(20,10))
		fig9.suptitle("Latency Histograms \n "+"file: "+file_name)
		fig9ax1 = fig9.add_subplot(1,1,1)
		drawHistogram(cam4,fig9ax1,cam4stats,4, bins1,'c')

		plt.close('all')

		print (" *************** DRAWING PC HISTOGRAM 0 **********************") 
		fig25 = plt.figure(figsize=(20,10))
		fig25.suptitle("PC Latency Histograms \n "+"file: "+file_name)
		fig25ax1 = fig25.add_subplot(1,1,1)
		drawpcHistogram(cam0,fig25ax1,cam0stats,0, bins1,'r')
		print (" *************** DRAWING PC HISTOGRAM 1 **********************") 
		fig26 = plt.figure(figsize=(20,10))
		fig26.suptitle("PC Latency Histograms \n "+"file: "+file_name)
		fig26ax1 = fig26.add_subplot(1,1,1)
		drawpcHistogram(cam1,fig26ax1,cam1stats,1, bins1,'g')
		print (" *************** DRAWING PC HISTOGRAM 2 **********************") 
		fig27 = plt.figure(figsize=(20,10))
		fig27.suptitle("PC Latency Histograms \n "+"file: "+file_name)
		fig27ax1 = fig27.add_subplot(1,1,1)
		drawpcHistogram(cam2,fig27ax1,cam2stats,2, bins1,'b')
		print (" *************** DRAWING PC HISTOGRAM 3 **********************") 
		fig28 = plt.figure(figsize=(20,10))
		fig28.suptitle("PC Latency Histograms \n "+"file: "+file_name)
		fig28ax1 = fig28.add_subplot(1,1,1)
		drawpcHistogram(cam3,fig28ax1,cam3stats,3, bins1,'m')
		print (" *************** DRAWING PC HISTOGRAM 4 **********************") 
		fig29 = plt.figure(figsize=(20,10))
		fig29.suptitle("PC Latency Histograms \n "+"file: "+file_name)
		fig29ax1 = fig29.add_subplot(1,1,1)
		drawpcHistogram(cam4,fig29ax1,cam4stats,4, bins1,'c')

		plt.close('all')

	if (save_fig):
		fig0.savefig(save_dir+file_name+"_latency_Camera0.jpg")
		fig1.savefig(save_dir+file_name+"_latency_Camera1.jpg")
		fig2.savefig(save_dir+file_name+"_latency_Camera2.jpg")
		fig3.savefig(save_dir+file_name+"_latency_Camera3.jpg")
		fig4.savefig(save_dir+file_name+"_latency_Camera4.jpg")

		fig5.savefig(save_dir+file_name+"_hist_Camera0.jpg")
		fig6.savefig(save_dir+file_name+"_hist_Camera1.jpg")
		fig7.savefig(save_dir+file_name+"_hist_Camera2.jpg")
		fig8.savefig(save_dir+file_name+"_hist_Camera3.jpg")
		fig9.savefig(save_dir+file_name+"_hist_Camera4.jpg")

		fig20.savefig(save_dir+file_name+"_pc_latency_Camera0.jpg")
		fig21.savefig(save_dir+file_name+"_pc_latency_Camera1.jpg")
		fig22.savefig(save_dir+file_name+"_pc_latency_Camera2.jpg")
		fig23.savefig(save_dir+file_name+"_pc_latency_Camera3.jpg")
		fig24.savefig(save_dir+file_name+"_pc_latency_Camera4.jpg")

		fig25.savefig(save_dir+file_name+"_pc_hist_Camera0.jpg")
		fig26.savefig(save_dir+file_name+"_pc_hist_Camera1.jpg")
		fig27.savefig(save_dir+file_name+"_pc_hist_Camera2.jpg")
		fig28.savefig(save_dir+file_name+"_pc_hist_Camera3.jpg")
		fig29.savefig(save_dir+file_name+"_pc_hist_Camera4.jpg")

		fig30.savefig(save_dir+file_name+"_com_latency_Camera0.jpg")
		fig31.savefig(save_dir+file_name+"_com_latency_Camera1.jpg")
		fig32.savefig(save_dir+file_name+"_com_latency_Camera2.jpg")
		fig33.savefig(save_dir+file_name+"_com_latency_Camera3.jpg")
		fig34.savefig(save_dir+file_name+"_com_latency_Camera4.jpg")

		fig40.savefig(save_dir+file_name+"_dif_latency_Camera0.jpg")
		fig41.savefig(save_dir+file_name+"_dif_latency_Camera1.jpg")
		fig42.savefig(save_dir+file_name+"_dif_latency_Camera2.jpg")
		fig43.savefig(save_dir+file_name+"_dif_latency_Camera3.jpg")
		fig44.savefig(save_dir+file_name+"_dif_latency_Camera4.jpg")

		fig50.savefig(save_dir+file_name+"_raw_latency_all.jpg")
		fig60.savefig(save_dir+file_name+"_satellite_all.jpg")
		fig61.savefig(save_dir+file_name+"_pc_network_latency_all.jpg")
		fig62.savefig(save_dir+file_name+"_pc_network_latency_with_latency_all.jpg")
		fig63.savefig(save_dir+file_name+"_pclml_all.jpg")



		data_dic["latency_cam0"] = file_name+"_latency_Camera0.jpg"
		data_dic["latency_cam1"] = file_name+"_latency_Camera1.jpg"
		data_dic["latency_cam2"] = file_name+"_latency_Camera2.jpg"
		data_dic["latency_cam3"] = file_name+"_latency_Camera3.jpg"
		data_dic["latency_cam4"] = file_name+"_latency_Camera4.jpg"
		
		data_dic["pc_latency_cam0"] = file_name+"_pc_latency_Camera0.jpg"
		data_dic["pc_latency_cam1"] = file_name+"_pc_latency_Camera1.jpg"
		data_dic["pc_latency_cam2"] = file_name+"_pc_latency_Camera2.jpg"
		data_dic["pc_latency_cam3"] = file_name+"_pc_latency_Camera3.jpg"
		data_dic["pc_latency_cam4"] = file_name+"_pc_latency_Camera4.jpg"

		data_dic["com_latency_cam0"] = file_name+"_com_latency_Camera0.jpg"
		data_dic["com_latency_cam1"] = file_name+"_com_latency_Camera1.jpg"
		data_dic["com_latency_cam2"] = file_name+"_com_latency_Camera2.jpg"
		data_dic["com_latency_cam3"] = file_name+"_com_latency_Camera3.jpg"
		data_dic["com_latency_cam4"] = file_name+"_com_latency_Camera4.jpg"

		data_dic["dif_latency_cam0"] = file_name+"_dif_latency_Camera0.jpg"
		data_dic["dif_latency_cam1"] = file_name+"_dif_latency_Camera1.jpg"
		data_dic["dif_latency_cam2"] = file_name+"_dif_latency_Camera2.jpg"
		data_dic["dif_latency_cam3"] = file_name+"_dif_latency_Camera3.jpg"
		data_dic["dif_latency_cam4"] = file_name+"_dif_latency_Camera4.jpg"

		data_dic["raw_latency_all"] = file_name+"_raw_latency_all.jpg"
		data_dic["satellite_all"] = file_name+"_satellite_all.jpg"
		data_dic["pc_network_latency"] = file_name+"_pc_network_latency_all.jpg"
		data_dic["pc_network_latency_with_latency"] = file_name+"_pc_network_latency_with_latency_all.jpg"
		data_dic["pc_network_latency_minus_latency"] = file_name+"_pclml_all.jpg"


		data_dic["hist_cam0"] = file_name+"_hist_Camera0.jpg"
		data_dic["hist_cam1"] = file_name+"_hist_Camera1.jpg"
		data_dic["hist_cam2"] = file_name+"_hist_Camera2.jpg"
		data_dic["hist_cam3"] = file_name+"_hist_Camera3.jpg"
		data_dic["hist_cam4"] = file_name+"_hist_Camera4.jpg"

		data_dic["pc_hist_cam0"] = file_name+"_pc_hist_Camera0.jpg"
		data_dic["pc_hist_cam1"] = file_name+"_pc_hist_Camera1.jpg"
		data_dic["pc_hist_cam2"] = file_name+"_pc_hist_Camera2.jpg"
		data_dic["pc_hist_cam3"] = file_name+"_pc_hist_Camera3.jpg"
		data_dic["pc_hist_cam4"] = file_name+"_pc_hist_Camera4.jpg"

	return data_dic

# add a base map to existing map
def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
    xmin, xmax, ymin, ymax = ax.axis()
    #print (xmin, xmax, ymin, ymax)
    basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    # restore original x/y limits
    ax.axis((xmin, xmax, ymin, ymax))

# convert degree minute seconds format to decimal
def dms2dd(s):
    # example: s = """051'56.29"S"""
    s = s.encode('utf-8')
    dat = s.split(" ")
    #print(s)
    degrees = float(dat[0][0:len(dat[0])-2])
    minutes = float(dat[1][0:1])
    seconds = float(dat[2][0:4])
    #degrees, minutes, seconds, direction = re.split('[\'"]+', s)
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    #if direction in ('S','W'):
    #    dd*= -1
    return dd

# get color map from data list
def getColorMap(data):
	cmap = plt.get_cmap(name) # Get desired colormap - you can change this!
	max_height = np.max(data)   # get range of colorbars so we can normalize
	min_height = np.min(data)
	# scale each z to [0,1], and get their rgb values
	rgba = [cmap(((k-min_height)/max_height) ) for k in data] 
	#rgba = [cmap(1.0 - ((k-min_height)/max_height) ) for k in data] 
	return rgba

# parse and get antenna information from json file:
def getAntennaData(frames):
	lat = list()
	lon = list()
	lic = list()
	com = list()
	for frame in frames:
		# look only for antennas
		if 'LON' not in frame:
			continue
		lat.append(frame['LAT'])
		lon.append(frame['LON'])
		lic.append(frame['RDS_PMS_NO'])
		com.append(frame['UNGB'])
	data = {'lat':lat,'lon':lon,'lic':lic,'com': com}
	antennas = pd.DataFrame(data)
	return antennas

# convert data to mercator format
def geographic_to_web_mercator(x_lon, y_lat):     
	if abs(x_lon) <= 180 and abs(y_lat) < 90:          
		num = x_lon * 0.017453292519943295         
		x = 6378137.0 * num         
		a = y_lat * 0.017453292519943295          
		x_mercator = x         
		y_mercator = 3189068.5 * math.log((1.0 + math.sin(a)) / (1.0 - math.sin(a)))         
		return x_mercator, y_mercator   
	else:         
		print('Invalid coordinate values for conversion')        

def lon_to_mercator(xlon):
	if abs(xlon)<=180.0:
		num = xlon * 0.017453292519943295
		x = 6378137.0 * num
		return x

def lat_to_mercator(ylat):
	if abs(ylat) < 90:
		a = ylat * 0.017453292519943295
		y = 3189068.5 * math.log((1.0 + math.sin(a)) / (1.0 - math.sin(a)))
		return y

# set size of an axis
def set_size(w,h, ax=None):
    """ w, h: width, height in inches """
    if not ax: ax=plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    ax.figure.set_size_inches(figw, figh)

# read gpx file and create a dataframe containing all data
def getGPXDataFrame(gpxfile, file_type):
	#load gpx file
	if (file_type == "1" or file_type == "2"):
		gpx_data = gpxpy.parse(gpxfile)

	# create a fake gpx file just for compatibility	
	if (file_type == "3"):
		# this DataFrame already has latitude and longitude
		# only need to add velocity
		gpxfile['ele'] = 0.0


		#gpxfile = gpxfile.groub
		
		# Creat a GPX File
		gpx_data = gpxpy.gpx.GPX()
		# Create first track in our GPX:
		gpx_track = gpxpy.gpx.GPXTrack()
		gpx_data.tracks.append(gpx_track)

		# Create first segment in our GPX track:
		gpx_segment = gpxpy.gpx.GPXTrackSegment()
		gpx_track.segments.append(gpx_segment)

		for (lat,lon,time, ele) in zip(gpxfile['lat'],gpxfile['lon'],gpxfile['time'],gpxfile['ele']):
			#print (lat,lon,time,ele)
			gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude =float(lat), longitude =float(lon), elevation=ele, time=time))


	#print(gpx_data.tracks[0].segments[0].points[0].latitude)
	#print(type(gpx_data.tracks[0].segments[0].points[0].latitude))
	#print(gpx.dtypes)
		
	lat = list()
	lon = list()
	ele = list()
	time = list()
	speed = list()
	for (i,track) in enumerate(gpx_data.tracks):
		#print ("For track "+str(i)+" there are "+str(len(track.segments))+" segments")
		for (j,segment) in enumerate(track.segments):
			#print("For segment "+str(j)+" there are "+str(len(segment.points))+" points")
			for (k,point) in enumerate(segment.points):
				lat.append(point.latitude)
				lon.append(point.longitude)
				ele.append(point.elevation)
				if(file_type == "1" or file_type == "2"):
					time.append(point.time+timedelta(hours = 9))
				if(file_type == "3"):
					time.append(point.time)
				# estimate traveling speed
				if(k > 0):
					speed.append(point.speed_between(segment.points[k - 1]))
				else:
					# append 0 just to create place holder and all datalists are the same
					# length at the moment of creating the dataframe
					speed.append(0)
				#print('Point at ({0},{1}) -> ({2},{3})'.format(point.latitude, point.longitude, point.elevation, point.time))
				#print (type(point.latitude), type(point.longitude), type(point.elevation), type(point.time))
	speed[0] = speed[1]
	columns = {'lat':lat,'lon':lon,'ele':ele,'time':time,'speed':speed}
	points = pd.DataFrame(columns)
	# convert to km/h
	points['speed'] = points['speed']*3.6

	#print(points.head(10))


	return points

# align latency_data and gps data, and create latency column in the gps data file
# based on the option passed:
# option 0: latency column is min latency
# option 1: latency column is average latency
# option 3: latency column is max latency
def alignGPSandLatency(latency_data, gps_data,option):

	# set the index of both dataframes to be time
	latency_data = latency_data.set_index('time')
	gps_data = gps_data.set_index('time').sort_index()



	#print("Latency data:\n {}".format(latency_data.head(10)))
	#print("GPS Data: \n {}".format(gps_data.head(10)))

	# group to calculate min, avg or max per second ( remeber every second receive 30 frames
	# and the gps data is per second, so it is necessary that each step in time is 1 second)
	if(option == 0):
		latency_data = latency_data.groupby(latency_data.index).min().sort_index()
	if(option == 1):
		latency_data = latency_data.groupby(latency_data.index).mean().sort_index()
	if(option == 2):
		latency_data = latency_data.groupby(latency_data.index).max().sort_index()


	# get indices to later get start and end index for each dataframe
	latency_index = latency_data.index.values
	gps_index = gps_data.index.values

	# Create an artificial date range to add to the latency data all the seconds
	# that were not recorded due to problems like freezing, connection fail, etc
	#a = pd.date_range(latency_index[0], latency_index[-1], freq='s')
	#tst = pd.Series(index = a)
	#print("Date range len:"+str(len(tst)))

	# Interpolate latency data after time resizing
	#latency_data = latency_data.reindex(a)
	#latency_data['latency'] = latency_data['latency'].interpolate(method = 'linear')
	#print("latency 0 index length (post interpolate): "+str(len(avgs['latency'])))


	start_time = 0
	end_time = 0
	# select data merging start time
	if( gps_index[0] > latency_index[0]):
		# if gps datapoints are delayed, then merging
		#should start with the first gps datapoint
		start_time = gps_index[0]
	else:
		# if not, merging starts with latency data
		start_time = latency_index[0]
	# select data merging finish time
	if ( gps_index[len(gps_index)-1] > latency_index[len(latency_index)-1] ):
		# if gps data finishes later than latency data
		# then maximum merging time should be that from lantecy data
		end_time = latency_index[len(latency_index)-1]
	else:
		# if not then data merging should finish on last gps datapoint 
		end_time = gps_index[len(gps_index)-1] 

	# crop latency data between start and end times
	latency_data = latency_data.loc[start_time:end_time,:]
	# reindex gps data to fit the timestamps in latency data
	gps_with_latency = gps_data.reindex(latency_data.index.tolist())
	#print("tdi after crop: "+str(len(track_datapoints_crop.index.tolist())))

	#
	if( pd.isna(gps_with_latency.iloc[0]['lat']) ):
		#print("El primera es NaN")
		gps_with_latency.at[start_time,'lat']=gps_data.at[gps_index[0],'lat']
		gps_with_latency.at[start_time,'lon']=gps_data.at[gps_index[0],'lon']
		gps_with_latency.at[start_time,'ele']=gps_data.at[gps_index[0],'ele']
		gps_with_latency.at[start_time,'speed']=gps_data.at[gps_index[0],'speed']


	if( pd.isna(gps_with_latency.iloc[-1]['lat']) ):
		#print("El ultimo es NaN")
		gps_with_latency.at[end_time,'lat']=gps_data.at[gps_index[len(gps_index)-1],'lat']
		gps_with_latency.at[end_time,'lon']=gps_data.at[gps_index[len(gps_index)-1],'lon']
		gps_with_latency.at[end_time,'ele']=gps_data.at[gps_index[len(gps_index)-1],'ele']
		gps_with_latency.at[end_time,'speed']=gps_data.at[gps_index[len(gps_index)-1],'speed']



	# Interpolate missing lat, lon, elevation data
	gps_with_latency['lat'] = gps_with_latency['lat'].interpolate(method = 'linear')
	gps_with_latency['lon'] = gps_with_latency['lon'].interpolate(method = 'linear')
	gps_with_latency['ele'] = gps_with_latency['ele'].interpolate(method = 'linear')
	gps_with_latency['speed'] = gps_with_latency['speed'].interpolate(method = 'linear')

	# Save the apropriate 
	if(option == 0):
		gps_with_latency['min_latency'] = latency_data['latency']
		gps_with_latency['min_pc_latency'] = latency_data['pc_latency']

	if(option == 1):
		gps_with_latency['avg_latency'] = latency_data['latency']
		gps_with_latency['avg_pc_latency'] = latency_data['pc_latency']
	if(option == 2):
		gps_with_latency['max_latency'] = latency_data['latency']
		gps_with_latency['max_pc_latency'] = latency_data['pc_latency']


	# add the rest of the columns
	gps_with_latency['sat'] = latency_data['sat']
	gps_with_latency['seq'] = latency_data['seq']
	gps_with_latency['dif_latency'] = latency_data['dif_latency']
	gps_with_latency['pc_network_latency'] = latency_data['pc_network_latency']

	return gps_with_latency

# get the number of antennas inside a circle of radius 'r' in meter, centered on 'p' in lat,lon
# 'a' is a dataframe containing the position of all antennas in lat,lon
# the distance is calculated using a simple approximation: the eart is flat  between the 2 points
def getSurroundingAntennas(p, r, a):
	count = 0

	# reduce search space to only around the current point p
	search_data = a[ a["lon"] <= (p[1]+margin_epsg4326*1.0) ]
	search_data = search_data[ search_data["lon"] >= (p[1]-margin_epsg4326*1.0) ]
	search_data = search_data[ search_data["lat"] <= (p[0]+margin_epsg4326*1.0) ]
	search_data = search_data[ search_data["lat"] >= (p[0]-margin_epsg4326*1.0) ]

	for (lat,lon)in zip(search_data['lat'],search_data['lon']):
		c = 2*np.pi/360.0  # degree to radian
		arc = np.sqrt( (lat-p[0])**2  + (lon-p[1])**2 )*c  #convert to radian
		d = R*arc    # distance = radius*arc
		if(d<=r):
			count = count + 1
		#print d
	return count 

# get the number of buildings inside a circle of radius 'r' in meter, centered on 'p' in lat,lon
# 'a' is a dataframe containing the position of all buildings in lat,lon
# the distance is calculated using a simple approximation: the eart is flat  between the 2 points
def getSurroundingBuildings(p, r, a):
	count = 0

	# reduce search space to only around the current point p
	search_data = a[ a["lon"] <= (p[1]+margin_epsg4326*1.0) ]
	search_data = search_data[ search_data["lon"] >= (p[1]-margin_epsg4326*1.0) ]
	search_data = search_data[ search_data["lat"] <= (p[0]+margin_epsg4326*1.0) ]
	search_data = search_data[ search_data["lat"] >= (p[0]-margin_epsg4326*1.0) ]

	for (lat,lon)in zip(search_data['lat'],search_data['lon']):

		c = 2*np.pi/360.0  # degree to radian
		arc = np.sqrt( (lat-p[0])**2  + (lon-p[1])**2 )*c  #convert to radian
		d = R*arc    # distance = radius*arc
		if(d<=r):
			count = count + 1
		#print d
	return count


def getSurroundingBuilding_AvgHeight(p, r, a):
	count = 0
	cum_height = 0
	avg_height = 0

	# reduce search space to only around the current point p
	search_data = a[ a["lon"] <= (p[1]+margin_epsg4326*1.0) ]
	search_data = search_data[ search_data["lon"] >= (p[1]-margin_epsg4326*1.0) ]
	search_data = search_data[ search_data["lat"] <= (p[0]+margin_epsg4326*1.0) ]
	search_data = search_data[ search_data["lat"] >= (p[0]-margin_epsg4326*1.0) ]

	for (lat,lon,h) in zip(search_data['lat'],search_data['lon'], search_data['height']):
		c = 2*np.pi/360.0  # degree to radian
		arc = np.sqrt( (lat-p[0])**2  + (lon-p[1])**2 )*c  #convert to radian
		d = R*arc    # distance = radius*arc
		if(d<=r):
			count = count + 1
			cum_height = cum_height + h
		#print d

	# careful with zero division
	# if there are no buildings around (count = 0), then 
	# the average building height is 0, of course
	if(count != 0):
		avg_height = cum_height/(count*1.0)
	else:
		avg_height = 0

	return avg_height


# calculate covariance
def cov():
	return 0


opt = 1   #option 2 = get max latency, 0 min lat, 1 avg lat

if __name__ == '__main__':
	#print("Camera 1 log:\n {}".format( cam1.head()))


	# earth radius, meters
	R =  6371000



	# dictionary to contain all information for creating the md file
	data_dic = {}

	# get arguments to the program
	args = createCommandLineParser()

	# get file name
	file_path = args.f
	dirs = file_path.split("/")

	file_name = dirs[-1].split(".")[0]
	print("File name:" + file_name)


	# save all files in the same directory as the log files
	save_dir = ""
	for element in dirs[0:len(dirs)-1]:
		save_dir = save_dir + element+"/"
	print("Save dir:"+save_dir)

	# use this cmap
	name = args.q


	# import log file
	log_raw = pd.read_csv(file_path, sep = ",", header = None)
	#import file depending on format version
	if args.x == "2":  # new format
		log_raw.columns = ["id","seq","send_time","recv_time", "size"]    #new format
	if args.x == "1":   # old format
		log_raw.columns = ["id","seq","size", "latency","time"]				# old format
	if args.x == "3":   # newest format 
		log_raw.columns = ["id","seq","send_time","recv_time","send_UTC", "recv_UTC","send_raw_UTC","recv_raw_UTC","local_send_time","size", "lon", "lat","sat"]				# newest format 20181214
		

	print ("---------- IMPORT RAW LOG DATA --------------")
	#print log_raw.head(10)
	#print ("Raw Log shape: "+str(log_raw.shape))
	#print log_raw.dtypes

	print("\n---------- CLEAN AND PARSE DATA--------------")
	clog = cleanData(log_raw)
	if args.x == "2":
		clog = convertData(clog, [int,int,int,int,int])                    # new format
	if args.x == "1":
		clog = convertData(clog, [int,int,int,int,datetime])				#old format
	if (args.x == "3"):
		clog = convertData(clog, [int,int,int,int,int,int,int,int,int,int,float,float,int])     #newest format

		#print("LATITUDE IMPORTADA")
		#print(clog['lat'].head())

		# copy necessary data to make gps file later
		gps_data_s = pd.DataFrame()
		gps_data_s['lon'] = clog['lon']
		gps_data_s['lat'] = clog['lat']
		#gps_data['send_UTC'] = log_raw['send_UTC']

		#  drop lon, lat columns that will be imported afterwards
		log_raw = log_raw.drop(columns=['lon','lat'])

	#print clog.head()

	# Calculate Latency
	if 'latency' not in clog.columns:
		if args.x == "2":
			clog['latency'] = clog['recv_time'] - clog["send_time"]
		if args.x == "3":
			clog['latency'] = clog['recv_UTC'] - clog["send_UTC"]





	# c = offset UTC (+0900) in milliseconds
	c = 32400000
	if 'time' not in clog.columns:
		if args.x == "2":
			clog["time"] = map(lambda x: pd.Timestamp(x+c,unit="ms").ceil(freq='s'), clog['send_time'])
		if args.x == "3":
			clog["time"] = map(lambda x: pd.Timestamp(x+c,unit="ms").ceil(freq='s'), clog['send_UTC'])
			gps_data_s['time'] = clog['time'].copy()

			# following will group data by index. This is because for a new data format
			# there can be multiple gps locations for the same timestamp, which leads to
			# repeated elements in the index. So we take the location to be the average
			# of the gps locations for each timestamp
			gps_data_s = gps_data_s.groupby('time').mean().sort_index()
			gps_data_s = gps_data_s.reset_index()
			#print(gps_data_s)


	# ------------------------------- CAREFUL
	#seqthreshold = 100000
	#clog = clog[ clog['latency'] < seqthreshold] 

	# Calculate offset1
	#print(clog.at[0,'send_UTC'])
	#print(clog.at[0,'send_time'])
	#print(clog.at[0,'recv_UTC'])
	#print(clog.at[0,'recv_time'])
	offset0 = clog.at[0,'send_UTC'] - clog.at[0,'send_time']
	offset1 = clog.at[0,'recv_UTC'] - clog.at[0,'recv_time']
	#print('Offset 0 {}'.format(offset0))
	#print('Offset 1 {}'.format(offset1))
	clog['pc_latency'] = map(lambda x,y: x-y-offset0+offset1, clog['recv_time'], clog['send_time'])
	clog['raw_UTC_latency'] = clog['send_raw_UTC']- clog['recv_raw_UTC']
	clog['dif_latency'] = clog['pc_latency'] - clog['latency']
	clog['pc_network_latency'] = clog['recv_UTC'] - clog['send_UTC'] + clog['send_time'] - clog["local_send_time"]
	print(clog.head())
	#print("Clean log:\n {}".format(clog.head(10)))
	#print(clog.dtypes)
	#print("GPS Data log:\n {}".format(gps_data_s.head(10)))


	#print(clog.head())


	print("\n---------- GET CAMARA 0 DATA --------------")
	cam0 = clog[ clog['id'] == 0 ]
	#print("Camera 0 log:\n {}".format(cam0.head()))
	#correct sequence number if it was wrong, WARNING this modifies original data and creates an
	# artifical sequence number
	init = cam0.at[cam0.index.values[0],'seq']
	cam0['seq'] = np.arange(0,len(cam0['seq']),1)+init
	cam0stats = cam0.describe()

	print("\n---------- GET CAMARA 1 DATA --------------")
	cam1 = clog[ clog['id'] == 1 ]
	#correct sequence number if it was wrong, WARNING this modifies original data and creates an
	# artifical sequence number that is as close as possible to the original
	init = cam1.at[cam1.index.values[0],'seq']
	cam1['seq'] = np.arange(0,len(cam1['seq']),1)+init
	cam1stats = cam1.describe()

	print("\n---------- GET CAMARA 2 DATA --------------")
	cam2 = clog[ clog['id'] == 2 ]
	#correct sequence number if it was wrong, WARNING this modifies original data and creates an
	# artifical sequence number that is as close as possible to the original
	init = cam2.at[cam2.index.values[0],'seq']
	cam2['seq'] = np.arange(0,len(cam2['seq']),1)+init
	#print ("Camera 2 log:\n {}".format(cam2.head()))
	cam2stats = cam2.describe()

	print("\n---------- GET CAMARA 3 DATA --------------")
	cam3 = clog[ clog['id'] == 3 ]
	#correct sequence number if it was wrong, WARNING this modifies original data and creates an
	# artifical sequence number that is as close as possible to the original
	init = cam3.at[cam3.index.values[0],'seq']
	cam3['seq'] = np.arange(0,len(cam3['seq']),1)+init
	#print ("Camera 3 log:\n {}".format(cam3.head()))
	cam3stats = cam3.describe()

	print("\n---------- GET CAMARA 4 DATA --------------")
	cam4 = clog[ clog['id'] == 4 ]
	#correct sequence number if it was wrong, WARNING this modifies original data and creates an
	# artifical sequence number that is as close as possible to the original
	init = cam4.at[cam4.index.values[0],'seq']
	cam4['seq'] = np.arange(0,len(cam4['seq']),1)+init
	#print ("Camera 3 log:\n {}".format(cam3.head()))
	cam4stats = cam4.describe()



	init = clog.at[clog.index.values[0],'seq']
	clog['seq'] = np.arange(0,len(clog['seq']),1)+init
	clogstats = clog.describe()

	# Calculate drop rate
	drop_rate = getDropRate(log_raw)

	# Graph and save images
	save_fig = 1 	#always set to 1 so report generatino works
	doplot = 1   #always set to 1 so report generatino works
	dohist= 1    # always set to 1 so report generation works
	data_dic = drawGraphs(data_dic)

	#plt.show()

	plt.close('all')


	# import gpx file of the lap done
	print("\n---------- IMPORT GPX FILE --------------")

	# Depending on file format, the gps data will be contained in another file
	# or in the same file
	if(args.x == "1" or args.x=="2"):
		gpx_file = open(args.g, 'r')
		track_datapoints = getGPXDataFrame(gpx_file,args.x)
	if(args.x == "3"):
		track_datapoints = getGPXDataFrame(gps_data_s,args.x)
	#print (track_datapoints.head())


	# import antenna information file
	print("\n---------- IMPORT ANTENNA LOCATION FILE --------------")
	#antenna = pd.read_excel('maps/antennas_SKKU_2018111500.xlsx',header = 0)
	#antenna = convertData(antenna, ["ignore","ignore",str,str,"ignore",str,"dms","dms","ignore","ignore",str,"ignore","ignore","ignore","ignore"])
	with open('maps/antenna_loc2/radius_8km.txt', encoding='cp949') as fh:
	    data = json.load(fh)
	antenna = getAntennaData(data)
	antenna = antenna[ antenna['lat'] != 0.0 ]
	#prov = antenna.groupby('com').mean()
	#print("Antennas before selecting KT4G : "+str(antenna.shape))
	antenna = antenna[ antenna['com'] == 'KT4GOUT']
	#print("Antennas after selecting KT4G : "+str(antenna.shape))

	print("\n---------- ALIGN DATA AND MERGE LATENCY AND GPS --------------")
	
	gps_lat_all = alignGPSandLatency(clog, track_datapoints, opt)
	gps_lat_cam0 = alignGPSandLatency(cam0, track_datapoints, opt)
	gps_lat_cam1 = alignGPSandLatency(cam1, track_datapoints, opt)
	gps_lat_cam2 = alignGPSandLatency(cam2, track_datapoints, opt)
	gps_lat_cam3 = alignGPSandLatency(cam3, track_datapoints, opt)
	gps_lat_cam4 = alignGPSandLatency(cam4, track_datapoints, opt)




	#print("GPS Latency All Cameras log:\n {}".format(gps_lat_all.head(10)))
	#print("GPS Latency  Camera0 log:\n {}".format(gps_lat_cam0.head(10)))
	#print("GPS Latency  Camera1 log:\n {}".format(gps_lat_cam1.head(10)))
	#print("GPS Latency  Camera2 log:\n {}".format(gps_lat_cam2.head(10)))
	#print("GPS Latency  Camera3 log:\n {}".format(gps_lat_cam3.head(10)))
	#print("GPS Latency  Camera4 log:\n {}".format(gps_lat_cam4.head(10)))


	if(opt == 0):
		lat_col = 'min_latency'
		pc_lat_col = 'min_pc_latency'
	if(opt == 1):
		lat_col = 'avg_latency'
		pc_lat_col = 'avg_pc_latency'
	if(opt == 2):
		lat_col = 'max_latency'
		pc_lat_col = 'max_pc_latency'

	# define graph parameters
	color_map=plt.get_cmap(name)
	s1 = 40         # track marker size
	s2 = 6.0        # antenna marker size
	alpha = 0.5     # transparency


	if(False):
		#colores = getColorMap(cam0.loc[0:len(track_datapoints['ele']),'latency'])

		print("\n---------- MAKE ROUTE MAP -------------- ")
		indexs = gps_lat_all.index.values
		print(indexs[0])
		start_point = gps_lat_all.loc[indexs[0]]
		print(start_point)
		finish_point = gps_lat_all.loc[indexs[-1]]
		track_fig = plt.figure()
		track1 = track_fig.add_subplot(1,1,1)
		# draw Cam0 because it has less points than the whole data
		track1.scatter(gps_lat_cam0['lon'],gps_lat_cam0['lat'],color='b', s = s1, label = "Route")
		track1.scatter(start_point['lon'],start_point['lat'], color = 'g', s = s1*10, marker = "*", label = "Start")
		track1.scatter(finish_point['lon'],finish_point['lat'], color = 'r', s = s1*10, marker = '^', label = "Finish")
		track1.legend(loc='upper left', shadow=True, fontsize='x-large')

		data_dic["track_image_path"]="web_track_image.png"
		mplleaflet.show()
		#plt.show()


	#//////////////////////////////////////////
	#
	#		IMPORT AND DRAW GIS DATA
	#
	#///////////////////////////////////////////




	# need this file for other calculations ... cannot be inside if()
	buildings = gpd.read_file("maps/buildings/Buildings_University2.geojson")
	# calculate display region
	margin = 500.0
	max_lat = max(track_datapoints['lat'])
	min_lat = min(track_datapoints['lat'])
	max_lon = max(track_datapoints['lon'])
	min_lon = min(track_datapoints['lon'])
	max_x = lon_to_mercator(max_lon)+margin
	min_x = lon_to_mercator(min_lon)-margin 
	max_y = lat_to_mercator(max_lat)+margin
	min_y = lat_to_mercator(min_lat)-margin



	if(True):
		print("\n---------- IMPORT GEOJSON DATA --------------")
		# import geojson file
		#admin = gpd.read_file('maps/seoul_south-korea.imposm-geojson/seoul_south-korea_admin.geojson')
		
		#buildings = buildings[ buildings['HEIGHT'] > 0.0 ]
		#places = gpd.read_file('maps/seoul_south-korea.imposm-geojson/seoul_south-korea_places.geojson')
		#roads = gpd.read_file('maps/seoul_south-korea.imposm-geojson/seoul_south-korea_roads.geojson')
		#roads_gen0 = gpd.read_file('maps/seoul_south-korea.imposm-geojson/seoul_south-korea_roads_gen0.geojson')
		#roads_gen1 = gpd.read_file('maps/seoul_south-korea.imposm-geojson/seoul_south-korea_roads_gen1.geojson')
		#transport_areas = gpd.read_file('maps/seoul_south-korea.imposm-geojson/seoul_south-korea_transport_areas.geojson')
		waterareas = gpd.read_file('maps/seoul_south-korea.imposm-geojson/seoul_south-korea_waterareas.geojson')

		# draw all layers

		map5 = plt.figure(figsize=(20,10))
		map5.suptitle("Latency Map All cameras")
		map0 = plt.figure(figsize=(20,10))
		map0.suptitle("Latency Map Camera 0")
		map1 = plt.figure(figsize=(20,10))
		map1.suptitle("Latency Map Camera 1")
		map2 = plt.figure(figsize=(20,10))
		map2.suptitle("Latency Map Camera 2")
		map3 = plt.figure(figsize=(20,10))
		map3.suptitle("Latency Map Camera 3")
		map4 = plt.figure(figsize=(20,10))
		map4.suptitle("Latency Map Camera 4")

		#rect = 0.05,0.05,0.8,0.8
		map5ax1 = map5.add_subplot(1,1,1) #add_axes(rect)
		map5ax1.set_aspect('equal')
		map0ax1 = map0.add_subplot(1,1,1)
		map0ax1.set_aspect('equal')
		map1ax1 = map1.add_subplot(1,1,1)
		map1ax1.set_aspect('equal')
		map2ax1 = map2.add_subplot(1,1,1)
		map2ax1.set_aspect('equal')
		map3ax1 = map3.add_subplot(1,1,1)
		map3ax1.set_aspect('equal')
		map4ax1 = map4.add_subplot(1,1,1)
		map4ax1.set_aspect('equal')

		#admin.plot(ax=map1ax1, color='white', edgecolor='black',alpha = 0.5)
		#buildings.plot(ax=map1ax1, color = 'green', alpha = 0.5)
		#places.plot(ax=map1ax1, color = 'black', alpha = 0.5)
		#roads.plot(ax = map1ax1, color = 'green', alpha = 0.0)
		#roads_gen0.plot(ax = map1ax1, color = 'magenta', alpha = 0.0)
		#roads_gen1.plot(ax = map1ax1, color = 'cyan', alpha = 0.0)
		#transport_areas.plot(ax = map1ax1, color = 'red', alpha = 0.5)
		#waterareas.plot(ax = map1ax1, color = 'blue', alpha = 0.5)

		#//////////////////////////////////////////
		#
		#		CONVERT DATA TO MERCATOR FOR BASEMAP DISPLAY
		#
		#///////////////////////////////////////////

		print("\n---------- CONVERT DATA TO MERCATOR --------------")

		#admin = admin.to_crs(epsg=3857)
		buildings = buildings.to_crs(epsg=3857)
		waterareas = waterareas.to_crs(epsg=3857)





		gps_lat_all['x_merc'] = map(lambda x: lon_to_mercator(x),gps_lat_all['lon'])
		gps_lat_all['y_merc'] = map(lambda x: lat_to_mercator(x),gps_lat_all['lat'])

		gps_lat_cam0['x_merc'] = map(lambda x: lon_to_mercator(x),gps_lat_cam0['lon'])
		gps_lat_cam0['y_merc'] = map(lambda x: lat_to_mercator(x),gps_lat_cam0['lat'])

		gps_lat_cam1['x_merc'] = map(lambda x: lon_to_mercator(x),gps_lat_cam1['lon'])
		gps_lat_cam1['y_merc'] = map(lambda x: lat_to_mercator(x),gps_lat_cam1['lat'])

		gps_lat_cam2['x_merc'] = map(lambda x: lon_to_mercator(x),gps_lat_cam2['lon'])
		gps_lat_cam2['y_merc'] = map(lambda x: lat_to_mercator(x),gps_lat_cam2['lat'])

		gps_lat_cam3['x_merc'] = map(lambda x: lon_to_mercator(x),gps_lat_cam3['lon'])
		gps_lat_cam3['y_merc'] = map(lambda x: lat_to_mercator(x),gps_lat_cam3['lat'])

		gps_lat_cam4['x_merc'] = map(lambda x: lon_to_mercator(x),gps_lat_cam4['lon'])
		gps_lat_cam4['y_merc'] = map(lambda x: lat_to_mercator(x),gps_lat_cam4['lat'])

		antenna['x_merc'] = map(lambda x: lon_to_mercator(x),antenna['lon'])
		antenna['y_merc'] = map(lambda x: lat_to_mercator(x),antenna['lat'])



		# Display region of interest
		#admin = admin.cx[min_lon:max_lon,min_lat: max_lat ]
		buildings = buildings.cx[min_x:max_x,min_y: max_y ]
		waterareas = waterareas.cx[min_x:max_x,min_y: max_y ]


		#colores = getColorMap(cam0.loc[0:len(track_datapoints['ele']),'latency'])

		print("\n---------- MAKE ROUTE MAP -------------- ")
		indexs = gps_lat_all.index.values
		#print(indexs[0])
		start_point = gps_lat_all.loc[indexs[0]]
		#print(start_point)
		finish_point = gps_lat_all.loc[indexs[-1]]

		seq_every = 100
		seq_labels =  gps_lat_cam0.iloc[::seq_every, :] 
		#print(gps_lat_cam0.head(10))

		#print(seq_labels.head(10))

		track_fig = plt.figure(figsize=(20,10))
		track1 = track_fig.add_subplot(1,1,1)
		# draw Cam0 because it has less points than the whole data
		track1.scatter(gps_lat_cam0['x_merc'],gps_lat_cam0['y_merc'],color='c', s = s1, label = "Route")
		track1.scatter(start_point['x_merc'],start_point['y_merc'], color = 'g', s = s1*10, marker = "*", label = "Start")
		track1.scatter(finish_point['x_merc'],finish_point['y_merc'], color = 'r', s = s1*10, marker = '^', label = "Finish")
		#for i, txt in enumerate(n):
	   	# 	ax.annotate(txt, (z[i], y[i]))

	   	# now annotate sequece
	   	map(lambda seq,x,y: track1.annotate("{:.0f}".format(seq),(x,y), fontsize= 'medium', fontweight = 'bold', rotation = 30),seq_labels['seq'],seq_labels['x_merc'],seq_labels['y_merc'])

		track1.legend(loc='upper left', shadow=True, fontsize='x-large')
		#admin.plot(ax=map5ax1, color='white', edgecolor='black',alpha = 0.2)
		buildings.plot(ax=track1, color = 'green', alpha = 0.5)
		waterareas.plot(ax = track1, color = 'blue', alpha = 0.5)

		track_fig.savefig(save_dir+file_name+"_annotated_track_image.jpg")
		data_dic["track_image_path"]=file_name+"_annotated_track_image.jpg"
		#mplleaflet.show()
		#plt.show()




		rect = 0.74,0.1,0.025,0.8


		if (True):
			#//////////////////////////////////////////
			#
			#		DRAW  GIS DATA WITH TRACK WITH LATENCY
			#
			#///////////////////////////////////////////


			# Plot GIS layers
			#admin.plot(ax=map5ax1, color='white', edgecolor='black',alpha = 0.2)
			buildings.plot(ax=map5ax1, color = 'green', alpha = 0.5)
			waterareas.plot(ax = map5ax1, color = 'blue', alpha = 0.5)
			# Plot Latency Map
			gps_lat_all = gps_lat_all.sort_values(by=[lat_col])
			colores = getColorMap(gps_lat_all[lat_col])
			map5ax1.scatter(gps_lat_all['x_merc'], gps_lat_all['y_merc'], color = colores, s = s1, alpha = alpha)
			map5ax1.scatter(antenna['x_merc'], antenna['y_merc'], color = 'blue', marker='^', s = s2)
			map5ax1.set_xlim(min_x,max_x)
			map5ax1.set_ylim(min_y,max_y)
			#Plot color bar
			map5ax2 = map5.add_axes(rect)
			latency_max = max(gps_lat_all[lat_col])
			latency_min = min(gps_lat_all[lat_col])
			ticks = np.linspace(latency_min, latency_max, 10)
			norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
			cb1 = mpl.colorbar.ColorbarBase(map5ax2, cmap=color_map, norm=norm, orientation='vertical')
			cb1.set_label('{ms}')
			cb1.set_ticks(ticks)

			# Plot GIS layers
			#admin.plot(ax=map0ax1, color='white', edgecolor='black',alpha = 0.2)
			buildings.plot(ax=map0ax1, color = 'green', alpha = 0.5)
			waterareas.plot(ax = map0ax1, color = 'blue', alpha = 0.5)
			# Plot Latency Map
			gps_lat_cam0 = gps_lat_cam0.sort_values(by=[lat_col])
			colores = getColorMap(gps_lat_cam0[lat_col])
			map0ax1.scatter(gps_lat_cam0['x_merc'], gps_lat_cam0['y_merc'], color = colores, s = s1, alpha = alpha)
			map0ax1.scatter(antenna['x_merc'], antenna['y_merc'], color = 'blue', marker='^', s = s2)
			map0ax1.set_xlim(min_x,max_x)
			map0ax1.set_ylim(min_y,max_y)
			#Plot color bar
			map0ax2 = map0.add_axes(rect)
			latency_max = max(gps_lat_cam0[lat_col])
			latency_min = min(gps_lat_cam0[lat_col])
			ticks = np.linspace(latency_min, latency_max, 10)
			norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
			cb2 = mpl.colorbar.ColorbarBase(map0ax2, cmap=color_map, norm=norm, orientation='vertical')
			cb2.set_label('{ms}')
			cb2.set_ticks(ticks)

			# Plot GIS layers
			#admin.plot(ax=map1ax1, color='white', edgecolor='black',alpha = 0.2)
			buildings.plot(ax=map1ax1, color = 'green', alpha = 0.5)
			waterareas.plot(ax = map1ax1, color = 'blue', alpha = 0.5)
			# Plot Latency Map
			gps_lat_cam1 = gps_lat_cam1.sort_values(by=[lat_col])
			colores = getColorMap(gps_lat_cam1[lat_col])
			map1ax1.scatter(gps_lat_cam1['x_merc'], gps_lat_cam1['y_merc'], color = colores, s = s1, alpha = alpha)
			map1ax1.scatter(antenna['x_merc'], antenna['y_merc'], color = 'blue', marker='^', s = s2)
			map1ax1.set_xlim(min_x,max_x)
			map1ax1.set_ylim(min_y,max_y)
			#Plot color bar
			map1ax2 = map1.add_axes(rect)
			latency_max = max(gps_lat_cam1[lat_col])
			latency_min = min(gps_lat_cam1[lat_col])
			ticks = np.linspace(latency_min, latency_max, 10)
			norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
			cb3 = mpl.colorbar.ColorbarBase(map1ax2, cmap=color_map, norm=norm, orientation='vertical')
			cb3.set_label('{ms}')
			cb3.set_ticks(ticks)


			# Plot GIS layers
			#admin.plot(ax=map2ax1, color='white', edgecolor='black',alpha = 0.2)
			buildings.plot(ax=map2ax1, color = 'green', alpha = 0.5)
			waterareas.plot(ax = map2ax1, color = 'blue', alpha = 0.5)
			# Plot Latency Map
			gps_lat_cam2 = gps_lat_cam2.sort_values(by=[lat_col])
			colores = getColorMap(gps_lat_cam2[lat_col])
			map2ax1.scatter(gps_lat_cam2['x_merc'], gps_lat_cam2['y_merc'], color = colores, s=s1, alpha = alpha)
			map2ax1.scatter(antenna['x_merc'], antenna['y_merc'], color = 'blue', marker='^', s= s2)
			map2ax1.set_xlim(min_x,max_x)
			map2ax1.set_ylim(min_y,max_y)
			#Plot color bar
			map2ax2 = map2.add_axes(rect)
			latency_max = max(gps_lat_cam2[lat_col])
			latency_min = min(gps_lat_cam2[lat_col])
			ticks = np.linspace(latency_min, latency_max, 10)
			norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
			cb4 = mpl.colorbar.ColorbarBase(map2ax2, cmap=color_map, norm=norm, orientation='vertical')
			cb4.set_label('{ms}')
			cb4.set_ticks(ticks)


			# Plot GIS layers
			#admin.plot(ax=map3ax1, color='white', edgecolor='black',alpha = 0.2)
			buildings.plot(ax=map3ax1, color = 'green', alpha = 0.5)
			waterareas.plot(ax = map3ax1, color = 'blue', alpha = 0.5)
			# Plot Latency Map
			gps_lat_cam3 = gps_lat_cam3.sort_values(by=[lat_col])
			colores = getColorMap(gps_lat_cam3[lat_col])
			map3ax1.scatter(gps_lat_cam3['x_merc'], gps_lat_cam3['y_merc'], color = colores, s = s1, alpha = alpha)
			map3ax1.scatter(antenna['x_merc'], antenna['y_merc'], color = 'blue', marker='^', s= s2)
			map3ax1.set_xlim(min_x,max_x)
			map3ax1.set_ylim(min_y,max_y)
			#Plot color bar
			map3ax2 = map3.add_axes(rect)
			latency_max = max(gps_lat_cam3[lat_col])
			latency_min = min(gps_lat_cam3[lat_col])
			ticks = np.linspace(latency_min, latency_max, 10)
			norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
			cb5 = mpl.colorbar.ColorbarBase(map3ax2, cmap=color_map, norm=norm, orientation='vertical')
			cb5.set_label('{ms}')
			cb5.set_ticks(ticks)

			# Plot GIS layers
			#admin.plot(ax=map3ax1, color='white', edgecolor='black',alpha = 0.2)
			buildings.plot(ax=map4ax1, color = 'green', alpha = 0.5)
			waterareas.plot(ax = map4ax1, color = 'blue', alpha = 0.5)
			# Plot Latency Map
			gps_lat_cam4 = gps_lat_cam4.sort_values(by=[lat_col])
			colores = getColorMap(gps_lat_cam4[lat_col])
			map4ax1.scatter(gps_lat_cam4['x_merc'], gps_lat_cam4['y_merc'], color = colores, s = s1, alpha = alpha)
			map4ax1.scatter(antenna['x_merc'], antenna['y_merc'], color = 'blue', marker='^', s= s2)
			map4ax1.set_xlim(min_x,max_x)
			map4ax1.set_ylim(min_y,max_y)
			#Plot color bar
			map4ax2 = map4.add_axes(rect)
			latency_max = max(gps_lat_cam4[lat_col])
			latency_min = min(gps_lat_cam4[lat_col])
			ticks = np.linspace(latency_min, latency_max, 10)
			norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
			cb6 = mpl.colorbar.ColorbarBase(map4ax2, cmap=color_map, norm=norm, orientation='vertical')
			cb6.set_label('{ms}')
			cb6.set_ticks(ticks)


			map5.savefig(save_dir+file_name+"_latency_map_all.jpg")
			map0.savefig(save_dir+file_name+"_latency_map_cam0.jpg")
			map1.savefig(save_dir+file_name+"_latency_map_cam1.jpg")
			map2.savefig(save_dir+file_name+"_latency_map_cam2.jpg")
			map3.savefig(save_dir+file_name+"_latency_map_cam3.jpg")
			map4.savefig(save_dir+file_name+"_latency_map_cam4.jpg")


		data_dic["lat_gps_all"] = file_name+"_latency_map_all.jpg"
		data_dic["lat_gps_cam0"] = file_name+"_latency_map_cam0.jpg"
		data_dic["lat_gps_cam1"] = file_name+"_latency_map_cam1.jpg"
		data_dic["lat_gps_cam2"] = file_name+"_latency_map_cam2.jpg"
		data_dic["lat_gps_cam3"] = file_name+"_latency_map_cam3.jpg"
		data_dic["lat_gps_cam4"] = file_name+"_latency_map_cam4.jpg"

		# Sort again by time
		gps_lat_all = gps_lat_all.sort_index()
		gps_lat_cam0 = gps_lat_cam0.sort_index()
		gps_lat_cam1 = gps_lat_cam1.sort_index()
		gps_lat_cam2 = gps_lat_cam2.sort_index()
		gps_lat_cam3 = gps_lat_cam3.sort_index()
		gps_lat_cam4 = gps_lat_cam4.sort_index()
		#print(gps_lat_all.head(10))

	#//////////////////////////////////////////
	#	 	ADD BASEMAP
	# Find more tile providers in : https://wiki.openstreetmap.org/wiki/Tile_servers
	# Add them by modifying file: /usr/local/lib/python2.7/dist-packages/contextily/tile_providers.py
	#///////////////////////////////////////////
	# https://wiki.openstreetmap.org/wiki/Tile_servers
	#add_basemap(map5ax1, zoom=10, url = ctx.sources.OSM_A)

	plt.close('all')


	#//////////////////////////////////////////
	#
	#  COMPUTE OTHER METRIC: 
	#   - speed vs latency
	#	- elevation vs latency
	#	- antenna density vs latency
	#	- surrounding height vs latency
	#//////////////////////////////////////////
	if(True):

		print("\n---------- GENERATE DATA ANALYSIS GRAPHS --------------")


		#  ------------- SPEED, LATENCY VS TIME GRAPH -----------------
		print("\n---------- SPEED, LATENCY VS TIME GRAPH --------------")

		ana1 = plt.figure(figsize=(20,10))
		#ana1.suptitle(" Data Analysis ")

		ana1ax1 = ana1.add_subplot(1,1,1)
		ana1ax1.set_title(" Latency {ms} and Speed {km/h} vs Time")
		ana1ax1.plot(gps_lat_all.index, gps_lat_all[lat_col], color = 'b', label = 'latency vs time')
		ana1ax1.set_xlabel(" Time ")
		ana1ax1.set_ylabel(" Latency {ms}", color = 'b')
		ana1ax1.legend(loc='upper left', shadow=True, fontsize='x-large')
		ana1ax1.tick_params(axis = 'y', labelcolor='b')
		#ana1ax1.set_xlim(gps_lat_all.index[0],gps_lat_all.index[-1])
		#ticks = pd.date_range(gps_lat_all.index[0],gps_lat_all.index[-1], freq='min')
		#ana1ax1.set_xticks(ticks)

		formatter = mpl.ticker.FuncFormatter(lambda ms, x: time.strftime('%S', time.gmtime(ms // 1000)))
		ana1ax1.xaxis.set_major_formatter(formatter)

		ana1ax2 = ana1ax1.twinx() #ana0.add_subplot(1,1,1) #ana1ax1.twinx()
		ana1ax2.plot(gps_lat_all.index, gps_lat_all['speed'], color = 'r', label = 'speed vs time')
		ana1ax2.set_ylabel('Speed {km/h}', color = 'r')
		ana1ax2.tick_params(axis='y', labelcolor='r')
		ana1ax2.legend(loc='upper right', shadow=True, fontsize='x-large')

		#ana1.tight_layout()

		#  ------------- LATENCY VS SPEED GRAPH -----------------
		print("\n---------- LATENCY VS SPEED GRAPH --------------")

		ana2 = plt.figure(figsize=(20,10))

		ana2.suptitle(" Data Analysis ")
		ana2ax1 = ana2.add_subplot(1,1,1)
		ana2ax1.set_title(" Latency {ms} vs Speed {km/h}")
		ana2ax1.scatter(gps_lat_all['speed'], gps_lat_all[lat_col], color = 'b', label = 'latency vs speed')
		ana2ax1.set_xlabel(" Speed {km/h}")
		ana2ax1.set_ylabel(" Latency {ms}")

		# plot speed vs something graphs
		h = 5  #km/h
		h1 = 2*h# *1000/(3600)
		dx = 0.5 #km/h
		speed_max = max(gps_lat_all['speed'])
		speed_min = min(gps_lat_all['speed'])
		print("Speed min: {}, max: {}".format(speed_min,speed_max))
		speed_group = gps_lat_all.groupby(pd.cut(gps_lat_all['speed'], np.arange(speed_min,speed_max,h1))).mean()
		speed_group['speed_mean'] = map(lambda x: x.mid, speed_group.index.values)
		#print (speed_group.head(10))
		#ana2ax1.scatter(speed_group['speed_mean'], speed_group[lat_col], color ='r', label = 'avg latency')

		low_lim = speed_min
		high_lim = low_lim + h1
		speed_centers = list()
		latency_avg = list()

		while( high_lim <= speed_max):
			# crop data between limits
			lat_avg = gps_lat_all[ gps_lat_all['speed'] >= low_lim ]
			lat_avg = lat_avg[ lat_avg['speed'] <= high_lim]
			#print(lat_avg.head(10))
			# get center point of window
			speed_centers.append((low_lim+high_lim)/2)
			# get latency average inside window
			latency_avg.append(lat_avg[lat_col].mean())
			# move window by delta x
			low_lim = low_lim+dx
			high_lim = high_lim+dx

		avg_lat = gps_lat_all.groupby('speed').mean()

		# draw 
		#ana2ax1.scatter(avg_lat.index, avg_lat[lat_col], color ='r', label = 'avg latency')
		ana2ax1.scatter(speed_centers, latency_avg, color ='r', label = 'avg latency')
		ana2ax1.legend(loc='upper right', shadow=True, fontsize='x-large')


		#  ------------- LATENCY VS ANTENNA INSIDE RADIUS -----------------
		print("\n---------- LATENCY VS ANTENNA INSIDE RADIUS --------------")
		margin_epsg4326 = 0.005  # the number of degrees by which the search area will be extended


		"""
		# reduce antenna search data to reduce computation time
		#print("Antenas antes de cortar: "+str(len(antenna['lat'])))
		a = antenna[ antenna['lon'] <= (max_lon+margin_epsg4326*2.0) ]
		a = a[ a['lon'] >= (min_lon-margin_epsg4326*2.0) ]
		a = a[ a['lat'] <= (max_lat+margin_epsg4326*2.0) ]
		a = a[ a['lat'] >= (min_lat-margin_epsg4326*2.0) ]
		#print("Despues antes de cortar: "+str(len(a['lat'])))
		"""

		# search radius for surrounding antennas

		# WARNING WARNING: If search increases to over 500m, the parameter margin_epsg4326 should be increased 
		# accordingly (margin_epsg4326 = 0.005 aprox to 557m). If want to make searches inside 1km radius
		# then margin epsg_4326 = 0.01 aprox 1.1km will be fine
		r_search = [250,200,150,100,50]
		r_names = ["r4", "r3", "r2", "r1", "r0"]
		for (rname, r) in zip(r_names,r_search):
			#data_dic['r']=r
			test = gps_lat_all[0:50]
			gps_lat_all['antennas'] = map(lambda x,y: getSurroundingAntennas([x,y], r, antenna),gps_lat_all['lat'],gps_lat_all['lon'])

			ana3 = plt.figure(figsize=(20,10))
			ana3ax1 = ana3.add_subplot(1,1,1)
			ana3ax1.set_title(" Latency {ms} vs Antennas in radius of "+str(r)+" m")
			ana3ax1.scatter(gps_lat_all['antennas'], gps_lat_all[lat_col], color = 'b')
			ana3ax1.set_xlabel(" Number of Antennas {}")
			ana3ax1.set_ylabel(" Latency {ms}")
			#ana3ax1.set_xlim(-1,)
			ana3.savefig(save_dir+file_name+"_latency_antenna_in_radius_"+str(r)+".jpg")

			data_dic["latency_antenna_in_radius_"+rname] = file_name+"_latency_antenna_in_radius_"+str(r)+".jpg"




		#  ------------- LATENCY VS BUILDING DENSITY GRAPH -----------------
		print("\n---------- LATENCY VS BUILDING DENSITY GRAPH --------------")

		
		# get building centroids. They will be used to represent the position of the 
		# building
		b_cents = pd.DataFrame()
		# reconvert buildings data to EPSG4326....remember I converted before to Mercator
		buildings = buildings.to_crs(epsg=4326)


		# get latitude and longiute separated
		b_cents["lon"] = buildings.centroid.map(lambda p: p.x)
		b_cents["lat"] = buildings.centroid.map(lambda p: p.y)
		b_cents["height"] = buildings['HEIGHT']
		#print("Buildings antes de cortar: "+str(b_cents.shape))

		# reduce building search area to reduce computation time
		#print("Antenas antes de cortar: "+str(len(antenna['lat'])))
		
		#print("route lon range: "+str((min_lon-margin_epsg4326*2))+", "+str((max_lon+margin_epsg4326*2)))
		#print("route lat range: "+str((min_lat-margin_epsg4326*2))+", "+str((max_lat+margin_epsg4326*2)))

		#print("b cents lon range: "+str(min(b_cents["lon"]))+", "+str(max(b_cents["lon"])))
		#print("b cents lat range: "+str(min(b_cents["lat"]))+", "+str(max(b_cents["lat"])))

		"""
		bc = b_cents[ b_cents["lon"] <= (max_lon+margin_epsg4326*2) ]
		bc = bc[ bc["lon"] >= (min_lon-margin_epsg4326*2) ]
		bc = bc[ bc["lat"] <= (max_lat+margin_epsg4326*2) ]
		bc = bc[ bc["lat"] >= (min_lat-margin_epsg4326*2) ]
		#print("Buildings despues de cortar: "+str(bc.shape))
		"""

		#get the number of surroinding buildings for each point
		gps_lat_all['buildings'] = map(lambda x,y: getSurroundingBuildings([x,y], r, b_cents),gps_lat_all['lat'],gps_lat_all['lon'])

		ana4 = plt.figure(figsize=(20,10))
		ana4ax1 = ana4.add_subplot(1,1,1)
		ana4ax1.set_title(" Latency {ms} vs Number of Buildings in radius of "+str(r)+" m")
		ana4ax1.scatter(gps_lat_all['buildings'], gps_lat_all[lat_col], color = 'c')
		ana4ax1.set_xlabel(" Number of Buildings {}")
		ana4ax1.set_ylabel(" Latency {ms}")
		#ana4ax1.set_xlim(-1,300)
		
		#  ------------- LATENCY VS AVERAGE BUILDING HEIGHT GRAPH-----------------
		
		print("\n---------- DRAW LATENCY VS AVERAGE BUILDING HEIGHT --------------")


		gps_lat_all['avg_build_height'] = map(lambda x,y: getSurroundingBuilding_AvgHeight([x,y], r, b_cents),gps_lat_all['lat'],gps_lat_all['lon'])

		ana5 = plt.figure(figsize=(20,10))
		ana5ax1 = ana5.add_subplot(1,1,1)
		ana5ax1.set_title(" Latency {ms} vs Avg Height of Buildings in radius of "+str(r)+" m")
		ana5ax1.scatter(gps_lat_all['avg_build_height'], gps_lat_all[lat_col], color = 'm')
		ana5ax1.set_xlabel(" AVG Building Height {m}")
		ana5ax1.set_ylabel(" Latency {ms}")

		
		#  ------------- Latency vs Velocity Histogram -----------------
		print("\n---------- DRAW LATENCY VS SPEED HISTOGRAM --------------")

		plt.close('all')


		ana6 = plt.figure(figsize=(20,10))
		ana6ax1 = ana6.add_subplot(1,1,1, projection='3d')
		ana6ax1.set_title("Latency vs Speed Histogram")

		latency_min = min(gps_lat_all[lat_col])
		latency_max = max(gps_lat_all[lat_col])
		hist_lv, xedges, yedges = np.histogram2d(gps_lat_all[lat_col],gps_lat_all['speed'], bins=(32,32), range=[ [latency_min, latency_max],[speed_min, speed_max]])
		#hist_rb, xedges, yedges = np.histogram2d(channels[0].flatten(), channels[2].flatten(), bins=(32,32), range=[[0, 256], [0, 256]])
		#hist_gb, xedges, yedges = np.histogram2d(channels[1].flatten(), channels[2].flatten(), bins=(32,32), range=[[0, 256], [0, 256]])

		# Construct arrays for the anchor positions of the 16 bars.
		#xpos, ypos = np.meshgrid(xedges[:-1] + 1, yedges[:-1] +1, indexing="ij")
		xpos, ypos = np.meshgrid( yedges[:-1]+yedges[1:], xedges[:-1]+xedges[1:])


		xpos = xpos.flatten()/2.
		ypos = ypos.flatten()/2.
		zpos = np.zeros_like(xpos)



		# Construct arrays with the dimensions for the 16 bars.
		dx = xedges[1]-xedges[0]
		dy = yedges[1]-yedges[0]
		dz = hist_lv.flatten()

		cmap = plt.get_cmap('jet') # Get desired colormap - you can change this!
		max_height = np.max(dz)   # get range of colorbars so we can normalize
		min_height = np.min(dz)
		# scale each z to [0,1], and get their rgb values
		colors = [cmap((k-min_height)/max_height) for k in dz] 
		ana6ax1.bar3d(ypos, xpos, zpos, dx, dy, dz, color=colors, zsort='average')
		ana6ax1.set_ylabel("Speed {km/h}")
		ana6ax1.set_xlabel("Latency {ms}")


		#  ------------- SAVE GRAPHS AND INSERT IN REPORT FILE -----------------

		ana1.savefig(save_dir+file_name+"_lat_time_speed_all.jpg")
		ana2.savefig(save_dir+file_name+"_lat_speed_all.jpg")
		#ana3.savefig(save_dir+file_name+"_lat_antennas_all.jpg")
		ana6.savefig(save_dir+file_name+"latency_speed_hist.jpg")


		data_dic["latency_speed_time"] = file_name+"_lat_time_speed_all.jpg"
		data_dic["latency_speed"] = file_name+"_lat_speed_all.jpg"
		#data_dic["latency_antennas"] = file_name+"_lat_antennas_all.jpg"
		#data_dic["lat_gps_cam2"] = file_name+"_latency_map_cam2.jpg"
		#data_dic["lat_gps_cam3"] = file_name+"_latency_map_cam3.jpg"
		data_dic["latency_speed_hist"] = file_name+"latency_speed_hist.jpg"


		#plt.show()

		plt.close('all')


	# ////////////////////////////////////////
	#
	#               PLOT COLORBARS FOR MPLLEAFLET
	#
	# ////////////////////////////////////////
	#Plot color bars first
	rect = 0.1,0.05,0.45,0.9
	figw = 1.5
	figh = 14

	if(True):

		print("\n---------- PLOT DATA IN MPLLEAFLET --------------")


		colorbar5 = plt.figure(figsize=(figw,figh))
		colorbar5ax1 = colorbar5.add_axes(rect)
		latency_max = max(gps_lat_all[lat_col])
		latency_min = min(gps_lat_all[lat_col])
		ticks = np.linspace(latency_min, latency_max, 10)
		norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
		cb5 = mpl.colorbar.ColorbarBase(colorbar5ax1, cmap=color_map, norm=norm, orientation='vertical')
		cb5.set_label('{ms}')
		cb5.set_ticks(ticks)


		colorbar0 = plt.figure(figsize=(figw,figh))
		colorbar0ax1 = colorbar0.add_axes(rect)
		latency_max = max(gps_lat_cam0[lat_col])
		latency_min = min(gps_lat_cam0[lat_col])
		ticks = np.linspace(latency_min, latency_max, 10)
		norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
		cb0 = mpl.colorbar.ColorbarBase(colorbar0ax1, cmap=color_map, norm=norm, orientation='vertical')
		cb0.set_label('{ms}')
		cb0.set_ticks(ticks)

		colorbar1 = plt.figure(figsize=(figw,figh))
		colorbar1ax1 = colorbar1.add_axes(rect)
		latency_max = max(gps_lat_cam1[lat_col])
		latency_min = min(gps_lat_cam1[lat_col])
		ticks = np.linspace(latency_min, latency_max, 10)
		norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
		cb1 = mpl.colorbar.ColorbarBase(colorbar1ax1, cmap=color_map, norm=norm, orientation='vertical')
		cb1.set_label('{ms}')
		cb1.set_ticks(ticks)

		colorbar2 = plt.figure(figsize=(figw,figh))
		colorbar2ax1 = colorbar2.add_axes(rect)
		latency_max = max(gps_lat_cam2[lat_col])
		latency_min = min(gps_lat_cam2[lat_col])
		ticks = np.linspace(latency_min, latency_max, 10)
		norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
		cb2 = mpl.colorbar.ColorbarBase(colorbar2ax1, cmap=color_map, norm=norm, orientation='vertical')
		cb2.set_label('{ms}')
		cb2.set_ticks(ticks)

		colorbar3 = plt.figure(figsize=(figw,figh))
		colorbar3ax1 = colorbar3.add_axes(rect)
		latency_max = max(gps_lat_cam3[lat_col])
		latency_min = min(gps_lat_cam3[lat_col])
		ticks = np.linspace(latency_min, latency_max, 10)
		norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
		cb3 = mpl.colorbar.ColorbarBase(colorbar3ax1, cmap=color_map, norm=norm, orientation='vertical')
		cb3.set_label('{ms}')
		cb3.set_ticks(ticks)

		colorbar4 = plt.figure(figsize=(figw,figh))
		colorbar4ax1 = colorbar4.add_axes(rect)
		latency_max = max(gps_lat_cam4[lat_col])
		latency_min = min(gps_lat_cam4[lat_col])
		ticks = np.linspace(latency_min, latency_max, 10)
		norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
		cb4 = mpl.colorbar.ColorbarBase(colorbar4ax1, cmap=color_map, norm=norm, orientation='vertical')
		cb4.set_label('{ms}')
		cb4.set_ticks(ticks)

		colorbar11 = plt.figure(figsize=(figw,figh))
		colorbar11ax1 = colorbar11.add_axes(rect)
		latency_max = max(gps_lat_all[pc_lat_col])
		latency_min = min(gps_lat_all[pc_lat_col])
		ticks = np.linspace(latency_min, latency_max, 10)
		norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
		cb11 = mpl.colorbar.ColorbarBase(colorbar11ax1, cmap=color_map, norm=norm, orientation='vertical')
		cb11.set_label('{ms}')
		cb11.set_ticks(ticks)


		colorbar6 = plt.figure(figsize=(figw,figh))
		colorbar6ax1 = colorbar6.add_axes(rect)
		latency_max = max(gps_lat_cam0[pc_lat_col])
		latency_min = min(gps_lat_cam0[pc_lat_col])
		ticks = np.linspace(latency_min, latency_max, 10)
		norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
		cb7 = mpl.colorbar.ColorbarBase(colorbar6ax1, cmap=color_map, norm=norm, orientation='vertical')
		cb7.set_label('{ms}')
		cb7.set_ticks(ticks)

		colorbar7 = plt.figure(figsize=(figw,figh))
		colorbar7ax1 = colorbar7.add_axes(rect)
		latency_max = max(gps_lat_cam1[pc_lat_col])
		latency_min = min(gps_lat_cam1[pc_lat_col])
		ticks = np.linspace(latency_min, latency_max, 10)
		norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
		cb8 = mpl.colorbar.ColorbarBase(colorbar7ax1, cmap=color_map, norm=norm, orientation='vertical')
		cb8.set_label('{ms}')
		cb8.set_ticks(ticks)

		colorbar8 = plt.figure(figsize=(figw,figh))
		colorbar8ax1 = colorbar8.add_axes(rect)
		latency_max = max(gps_lat_cam2[pc_lat_col])
		latency_min = min(gps_lat_cam2[pc_lat_col])
		ticks = np.linspace(latency_min, latency_max, 10)
		norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
		cb9 = mpl.colorbar.ColorbarBase(colorbar8ax1, cmap=color_map, norm=norm, orientation='vertical')
		cb9.set_label('{ms}')
		cb9.set_ticks(ticks)

		colorbar9 = plt.figure(figsize=(figw,figh))
		colorbar9ax1 = colorbar9.add_axes(rect)
		latency_max = max(gps_lat_cam3[pc_lat_col])
		latency_min = min(gps_lat_cam3[pc_lat_col])
		ticks = np.linspace(latency_min, latency_max, 10)
		norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
		cb10 = mpl.colorbar.ColorbarBase(colorbar9ax1, cmap=color_map, norm=norm, orientation='vertical')
		cb10.set_label('{ms}')
		cb10.set_ticks(ticks)

		colorbar10 = plt.figure(figsize=(figw,figh))
		colorbar10ax1 = colorbar10.add_axes(rect)
		latency_max = max(gps_lat_cam4[pc_lat_col])
		latency_min = min(gps_lat_cam4[pc_lat_col])
		ticks = np.linspace(latency_min, latency_max, 10)
		norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
		cb12 = mpl.colorbar.ColorbarBase(colorbar10ax1, cmap=color_map, norm=norm, orientation='vertical')
		cb12.set_label('{ms}')
		cb12.set_ticks(ticks)


		colorbar20 = plt.figure(figsize=(figw,figh))
		colorbar20ax1 = colorbar20.add_axes(rect)
		latency_max = max(gps_lat_all['sat'])
		latency_min = min(gps_lat_all['sat'])
		ticks = np.linspace(latency_min, latency_max, 2)
		norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
		cb20 = mpl.colorbar.ColorbarBase(colorbar20ax1, cmap=color_map, norm=norm, orientation='vertical')
		cb20.set_label('{count}')
		cb20.set_ticks(ticks)

		colorbar5.savefig(save_dir+file_name+"_colorbar_map_all.jpg")
		colorbar0.savefig(save_dir+file_name+"_colorbar_map_cam0.jpg")
		colorbar1.savefig(save_dir+file_name+"_colorbar_map_cam1.jpg")
		colorbar2.savefig(save_dir+file_name+"_colorbar_map_cam2.jpg")
		colorbar3.savefig(save_dir+file_name+"_colorbar_map_cam3.jpg")
		colorbar4.savefig(save_dir+file_name+"_colorbar_map_cam4.jpg")

		colorbar11.savefig(save_dir+file_name+"_pc_colorbar_map_all.jpg")
		colorbar6.savefig(save_dir+file_name+"_pc_colorbar_map_cam0.jpg")
		colorbar7.savefig(save_dir+file_name+"_pc_colorbar_map_cam1.jpg")
		colorbar8.savefig(save_dir+file_name+"_pc_colorbar_map_cam2.jpg")
		colorbar9.savefig(save_dir+file_name+"_pc_colorbar_map_cam3.jpg")
		colorbar10.savefig(save_dir+file_name+"_pc_colorbar_map_cam4.jpg")

		colorbar20.savefig(save_dir+file_name+"_satellite_colobar.jpg")

		data_dic["latency_map_all_colorbar"] = file_name+"_colorbar_map_all.jpg"
		data_dic["latency_map_cam0_colorbar"] = file_name+"_colorbar_map_cam0.jpg"
		data_dic["latency_map_cam1_colorbar"] = file_name+"_colorbar_map_cam1.jpg"
		data_dic["latency_map_cam2_colorbar"] = file_name+"_colorbar_map_cam2.jpg"
		data_dic["latency_map_cam3_colorbar"] = file_name+"_colorbar_map_cam3.jpg"
		data_dic["latency_map_cam4_colorbar"] = file_name+"_colorbar_map_cam4.jpg"

		data_dic["pc_latency_map_all_colorbar"] = file_name+"_colorbar_map_all.jpg"
		data_dic["pc_latency_map_cam0_colorbar"] = file_name+"_colorbar_map_cam0.jpg"
		data_dic["pc_latency_map_cam1_colorbar"] = file_name+"_colorbar_map_cam1.jpg"
		data_dic["pc_latency_map_cam2_colorbar"] = file_name+"_colorbar_map_cam2.jpg"
		data_dic["pc_latency_map_cam3_colorbar"] = file_name+"_colorbar_map_cam3.jpg"
		data_dic["pc_latency_map_cam4_colorbar"] = file_name+"_colorbar_map_cam4.jpg"

		data_dic["satellite_map_colorbar"] = file_name+"_satellite_colobar.jpg"


		plt.close('all')


	####### CREATE WEB MAP FILES

	if(True):
		print("\n---------- CREATE WEB MAP FILES --------------")

		#plt.hold(True)

		 
		a = antenna[ antenna['x_merc'] <= (max_x+(margin*2)) ]
		a = a[ a['x_merc'] >= (min_x-(margin*2)) ]
		a = a[ a['y_merc'] <= (max_y+(margin*2)) ]
		a = a[ a['y_merc'] >= (min_y-(margin*2)) ]

		if(args.y == "5"):
			#name = "Greys"
			map5 = plt.figure(figsize=(20,10))
			map5ax1 = map5.add_subplot(1,1,1) #add_axes(rect)
			map5ax1.set_aspect('equal')
			print("Drawing Latency Map for All Cameras")
			gps_lat_all = gps_lat_all.sort_values(by=[lat_col],ascending=False)
			colores = getColorMap(gps_lat_all[lat_col])
			#map5ax1.scatter(gps_lat_all['lon'], gps_lat_all['lat'], color = "k", s = s1+2, alpha = alpha)#,edgecolors = "k", linewidths='3')
			map5ax1.scatter(gps_lat_all['lon'], gps_lat_all['lat'], color = colores, s = s1, alpha = alpha)# ,edgecolors = "k", linewidths=0.5)
			map5ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)
			#map5ax1.scatter(bc['lon'], bc['lat'], color = 'green', marker='*', s = s2)

			# highlight highest values by drawing them again
			max_lat = max(gps_lat_all[lat_col])
			min_lat = min(gps_lat_all[lat_col])
			lat34 = (max_lat-min_lat)*0.25
			highest = gps_lat_all[ gps_lat_all[lat_col] > (max_lat - lat34)  ]
			# add lowest value just for the color map to be correct
			lowest = gps_lat_all[ gps_lat_all[lat_col] == (min_lat)]
			highest = pd.concat([highest,lowest], ignore_index=True)
			highest = highest.sort_values(by=[lat_col],ascending=False)
			print(highest)
			colores = getColorMap(highest[lat_col])		
			map5ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

			mplleaflet.show()

		if(args.y == "0"):
			#name = "Purples"
			map0 = plt.figure(figsize=(20,10))
			map0ax1 = map0.add_subplot(1,1,1)
			map0ax1.set_aspect('equal')
			print("Drawing Latency Map for Camera 0")
			gps_lat_cam0 = gps_lat_cam0.sort_values(by=[lat_col],ascending=False)
			colores = getColorMap(gps_lat_cam0[lat_col])
			map0ax1.scatter(gps_lat_cam0['lon'], gps_lat_cam0['lat'], color = colores, s = s1, alpha = alpha)
			map0ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)

			# highlight highest values by drawing them again
			max_lat = max(gps_lat_all[lat_col])
			min_lat = min(gps_lat_all[lat_col])
			lat34 = (max_lat-min_lat)*0.25
			highest = gps_lat_all[ gps_lat_all[lat_col] > (max_lat - lat34)  ]
			# add lowest value just for the color map to be correct
			lowest = gps_lat_all[ gps_lat_all[lat_col] == (min_lat)]
			highest = pd.concat([highest,lowest], ignore_index=True)
			highest = highest.sort_values(by=[lat_col],ascending=False)
			print(highest)
			colores = getColorMap(highest[lat_col])		
			map0ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

			

			mplleaflet.show()

		if(args.y == "1"):
			#name = "Blues"
			map1 = plt.figure(figsize=(20,10))
			map1ax1 = map1.add_subplot(1,1,1)
			map1ax1.set_aspect('equal')
			print("Drawing Latency Map for Camera 1")
			gps_lat_cam1 = gps_lat_cam1.sort_values(by=[lat_col],ascending=False)
			colores = getColorMap(gps_lat_cam1[lat_col])
			map1ax1.scatter(gps_lat_cam1['lon'], gps_lat_cam1['lat'], color = colores, s = s1, alpha = alpha)
			map1ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)

			# highlight highest values by drawing them again
			max_lat = max(gps_lat_all[lat_col])
			min_lat = min(gps_lat_all[lat_col])
			lat34 = (max_lat-min_lat)*0.25
			highest = gps_lat_all[ gps_lat_all[lat_col] > (max_lat - lat34)  ]
			# add lowest value just for the color map to be correct
			lowest = gps_lat_all[ gps_lat_all[lat_col] == (min_lat)]
			highest = pd.concat([highest,lowest], ignore_index=True)
			highest = highest.sort_values(by=[lat_col],ascending=False)
			print(highest)
			colores = getColorMap(highest[lat_col])		
			map1ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

			

			mplleaflet.show()

		if(args.y == "2"):
			#name = "Greens"
			map2 = plt.figure(figsize=(20,10))
			map2ax1 = map2.add_subplot(1,1,1)
			map2ax1.set_aspect('equal')
			print("Drawing Latency Map for Camera 2")
			gps_lat_cam2 = gps_lat_cam2.sort_values(by=[lat_col],ascending=False)
			colores = getColorMap(gps_lat_cam2[lat_col])
			map2ax1.scatter(gps_lat_cam2['lon'], gps_lat_cam2['lat'], color = colores, s = s1, alpha = alpha)
			map2ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)

			# highlight highest values by drawing them again
			max_lat = max(gps_lat_all[lat_col])
			min_lat = min(gps_lat_all[lat_col])
			lat34 = (max_lat-min_lat)*0.25
			highest = gps_lat_all[ gps_lat_all[lat_col] > (max_lat - lat34)  ]
			# add lowest value just for the color map to be correct
			lowest = gps_lat_all[ gps_lat_all[lat_col] == (min_lat)]
			highest = pd.concat([highest,lowest], ignore_index=True)
			highest = highest.sort_values(by=[lat_col],ascending=False)
			print(highest)
			colores = getColorMap(highest[lat_col])		
			map2ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

			

			mplleaflet.show()

		if(args.y == "3"):
			#name = "BuPu"
			map3 = plt.figure(figsize=(20,10))
			map3ax1 = map3.add_subplot(1,1,1)
			map3ax1.set_aspect('equal')
			print("Drawing Latency Map for Camera 3")
			gps_lat_cam3 = gps_lat_cam3.sort_values(by=[lat_col],ascending=False)
			colores = getColorMap(gps_lat_cam3[lat_col])
			map3ax1.scatter(gps_lat_cam3['lon'], gps_lat_cam3['lat'], color = colores, s = s1, alpha = alpha)
			map3ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)

			# highlight highest values by drawing them again
			max_lat = max(gps_lat_all[lat_col])
			min_lat = min(gps_lat_all[lat_col])
			lat34 = (max_lat-min_lat)*0.25
			highest = gps_lat_all[ gps_lat_all[lat_col] > (max_lat - lat34)  ]
			# add lowest value just for the color map to be correct
			lowest = gps_lat_all[ gps_lat_all[lat_col] == (min_lat)]
			highest = pd.concat([highest,lowest], ignore_index=True)
			highest = highest.sort_values(by=[lat_col],ascending=False)
			print(highest)
			colores = getColorMap(highest[lat_col])		
			map3ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

			

			mplleaflet.show()

		if(args.y == "4"):
			#name = "YlGnBu"
			map4 = plt.figure(figsize=(20,10))
			map4ax1 = map4.add_subplot(1,1,1)
			map4ax1.set_aspect('equal')
			print("Drawing Latency Map for Camera 3")
			gps_lat_cam4 = gps_lat_cam4.sort_values(by=[lat_col],ascending=False)
			colores = getColorMap(gps_lat_cam4[lat_col])
			map4ax1.scatter(gps_lat_cam4['lon'], gps_lat_cam4['lat'], color = colores, s = s1, alpha = alpha)
			map4ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)

			# highlight highest values by drawing them again
			max_lat = max(gps_lat_all[lat_col])
			min_lat = min(gps_lat_all[lat_col])
			lat34 = (max_lat-min_lat)*0.25
			highest = gps_lat_all[ gps_lat_all[lat_col] > (max_lat - lat34)  ]
			# add lowest value just for the color map to be correct
			lowest = gps_lat_all[ gps_lat_all[lat_col] == (min_lat)]
			highest = pd.concat([highest,lowest], ignore_index=True)
			highest = highest.sort_values(by=[lat_col],ascending=False)
			print(highest)
			colores = getColorMap(highest[lat_col])		
			map4ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

			

			mplleaflet.show()

		if(args.y == "11"):
			#name = "Greys"
			map5 = plt.figure(figsize=(20,10))
			map5ax1 = map5.add_subplot(1,1,1) #add_axes(rect)
			map5ax1.set_aspect('equal')
			print("Drawing Latency Map for All Cameras")
			gps_lat_all = gps_lat_all.sort_values(by=[pc_lat_col],ascending=False)
			colores = getColorMap(gps_lat_all[pc_lat_col])
			#map5ax1.scatter(gps_lat_all['lon'], gps_lat_all['lat'], color = "k", s = s1+2, alpha = alpha)#,edgecolors = "k", linewidths='3')
			map5ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)	
			map5ax1.scatter(gps_lat_all['lon'], gps_lat_all['lat'], color = colores, s = s1, alpha = alpha)# ,edgecolors = "k", linewidths=0.5)
			
			# highlight highest values by drawing them again
			max_lat = max(gps_lat_all[pc_lat_col])
			min_lat = min(gps_lat_all[pc_lat_col])
			lat34 = (max_lat-min_lat)*0.25
			highest = gps_lat_all[ gps_lat_all[pc_lat_col] > (max_lat - lat34)  ]
			# add lowest value just for the color map to be correct
			lowest = gps_lat_all[ gps_lat_all[pc_lat_col] == (min_lat)]
			highest = pd.concat([highest,lowest], ignore_index=True)
			highest = highest.sort_values(by=[pc_lat_col],ascending=False)
			print(highest)
			colores = getColorMap(highest[pc_lat_col])		
			map5ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

			

			#map5ax1.scatter(bc['lon'], bc['lat'], color = 'green', marker='*', s = s2)
			mplleaflet.show()

		if(args.y == "6"):
			#name = "Purples"
			map0 = plt.figure(figsize=(20,10))
			map0ax1 = map0.add_subplot(1,1,1)
			map0ax1.set_aspect('equal')
			print("Drawing Latency Map for Camera 0")
			gps_lat_cam0 = gps_lat_cam0.sort_values(by=[pc_lat_col],ascending=False)
			colores = getColorMap(gps_lat_cam0[pc_lat_col])
			map0ax1.scatter(gps_lat_cam0['lon'], gps_lat_cam0['lat'], color = colores, s = s1, alpha = alpha)
			map0ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)

			# highlight highest values by drawing them again
			max_lat = max(gps_lat_all[pc_lat_col])
			min_lat = min(gps_lat_all[pc_lat_col])
			lat34 = (max_lat-min_lat)*0.25
			highest = gps_lat_all[ gps_lat_all[pc_lat_col] > (max_lat - lat34)  ]
			# add lowest value just for the color map to be correct
			lowest = gps_lat_all[ gps_lat_all[pc_lat_col] == (min_lat)]
			highest = pd.concat([highest,lowest], ignore_index=True)
			highest = highest.sort_values(by=[pc_lat_col],ascending=False)
			print(highest)
			colores = getColorMap(highest[pc_lat_col])		
			map0ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

			


			mplleaflet.show()


		if(args.y == "7"):
			#name = "Blues"
			map1 = plt.figure(figsize=(20,10))
			map1ax1 = map1.add_subplot(1,1,1)
			map1ax1.set_aspect('equal')
			print("Drawing Latency Map for Camera 1")
			gps_lat_cam1 = gps_lat_cam1.sort_values(by=[pc_lat_col],ascending=False)
			colores = getColorMap(gps_lat_cam1[pc_lat_col])
			map1ax1.scatter(gps_lat_cam1['lon'], gps_lat_cam1['lat'], color = colores, s = s1, alpha = alpha)
			map1ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)
			
			# highlight highest values by drawing them again
			max_lat = max(gps_lat_all[pc_lat_col])
			min_lat = min(gps_lat_all[pc_lat_col])
			lat34 = (max_lat-min_lat)*0.25
			highest = gps_lat_all[ gps_lat_all[pc_lat_col] > (max_lat - lat34)  ]
			# add lowest value just for the color map to be correct
			lowest = gps_lat_all[ gps_lat_all[pc_lat_col] == (min_lat)]
			highest = pd.concat([highest,lowest], ignore_index=True)
			highest = highest.sort_values(by=[pc_lat_col],ascending=False)
			print(highest)
			colores = getColorMap(highest[pc_lat_col])		
			map1ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

			mplleaflet.show()




		if(args.y == "8"):
			#name = "Greens"
			map2 = plt.figure(figsize=(20,10))
			map2ax1 = map2.add_subplot(1,1,1)
			map2ax1.set_aspect('equal')
			print("Drawing Latency Map for Camera 2")
			gps_lat_cam2 = gps_lat_cam2.sort_values(by=[pc_lat_col],ascending=False)
			colores = getColorMap(gps_lat_cam2[pc_lat_col])
			map2ax1.scatter(gps_lat_cam2['lon'], gps_lat_cam2['lat'], color = colores, s = s1, alpha = alpha)
			map2ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)
			
			# highlight highest values by drawing them again
			max_lat = max(gps_lat_all[pc_lat_col])
			min_lat = min(gps_lat_all[pc_lat_col])
			lat34 = (max_lat-min_lat)*0.25
			highest = gps_lat_all[ gps_lat_all[pc_lat_col] > (max_lat - lat34)  ]
			# add lowest value just for the color map to be correct
			lowest = gps_lat_all[ gps_lat_all[pc_lat_col] == (min_lat)]
			highest = pd.concat([highest,lowest], ignore_index=True)
			highest = highest.sort_values(by=[pc_lat_col],ascending=False)
			print(highest)
			colores = getColorMap(highest[pc_lat_col])		
			map2ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

			mplleaflet.show()

		if(args.y == "9"):
			#name = "BuPu"
			map3 = plt.figure(figsize=(20,10))
			map3ax1 = map3.add_subplot(1,1,1)
			map3ax1.set_aspect('equal')
			print("Drawing Latency Map for Camera 3")
			gps_lat_cam3 = gps_lat_cam3.sort_values(by=[pc_lat_col],ascending=False)
			colores = getColorMap(gps_lat_cam3[pc_lat_col])
			map3ax1.scatter(gps_lat_cam3['lon'], gps_lat_cam3['lat'], color = colores, s = s1, alpha = alpha)
			map3ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)
			
			# highlight highest values by drawing them again
			max_lat = max(gps_lat_all[pc_lat_col])
			min_lat = min(gps_lat_all[pc_lat_col])
			lat34 = (max_lat-min_lat)*0.25
			highest = gps_lat_all[ gps_lat_all[pc_lat_col] > (max_lat - lat34)  ]
			# add lowest value just for the color map to be correct
			lowest = gps_lat_all[ gps_lat_all[pc_lat_col] == (min_lat)]
			highest = pd.concat([highest,lowest], ignore_index=True)
			highest = highest.sort_values(by=[pc_lat_col],ascending=False)
			print(highest)
			colores = getColorMap(highest[pc_lat_col])		
			map3ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

			
			mplleaflet.show()

		if(args.y == "10"):
			#name = "YlGnBu"
			map4 = plt.figure(figsize=(20,10))
			map4ax1 = map4.add_subplot(1,1,1)
			map4ax1.set_aspect('equal')
			print("Drawing Latency Map for Camera 3")
			gps_lat_cam4 = gps_lat_cam4.sort_values(by=[pc_lat_col],ascending=False)
			colores = getColorMap(gps_lat_cam4[pc_lat_col])
			map4ax1.scatter(gps_lat_cam4['lon'], gps_lat_cam4['lat'], color = colores, s = s1, alpha = alpha)
			map4ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)
			
			# highlight highest values by drawing them again
			max_lat = max(gps_lat_all[pc_lat_col])
			min_lat = min(gps_lat_all[pc_lat_col])
			lat34 = (max_lat-min_lat)*0.25
			highest = gps_lat_all[ gps_lat_all[pc_lat_col] > (max_lat - lat34)  ]
			# add lowest value just for the color map to be correct
			lowest = gps_lat_all[ gps_lat_all[pc_lat_col] == (min_lat)]
			highest = pd.concat([highest,lowest], ignore_index=True)
			highest = highest.sort_values(by=[pc_lat_col],ascending=False)
			print(highest)
			colores = getColorMap(highest[pc_lat_col])		
			map4ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)



			mplleaflet.show()		

		#mplleaflet.show()
		# show Graphs in screen
		#plt.show()

		plt.close('all')


	# ////////////////////////////////////////
	#
	#               CREATE REPORT FILE
	#
	# ////////////////////////////////////////

	print("\n---------- CREATE REPORT FILE --------------")

	if(True):
		date = str(gps_lat_all.index.values[0])
		data_dic["date"]=date
		data_dic["name"]=args.t
		data_dic["video_res"]=args.r
		#data_dic["track_image_path"]=args.a
		#data_dic["data_image_path"] = args.k



		myfile = codecs.open('fm2.md','r', encoding='utf-8' )
		data=myfile.read()
		myfile.close()
		#print data
		rep_for = data.format(**data_dic)
		#print(rep_for)
		myfile = codecs.open(save_dir+'report.md','w', encoding='utf-8' )
		myfile.write(rep_for)
		myfile.close()


	# ////////////////////////////////////////
	#
	#               GET GOOGLE STREET VIEW IMAGES
	#
	# ////////////////////////////////////////

	print("\n---------- GET GOOGLE STREET VIEW IMAGES --------------")

	if(False):


		key = "AIzaSyAood30jRDeVrxCrsEiRxUr1X7F5ZNTQ7Q"
		gps_lat_all = gps_lat_all.sort_values(by=[lat_col], ascending = False)
		ix = gps_lat_all.index.values
		max_lat1 = gps_lat_all.at[ix[0],lat_col]
		max_lat2 = gps_lat_all.at[ix[1],lat_col]
		max_lat3 = gps_lat_all.at[ix[2],lat_col]
		max_lat1_c = str(gps_lat_all.at[ix[0],'lat'])+","+str(gps_lat_all.at[ix[0],'lon'])
		max_lat2_c = str(gps_lat_all.at[ix[1],'lat'])+","+str(gps_lat_all.at[ix[1],'lon'])
		max_lat3_c = str(gps_lat_all.at[ix[2],'lat'])+","+str(gps_lat_all.at[ix[2],'lon'])

		print(str(max_lat1)+": "+max_lat1_c)
		print(str(max_lat2)+": "+max_lat2_c)
		print(str(max_lat3)+": "+max_lat3_c)




		"""

		loc = str(gps_lat_all.at[ix[0],'lat'])+","+str(gps_lat_all.at[ix[0],'lon'])
		print(loc)

		# Define parameters for street view api
		params = [{
		  'size': '600x300', # max 640x640 pixels
		  'location': loc,
		  'heading': '90',
		  'pitch': '-0.76',
		  'key': key
		}]


		import streetview
		panoids = streetview.panoids(lat=gps_lat_all.at[ix[0],'lat'], lon=gps_lat_all.at[ix[0],'lon'])
		#print(panoids)
		panoid = panoids[2]['panoid']
		print(panoid)
		for im in panoids:
			panoid = im['panoid']
			streetview.api_download(panoid, '90', save_dir[0:-1], key)

			lat = im['lat']
			lon = im['lon']
			loc = str(lat)+","+str(lon)
			print(loc)
			params[0]['location'] = loc
			# Create a results object
			results = google_streetview.api.results(params)

			# Preview results
			#results.preview()

			# Download images to directory 'downloads'
			results.download_links("maps")
			results.save_links("maps/links.txt")
		"""




	# ////////////////////////////////////////
	#
	#               PATTERN RECOGNITION
	#
	# ////////////////////////////////////////

	print("\n---------- TRY TO RECOGNIZE PATTERNS --------------")

	gps_lat_all.to_csv(save_dir+"gps_lat_all.csv", sep=",",header=True)
	gps_lat_cam0.to_csv(save_dir+"gps_lat_cam0.csv", sep=",",header=True)
	gps_lat_cam1.to_csv(save_dir+"gps_lat_cam1.csv", sep=",",header=True)
	gps_lat_cam2.to_csv(save_dir+"gps_lat_cam2.csv", sep=",",header=True)
	gps_lat_cam3.to_csv(save_dir+"gps_lat_cam3.csv", sep=",",header=True)
	gps_lat_cam4.to_csv(save_dir+"gps_lat_cam4.csv", sep=",",header=True)
	antenna.to_csv(save_dir+"antenna.csv", sep=",",header=True)



	if(True):

		# original data import
		o_data = pd.read_csv("data.csv", sep=",", header = 0)
		data1 = o_data.loc[:,['lat','lon','antennas','speed','ele','buildings','avg_build_height', lat_col]]


		#print(data1.head())
		#print(data1.cov())

		#data = data1.loc[:,['lat','lon','antennas','speed','ele','buildings','avg_build_height']].values
		data = data1.loc[:,['antennas','speed','ele','buildings','avg_build_height']].values

		#print(data[0:5])
		#print(data.shape[1])
		#y = gps_lat_all.iloc[:,'latency'].values
		data_std = StandardScaler().fit_transform(data)

		#data_std = data

		# get covariance matrix, pass transpose of data because that is what np.cov expects
		cov = np.cov(data_std.T)
		# get eigen values and vectors
		eig_vals, eig_vecs = np.linalg.eig(cov)
		#print('Eigen Values {}'.format(eig_vals))
		#print('Eigen Vectors {}'.format(eig_vecs))

		# Make a list of (eigenvalue, eigenvector) tuples
		eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]

		# Sort the (eigenvalue, eigenvector) tuples from high to low
		eig_pairs.sort()
		eig_pairs.reverse()

		# Draw information 
		tot = sum(eig_vals)
		var_exp = [(i / tot)*100 for i in sorted(eig_vals, reverse=True)]
		cum_var_exp = np.cumsum(var_exp)
		print(cum_var_exp)

		fig = plt.figure(figsize=(20,10))

		ax = fig.add_subplot(1,1,1)
		ax.plot(['PC %s' %i for i in range(0,len(var_exp))], cum_var_exp, color='m', label = "Cumulative Explained Variance" )
		ax.bar(['PC %s' %i for i in range(0,len(var_exp))], var_exp, color ='g', label = "Explained Variance")
		ax.set_title("Explained Variance")
		ax.set_ylabel("Explained Variance")
		ax.set_xlabel("Principal Components")
		ax.legend(loc='center right', shadow=True, fontsize='large')




		figk = plt.figure(figsize=(20,10))

		ax2 = figk.add_subplot(1,1,1)

		# Make transformation matrix
		#matrix_w = eig_pairs[0][1].reshape(5,1)
		matrix_w = np.hstack((eig_pairs[0][1].reshape(data_std.shape[1],1), eig_pairs[1][1].reshape(data_std.shape[1],1)))
		matrix_w2 = np.hstack((eig_pairs[0][1].reshape(data_std.shape[1],1), eig_pairs[1][1].reshape(data_std.shape[1],1),eig_pairs[2][1].reshape(data_std.shape[1],1) ))

		#print("Transformation")
		#print(matrix_w)

		# Reproject data
		y = data_std.dot(matrix_w)
		y2 = data_std.dot(matrix_w2)
		#print("Reprojected")
		#print(y[0:5])
		# use this cmap
		name = 'RdYlGn'
		color_map=plt.get_cmap(name)
		colores = getColorMap(data1[lat_col])
		#ax2.scatter(y[:,0], [0]*len(y[:,0]), color = colores)
		ax2.scatter(y[:,0],y[:,1], color = colores)
		# R-G-B Scatter




		#Plot color bar
		rect = 0.92,0.1,0.025,0.8
		colbar = figk.add_axes(rect)
		latency_max = max(data1[lat_col])
		latency_min = min(data1[lat_col])
		ticks = np.linspace(latency_min, latency_max, 10)
		norm = mpl.colors.Normalize(vmin=latency_min, vmax=latency_max)
		cb5 = mpl.colorbar.ColorbarBase(colbar, cmap=color_map, norm=norm, orientation='vertical')
		cb5.set_label('Latency {ms}')
		cb5.set_ticks(ticks)


		window = plt.figure(figsize=(20,10))

		ax5 = window.add_subplot(1,1,1, projection='3d')
		ax5.scatter(y2[:,0],y2[:,1], y2[:,2], color = colores)
		ax5.set_xlabel('PC1')
		ax5.set_ylabel('PC2')
		ax5.set_zlabel('PC3')

		#Plot color bar
		colbar2 = window.add_axes(rect)
		cb6 = mpl.colorbar.ColorbarBase(colbar2, cmap=color_map, norm=norm, orientation='vertical')
		cb6.set_label('Latency {ms}')
		cb6.set_ticks(ticks)

		#print (buildings.head(2))
		#index_pos = buildings.index.values[0]
		#print (buildings.at[index_pos,'geometry'])
		#print (buildings.columns)



		plt.show()




