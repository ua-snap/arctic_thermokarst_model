"""test_ice_grid.py
"""
import unittest
from context import atm
from atm.grids import lake_pond_grid

import os
import numpy as np

class TestLakePondGridClass_random(unittest.TestCase):
    """test the IceGrid class with random ice types set
    """
    def setUp(self):
        """setup class for tests 
        """
        config = lake_pond_grid.config_ex
        
        config['pickle path'] = 'test_pickles'
        try:
            os.makedirs(config['pickle path'])
        except:
            pass
        
        self.lake_pond = lake_pond_grid.LakePondGrid(config)
    
    def tearDown(self):
        """
        """
        try:
            pass
            os.remove(self.lake_pond.pickle_path)
            os.removedirs('test_pickles')
        except:
            pass
        
    def test_init(self):
        """test init results are correct
        """
        self.assertEqual( (10,10), self.lake_pond.shape )
        self.assertEqual( 1900, self.lake_pond.start_year )
        
        self.assertEqual( 12, len(self.lake_pond.counts))
        
        for item in self.lake_pond.counts:
            self.assertEqual( 0, self.lake_pond.counts[item][0])
        
        for item in self.lake_pond.depths:
            self.assertEqual( (10*10,), self.lake_pond.depths[item].shape)
            self.assertEqual('float64', self.lake_pond.depths[item].dtype)
        
        for item in self.lake_pond.time_since_growth:
            self.assertEqual( (10*10,), self.lake_pond.time_since_growth[item].shape)
        
        for item in lake_pond_grid.config_ex['lake types']:
            self.assertTrue(
                np.logical_and(
                    lake_pond_grid.config_ex['lake depth range'][0] <=\
                        self.lake_pond.depths[item],
                    lake_pond_grid.config_ex['lake depth range'][1] >=\
                        self.lake_pond.depths[item],
                ).all()
            )
            
        for item in lake_pond_grid.config_ex['pond types']:
            self.assertTrue(
                np.logical_and(
                    lake_pond_grid.config_ex['pond depth range'][0] <=\
                        self.lake_pond.depths[item],
                    lake_pond_grid.config_ex['pond depth range'][1] >=\
                        self.lake_pond.depths[item],
                ).all()
            )
            
        self.assertTrue(
            np.logical_and(
                lake_pond_grid.config_ex['ice depth alpha range'][0] <=\
                    self.lake_pond.ice_depth_constants,
                lake_pond_grid.config_ex['ice depth alpha range'][1] >=\
                    self.lake_pond.ice_depth_constants
            ).all()
        )
            
        self.assertEqual( (10*10,), self.lake_pond.ice_depth.shape)
        self.assertEqual( 
            (10*10,), self.lake_pond.climate_expansion_lakes.shape
        )
        self.assertEqual(
            (10*10,), self.lake_pond.climate_expansion_ponds.shape
        )

            
    def test_current_year (self):
        """ Function doc """
        self.assertEqual(1900, self.lake_pond.current_year())
        self.lake_pond.increment_time_step(False)
        self.assertEqual(1901, self.lake_pond.current_year())
        
    def test_apply_mask (self):
        """"""
        mask = np.ones(100)
        mask[:50] = 0
        mask = mask == 1
        self.lake_pond.apply_mask('Pond_WT_Y', mask)
        
        test = np.zeros(100) + .3
        test[:50] = 0
        

        self.assertTrue(
            (test == self.lake_pond['Pond_WT_Y', 1900].flatten()
        ).all())
        
        
        
        
    
            
    def test_increment_time_step (self):
        """ test incrmetn time step, load history"""
        self.assertEqual(1900, self.lake_pond.current_year())
        self.lake_pond['Pond_WT_Y'] = \
            self.lake_pond['Pond_WT_Y',self.lake_pond.current_year()] - \
            self.lake_pond['Pond_WT_Y', self.lake_pond.current_year()]
        self.lake_pond.increment_time_step()
        self.lake_pond['Pond_WT_Y'] = \
            self.lake_pond['Pond_WT_Y', self.lake_pond.current_year()] + 1
        self.assertEqual(1901, self.lake_pond.current_year())
        
        self.assertTrue(
            (
                1 == self.lake_pond['Pond_WT_Y', self.lake_pond.current_year()]
            ).all()
        )
        self.lake_pond.increment_time_step()
        self.lake_pond['Pond_WT_Y'] = \
            self.lake_pond['Pond_WT_Y', self.lake_pond.current_year()] + 1
        self.assertTrue(
            (
                2 == self.lake_pond['Pond_WT_Y', self.lake_pond.current_year()]
            ).all()
        )
        
        ## test load from pickle
        self.assertTrue(
            (
                1 == self.lake_pond['Pond_WT_Y', 1901]
            ).all()
        )
        self.assertTrue(
            (
                0 == self.lake_pond['Pond_WT_Y', 1900]
            ).all()
        )
        
        
    def test__getitem__ (self):
        """## todo need to test exceptions
        """
        items = self.lake_pond['Pond_WT_Y']
        self.assertEqual(1,len(items))
        
        self.lake_pond['Pond_WT_Y'] = \
            self.lake_pond['Pond_WT_Y',self.lake_pond.current_year()] - \
            self.lake_pond['Pond_WT_Y', self.lake_pond.current_year()]
        
        self.lake_pond.increment_time_step()
        self.lake_pond['Pond_WT_Y'] = \
            self.lake_pond['Pond_WT_Y', self.lake_pond.current_year()] + 1

        self.lake_pond.increment_time_step()
        self.lake_pond['Pond_WT_Y'] = \
            self.lake_pond['Pond_WT_Y', self.lake_pond.current_year()] + 1
        
        # test get item at time
        ## test load current
        self.assertTrue(
            (
                2 == self.lake_pond['Pond_WT_Y', self.lake_pond.current_year()]
            ).all()
        )
        
        ## test load from pickle
        self.assertTrue(
            (
                1 == self.lake_pond['Pond_WT_Y', 1901]
            ).all()
        )
        self.assertTrue(
            (
                0 == self.lake_pond['Pond_WT_Y', 1900]
            ).all()
        )
        
        # test get shapshot, old, current
        items = self.lake_pond[1900]
        self.assertTrue((0 == items['Pond_WT_Y']).all())
        items = self.lake_pond[1902]
        self.assertTrue((2 == items['Pond_WT_Y']).all())
        
        # test get history
        items = self.lake_pond['Pond_WT_Y']
        self.assertEqual(3, len(items))
        for i in range(3):
            self.assertTrue((i == items[i]).all())
            
    def test_count_feature (self):
        self.assertEqual(0, self.lake_pond.get_count('Pond_WT_Y')[0])
        self.lake_pond.set_count('Pond_WT_Y', np.zeros((10,10))+10)
        self.assertEqual(10, self.lake_pond.get_count('Pond_WT_Y')[0])
        
        
        self.lake_pond.increment_time_step()
        self.lake_pond.increment_time_step()
        
        self.lake_pond.set_count('Pond_WT_Y', np.zeros((10,10))+20)
        self.assertEqual(20, self.lake_pond.get_count('Pond_WT_Y')[0])
        
        self.lake_pond.write_to_pickle(self.lake_pond.time_step)
        data = self.lake_pond.read_from_pickle()
        count = [ ts['counts']['Pond_WT_Y'][0] for ts in data]
        self.assertEqual(3, len(count))
        self.assertEqual([10,10,20], count)
        
    def test_read_pickle(self):
        
        self.lake_pond.increment_time_step()
        self.lake_pond.set_count('Pond_WT_Y', np.zeros((10,10))+10)
        self.lake_pond.increment_time_step()
        
        self.lake_pond.set_count('Pond_WT_Y', np.zeros((10,10))+20)
        self.lake_pond.increment_time_step()
        self.lake_pond.set_count('Pond_WT_Y', np.zeros((10,10))+30)
        
        #~ self.lake_pond.write_to_pickle(self.lake_pond.time_step)
        data = self.lake_pond.read_from_pickle(set_current= True)
        count = [ ts['counts']['Pond_WT_Y'][0] for ts in data]
        self.assertEqual(3, len(count))
        self.assertEqual([0,10,20], count)
        self.assertEqual(2, self.lake_pond.time_step)
        
    def test_load_pickle (self):
        """
        """
        self.lake_pond.increment_time_step()
        self.lake_pond.set_count('Pond_WT_Y', np.zeros((10,10))+10)
        self.lake_pond.increment_time_step()
        
        self.lake_pond.set_count('Pond_WT_Y', np.zeros((10,10))+20)
        self.lake_pond.increment_time_step()
        self.lake_pond.set_count('Pond_WT_Y', np.zeros((10,10))+30)
        
        self.lake_pond.write_to_pickle(self.lake_pond.time_step)
        
        
        new = lake_pond_grid.LakePondGrid(self.lake_pond.pickle_path)
        
        self.assertTrue(
            (new.depths['Pond_WT_Y'] == self.lake_pond.depths['Pond_WT_Y'] ).all()
        )
        self.assertTrue(
            (new.depths['LargeLakes_WT_Y'] == \
            self.lake_pond.depths['LargeLakes_WT_Y']).all()
        )
        
        self.assertTrue(
            (new.counts['Pond_WT_Y'] ==\
                self.lake_pond.counts['Pond_WT_Y'] ).all()
        )

        self.assertEqual(new.start_year, self.lake_pond.start_year)
        self.assertEqual(new.pickle_path, self.lake_pond.pickle_path)
        self.assertEqual(new.time_step, self.lake_pond.time_step)
        self.assertEqual(new.shape, self.lake_pond.shape)
        self.assertTrue(
            (new.ice_depth_constants == \
            self.lake_pond.ice_depth_constants).all()
        )
        


if __name__ == '__main__':
    unittest.main()