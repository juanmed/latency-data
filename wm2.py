# Draw web latency maps based on predefined data

import numpy as np 
import pandas as pd
import mplleaflet
import logAnalysis as la
import matplotlib.pyplot as plt
import matplotlib as mpl




# get color map from data list
def getColorMap(data):
	cmap = plt.get_cmap(name) # Get desired colormap - you can change this!
	max_height = np.max(data)   # get range of colorbars so we can normalize
	min_height = np.min(data)
	# scale each z to [0,1], and get their rgb values
	rgba = [cmap(((k-min_height)/max_height) ) for k in data] 
	#rgba = [cmap(1.0 - ((k-min_height)/max_height) ) for k in data] 
	return rgba

# draw latency map over webmap
def drawWebMap(data, cam_num, ant, col):
	# create a fig that spans the whole screen
	fig = plt.figure(figsize=(20,10))
	#fig.suptitle(", ".join(names)+" "+title, fontsize='x-large', fontweight = 'bold')
	
	# define dimensions of graph area
	rect = 0.05,0.05,0.9,0.85
	ax = fig.add_axes(rect)

	try:
		# get data for selected camera only
		print(data.head(10))
		print(" - ID Seleccionado: {}".format(cam_num))
		cam_data = data[ data['id'] == cam_num]
		print(cam_data.head(10))
	except:
		print(" - Camera ID requested non existent. Drawing for all cameras.")
		cam_data = data

	cam_data = cam_data.sort_values(by=[col],ascending=False)
	# get colors based on latency
	colores = getColorMap(cam_data[col])
	ax.scatter(cam_data['lon'], cam_data['lat'], color = colores, s = s1, alpha = alpha)# ,edgecolors = "k", linewidths=0.5)
	# now draw 4G antennas
	ax.scatter(ant['lon'], ant['lat'], color = 'blue', marker='^', s = s2)

	return fig, ax 

# get arguments to the program
args = la.createCommandLineParser()

#color map name
name = 'inferno_r'

# get file name
file_path = args.f
dirs = file_path.split("/")

file_name = dirs[-1].split(".")[0]
#print("File name:" + file_name)


# save all files in the same directory as the log files
save_dir = ""
for element in dirs[0:len(dirs)-1]:
	save_dir = save_dir + element+"/"
#print("Save dir:"+save_dir)


# ////////////////////////////////////////
#
#               PLOT COLORBARS FOR MPLLEAFLET
#
# ////////////////////////////////////////
#Plot color bars first
rect = 0.1,0.05,0.45,0.9
figw = 1.5
figh = 14


gps_lat_all = pd.read_csv(save_dir+"gps_lat_all.csv", sep=",", header = 0)
gps_lat_cam0 = pd.read_csv(save_dir+"gps_lat_cam0.csv", sep=",", header = 0)
gps_lat_cam1 = pd.read_csv(save_dir+"gps_lat_cam1.csv", sep=",", header = 0)
gps_lat_cam2 = pd.read_csv(save_dir+"gps_lat_cam2.csv", sep=",", header = 0)
gps_lat_cam3 = pd.read_csv(save_dir+"gps_lat_cam3.csv", sep=",", header = 0)
gps_lat_cam4 = pd.read_csv(save_dir+"gps_lat_cam4.csv", sep=",", header = 0)
gps_lat_cam5 = pd.read_csv(save_dir+"gps_lat_cam4.csv", sep=",", header = 0)
antenna = pd.read_csv(save_dir+"antenna.csv", sep=",", header = 0)


#print("GPS Latency All Cameras log:\n {}".format(gps_lat_all.head(10)))
#print("GPS Latency  Camera0 log:\n {}".format(gps_lat_cam0.head(10)))
#print("GPS Latency  Camera1 log:\n {}".format(gps_lat_cam1.head(10)))
#print("GPS Latency  Camera2 log:\n {}".format(gps_lat_cam2.head(10)))
#print("GPS Latency  Camera3 log:\n {}".format(gps_lat_cam3.head(10)))
#print("GPS Latency  Camera4 log:\n {}".format(gps_lat_cam4.head(10)))
#print("Antenna log:\n {}".format(antenna.head(10)))


