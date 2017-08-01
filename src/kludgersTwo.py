#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 12:07:59 2017

@author: musci2

WHEN BIG KAHUNA IS RUN AND ENCOUNTERS AN ERROR AT 'CMOR.WRITE', IT IS IN MOST CASES DUE TO INCOMPATIBLE UNITS OR A UNITS ERROR.
THE UNITS INPUT FROM THE XML ARE OFTEN WRONG, SO THE UNITS EXCEPTIONS FOR EACH VARIABLE ARE HOUSED HERE
ADD NEW EXCEPTIONS TO THE 'EXCEPTIONS' DICTIONARY BELOW FOR THE CORRESPONDING VARIABLE
UNIT CONVERSIONS CAN ALSO BE CARRIED OUT THROUGH THIS FILE USING THE CONVERSIONS DICTIONARY - SEE 'PR' FOR EXAMPLE
"""
## WHEN BIG KAHUNDA IS RUN

import os 
os.chdir('/export/musci2/git/CMIP2_CVs/src')

def kludgers(var, d, axis_ids, alias ):    

     import cmor, gc, json, sys, os, shutil
     import cdms2 as cdm
     import cdutil as cdu
     import numpy as np
     
     Amon = json.load(open('/export/musci2/git/cmip6-cmor-tables/Tables/CMIP6_Amon.json'))
     DefaultUnits = Amon['variable_entry'][var]['units'].encode('ascii','ignore')
     PostvDirec = Amon['variable_entry'][var]['positive']
     
#    
     Converter = 1
     exceptions = {}
     conversions ={}
     exceptions['pr']=['']
     conversions['pr'] = ['mm/day',1.0/86400]
     #exceptions['tas']=['']
     exceptions['rlut']=[" ", "m/s",'K','Watts/meter**2H']
     exceptions['hfss']=[" ","m/s", "w/m2","K","Watts/meter**2H"]
     exceptions['tauu']=[" ","pa"]
     exceptions['tauv']=[" ","pa"]
     exceptions['psl']=[" ","pa","Pa0"]
     exceptions['ua']=[" ",'K','meters/second{|\xe8']
     #exceptions['ta']=['',' ','m/s','KelvinB49.0)']
     exceptions['zg']=['','  ','m^2/s^2','gpm','K','metersB']
     exceptions['va']=[" ",'K','meters/second{|\xe8']
     #exceptions['ts']=['',' ']
     exceptions['rlutcs']=[' ','K','Watts/meter**2Hime','Watts/meter**2He']
     exceptions['hfls']=[' ','  ','K','Watts/meter**2Hime','Watts/meter**2H']
     exceptions['rsut']=[' ','  ','K','Watts/meter**2Hime','Watts/meter**2H','hPa']
     exceptions['hus']=[' ','  ','hPa','kg/kg\xdfB']
     exceptions['rsutcs']=[' ','  ','K','Watts/meter**2Hime','Watts/meter**2H','hPa','m/s']
     exceptions['clt']=[' ','  ']
     exceptions['rsds']=[' ','  ','K','Watts/meter**2Hime','Watts/meter**2H','hPa','m/s']
     exceptions['rsus']=[' ','  ','K','Watts/meter**2Hime','Watts/meter**2H','hPa','m/s']
     exceptions['rltcrfm2']=[' ','  ','m/s']
     exceptions['rlns']=[' ','  ','m/s']
     exceptions['rlds']=[' ','  ','K','Watts/meter**2Hime','Watts/meter**2H','hPa','m/s']
     exceptions['prc']=[' ','  ']
     exceptions['snw']=[' ','  ']
     exceptions['rsns']=[' ','  ']
     exceptions['prl']=[' ','  ']
     exceptions['rstcrfm2']=[' ','  ']
     exceptions['rsnt']=[' ','  ','m/s']
     exceptions['rlus']=[' ','  ','m/s']
     exceptions['evspsbl']=[' ','  ','m/s']
     exceptions['tasmin']=[' ','  ']
     exceptions['tasmax']=[' ','  ']
     exceptions['sit']=[' ','  ']
     exceptions['sic']=[' ','  ']
     exceptions['ps']=[' ','  ']
     exceptions['prw']=[' ','  ','m/s','mm']
     exceptions['prs']=[' ','  ']
     exceptions['prsm']=[' ','  ']
     exceptions['vas']=[' ','  ']
     exceptions['uas']=[' ','  ']
     exceptions['wap']=[' ','  ','hPa']
     exceptions['rsdt']=[' ','  ','m/s']
     exceptions['rsdscs']=[' ','  ','m/s','K']
     exceptions['rldscs']=[' ','  ','m/s']
     exceptions['rldscd']=[' ','  ','m/s']
     exceptions['rtmt']=[' ','  ','Watts/meter**2Hime','Watts/meter**2H','hPa','m/s','Watts/meter**2He']
     exceptions['clw']=[' ','  ','K']
     exceptions['tauvgwd']=[' ','  ']
     exceptions['tauugwd']=[' ','  ']
     exceptions['rsuscs']=[' ','  ','m/s']
     exceptions['mrros']=[' ','  ']
     exceptions['huss']=[' ','  ']
     exceptions['hur']=[' ','  ']
     exceptions['clwvi']=[' ','  ']
     exceptions['cli']=[' ','  ']
     exceptions['water']=[' ','  ']
     exceptions['tntsw']=[' ','  ']
     exceptions['tntmc']=[' ','  ']
     exceptions['tntlw']=[' ','  ']
     exceptions['tntlsp']=[' ','  ']
     exceptions['tnmrc']=[' ','  ']
     exceptions['tnmmvgwd']=[' ','  ']
     exceptions['tnmmugwd']=[' ','  ']
     exceptions['stfgif']=[' ','  ']
     exceptions['snow']=[' ','  ']
     exceptions['rss']=[' ','  ']
     exceptions['rls']=[' ','  ']
     exceptions['prsn']=[' ','  ','m/s']
     exceptions['prec_ls']=[' ','  ']
     exceptions['mrsos']=[' ','  ']
     exceptions['mrso']=[' ','  ']
     exceptions['mrro']=[' ','  ']
     exceptions['mpuua']=[' ','  ']
     exceptions['mptta']=[' ','  ']
     exceptions['clivi']=[' ','  ']


     try:
         print d.units
         oldUnits = d.units
     except:
         oldUnits = 'Error Raised'
     
     if var in ['tas','ts','ta']:
         uniMsg = ' ' 
         if d.min() > 100.: # cccma-c01a tas min=192.5,max=313.9
             #print 'enter K'
             d.units = 'K' ; # 'degC'
         elif d.min() > -150. and d.max() < 100.:
             #print 'enter degC'
             d.units = 'degC'
         else:
             d.units = 'K'
             uniMsg = 'd.min was below 100, yet d.max was above 100, so just set to K'

         print d.units
         print d.min()
         print d.max()
         #print 'NOOOOOOOO!'
         varid = cmor.variable(var,d.units,axis_ids)
         
     elif alias and var in ['gfdl-c03a', 'psl']:
         d.units = DefaultUnits
         uniMsg = 'Forced units - Special case'
         print 'Forced units - Special case'
    
     else:
         print ' in right place'
         try: 
             print d.units
             uniMsg = ' ' 
             if d.units in exceptions[var]:
                 d.units = DefaultUnits
                 uniMsg = 'Forced units b/c of exception'
                 print 'Forced units b/c of exception'                 
         except AttributeError:
                     d.units = DefaultUnits
                     print 'Forced units b/c Attrib Error'
                     uniMsg = 'Forced units b/c Attrib Error'
                         
     try:
         if d.units in conversions[var]:
             d.units = DefaultUnits
             Converter = conversions[var][1]
             uniMsg = 'Converted units to Default'
             print 'Converted units to default'
     except KeyError:
        print ' no conversions necessary'
             
         
     print 'kludge done..'
     varid   = cmor.variable(var,d.units,axis_ids,positive= PostvDirec)
     print 'varid done'

     
     print uniMsg, oldUnits, d.units, Converter  
     return (uniMsg, d.units, varid, Converter, oldUnits)