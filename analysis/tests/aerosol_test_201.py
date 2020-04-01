#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for functions/aerosols_201.py functions.

Created on Thu Jan  9 10:57:07 2020

@author: Caterina Mogno c.mogno@ed.ac.uk
"""
import numpy as np
import xarray as xr
import sys
sys.path.append('/exports/csce/datastore/geos/users/s1878599/python_code/')
from WRFChemToolkit.analysis import aerosols_201 as ar201

# Load test data.
data_path = '../../../sample_WRF_chem_out_201'
ds = xr.open_dataset(data_path)

# --------------------------- CHEM-OPT = 201 -------------------------------

#TEST1: compare calculated pm25 with diagnostic variable PM2_5_DRY.
ar201.calculate_pm25_species_3bins(ds)
ar201.calculate_total_pm25(ds)

np.testing.assert_allclose(
    ds.pm25_calc.values, ds.PM2_5_DRY.values, rtol=1e-06)
                             

#TEST2: compare calculated pm25 from components with diagnostic variable 
#PM2_5_DRY.
ar201.calculate_pm25_components(ds)
ds['pm25_comp'] = (ds.pm25_SOA + ds.pm25_SIA + ds.pm25_POA + ds.pm25_dust 
                   + ds.pm25_seasalt + ds.pm25_bc)

np.testing.assert_allclose(
    ds.pm25_comp.values, ds.PM2_5_DRY.values, rtol=1e-06)

print('All tests passed for chem_opt=201!')







