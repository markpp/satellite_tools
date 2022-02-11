import argparse
import cv2
import numpy as np
import tifffile as tf
import os


if __name__ == '__main__':
    """
    Plot a sentinel1 sample(s).

    use -p <dir>/<filename>.tif to plot a single file
    use -d <dir> to create image series from all tif files in dir

    Command:
        python sentinel1_visualise.py
    """
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str,
                    default=None, help="file path")
    ap.add_argument("-d", "--dir", type=str,
                    default=None, help="dir path")
    ap.add_argument("-o", "--output", type=str,
                    default="output", help="output dir")
    ap.add_argument("-s", "--show", type=int,
                    default=0, help="show frames")
    ap.add_argument("-min", "--minimum", type=float,
                    #default=None, help="minium value")
                    default=-78.0, help="minium value")
    ap.add_argument("-max", "--maximum", type=float,
                    #default=None, help="maximum value")
                    default=29.0, help="maximum value")
    args = vars(ap.parse_args())


    if args['path'] is not None:
        print(args['path'])
        tif_img = tf.imread(args['path'])
        print(tif_img.shape)
        img = tif_img[:, :, 1] #
        norm_img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

        cv2.imshow('Normalized Image', norm_img)
        cv2.waitKey()

    elif args['dir'] is not None:
        os.makedirs(args['output'], exist_ok=True)

        from glob import glob
        tif_list = sorted([y for y in glob(args['dir']+'/*.tif', recursive=True)])

        if args['minimum'] is None and args['maximum'] is None:
            min_global, max_global = 0.0, 0.0
        else:
            min_global, max_global =  args['minimum'], args['maximum']
        for i, tif_path in enumerate(tif_list):
            #print("{}, size: {}".format(i,os.path.getsize(tif_path)))
            if os.path.getsize(tif_path) > 15_000_000:
                tif_img = tf.imread(tif_path)

                img = tif_img[:, :, 0]

                if args['minimum'] is None and args['maximum'] is None:
                    min, max = np.min(img), np.max(img)
                    min_global = min if min < min_global else min_global
                    max_global = max if max > max_global else max_global
                else:
                    min, max = args['minimum'], args['maximum']

                norm_img = (img - min) / (max - min)

                time_stamp = os.path.basename(tif_path).split('_')[4]
                Y, M, D = time_stamp[:4], time_stamp[4:6], time_stamp[6:8]
                h, m, s = time_stamp[9:11], time_stamp[11:13], time_stamp[13:15]
                tmp = (norm_img*255).astype(np.uint8)
                tmp = cv2.cvtColor(tmp, cv2.COLOR_GRAY2BGR)
                cv2.putText(tmp,"Y: {}, M: {}, D: {} - h: {}, m: {}, s: {}".format(Y, M, D, h, m, s), (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 2)

                if args['show']:
                    cv2.imshow('Normalized Image', tmp)
                    key = cv2.waitKey()
                    if key == 27:
                        break

                if args['minimum'] is not None and args['maximum'] is not None:
                    cv2.imwrite(os.path.join(args['output'],"{}.png".format(i)),tmp)

        print("min_global: {}, max_global: {}".format(min_global, max_global))
