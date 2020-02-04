#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for analysis WRFchemToolkit.

Created on Mon Feb  3 15:35:57 2020

@author: Caterina Mogno c.mogno@ed.ac.uk
"""


import xarray as xr


def _sum_(*args):
    """
    Utility function to sum up an arbitrary number of arguments.
    """
    sum = 0
    
    for i in args:
        sum = sum + i
   
    return sum


def _get_data_subset_(ds, var_list):
    
    """
    Utility function to substract from WRF-Chem output a subset of 
    selected variables.

    :param ds: WRF-chem output.
    :type ds: xarray DataSet.
    :param var_list: list of variables name to subset.
    :type ds: list of strings.
    
    :return: reduced dataset with selected variables only.
    :rtype: xarray DataSet.

    """
    
    #create empty dataset with same parent coords.
    subset = xr.Dataset(coords = dict(ds.coords))
    
    #fill subset with selected variables.
    
    for var in var_list:        
        subset[var] = ds[var]
        
    return subset
     