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
s1 = 40         # track marker size
s2 = 6.0        # antenna marker size
alpha = 0.7     # transparency


opt = la.opt

if(opt == 0):
	lat_col = 'min_latency'
	pc_lat_col = 'min_pc_latency'
if(opt == 1):
	lat_col = 'avg_latency'
	pc_lat_col = 'avg_pc_latency'
if(opt == 2):
	lat_col = 'max_latency'
	pc_lat_col = 'max_pc_latency'

#print(lat_col)
#print(pc_lat_col)

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
	ticks = np.linspace(latency_min, latency_max, 6)
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


	plt.close('all')


margin = 500.0
margin_epsg4326 = 0.005
max_lat = max(gps_lat_all['lat'])
min_lat = min(gps_lat_all['lat'])
max_lon = max(gps_lat_all['lon'])
min_lon = min(gps_lat_all['lon'])


if(True):
	print("\n---------- CREATE WEB MAP FILES --------------")

	#plt.hold(True)

	 
	a = antenna[ antenna['lon'] <= (max_lon+(margin_epsg4326*2)) ]
	a = a[ a['lon'] >= (min_lon-(margin_epsg4326*2)) ]
	a = a[ a['lat'] <= (max_lat+(margin_epsg4326*2)) ]
	a = a[ a['lat'] >= (min_lat-(margin_epsg4326*2)) ]

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
		#print(highest)
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
		#print(highest)
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
		#print(highest)
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
		#print(highest)
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
		#print(highest)
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
		#print(highest)
		colores = getColorMap(highest[lat_col])		
		map4ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		

		mplleaflet.show()

	if(args.y == "11"):
		#name = "Greys"
		map5 = plt.figure(figsize=(20,10))
		map5ax1 = map5.add_subplot(1,1,1) #add_axes(rect)
		map5ax1.set_aspect('equal')
		print("Drawing PC Latency Map for All Cameras")
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
		#print(highest)
		colores = getColorMap(highest[pc_lat_col])		
		map5ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		

		#map5ax1.scatter(bc['lon'], bc['lat'], color = 'green', marker='*', s = s2)
		mplleaflet.show()

	if(args.y == "6"):
		#name = "Purples"
		map0 = plt.figure(figsize=(20,10))
		map0ax1 = map0.add_subplot(1,1,1)
		map0ax1.set_aspect('equal')
		print("Drawing PC  Latency Map for Camera 0")
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
		#print(highest)
		colores = getColorMap(highest[pc_lat_col])		
		map0ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		


		mplleaflet.show()

	if(args.y == "7"):
		#name = "Blues"
		map1 = plt.figure(figsize=(20,10))
		map1ax1 = map1.add_subplot(1,1,1)
		map1ax1.set_aspect('equal')
		print("Drawing PC  Latency Map for Camera 1")
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
		#print(highest)
		colores = getColorMap(highest[pc_lat_col])		
		map1ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		mplleaflet.show()

	if(args.y == "8"):
		#name = "Greens"
		map2 = plt.figure(figsize=(20,10))
		map2ax1 = map2.add_subplot(1,1,1)
		map2ax1.set_aspect('equal')
		print("Drawing PC  Latency Map for Camera 2")
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
		#print(highest)
		colores = getColorMap(highest[pc_lat_col])		
		map2ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		mplleaflet.show()

	if(args.y == "9"):
		#name = "BuPu"
		map3 = plt.figure(figsize=(20,10))
		map3ax1 = map3.add_subplot(1,1,1)
		map3ax1.set_aspect('equal')
		print("Drawing PC  Latency Map for Camera 3")
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
		#print(highest)
		colores = getColorMap(highest[pc_lat_col])		
		map3ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)

		
		mplleaflet.show()

	if(args.y == "10"):
		#name = "YlGnBu"
		map4 = plt.figure(figsize=(20,10))
		map4ax1 = map4.add_subplot(1,1,1)
		map4ax1.set_aspect('equal')
		print("Drawing PC  Latency Map for Camera 3")
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
		#print(highest)
		colores = getColorMap(highest[pc_lat_col])		
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
		
		"""
		# highlight highest values by drawing them again
		max_lat = max(gps_lat_all[pc_lat_col])
		min_lat = min(gps_lat_all[pc_lat_col])
		lat34 = (max_lat-min_lat)*0.25
		highest = gps_lat_all[ gps_lat_all[pc_lat_col] > (max_lat - lat34)  ]
		# add lowest value just for the color map to be correct
		lowest = gps_lat_all[ gps_lat_all[pc_lat_col] == (min_lat)]
		highest = pd.concat([highest,lowest], ignore_index=True)
		highest = highest.sort_values(by=[pc_lat_col],ascending=False)
		#print(highest)
		colores = getColorMap(highest[pc_lat_col])		
		map4ax1.scatter(highest['lon'], highest['lat'], color = colores, s = s1+25, alpha = 1.0)# ,edgecolors = "k", linewidths=0.5)
		"""
		mplleaflet.show()		

	#mplleaflet.show()
	# show Graphs in screen
	#plt.show()

	plt.close('all')


