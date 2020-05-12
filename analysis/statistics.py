#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions for recurrent statistics for WRF-Chem outputs.

Created on Thu Jan  9 10:57:07 2020

@author: Caterina Mogno c.mogno@ed.ac.uk
"""

import xarray as xr


def merge_ds(data_path):
 """
  Merge in a single dataset all data linked in the path. To consider multiple
  files the syntax is for example /mydir/wrfout_d01_2010-04-0*.

  :param data_path:
    path to data files.
  :type data_path: string
  :return:
    single dataset of multiple files.
  :rtype: xarray Dataset
 """
 dataset = xr.open_mfdataset(data_path,decode_times=True)
 return dataset


def time_mean(ds, time_nm):
 """
  Make the average over 'Time' dimension of a dataset.

  :param ds:
    dataset to be averaged.
  :type ds: xarray DataSet.
  :param time_nm:
      name of the time time dimension.
  :type time_nm: string.
  :return:
    Time averaged ds.
  :rtype: xarray DataSet.
 """
 return xr.Dataset(dict(ds.mean(dim=time_nm, keep_attrs=True, 
                   skipna=True).data_vars), coords=dict(ds.coords))


def space_mean(ds):
 """
  Make the average over latitute and longitude dimension of a DataSet.

  :param ds:
    dataset to be averaged.
  :type ds: xarray DataSet.
  :return:
    Time averaged ds.
  :rtype: xarray DataSet.
 """
 return xr.Dataset(dict(ds.mean(dim= ['south_north','west_east'],
                     keep_attrs=True, skipna=True).data_vars), 
                     coords=dict(ds.coords))


def space_subset(ds, lat_lim, long_lim ):
    """
    Extract spatial subset of a dataset given lat and long limits.

   :param ds: 
     dataset.
  :type ds: xarray DataSet.
  :return:
     subset of dataset.
  :rtype: xarray DataSet.
 """
    
    s_subset=ds.where((long_lim[0] < ds.XLONG) & (ds.XLONG < long_lim[1]) & 
                (lat_lim[0] < ds.XLAT) & (ds.XLAT < lat_lim[1]), drop=True)
  
    return s_subset