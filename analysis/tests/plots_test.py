#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for plot.py functions.

Created on Tue Feb  4 17:23:44 2020

@author: Caterina Mogno c.mogno@ed.ac.uk
"""


from WRFChemToolkit.analysis import plots as plot
import xarray as xr
import pandas as pd
import sys as sys

data_path = '../../../sample_WRF_chem_out_202'
ds = xr.open_dataset(data_path)


def test_map_2D():
    
    # Time average of dataset. For plot need to have a fixed value for time.
    ds_tavg=xr.Dataset(dict(ds.mean(dim='Time', keep_attrs=True).data_vars), 
           coords = dict(ds.coords))

    # Plot map
    plot.map_2D(ds_tavg, 'PM2_5_DRY', title='Test Title: PM2_5_DRY', level=1, 
            mask_values=40, pixels=True, save='2D_map_test', format='png')


def test_time_series():
    
    #create dates array.
    dates = pd.DatetimeIndex(ds.Time.values)

    # creates space mean
    so2 = ds.so2.mean(dim = ('south_north','west_east'))
    no2 = ds.so2.mean(dim = ('south_north','west_east'))
    nh3 = ds.nh3.mean(dim = ('south_north','west_east'))
    
    # time_series

    plot.time_series(dates,variables= [so2, nh3, no2],labels=['SO2','NH3','NO2'],
            title='Timeseries test', xlabel='Time', ylabel=' mixing ratio')
     
    
# Pick up test from command line
    
    if sys.argv[1] == 'map_2D' :
        print('Testing function map_2D')
        test_map_2D()
        print('Test passed!')
      
    elif sys.argv[1] == 'time_series' :
        print('Testing function time_series')
        test_time_series()
        print('Test passed!')
      
    else:
        print('Unknown function to test. Add name of function to test.')
      
      
      
