"""Contains objects to represent internal grid cohort data in ATM
"""
import numpy as np
import gdal
import os

from collections import namedtuple

import matplotlib.pyplot as plt

class MassBalanceError (Exception):
    """Raised if there is a mass balance problem"""

RASTER_METADATA = namedtuple('RASTER_METADATA', 
    ['transform', 'projection', 
        'nX', 'nY', 'deltaX', 'deltaY', 'originX', 'originY'
    ]
)

def load_raster (filename):
    """Load a raster file and it's medatadata
    
    Parameters
    ----------
    filename: str
        path to raster file to read
        
    Returns 
    -------
    np.array
        2d raster data
    RASTER_METADATA
        metadata on raster file read
    """
    dataset = gdal.Open(filename, gdal.GA_ReadOnly)
    #~ print type(dataset)
    (X, deltaX, rotation, Y, rotation, deltaY) = dataset.GetGeoTransform()

    metadata = RASTER_METADATA(
        transform = (X, deltaX, rotation, Y, rotation, deltaY),
        projection = dataset.GetProjection(),  
        nX = dataset.RasterXSize,
        nY = dataset.RasterYSize,
        deltaX = deltaX,
        deltaY = deltaY,
        originX = X,
        originY = Y
    )
    ## assumes one band, also gdal uses one based indexing here 
    data = dataset.GetRasterBand(1).ReadAsArray()
    return data, metadata
    
def save_bin (data, path):
    """ Function doc """
    data.tofile(path)

    
def save_img (data, path, title):
    """ Function doc """
    imgplot = plt.imshow(
        data, 
        interpolation = 'nearest', 
        cmap = 'spectral', 
        vmin = 0.0, 
        vmax = 1.0
    )
    plt.title(title)
    plt.colorbar(extend = 'neither', shrink = 0.92)
    #~ imgplot.save(path)
    #~ plt.imsave(path, imgplot)
    plt.savefig(path)
    plt.close()

