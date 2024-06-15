import numpy as np
from scipy.interpolate import griddata

def create_gridx_gridy(data_gdf, cell_size=1., buffer=0.):
    """
    Generates grid x and grid y arrays over the given GeoDataFrame.

    Parameters:
    data_gdf (GeoDataFrame): Input GeoDataFrame containing point geometries.
    cell_size (float, optional): Size of each cell in the grid. Default is 1.
    buffer (float, optional): Buffer distance to extend beyond the total bounds of the GeoDataFrame. Default is 0.

    Returns:
    tuple: Two numpy arrays representing the x and y coordinates of the grid.
    """   
    
    minx, miny, maxx, maxy = data_gdf.total_bounds
    minx = minx - buffer
    miny = miny - buffer
    maxx = maxx + buffer
    maxy = maxy + buffer
    grid_x, grid_y = np.mgrid[minx:maxx:cell_size, miny:maxy:cell_size]
    return grid_x, grid_y


def interpolate_pnt_griddata(data_gdf, column, cell_size=1., buffer=0.):
    """
    Interpolates point data from a GeoDataFrame to a grid using the nearest method.

    Parameters:
    data_gdf (GeoDataFrame): Input GeoDataFrame containing point geometries.
    column (str): Column name in the GeoDataFrame to interpolate.
    cell_size (float, optional): Size of each cell in the grid. Default is 1.
    buffer (float, optional): Buffer distance to extend beyond the total bounds of the GeoDataFrame. Default is 0.

    Returns:
    dict: Dictionary containing the interpolated raster data and metadata.
    """
    grid_x, grid_y = create_gridx_gridy(data_gdf, cell_size=cell_size, buffer=0)

    points = np.array(list(zip(data_gdf.geometry.x, data_gdf.geometry.y)))
    values = data_gdf[column].values

    grid_z = griddata(points, values, (grid_x, grid_y), method="nearest")

    # preprocess
    grid_z = grid_z[:, ::-1].T
    grid_z[np.isnan(grid_z)] = -2
    grid_z[grid_z<0] = 0

    # create a dictionary for the raster data
    GeoT_im = (grid_x.min(), cell_size, 0, grid_y.max(), 0, -cell_size)
    ProjR_im = data_gdf.crs.to_wkt()

    data_raster = {"Image": grid_z, "nodata":-2}
    data_raster["band_name"] = [column]
    data_raster["GeoT_im"] = GeoT_im
    data_raster["ProjR_im"] = ProjR_im
    return data_raster

def interpolate_pnt_idw(data_gdf, column, cell_size=1, distance_coef=2.0, buffer=0.):
    """
    Interpolates point data from a GeoDataFrame to a grid using the Inverse Distance Weighting (IDW) method.

    Parameters:
    data_gdf (GeoDataFrame): Input GeoDataFrame containing point geometries.
    column (str): Column name in the GeoDataFrame to interpolate.
    cell_size (float, optional): Size of each cell in the grid. Default is 1.
    distance_coef (float, optional): Power parameter for the inverse distance weighting. Default is 2.
    buffer (float, optional): Buffer distance to extend beyond the total bounds of the GeoDataFrame. Default is 0.

    Returns:
    dict: Dictionary containing the interpolated raster data and metadata.
    """

    xi, yi = create_gridx_gridy(data_gdf, cell_size=cell_size, buffer=buffer)

    x = data_gdf.geometry.x.values
    y = data_gdf.geometry.y.values
    target = data_gdf[column].values

    dist = np.sqrt((x[:,None,None] - xi[None,:,:])**2 + (y[:,None,None] - yi[None,:,:])**2)
    weights = 1 / ((dist + 1e-10)**distance_coef)
    weights /= (weights.sum(axis=0) + 1e-10)
    grid_z = np.sum(weights * target[:,None,None], axis=0)

    # preprocess
    grid_z = grid_z[:, ::-1]
    grid_z[np.isnan(grid_z)] = -2
    grid_z[grid_z<0] = 0

    # create a dictionary for the raster data
    GeoT_im = (xi.min(), cell_size, 0, yi.max(), 0, -cell_size)
    ProjR_im = data_gdf.crs.to_wkt()

    data_raster = {"Image": grid_z.T, "nodata":-2}
    data_raster["band_name"] = [column]
    data_raster["GeoT_im"] = GeoT_im
    data_raster["ProjR_im"] = ProjR_im
    return data_raster