import geopandas as gpd
from shapely.geometry import MultiPoint, Polygon
from shapely.ops import nearest_points


# define bnd from the points and increate the bnd to 2 meter
def find_minimum_rectangle_gdf(data_gdf, buffer=1.):
    """
    Finds the minimum bounding rectangle of the points in a GeoDataFrame and increases the boundary by a specified buffer distance.

    Parameters:
    data_gdf (GeoDataFrame): Input GeoDataFrame containing point geometries.
    buffer (float, optional): Distance to extend the boundary of the minimum rectangle. Default is 1.

    Returns:
    GeoDataFrame: GeoDataFrame containing the buffered minimum bounding rectangle.
    """    
    bounds = data_gdf.unary_union.bounds
    minx, miny, maxx, maxy = bounds

    polygon = Polygon([(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny), (minx, miny)])

    buffered_pol = polygon.buffer(buffer)
    bnd_gdf = gpd.GeoDataFrame(geometry=[buffered_pol], crs=data_gdf.crs)

    return bnd_gdf


def distance_nearest_neighbor_pnt(gdf):
    """
    Calculates the distance between each point in a GeoDataFrame and its nearest neighbor.

    Parameters:
    gdf (GeoDataFrame): Input GeoDataFrame containing point geometries.

    Returns:
    list: List of distances to the nearest neighbor for each point.
    """
        
    distances = []
    for i, point in enumerate(gdf.geometry):
        # Exclude the point itself
        other_points = gdf.drop(i)
        nearest = nearest_points(point, other_points.unary_union)[1]
        distance = point.distance(nearest)
        distances.append(distance)
    return distances