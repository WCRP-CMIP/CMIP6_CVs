#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 11:46:56 2017

@author: musci2
"""
#%% Import statements
#import copy ; # Useful for copy.deepcopy() of dictionaries
import datetime
import gc
import json
import os,sys
import shlex
import ssl
import subprocess
sys.path.insert(0,'/export/musci2/git/durolib/lib') ; # Add Paul's library to python path
from durolib import readJsonCreateDict
from durolib import getGitInfo
#import pyexcel_xlsx as pyx ; # requires openpyxl ('pip install openpyxl'), pyexcel-io ('git clone https://github.com/pyexcel/pyexcel-io')
# pyexcel-xlsx ('git clone https://github.com/pyexcel/pyexcel-xlsx'), and unidecode ('conda install unidecode')
#from string import replace
#from unidecode import unidecode
#import pdb

#%% Define functions
# Get repo metadata
def getFileHistory(filePath):
    # Call getGitInfo
    versionInfo = getGitInfo(filePath)
    if versionInfo == None:
        return None
    else:
        # print results
        #for count in range(0,len(versionInfo)):
        #    print count,versionInfo[count]

        version_metadata = {}
        version_metadata['author'] = versionInfo[4].replace('author: ','')
        version_metadata['creation_date'] = versionInfo[3].replace('date: ','')
        version_metadata['institution_id'] = 'PCMDI'
        version_metadata['latest_tag_point'] = versionInfo[2].replace('latest_tagPoint: ','')
        version_metadata['note'] = versionInfo[1].replace('note: ','')
        version_metadata['previous_commit'] = versionInfo[0].replace('commit: ','')

        #print version_metadata

        return version_metadata


#%% Create source_id dictionary
source_id= dict()
key = '24-L_ST-GCM'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'uiuc-98a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'UIUC'
]
source_id[key]['label'] = '24-L_ST-GCM'
source_id[key]['label_extended'] = '24-L_ST-GCM'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 24 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ''
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'A5407.VI'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'DNM'
]
source_id[key]['label'] = 'A5407.VI'
source_id[key]['label_extended'] = 'A5407.VI'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 7 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Galin","Dymnikov"
]
source_id[key]['release_year'] = '1991'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'A5421'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'dnm-98a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'DNM'
]
source_id[key]['label'] = 'A5421'
source_id[key]['label_extended'] = 'A5421'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 21 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'AGCM'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'ccsr-98a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'CCSR/NIES'
]
source_id[key]['label'] = 'AGCM'
source_id[key]['label_extended'] = 'AGCM'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'AGCM_6.4'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'UCLA'
]
source_id[key]['label'] = 'AGCM 6.4'
source_id[key]['label_extended'] = 'AGCM 6.4'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 15 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Mechoso"
]
source_id[key]['release_year'] = '1992'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'AMIP2.01'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'mgo-01a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'MGO'
]
source_id[key]['label'] = 'AMIP2.01'
source_id[key]['label_extended'] = 'AMIP2.01'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 14 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Mechoso"
]
source_id[key]['release_year'] = '2001'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'AMIP92'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'MGO'
]
source_id[key]['label'] = 'AMIP92'
source_id[key]['label_extended'] = 'AMIP92'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T30, ?? x ?? longitude/latitude; 14 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Meleshko"
]
source_id[key]['release_year'] = '1992'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'ARPEGE_Cy18'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'cnrm-00a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'CNRM'
]
source_id[key]['label'] = 'ARPEGE Cy18'
source_id[key]['label_extended'] = 'ARPEGE Cy18'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T63, ?? x ?? longitude/latitude; 45 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '2000'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'B295DM12'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'giss-98a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'GISS'
]
source_id[key]['label'] = 'B295DM12'
source_id[key]['label_extended'] = 'B295DM12'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 12 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'BMRC_2.3'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'BMRC'
]
source_id[key]['label'] = 'BMRC 2.3'
source_id[key]['label_extended'] = 'BMRC 2.3'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'R31, ?? x ?? longitude/latitude; 9 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "McAvaney"
]
source_id[key]['release_year'] = '1990'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'CCM1-TG'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'SUNYA'
]
source_id[key]['label'] = 'CCM1-TG'
source_id[key]['label_extended'] = 'CCM1-TG'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'R15, ?? x ?? longitude/latitude; 12 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Wang"
]
source_id[key]['release_year'] = '1990'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'CCM2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'pnnl-97a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'PNNL'
]
source_id[key]['label'] = 'CCM2'
source_id[key]['label_extended'] = 'CCM2'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1997'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'CCM2 '
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'NCAR'
]
source_id[key]['label'] = 'CCM2'
source_id[key]['label_extended'] = 'CCM2'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Williamson"
]
source_id[key]['release_year'] = '1992'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'CCM3'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'sunya-99a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'SUNYA'
]
source_id[key]['label'] = 'CCM3'
source_id[key]['label_extended'] = 'CCM3'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Williamson"
]
source_id[key]['release_year'] = '1999'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'CCM3.5'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'ncar-98a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'NCAR'
]
source_id[key]['label'] = 'CCM3.5'
source_id[key]['label_extended'] = 'CCM3.5'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'CDG1'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'GFDL'
]
source_id[key]['label'] = 'CDG1'
source_id[key]['label_extended'] = 'CDG1'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'R30, ?? x ?? longitude/latitude; 14 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Wetherald"
]
source_id[key]['release_year'] = '1992'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'COLA_1.1'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'COLA'
]
source_id[key]['label'] = 'COLA 1.1'
source_id[key]['label_extended'] = 'COLA 1.1'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'R40, ?? x ?? longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Straus"
]
source_id[key]['release_year'] = '1993'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'CSIRO_9_Mark_1'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'CSIRO'
]
source_id[key]['label'] = 'CSIRO 9 Mark_1'
source_id[key]['label_extended'] = 'CSIRO 9 Mark_1'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'R21, ?? x ?? longitude/latitude; 9 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Hunt"
]
source_id[key]['release_year'] = '1992'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'CSU_91'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'CSU'
]
source_id[key]['label'] = 'CSU 91'
source_id[key]['label_extended'] = 'CSU 91'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 17 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Randall"
]
source_id[key]['release_year'] = '1991'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'CY18R5'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'ecmwf-98a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'ECMWF'
]
source_id[key]['label'] = 'CY18R5'
source_id[key]['label_extended'] = 'CY18R5'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 21 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'ECHAM3'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'MPI'
]
source_id[key]['label'] = 'ECHAM3'
source_id[key]['label_extended'] = 'ECHAM3'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 19 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Dumenil","Schlese"
]
source_id[key]['release_year'] = '1992'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'ECHAM4'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'mpi-98a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'MPI'
]
source_id[key]['label'] = 'ECHAM4'
source_id[key]['label_extended'] = 'ECHAM4'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 19 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'ECMWF_Cy36'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'ECMWF'
]
source_id[key]['label'] = 'ECMWF Cy36'
source_id[key]['label_extended'] = 'ECMWF Cy36'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 19 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Ferranti","Burridge"
]
source_id[key]['release_year'] = '1990'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'EMERAUDE'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'CNRM'
]
source_id[key]['label'] = 'EMERAUDE'
source_id[key]['label_extended'] = 'EMERAUDE'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 30 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Deque"
]
source_id[key]['release_year'] = '1992'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'GCM-01.0_AMIP-01'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'GLA'
]
source_id[key]['label'] = 'GCM-01.0 AMIP-01'
source_id[key]['label_extended'] = 'GCM-01.0 AMIP-01'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 17 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Lau"
]
source_id[key]['release_year'] = '1992'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'GCM-II'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'MRI'
]
source_id[key]['label'] = 'GCM-II'
source_id[key]['label_extended'] = 'GCM-II'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 15 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Kitoh","Tokioka"
]
source_id[key]['release_year'] = '1993'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'GCM3'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'cccma-99a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'CCCma'
]
source_id[key]['label'] = 'GCM3'
source_id[key]['label_extended'] = 'GCM3'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T47, ?? x ?? longitude/latitude; 32 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1999'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key





key = 'GCM_II '
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'CCCma'
]
source_id[key]['label'] = 'GCM_II'
source_id[key]['label_extended'] = 'GCM_II'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T32, ?? x ?? longitude/latitude; 10 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Boer"
]
source_id[key]['release_year'] = '1990'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'GENESIS_1.5'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'SUNYA/NCAR'
]
source_id[key]['label'] = 'GENESIS 1.5'
source_id[key]['label_extended'] = 'GENESIS 1.5'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T31, ?? x ?? longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Wang","Thompson"
]
source_id[key]['release_year'] = '1994'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'GEOS-1'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'GSFC'
]
source_id[key]['label'] = 'GEOS-1'
source_id[key]['label_extended'] = 'GEOS-1'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 20 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Park"
]
source_id[key]['release_year'] = '1993'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'GEOS-2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'gla-98a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'GLA'
]
source_id[key]['label'] = 'GEOS-2'
source_id[key]['label_extended'] = 'GEOS-2'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 20 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'GFDLSM392.2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'derf-98a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'DERF'
]
source_id[key]['label'] = 'GFDLSM392.2'
source_id[key]['label_extended'] = 'GFDLSM392.2'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'GFDL_SM392.2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'DERF'
]
source_id[key]['label'] = 'GFDL SM392.2'
source_id[key]['label_extended'] = 'GFDL SM392.2'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Miyakoda"
]
source_id[key]['release_year'] = '1993'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'GSM8911'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'JMA'
]
source_id[key]['label'] = 'GSM8911'
source_id[key]['label_extended'] = 'GSM8911'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 21 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Sato"
]
source_id[key]['release_year'] = '1993'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'GSM9603'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'jma-98a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'JMA'
]
source_id[key]['label'] = 'GSM9603'
source_id[key]['label_extended'] = 'GSM9603'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T63, ?? x ?? longitude/latitude; 30 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'HADAM3'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'ugamp-98a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'UGAMP'
]
source_id[key]['label'] = 'HADAM3'
source_id[key]['label_extended'] = 'HADAM3'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '3.75 x 2.5 degree, 144 x 48 longitude/latitude; 58 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'HADAM3_uk'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'ukmo-98a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'UKMO'
]
source_id[key]['label'] = 'HADAM3'
source_id[key]['label_extended'] = 'HADAM3'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '3.75 x 2.5 degree, 144 x 48 longitude/latitude; 19 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'IAP-2L'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'IAP'
]
source_id[key]['label'] = 'IAP-2L'
source_id[key]['label_extended'] = 'IAP-2L'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 2 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Wang","Zeng"
]
source_id[key]['release_year'] = '1993'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'JMA98'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'mri-98a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'MRI'
]
source_id[key]['label'] = 'JMA98'
source_id[key]['label_extended'] = 'JMA98'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 30 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'LMD5'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'LMD'
]
source_id[key]['label'] = 'LMD5'
source_id[key]['label_extended'] = 'LMD5'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '3.6 x 5.6 degree, 64 x 50 longitude/latitude; 11 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Polcher"
]
source_id[key]['release_year'] = '1991'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'MLAM-AMIP'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'UIUC'
]
source_id[key]['label'] = 'MLAM-AMIP'
source_id[key]['label_extended'] = 'MLAM-AMIP'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 17 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Schlesinger"
]
source_id[key]['release_year'] = '1993'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'MODEL_II_Prime'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'GISS'
]
source_id[key]['label'] = 'MODEL II Prime'
source_id[key]['label_extended'] = 'MODEL II Prime'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 9 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Lo","Del Genio"
]
source_id[key]['release_year'] = '1994'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'MRF'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'NCEP'
]
source_id[key]['label'] = 'MRF'
source_id[key]['label_extended'] = 'MRF'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T40, ?? x ?? longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "van den Dool","Kalnay"
]
source_id[key]['release_year'] = '1992'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'NOGAPS_3.2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'NRL'
]
source_id[key]['label'] = 'NOGAPS 3.2'
source_id[key]['label_extended'] = 'NOGAPS 3.2'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Rosmond"
]
source_id[key]['release_year'] = '1993'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'NTU__'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'ntu-01a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'NTU'
]
source_id[key]['label'] = 'NTU???'
source_id[key]['label_extended'] = 'NTU???'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '2001'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'NWP-D40P29'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'RPN'
]
source_id[key]['label'] = 'NWP-D40P29'
source_id[key]['label_extended'] = 'NWP-D40P29'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 21 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Ritchie"
]
source_id[key]['release_year'] = '1993'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'REANL2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'ncep-99a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'NCEP'
]
source_id[key]['label'] = 'REANL2'
source_id[key]['label_extended'] = 'REANL2'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 18levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key



key = 'ST15'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'yonu-98a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'YONU'
]
source_id[key]['label'] = 'ST15'
source_id[key]['label_extended'] = 'ST15'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 15 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '1998'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'TR_5.1'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'YONU'
]
source_id[key]['label'] = 'TR 5.1'
source_id[key]['label_extended'] = 'TR 5.1'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '4 x 5 degree, 72 x 45 longitude/latitude; 5 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Oh"
]
source_id[key]['release_year'] = '1994'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'UGCM_1.3'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'UGAMP'
]
source_id[key]['label'] = 'UGCM_1.3'
source_id[key]['label_extended'] = 'UGCM_1.3'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'T42, ?? x ?? longitude/latitude; 19 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Blackburn","Slingo"
]
source_id[key]['release_year'] = '1993'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'UGEM_NWP'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'rpn-01a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'RPN'
]
source_id[key]['label'] = 'UGEM NWP'
source_id[key]['label_extended'] = 'UGEM NWP'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'G1.875???, ?? x ?? longitude/latitude; 40 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '2001'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'UM-CLIMATE'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP1'
]
source_id[key]['aliases']= [
 'TBD'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'RPN'
]
source_id[key]['label'] = 'UM-CLIMATE'
source_id[key]['label_extended'] = 'UM-CLIMATE'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = '2.5 x 3.75 degree, 96 x 72 longitude/latitude; 20 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 "Pope"
]
source_id[key]['release_year'] = '1993'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key




key = 'V2.2'
source_id[key] = {}
source_id[key]['activity_participation'] = [
 'AMIP'
]
source_id[key]['cohort'] = [
 'AMIP2'
]
source_id[key]['aliases']= [
 'cola-00a'
]
source_id[key]['flux_adjustment'] = [
  ''
]
source_id[key]['institution_id'] = [
 'COLA'
]
source_id[key]['label'] = 'V2.2'
source_id[key]['label_extended'] = 'V2.2'
source_id[key]['model_component'] = {}
source_id[key]['model_component']['atmos'] = {}
source_id[key]['model_component']['atmos']['description'] = 'R40, ?? x ?? longitude/latitude; 18 levels'
source_id[key]['model_component']['atmos']['nominal_resolution'] = '???'
source_id[key]['reference'] = [
 ""
]
source_id[key]['release_year'] = '2000'
source_id[key]['notes'] = ''
source_id[key]['source_id'] = key

j = json.dumps(source_id, sort_keys=True, indent=4, ensure_ascii=True,separators=(',',':'))
f = open('AMIP1&2_source_id.json', 'w')
print >> f, j
f.close()

