# Data sources
The target variables; carbon content, peat and water level will correlate with other more accessible variables such as color, height, etc. Here, we describe any potentially useful data and their sources.


## In-field soil measurements
AU has a large collection of historic soil measurements. While this variables are valuable, they are sparse and expensive to collect. For this reason, they will primarily be used as ground truth and evaluation.

## Satellite and aerial imaging
Images captured by satellite and from airplanes are available in large quantities and at low cost. The measurements are dense and makes it possible to completely cover large geographic areas at intervals of a few days.
The main challenge is typically cloud coverage.
it would be interesting to find out if any satellite based radar data is available!

### Sentinel-2
Sentinel-2 covers 13 spectral bands ranging from Visible (VNIR) and Near Infra-Red (NIR) to Short Wave Infra-Red (SWIR). The 13 spectral bands are distributed across 3 resolutions:

- 4 bands with 10 meter resolution: the classical RGB bands ((Blue (~493nm), Green (560nm), and Red (~665nm)) and a Near Infra-Red (~833nm) band.
- 6 bands with 20 meter resolution: 4 narrow Bands in the VNIR vegetation red edge spectral domain (~704nm,~740nm, ~783nm and ~865nm) and 2 wider SWIR bands (~1610nm and ~2190nm) for applications such as snow/ice/cloud detection, or vegetation moisture stress assessment.
- 3 bands with 60 meter resolution: ~443nm for aerosols, ~945nm for water vapour and ~1374nm for cirrus detection.

Radiometric resolution is the capacity of the instrument to distinguish differences in light intensity or reflectance. The MSI instrument has a 12 bit resolution, enabling the images to be acquired over a range of 0 to 4095 intensity values.

#### Bands

![10m](https://sentinels.copernicus.eu/image/image_gallery?uuid=c5fa6c3e-2978-4fb8-ac95-3be9c5171be2&groupId=247904&t=1345630320883 "10 meter spatial resolution")
Figure 1: SENTINEL-2 10 m spatial resolution bands: B2 (490 nm), B3 (560 nm), B4 (665 nm) and B8 (842 nm)

![20m](https://sentinels.copernicus.eu/image/image_gallery?uuid=15dad96b-be6a-4b04-931d-d8c4db39e9e2&groupId=247904&t=1345630328076 "10 meter spatial resolution")
Figure 2: SENTINEL-2 20 m spatial resolution bands: B5 (705 nm), B6 (740 nm), B7 (783 nm), B8a (865 nm), B11 (1610 nm) and B12 (2190 nm)

![60m](https://sentinels.copernicus.eu/image/image_gallery?uuid=f6117fbe-1513-4a84-acc4-845e14e5c876&groupId=247904&t=1345630315020 "10 meter spatial resolution")
Figure 3: SENTINEL-2 60 m spatial resolution bands: B1 (443 nm), B9 (940 nm) and B10 (1375 nm)

[https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi)
[https://en.wikipedia.org/wiki/Sentinel-2](https://en.wikipedia.org/wiki/Sentinel-2)

### SPOT-5

### Landsat-8

### MODIS
Moderate Resolution Imaging Spectroradiometer (MODIS) is a sensor operating on the Terra and Aqua satellites, both launched by NASA. The Terra and Aqua MODIS can acquire radiometric-sensitive data (12 bit) in 36 spectral bands (groups of wavelengths ranging from 0.4 to 14.4 μm) and sweep the entire Earth surface every 1 to 2 days. MODIS datasets can be found in Google's Earth Engine catalogue - https://developers.google.com/earth-engine/datasets/catalog/modis.

## Types of aerial imaging
General introduction to aerial imaging and how it relates to bands - https://earthobservatory.nasa.gov/features/FalseColor

### Classic RGB images
Photo-like images that can be used for NN training.

### Synthetic-aperture radar (SAR)

### NDVI and EVI
Vegetation reflects light in the near-infrared (NIR) part of the electromagnetic spectrum and absorbs light in the red part. The Normalized Difference Vegetation Index (NDVI) and the Enhanced vegetation index (EVI) use this to create a single value that roughly reflects the photosynthetic activity occurring at a pixel.

EVI is very similar to NDVI. The only difference is that it corrects atmospheric and canopy background noise, particularly in regions with high biomass.

Dataset example - https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13Q1

### NDWI
NDWI monitors changes in water content of leaves, using near-infrared (NIR) and short-wave infrared (SWIR) wavelengths, as proposed by Gao in 1996. This could be relevant as the main issue with the peatlands is the lack of water.

Dataset example - https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C01_T1_8DAY_NDWI

### Atmosphere monitoring
Thanks to the satellite Sentinel-5P, it is now possible to assess air quality above Europe using aerial imagining. One of the measured elements is methane. Methane itself is a greenhouse gas, but it is also a byproduct of healthy peatlands. Therefore, using this method it is theoretically possible to identify drying peatlands, i.e. methane output decreases along with the water and the vegetation in the area.

Issues → Sentinel-5P is very new, data only goes back to 2019. The methane output of the wet peatlands may not be enough to raise a flag.

Further research → What other gases are byproducts of wet or drained peatlands, and is it possible to detect them using Sentinel-5P? Currently, carbon dioxide is not measured using Sentinel-5P.

Sentinel-5P datasets in the Google's Earth Engine catalogue - https://developers.google.com/earth-engine/datasets/catalog/sentinel-5p

## Sentinel Missions

Sentinel missions collect information on different aspects of Earth’s physical, chemical, and biological processes. These aspects then relate to six main applications. These are:
* Atmospheric monitoring
* Security
* Marine monitoring
* Land monitoring
* Emergency management
* Climate change

Out of these six areas, land monitoring is the one that relates the most to our goal. Sentinel missions that provide data on the land monitoring are:
* Sentinel-1
* Sentinel-2
* Sentinel-3

### Sentinel-1
Sentinel-1 provides day and night C-band synthetic aperture radar (SAR) imaging, which allows for image acquisition in all weather conditions. Synthetic aperture relates to the method of producing fine-resolution images using a resolution-limited radar system.  C-band has a frequency between 4 - 8 GHz and a wavelength of 7.5 - 3.8 cm.

The Sentinel-1 dataset is available through Google’s Earth Engine. For more detailed description on the dataset, read this [file](sentinel1.md).

![Sentinel-1](https://developers.google.com/earth-engine/images/datasets/copernicus_s1_grd_1280_720.jpg "An example of Sentinel-1 SAR data")


### Sentinel-2

Sentinel-2 is a wide-swath, high-resolution, multi-spectral imaging mission. The onboard multi-spectral instrument (MSI) samples 13 spectral bands. The MSI collects data passively, which means that it records the sunlight reflected from the Earth, therefore it is not weatherproof like Sentinel-1.
The 13 collected spectral bands range from the Visible (VNIR) and Near Infra-Red (NIR) to the Short Wave Infra-Red (SWIR).

The Sentinel-2 data is available through Google’s Earth Engine in two levels. Level-2A provides surface reflectance data. Level-1C provides top-of-atmosphere reflectance data. The difference can be seen in the figure below.

![Sentinel-2 L2A](https://developers.google.com/earth-engine/images/datasets/copernicus_s2_sr_1280_720.jpg "An example of Sentinel-2 surface reflectance data")

![Sentinel-2 L1C](https://developers.google.com/earth-engine/images/datasets/copernicus_s2_toa_1280_720.jpg "An example of Sentinel-2 top-of-atmosphere reflectance data")

### Sentinel-3
The Sentinel-3 mission is to collect data on sea-surface topography, sea and land surface temperature, and ocean and land surface colour with high accuracy and reliability.
Sentinel-3 takes advantage of multiple sensing instruments:
* Sea and Land Surface Temperature Radiometer (SLSTR)
	* The spatial resolution – 500 m for the first 6 bands, 1 km for the last 3 bands
* Ocean and Land Colour Instrument (OLCI)
	* OLCI is a medium-resolution optical spectrometer with the spatial resolution of 300 m
* Synthetic Aperture Radar Altimeter (SRAL)
	* The spatial resolution of 300 m

Sentinel-3 OLCI data is available through Google’s Earth Engine.

![Sentinel-3 OLCI](https://developers.google.com/earth-engine/images/datasets/copernicus_s3_olci_1280_720.jpg "An example of Sentinel-3 OLCI data")
