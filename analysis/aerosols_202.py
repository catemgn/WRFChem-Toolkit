#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions for aerosols calculations for chem_opt = 202 WRF-Chem.

Created on Mon Feb 3 15:34:57 2020

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
    # in module_mosaic_sumpm.F subroutine sum_pm_mosaic_vbs4.
    
    species = ['so4','nh4','no3','glysoa_r1','glysoa_r2','glysoa_oh','glysoa_sfc',
               'glysoa_nh4','oc', 'bc', 'oin','na','cl','asoaX','asoa1','asoa2',
               'asoa3', 'asoa4', 'bsoaX','bsoa1','bsoa2', 'bsoa3', 'bsoa4' ]
    
    conversion = ds['ALT'] # inverse densitiy.
    
    # Calculating contributions: summing up the first 3 bins 
    # (diameter < 2.5 um) for each species.
    for species in species:
      ds['pm25_'+ species] = utl._sum_(
                              ds[species + '_a01'], 
                              ds[species + '_a02'],
                              ds[species + '_a03']
                              )/conversion
      ds['pm25_'+ species].attrs['units']= 'ug m-3'
      
      
def calculate_pm25_components(ds):
    
    """
    Calcualtes and add to dataset SIA, SOA, POA, dust, seasalt contributions 
    to PM2.5. 
    Need to call function calculate_pm25_species_3bins before use.
   (NB: BC contribution is already calculated in calculate_pm25_species_3bins).

    :param ds: WRF-chem output.
    :type ds: xarray DataSet.
    :return: Dataset with added components.
    :rtype: xarray DataSet.
    
    """
    
    # Secondary Organic Aerosols SOA.
    ds['pm25_SOA'] =utl._sum_(ds['pm25_glysoa_r1'],
                          ds['pm25_glysoa_r2'], 
                          ds['pm25_glysoa_oh'],
                          ds['pm25_glysoa_nh4'], 
                          ds['pm25_glysoa_sfc'],
                          ds['pm25_asoaX'],
                          ds['pm25_asoa1'],
                          ds['pm25_asoa2'],
                          ds['pm25_asoa3'],
                          ds['pm25_asoa4'],
                          ds['pm25_bsoaX'],
                          ds['pm25_bsoa1'],
                          ds['pm25_bsoa2'],
                          ds['pm25_bsoa3'],
                          ds['pm25_bsoa4']
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
    

def calculate_total_pm25(ds):
    """
    Add to dataset the calculated pm2.5 in ug m-3. Should be equal to the 
    WRF-Chem variable PM2_5_DRY. Calcualation for sum follows the calculation 
    in WRF-Chem module_mosaic_sumpm.F subroutine sum_pm_mosaic_vbs4.
    Need to call function calculate_pm25_species_3bins and 
    calculate_pm25_components before use.

    :param ds: WRF-chem output.
    :type ds: xarray DataSet.
    :return: Dataset with added tot pm2.5 component.
    :rtype: xarray DataSet.
    
    """

    ds['pm25_calc'] =utl._sum_(
                           ds['pm25_SOA'],
                           ds['pm25_SIA'],  
                           ds['pm25_dust'], 
                           ds['pm25_seasalt'],                 
                           ds['pm25_POA'], # POA (organic carbon).
                           ds['pm25_bc']  
                           )
    
    ds['pm25_calc'].attrs['units']= 'ug m-3'
   

def get_aerosols(ds):
    
    """
    This function creates a dataset with all the pm2.5 useful data from 
    the WRF-Chem output.
    
    :param ds: WRF-chem output.
    :type ds: xarray DataSet.
    :return: Reduced dataset with pm25 data.
    :rtype: xarray DataSet.
    
    """
    
    #list of relevant aerosols variables for pm2.5 and pm10.
    aerosols = [
        'so4_a01','so4_a02', 'so4_a03', 'so4_a04', # sulfate.
        'no3_a01','no3_a02', 'no3_a03', 'no3_a04', # nitrate.
        'nh4_a01','nh4_a02', 'nh4_a03', 'nh4_a04', # ammonium.
        'bc_a01','bc_a02', 'bc_a03', 'bc_a04', # black carbon.
        'oc_a01','oc_a02', 'oc_a03', 'oc_a04', # organic carbon (POA). 
        'glysoa_r1_a01','glysoa_r1_a02', 'glysoa_r1_a03', 'glysoa_r1_a04', # glyoxal SOA. 
        'glysoa_r2_a01','glysoa_r2_a02', 'glysoa_r2_a03', 'glysoa_r2_a04',
        'glysoa_sfc_a01','glysoa_sfc_a02', 'glysoa_sfc_a03', 'glysoa_sfc_a04',
        'glysoa_oh_a01','glysoa_oh_a02', 'glysoa_oh_a03', 'glysoa_oh_a04',
        'glysoa_nh4_a01','glysoa_nh4_a02', 'glysoa_nh4_a03', 'glysoa_nh4_a04',       
        'asoaX_a01','asoaX_a02', 'asoaX_a03','asoaX_a04', # anthopogenic SOA.
        'asoa1_a01','asoa1_a02', 'asoa1_a03','asoa1_a04',
        'asoa2_a01','asoa2_a02', 'asoa2_a03','asoa2_a04',
        'asoa3_a01','asoa3_a02', 'asoa3_a03','asoa3_a04',
        'asoa4_a01','asoa4_a02', 'asoa4_a03','asoa4_a04',
        'bsoaX_a01','bsoaX_a02', 'bsoaX_a03','bsoaX_a04', # biogenic SOA.
        'bsoa1_a01','bsoa1_a02', 'bsoa1_a03','bsoa1_a04',
        'bsoa2_a01','bsoa2_a02', 'bsoa2_a03','bsoa2_a04',
        'bsoa3_a01','bsoa3_a02', 'bsoa3_a03','bsoa3_a04',
        'bsoa4_a01','bsoa4_a02', 'bsoa4_a03','bsoa4_a04',        
        'oin_a01','oin_a02', 'oin_a03', 'oin_a04', # dust.
        'na_a01','na_a02', 'na_a03', 'na_a04', # seasalt (sodium).
        'cl_a01','cl_a02', 'cl_a03', 'cl_a04', # seasalt (cloride).
        'PM2_5_DRY', # dry pm2.5 (prognostic variable).
        'num_a01','num_a02', 'num_a03', 'num_a04', # pm2.5 density number.
        'ALT' #inverse density.
        ]
    
    ds_aer = utl._get_data_subset_(ds,aerosols)
    calculate_pm25_species_3bins(ds_aer)
    calculate_pm25_components(ds_aer)
    calculate_total_pm25(ds_aer)
   
    
    return ds_aer
    

    


 