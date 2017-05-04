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
    lat =ncdf.variables["g4_lat_1"][:]
    lon =ncdf.variables["g4_lon_2"][:]
    lev =ncdf.variables["lv_ISBL0"][:]
    var  = ncdf.variables[varname][:,:,:]
    return lat, lon, lev, var

def read_ncdf_field(pfname, varname):
    ncdf = Dataset(pfname)
    var  = ncdf.variables[varname][:,:,:]
    return var

# Out level
#outlvl=[100000, 92500, 85000, 70000, 50000, 20000, 10000, 5000, 1000]
outlvl=[1000, 925, 850,700, 500, 200, 100, 50, 10]

# get parameter and download the file
d_time_str=sys.argv[1]
down_time_obj = datetime.datetime.strptime(d_time_str, '%Y%m%d%H')

ofile_name='/Volumes/ERA-UV/ei.oper.an.pl.regn128uv.'+down_time_obj.strftime('%Y%m%d%H')+'.grib1'
#ofile_name='ei.oper.an.pl.regn128uv.'+down_time_obj.strftime('%Y%m%d%H')+'.grib1'
ofile_ncname='ei.oper.an.pl.regn128uv.'+down_time_obj.strftime('%Y%m%d%H')+'.nc'

#convert to interim netcdf file
print 'converting...'
os.system('ncl_convert2nc '+ofile_name)

# convert to json file
with open('sample.json', 'r') as f:
    json_smp = json.load(f)

lat_array, lon_array, lev_array, var1f = read_ncdf_all(ofile_ncname, "U_GDS4_ISBL")
var2f=read_ncdf_field(ofile_ncname, "V_GDS4_ISBL")

nlat=len(lat_array)
nlon=len(lon_array)
nlev=len(lev_array)
dlat=abs(lat_array[1]-lat_array[0])
dlon=abs(lon_array[1]-lon_array[0])

#adjust from sample json
for jsp in json_smp:
    jsp['header']['refTime']=unicode(down_time_obj.strftime('%Y-%m-%d')+'T'+down_time_obj.strftime('%H')+':00:00.000Z')
    jsp['header']['nx']=int(nlon)
    jsp['header']['ny']=int(nlat)
    jsp['header']['lo1']=float(lon_array[0])
    jsp['header']['lo2']=float(lon_array[-1])
    jsp['header']['la1']=float(lat_array[0])
    jsp['header']['la2']=float(lat_array[-1])
    jsp['header']['dx']=float(dlon)
    jsp['header']['dy']=float(dlat)
    

for idx, lvl in enumerate(lev_array):
    if int(lvl) in outlvl:
        jlist=[]
        jlist2=[]
        print(str(int(lvl))+"hPa...")
        for ii in range(nlat):
            for jj in range(nlon):
                jlist.append(float(var1f[idx,ii,jj]))
                jlist2.append(float(var2f[idx,ii,jj]))
        json_smp[0]['data']=jlist
        json_smp[1]['data']=jlist2
        fileObject = open('current-wind-isobaric-'+str(int(lvl))+'hPa-gfs-1.0.json', 'w')  
        jsObj = json.dumps(json_smp, indent=2)
        fileObject.write(jsObj)  
        fileObject.close()  
os.system("cp current*1000hPa* current-wind-surface-level-gfs-1.0.json")
os.system("mv current* ../data/weather/current/")
os.system("rm "+ofile_ncname)
