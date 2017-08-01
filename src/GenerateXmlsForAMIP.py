#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 17:13:30 2017

@author: musci2
"""

## THIS SCRIPT FILTERS THROUGH ALL OF THE VARIABLES AND MODELS IN THE PATH 
#PROVIDED AND CREATES A NEW XML BY COMBINING ALL THE NETCDF FIULES IN EACH 
#DIRECTORY
#THIS WAS NECESDDARY FOR THE AMIP DATA FOUND IN 'AMIP2-STORAGE'
import sys, os

pathin = '/oldCMIPs/PJG_StorageRetrieval/AMIP2-STORAGE/mo/'
lst = os.listdir(pathin)
lst.sort()
for count,varb in enumerate(lst[120:128]):
    print varb
    pathin1 = pathin+varb+'/'
    lst1=os.listdir(pathin1)
    for count,alias in enumerate(lst1):
        print alias
        path2 = pathin1+alias
        os.chdir(path2)
        xml = varb+'_'+alias+'_'+'BEN.xml'
        command = 'cdscan -x '+xml+' *.nc'
        os.system(command)

#                 os.chdir(useful) #change to directory that the data was just moved to
#                 print 'purge...?'
#                 cwd = os.getcwd()
#                 print 'copied data over'
#                 
#                 #delete all previous xml files in the file of imported data
#                 filelist = glob.glob("*.xml")
#                 for q in filelist:
#                     os.remove(q)
#                 #delete all files containing con or per in the file of imported data
#                 filelist2 = os.listdir(cwd)
#                 for w in filelist2:
#                     if "_per_" in w:
#                         os.remove(w)
#                 #create xml file combining all the remaining netcdf files in the imported data folder
#                 os.system("cdscan -x tmp.xml *.nc")
#                 print 'Looking for xml'
#                 check = os.path.isfile(useful+'/'+'tmp.xml')
#                 if check == False:
#                     print 'skipping that one'
#                     break