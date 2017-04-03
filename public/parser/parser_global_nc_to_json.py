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
    lat =ncdf.variables["lat"][:]
    lon =ncdf.variables["lon"][:]
    lev =ncdf.variables["level"][:]
    var  = ncdf.variables[varname][:,:,:]
    return lat, lon, lev, var

def read_ncdf_field(pfname, varname):
    ncdf = Dataset(pfname)
    var  = ncdf.variables[varname][:,:,:]
    return var

# Out level
outlvl=[100000, 92500, 85000, 70000, 50000, 20000, 10000]

# get filename
d_time_str=sys.argv[1]


# convert to json file
with open('sample.json', 'r') as f:
    json_smp = json.load(f)

lat_array, lon_array, lev_array, var1f = read_ncdf_all(ofile_ncname, "UGRD_P0_L100_GLL0")
var2f=read_ncdf_field(ofile_ncname, "VGRD_P0_L100_GLL0")

nlat=len(lat_array)
nlon=len(lon_array)
nlev=len(lev_array)
dlat=abs(lat_array[1]-lat_array[0])
dlon=abs(lon_array[1]-lon_array[0])

#adjust from sample json
print json_smp[0]['header']
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
        for ii in range(nlat):
            for jj in range(nlon):
                jlist.append(float(var1f[idx,ii,jj]))
                jlist2.append(float(var2f[idx,ii,jj]))
        json_smp[0]['data']=jlist
        json_smp[1]['data']=jlist2
        fileObject = open('current-wind-isobaric-'+str(int(lvl)/100)+'hPa-gfs-1.0.json', 'w')  
        jsObj = json.dumps(json_smp, indent=2)
        fileObject.write(jsObj)  
        fileObject.close()  

