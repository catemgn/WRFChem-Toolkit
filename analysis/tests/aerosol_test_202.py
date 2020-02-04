#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for functions/aerosols_202.py functions.

Created on Mon Feb  3 16:20:51 2020

@author: Caterina Mogno c.mogno@ed.ac.uk
"""

import numpy as np
import xarray as xr
from WRFChemToolkit.analysis import aerosols_202 as ar202

# Load test data.
data_path = '../../../sample_WRF_chem_out_202_2'
ds = xr.open_dataset(data_path)

# --------------------------- CHEM-OPT = 202 -------------------------------

#TEST1: compare calculated pm25 with diagnostic variable PM2_5_DRY.
ar202.calculate_pm25_species_3bins(ds)
ar202.calculate_pm25_components(ds)
ar202.calculate_total_pm25(ds)

np.testing.assert_allclose(
    ds.pm25_calc.values, ds.PM2_5_DRY.values, rtol=1e-06)

print('All tests passed for chem_opt=202!')