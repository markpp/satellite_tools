import numpy as np
import argparse
import os, sys
import glob
import tifffile as tf # documentation: https://github.com/cgohlke/tifffile
import cv2
# download the sample tiff files next to this file
# https://drive.google.com/file/d/1LJQ8ekzZM8NBdhvyDSK0O6UiBf-uTGFt/view?usp=sharing

def read_tif_dir(dir):
    # look for tiff files in each sub dir
    tiff_files = sorted(glob.glob(os.path.join(dir,"*UNG.tif")))

    for tiff_file in tiff_files[:]:
        if os.path.getsize(tiff_file) > 1_500_000: # Bytes
            print(tiff_file)
            time_stamp = os.path.basename(tiff_file).split('_')[0]
            Y, M, D = time_stamp[:4], time_stamp[4:6], time_stamp[6:8]
            h, m, s = time_stamp[9:11], time_stamp[11:13], time_stamp[13:15]
            raster = tf.imread(tiff_file)[:,:,:3]
            #print("min {}, max {}".format(raster.min(),raster.max()))

            tif = tf.TiffFile(tiff_file)
            print(tif.geotiff_metadata)

            '''
            page = tif.pages[0]
            print(page.axes)
            print(page.dtype)
            print(page.shape)
            '''

            output = cv2.cvtColor(raster, cv2.COLOR_BGR2RGB)

            cv2.putText(output,"Y: {}, M: {}, D: {} - h: {}, m: {}, s: {}".format(Y, M, D, h, m, s), (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 1.0 , (0,0,255), 2)

            cv2.imshow("test", output)
            cv2.waitKey()

if __name__ == "__main__":
    """
    Main function for executing the .py script.
    Takes the path to a folder filled with tif files and visualize the images through time
    Command:
        -p path/<tif folder>
    """
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str, default='/media/aau/Storage/Datasets/satellite/sentinel/id-136/rgb',
                    help="path to dir")
    ap.add_argument("-b", "--band", type=int, default=2,
                    help="path to dir")
    args = vars(ap.parse_args())

    #for dir in [x[0] for x in os.walk(args["path"])][1:]: # visit each sub dir

    dir = args["path"]
    print(dir)

    read_tif_dir(dir)
