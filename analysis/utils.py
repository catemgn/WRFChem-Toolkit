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

def get_tot_pressure(ds):
     """
     Add the total pressure [Pa] from base pressure and perturbation pressure.
     """
     ds["TP"]= ds.PB+ds.P
     ds["TP"].attrs["units"]="Pa"
    

def get_abs_temperature(ds):
    """
    Add the absolute temperature [k] via Poisson's eq.
    
    """
     
    ds["theta"] = ds.T + 300 #potenital temperature
    ds["theta"].attrs["units"]="K"
     
    ds["AT"]=(ds.theta*((ds.PB+ds.P)/1000))**(2/7) # Poisson's eq.
    ds["AT"].attrs["units"]="K"
     
     
     
    
     