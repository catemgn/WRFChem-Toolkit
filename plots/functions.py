import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


def var_plot_2D(dataset, var_name, level, title):

    """
    Plots a 2D-map of a variable at a specified level and at a GIVEN TIME.
    (For set the time if multiples: dataset[0]  or 1,2,3 in the brackets.)

    :param dataset: Datast containing the varaible.
    :type dataset: xarray DataSet.
    :param var_name: variable name as in the dataset.
    :type var_name: string.
    :param level: vertical level at which to plot.
    :type level: integer.
    :param title: title of the plot.
    :type title: string.
    """
    #TODO add possibility to plot at user defined time.

    var = dataset[var_name]

    # draw map
    ax = plt.subplot(projection=ccrs.PlateCarree())

    # draw coastlines and borders
    ax.add_feature(cfeature.COASTLINE, lw=0.5)
    ax.add_feature(cfeature.BORDERS, lw=0.5)

    # Create a feature for States/Admin 1 regions at 1:50m from Natural Earth
    #states_provinces = cfeature.NaturalEarthFeature(
        #category='cultural',
        #name='admin_1_states_provinces_lines',
        #scale='100m',
        #facecolor='none')
    #ax.add_feature(states_provinces)

    # draw meridians and parallels
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                          linewidth=0.5, color='k', alpha=0.4, linestyle='-')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 10, 'color': 'gray'}
    gl.ylabel_style = {'size': 10, 'color': 'grey'}

    # plot data at desired level
    long = dataset.XLONG.values[0, :, :]
    lat = dataset.XLAT.values[0, :, :]
    var_values = var[level, :, :]
    res = 15  # controls the resolution for the map plotting.

    cs = plt.contourf(long, lat, var_values, res,
         transform=ccrs.PlateCarree(), cmap=plt.cm.YlGnBu)

    # colorbar
    cbar = plt.colorbar(cs)  # pad=0.2 #format='%.2e'
    cbar.set_label(var.units)
    ax.set_title(title)

    plt.savefig("2D_plot.png")