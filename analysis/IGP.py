#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

Specific functions for Indo Gangetic Plain (IGP) spatial data analysis.
These functions are based on:
 -salem  python package:https://salem.readthedocs.io/en/v0.2.3/index.html.
 -GDAM administive areas: https://gadm.org/index.html.

Created on Sat Mar 14 19:08:57 2020

@author: Caterina Mogno c.mogno@ed.ac.uk
"""

def get_IGP(data_path, shp_path):
    """
     Return only data in IGP adminsitrative domains (based on masking process). 
     Return type is a dictionary containing WRF-Chem outputs datasets with keys:
     
     - IGP :contains all IGP states in BGD, PAK, IND.
     - U_IGP : data for states Sindh, Punjab (PAK), Punjab (IND).
     - M_IGP : data for states Haryana, Delhi NCT, Uttar Pradesh (IND).
     - L_IGP : data for states Bihar, West Bengal (IND), Barisal, 
       Dhaka, Khulna, Rajshahi, Rangpur (BGD).
     - Single states subsets (TO DO)."
    
    WARNING: this division of IGP is arbitrary, given that there is no 
             official IGP administrative domain. 
    
    
    :param data_path:
     path to data files.
    :type data_path: string
    :param shp_path:
     path to IGP shapefiles.
    :type shp_path: string
    :return:
    dictionary of xarray.Dataset.
  :rtype: dict
 """
    
    import salem

    igp_data={} # dictionary for containing datasets.

    
    ds = salem.open_mf_wrf_dataset(data_path) # open data with salem.
    
    # get IGP states shapefiles.
    shdf= salem.read_shapefile(shp_path) # IGP shp.
    shdf_UIGP = shdf.loc[
                      (shdf['HASC_1'] == 'PK.SD')
                    | (shdf['HASC_1'] == 'IN.PB')
                    | (shdf['HASC_1'] == 'PK.PB')
                    ]
    shdf_MIGP = shdf.loc[
                      (shdf['HASC_1'] == 'IN.DL')
                    |  (shdf['HASC_1'] == 'IN.HR')
                    | (shdf['HASC_1'] == 'IN.UP')
                    ]
    shdf_LIGP = shdf.loc[
                      (shdf['HASC_1'] == 'IN.WB')
                    | (shdf['HASC_1'] == 'IN.BR')
                    | (shdf['HASC_1'] == 'BD.BA')
                    | (shdf['HASC_1'] == 'BD.KH')
                    | (shdf['HASC_1'] == 'BD.RS')
                    | (shdf['HASC_1'] == 'BD.RP')
                    |  (shdf['HASC_1'] == 'BD.DH')
                    ]
    
    # Get data subsets.
    IGP = ds.salem.roi(shape=shdf)   
    UIGP = ds.salem.roi(shape=shdf_UIGP)
    MIGP = ds.salem.roi(shape=shdf_MIGP)
    LIGP = ds.salem.roi(shape=shdf_LIGP)
    
    # Add to list.
    igp_data.update({'IGP': IGP})
    igp_data.update({'U_IGP': UIGP})
    igp_data.update({'M_IGP': MIGP})
    igp_data.update({'L_IGP': LIGP})
    

    return igp_data
