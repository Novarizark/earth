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
    lat =ncdf.variables["lat_0"][:]
    lon =ncdf.variables["lon_0"][:]
    lev =ncdf.variables["lv_ISBL0"][:]
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
#ofile_ncname='gfs_sample.nc'
#req=urllib2.Request(add_line)
#infile=urllib2.urlopen(req)
print 'downloading '+ add_line+'...'

#outfile=open(ofile_name,'wb')
#outfile.write(infile.read())
#outfile.close()

#convert to interim netcdf file
print 'converting...'
#os.system('ncl_convert2nc '+ofile_name+' -v lv_ISBL0,lat_0,lon_0,UGRD_P0_L100_GLL0,VGRD_P0_L100_GLL0')

# convert to json file
with open('sample.json', 'r') as f:
    json_smp = json.load(f)

lat_array, lon_array, lev_array, var1f = read_ncdf_all(ofile_ncname, "UGRD_P0_L100_GLL0")
var2f=read_ncdf_field(ofile_ncname, "VGRD_P0_L100_GLL0")

nlat=len(lat_array)
nlon=len(lon_array)
nlev=len(lev_array)
dlat=lat_array[1]-lat_array[0]
dlon=lon_array[1]-lon_array[0]

#adjust from sample json
for jsp in json_smp:
    jsp['header']['refTime']=unicode(down_time_obj.strftime('%Y-%m-%d')+'T'+down_time_obj.strftime('%H')+':00:00.000Z')
    jsp['header']['nx']=nlon
    jsp['header']['ny']=nlat
    jsp['header']['lo1']=lon_array[0]
    jsp['header']['lo2']=lon_array[-1]
    jsp['header']['la1']=lat_array[0]
    jsp['header']['la2']=lat_array[-1]
    jsp['header']['dx']=dlon
    jsp['header']['dy']=dlat
    


print var1f[-1,0,:]

