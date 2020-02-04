#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions for aerosols calculations for chem_opt = 201 WRF-Chem.

Created on Wed Jan  8 10:45:57 2020

@author: Caterina Mogno - c.mogno@ed.ac.uk
"""

from WRFChemToolkit.analysis import utils as utl


def calculate_pm25_species_3bins(ds):
    
    """
    Add to datset each aerosol species contribution to pm2.5 in ug m-3.

    :param ds: WRF-chem output.
    :type ds: xarray DataSet.
    :return: Dataset with added components.
    :rtype: xarray DataSet.
    
    """
    
    # List of aerosol species contributing to PM25. According to WRF-Chem code 
    # in module_mosaic_sumpm.F subroutine sum_pm_mosaic_vbs0.
    
    species = ['so4','nh4','no3','biog1_o','biog1_c','smpbb','smpa',
               'glysoa_sfc','oc', 'bc', 'oin','na','cl']
    
    conversion = ds['ALT'] # inverse densitiy.
    
    # Calculating contributions: summing up the first 3 bins 
    # (diameter < 2.5 um) for each species.
    for species in species:
      ds['pm25_'+ species] = utl._sum_(ds[species + '_a01'],
                              ds[species + '_a02'],
                              ds[species + '_a03']
                              )/conversion
      ds['pm25_'+ species].attrs['units']= 'ug m-3'
      


def calculate_total_pm25(ds):
    """
    Add to dataset the calculated pm2.5 in ug m-3. Should be equal to the 
    WRF-Chem variable PM2_5_DRY. Calcualation for sum follows the calculation 
    in WRF-Chem module_mosaic_sumpm.F subroutine sum_pm_mosaic_vbs0.
    Need to call function calculate_pm25_species_3bins before use.

    :param ds: WRF-chem output.
    :type ds: xarray DataSet.
    :return: Dataset with added tot pm2.5 component.
    :rtype: xarray DataSet.
    
    """

    ds['pm25_calc'] =utl._sum_(
                           ds['pm25_biog1_o'],  # SOA.
                           ds['pm25_biog1_c'], 
                           ds['pm25_smpbb'],
                           ds['pm25_smpa'], 
                           ds['pm25_glysoa_sfc'],
                           ds['pm25_so4'],  # SIA.
                           ds['pm25_nh4'],
                           ds['pm25_no3'],                           
                           ds['pm25_bc'],                         
                           ds['pm25_na'],   # seasalt.
                           ds['pm25_cl'],                           
                           ds['pm25_oc'],   # POA.
                           ds['pm25_oin']   # dust.
                           )
    
    ds['pm25_calc'].attrs['units']= 'ug m-3'
    


def calculate_pm25_components(ds):
    
    """
    Calcualtes and add to dataset SIA, SOA, POA, dust, seasalt contributions 
    to PM2.5. NB: BC contribution is
    Need to call function calculate_pm25_species_3bins before use.

    :param ds: WRF-chem output.
    :type ds: xarray DataSet.
    :return: Dataset with added components.
    :rtype: xarray DataSet.
    
    """
    
    # Secondary Organic Aerosols SOA.
    ds['pm25_SOA'] =utl._sum_(ds['pm25_biog1_o'],
                          ds['pm25_biog1_c'], 
                          ds['pm25_smpbb'],
                          ds['pm25_smpa'], 
                          ds['pm25_glysoa_sfc']
                          )   
    ds['pm25_SOA'].attrs['units'] = 'ug m-3'
    
    # Secondary Inorganic Aerosols SIA.
    ds['pm25_SIA'] = utl._sum_(ds['pm25_so4'],
                           ds['pm25_nh4'],
                           ds['pm25_no3']
                           )
    ds['pm25_SIA'].attrs['units'] = 'ug m-3'
    
    #Primary Organic Aerosols
    ds['pm25_POA'] = ds['pm25_oc']
    
    #Seasalt
    ds['pm25_seasalt'] = utl._sum_(ds['pm25_na'], ds['pm25_cl'])
    ds['pm25_seasalt'].attrs['units'] = 'ug m-3'
    
    #Dust
    ds['pm25_dust'] = ds['pm25_oin']
    
    

def get_aerosols(ds):
    
    """
    This function creates a dataset with all the pm2.5 useful data from 
    the WRF-Chem output.
    
    :param ds: WRF-chem output.
    :type ds: xarray DataSet.
    :return: Reduced dataset with pm25 data.
    :rtype: xarray DataSet.
    
    """
    
    #list of relevant aerosols variables for pm2.5.
    aerosols = [
        'so4_a01','so4_a02', 'so4_a03', 'so4_a04', # sulfate.
        'no3_a01','no3_a02', 'no3_a03', 'no3_a04', # nitrate.
        'nh4_a01','nh4_a02', 'nh4_a03', 'nh4_a04', # ammonium.
        'bc_a01','bc_a02', 'bc_a03', 'bc_a04', # black carbon.
        'oc_a01','oc_a02', 'oc_a03', 'oc_a04', # organic carbon (POA).
        'smpa_a01','smpa_a02', 'smpa_a03', 'smpa_a04', # anthro SOA.
        'smpbb_a01','smpbb_a02', 'smpbb_a03', 'smpbb_a04', # biomass burning SOA.
        'biog1_o_a01','biog1_o_a02', 'biog1_o_a03', 'biog1_o_a04', # biogenic SOA (isporene).
        'biog1_c_a01','biog1_c_a02', 'biog1_c_a03', 'biog1_c_a04', # biogenic SOA (pinenes).       
        'glysoa_sfc_a01','glysoa_sfc_a02', 'glysoa_sfc_a03', 'glysoa_sfc_a04',  # glyoxal SOA.      
        'oin_a01','oin_a02', 'oin_a03', 'oin_a04', # dust.
        'na_a01','na_a02', 'na_a03', 'na_a04', # seasalt (sodium).
        'cl_a01','cl_a02', 'cl_a03', 'cl_a04', # seasalt (cloride).
        'PM2_5_DRY', # dry pm2.5 (prognostic variable).
        'water_a01','water_a02', 'water_a03', 'water_a04', # wet pm2.5 component.
        'num_a01','num_a02', 'num_a03', 'num_a04', # pm2.5 density number.
        'ALT' #inverse density.
        ]
    
    ds_aer = utl._get_data_subset_(ds,aerosols)
    calculate_pm25_species_3bins(ds_aer)
    calculate_total_pm25(ds_aer)
    calculate_pm25_components(ds_aer)
    
    return ds_aer
    

    


 