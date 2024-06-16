import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm

from osgeo import gdal


def save_raster(raster_data, file_name):
    """
    Saves raster data to a file using GDAL.

    Parameters:
    raster_data (dict): Dictionary containing the raster data and metadata. 
                        Expected keys are 'Image', 'band_name', 'GeoT_im', 'ProjR_im', and 'nodata'.
    file_name (str): Path to the output file. Should have a '.tif' or '.tiff' extension.

    Returns:
    None
    """
    
    gdal.UseExceptions()

    # Extract raster data and reshape if necessary
    image = raster_data.get("Image")
    if image is None:
        raise ValueError("raster_data must contain 'Image' key.")
        
    if len(image.shape) == 2:
        image = image[:, :, np.newaxis]

    band_names = raster_data.get("band_name")
    geotransform = raster_data.get("GeoT_im")
    projection = raster_data.get("ProjR_im")
    nodata_value = raster_data.get("nodata")

    # Determine data type
    data_type = gdal.GDT_Float64

    # Determine the driver to use
    if file_name.lower().endswith(('.tif', '.tiff')):
        driver = gdal.GetDriverByName("GTiff")
    else:
        raise ValueError("Output file must have a .tif or .tiff extension.")

    # Create the dataset
    dataset = driver.Create(file_name, image.shape[1], image.shape[0], image.shape[2], data_type)
    if dataset is None:
        raise RuntimeError("Failed to create the dataset. Check the file path and permissions.")

    # Set the geotransform and projection
    if geotransform:
        dataset.SetGeoTransform(geotransform)
    if projection:
        dataset.SetProjection(projection)

    # Write the array and set metadata
    for i in range(image.shape[2]):
        band = dataset.GetRasterBand(i + 1)
        band.WriteArray(image[:, :, i])
        if nodata_value is not None:
            band.SetNoDataValue(nodata_value)
        if band_names and i < len(band_names):
            band.SetDescription(band_names[i])

    # Close the dataset
    dataset = None



def calculate_raster_extent(geotrans_im, raster_size):
    """
    Calculates the extent of the raster image based on geotransformation parameters and raster size.

    Parameters:
    - geotrans_im: list of floats
        Geotransformation parameters.
    - raster_size: tuple of ints
        Size of the raster data (number of rows, number of columns).

    Returns:
    - extent: list of floats
        Extent of the image in the format [xmin, xmax, ymin, ymax].
    """
    xmin, cell_size_x, _, ymax, _, cell_size_y_neg = geotrans_im
    cell_size_y = -cell_size_y_neg

    x_max = xmin + cell_size_x * raster_size[1]
    y_min = ymax - cell_size_y * raster_size[0]
    extent = [xmin, x_max, y_min, ymax]
    return extent


def imshow_raster(raster_data, name='', cmap='rainbow'):
    """
    Displays a raster image with specified geotransformation and color normalization.

    Parameters:
    - rater data: a dictionary
        The raster data to be displayed. that has Image (2Darray) and geotrans_im (Geotransformation parameters)
    - name: str, optional
        The label for the colorbar and the title suffix. Default is an empty string.
    - cmap: str optional
        the colormap name for visualization of the image. Default is rainbow
    """
    
    
    img_array = raster_data['Image']
    geotrans_im = raster_data['GeoT_im']
    extent = calculate_raster_extent(geotrans_im, img_array.shape)
    
    low_log = np.min(img_array[img_array > 0])
    if low_log<100:
        low_log = 100
    high_log = img_array.max()

    plt.figure(figsize=(8, 6))
    cmap = plt.get_cmap(cmap)

    # Create the plot with the colormap and colorbar
    img = plt.imshow(img_array, cmap=cmap, norm=LogNorm(vmin=low_log, vmax=high_log), extent=extent, origin='upper')
    cbar = plt.colorbar(img)

    cbar_ticks = np.logspace(np.log10(low_log), np.log10(high_log), num=5)
    cbar.set_ticks(cbar_ticks)
    cbar.ax.set_yticklabels([f'{tick/1000:0.2f}K' for tick in cbar_ticks])

    # Colorbar label
    cbar.set_label(name)
    
    # Add a scale bar
    fontprops = fm.FontProperties(size=12)
    scalebar = AnchoredSizeBar(plt.gca().transData,
                               10, '10m', 'upper left', 
                               pad=0.1,
                               color='white',
                               frameon=False,
                               size_vertical=1,
                               fontproperties=fontprops)
    plt.gca().add_artist(scalebar)

    plt.title(f'{name} concentration map - (colorbar is in log scale)')
    plt.xlabel('x (m!)')
    plt.ylabel('y (m!)')
    plt.grid()