# maps alternate name to the names used by ATM internally
#
# See Also
# --------
#   find_canon_name
CANON_COHORT_NAMES = {
    ('CoalescentLowCenterPolygon_WetlandTundra_Medium',): 'CLC_WT_M',
    ('CoalescentLowCenterPolygon_WetlandTundra_Old',): 'CLC_WT_O',
    ('CoalescentLowCenterPolygon_WetlandTundra_Young',): 'CLC_WT_Y',
    
    ('CoastalWaters_WetlandTundra_Old',): 'CoastalWaters_WT_O',
    
    ('DrainedSlope_WetlandTundra_Medium',): 'DrainedSlope_WT_M',
    ('DrainedSlope_WetlandTundra_Old',): 'DrainedSlope_WT_O',
    ('DrainedSlope_WetlandTundra_Young',): 'DrainedSlope_WT_Y',
    
    ('FlatCenterPolygon_WetlandTundra_Medium',): 'FCP_WT_M',
    ('FlatCenterPolygon_WetlandTundra_Old',): 'FCP_WT_O',
    ('FlatCenterPolygon_WetlandTundra_Young',): 'FCP_WT_Y',
    
    ('HighCenterPolygon_WetlandTundra_Medium',): 'HCP_WT_M',
    ('HighCenterPolygon_WetlandTundra_Old',): 'HCP_WT_O',
    ('HighCenterPolygon_WetlandTundra_Young',): 'HCP_WT_Y',
    
    ('LargeLakes_WetlandTundra_Medium',): 'LargeLakes_WT_M',
    ('LargeLakes_WetlandTundra_Old',): 'LargeLakes_WT_O',
    ('LargeLakes_WetlandTundra_Young',): 'LargeLakes_WT_Y',
    
    ('LowCenterPolygon_WetlandTundra_Medium',): 'LCP_WT_M',
    ('LowCenterPolygon_WetlandTundra_Old',): 'LCP_WT_O',
    ('LowCenterPolygon_WetlandTundra_Young',): 'LCP_WT_Y',
    
    ('Meadow_WetlandTundra_Medium',): 'Meadow_WT_M',
    ('Meadow_WetlandTundra_Old',): 'Meadow_WT_O',
    ('Meadow_WetlandTundra_Young',): 'Meadow_WT_Y',
    
    ('MediumLakes_WetlandTundra_Medium',): 'MediumLakes_WT_M ',
    ('MediumLakes_WetlandTundra_Old',): 'MediumLakes_WT_O',
    ('MediumLakes_WetlandTundra_Young',): 'MediumLakes_WT_Y' ,
    
    ('NoData_WetlandTundra_Old', ): 'NoData_WT_O',
    
    ('Ponds_WetlandTundra_Medium',): 'Ponds_WT_M',
    ('Ponds_WetlandTundra_Old',): 'Ponds_WT_O',
    ('Ponds_WetlandTundra_Young',): 'Ponds_WT_Y',
    
    ('Rivers_WetlandTundra_Medium',): 'Rivers_WT_M',
    ('Rivers_WetlandTundra_Old',): 'Rivers_WT_O',
    ('Rivers_WetlandTundra_Young',): 'Rivers_WT_Y',
    
    ('SandDunes_WetlandTundra_Medium',): 'SandDunes_WT_M',
    ('SandDunes_WetlandTundra_Old',): 'SandDunes_WT_O',
    ('SandDunes_WetlandTundra_Young',): 'SandDunes_WT_Y',
    
    ('SaturatedBarrens_WetlandTundra_Medium',): 'SaturatedBarrens_WT_M',
    ('SaturatedBarrens_WetlandTundra_Old',): 'SaturatedBarrens_WT_O',
    ('SaturatedBarrens_WetlandTundra_Young',): 'SaturatedBarrens_WT_Y',
    
    ('Shrubs_WetlandTundra_Old',): 'Shrubs_WT_O',
    
    ('SmallLakes_WetlandTundra_Medium',): 'SmallLakes_WT_M',
    ('SmallLakes_WetlandTundra_Old',): 'SmallLakes_WT_O',
    ('SmallLakes_WetlandTundra_Young',): 'SmallLakes_WT_Y',
    
    ('Urban_WetlandTundra_Old',): 'Urban_WetlandTundra_Old',
    
    ## barrow NO AGE STUFF ?? ask bob.
    ('Rivers',): 'Rivers',
    ('Ponds',): 'Ponds',
    ('Lakes',): 'Lakes',
    ('FlatCenter',): 'FCP',
    ('Urban',): 'Urban',
    ('Meadows',): 'Meadows',
    ('CoalescentLowCenter',): 'CLC',
    ('HighCenter',) : 'HCP',
    
    ## Tanana flats
    ('OldBog',): 'TF_OB',
    ('OldFen',): 'TF_OF',
    ('Coniferous_PermafrostPlateau',): 'TF_Con_PP',
    ('Deciduous_PermafrostPlateau',): 'TF_Dec_PP',
    ('ThermokarstLake',): 'TF_TL',
    ('YoungBog',): 'TF_YB',
    ('YoungFen',): 'TF_YF',
    
    ## Yukon Flats
    ('Barren_Yukon',): 'Barren_Yukon',
    ('Bog_Yukon',): 'Bog_Yukon',
    ('DeciduousForest_Yukon',): 'DeciduousForest_Yukon',
    ('DwarfShrub_Yukon',): 'DwarfShrub_Yukon',
    ('EvergreenForest_Yukon',): 'EvergreenForest_Yukon',
    ('Fen_Yukon',): 'Fen_Yukon',
    ('Lake_Yukon',): 'Lake_Yukon',
    ('Pond_Yukon',): 'Pond_Yukon',
    ('River_Yukon',): 'River_Yukon',
    ('ShrubScrub_Yukon',): 'ShrubScrub_Yukon',
    ('Unclassified_Yukon',): 'Unclassified_Yukon',
}

def find_canon_name (name):
    """find canonical name of cohort given an alternate name
    
    Parameters
    ----------
    name: str
        the alternative name
        
    Raises
    ------
    KeyError
        if canon name not found
    
    Returns
    -------
    Str
        Canon name of cohort
    """
    ## is name a canon name
    if name in CANON_COHORT_NAMES.values():
        return name
    
    ## loop to find canon name
    for alt_names in CANON_COHORT_NAMES:
        if name in alt_names:
            return CANON_COHORT_NAMES[alt_names]
    raise KeyError, 'No canon cohort name for exists ' + name 


