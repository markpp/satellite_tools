import os
import tifffile as tf # documentation: https://github.com/cgohlke/tifffile
import json
import numpy
import matplotlib.pyplot as plt

in_dir_asc = 'F:/Sentinel1/2020_GRD/293/asc'
in_dir_des = 'F:/Sentinel1/2020_GRD/293/des'
in_dir_asc_float = 'F:/Sentinel1/2020_GRD_FLOAT/293/asc'
in_dir_des_float = 'F:/Sentinel1/2020_GRD_FLOAT/293/des'


def get_diff(dir, channel):
    _, _, files = next(os.walk(dir))
    max_list = []
    min_list = []
    for file in files:
        if file == "metadata.csv":
            continue
        path = os.path.join(dir, file)
        mat = tf.imread(path)
        max_list.append(mat[:, :, channel].max())
        min_list.append(mat[:, :, channel].min())
    #print(max_list)
    #print(min_list)

    diff_max = []
    diff_min = []
    for i in range(0, len(max_list) - 1):
        diff = abs(max_list[i] - max_list[i + 1])
        diff_max.append(diff)
        diff = abs(min_list[i] - min_list[i + 1])
        diff_min.append(diff)
    #print(diff_max)
    #print(diff_min)
    return diff_max, diff_min


def add_samples(dir):
    _, _, files = next(os.walk(dir))

    for i in range(0, len(files)):
        filename_1 = files[i]
        file_1 = files[i][17:25]
        for j in range(i + 1, len(files)):
            filename_2 = files[j]
            file_2 = files[j][17:25]
            if file_2 == file_1:
                file_1_path = os.path.join(dir, filename_1)
                file_2_path = os.path.join(dir, filename_2)
                tif_1_mat = tf.imread(file_1_path)
                tif_2_mat = tf.imread(file_2_path)
                tif_3_mat = tif_1_mat + tif_2_mat
                tif_1_img = tf.TiffFile(file_1_path)
                tif_metadata = tif_1_img.geotiff_metadata
                tif_metadata = json.dumps(tif_metadata)
                path = os.path.join(dir, filename_1)
                tf.imsave(path, tif_3_mat, description=str(tif_metadata))
                os.remove(file_2_path)


def plot(plot_name, diff_0_max, diff_0_min, diff_1_max, diff_1_min):
    fig, axs = plt.subplots(4, sharex=True, sharey=True)
    x_axis = range(0, len(diff_0_max))
    fig.suptitle(plot_name)
    axs[0].plot(x_axis, diff_0_max)
    axs[0].set_title('1st Band, diff_max')
    axs[1].plot(x_axis, diff_1_max)
    axs[1].set_title('2nd Band, diff_max')
    axs[2].plot(x_axis, diff_0_min, 'tab:red')
    axs[2].set_title('1s Band, diff_min')
    axs[3].plot(x_axis, diff_1_min, 'tab:red')
    axs[3].set_title('2nd Band, diff_min')

    for ax in axs:
        ax.set_ylabel('|diff|')


def remove_samples(dir):
    _, _, files = next(os.walk(dir))

    for file in files:
        path = os.path.join(dir, file)
        file_size = os.path.getsize(path)
        if file_size < 18000000:
            os.remove(path)


add_samples(in_dir_asc)
add_samples(in_dir_des)
add_samples(in_dir_asc_float)
add_samples(in_dir_des_float)

_diff_0_max, _diff_0_min = get_diff(in_dir_asc, 0)
_diff_1_max, _diff_1_min = get_diff(in_dir_asc, 1)
plot("Region 293, asc", _diff_0_max, _diff_0_min, _diff_1_max, _diff_1_min)

_diff_0_max, _diff_0_min = get_diff(in_dir_des, 0)
_diff_1_max, _diff_1_min = get_diff(in_dir_des, 1)
plot("Region 293, des", _diff_0_max, _diff_0_min, _diff_1_max, _diff_1_min)

_diff_0_max, _diff_0_min = get_diff(in_dir_asc_float, 0)
_diff_1_max, _diff_1_min = get_diff(in_dir_asc_float, 1)
plot("Region 293, both", _diff_0_max, _diff_0_min, _diff_1_max, _diff_1_min)

_diff_0_max, _diff_0_min = get_diff(in_dir_des_float, 0)
_diff_1_max, _diff_1_min = get_diff(in_dir_des_float, 1)
plot("Region 293, asc_reduced", _diff_0_max, _diff_0_min, _diff_1_max, _diff_1_min)

plt.show()


"""
tif_3_img = tf.TiffFile(path_to_save)
tif_metadata_string = tif_3_img.pages[0].tags['ImageDescription'].value
tif_metadata = json.loads(tif_metadata_string)
print(tif_metadata)
print(type(tif_metadata))
for k,v in tif_metadata.items():
    print(k,v)
"""