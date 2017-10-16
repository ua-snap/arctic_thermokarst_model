"""ald_grid.py

for the puproses of this file ALD(or ald) refers to Active layer depth,
and PL (or pl) to Protective layer
"""
import numpy as np

from terraingrid import ROW, COL


class ALDGrid(object):
    """ Class doc """
    
    def __init__ (self, config):
        """ Class initialiser """
        
        shape = config['shape']
        cohort_list = config['cohort list']
        init_ald = config ['init ald']
        self.start_year = config ['start year']
        
        ## setup soil properites
        self.porosity = config['porosities']
        self.protective_layer_factor = ['PL factors']
       
        ald, pl, pl_map = self.setup_grid ( shape, cohort_list, init_ald)
        self.init_ald_grid = ald
        self.init_pl_grid = pl
        self.pl_key_to_index = pl_map
        
       
        self.shape = shape
        self.ald_grid = [ self.init_ald_grid ]
        self.pl_grid = [ self.init_pl_grid ]
    
        
    def __getitem__ (self, key):
        """Gets ALD or PL or PL for a cohort
        
        Parameters
        ----------
        key: str, tuple (str, int)
        
        Raises
        ------
        NotImplementedError:
            get ALD or PL at all time steps functions not implemented
        KeyError:
            if key is does not meet key requirments
        
        Returns
        -------
        np.array
            requested grid, each grid will match the shape attribute
        """
        if type(key) is str:
            if key == 'ALD':
                return self.get_ald(flat = False)
            elif key == 'PL':
                #return self.get_pl()
                raise NotImplementedError, 'get all PL ts not implemented'
            else:
                raise KeyError, 'String key must be ALD, or PL'
               
        elif type(key) is tuple:
            if key[0] == 'ALD':
                if type(key[1]) is int:
                    ts = key[1] - self.start_year
                    return self.get_ald_at_time_step(ts, False)
                else:
                    raise KeyError, 'Tuple key(ALD) index 1 must be an int'
                
            elif key[0] == 'PL':
                if type(key[1]) is int:
                    ts = key[1] - self.start_year
                    return self.get_pl_at_time_step(ts, flat = False)
                else:
                    raise KeyError, 'Tuple key(PL) index 1 must be an int'
            
            elif key[0] in self.pl_key_to_index.keys():
                if type(key[1]) is int:
                    ts = key[1] - self.start_year
                    return self.get_pl_at_time_step(ts,
                        cohort = key[0], flat = False)
                else:
                    raise KeyError, 'Tuple key(cohort) index 1 must be an int'
            
            else:
                msg = ('Tuple keys first item must be ALD,'
                        ' or PL, or a cohort in pl_grid')
                raise KeyError, msg

        else:
            raise KeyError, 'Key is not a str or tuple.'
        
    def __setitem__ (self, key, value):
        """Set ALD or PL data. 
        
        
        Parameters
        ----------
        key: Str, or tuple(str, int)
            if key is a string, raises NotImplementedError
            if key is tuple, the str should be ALD, PL, or a cohort in the 
            PL grid. the int should start_year <= int <= start_year + len(grid)
        data: np.ndarray
            data of the proper shape, for key provided
            
            
        Raises
        ------
        KeyError: 
            if key does not match key parameters
        NotImplementedError:
            if key is str
        """
        if type(key) is str:
            raise NotImplementedError, 'cannont set whole ALD or PL array'
            
        elif type(key) is tuple:
            if type(key[1]) is int:
                year = key[1]
                if year == self.start_year + len(self.ald_grid):
                ## year == end year + 1 
                ## (I.e start_year == 1900, len(grid) =10, year = 1910)
                ## time steps from 0 - 9, (1900 - 1909)
                ## year - star_year = 10, no 10 as a time,
                ## but 10 == year - star_year, or 1910 == start_year+len(grid)
                ## so, will add a new grid year, because it is end +1, and set 
                ## values to 0
                    self.add_time_step(True)
                elif year > self.start_year + len(self.ald_grid):
                    raise KeyError, 'Year too far after current end'
                elif year < self.start_year:
                    raise KeyError, 'Year before start year'
            else:
                raise KeyError, 'tuple index 1 should be int'
            
            ts = year - self.start_year
            
            if key[0] is 'ALD':
                self.set_ald_at_time_step(ts, value)
            elif key[0] == 'PL':
                self.set_pl_at_time_step(ts, value)
            elif key[0] in self.pl_key_to_index.keys():
                self.set_pl_cohort_at_time_step(ts, key[0], value)
            else: 
                msg = ('Tuple keys first item must be ALD,'
                        ' or PL, or a cohort in pl_grid')
                raise KeyError, msg
        else:
            raise KeyError, 'Key is not a str or tuple.'
        
        
    def setup_grid (self, shape, cohorts, init_ald, pl_modifiers = {}):
        """
        
        Parameters
        ----------
        dimensions: tuple of ints
            size of grid
        cohorts: list 
            list of cohorts in model domain
        init_ald: tuple, 2d array, of filename
            if it is as tuple it should have 2 elements (min, max)
        """
        ## TODO READ pl_modifiers from config
        
        if type(init_ald) is tuple:
            ald_grid = self.random_grid(shape, init_ald)
        else:
            ald_grid = self.read_grid(init_ald)
        
        if pl_modifiers == {}:
            pl_modifiers = {key: 1 for key in cohorts}
        
        ## protective layer (pl)
        pl_grid = []
        pl_key_to_index = {}
        index = 0 
        for cohort in cohorts:
            pl_grid.append(ald_grid * pl_modifiers[cohort]) 
            pl_key_to_index[ cohort ] = index
            index += 1
            
        return ald_grid, np.array(pl_grid), pl_key_to_index
        ## need to add random chance + setup for future reading of values

    def random_grid (self, shape, init_ald):
        """ Function doc """
        return np.random.uniform(init_ald[0],init_ald[1], shape ).flatten()
    
    def read_grid (self, init_ald):
        """Read init ald from file or object"""
        raise NotImplementedError
        
    def get_ald_at_time_step (self, time_step = -1, flat = True):
        """returns ald at a given time step
        
        Parameters
        ----------
        time_step: int, default -1
            timestep to get ald at
        flat: bool
            if true returns 1d array, else reshapes to shape
            
        Returns
        -------
        np.array
            ald at time step
        """
        shape = self.ald_grid[time_step].shape
        if not flat:
            shape = self.shape
        return self.ald_grid[time_step].reshape(shape)
        
    def get_ald (self, flat = True):
        """gets ald grid
        
         Parameters
        ----------
        flat: bool
            if true each year is a 1d array, else each year reshapes to shape
        
        Returns
        -------
        np.array
            the ald grid at all time steps
        """
        shape = tuple([len(self.ald_grid)] + list(self.ald_grid[0].shape))
        if not flat:
            shape = tuple([len(self.ald_grid)] + list(self.shape))
            
        return np.array(self.ald_grid).reshape(shape)
        
    def set_ald_at_time_step (self, time_step, grid):
        """Sets the ALD grid at a time step
        
        Parameters
        ----------
        time_step: int
            time step to set
        grid: np.array
            2D array with shape matching shape attribute
        """
        if grid.shape != self.shape:
            raise StandardError('grid shapes do not match')
        self.ald_grid[time_step] = grid.flatten()
        
    def get_pl_at_time_step (self, time_step, cohort = None, flat = True):
        """gets the ALD grid at a time step
        
        Parameters
        ----------
        time_step: int
            time step to get
        cohort: Str or None
            cohort to return
        flat: bool
            keeps grid flat if true
            
        Returns
        -------
        np.array
            the grid of the cohort, if a cohort is provided, other wise
            returns all cohorts. Data is reshaped to grid shape if flat is
            false
        """
        if cohort is None:
            if flat:
                return pl_self.grid[time_step] 
            else:
                return self.pl_grid[time_step].reshape(
                    len(self.init_pl_grid),
                    self.shape[ROW],
                    self.shape[COL]
                )
        # else get cohort
        cohort = self.pl_key_to_index[cohort]
        r_val = self.pl_grid[time_step][cohort]
        if flat:
            return r_val
        else: 
            return r_val.reshape(self.shape[ROW], self.shape[COL])
        
        
    def set_pl_at_time_step (self, time_step, data):
        """Sets the PL grid at a time step
        
        Parameters
        ----------
        time_step: int
            time step to set
        grid: np.array
            3D array that can be reshaped to match inital_l_grid shape
        """
        shape = self.init_pl_grid.shape
        self.pl_grid[time_step] = data.reshape(shape)

    def set_pl_cohort_at_time_step (self, time_step, cohort, data):
        """Sets the PL grid for a cohort at a time step
        
        Parameters
        ----------
        time_step: int
            time step to set
        cohort: str
            cohort to set
        grid: np.array
            2d array that can has shape equal to  self.shape
        """
        idx = self.pl_key_to_index[cohort]
        if data.shape != self.shape:
            raise StandardError, 'Set shape Error'
        
        self.pl_grid[time_step][idx] = data.flatten()
        
    def add_time_step (self, zeros = False):
        """adds a time step for ald_grid and pl_grid
        
        Parameters
        ----------
        zeros: bool
            if set to true data is set as all zeros
        
        """
        self.ald_grid.append(self.ald_grid[-1])
        self.pl_grid.append(self.pl_grid[-1])
        if zeros:
            self.ald_grid[-1] = self.ald_grid[-1]*0
            self.pl_grid[-1] = self.pl_grid[-1]*0
        
        
        
    def save_ald (self, time_step):
        """ save ald at time step """
        pass
        