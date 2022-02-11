import os

# Define path to the folder with images
out_dir = 'D:/Sentinel2/161'
out_dir_RGB = os.path.join(out_dir, 'rgb')
out_dir_Bands = os.path.join(out_dir, 'bands')

# Read the files in the Band and RGB folders.
_, _, files_Bands = next(os.walk(out_dir_Bands))
_, _, files_RGB = next(os.walk(out_dir_RGB))
# Calculate the number of files, we will use this for iterating over the files.
number_of_files = len(files_RGB) - 1

# Take the MGRS code of the first file. Compare it against MGRS codes of other files.
# Save all the found MGRS codes to the list.
MGRS_list = [files_RGB[0][-7:-4]]
for file in files_RGB:
    if file == 'metadata.csv':
        continue
    MGRS_file = file[-7:-4]
    if MGRS_file != MGRS_list[0]:
        if MGRS_file not in MGRS_list:
            MGRS_list.append(MGRS_file)

# Create a nested array with the number of rows equal to the number of entries in the MGRS_list
file_matrix = []
for entry in MGRS_list:
    file_matrix.append([])
size_list = []
indexer = 0

# Collect files with the same MGSR code into one row of the file matrix.
# While collecting the files, also calculate the overall size of all RGB files with the given MGSR code.
for MGSR in MGRS_list:
    size = 0
    for file in files_RGB:
        if MGSR == file[-7:-4]:
            file_path_RGB = os.path.join(out_dir_RGB, file)
            file_path_Bands = os.path.join(out_dir_Bands, file)
            file_matrix[indexer].append(file_path_RGB)
            file_matrix[indexer].append(file_path_Bands)
            file_size = os.path.getsize(file_path_RGB)
            size += file_size
    size_list.append(size)
    indexer += 1

# Take the MGSR code that corresponds to the smaller overall file size and remove the files.
min_index = size_list.index(min(size_list))
for path in file_matrix[min_index]:
    os.remove(path)

# Take the MGSR code that corresponds to the bigger overall file size and do something with them.
# You can use this code when you don't want to remove sample, only skip reading them.
# max_index = size_list.index(max(size_list))
# for path in file_matrix[max_index]:
    # Enter code for what to do with each path in the file matrix
