import os
import argparse
import numpy as np
import concurrent.futures
import geemap
import ee

# Initialize connection with the earth engine servers
ee.Initialize()


# Function to download each image in the collection. Takes an image name as the input.
def get_bands(image_name, epsg='EPSG:25832'):
    print('Starting a Band thread')
    image = ee.Image(image_name).select(band_list)
    name = image.get("system:index").getInfo() + ".tif"
    filename = os.path.join(os.path.abspath(out_dir_Bands), name)
    geemap.ee_export_image(image,
                           filename=filename,
                           scale=10,
                           crs=epsg,
                           region=bbox,
                           file_per_band=False)
    print('Killing a Band thread')


# Same as get_band() but downloads RGB bands of an input image
def get_rgb(image_name, epsg='EPSG:25832'):
    print('Starting an RGB thread')
    image = ee.Image(image_name).select(RGB)
    name = image.get("system:index").getInfo() + ".tif"
    filename = os.path.join(os.path.abspath(out_dir_RGB), name)
    geemap.ee_export_image(image,
                           filename=filename,
                           scale=10,
                           crs=epsg,
                           region=bbox,
                           file_per_band=False)
    print('Killing an RGB thread')


# Function to download missing images.
# This is done by comparing images in the folder with the list of images from the metadata.
def download_missing(metadata, number_of_files_from_metadata, directory, download_type, num_workers):
    downloaded_all = False
    print('Downloading missing files')

    _, _, files = next(os.walk(directory))
    while not downloaded_all:
        missing_files = []
        for entry in metadata:
            image_name = entry
            entry = entry[17:] + '.tif'
            if entry not in files:
                missing_files.append(image_name)

        # print(len(missing_files))
        if download_type == 'rgb':
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                executor.map(get_rgb, missing_files)
        elif download_type == 'bands':
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                executor.map(get_bands, missing_files)
        else:
            print('Download missing failed, wrong download type')

        _, _, files = next(os.walk(directory))
        number_of_files_in_folder = len(files) - 1
        if number_of_files_in_folder == number_of_files_from_metadata:
            downloaded_all = True


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
    ap.add_argument("-o", "--output_dir", type=str, default='/media/markpp/Storage/datasets/other/Skagerak/Sentinel2', help="Path to output directory")
    ap.add_argument("-d", "--dataset", type=str, default='COPERNICUS/S2_SR', help="Specify which dataset to download 'COPERNICUS/S2_SR'")
    ap.add_argument("-e", "--epsg", type=str, default='EPSG:25832', help="Specify the EPSG code") # https://epsg.io/25832
    ap.add_argument("-i", "--last_id", type=int, default=0, help="Select which tile id to start from")
    ap.add_argument("-n", "--num_workers", type=int, default=4, help="Set number of workers")

    args = vars(ap.parse_args())

    out_dir = args['output_dir']
    # out_dir = '/media/markpp/Seagate Expansion Drive/Sentinel2/2019/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Define a time period you would like to download
    beginning, end = args['period'].split(':')
    dates = geemap.date_sequence(start=beginning, end=end, unit='week')
    dates_size = dates.size().getInfo()

    # Path to the csv file with regions of interest
    regions = np.genfromtxt(args['tiles'], delimiter=',', dtype='str', skip_header=1)

    # Define a time period you would like to download
    dates = geemap.date_sequence(start='2017-01-01', end='2018-01-01', unit='month')
    dates_size = dates.size().getInfo()

    #'''
    # Identify the last initiated region id
    _, id_folders, _ = next(os.walk(out_dir))
    if id_folders:
        ids = []
        for folder in id_folders:
            ids.append(int(folder))
        sorted_ids = sorted(ids)
        args['last_id'] = sorted_ids[-1]
    else:
        args['last_id'] = 0
    #'''

    # Define a projection from a default Earth Engine EPSG to the EPSG of the coordinates listed in tiles.csv
    proj = ee.Projection(args["epsg"])

    # Selection of bands to download
    band_list = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12']
    # Visualisation bands
    RGB = ['TCI_R', 'TCI_G', 'TCI_B']

    # Loop through the regions, define the ROI of this iteration, bbox variable, using the coordinates from the 10km.csv
    # Use the last found id as a starting point
    for region in regions[args['last_id']:]:
        # Initialize connection to the earth engine servers in order to prevent connection timeout
        ee.Initialize()
        id = int(region[0])
        print('Downloading region ', id)
        x_min, x_max = float(region[2]), float(region[4])
        y_min, y_max = float(region[3]), float(region[5])
        bbox = ee.Geometry.Rectangle([x_min, y_min, x_max, y_max], proj, True, False)

        # Set the output directories for images and metadata files
        out_dir_RGB = os.path.join(out_dir, str(id) + '/rgb')
        if not os.path.exists(out_dir_RGB):
            os.makedirs(out_dir_RGB)

        out_dir_Bands = os.path.join(out_dir, str(id) + '/bands')
        if not os.path.exists(out_dir_Bands):
            os.makedirs(out_dir_Bands)

        metadata_dir_Bands = os.path.join(out_dir_Bands, 'metadata.csv')
        metadata_dir_RGB = os.path.join(out_dir_RGB, 'metadata.csv')

        # Create an image collection. Filter by the region and the time period
        col = ee.ImageCollection(args['dataset']) \
            .filterBounds(bbox) \
            .filterDate(dates.getString(0).getInfo(), dates.getString(dates_size - 1).getInfo())
        # Split the collection in two. One with for multi-spectral images, col_Bands, one for RGB images, col_RGB
        col_Bands = col.select(band_list)
        col_RGB = col.select(RGB)

        # Create metadata for both image collections
        feature_col_Bands = ee.FeatureCollection(col_Bands)
        feature_col_RGB = ee.FeatureCollection(col_RGB)
        geemap.ee_to_csv(feature_col_Bands, filename=metadata_dir_Bands)
        geemap.ee_to_csv(feature_col_RGB, filename=metadata_dir_RGB)
        metadata_Bands = np.genfromtxt(metadata_dir_Bands, delimiter=',', dtype='str', skip_header=1, usecols=4)
        metadata_RGB = np.genfromtxt(metadata_dir_RGB, delimiter=',', dtype='str', skip_header=1, usecols=4)

        # Run the multithreading. Assign each image in the collection its own download thread.
        # First, download multi-spectal images, then RGB
        with concurrent.futures.ThreadPoolExecutor(max_workers=args['num_workers']) as executor:
            executor.map(get_bands, metadata_Bands)
            executor.map(get_rgb, metadata_RGB)

        # Here starts the AFTER-DOWNLOAD CLEANUP
        # Parse the metadata to figure out how many images are supposed to be in a region folder.
        number_of_files_metadata_Bands = len(metadata_Bands)
        number_of_files_metadata_RGB = len(metadata_RGB)
        _, _, files_Bands = next(os.walk(out_dir_Bands))
        _, _, files_RGB = next(os.walk(out_dir_RGB))
        number_of_files_in_Bands = len(files_Bands) - 1
        number_of_files_in_RGB = len(files_RGB) - 1

        # Log how many files have downloaded
        with open(os.path.join(out_dir, 'log.txt'), 'a') as f:
            line = 'Region id-' + str(id) + ' -- ' \
                   + str(number_of_files_in_Bands) + '/' \
                   + str(number_of_files_in_RGB) + '/' \
                   + str(number_of_files_metadata_RGB) + '\n'
            f.write(line)

        # Compare the number of images. If not equal, download missing
        if number_of_files_in_RGB != number_of_files_metadata_RGB or number_of_files_in_Bands != number_of_files_metadata_Bands:
            with open(os.path.join(out_dir, 'log.txt'), 'a') as f:
                line = 'Region id-' + str(id) + ' has not downloaded successfully. Check for missing files.\n'
                f.write(line)

            download_missing(metadata_Bands, number_of_files_metadata_Bands, out_dir_Bands, 'bands', num_workers=args['num_workers'])
            download_missing(metadata_RGB, number_of_files_metadata_RGB, out_dir_RGB, 'rgb', num_workers=args['num_workers'])

            _, _, files_Bands = next(os.walk(out_dir_Bands))
            _, _, files_RGB = next(os.walk(out_dir_RGB))
            number_of_files_in_Bands = len(files_Bands) - 1
            number_of_files_in_RGB = len(files_RGB) - 1

            # Log how many images are in the folder after missing files have been downloaded.
            # In theory, this part will not even run until all the missing files have been downloaded.
            with open(os.path.join(out_dir, 'log.txt'), 'a') as f:
                line = 'Region id-' + str(id) + ' -- ' \
                       + str(number_of_files_in_Bands) + '/' \
                       + str(number_of_files_in_RGB) + '/' \
                       + str(number_of_files_metadata_RGB) + '\n'
                f.write(line)

        # Clean up files that are smaller than 1 500 000 bytes. This will remove corrupted and mostly cloud images.
        _, _, files_Bands = next(os.walk(out_dir_Bands))
        _, _, files_RGB = next(os.walk(out_dir_RGB))
        for f in files_RGB:
            if f == 'metadata.csv':
                continue
            file_RGB = os.path.join(out_dir_RGB, f)
            file_Bands = os.path.join(out_dir_Bands, f)
            file_size = os.path.getsize(file_RGB)
            if file_size < 1_500_000:
                os.remove(file_RGB)
                os.remove(file_Bands)





