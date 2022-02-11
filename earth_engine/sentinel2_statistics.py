import ee
ee.Initialize()
import geemap
import os
import numpy as np
import csv

# Read the csv file with regions of interest
path = os.path.join(os.path.expanduser('~'), 'Downloads/EE/statistics/10km_sample.csv')
regions = np.genfromtxt(path, delimiter=',', dtype='str', skip_header=1)

# Define a header for csv files that will collect the statistics
header=['region id', 'cloud coverage', 'date start', 'date end', 'number of images']

# Define a projection from a default Earth Engine EPSG to the EPSG of the coodrinates listed in 10_km.csv
proj=ee.Projection('EPSG:25832')

# List the bands of interest
band_list = ['B1','B2','B3','B4','B5','B6','B7','B8','B8A','B9','B11','B12']

# Define a time period for which to collect the statistics
dates=geemap.date_sequence(start='2018-01-01',end='2021-01-01',unit='month')
dates_size=dates.size().getInfo()

# Define desired levels of cloud coverage in percentage. These are later used to construct a filter
cloud_coverage=[10,20,30,40,50,75]

for region in regions:
    # Read the id, and the coordinates of the ROI
    id = int(region[0])
    x_min, x_max = float(region[2]), float(region[4])
    y_min, y_max = float(region[3]), float(region[5])
    # Create a bounding box based on the coordinates of the ROI
    # IMPORTANT - do not change True and False at the end, it will break the code
    bbox = ee.Geometry.Rectangle([x_min,y_min,x_max,y_max],proj, True, False)

    for coverage in cloud_coverage:
        # Construct a filter based on the
        filterCloudCoverage = ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', coverage)

        # Define where to save the csv file, then open it and write in the header
        path_out = os.path.join(os.path.expanduser('~'), 'Downloads/EE/statistics/statistics-'+str(id)+'-'+str(coverage)+'.csv')
        f = open(path_out, 'w', newline='')
        writer = csv.writer(f)
        writer.writerow(header)

        for i in range(dates_size-1):
            # Filter the image collection
            col = ee.ImageCollection('COPERNICUS/S2_SR') \
                .filterBounds(bbox) \
                .filterDate(dates.getString(i).getInfo(), dates.getString(i+1).getInfo()) \
                .select(band_list) \
                .filter(filterCloudCoverage)
            col_size=col.size().getInfo()

            print(' region id ', id,
                  ' cloud coverage ', coverage,
                  ' date start ', dates.getString(i).getInfo(),
                  ' date end ', dates.getString(i+1).getInfo(),
                  ' number of images ', col_size)
            # Write the collected statistics into the csv file
            row=[id, coverage, dates.getString(i).getInfo(), dates.getString(i+1).getInfo(), col_size]
            writer.writerow(row)
        f.close()




