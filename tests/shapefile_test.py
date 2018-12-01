# using shape files in python
# 
import geopandas as gpd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd


buildings = gpd.read_file("../maps/buildings/Buildings_University2.geojson")
admin = gpd.read_file('../maps/seoul_south-korea.imposm-geojson/seoul_south-korea_admin.geojson')
print(buildings.shape)

#buildings = buildings[ buildings['HEIGHT'] > 0.0 ]
print(buildings.shape)

bcents = buildings.centroid
print(bcents.head())
#bcents = pd.Series(bcents)
#print(bcents.head())
buildings["x"] = buildings.centroid.map(lambda p: p.x)
buildings["y"] = buildings.centroid.map(lambda p: p.y)

df = pd.DataFrame()
df['x'] = buildings["x"]
df['y'] = buildings["y"]
print (df.head())

# set the EPSG4004 Coordinate Reference System of the data 
#buildings.crs = {'init' :'epsg:4004'}
# and reproject to latitude longitude
#buildings.to_crs({'init' :'epsg:4326'})

# create a window to graph
bmap = plt.figure(figsize=(20,10))
bax = bmap.add_subplot(1,1,1)
buildings.plot(ax = bax, color = 'blue', alpha = 0.8)
admin.plot(ax=bax, color='white', edgecolor='black',alpha = 0.5)
#bcents.plot(ax=bax, color='red')

plt.show()
#mplleaflet.show()
