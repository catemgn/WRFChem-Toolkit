#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for functions/aerosols_202.py functions.

Created on Mon Feb  3 16:20:51 2020

@author: Caterina Mogno c.mogno@ed.ac.uk
"""

import numpy as np
import xarray as xr

import sys
sys.path.append('/exports/csce/datastore/geos/users/s1878599/python_code/')
from WRFChemToolkit.analysis import aerosols_202 as ar202

# Load test data.
data_path = '../../../sample_WRF_chem_out_202.nc'
ds = xr.open_dataset(data_path)

# --------------------------- CHEM-OPT = 202 -------------------------------

ar202.get_pm_species(ds)
ar202.get_pm_components(ds)
ar202.calculate_tot_pm(ds)
ar202.direct_pm(ds)

#TEST1: compare calculated pm25 with diagnostic variable PM2_5_DRY.           
print('Testing pm2.5 from components')
np.testing.assert_allclose(
           ds.pm25_tot.values, ds.PM2_5_DRY.values,rtol=1e-06)

#TEST2: compare directed calculated pm25 with diagnostic variable PM2_5_DRY.           
print('Testing direc pm2.5 calculation')
np.testing.assert_allclose(
           ds.pm25_dir_tot.values, ds.PM2_5_DRY.values,rtol=1e-06)

#TEST3: compare calculated pm10 with diagnostic variable PM10.
print('Testing pm10')
np.testing.assert_allclose(
           ds.pm10_tot.values, ds.PM10.values,rtol=1e-06)

     
print('All tests passed for chem_opt=202!')