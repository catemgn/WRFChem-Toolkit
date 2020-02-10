#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions for plots and graphs of WRF-Chem outputs.

Created on Thu Jan  9 10:57:07 2020

@author: Caterina Mogno c.mogno@ed.ac.uk
"""


def map_2D(dataset, var_name, level=0, mask_values=None,
           title=None, cmap = 'OrRd', coastline=True, borders=True,
           pixels=False, save=False, format='pdf', dpi=1000):

    """
    Plots a 2D-map of a variable at a given time (and level).
    NB: input dataset must already contain only one time value.
    (For set the time if multiples: dataset[0]  or 1,2,3 in the brackets.)

    :param dataset: WRF-Chem output.
    :type dataset: xarray DataSet
    :param var_name: variable name as in the dataset.
    :type var_name: string
    :param level: vertical level at which to plot. Default surface level.
    :type level: integer
    :param mask_values: mask values to plot below a certain level. Default no mask.
    :type mask_values: float 
    :param title: title of the plot. Default no title.
    :type title: string
    :param coastline: plot or not coastline. Default True.
    :type coastline: bool
    :param borders: plot or not borders. Default True.
    :type borders: bool
    :param pixels: plot as pcolormesh (raw pixels). Default False.
    :type pixels: bool
    :param save: save plot to path destination, including figure name. Default False.
    :type save: bool
    :param format: format of the saved plot (pdf, png, eps..), Default pdf.
    :type format: string
    :param dpi: resolution of the saved plot in dots per inches. Default 1000.
    :type dpi: integer
    """
    
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
    import numpy as np
    
    
    # ------------------------- DRAW THE MAP --------------------------------
    # draw map.
    ax = plt.subplot(projection=ccrs.PlateCarree())
 
    # draw meridians and parallels.
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                          linewidth=0.5, color='k', alpha=0.4, linestyle='-')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 10, 'color': 'gray'}
    gl.ylabel_style = {'size': 10, 'color': 'grey'}


    # draw coastlines and borders.
    if coastline:
        ax.add_feature(cfeature.COASTLINE, lw=0.5)
    if borders:
        ax.add_feature(cfeature.BORDERS, lw=0.5)

   # ------------------------- GET DATA TO PLOT------------------------------
   
    # get variable from dataset.   
    var = dataset[var_name]
      
    # plot data at desired level.
    long = dataset.XLONG.values[0, :, :]
    lat = dataset.XLAT.values[0, :, :]
    
    if mask_values is None:
        var_values = var[level, :, :]
    else: 
        var_values= np.ma.masked_where(var[level,:,:].values < mask_values,
                                       var[level,:,:].values) 
   

   # -------------------------  PLOT DATA ----------------------------------
    
    #plot type: contourf or pcolormesh.
    if pixels:
        cs = plt.pcolormesh(long, lat,var_values,
            transform=ccrs.PlateCarree(), cmap =cmap)
    else:    
        cs = plt.contourf(long, lat, var_values,
            transform=ccrs.PlateCarree(), cmap=cmap)
    
    # colorbar.
    cbar = plt.colorbar(cs)
    cbar.set_label(var.units)
    
    #title.
    ax.set_title(title)
    
    #save
    if save:
        plt.savefig( save + '.' + format, format=format, dpi=dpi)
    
    plt.show()
    
    
def time_series(dates, variables, labels,title=None, xlabel=None, ylabel=None):
   
    """
    Plots timeseries of given varialbels in one single plot.
 
    :param dates: timeseries dates.
    :type dates: numpy.array
    :param variables: variables to be plotted.
    :type variables: list of xarray.DataArray
    :param labels: labels for the each line plot.
    :type labels: list of strings.
    :param title: title of the plot. Default no title.
    :type title: string
    :param xlabel: x-axis label. Default no label.
    :type  xlabel: string
    :param xlabel: y-axis label. Default no label.
    :type  xlabel: string
    """
    
    import plotly.graph_objs as go
    
    data=[] #empty list for storing traces.
    
    # create trace for each variable
    for i in range(len(variables)):
            trace = go.Scatter(
            x=dates, 
            y=variables[i][1,:].values,
            name= labels[i],
            mode='lines',
            )
            data.append(trace)
    
    # set layout of the plot       
    layout = go.Layout(
    xaxis=dict(title= xlabel),
    yaxis=dict(title= ylabel),
    title=title,
    showlegend = True)
    
    # plot
    fig = go.Figure(data=data, layout=layout)
    fig.show()
    
            
            
            
 