# define graph parameters
color_map=plt.get_cmap(name)
s1 = 75         # track marker size
s2 = 15.0        # antenna marker size
alpha = 0.7     # transparency


opt = la.opt

if(opt == 0):
	enc_lat_col = 'encoding_latency'
	net_lat_col = 'network_latency'
	tot_lat_col = 'total_latency'

if(opt == 1):
	enc_lat_col = 'encoding_latency'
	net_lat_col = 'network_latency'
	tot_lat_col = 'total_latency'
if(opt == 2):
	enc_lat_col = 'encoding_latency'
	net_lat_col = 'network_latency'
	tot_lat_col = 'total_latency'

#print(tot_lat_col)
#print(net_lat_col)

margin = 500.0
margin_epsg4326 = 0.005
max_lat = max(gps_lat_all['lat'])
min_lat = min(gps_lat_all['lat'])
max_lon = max(gps_lat_all['lon'])
min_lon = min(gps_lat_all['lon'])


if(True):
	#print("\n---------- CREATE WEB MAP FILES --------------")

	#plt.hold(True)

	 
	a = antenna[ antenna['lon'] <= (max_lon+(margin_epsg4326*2)) ]
	a = a[ a['lon'] >= (min_lon-(margin_epsg4326*2)) ]
	a = a[ a['lat'] <= (max_lat+(margin_epsg4326*2)) ]
	a = a[ a['lat'] >= (min_lat-(margin_epsg4326*2)) ]

	# create a figure to draw map
	#map5 = plt.figure(figsize=(20,10))
	#ax1 = map5.add_subplot(1,1,1)

	# see if requested camera
	"""
	try:
		sel = int(args.y)
		# select draw GPS Latency
		if( sel < 6):
			print(" - GPS Latency web map for Camera {}".format(sel))
			fig, ax = drawWebMap(gps_lat_all, sel, a, tot_lat_col)
		else:
		# or selected draw PC Clock Latency
			sel = sel - 6
			print(" - PC Clock Latency web map for Camera {}".format(sel))
			fig, ax = drawWebMap(gps_lat_all, sel, a, net_lat_col)


	except: 
		print("Requested: "+args.y)
		sel = 5
		fig, ax = drawWebMap(gps_lat_all, sel, a, "sat")


	mplleaflet.show()	

	"""
	#name = "Greys"
	map5 = plt.figure(figsize=(20,10))
	map5ax1 = map5.add_subplot(1,1,1) #add_axes(rect)
	map5ax1.set_aspect('equal')
	try:
		sel = int(args.y)
		# if selected encoding latency
		if(sel < 10):
			col = 'encoding_latency'
			m = "Drawing Encoding Latency "
		# if selected network latency
		elif(sel < 20):
			col = 'network_latency'
			sel = sel - 10
			m = "Drawing Network Latency "
		# if selected total latency
		elif(sel < 30):
			col = 'total_latency'
			sel = sel - 20
			m = "Drawing Total Latency "
		else:
			print(" - Unexisting camera number.")

		#print("Selected camera: {}".format(sel))
		# verify if request a valid cam number

		# have to input camera ids for now
		if( sel > max([0,1,2,3,4,5]) ):
			m = m + "for All Cameras"
			data = gps_lat_all
		#if not will draw data for all cameras
		else:
			m = m + "for Camera {}".format(sel)
			#switcher = {0:gps_lat_cam0,1:gps_lat_cam1,2:gps_lat_cam2,3:gps_lat_cam3,4:gps_lat_cam4,5:gps_lat_cam5}
			#data = switcher.get(sel)
			
			if (sel == 0):
				data = gps_lat_cam0
			if (sel == 1):
				data = gps_lat_cam1
			if (sel == 2):
				data = gps_lat_cam2
			if (sel == 3):
				data = gps_lat_cam3
			if (sel == 4):
				data = gps_lat_cam4
			if (sel == 5):
				data = gps_lat_cam5
			
	except:
		print("Requested: "+args.y)
		col = "number_of_satellites"
		data = gps_lat_all
		m = "Drawing Satellite Count for All Cameras"

	print(m)

	data = data.sort_values(by=[col],ascending=False)
	colores = getColorMap(data[col])
	map5ax1.scatter(data['lon'], data['lat'], color = colores, s = s1, alpha = alpha)# ,edgecolors = "k", linewidths=0.5)
	map5ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)
	# highlight highest values by drawing them again
	max_lat = max(data[col])
	min_lat = min(data[col])
	lat34 = (max_lat-min_lat)*0.25
	highest = data[ data[col] > (max_lat - lat34)  ]
	# add lowest value just for the color map to be correct
	lowest = data[ data[col] == (min_lat)]
	highest = pd.concat([highest,lowest], ignore_index=True)
	highest = highest.sort_values(by=[col],ascending=False)
	#print(highest)
	colores = getColorMap(highest[col])		
	map5ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1*2, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

	mplleaflet.show()
	"""

	if(args.y == "5"):
		#name = "Greys"
		map5 = plt.figure(figsize=(20,10))
		map5ax1 = map5.add_subplot(1,1,1) #add_axes(rect)
		map5ax1.set_aspect('equal')
		print("Drawing Latency Map for All Cameras")
		gps_lat_all = gps_lat_all.sort_values(by=[tot_lat_col],ascending=False)
		colores = getColorMap(gps_lat_all[tot_lat_col])
		#map5ax1.scatter(gps_lat_all['lon'], gps_lat_all['lat'], color = "k", s = s1+2, alpha = alpha)#,edgecolors = "k", linewidths='3')
		map5ax1.scatter(gps_lat_all['lon'], gps_lat_all['lat'], color = colores, s = s1, alpha = alpha)# ,edgecolors = "k", linewidths=0.5)
		map5ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)
		#map5ax1.scatter(bc['lon'], bc['lat'], color = 'green', marker='*', s = s2)

		# highlight highest values by drawing them again
		max_lat = max(gps_lat_all[tot_lat_col])
		min_lat = min(gps_lat_all[tot_lat_col])
		lat34 = (max_lat-min_lat)*0.25
		highest = gps_lat_all[ gps_lat_all[tot_lat_col] > (max_lat - lat34)  ]
		# add lowest value just for the color map to be correct
		lowest = gps_lat_all[ gps_lat_all[tot_lat_col] == (min_lat)]
		highest = pd.concat([highest,lowest], ignore_index=True)
		highest = highest.sort_values(by=[tot_lat_col],ascending=False)
		#print(highest)
		colores = getColorMap(highest[tot_lat_col])		
		map5ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		mplleaflet.show()

	if(args.y == "0"):
		#name = "Purples"
		map0 = plt.figure(figsize=(20,10))
		map0ax1 = map0.add_subplot(1,1,1)
		map0ax1.set_aspect('equal')
		print("Drawing Latency Map for Camera 0")
		gps_lat_cam0 = gps_lat_cam0.sort_values(by=[tot_lat_col],ascending=False)
		colores = getColorMap(gps_lat_cam0[tot_lat_col])
		map0ax1.scatter(gps_lat_cam0['lon'], gps_lat_cam0['lat'], color = colores, s = s1, alpha = alpha)
		map0ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)

		# highlight highest values by drawing them again
		max_lat = max(gps_lat_all[tot_lat_col])
		min_lat = min(gps_lat_all[tot_lat_col])
		lat34 = (max_lat-min_lat)*0.25
		highest = gps_lat_all[ gps_lat_all[tot_lat_col] > (max_lat - lat34)  ]
		# add lowest value just for the color map to be correct
		lowest = gps_lat_all[ gps_lat_all[tot_lat_col] == (min_lat)]
		highest = pd.concat([highest,lowest], ignore_index=True)
		highest = highest.sort_values(by=[tot_lat_col],ascending=False)
		#print(highest)
		colores = getColorMap(highest[tot_lat_col])		
		map0ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		

		mplleaflet.show()

	if(args.y == "1"):
		#name = "Blues"
		map1 = plt.figure(figsize=(20,10))
		map1ax1 = map1.add_subplot(1,1,1)
		map1ax1.set_aspect('equal')
		print("Drawing Latency Map for Camera 1")
		gps_lat_cam1 = gps_lat_cam1.sort_values(by=[tot_lat_col],ascending=False)
		colores = getColorMap(gps_lat_cam1[tot_lat_col])
		map1ax1.scatter(gps_lat_cam1['lon'], gps_lat_cam1['lat'], color = colores, s = s1, alpha = alpha)
		map1ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)

		# highlight highest values by drawing them again
		max_lat = max(gps_lat_all[tot_lat_col])
		min_lat = min(gps_lat_all[tot_lat_col])
		lat34 = (max_lat-min_lat)*0.25
		highest = gps_lat_all[ gps_lat_all[tot_lat_col] > (max_lat - lat34)  ]
		# add lowest value just for the color map to be correct
		lowest = gps_lat_all[ gps_lat_all[tot_lat_col] == (min_lat)]
		highest = pd.concat([highest,lowest], ignore_index=True)
		highest = highest.sort_values(by=[tot_lat_col],ascending=False)
		#print(highest)
		colores = getColorMap(highest[tot_lat_col])		
		map1ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		

		mplleaflet.show()

	if(args.y == "2"):
		#name = "Greens"
		map2 = plt.figure(figsize=(20,10))
		map2ax1 = map2.add_subplot(1,1,1)
		map2ax1.set_aspect('equal')
		print("Drawing Latency Map for Camera 2")
		gps_lat_cam2 = gps_lat_cam2.sort_values(by=[tot_lat_col],ascending=False)
		colores = getColorMap(gps_lat_cam2[tot_lat_col])
		map2ax1.scatter(gps_lat_cam2['lon'], gps_lat_cam2['lat'], color = colores, s = s1, alpha = alpha)
		map2ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)

		# highlight highest values by drawing them again
		max_lat = max(gps_lat_all[tot_lat_col])
		min_lat = min(gps_lat_all[tot_lat_col])
		lat34 = (max_lat-min_lat)*0.25
		highest = gps_lat_all[ gps_lat_all[tot_lat_col] > (max_lat - lat34)  ]
		# add lowest value just for the color map to be correct
		lowest = gps_lat_all[ gps_lat_all[tot_lat_col] == (min_lat)]
		highest = pd.concat([highest,lowest], ignore_index=True)
		highest = highest.sort_values(by=[tot_lat_col],ascending=False)
		#print(highest)
		colores = getColorMap(highest[tot_lat_col])		
		map2ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		

		mplleaflet.show()

	if(args.y == "3"):
		#name = "BuPu"
		map3 = plt.figure(figsize=(20,10))
		map3ax1 = map3.add_subplot(1,1,1)
		map3ax1.set_aspect('equal')
		print("Drawing Latency Map for Camera 3")
		gps_lat_cam3 = gps_lat_cam3.sort_values(by=[tot_lat_col],ascending=False)
		colores = getColorMap(gps_lat_cam3[tot_lat_col])
		map3ax1.scatter(gps_lat_cam3['lon'], gps_lat_cam3['lat'], color = colores, s = s1, alpha = alpha)
		map3ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)

		# highlight highest values by drawing them again
		max_lat = max(gps_lat_all[tot_lat_col])
		min_lat = min(gps_lat_all[tot_lat_col])
		lat34 = (max_lat-min_lat)*0.25
		highest = gps_lat_all[ gps_lat_all[tot_lat_col] > (max_lat - lat34)  ]
		# add lowest value just for the color map to be correct
		lowest = gps_lat_all[ gps_lat_all[tot_lat_col] == (min_lat)]
		highest = pd.concat([highest,lowest], ignore_index=True)
		highest = highest.sort_values(by=[tot_lat_col],ascending=False)
		#print(highest)
		colores = getColorMap(highest[tot_lat_col])		
		map3ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		

		mplleaflet.show()

	if(args.y == "4"):
		#name = "YlGnBu"
		map4 = plt.figure(figsize=(20,10))
		map4ax1 = map4.add_subplot(1,1,1)
		map4ax1.set_aspect('equal')
		print("Drawing Latency Map for Camera 4")
		gps_lat_cam4 = gps_lat_cam4.sort_values(by=[tot_lat_col],ascending=False)
		colores = getColorMap(gps_lat_cam4[tot_lat_col])
		map4ax1.scatter(gps_lat_cam4['lon'], gps_lat_cam4['lat'], color = colores, s = s1, alpha = alpha)
		map4ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)

		# highlight highest values by drawing them again
		max_lat = max(gps_lat_all[tot_lat_col])
		min_lat = min(gps_lat_all[tot_lat_col])
		lat34 = (max_lat-min_lat)*0.25
		highest = gps_lat_all[ gps_lat_all[tot_lat_col] > (max_lat - lat34)  ]
		# add lowest value just for the color map to be correct
		lowest = gps_lat_all[ gps_lat_all[tot_lat_col] == (min_lat)]
		highest = pd.concat([highest,lowest], ignore_index=True)
		highest = highest.sort_values(by=[tot_lat_col],ascending=False)
		#print(highest)
		colores = getColorMap(highest[tot_lat_col])		
		map4ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		

		mplleaflet.show()

	if(args.y == "11"):
		#name = "Greys"
		map5 = plt.figure(figsize=(20,10))
		map5ax1 = map5.add_subplot(1,1,1) #add_axes(rect)
		map5ax1.set_aspect('equal')
		print("Drawing PC Latency Map for All Cameras")
		gps_lat_all = gps_lat_all.sort_values(by=[net_lat_col],ascending=False)
		colores = getColorMap(gps_lat_all[net_lat_col])
		#map5ax1.scatter(gps_lat_all['lon'], gps_lat_all['lat'], color = "k", s = s1+2, alpha = alpha)#,edgecolors = "k", linewidths='3')
		map5ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)	
		map5ax1.scatter(gps_lat_all['lon'], gps_lat_all['lat'], color = colores, s = s1, alpha = alpha)# ,edgecolors = "k", linewidths=0.5)
		
		# highlight highest values by drawing them again
		max_lat = max(gps_lat_all[net_lat_col])
		min_lat = min(gps_lat_all[net_lat_col])
		lat34 = (max_lat-min_lat)*0.25
		highest = gps_lat_all[ gps_lat_all[net_lat_col] > (max_lat - lat34)  ]
		# add lowest value just for the color map to be correct
		lowest = gps_lat_all[ gps_lat_all[net_lat_col] == (min_lat)]
		highest = pd.concat([highest,lowest], ignore_index=True)
		highest = highest.sort_values(by=[net_lat_col],ascending=False)
		#print(highest)
		colores = getColorMap(highest[net_lat_col])		
		map5ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		

		#map5ax1.scatter(bc['lon'], bc['lat'], color = 'green', marker='*', s = s2)
		mplleaflet.show()

	if(args.y == "6"):
		#name = "Purples"
		map0 = plt.figure(figsize=(20,10))
		map0ax1 = map0.add_subplot(1,1,1)
		map0ax1.set_aspect('equal')
		print("Drawing PC  Latency Map for Camera 0")
		gps_lat_cam0 = gps_lat_cam0.sort_values(by=[net_lat_col],ascending=False)
		colores = getColorMap(gps_lat_cam0[net_lat_col])
		map0ax1.scatter(gps_lat_cam0['lon'], gps_lat_cam0['lat'], color = colores, s = s1, alpha = alpha)
		map0ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)

		# highlight highest values by drawing them again
		max_lat = max(gps_lat_all[net_lat_col])
		min_lat = min(gps_lat_all[net_lat_col])
		lat34 = (max_lat-min_lat)*0.25
		highest = gps_lat_all[ gps_lat_all[net_lat_col] > (max_lat - lat34)  ]
		# add lowest value just for the color map to be correct
		lowest = gps_lat_all[ gps_lat_all[net_lat_col] == (min_lat)]
		highest = pd.concat([highest,lowest], ignore_index=True)
		highest = highest.sort_values(by=[net_lat_col],ascending=False)
		#print(highest)
		colores = getColorMap(highest[net_lat_col])		
		map0ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		


		mplleaflet.show()

	if(args.y == "7"):
		#name = "Blues"
		map1 = plt.figure(figsize=(20,10))
		map1ax1 = map1.add_subplot(1,1,1)
		map1ax1.set_aspect('equal')
		print("Drawing PC  Latency Map for Camera 1")
		gps_lat_cam1 = gps_lat_cam1.sort_values(by=[net_lat_col],ascending=False)
		colores = getColorMap(gps_lat_cam1[net_lat_col])
		map1ax1.scatter(gps_lat_cam1['lon'], gps_lat_cam1['lat'], color = colores, s = s1, alpha = alpha)
		map1ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)
		
		# highlight highest values by drawing them again
		max_lat = max(gps_lat_all[net_lat_col])
		min_lat = min(gps_lat_all[net_lat_col])
		lat34 = (max_lat-min_lat)*0.25
		highest = gps_lat_all[ gps_lat_all[net_lat_col] > (max_lat - lat34)  ]
		# add lowest value just for the color map to be correct
		lowest = gps_lat_all[ gps_lat_all[net_lat_col] == (min_lat)]
		highest = pd.concat([highest,lowest], ignore_index=True)
		highest = highest.sort_values(by=[net_lat_col],ascending=False)
		#print(highest)
		colores = getColorMap(highest[net_lat_col])		
		map1ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		mplleaflet.show()

	if(args.y == "8"):
		#name = "Greens"
		map2 = plt.figure(figsize=(20,10))
		map2ax1 = map2.add_subplot(1,1,1)
		map2ax1.set_aspect('equal')
		print("Drawing PC  Latency Map for Camera 2")
		gps_lat_cam2 = gps_lat_cam2.sort_values(by=[net_lat_col],ascending=False)
		colores = getColorMap(gps_lat_cam2[net_lat_col])
		map2ax1.scatter(gps_lat_cam2['lon'], gps_lat_cam2['lat'], color = colores, s = s1, alpha = alpha)
		map2ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)
		
		# highlight highest values by drawing them again
		max_lat = max(gps_lat_all[net_lat_col])
		min_lat = min(gps_lat_all[net_lat_col])
		lat34 = (max_lat-min_lat)*0.25
		highest = gps_lat_all[ gps_lat_all[net_lat_col] > (max_lat - lat34)  ]
		# add lowest value just for the color map to be correct
		lowest = gps_lat_all[ gps_lat_all[net_lat_col] == (min_lat)]
		highest = pd.concat([highest,lowest], ignore_index=True)
		highest = highest.sort_values(by=[net_lat_col],ascending=False)
		#print(highest)
		colores = getColorMap(highest[net_lat_col])		
		map2ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		mplleaflet.show()

	if(args.y == "9"):
		#name = "BuPu"
		map3 = plt.figure(figsize=(20,10))
		map3ax1 = map3.add_subplot(1,1,1)
		map3ax1.set_aspect('equal')
		print("Drawing PC  Latency Map for Camera 3")
		gps_lat_cam3 = gps_lat_cam3.sort_values(by=[net_lat_col],ascending=False)
		colores = getColorMap(gps_lat_cam3[net_lat_col])
		map3ax1.scatter(gps_lat_cam3['lon'], gps_lat_cam3['lat'], color = colores, s = s1, alpha = alpha)
		map3ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)
		
		# highlight highest values by drawing them again
		max_lat = max(gps_lat_all[net_lat_col])
		min_lat = min(gps_lat_all[net_lat_col])
		lat34 = (max_lat-min_lat)*0.25
		highest = gps_lat_all[ gps_lat_all[net_lat_col] > (max_lat - lat34)  ]
		# add lowest value just for the color map to be correct
		lowest = gps_lat_all[ gps_lat_all[net_lat_col] == (min_lat)]
		highest = pd.concat([highest,lowest], ignore_index=True)
		highest = highest.sort_values(by=[net_lat_col],ascending=False)
		#print(highest)
		colores = getColorMap(highest[net_lat_col])		
		map3ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		
		mplleaflet.show()

	if(args.y == "10"):
		#name = "YlGnBu"
		map4 = plt.figure(figsize=(20,10))
		map4ax1 = map4.add_subplot(1,1,1)
		map4ax1.set_aspect('equal')
		print("Drawing PC  Latency Map for Camera 4")
		gps_lat_cam4 = gps_lat_cam4.sort_values(by=[net_lat_col],ascending=False)
		colores = getColorMap(gps_lat_cam4[net_lat_col])
		map4ax1.scatter(gps_lat_cam4['lon'], gps_lat_cam4['lat'], color = colores, s = s1, alpha = alpha)
		map4ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)
		
		# highlight highest values by drawing them again
		max_lat = max(gps_lat_all[net_lat_col])
		min_lat = min(gps_lat_all[net_lat_col])
		lat34 = (max_lat-min_lat)*0.25
		highest = gps_lat_all[ gps_lat_all[net_lat_col] > (max_lat - lat34)  ]
		# add lowest value just for the color map to be correct
		lowest = gps_lat_all[ gps_lat_all[net_lat_col] == (min_lat)]
		highest = pd.concat([highest,lowest], ignore_index=True)
		highest = highest.sort_values(by=[net_lat_col],ascending=False)
		#print(highest)
		colores = getColorMap(highest[net_lat_col])		
		map4ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		mplleaflet.show()		

	if(args.y == "sat"):
		#name = "YlGnBu"
		map4 = plt.figure(figsize=(20,10))
		map4ax1 = map4.add_subplot(1,1,1)
		map4ax1.set_aspect('equal')
		print("Drawing Satellite Map")
		gps_lat_all = gps_lat_all.sort_values(by=['sat'],ascending=False)
		colores = getColorMap(gps_lat_cam4['sat'])
		map4ax1.scatter(gps_lat_cam4['lon'], gps_lat_cam4['lat'], color = colores, s = s1, alpha = alpha)
		map4ax1.scatter(a['lon'], a['lat'], color = 'blue', marker='^', s = s2)
		
		
		# highlight highest values by drawing them again
		#max_lat = max(gps_lat_all[net_lat_col])
		#min_lat = min(gps_lat_all[net_lat_col])
		#lat34 = (max_lat-min_lat)*0.25
		#highest = gps_lat_all[ gps_lat_all[net_lat_col] > (max_lat - lat34)  ]
		## add lowest value just for the color map to be correct
		#lowest = gps_lat_all[ gps_lat_all[net_lat_col] == (min_lat)]
		#highest = pd.concat([highest,lowest], ignore_index=True)
		#highest = highest.sort_values(by=[net_lat_col],ascending=False)
		##print(highest)
		#colores = getColorMap(highest[net_lat_col])		
		#map4ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)
		
		mplleaflet.show()		
	"""
	
	#mplleaflet.show()
	# show Graphs in screen
	#plt.show()

	plt.close('all')


