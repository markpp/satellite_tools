# Google Earth Engine
GEE is by far the most user friendly and stable api for acquiring satellite data (that doesn't say a lot btw). 

# Deps
Mainly: pip3 install geopandas sentinelhub shapely tifffile earthengine-api geemap

# Usage

1. Specify a region of interest in the geojson format. An easy solution is https://geojson.io/

2. Convert the roi into nice tiles of the desired size. This can be done using roi2tiles.py. the resulting tiles are stored in tiles.csv.

3. Start downloading the tiles using either the sentinel1 or 2 download scripts (sentinel2 scripts seems to be broken not sure why). Data is downloaded between a start and end date specifed in the download script. E.g. dateStart = '2018-01-01' and dateEnd = '2018-12-31' for all of 2018. 
Unless you have TBs of storage make sure to limit the time span and the size of the region of interest.


