#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Download GFS data, convert to json file
# 
#
#       L_Zealot
#       Mar 31, 2017
#
#
import sys
import os
import json
import datetime
import urllib2
import math
from netCDF4 import Dataset
import numpy as np

def read_ncdf_all(pfname, varname):
    ncdf = Dataset(pfname)
    lat =ncdf.variables["lv_ISBL0"][:]
    lon =ncdf.variables["lat_0"][:]
    lev =ncdf.variables["lon_0"][:]
    var  = ncdf.variables[varname][:,:,:]
    return lat, lon, lev, var

def read_ncdf_field(pfname, varname):
    ncdf = Dataset(pfname)
    var  = ncdf.variables[varname][:,:,:]
    return var

# get parameter and download the file
d_time_str=sys.argv[1]
down_time_obj = datetime.datetime.strptime(d_time_str, '%Y%m%d%H')

add_line='ftp://nomads.ncdc.noaa.gov/GFS/analysis_only/'+down_time_obj.strftime('%Y%m')+'/'+down_time_obj.strftime('%Y%m%d')+'/gfsanl_4_'+down_time_obj.strftime('%Y%m%d')+'_'+down_time_obj.strftime('%H')+'00_000.grb2'
ofile_name='gfsanl_4_'+down_time_obj.strftime('%Y%m%d')+'_'+down_time_obj.strftime('%H')+'00_000.grb2'
ofile_ncname='gfsanl_4_'+down_time_obj.strftime('%Y%m%d')+'_'+down_time_obj.strftime('%H')+'00_000.nc'
req=urllib2.Request(add_line)
infile=urllib2.urlopen(req)
print 'downloading '+ add_line+'...'

outfile=open(ofile_name,'wb')
outfile.write(infile.read())
outfile.close()

 convert to enterim netcdf file
print 'converting...'
os.system('ncl_convert2nc '+ofile_name+' -v lv_ISBL0,lat_0,lon_0,UGRD_P0_L100_GLL0,VGRD_P0_L100_GLL0')

# convert to json file
with open('sample.json', 'r') as f:
    json_smp = json.load(f)

json_smp[0]['header']['refTime']=unicode(down_time_obj.strftime('%Y-%m-%d')+'T'+down_time_obj.strftime('%H')+':00:00.000Z')
print json_smp[1]['header']
lat_array, lon_array, lev_array, var1f = read_ncdf_all(ofile_ncname, "UGRD_P0_L100_GLL0")
var2f=read_ncdf_field(ofile_name, "VGRD_P0_L100_GLL0")
print var1f[0][:][0]









