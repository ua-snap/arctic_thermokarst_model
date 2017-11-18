"""
Generate Raster
---------------

tools for generating atm input rasters
"""
from osgeo import ogr, gdal
from collections import OrderedDict
import os


# shapefile to raster metadata type
sample_metadata = {
    'NoData': 0,
    'Coalescent low-center polygons': 2,
    'Low-center polygons': 3,
    'Meadow': 4,
    'Drained slope': 7,
    'Flat-center polygons': 8,
    'High-center polygons': 9,
    'Sandy Barrens': 10,
    'Sand Dunes':  11,
    'Ice': 12,
    'Saline coastal water': 13,
    'Rivers': 16,
    'Urban': 17,
    'Riparian shrub': 18,
    'Ponds': 20,
    'Small Lakes': 21,
    'Medium Lakes': 22,
    'Large Lakes': 23,
}

def create_empty_raster ( 
        out_raster, extent, pixel_size, num_layers = 1, dtype = gdal.GDT_Byte
    ):
    """Create an empty raster
    
    Parameters
    ----------
    out_raster: path
        path to output file
    extent: tuple
        extent of raster to create (x_min, x_max, y_min, y_max)
    pixel_size: int
        size of pixel in meters
    num_layers: int, defaults 1
        number of layers to create in raster
    dtype: gdal type, defaults gdal.GDT_Byte
        type of data to create
        
    Returns
    -------
    dest:
        open gdal raster object
    """
    # Create Raster
    #~ print type(extent), extent
    x_min, x_max, y_min, y_max = extent
    x_res = int((x_max - x_min) / pixel_size)
    y_res = int((y_max - y_min) / pixel_size)
    dest = gdal.GetDriverByName('GTiff').Create(
        out_raster,
        x_res,
        y_res, 
        num_layers, 
        dtype )
    dest.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size)) 
    
    ## need to set the    
    
    return dest   

def from_shapefile(
        in_shape, out_raster, metadata,
        log = False, single = False, out_path = './', dtype = gdal.GDT_Byte
    ):
    """convert shape file to raster files(file)
    
    adapted from:
        https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html
        see: convert-an-ogr-file-to-a-raster
    and 
        http://ceholden.github.io/open-geo-tutorial/python/chapter_4_vector.html
        see: Pure-Python-version----gdal.RasterizeLayer
        
    Parameters
    ----------
    in_shapefile: path
        path to .shp file, other shape file files must be present at same
        location
    out_raster: str
        name to give, or prefix, raster files
    metadata: Dict like
        dictionary of raster layer names keys, layer attribute values
    log: Bool, defaults False
        if true prints which layer is being processed
    single:  Bool, defaults False
        if True, save as a single raster
    out_path: path, defaults ./
        path to save rasters at
    dtype: gdal type, defaults gdal.GDT_Byte
        a gdal data type to use to create raster
    """
    # important coefficients
    filter_attr = '"GRIDCODE"'
    pixel_size = 25
    NoData_value = -9999
    rasterize_attr = 'Shape_Area'

    # Open the data source and read in the extent
    source = ogr.Open(in_shape)
    layer = source.GetLayer(0)
    extent = layer.GetExtent()
    #~ print extent
    
    
    

    if single:
        if len(out_raster.split('.')) == 1:
            out_raster += '.tif'
        dest = create_empty_raster(
            os.path.join(out_path,out_raster), extent, pixel_size, num_layers = len(metadata)
        )
    
    
    band_num = 1
    for attr in metadata:
        
        
        if log:
            print 'Generating raster band for ' + attr
        
        if not single:  
            dest = None
            out = \
                out_raster.split('.')[0] + "_" + attr.replace(' ','_') + '.tif'
            dest = create_empty_raster(os.path.join(out_path,out), extent, pixel_size)
        
        val = metadata[attr]
        layer.SetAttributeFilter( filter_attr + ' = ' + str(val) )
        band = dest.GetRasterBand(band_num)
        band.SetNoDataValue(NoData_value)
        gdal.RasterizeLayer(
            dest, 
            [band_num], 
            layer, 
            None, 
            None, 
            [0], 
            ['ATTRIBUTE=Shape_Area']
        )
        
        if single:
            band_num += 1
        
    dest = None
        
def parse_metadata(text):
    """parse yaml metadata on raster layers
    
    Parameters
    ----------
    text: str
        text in yaml format
        
    Returns
    -------
    OrderedDict:
        layer name: raster attribute number
    """
    text = text.rstrip()
    metadata = OrderedDict()
    for line in text.split('\n'):
        key, val = line.split(':')
        val = int(val)
        #~ print key, val
        metadata[key] = val
    
    return metadata



    
    
