#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for functions/aerosols.py functions.

Created on Thu Jan  9 10:57:07 2020

@author: Caterina Mogno c.mogno@ed.ac.uk
"""

import xarray as xr
from WRFChemToolkit.analysis import aerosols as ar

# Load test data.
data_path = '../../../sample_WRF_Chem_output'
ds = xr.open_dataset(data_path)

print('ok!')

import sys
print(type(sys.path))
#Test calculate_pm25_species_3bins
#ds1 = ar.calculate_pm25_species_3bins(ds)



