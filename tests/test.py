from analysis import functions as nlys
from plots import functions as plot

# Path for multiple netCDF files
data_path = 'R:\\WRFchem4.0\\model\\WRF\\test\\em_real\\outputs' \
            '\\test_india_24h\\test3_201\\W*'

#merging all together different netCDF files from files-path.
ds = nlys.merge_datasets(data_path)

#time average of files.
time_avg = nlys.var_time_mean(ds)

#plotting averaged ozone for the day
plot.var_plot_2D(time_avg, 'PM2_5_DRY', 0, 'Average surface PM2.5 '
                                           'concentration on 01-04-210')

print('Test Done!')