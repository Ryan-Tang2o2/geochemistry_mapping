import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm

from osgeo import gdal


def save_raster(Data, FileName):
    """
    Saves raster data to a file using GDAL.

    Parameters:
    Data (dict): Dictionary containing the raster data and metadata. 
                 Expected keys are 'Image', 'band_name', 'GeoT_im', 'ProjR_im', and 'nodata'.
    FileName (str): Path to the output file. Should have a '.tif' or '.tiff' extension.

    Returns:
    successful: 200
    """

    I = Data["Image"]
    I = I.reshape(I.shape[0], I.shape[1], 1)

    bnameExist = False
    if "band_name" in Data:
        bnameExist=True
        band_name = Data["band_name"]

    DataType = gdal.GDT_Float64

    if FileName[-3::] in ("tiff", "tif", "TIF", "TIFF"):
        driver = gdal.GetDriverByName("GTiff")

    DataSet =   driver.Create( FileName, I.shape[1], I.shape[0], I.shape[2], DataType )

    if "GeoT_im" in Data:
        GeoT_im = Data["GeoT_im"]
        DataSet.SetGeoTransform(GeoT_im)

    if "ProjR_im" in Data:
        ProjR_im = Data["ProjR_im"]
        DataSet.SetProjection(ProjR_im)

    # Write the array
    for i in range(I.shape[2]):
        DataSet.GetRasterBand(i+1).WriteArray(   I[:,:,i] )
        if "nodata" in Data:
            DataSet.GetRasterBand(i+1).SetNoDataValue(Data["nodata"])
        if bnameExist:
            DataSet.GetRasterBand(i+1).SetDescription(band_name[i])

    del DataSet
    return 200, 'raster was saved'



def imshow_raster(raster_data, name='', cmap='rainbow'):
    """
    Displays a raster image with specified geotransformation and color normalization.

    Parameters:
    - rater data: a dictionary
        The raster data to be displayed. that has Image (2Darray) and GeoT_im (Geotransformation parameters)
    - name: str, optional
        The label for the colorbar and the title suffix. Default is an empty string.
    - cmap: str optional
        the colormap name for visualization of the image. Default is rainbow
    """
    
    def calculate_raster_extent(GeoT_im, raster_size):
        """
        Calculates the extent of the raster image based on geotransformation parameters and raster size.

        Parameters:
        - GeoT_im: list of floats
            Geotransformation parameters.
        - raster_size: tuple of ints
            Size of the raster data (number of rows, number of columns).

        Returns:
        - extent: list of floats
            Extent of the image in the format [xmin, xmax, ymin, ymax].
        """
        xmin, cell_size_x, _, ymax, _, cell_size_y_neg = GeoT_im
        cell_size_y = -cell_size_y_neg

        x_max = xmin + cell_size_x * raster_size[1]
        y_min = ymax - cell_size_y * raster_size[0]
        extent = [xmin, x_max, y_min, ymax]
        return extent
    
    img_array = raster_data['Image']
    geoT_im = raster_data['GeoT_im']
    extent = calculate_raster_extent(geoT_im, img_array.shape)
    
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