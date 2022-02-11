import matplotlib.pyplot as plt
import numpy as np
import argparse
import os, sys
import glob
import rasterio
from rasterio.plot import show as rasterplot
import geopandas

# download the sample tiff files next to this file
# https://drive.google.com/file/d/1LJQ8ekzZM8NBdhvyDSK0O6UiBf-uTGFt/view?usp=sharing

if __name__ == "__main__":
    """
    Main function for executing the .py script.
    Command:
        -p path/<filename>.npy
    """
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str, default='.',
                    help="path to dir")
    ap.add_argument("-b", "--band", type=int, default=2,
                    help="path to dir")
    args = vars(ap.parse_args())

    fig, ax = plt.subplots()

    '''
    for dir in [x[0] for x in os.walk(args["path"])][1:]: # visit each sub dir
        print(dir)

        # look for tiff files in each sub dir
        tiff_files = glob.glob(os.path.join(dir,"*.tiff"))

        #plot the first tiff file
        raster = rasterio.open(tiff_files[1])
        rasterplot((raster,args["band"]), ax=ax)

        print("region {}".format(raster.bounds))
        print("number of bands {}".format(raster.count))
        selected_band = raster.read(args["band"]) # numpy array
        print(selected_band.shape)
        print("band min {}, max {}".format(np.min(selected_band),np.max(selected_band)))
    '''
    # plot outline of jylland
    jylland = geopandas.read_file(os.path.join(args["path"],'jylland.geojson'))
    jylland.plot(ax=ax, facecolor='none', edgecolor='r')

    plt.show()
