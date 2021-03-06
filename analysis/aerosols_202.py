#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions for aerosols calculations for chem_opt = 202 WRF-Chem.

Created on Mon Feb 3 15:34:57 2020

@author: Caterina Mogno - c.mogno@ed.ac.uk
"""

from WRFChemToolkit.analysis import utils as utl

def get_pm_species(ds):
    
    """
    Add to datset each aerosol species contribution to pm2.5 and pm10 in ug m-3.

    :param ds: WRF-chem output.
    :type ds: xarray DataSet.
    :return: Dataset with added components.
    :rtype: xarray DataSet.
    
    """
     # List of aerosol species contributing to PM. According to WRF-Chem code 
     # in module_mosaic_sumpm.F subroutine sum_pm_mosaic_vbs4.
    
    species = ['so4','nh4','no3','glysoa_r1','glysoa_r2','glysoa_oh','glysoa_sfc',
            'glysoa_nh4','oc', 'bc', 'oin','na','cl','asoaX','asoa1','asoa2',
            'asoa3', 'asoa4', 'bsoaX','bsoa1','bsoa2', 'bsoa3', 'bsoa4','water']
    
    
    conv = ds.ALT # inverse densitiy.
    
    # Calculating contributions for PM2.5: summing up the first 3 bins 
    # (diameter < 2.5 um) for each species.
    
    for sp in species:
        
     #convert species to ug/m3.
    
    # add PM2.5 components.
     ds['pm25_'+ sp] = (utl._sum_(
                              ds[sp + '_a01'], 
                              ds[sp + '_a02'],
                              ds[sp + '_a03']
                              ))/conv
     ds['pm25_'+ sp].attrs['units']= 'ug m-3'
     
     # add PM10 components (PM2.5 + bin04).
     ds['pm10_'+ sp] =( ds['pm25_'+ sp] + (ds[sp + '_a04']/ds.ALT))
        

        
        
def get_pm_components(ds):
    
    """
    Once calculated PM species, this function calcualtes and add to dataset 
    SIA, SOA, POA, dust, seasalt contributions to PM2.5 and PM10. 
    (NB: BC contribution is already calculated in get_pm_species).

    :param ds: WRF-chem output.
    :type ds: xarray DataSet.
    :return: Dataset with added components.
    :rtype: xarray DataSet.
    
    """
        
    #PM2.5
    
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
    
    ds['pm25_glySOA'] =utl._sum_(ds['pm25_glysoa_r1'],
                          ds['pm25_glysoa_r2'], 
                          ds['pm25_glysoa_oh'],
                          ds['pm25_glysoa_nh4'], 
                          ds['pm25_glysoa_sfc'])
    ds['pm25_glySOA'].attrs['units'] ='ug m-3'
     
    ds['pm25_aSOA'] =utl._sum_(ds['pm25_asoaX'],
                          ds['pm25_asoa1'],
                          ds['pm25_asoa2'],
                          ds['pm25_asoa3'],
                          ds['pm25_asoa4'])
    ds['pm25_aSOA'].attrs['units'] ='ug m-3'
     
    ds['pm25_bSOA'] =utl._sum_(ds['pm25_bsoaX'],
                          ds['pm25_bsoa1'],
                          ds['pm25_bsoa2'],
                          ds['pm25_bsoa3'],
                          ds['pm25_bsoa4'])
    ds['pm25_bSOA'].attrs['units'] ='ug m-3'
    
    
    # Secondary Inorganic Aerosols SIA.
    ds['pm25_SIA'] = utl._sum_(ds['pm25_so4'],
                               ds['pm25_nh4'],
                               ds['pm25_no3']
                              )
    ds['pm25_SIA'].attrs['units'] = 'ug m-3'
        
    #Primary Organic Aerosols.
    ds['pm25_POA'] = ds['pm25_oc']
    
    #Tot OA.
    ds['pm25_OA'] = ds['pm25_POA'] + ds['pm25_SOA']
    ds['pm25_OA'].attrs['units'] = 'ug m-3'
    
        
    #Seasalt.
    ds['pm25_sea'] = utl._sum_(ds['pm25_na'], ds['pm25_cl'])
    ds['pm25_sea'].attrs['units'] = 'ug m-3'
        
    #Dust
    ds['pm25_dust'] = ds['pm25_oin']
    
    
    #for PM10
    
    ds['pm10_SOA'] =utl._sum_(ds['pm10_glysoa_r1'],
                          ds['pm10_glysoa_r2'], 
                          ds['pm10_glysoa_oh'],
                          ds['pm10_glysoa_nh4'], 
                          ds['pm10_glysoa_sfc'],
                          ds['pm10_asoaX'],
                          ds['pm10_asoa1'],
                          ds['pm10_asoa2'],
                          ds['pm10_asoa3'],
                          ds['pm10_asoa4'],
                          ds['pm10_bsoaX'],
                          ds['pm10_bsoa1'],
                          ds['pm10_bsoa2'],
                          ds['pm10_bsoa3'],
                          ds['pm10_bsoa4']
                          )   
    ds['pm10_SOA'].attrs['units'] = 'ug m-3'
    
    ds['pm10_glySOA'] =utl._sum_(ds['pm10_glysoa_r1'],
                          ds['pm10_glysoa_r2'], 
                          ds['pm10_glysoa_oh'],
                          ds['pm10_glysoa_nh4'], 
                          ds['pm10_glysoa_sfc'])
    ds['pm10_glySOA'].attrs['units'] ='ug m-3'
     
    ds['pm10_aSOA'] =utl._sum_(ds['pm10_asoaX'],
                          ds['pm10_asoa1'],
                          ds['pm10_asoa2'],
                          ds['pm10_asoa3'],
                          ds['pm10_asoa4'])
    ds['pm10_aSOA'].attrs['units'] ='ug m-3'
     
    ds['pm10_bSOA'] =utl._sum_(ds['pm10_bsoaX'],
                          ds['pm10_bsoa1'],
                          ds['pm10_bsoa2'],
                          ds['pm10_bsoa3'],
                          ds['pm10_bsoa4'])
    
    ds['pm10_bSOA'].attrs['units'] ='ug m-3'
    
    
    # Secondary Inorganic Aerosols SIA.
    ds['pm10_SIA'] = utl._sum_(ds['pm10_so4'],
                               ds['pm10_nh4'],
                               ds['pm10_no3']
                              )
    ds['pm10_SIA'].attrs['units'] = 'ug m-3'
        
    #Primary Organic Aerosols.
    ds['pm10_POA'] = ds['pm10_oc']
    
     #Tot OA.
    ds['pm10_OA'] = ds['pm10_POA'] + ds['pm10_SOA']
    ds['pm10_OA'].attrs['units'] = 'ug m-3'
        
    #Seasalt.
    ds['pm10_sea'] = utl._sum_(ds['pm10_na'], ds['pm10_cl'])
    ds['pm10_sea'].attrs['units'] = 'ug m-3'
        
    #Dust
    ds['pm10_dust'] = ds['pm10_oin']

    
    
        
def calculate_tot_pm(ds):
    """
    Add to dataset the calculated pm2.5 and PM10 in ug m-3 from components SIA POA SOA bc dust and seasalt. 
    Total should be equal to the WRF-Chem variable PM2_5_DRY and PM10. Calculation for sum follows 
    the calculation in WRF-Chem module_mosaic_sumpm.F subroutine sum_pm_mosaic_vbs4.
   
    :param ds: WRF-chem output.
    :type ds: xarray DataSet.
    :return: Dataset with added tot pm component.
    :rtype: xarray DataSet.
    
    """
    
    # PM2.5.
    ds['pm25_tot'] =utl._sum_(
                           ds['pm25_SOA'],
                           ds['pm25_SIA'],  
                           ds['pm25_dust'], 
                           ds['pm25_sea'],                 
                           ds['pm25_POA'], # POA (organic carbon).
                           ds['pm25_bc']  
                           )
    
    ds['pm25_tot'].attrs['units']= 'ug m-3'
    
    # PM10.
    ds['pm10_tot'] =utl._sum_(
                           ds['pm10_SOA'],
                           ds['pm10_SIA'],  
                           ds['pm10_dust'], 
                           ds['pm10_sea'],                 
                           ds['pm10_POA'], # POA (organic carbon).
                           ds['pm10_bc']  
                           )
    
    ds['pm10_tot'].attrs['units']= 'ug m-3'
   
def direct_pm25(ds):
    """
    Add to dataset the calculated pm2.5 direclty fromWRFchem outputs variables.
    Calculation for sum follows the calculation in WRF-Chem 
    module_mosaic_sumpm.F subroutine sum_pm_mosaic_vbs4.
   
    :param ds: WRF-chem output.
    :type ds: xarray DataSet.
    :return: Dataset with added tot pm25.
    :rtype: xarray DataSet.
    
    """
    
    ds["pm25_dir_tot"]= ((ds.so4_a01 +ds.so4_a02 + ds.so4_a03)/ds.ALT +
                    (ds.nh4_a01 +ds.nh4_a02 + ds.nh4_a03)/ds.ALT +
                     (ds.no3_a01 +ds.no3_a02 + ds.no3_a03)/ds.ALT +
                     (ds.bc_a01 + ds.bc_a02 + ds.bc_a03)/ds.ALT +
                     (ds.oc_a01 + ds.oc_a02 + ds.oc_a03)/ds.ALT +
                     (ds.glysoa_r1_a01 +ds.glysoa_r1_a02+ ds.glysoa_r1_a03)/ds.ALT +
                     (ds.glysoa_r2_a01 +ds.glysoa_r2_a02+ ds.glysoa_r2_a03)/ds.ALT +
                     (ds.glysoa_oh_a01 +ds.glysoa_oh_a02+ ds.glysoa_oh_a03)/ds.ALT +
                     (ds.glysoa_sfc_a01 +ds.glysoa_sfc_a02+ ds.glysoa_sfc_a03)/ds.ALT +
                     (ds.glysoa_nh4_a01 +ds.glysoa_nh4_a02+ ds.glysoa_nh4_a03)/ds.ALT +
                     (ds.oin_a01 + ds.oin_a02 +ds.oin_a03)/ds.ALT +
                     (ds.na_a01 +ds.na_a02 +ds.na_a03)/ds.ALT +
                     (ds.cl_a01 +ds.cl_a02 +ds.cl_a03)/ds.ALT +
                     (ds.asoaX_a01 +ds.asoaX_a02 +ds.asoaX_a03)/ds.ALT +
                     (ds.asoa1_a01 +ds.asoa1_a02 +ds.asoa1_a03)/ds.ALT +
                     (ds.asoa2_a01 +ds.asoa2_a02 +ds.asoa2_a03)/ds.ALT +
                     (ds.asoa3_a01 +ds.asoa3_a02 +ds.asoa3_a03)/ds.ALT +
                     (ds.asoa4_a01 +ds.asoa4_a02 +ds.asoa4_a03)/ds.ALT +
                     (ds.bsoaX_a01 +ds.bsoaX_a02 +ds.bsoaX_a03)/ds.ALT +
                     (ds.bsoa1_a01 +ds.bsoa1_a02 +ds.bsoa1_a03)/ds.ALT +
                     (ds.bsoa2_a01 +ds.bsoa2_a02 +ds.bsoa2_a03)/ds.ALT +
                     (ds.bsoa3_a01 +ds.bsoa3_a02 +ds.bsoa3_a03)/ds.ALT +
                     (ds.bsoa4_a01 +ds.bsoa4_a02 +ds.bsoa4_a03)/ds.ALT)



def convert_cv(ds,cvap):
    """
    This function converts condesable apour varaibles from ppmv to ug/m3. 
    :param ds: WRF-chem output.
    :type ds: xarray DataSet.
    :param cv: list of condesable vapour varaibles.
    :type cv: list.
    :return: Reduced dataset with pm data.
    :rtype: xarray DataSet.
    
    """
    # Using cv_mw =250 g/mol for cond vap as in Knote et al 2015 +
    #  ideal gas law in the form: PV=nRT
    
    cv_mw=250   # g/mol
    r= 8.3145   # J mol-1 K-1
    gug=1e6  # grams to ug conversion.
    
    utl.get_tot_pressure(ds)    # Get T and P
    utl.get_abs_temperature(ds)
    
    for cv in cvap:
        #convert species from ppmv to ug/m3. Note:divide value in ppmv by 1e6.
         #ds[cv] = (ds[cv]/1e6)*(cv_mw*gug)*(ds.TP/(ds.AT*r))
         ds[cv] = (ds[cv]/1e6)*cv_mw/29* 1e9/ds.ALT
         ds[cv].attrs['units']= 'ug m-3'
      
        

def get_aerosols(ds):
    
    """
    This function creates a dataset with all the pm2.5 and pm10 useful data from 
    the WRF-Chem output.
    
    :param ds: WRF-chem output.
    :type ds: xarray DataSet.
    :return: Reduced dataset with pm data.
    :rtype: xarray DataSet.
    
    """
    
    #list of relevant aerosols variables for pm2.5 and pm10 in option 202.
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
        'water_a01','water_a02', 'water_a03', 'water_a04', # pm2.5 water.
        'ALT' #inverse density.
        ]
    
    #list of condensable vapours for VBS.
    cond_vap=[
        'cvasoaX','cvasoa1','cvasoa2','cvasoa3','cvasoa4',
        'cvbsoaX','cvbsoa1','cvbsoa2','cvbsoa3','cvbsoa4',
        ]  
    
    state_var =["ALT", "P","PB","T"]
    
    ds_aer = utl._get_data_subset_(ds,aerosols)
    
    get_pm_species(ds_aer)
    get_pm_components(ds_aer)
    calculate_tot_pm(ds_aer)
    
    # add condensable vapors
    ds_cv =  utl._get_data_subset_(ds,cond_vap + state_var)
    convert_cv(ds_cv,cond_vap)
    
    ds_aer = ds_aer.merge(ds_cv,compat='override')
    
    return ds_aer   



                     
                     
                     
                     