# index names for rows and columns to make code easier to read/update
#
ROW, Y = 0, 0 ## index for dimensions 
COL, X = 1, 1 ## index for dimensions 

class CohortGrid(object):
    """ Concept Class for atm TerrainGrid that represents the data  """
    def __init__ (self, config):
        """This class represents model area grid as fractional areas of each
        cohort that make up a grid element. In each grid element all
        fractional cohorts should sum to one.
        
        
        .. note:: Note on grid coordinates
            Origin (Y,X) is top left. rows = Y, cols = X
            Object will store dimensional(resolution, dimensions) 
            metadata as a tuple (Y val, X val).
            
        Parameters
        ----------
        input_data: list
            list of tiff files to read
        target_resolution: tuple
            (Y, X) target grid size in (m, m)
            
        Attributes
        ----------
        input_data : list
            list of input files used
        shape : tuple of ints
            Shape of the grid (y,x) (rows,columns)
        resolution : tuple of ints
            resolution of grid elements in m (y,x)
        grid : array
                This 3d array is the grid data at each time step. 
            The first dimension is the time step with 0 being the initial data.
            The second dimension is the flat grid for given cohort, mapped using  
            key_to_index. The third dimension is the grid element. Each cohort
            can be reshaped using  shape to get the proper grid
        init_grid: np.ndarray 
                The initial data corrected to the target resolution. Each
            row is one cohort percent grid flattened to a 1d array. The 
            the index to get a given cohort can be looked up in the 
            key_to_index attribute.
        key_to_index : dict
                Maps canon cohort names to the index for that cohort in the 
            data object 
        raster_info : dict of RASTER_METADATA
            Metadata on each of the initial raster files read
        
        
        """
        input_data = config['input data'] 
        target_resolution = config['target resolution']
        self.start_year = int(config['start year'])
        
        self.input_data = input_data
        ## read input
        ## rename init_grid??
        self.init_grid, self.raster_info, self.key_to_index = \
            self.read_layers(target_resolution)
        
        ## rename grid_history?
        self.grid = [self.init_grid]
        
        self.check_mass_balance() ## check mass balance at initial time_step
        
        #get resolution, and shape of gird data as read in
        original = self.raster_info.values()[0]
        o_shape = (original.nY, original.nX) 
        o_res = (original.deltaY, original.deltaX) 
        self.shape = (
            abs(int(o_shape[ROW] *o_res[ROW] /target_resolution[ROW])),
            abs(int(o_shape[COL] *o_res[COL] /target_resolution[COL])),
        )
        self.resolution = target_resolution
        
    def __getitem__ (self, key):
        """Gets cohort data.
        
        Can get data for a cohort at all time steps, all cohorts at a ts, 
        or a cohort at a given ts
        
        Parameters
        ----------
        key: Str, int, or tuple(int,str)
            if key is a string, it should be a canon cohort name.
            if key is an int, it should be a year >= start_year, 
            but < start_year + len(grid)
            if key is tuple, the int should fit the int requirements, and the 
            string the string requirements. 
            
        Returns
        -------
        np.array
            if key is a string, 3D, dimension are [timestep][grid row][grid col],
            timestep is year(key) - start year
            if key is a int, 3D, dimension are [cohort #][grid row][grid col],
            use key_to_int to find cohort #
            if key is tuple, 2D, [grid row][grid col]
        """
        if type(key) is str: ## cohort at all ts
            get_type = 'cohort' 
        elif type(key) is int: ## all cohorts at a ts
            get_type = 'ts' 
        else: # tuple ## a cohort at a ts
            get_type = 'cohort at ts' 
            
            
        if 'cohort' == get_type: 
            return self.get_cohort(key, False)
        elif 'ts' == get_type:
            year = key - self.start_year
            return self.get_all_cohorts_at_time_step(year, False)
        elif 'cohort at ts' == get_type:
            year, cohort = key
            year = year-self.start_year
            return self.get_cohort_at_time_step(cohort, year, False)
        
        
    def read_layers(self, target_resolution):
        """Read cohort layers from raster files
        
        Parameters
        ----------
        target_resolution: tuple of ints
            target resolution of each grid element (y,x)
            
        Returns
        -------
        Layers : np.ndarray
            2d array of flattened cohort grids, corrected to the proper
        resolution, and normalized. First dimension is layer index, which can be 
        found with the keys_to_index dict. The second dimension is gird element 
        index.
        metadata_dict : dict
            metadata for each raster loaded. Keys being canon name of layer
        keys_to_index : dict
            Maps each canon cohort name to the int index used in layer grid 
        """
        layers = []
        metadata_dict = {}
        key_to_index = {}
        idx = 0
        shape, resolution = None, None
        
        for f in self.input_data:
            ## add path here
            path = f
            data, metadata = load_raster (path)
            
            ## set init shape and resolution
            ## TODO maybe do this differently 
            if shape is None:
                shape = (metadata.nY,metadata.nX)
            elif shape != (metadata.nY,metadata.nX):
                raise StandardError, 'Raster Size Mismatch'
                
            if resolution is None:    
                resolution = (abs(metadata.deltaY),abs(metadata.deltaX))
            elif resolution != (abs(metadata.deltaY), abs(metadata.deltaX)):
                raise StandardError, 'Resolution Size Mismatch'
            
            try:
                filename = os.path.split(f)[-1]
                name = find_canon_name(filename.split('.')[0])
            except KeyError as e:
                print e
                continue
            ## update key to index map, metadata dict, layers, 
            ## and increment index
            key_to_index[name + '--0'] = idx
            slice_start = idx
            idx += 1 # < moved here because of the loop in a bit
        
            metadata_dict[name] = metadata

            
            cohort_year_0 = self.resize_grid_elements(
                data, resolution, target_resolution
            )
            layers.append( cohort_year_0 ) 
            
            flat_grid_size = len(cohort_year_0) 
            num_years = 1 # < to be set based on cohort age range later
            for age in range(1, num_years):
                layers.append(np.zeros(flat_grid_size))
                key_to_index[name + '--' + str(idx) ] = idx
                idx += 1
            slice_end = idx
            key_to_index[name] = slice(slice_start,slice_end)
           
        layers = self.normalize_layers(
            np.array(layers), resolution, target_resolution
        )
        #~ print layers
        return layers, metadata_dict, key_to_index
       
    ## make a static method?
    def normalize_layers(self, layers, current_resolution, target_resolution):
        """Normalize Layers. Ensures that the fractional cohort areas in each 
        grid element sums to one. 
        """
        total = layers.sum(0) #sum fractional cohorts at each grid element
        cohorts_required = \
            (float(target_resolution[ROW])/(current_resolution[ROW])) * \
            (float(target_resolution[COL])/(current_resolution[COL]))

        cohort_check = total / cohorts_required
        ## the total is zero in non study cells. Fix warning there
        adjustment = float(cohorts_required)/total

        check_mask = cohort_check > .5
        new_layers = []
        for layer in layers:
            
            layer_mask = np.logical_and(check_mask,(layer > 0))
            layer[layer_mask] = np.multiply(
                layer,adjustment, where=layer_mask)[layer_mask]
            
            layer = np.round((layer) / cohorts_required, decimals = 6)
            new_layers.append(layer)
        new_layers = np.array(new_layers)
        return new_layers
    
    ## make a static method?
    def resize_grid_elements (self, 
        layer, current_resolution, target_resolution):
        """resize cells to target resolution
        
        Parameters
        ----------
        layer : np.ndarray
            2d raster data
        current_resolution: tuple of ints
            current resolution of each grid element (y,x)
        target_resolution: tuple of ints
            target resolution of each grid element (y,x)
            
        Returns 
        -------
        np.ndarray
            flattened representation of resized layer
        """
        ## check that this is correct
        if target_resolution == current_resolution:
            layer[layer<=0] = 0
            layer[layer>0] = 1
            return layer.flatten()
        
        resize_num = (
            abs(int(target_resolution[ROW]/current_resolution[ROW])),
            abs(int(target_resolution[COL]/current_resolution[COL]))
        )
        resized_layer = []
        
        shape = layer.shape
        
        ## regroup at new resolution
        for row in range(0, int(shape[ROW]), resize_num[ROW]):
            for col in range(0, int(shape[COL]), resize_num[COL]):
                A = layer[row : row+resize_num [ROW], col:col + resize_num[COL]]
                b = A > 0
                resized_layer.append(len(A[b]))
        
        return np.array(resized_layer)
        
        
    def get_cohort_at_time_step (self, cohort, time_step = -1, flat = True):
        """Get a cohort at a given time step
        
        Parameters
        ----------
        cohort: str
            canon cohort name
        time_step: int, defaults -1
            time step to retrieve, default is last time step
        flat: bool
            keep the data flat, or convert to 2d grid with correct dimension
            
        Returns
        -------
        np.array
            The cohorts fractional area grid at a given time step. 
        """
        cohort = self.key_to_index[cohort]
        
        
        r_val = self.grid[time_step][cohort]
        if type(cohort) is slice:
            # sum all age buckets for cohort      
            r_val = r_val.sum(0)
       
        if flat:
            return r_val
        else: 
            return r_val.reshape(
                self.shape[ROW], self.shape[COL]
            )
    
    ## NEED TO TEST
    def get_cohort (self, cohort, flat = True):
        """Get a cohort at all time steps
        
        Parameters
        ----------
        cohort: str
            canon cohort name
        flat: bool
            keep the data flat, or convert to 2d grid with correct dimensions
            
        Returns
        -------
        np.array
            The cohorts fractional area grid at all time steps. 
        """
        cohort = self.key_to_index[cohort]
        
        
        r_val = np.array(self.grid)[:,cohort]
        if type(cohort) is slice:
            # sum all age buckets for cohort      
            r_val = r_val.sum(1)
        
        if flat:
            # sum all age buckets for cohort(check1)
            return r_val
        else:
            return r_val.reshape(len(self.grid),
                self.shape[ROW], self.shape[COL])
                
    def get_all_cohorts_at_time_step (self, time_step = -1, flat = True):
        """Get all cohorts at a given time step
        
        Parameters
        ----------
        time_step: int, defaults -1
            time step to retrieve, default is last time step
        flat: bool
            keep the data flat, or convert to 2d grid with correct divisions
            
        Returns
        -------
        np.array
            all cohorts fractional area grids at a given time step in a 2d 
        array. 
        """
        ## do we want this to sum the age buckets
        if flat:
            # sum all age buckets for cohort
            return self.grid[time_step] 
        else:
            return self.grid[time_step].reshape(len(self.init_grid),
                self.shape[ROW], self.shape[COL])
                
    def check_mass_balance (self, time_step=-1):
        """reruns true if mass balance is preserved. Raises an exception, 
        otherwise
        
        Parameters 
        ----------
        time_step : int, defaults -1
            time step to test
        
        Raises
        ------
        MassBalanceError
            if any grid element at time_step is <0 or >1
        
        Returns
        -------
        Bool
            True if no mass balance problem found.
        """
        grid = self.grid[time_step]
        
        ATTM_Total_Fractional_Area = np.round(grid.sum(0), decimals = 6 )
        if (np.round(ATTM_Total_Fractional_Area, decimals = 4) > 1.0).any():
            raise MassBalanceError, 'mass balance problem 1'
            ## write a check to locate mass balance error
        if (np.round(ATTM_Total_Fractional_Area, decimals = 4) < 0.0).any():
            raise MassBalanceError, 'mass balance problem 2'
            
        return True
        
    ## don't need a set_cohort, because we only want to set one ts at a time
    ## really only the most recent time_step.
    def set_cohort (self, cohort, data):
        """If implemented should set a cohort at all time steps
        
        Parameters
        ----------
        cohort: str
            canon name of cohort
        data: array like
        """
        raise NotImplementedError, 'cannot set a cohort at all time steps'
    
    def set_cohort_at_time_step(self, cohort, time_step, data):
        """Set a cohort at a given time step
        
        Parameters
        ----------
        cohort: str
            canon name of cohort
        time_step: int
            0 <= # < len(grid)
        data: np.ndarray
            2D array with shape matching shape attribute
            
        Raises
        ------
        StandardError
            bad shape
        """
        if cohort.find('--') == -1:
            raise StandardError, 'needs the age set'
        idx = self.key_to_index[cohort]
        if data.shape != self.shape:
            raise StandardError, 'Set shape Error'
        
        self.grid[time_step][idx] = data.flatten()
        
    def set_all_cohorts_at_time_step(self, time_step, data):
        """Sets all cohorts at a time step
        
        
        Parameters
        ----------
        time_step: int
            0 <= # < len(grid)
        data: np.ndarray
            3D array with shape rebroadcastable to init_grid.shape())
            i.e [cohorts][ages][grid]
        """
        shape = self.init_grid.shape
        self.grid[time_step] = data.reshape(shape)
        
         
    def __setitem__ (self, key, data):
        """Set cohort data. 
        
        Can set a grid for a cohort(or all cohorts) at a timestep. Will add 
        time step id desired time step == len(grid)
        
        Parameters
        ----------
        key: Str, int, or tuple(int,str)
            if key is a string, raises NotImplementedError
            if key is an int, it should be a year >= start_year, 
            but <= start_year + len(grid)
            if key is tuple, the int should fit the int requirements, and the 
            string should be a canon cohort name
        data: np.ndarray
            data of the proper shape. for tuple key shape = shape attribute, 
            else rebroadcastable to shape of init_grid
            
        Raises
        ------
        NotImplementedError
            if key is str, 'cannot set a cohort at all time steps'
        KeyError, 
            if key's year value < star_year or > star_year + len(grid)
        """
        if type(key) is str: ## cohort at all ts
            #~ get_type = 'cohort' 
            raise NotImplementedError, 'cannot set a cohort at all time steps'
        elif type(key) is int: ## all cohorts at a ts
            get_type = 'ts' 
            year = key
        else: # tuple ## a cohort at a ts
            get_type = 'cohort at ts' 
            year, cohort = key
            
        if year == self.start_year + len(self.grid):
            ## year == end year + 1 
            ## (I.e start_year == 1900, len(grid) =10, year = 1910)
            ## time steps from 0 - 9, (1900 - 1909)
            ## year - star_year = 10, no 10 as a time,
            ## but 10 == year - star_year, or 1910 == start_year+len(grid)
            ## so, will add a new grid year, because it is end +1, and set 
            ## values to 0
            self.append_grid_year(True)
        elif year > self.start_year + len(self.grid):
            raise KeyError, 'Year too far after current end'
        elif year < self.start_year:
            raise KeyError, 'Year before start year'
        
            
        if  'ts' == get_type:
            ts = year - self.start_year
            self.set_all_cohorts_at_time_step(ts, data)
        elif  'cohort at ts' == get_type:
            ts = year - self.start_year
            self.set_cohort_at_time_step(cohort, ts, data)
            
        
    def append_grid_year (self, zeros=False):
        """adds a new grid timestep and exact copy of the previous timestep
        
        Parameters
        ----------
        zeros : bool
            set new years data to 0 if true
        """
        self.grid.append(self.grid[-1])
        if zeros:
            self.grid[-1] = self.grid[-1]*0
    
    def save_cohort_at_time_step (self, cohort, path,
            time_step = -1, bin_only = True, binary_pixels = False):
        """various save functions should be created to save, reports, images, 
        or videos
        
        returns base file name
        """
        cohort_data = self.get_cohort_at_time_step(
            cohort, time_step, flat = False
        )
        
        if binary_pixels:
            ## see if cohort is present or not
            cohort_data[cohort_data>0] = 1
        #~ self.ts_to_year(time_step)
        year = 'TEMP_YEAR'
        filename = cohort+ "_Fractional_Area_" + str(year)
        bin_path = os.path.join(path, filename + '.bin')
        save_bin(cohort_data, bin_path)
        if not bin_only:
            img_path = os.path.join(path, filename + '.png')
            save_img(cohort_data, img_path, filename) # pretty names
            
        return filename
            
            
        
def test (files):
    """
    """
    config = {
        'target resolution': (1000,1000),
        'start year': 1900,
        'input data': files,
    }
    
    return CohortGrid(config)