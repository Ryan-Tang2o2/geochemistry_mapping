# Project Title
Continuous spatial distribution of Cu and Co concentrations

## Project Overview
Geochemical soil surveys are commonly used in mineral exploration. Workers walk or drive around a (potentially large) area and collect soil samples at specified locations. These samples are analyzed to determine the concentration of certain trace metals. The metal content in soils depends both on the composition of the bedrock directly beneath the soils and by surficial processes like fluid flows.

This project processes CSV files to plot Cu (Copper) and Co (Cobalt) concentrations, generating images (TIFF) and shapefiles that can be used in GIS software like QGIS.


## Directory Structure
project_root
│
├── readme.md
├── description.md
├── requirements.txt               
├── main_mapping_Cu_Co.ipynb       # main code 
│
├── utility_function/              # All utility functions
│   ├── interpolations_method.py   # Interpolation algorithms
│   ├── raster_process.py          # Functions to analyze raster data
│   └── victor_process.py          # Functions to analyze vector data
│
├── data/
│   ├── raw/                       # Original CSV files
│   ├── processed/                 # Processed CSV files
│   └── outputs/                   # Output files
│       ├── bnd.geojson            # Boundary of the data points
│       ├── pnt_cu_co.geojson      # GeoJSON file of the data points
│       ├── polygon_cu_co.geojson  # GeoJSON file of the data in polygon format
│       ├── cu_idw_3.tif           # TIFF image of Cu based on IDW interpolation (weight = 3)
│       └── co_idw_3.tif           # TIFF image of Co based on IDW interpolation (weight = 3)
│
├── docs/                          # Project documentation in PDF
└── result_images/                 # Output images from my code. PNG file that present Cu and Co cocentration in 2D
│       └── seconday_results       # Output images from my code. PNG files
│
└── test/                          # Output images from my code or QGIS 
│   ├──  test_function.ipynb       # code to test my functions




## Data Processing Steps
To generate plots of Cu and Co concentrations across the region, several processing steps are necessary:

1. Data Exploration:
- Scatterplots and Histograms: Plot scatterplots and histograms of the data to understand the spatial distribution and identify patterns. For this project I did not focuse on anamolies, as the data was assumed to be reliable
2. Data preperation:
- Unit converion: All data with pct unit was converted to ppm 
- Fill Null value: Several different model were used to fill Null value fo Co.
3. Boundary creation:
- boundary creation: Create a boundary of the geospatial data using the minimum bounding box of the data points. A buffer of 5 meter was used to have a bigger bounday
4. Interpolation:
- Grid Creation: Create grid cells over the boundary of the data.
- Inverse Distance Weighting (IDW): Use the IDW method with a distance coefficient of 3.
5. Raster Data Generation:
- Raster Conversion: Convert the interpolated grid cells into raster data (TIFF format) for use in GIS software.
- viualize raste: the final map of Cu and Co concentration was shown in a log scale.

## Dependencies
- Python 3.x
- Required Python packages:
  - numpy
  - pandas
  - geopandas
  - shapely
  - gdal
  - matplotlib
  - seaborn
  - sklearn
  - scipy


## Usage Instructions
- pull the repository
- install the required dependecis
- run the notebook to process the data and generate the outputs
- the generated files will be saved in the appropriate directories


## Contact Information
For further assistance, please contact Ata Haddadi at ata.haddadi@gmail.com