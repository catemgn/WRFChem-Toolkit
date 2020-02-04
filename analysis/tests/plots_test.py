#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for plot.py functions.

Created on Tue Feb  4 17:23:44 2020

@author: Caterina Mogno c.mogno@ed.ac.uk
"""


from WRFChemToolkit.analysis import plots as plot
import xarray as xr

data_path = '../../../sample_WRF_chem_out_202'
ds = xr.open_dataset(data_path)


# Time average of dataset. For plot need to have a fixed value for time.
ds_tavg=xr.Dataset(dict(ds.mean(dim='Time', keep_attrs=True).data_vars), 
           coords = dict(ds.coords))

# Plot map
plot.map_2D(ds_tavg, 'PM2_5_DRY', title='Test Title: PM2_5_DRY', level=1, 
            mask_values=40, pixels=True, save='2D_map_test', format='png')
