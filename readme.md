# Project Title
Continuous spatial distribution of Cu and Co concentrations

## Project Overview
Geochemical soil surveys are commonly used in mineral exploration. Workers collect soil samples from specified locations across an area. These samples are analyzed to determine the concentrations of trace metals like copper (Cu) and cobalt (Co).

This project processes CSV files to plot Cu and Co concentrations, generating images (TIFF) and shapefiles that can be used in GIS software like QGIS.

In the `description.md file, more information about the assumptions made during this process, discussions about the results, and the final outcomes can be found.


## Directory Structure
project_root
│
├── readme.md
├── description.md                 # Description of approach and final results
├── environment.yml                # List of required dependencies
├── main_mapping_Cu_Co.ipynb       # Main code
│
├── utility_function/              # Utility functions
│   ├── interpolations_method.py   # Interpolation algorithms
│   ├── raster_process.py          # Functions to analyze raster data
│   └── vector_process.py          # Functions to analyze vector data
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
├── result_images/                 # Output images from the code
│   └── secondary_results          # Additional output images
│
└── test/                          # Testing functions and outputs
    ├── test_function.ipynb        # Code to test functions



## Data Processing Steps
To generate plots of Cu and Co concentrations, follow these steps:

1. Data Exploration:
- Scatterplots and Histograms: Plot scatterplots and histograms to understand spatial distribution and identify patterns. Anomalies were not the focus as the data was assumed to be reliable.
2. Data preperation:
- Unit converion: All data with pct unit was converted to ppm 
- Fill Null value: Several different model were used to fill Null value fo Co.
3. Boundary creation:
- boundary creation: Create a boundary of the geospatial data using the minimum bounding box of the data points with a 5-meter buffer.
4. Interpolation:
- Inverse Distance Weighting (IDW): Use the IDW method with a distance coefficient of 3.
5. Raster Data Generation:
- Raster Conversion: Convert the interpolated grid cells into raster data (TIFF format) for use in GIS software.
- viualize raste. Visualize the final map of Cu and Co concentration on a log scale.


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
1. Unzip the file.
2. Navigate to the project directory.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
4. If using VS Code, run the Jupyter notebook to process the data and generate outputs:
- Change the Python interpreter to the environment you built.
- Open a terminal and run:
  ```bash
  jupyter notebook main_mapping_Cu_Co.ipynb
5. The generated files will be saved in the appropriate directories under data/outputs/.

** The main_mapping_Cu_Co.ipynb can also works on Colab



## Contact Information
For further assistance, please contact Ata Haddadi at ata.haddadi@gmail.com