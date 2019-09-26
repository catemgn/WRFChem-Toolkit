import xarray as xr

def merge_datasets(data_path):
 """
  Merge in a single dataset all data linked in the path. To consider multiple
  files the syntax is for example /mydir/wrfout_d01_2010-04-0*.

  :param data_path:
    path to data files.
  :type data_path: string
  :return:
    single dataset of multiple files.
  :rtype: xarray Dataset
 """
 dataset = xr.open_mfdataset(data_path,decode_times=True)
 return dataset


def var_time_mean(da):
 """
  Make the average over 'Time' dimension of a datarray.

  :param da:
    dataset to be averaged.
  :type da: xarray DataArray.
  :return:
    Time averaged da.
  :rtype: xarray DataSet.
 """
 return xr.Dataset(dict(da.mean(dim='Time', keep_attrs=True).data_vars),
                    coords=dict(da.coords))


