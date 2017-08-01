#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 09:47:34 2017

@author: musci2
"""

import datetime
import gc
import json
import os,sys
import shlex
import ssl
import subprocess


source_id= dict()
key = 'ARPEGE-OPA1'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 'CMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'CERFACS'
]
source_id[key]['label'] = 'ARPEGE/OPA1'
source_id[key]['label_extended'] = 'ARPEGE/OPA1'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T21, 64 x 32 longitude/latitude; 30 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '500 km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['complex land surface scheme']
source_id[key]['model_component']['land']['nominal_resolution'] = '500 km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '2 x 2 degree, 180 x 90 longitude/latitude; 31 levels; enhanced horizontal resolution near the Equator'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '250 km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ['ice extent/thickness determined diagnostically from ocean surface temperature']
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '250 km'
source_id[key]['reference'] = [
 'Guilyardi and Madec (1997) doi:10.1007/s003820050157'
]
source_id[key]['release_year'] = '1997'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key


key = 'ARPEGE-OPA2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 'CMIP2'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'CERFACS'
]
source_id[key]['label'] = 'ARPEGE/OPA2'
source_id[key]['label_extended'] = 'ARPEGE/OPA2'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T31, 92 x 46 longitude/latitude; 19 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['complex land surface scheme']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '2 x 2 degree, 180 x 90 longitude/latitude; 31 levels; enhanced horizontal resolution near the Equator'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ['thermodynamic ice model']
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 'Barthelet et al., 1998a,b doi: 10.1007/s00382-003-0332-6'
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key


key = 'BMRCa'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 'CMIP1'
]
source_id[key]['aliases']= [
 'bmrc-nka?'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'BMRC'
]
source_id[key]['label'] = 'BMRCa'
source_id[key]['label_extended'] = 'BMRCa'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'R21, 64 x 56 longitude/latitude; 9 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['multi-layer temperature scheme', 'standard bucket hydrology scheme']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '3.2 x 5.6 degree, 64 x 56 longitude/latitude; 12 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ['thermodynamic ice model']
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 'Power et al., 1993 doi: ????????????'
]
source_id[key]['release_year'] = '1993'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'BMRCb'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 'CMIP2'
]
source_id[key]['aliases']= [
 'bmrc-nka?'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water"
]
source_id[key]['institution_id'] = [
 'BMRC'
]
source_id[key]['label'] = 'BMRCb'
source_id[key]['label_extended'] = 'BMRCb, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'R21, 64 x 56 longitude/latitude; 17 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['multi-layer temperature scheme', 'standard bucket hydrology scheme']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '3.2 x 5.6 degree, 64 x 56 longitude/latitude; 12 levels; enhanced horizontal resolution near the Equator'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ['thermodynamic ice model']
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 'Power et al., 1998 doi: ????????????'
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'CCSR-NIES'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1","CMIP2"
]
source_id[key]['aliases']= [
 'ccsr-nka??'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water"
]
source_id[key]['institution_id'] = [
 'CCSR/NIES'
]
source_id[key]['label'] = 'CCSR/NIES'
source_id[key]['label_extended'] = 'CCSR/NIES, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T21, 64 x 32 longitude/latitude; 20 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['multi-layer temperature scheme', 'modified bucket scheme with spatially varying soil moisture capacity and/or a surface resistance']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '2.8 x 2.8 degree, 128 x 64 longitude/latitude; 17 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ['thermodynamic ice model']
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 'Emori et al., 1999 doi: 10.2151/jmsj1965.77.6_1299'
]
source_id[key]['release_year'] = '1999'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'CCSR-NIES2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIPX?"
]
source_id[key]['aliases']= [
 'ccsr-nka??'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water"
]
source_id[key]['institution_id'] = [
 'CCSR/NIES'
]
source_id[key]['label'] = 'CCSR/NIES2'
source_id[key]['label_extended'] = 'CCSR/NIES2, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T21, 64 x 32 longitude/latitude; 20 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['multi-layer temperature scheme', 'modified bucket scheme with spatially varying soil moisture capacity and/or a surface resistance']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '2.8 x 3.8 degree, 94 x 64 longitude/latitude; 17 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ['thermodynamic ice model only']
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 'Nozawa et al., 2000 doi: ????'
]
source_id[key]['release_year'] = '2000'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'CGCM1'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1","CMIP2"
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water"
]
source_id[key]['institution_id'] = [
 'CCCma'
]
source_id[key]['label'] = 'CGCM1'
source_id[key]['label_extended'] = 'CGCM1, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T32, 96 x 47 longitude/latitude; 10 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['multi-layer temperature scheme', 'modified bucket scheme with spatially varying soil moisture capacity and/or a surface resistance']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '1.8 x 1.8 degree, 200 x 100 longitude/latitude; 29 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ['thermodynamic ice model only']
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Boer et al.,2000 doi:  10.1007/s003820050337","Flato et al., 2000 doi: 10.1007/s003820050339"
]
source_id[key]['release_year'] = '2000'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'CGCM2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP2+"
]
source_id[key]['aliases']= [
 'cccma-c01a'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water"
]
source_id[key]['institution_id'] = [
 'CCCma'
]
source_id[key]['label'] = 'CGCM2'
source_id[key]['label_extended'] = 'CGCM2, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T32, 96 x 47 longitude/latitude; 10 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['multi-layer temperature scheme', 'modified bucket scheme with spatially varying soil moisture capacity and/or a surface resistance']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '1.8 x 1.8 degree, 200 x 100 longitude/latitude; 29 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model","ice rheology included"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Flato and Boer, 2001 doi: 10.1029/2000GL012121"
]
source_id[key]['release_year'] = '2001'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'COLA1'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1"
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ""
]
source_id[key]['institution_id'] = [
 'COLA'
]
source_id[key]['label'] = 'COLA1'
source_id[key]['label_extended'] = 'COLA1'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'R15, 48 x 40 longitude/latitude; 9 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['a complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '1.5 x 1.5 degree, 240 x 120 longitude/latitude; 20 levels; enhanced horizontal resolution near the Equator'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Schneider et al., 1997 doi: 10.1175/1520-0493(1997)125<0680:ACAEIA>2.0.CO;2","Schneider and Zhu, 1998 doi: 10.1175/1520-0442(1998)011<1932:SOTSAC>2.0.CO;2"
]
source_id[key]['release_year'] = '1997'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'COLA2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1"
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ""
]
source_id[key]['institution_id'] = [
 'COLA'
]
source_id[key]['label'] = 'COLA2'
source_id[key]['label_extended'] = 'COLA2'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T30, 90 x 45 longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['a complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '3 x 3 degree, 120 x 60 longitude/latitude; 20 levels; enhanced horizontal resolution near the Equator'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Dewitt and Schneider, 1999 doi: 10.1175/1520-0493(1999)127<0381:TPDTAC>2.0.CO;2"
]
source_id[key]['release_year'] = '1999'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'CSIRO_Mk2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1","CMIP2"
]
source_id[key]['aliases']= [
 'csiro-c97a'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water","Momentum"
]
source_id[key]['institution_id'] = [
 'CSIRO'
]
source_id[key]['label'] = 'CSIRO Mk2'
source_id[key]['label_extended'] = 'CSIRO Mk2, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'R21, 64 x 56 longitude/latitude; 9 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['a complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '3.2 x 5.6 degree, 64 x 56 longitude/latitude; 20 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model","ice rheology included"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Gordon and O'Farrell, 1997 doi: 10.1175/1520-0493(1997)125<0875:TCCITC>2.0.CO;2"
]
source_id[key]['release_year'] = '1997'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'CSM_1.0'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1","CMIP2"
]
source_id[key]['aliases']= [
 'ncar-c97a'
 ]
source_id[key]['flux_adjustment'] = [
  ""
]
source_id[key]['institution_id'] = [
 'NCAR'
]
source_id[key]['label'] = 'CSM 1.0'
source_id[key]['label_extended'] = 'CSM 1.0'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, 128 x 64 longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['a complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '2 x 2.4 degree, 150 x 90 longitude/latitude; 45 levels; enhanced horizontal resolution near the Equator'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model","ice rheology included"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Boville and Gent, 1998 doi:10.1175/1520-0442(1998)011%3C1115:TNCSMV%3E2.0.CO;2"
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'CSM_1.3'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIPX?"
]
source_id[key]['aliases']= [
 'ncar-c02a,ncar-c02b,ncar-c03a,ncar-c03b--grid size doesnt match'
]
source_id[key]['flux_adjustment'] = [
  ""
]
source_id[key]['institution_id'] = [
 'NCAR'
]
source_id[key]['label'] = 'CSM 1.3'
source_id[key]['label_extended'] = 'CSM 1.3'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, 128 x 64 longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['a complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '2 x 2.4 degree, 150 x 90 longitude/latitude; 45 levels; enhanced horizontal resolution near the Equator'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model","ice rheology included"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Boville et al., 2001 doi: 10.1175/1520-0442(2001)014<0164:ITTNCF>2.0.CO;2"
]
source_id[key]['release_year'] = '2001'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'DOE_PCM'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP2"
]
source_id[key]['aliases']= [
 'pcm-c99a'
]
source_id[key]['flux_adjustment'] = [
  ""
]
source_id[key]['institution_id'] = [
 'NCAR'
]
source_id[key]['label'] = 'DOE PCM'
source_id[key]['label_extended'] = 'DOE PCM'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, 128 x 64 longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['a complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '0.67 x 0.67 degree, 537 x 269 longitude/latitude; 32 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model","ice rheology included"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Washington et al., 2000 doi: 10.1007/s003820000079"
]
source_id[key]['release_year'] = '2000'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'ECHAM1_LSG'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1"
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water","Momentum"
]
source_id[key]['institution_id'] = [
 'DKRZ'
]
source_id[key]['label'] = 'ECHAM1/LSG'
source_id[key]['label_extended'] = 'ECHAM1/LSG, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T21, 64 x 32 longitude/latitude; 19 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['a complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '4 x 4 degree, 90 x 45 longitude/latitude; 11 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Cubasch et al., 1992 doi:  10.1007/BF00209163","von Storch, 1994 doi: 10.1034/j.1600-0870.1994.t01-2-00007.x","von Storch et al., 1997 doi: 10.1175/1520-0442(1997)010<1525:ADOAYC>2.0.CO;2"
]
source_id[key]['release_year'] = '1992'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'ECHAM3_LSG'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1","CMIP2"
]
source_id[key]['aliases']= [
 'mpi-c96a'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water","Momentum"
]
source_id[key]['institution_id'] = [
 'DKRZ'
]
source_id[key]['label'] = 'ECHAM3/LSG'
source_id[key]['label_extended'] = 'ECHAM3/LSG, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T21, 64 x 32 longitude/latitude; 19 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['a complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '4 x 4 degree, 90 x 45 longitude/latitude; 11 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Cubasch et al., 1997 doi: 10.1007/s003820050196","Voss et al., 1998 doi: 10.1007/s003820050221"
]
source_id[key]['release_year'] = '1997'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'ECHAM4_OPCY3'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1"
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water-annual mean flux adjustment only"
]
source_id[key]['institution_id'] = [
 'DKRZ'
]
source_id[key]['label'] = 'ECHAM4/OPCY3'
source_id[key]['label_extended'] = 'ECHAM4/OPCY3, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, 128 x 64 longitude/latitude; 19 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['a complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '2.8 x 2.8 degree, 128 x 64 longitude/latitude; 11 levels; enhanced horizontal resolution near equator'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model","ice rheology included"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Roeckner et al., 1996 doi: 10.1007/s003820050140"
]
source_id[key]['release_year'] = '1996'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'GFDL_R15_a'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1","CMIP2"
]
source_id[key]['aliases']= [
 'no gfdls have matching res or levels (gfdl-c04a & gfdl-c03a)'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water"
]
source_id[key]['institution_id'] = [
 'GFDL'
]
source_id[key]['label'] = 'GFDL_R15_a'
source_id[key]['label_extended'] = 'GFDL_R15_a, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'R15, 48 x 40 longitude/latitude; 9 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['standard bucket hydrology scheme']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '4.5 x 3.7 degree, 96 x 40 longitude/latitude; 12 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model","free drift' dynamics"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Manabe et al., 1991 doi: 10.1175/1520-0442(1991)004<0785:TROACO>2.0.CO;2","Manabe and Stouffer, 1996 doi: 10.1175/1520-0442(1996)009<0376:LFVOSA>2.0.CO;2"
]
source_id[key]['release_year'] = '1991'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'GFDL_R15_b'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIPX?"
]
source_id[key]['aliases']= [
 'no gfdls have matching grid res or levels (gfdl-c04a &gfdl-c03a)'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water"
]
source_id[key]['institution_id'] = [
 'GFDL'
]
source_id[key]['label'] = 'GFDL_R15_b'
source_id[key]['label_extended'] = 'GFDL_R15_b, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'R15, 48 x 40 longitude/latitude; 9 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['standard bucket hydrology scheme']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '4.5 x 3.7 degree, 96 x 40 longitude/latitude; 12 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model","'free drift' dynamics"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Dixon and Lanzante, 1999 doi: 10.1029/1999GL900382"
]
source_id[key]['release_year'] = '1999'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'GFDL_R30_c'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP2+"
]
source_id[key]['aliases']= [
 'gfdl-c96a'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water"
]
source_id[key]['institution_id'] = [
 'GFDL'
]
source_id[key]['label'] = 'GFDL_R30_c'
source_id[key]['label_extended'] = 'GFDL_R30_c, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'R30, 96 x 80 longitude/latitude; 14 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['standard bucket hydrology scheme']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '1.875 x 2.25 degree, 160 x 96 longitude/latitude; 18 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model","'free drift' dynamics"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Knutson et al., 1999 doi: 10.1029/1999JD900965"
]
source_id[key]['release_year'] = '1999'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'GISS1'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1"
]
source_id[key]['aliases']= [
 'giss-nka??'
]
source_id[key]['flux_adjustment'] = [
  ""
]
source_id[key]['institution_id'] = [
 'GISS'
]
source_id[key]['label'] = 'GISS1'
source_id[key]['label_extended'] = 'GISS1'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 9 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 16 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Miller and Jiang, 1996 doi: 10.1175/1520-0442(1996)009<1599:SEFACV>2.0.CO;2"
]
source_id[key]['release_year'] = '1996'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'GISS2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1","CMIP2"
]
source_id[key]['aliases']= [
 'giss-nka??'
]
source_id[key]['flux_adjustment'] = [
  ""
]
source_id[key]['institution_id'] = [
 'GISS'
]
source_id[key]['label'] = 'GISS2'
source_id[key]['label_extended'] = 'GISS2'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 9 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 13 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Russell et al, 1995 doi: 10.1080/07055900.1995.9649550"
]
source_id[key]['release_year'] = '1995'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'GOALS'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1","CMIP2"
]
source_id[key]['aliases']= [
 'iap-nka'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water","Momentum"
]
source_id[key]['institution_id'] = [
 'IAP/LASG'
]
source_id[key]['label'] = 'GOALS'
source_id[key]['label_extended'] = 'GOALS, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'R15, 48 x 40 longitude/latitude; 9 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 20 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Wu et al., 1997 doi: 10.1007/BF02915398","Zhang et al., 2000 doi: ??????"
]
source_id[key]['release_year'] = '1997'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'HadCM2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1","CMIP2"
]
source_id[key]['aliases']= [
 'hadcm2-c95a'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water"
]
source_id[key]['institution_id'] = [
 'UKMO'
]
source_id[key]['label'] = 'HadCM2'
source_id[key]['label_extended'] = 'HadCM2, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '2.5 x 3.75 degree, 96 x 72 longitude/latitude; 19 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '2.5 x 3.75 degree, 144 x 48 longitude/latitude; 20 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model","'free drift' dynamics"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Johns, 1996 doi: ?????","Johns et al., 1997 doi: 10.1007/s003820050155"
]
source_id[key]['release_year'] = '1996'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'HadCM3'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP2"
]
source_id[key]['aliases']= [
 'hadcm3-c97a'
]
source_id[key]['flux_adjustment'] = [
  ""
]
source_id[key]['institution_id'] = [
 'UKMO'
]
source_id[key]['label'] = 'HadCM3'
source_id[key]['label_extended'] = 'HadCM3'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '2.5 x 3.75 degree, 96 x 72 longitude/latitude; 19 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '1.25 x 1.25 degree, 288 x 144 longitude/latitude; 20 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model","'free drift' dynamics"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Gordon et al., 2000 doi: 10.1007/s003820050010"
]
source_id[key]['release_year'] = '2000'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'IPSL-CM1'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1"
]
source_id[key]['aliases']= [
 'lmd-nka?? --the lat long dimensions are reversed?'
]
source_id[key]['flux_adjustment'] = [
  ""
]
source_id[key]['institution_id'] = [
 'IPSL/LMD'
]
source_id[key]['label'] = 'IPSL-CM1'
source_id[key]['label_extended'] = 'IPSL-CM1'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '5.6 x 3.8 degree, 94 x 32 longitude/latitude; 15 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '2 x 2 degree, 180 x 90 longitude/latitude; 31 levels; enhanced horizontal resolution near the Equator'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["ice extent/thickness determined diagnostically from ocean surface temperature"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Braconnot et al., 2000 doi: 10.1175/1520-0442(2000)013<1537:OFIRTK>2.0.CO;2"
]
source_id[key]['release_year'] = '2000'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'IPSL-CM2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP2"
]
source_id[key]['aliases']= [
 'lmd-nka?? --the lat long dimensions are reversed?'
]
source_id[key]['flux_adjustment'] = [
  ""
]
source_id[key]['institution_id'] = [
 'IPSL/LMD'
]
source_id[key]['label'] = 'IPSL-CM2'
source_id[key]['label_extended'] = 'IPSL-CM2'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '5.6 x 3.8 degree, 94 x 32 longitude/latitude; 15 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '2 x 2 degree, 180 x 90 longitude/latitude; 31 levels; enhanced horizontal resolution near the Equator'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Laurent et al., 1998 doi: ??????"
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'MRI1'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1","CMIP2","model MRI1 exists in two versions. at time of writing more data was available for earlier version whos control run is in CMIP1 database. The later model has two extra ocean levels and a modified ocean mixing scheme, its control run is in CMIP2 databas, the equillibrium climate sensitivites and transient climate responses of the two models are the same."
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water"
]
source_id[key]['institution_id'] = [
 'MRI'
]
source_id[key]['label'] = 'MRI1'
source_id[key]['label_extended'] = 'MRI1, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 15 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ["multi-layer temperature scheme","standard bucket hydrology scheme"]
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '2 x 2.5 degree, 144 x 90 longitude/latitude; 21 levels; enhanced horizontal resolution near the Equator'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model","'free drift' dynamics"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Tokioka et al., 1996 doi: 10.2151/jmsj1965.73.4_817"
]
source_id[key]['release_year'] = '1996'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'MRI2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP2+"
]
source_id[key]['aliases']= [
 'mri-c02a'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water","Momentum"
]
source_id[key]['institution_id'] = [
 'MRI'
]
source_id[key]['label'] = 'MRI2'
source_id[key]['label_extended'] = 'MRI2, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, 128 x 64 longitude/latitude; 30 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['complex land surface scheme usually including multi-soil layers for temperature and soil moisture, and an explicit representation of canopy processes']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '2 x 2.5 degree, 144 x 90 longitude/latitude; 23 levels; enhanced horizontal resolution near the Equator'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model","'free drift' dynamics"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Yukimoto et al., 2000 doi: 10.1029/2000JC900034"
]
source_id[key]['release_year'] = '2000'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'NCAR1'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1","CMIP2"
]
source_id[key]['aliases']= [
 'NO NCAR MODELS MATCH RES or levels???'
]
source_id[key]['flux_adjustment'] = [
  ""
]
source_id[key]['institution_id'] = [
 'NCAR'
]
source_id[key]['label'] = 'NCAR1'
source_id[key]['label_extended'] = 'NCAR1'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'R15, 48 x 40 longitude/latitude; 9 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['standard bucket hydrology scheme']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '1 x 1 degree, 360 x 180 longitude/latitude; 20 levels'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model","ice rheology included"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Meehl and Washington, 1995 doi: 10.1007/BF00209514","Washington and Meehl, 1996 doi: 10.1029/96JD00505"
]
source_id[key]['release_year'] = '1995'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'NRL'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'CMIP'
]
source_id[key]['cohort'] = [
 "CMIP1","CMIP2"
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  "Heat","Fresh Water-annual mean flux adjustment only"
]
source_id[key]['institution_id'] = [
 'NRL'
]
source_id[key]['label'] = 'NRL'
source_id[key]['label_extended'] = 'NRL, flux adjusted'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T47, 144 x 72 longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['land'] = {}
source_id[key]['model_component']['land']['description'] = ['modified bucket scheme with spatially varying soil moisture capacity and/or a surface resistance']
source_id[key]['model_component']['land']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['ocean'] = {}
source_id[key]['model_component']['ocean']['description'] = '1 x 2.0 degree, 180 x 180 longitude/latitude; 25 levels; enhanced horizontal resolution near Equator'
source_id[key]['model_component']['ocean']['nominal_resolution'] = '??? km'
source_id[key]['model_component']['seaIce'] = {}
source_id[key]['model_component']['seaIce']['description'] = ["thermodynamic ice model","ice extent prescribed"]
source_id[key]['model_component']['seaIce']['nominal_resolution'] = '??? km'
source_id[key]['reference'] = [
 "Hogan and Li, 1997 doi: ?????","Li and Hogan, 1999 doi: 10.1175/1520-0442(1999)012<0780:TROTAM>2.0.CO;2"
]
source_id[key]['release_year'] = '1997'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key

source_id['notes']={}
source_id['notes']['notes']='NO obvious potential matches for md-c99a(96*48 lon8lat) or mpi-c96a(128*64 lon*lat), ncar: have 4 aliases that need to be matched but only 3 source ids that seem related to ncar'
source_id['notes']['aliases']='none'

j = json.dumps(source_id, sort_keys=True, indent=4, ensure_ascii=True,separators=(',',':'))
f = open('/export/musci2/CMIP1&2_source_id.json', 'w')
print >> f, j
f.close()