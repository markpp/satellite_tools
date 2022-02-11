import geopandas as gpd
import matplotlib.pyplot as plt
import argparse
import numpy as np
import os, sys

def create_grid(roi, tile_size=10000, OUTPUT_FOLDER=''):
    roi_shape = roi.geometry.values[0]
    roi_width = roi_shape.bounds[2] - roi_shape.bounds[0]
    roi_height = roi_shape.bounds[3] - roi_shape.bounds[1]
    print(f'Dimension of the area is {roi_width:.0f} x {roi_height:.0f} m2')

    # Create a splitter to obtain a list of bboxes with the given tile_size
    #https://sentinelhub-py.readthedocs.io/en/latest/_modules/sentinelhub/areas.html#TileSplitter.get_tile_dict
    from sentinelhub import UtmZoneSplitter, BBoxSplitter, TileSplitter, CRS
    #bbox_splitter = BBoxSplitter([roi_shape], roi.crs, split_shape=(45, 35))
    #bbox_splitter = TileSplitter([roi_shape], roi.crs, time_interval=, tile_split_shape=)
    bbox_splitter = UtmZoneSplitter([roi_shape], roi.crs, tile_size) #https://github.com/sentinel-hub/sentinelhub-py/issues/123

    bbox_list = np.array(bbox_splitter.get_bbox_list())
    info_list = np.array(bbox_splitter.get_info_list())

    # Prepare info of selected EOPatches
    from shapely.geometry import Polygon
    geometry = [Polygon(bbox.get_polygon()) for bbox in bbox_list]
    idxs = [info['index'] for info in info_list]
    idxs_x = [info['index_x'] for info in info_list]
    idxs_y = [info['index_y'] for info in info_list]

    bbox_gdf = gpd.GeoDataFrame({'index': idxs, 'index_x': idxs_x, 'index_y': idxs_y},crs=roi.crs, geometry=geometry)

    fig, ax = plt.subplots(figsize=(30, 30))
    ax.set_title('Tiles from ROI', fontsize=25)
    roi.plot(ax=ax, facecolor='w', edgecolor='b', alpha=0.5)
    bbox_gdf.plot(ax=ax, facecolor='w', edgecolor='r', alpha=0.5)

    f = open(os.path.join(OUTPUT_FOLDER,'tiles.csv'),'w')
    f.write('id,crs,bbox\n')
    for bbox, info in zip(bbox_list, info_list):
        #print(info)
        f.write('{},{},{}\n'.format(info['index'],info['crs'],bbox))
        geo = bbox.geometry
        ax.text(geo.centroid.x, geo.centroid.y, info['index'], ha='center', va='center')
    f.close()
    plt.axis('off')

if __name__ == "__main__":
    """
    Main function for executing the .py script.
    Command:
        -r path/<filename>.geojson
    """
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--roi", type=str, default='roi.geojson', help="Path to roi file")
    ap.add_argument("-e", "--epsg", type=int, default=25832, help="Select appropriate epsg") # https://epsg.io/25832
    ap.add_argument("-s", "--size", type=int, default=10000, help="Select tile size")

    args = vars(ap.parse_args())

    roi = gpd.read_file(args['roi'])
    roi = roi.to_crs(epsg=args['epsg']) 
    #roi.plot()
    print(roi.crs)
    print(roi.total_bounds)

    create_grid(roi=roi, tile_size=args['size'])
    plt.show()

