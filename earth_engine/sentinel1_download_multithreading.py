import os
from datetime import datetime
import numpy as np
import concurrent.futures
import argparse
import geemap
import ee

# Initialize connection with the earth engine servers
ee.Initialize()


# Function to download each image in the collection. Takes an image name as the input.
def get_bands_asc(image_name):
    print('Starting a download thread')
    image = ee.Image(image_name)
    # [17:46]
    name = image.get("system:index").getInfo() + ".tif"
    filename = os.path.join(os.path.abspath(out_dir_asc), name)
    geemap.ee_export_image(image,
                           filename=filename,
                           scale=10,
                           crs='EPSG:25832',
                           region=bbox,
                           file_per_band=False)
    time_now = datetime.now()
    print('Killing a download thread', time_now)


def get_bands_des(image_name):
    print('Starting a download thread')
    image = ee.Image(image_name)
    name = image.get("system:index").getInfo() + ".tif"
    filename = os.path.join(os.path.abspath(out_dir_des), name)
    geemap.ee_export_image(image,
                           filename=filename,
                           scale=10,
                           crs='EPSG:25832',
                           region=bbox,
                           file_per_band=False)
    time_now = datetime.now()
    print('Killing a download thread', time_now)

if __name__ == "__main__":
    """
    Main function for executing the .py script.
    Command:
        -t path/<filename>.csv
    """
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--tiles", type=str, default='tiles.csv', help="Path to tiles.csv")
    ap.add_argument("-p", "--period", type=str, default='2019-01-01:2019-02-01', help="Path to tiles.csv")
    ap.add_argument("-o", "--output_dir", type=str, default='/media/markpp/Storage/datasets/other/Skagerak/Sentinel1', help="Path to output directory")
    ap.add_argument("-d", "--dataset", type=str, default='COPERNICUS/S1_GRD', help="Specify which dataset to download 'COPERNICUS/S1_GRD' or COPERNICUS/S1_GRD_FLOAT'")
    ap.add_argument("-e", "--epsg", type=str, default='EPSG:25832', help="Specify the EPSG code") # https://epsg.io/25832
    ap.add_argument("-i", "--last_id", type=int, default=0, help="Select which tile id to start from")
    ap.add_argument("-n", "--num_workers", type=int, default=4, help="Set number of workers")

    args = vars(ap.parse_args())

    if args['dataset'] == 'COPERNICUS/S1_GRD_FLOAT':
        system_id_col = 6
    elif args['dataset'] == 'COPERNICUS/S1_GRD':
        system_id_col = 0
    else:
        print("Not a recognized dataset")

    out_dir = args['output_dir']
    # out_dir = '/media/markpp/Seagate Expansion Drive/Sentinel1/2019/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Define a time period you would like to download
    beginning, end = args['period'].split(':')
    dates = geemap.date_sequence(start=beginning, end=end, unit='week')
    dates_size = dates.size().getInfo()

    # Path to the csv file with regions of interest
    regions = np.genfromtxt(args['tiles'], delimiter=',', dtype='str', skip_header=1)

    # Automatically identify the last initiated region id
    """
    _, id_folders, _ = next(os.walk(out_dir))
    if id_folders:
        ids = []
        for folder in id_folders:
            ids.append(int(folder))
        sorted_ids = sorted(ids)
        last_id = sorted_ids[-1]
    else:
        last_id = 0
    """

    # Define a projection from a default Earth Engine EPSG to the EPSG of the coordinates listed in tiles.csv
    proj = ee.Projection(args["epsg"])

    # Loop through the regions, define the ROI of this iteration, bbox variable, using the coordinates from the tiles.csv
    # Use the last found id as a starting point
    for region in regions[args["last_id"]:]:
        # Initialize connection to the earth engine servers in order to prevent connection timeout
        ee.Initialize()
        id = int(region[0])
        print('Downloading region ', id)
        x_min, x_max = float(region[2]), float(region[4])
        y_min, y_max = float(region[3]), float(region[5])
        bbox = ee.Geometry.Rectangle([x_min, y_min, x_max, y_max], proj, True, False)

        # Set the output directory for images
        out_dir_asc = os.path.join(out_dir, str(id) + "/asc")
        if not os.path.exists(out_dir_asc):
            os.makedirs(out_dir_asc)

        out_dir_des = os.path.join(out_dir, str(id) + "/des")
        if not os.path.exists(out_dir_des):
            os.makedirs(out_dir_des)

        # Set the output directory for a metadata of a collection
        metadata_dir_asc = os.path.join(out_dir_asc, 'metadata.csv')
        metadata_dir_des = os.path.join(out_dir_des, 'metadata.csv')

        # Create an image collection. Filter by the region and the time period
        #.filter(ee.Filter.eq('instrumentMode', 'IW'))
        col = ee.ImageCollection(args['dataset'])\
            .filterBounds(bbox)\
            .filterDate(dates.getString(0).getInfo(), dates.getString(dates_size-1).getInfo())

        col_asc = col.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
        col_des = col.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))

        # Create the metadata for the collection
        feature_col_asc = ee.FeatureCollection(col_asc)
        geemap.ee_to_csv(feature_col_asc, filename=metadata_dir_asc)
        metadata_asc = np.genfromtxt(metadata_dir_asc, delimiter=',', dtype='str', skip_header=1, usecols=system_id_col)
        feature_col_des = ee.FeatureCollection(col_des)
        geemap.ee_to_csv(feature_col_des, filename=metadata_dir_des)
        metadata_des = np.genfromtxt(metadata_dir_des, delimiter=',', dtype='str', skip_header=1, usecols=system_id_col)

        # Run the multithreading. Assign each image in the collection its own download thread.
        with concurrent.futures.ThreadPoolExecutor(max_workers=args["num_workers"]) as executor:
            executor.map(get_bands_asc, metadata_asc)
            executor.map(get_bands_des, metadata_des)

        # Parse the metadata to figure out how many images are supposed to be in a region folder.
        number_of_files_metadata_asc = len(metadata_asc)
        _, _, files_asc = next(os.walk(out_dir_asc))
        number_of_files_in_asc = len(files_asc) - 1

        number_of_files_metadata_des = len(metadata_des)
        _, _, files_des = next(os.walk(out_dir_des))
        number_of_files_in_des = len(files_des) - 1

        # Log how many files have downloaded
        with open(os.path.join(out_dir, 'log.txt'), 'a') as f:
            line = 'Region id-' + str(id) + ' -- ASC ' \
                + str(number_of_files_in_asc) + '/' \
                + str(number_of_files_metadata_asc) + '/' \
                + ' DES ' + str(number_of_files_in_des) + '/' \
                + str(number_of_files_metadata_des) + '\n'
            f.write(line)
