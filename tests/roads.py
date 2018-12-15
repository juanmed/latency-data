import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


roads = gpd.read_file('../maps/seoul_south-korea.imposm-geojson/seoul_south-korea_roads.geojson')
print(roads.head(1))

roads.plot()

plt.show()