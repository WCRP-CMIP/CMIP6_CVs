#!/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 14:12:21 2016

Paul J. Durack 11th July 2016

This script generates all controlled vocabulary (CV) json files residing this this subdirectory

PJD 11 Jul 2016    - Started
PJD 17 May 2017    - Revise source_id EMAC-2-53-Vol https://github.com/WCRP-CMIP/CMIP6_CVs/issues/231
PJD 27 May 2017    - Rename and revise sspxy to ssp119 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/329
PJD 27 May 2017    - Revise source_id CanESM5 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/330
PJD 30 May 2017    - Revise institution_id NCAR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/335
PJD 30 May 2017    - Remove frequency 3hrClim https://github.com/WCRP-CMIP/CMIP6_CVs/issues/334
                   - TODO: Generate table_id from dataRequest https://github.com/WCRP-CMIP/CMIP6_CVs/issues/166
                   - TODO: Redirect sources to CMIP6_CVs master files (not cmip6-cmor-tables) ; coordinate, formula_terms, grids
                   - TODO: Generate function for json compositing

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

#%% Set commit message
commitMessage = '\"CreateCMIP2 source_id json file\"'

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

#%% Create urllib2 context to deal with lab/LLNL web certificates
ctx                 = ssl.create_default_context()
ctx.check_hostname  = False
ctx.verify_mode     = ssl.CERT_NONE

#%% List target controlled vocabularies (CVs)
masterTargets = [
    'activity_id',
    'experiment_id',
    'frequency',
    'grid_label',
    'institution_id',
    'license',
    'mip_era',
    'nominal_resolution',
    'realm',
    'required_global_attributes',
    'source_id',
    'source_type',
    'sub_experiment_id',
    'table_id'
]

#%% Activities
activity_id = [
    'AerChemMIP',
    'C4MIP',
    'CFMIP',
    'CMIP',
    'CORDEX',
    'DAMIP',
    'DCPP',
    'DynVarMIP',
    'FAFMIP',
    'GMMIP',
    'GeoMIP',
    'HighResMIP',
    'ISMIP6',
    'LS3MIP',
    'LUMIP',
    'OMIP',
    'PMIP',
    'RFMIP',
    'SIMIP',
    'ScenarioMIP',
    'VIACSAB',
    'VolMIP'
]

#%% Experiments
tmp = [['experiment_id','https://raw.githubusercontent.com/bmusci3/CMIP6_CVs/master/CMIP6_experiment_id.json']
      ] ;
experiment_id = readJsonCreateDict(tmp)
experiment_id = experiment_id.get('experiment_id')
experiment_id = experiment_id.get('experiment_id') ; # Fudge to extract duplicate level

# Fix issues
#==============================================================================
# Example new experiment_id entry
#key = 'ssp119'
#experiment_id[key] = {}
#experiment_id[key]['activity_id'] = ['ScenarioMIP']
#experiment_id[key]['additional_allowed_model_components'] = ['AER','CHEM','BGC']
#experiment_id[key]['description'] = 'Future scenario with low radiative forcing throughout reaching about 1.9 W/m2 in 2100 based on SSP1. Concentration-driven'
#experiment_id[key]['end_year'] = '2100'
#experiment_id[key]['experiment'] = 'low-end scenario reaching 1.9 W m-2, based on SSP1'
#experiment_id[key]['experiment_id'] = key
#experiment_id[key]['min_number_yrs_per_sim'] = '86'
#experiment_id[key]['parent_activity_id'] = ['CMIP']
#experiment_id[key]['parent_experiment_id'] = ['historical']
#experiment_id[key]['required_model_components'] = ['AOGCM']
#experiment_id[key]['start_year'] = '2015'
#experiment_id[key]['sub_experiment_id'] = ['none']
#experiment_id[key]['tier'] = '2'
# Rename
#experiment_id['land-noShiftCultivate'] = experiment_id.pop('land-noShiftcultivate')
# Remove
#experiment_id.pop('land-noShiftcultivate')
#==============================================================================
'''
# xlsx import
# Fields
# Alpha/json order, xlsx column, value
# 1  0  experiment_id string
# 2  1  activity_id list
# 3  8  additional_allowed_model_components list
# 4  13 description string
# 5  10 end_year string
# 6  2  experiment string
# 7  11 min_number_yrs_per_sim string
# 8  12 parent_activity_id list
# 9  6  parent_experiment_id list
# 10 7  required_model_components list
# 11 9  start_year string
# 12 5  sub_experiment string
# 13 4  sub_experiment_id string
# 14 3  tier string

os.chdir('/sync/git/CMIP6_CVs/src')
inFile = '170307_CMIP6_expt_list.xlsx'
data = pyx.get_data(inFile)
data = data['Sheet1']
headers = data[3]
experiment_id = {}
for count in range(4,len(data)):
    if data[count] == []:
        #print count,'blank field'
        continue
    row = data[count]
    key = row[0] ; #replace(row[0],'_ ','_')
    experiment_id[key] = {}
    for count2,entry in enumerate(headers):
        if count2 == 5:
            continue ; # Skip sub_experiment
        entry = replace(entry,'_ ','_') ; # clean up spaces
        entry = replace(entry,' ', '_') ; # replace spaces with underscores
        if count2 >= len(row):
            experiment_id[key][entry] = ''
            continue
        value = row[count2]
        if count2 in [1,4,6,7,8,12]:
            if value == None:
                pass
            elif value == 'no parent':
                pass
            elif 'no parent,' in value:
                value = ['no parent',replace(value,'no parent,','').strip()] ; # deal with multiple entries (including 'no parent')
                pass
            else:
                value = replace(value,',','') ; # remove ','
                value = value.split() ; # Change type to list
                #print value
        if type(value) == long:
            experiment_id[key][entry] = str(value) ; #replace(str(value),' ','')
        elif type(value) == list:
            experiment_id[key][entry] = value
        elif value == None:
            experiment_id[key][entry] = '' ; # changed from none to preserve blank entries
        else:
            value = replace(value,'    ',' ') ; # replace whitespace
            value = replace(value,'   ',' ') ; # replace whitespace
            value = replace(value,'  ',' ') ; # replace whitespace
            experiment_id[key][entry] = unidecode(value) ; #replace(unidecode(value),' ','')
            try:
                unidecode(value)
            except:
                print count,count2,key,entry,value
del(inFile,data,headers,count,row,key,entry,value) ; gc.collect()
'''

#%% Frequencies
frequency = [
    '1hr',
    '1hrClimMon',
    '3hr',
    '6hr',
    'day',
    'decadal',
    'fx',
    'mon',
    'monClim',
    'subhr',
    'yr',
    'yrClim']

#%% Grid labels
grid_label = [
    'gm',
    'gn',
    'gna',
    'gng',
    'gnz',
    'gr',
    'gr1',
    'gr1a',
    'gr1g',
    'gr1z',
    'gr2',
    'gr2a',
    'gr2g',
    'gr2z',
    'gr3',
    'gr3a',
    'gr3g',
    'gr3z',
    'gr4',
    'gr4a',
    'gr4g',
    'gr4z',
    'gr5',
    'gr5a',
    'gr5g',
    'gr5z',
    'gr6',
    'gr6a',
    'gr6g',
    'gr6z',
    'gr7',
    'gr7a',
    'gr7g',
    'gr7z',
    'gr8',
    'gr8a',
    'gr8g',
    'gr8z',
    'gr9',
    'gr9a',
    'gr9g',
    'gr9z',
    'gra',
    'grg',
    'grz'
]

#%% Institutions
institution_id = {
    'AWI': 'Alfred Wegener Institute, Helmholtz Centre for Polar and Marine Research, Am Handelshafen 12, 27570 Bremerhaven, Germany',
    'BNU': 'Beijing Normal University, Beijing 100875, China',
    'CAMS': 'Chinese Academy of Meteorological Sciences, Beijing 100081, China',
    'CCCR-IITM': 'Centre for Climate Change Research, Indian Institute of Tropical Meteorology Pune, Maharashtra 411 008, India',
    'CCCma': 'Canadian Centre for Climate Modelling and Analysis, Victoria, BC V8P 5C2, Canada',
    'CMCC': 'Fondazione Centro Euro-Mediterraneo sui Cambiamenti Climatici, Lecce 73100, Italy',
    'CNRM-CERFACS': 'CNRM (Centre National de Recherches Meteorologiques, Toulouse 31057, France), CERFACS (Centre Europeen de Recherche et de Formation Avancee en Calcul Scientifique, Toulouse 31100, France)',
    'COLA-CFS': 'Center for Ocean-Land-Atmosphere Studies, Fairfax, VA 22030, USA',
    'CSIR-CSIRO': 'CSIR (Council for Scientific and Industrial Research - Natural Resources and the Environment, Pretoria, 0001, South Africa), CSIRO (Commonwealth Scientific and Industrial Research Organisation and Bureau of Meteorology, Melbourne, Victoria 3208, Australia)',
    'CSIRO-BOM': 'Commonwealth Scientific and Industrial Research Organisation and Bureau of Meteorology, Melbourne, Victoria 3208, Australia',
    'EC-Earth-Consortium': 'KNMI, The Netherlands; SMHI, Sweden; DMI, Denmark; AEMET, Spain; Met Eireann, Ireland; CNR-ISAC, Italy; Instituto de Meteorologia, Portugal; FMI, Finland; BSC, Spain; Centro de Geofisica, University of Lisbon, Portugal; ENEA, Italy; Geomar, Germany; Geophysical Institute, University of Bergen, Norway; ICHEC, Ireland; ICTP, Italy; IMAU, The Netherlands; IRV, Sweden;  Lund University, Sweden; Meteorologiska Institutionen, Stockholms University, Sweden; Niels Bohr Institute, University of Copenhagen, Denmark; NTNU, Norway; SARA, The Netherlands; Unite ASTR, Belgium; Universiteit Utrecht, The Netherlands; Universiteit Wageningen, The Netherlands; University College Dublin, Ireland; Vrije Universiteit Amsterdam, the Netherlands; University of Helsinki, Finland; KIT, Karlsruhe, Germany; USC, University of Santiago de Compostela, Spain; Uppsala Universitet, Sweden; NLeSC, Netherlands eScience Center, The Netherlands',
    'FIO-RONM': 'FIO (First Institute of Oceanography, State Oceanic Administration, Qingdao 266061, China), RONM (Laboratory for Regional Oceanography and Numerical Modeling, Qingdao National Laboratory for Marine Science and Technology, Qingdao 266237, China)',
    'INM': 'Institute for Numerical Mathematics, Moscow 119991, Russia',
    'INPE': 'National Institute for Space Research, Cachoeira Paulista, SP 12630-000, Brazil',
    'IPSL': 'Institut Pierre Simon Laplace, Paris 75252, France',
    'LASG-IAP': 'Institute of Atmospheric Physics, Chinese Academy of Sciences, Beijing 100029, China',
    'MESSy-Consortium': 'The Modular Earth Submodel System (MESSy) Consortium, represented by the Institute for Physics of the Atmosphere, Deutsches Zentrum fur Luft- und Raumfahrt (DLR), Wessling, Bavaria 82234, Germany',
    'MIROC': 'JAMSTEC (Japan Agency for Marine-Earth Science and Technology, Kanagawa 236-0001, Japan), AORI (Atmosphere and Ocean Research Institute, The University of Tokyo, Chiba 277-8564, Japan), NIES (National Institute for Environmental Studies, Ibaraki 305-8506, Japan), and AICS (RIKEN Advanced Institute for Computational Science, Hyogo 650-0047, Japan)',
    'MOHC': 'Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK',
    'MPI-M': 'Max Planck Institute for Meteorology, Hamburg 20146, Germany',
    'MRI': 'Meteorological Research Institute, Tsukuba, Ibaraki 305-0052, Japan',
    'NASA-GISS': 'Goddard Institute for Space Studies, New York, NY 10025, USA',
    'NCAR': 'National Center for Atmospheric Research, Boulder, CO 80301, USA',
    'NCC': 'NorESM Climate modeling Consortium consisting of CICERO (Center for International Climate and Environmental Research, Oslo 0349), MET-Norway (Norwegian Meteorological Institute, Oslo 0313), NERSC (Nansen Environmental and Remote Sensing Center, Bergen 5006), NILU (Norwegian Institute for Air Research, Kjeller 2027), UiB (University of Bergen, Bergen 5007), UiO (University of Oslo, Oslo 0313) and UNI (Uni Research, Bergen 5008), Norway',
    'NERC': 'Natural Environment Research Council, STFC-RAL, Harwell, Oxford, OX11 0QX, UK',
    'NIMS-KMA': 'National Institute of Meteorological Sciences/Korea Meteorological Administration, Climate Research Division, Seoho-bukro 33, Seogwipo-si, Jejudo 63568, Republic of Korea',
    'NOAA-GFDL': 'National Oceanic and Atmospheric Administration, Geophysical Fluid Dynamics Laboratory, Princeton, NJ 08540, USA',
    'NOAA-NCEP': 'National Oceanic and Atmospheric Administration, National Centers for Environmental Prediction, Camp Springs, MD 20746, USA',
    'NUIST': 'Nanjing University of Information Science and Technology, Nanjing, 210044, China',
    'PCMDI': 'Program for Climate Model Diagnosis and Intercomparison, Lawrence Livermore National Laboratory, Livermore, CA 94550, USA',
    'THU': 'Department of Earth System Science, Tsinghua University, Beijing 100084, China'
}

#%% CMIP6 License
license = [
    'CMIP6 model data produced by <Your Centre Name> is licensed under a Creative Commons Attribution-[NonCommercial-]ShareAlike 4.0 International License (https://creativecommons.org/licenses). Consult https://pcmdi.llnl.gov/CMIP6/TermsOfUse for terms of use governing CMIP6 output, including citation requirements and proper acknowledgment. Further information about this data, including some limitations, can be found via the further_info_url (recorded as a global attribute in this file)[ and at <some URL maintained by modeling group>]. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law.'
]

#%% MIP eras
mip_era = ['CMIP1', 'CMIP2', 'CMIP3', 'CMIP5', 'CMIP6']

#%% Nominal resolutions
nominal_resolution = [
    '0.5 km',
    '1 km',
    '10 km',
    '100 km',
    '1000 km',
    '10000 km',
    '1x1 degree',
    '2.5 km',
    '25 km',
    '250 km',
    '2500 km',
    '5 km',
    '50 km',
    '500 km',
    '5000 km'
]

#%% Realms
realm = {
    'aerosol': 'Aerosol',
    'atmos': 'Atmosphere',
    'atmosChem': 'Atmospheric Chemistry',
    'land': 'Land Surface',
    'landIce': 'Land Ice',
    'ocean': 'Ocean',
    'ocnBgchem': 'Ocean Biogeochemistry',
    'seaIce': 'Sea Ice'
}

#%% Required global attributes
required_global_attributes = [
    'Conventions',
    'activity_id',
    'creation_date',
    'data_specs_version',
    'experiment',
    'experiment_id',
    'forcing_index',
    'frequency',
    'further_info_url',
    'grid',
    'grid_label',
    'initialization_index',
    'institution',
    'institution_id',
    'license',
    'mip_era',
    'nominal_resolution',
    'physics_index',
    'product',
    'realization_index',
    'realm',
    'source',
    'source_id',
    'source_type',
    'sub_experiment',
    'sub_experiment_id',
    'table_id',
    'tracking_id',
    'variable_id',
    'variant_label'
]

#%% Source identifiers
#tmp = [['source_id','https://raw.githubusercontent.com/bmusci3/CMIP6_CVs/master/CMIP2_source_id.json']
#      ] ;
#source_id = readJsonCreateDict(tmp)
#source_id = source_id.get('source_id')
#source_id = source_id.get('source_id') ; # Fudge to extract duplicate level

source_id = {}
# Fix issues
#==============================================================================
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
 'TBD'
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
 'TBD'
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
 'TBD'
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
 ""
]
source_id[key]['aliases']= [
 'TBD'
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
 ""
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
 'TBD'
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
 'TBD'
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
 ""
]
source_id[key]['aliases']= [
 'TBD'
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
 'TBD'
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
 'TBD'
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
 'TBD'
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
 ""
]
source_id[key]['aliases']= [
 'TBD'
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
 ""
]
source_id[key]['aliases']= [
 'TBD'
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
 'TBD'
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
 'TBD'
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
 'TBD'
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
 'TBD'
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
 'TBD'
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
 'TBD'
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
 'TBD'
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
 ""
]
source_id[key]['aliases']= [
 'TBD'
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
 'TBD'
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





'''
Descriptors were documented in http://pcmdi.github.io/projects/cmip5/CMIP5_output_metadata_requirements.pdf?id=76
Information above can be found in AR5 Table 9.A.1 http://www.climatechange2013.org/images/report/WG1AR5_Chapter09_FINAL.pdf#page=114
'''

#%% Source types
source_type = [
    'AER',
    'AGCM',
    'AOGCM',
    'BGCM',
    'CHEM',
    'ESM',
    'ISM',
    'LAND',
    'OGCM',
    'RAD',
    'SLAB'
]

#%% Sub experiment ids
sub_experiment_id = {}
sub_experiment_id['none'] = 'none'
sub_experiment_id['s1910'] = 'initialized near end of year 1910'
sub_experiment_id['s1950'] = 'initialized near end of year 1950'
for yr in range(1960,2030):
    sub_experiment_id[''.join(['s',str(yr)])] = ' '.join(['initialized near end of year',str(yr)])

#%% Table ids
table_id = [
    '3hr',
    '6hrLev',
    '6hrPlev',
    '6hrPlevPt',
    'AERday',
    'AERhr',
    'AERmon',
    'AERmonZ',
    'Amon',
    'CF3hr',
    'CFday',
    'CFmon',
    'CFsubhr',
    'E1hr',
    'E1hrClimMon',
    'E3hr',
    'E3hrPt',
    'E6hrZ',
    'Eday',
    'EdayZ',
    'Efx',
    'Emon',
    'EmonZ',
    'Esubhr',
    'Eyr',
    'IfxAnt',
    'IfxGre',
    'ImonAnt',
    'ImonGre',
    'IyrAnt',
    'IyrGre',
    'LImon',
    'Lmon',
    'Oclim',
    'Oday',
    'Odec',
    'Ofx',
    'Omon',
    'Oyr',
    'SIday',
    'SImon',
    'day',
    'fx'
]

#%% Define clean functions
def cleanString(string):
    if isinstance(string,str) or isinstance(string,unicode):
    # Take a string and clean it for standard errors
        string = string.strip()  # Remove trailing whitespace
        string = string.strip(',.')  # Remove trailing characters
        string = string.replace(' + ', ' and ')  # Replace +
        string = string.replace(' & ', ' and ')  # Replace +
        string = string.replace('   ', ' ')  # Replace '  ', '   '
        string = string.replace('  ', ' ')  # Replace '  ', '   '
        string = string.replace('None','none')  # Replace None, none
        #string = string.replace('(&C', '(and C') # experiment_id html fix
        #string = string.replace('(& ','(and ') # experiment_id html fix
        #string = string.replace('GHG&ODS','GHG and ODS') # experiment_id html fix
        #string = string.replace('anthro ', 'anthropogenic ')  # Replace anthro
        #string = string.replace('piinatubo', 'pinatubo')  # Replace piinatubo
    else:
        print 'Non-string argument, aborting..'
        print string
        return string

    return string

def dictDepth(x):
    if type(x) is dict and x:
        return 1 + max(dictDepth(x[a]) for a in x)
    if type(x) is list and x:
        return 1 + max(dictDepth(a) for a in x)
    return 0

#You can walk a nested dictionary using recursion
def walk_dict(dictionary):
    for key in dictionary:
        if isinstance(dictionary[key], dict):
           walk_dict(dictionary[key])
        else:
           #do something with dictionary[k]
           pass

#%% Write variables to files
for jsonName in masterTargets:
    # Clean experiment formats
    if jsonName in ['experiment_id','source_id']:
        dictToClean = eval(jsonName)
        for key, value in dictToClean.iteritems():
            for values in value.iteritems():
                # values is a tuple
                # test for dictionary
                if type(values[1]) is list:
                    #print 'elif list'
                    #print values[1],values[0]
                    new = []
                    for count in range(0,len(values[1])):
                        #print key,count
                        #print type(values[1][count])
                        string = values[1][count]
                        string = cleanString(string) ; # Clean string
                        new += [string]
                        #print new
                    dictToClean[key][values[0]] = new
                elif type(values[1]) is dict:
                    #print 'elif dict'
                    # determine dict depth
                    pdepth = dictDepth(values[1])
                    keyInd = values[0]
                    keys1 = values[1].keys()
                    for d1Key in keys1:
                        keys2 = values[1][d1Key].keys()
                        for d2Key in keys2:
                            #print key
                            #print values[0]
                            #print values[1]
                            #print d1Key,d2Key
                            string = dictToClean[key][keyInd][d1Key][d2Key]
                            string = cleanString(string) ; # Clean string
                            dictToClean[key][keyInd][d1Key][d2Key] = string
                elif type(values[0]) in [str,unicode]:
                    #print 'elif str unicode',type(values[0])
                    string = dictToClean[key][values[0]]
                    string = cleanString(string) ; # Clean string
                    dictToClean[key][values[0]] = string
                # Original checks
                #string = dictToClean[key][values[0]]
                #string = cleanString(string) ; # Clean string
                #dictToClean[key][values[0]] = string
        vars()[jsonName] = dictToClean
    # Write file
    if jsonName == 'mip_era':
        outFile = ''.join(['../', jsonName, '.json'])
    else:
        outFile = ''.join(['../CMIP6_', jsonName, '.json'])
    # Get repo version/metadata
    path = os.path.realpath(__file__)
    print 'path',path
    print os.getcwd()
    outFileTest = outFile.replace('../',path.replace('src/writeJson.py',''))
    os.chdir(path.replace('/writeJson.py','')) ; # Reset path to local dir
    print os.getcwd()
    versionInfo = getFileHistory(outFileTest)
    #versionInfo = None ; # Used to add a new file
    if versionInfo == None:
        versionInfo = {}
        versionInfo['author'] = 'Benjamin C. Musci <musci2@llnl.gov>'
        versionInfo['creation_date'] = ''.join([datetime.datetime.now().strftime('%c'),' -0800'])
        versionInfo['institution_id'] = 'PCMDI'
        versionInfo['latest_tag_point'] = 'None'
        versionInfo['note'] = 'None'
        versionInfo['previous_commit'] = 'None'

    # Check file exists
    if os.path.exists(outFile):
        print 'File existing, purging:', outFile
        os.remove(outFile)
    # Create host dictionary
    jsonDict = {}
    jsonDict[jsonName] = eval(jsonName)
    # Append repo version/metadata
    jsonDict['version_metadata'] = versionInfo
    print '***'
    print os.getcwd()
    print outFile
    fH = open(outFile, 'w')
    json.dump(
        jsonDict,
        fH,
        ensure_ascii=True,
        sort_keys=True,
        indent=4,
        separators=(
            ',',
            ':'),
        encoding="utf-8")
    fH.close()

    # Convert to a per file commit
    args = shlex.split(''.join(['git commit -am ',commitMessage]))
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='./')

    # If source_id generate revised html - process both experiment_id and source_id (alpha order)
    if jsonName == 'source_id':
        #json_to_html.py ../CMIP6_experiment_id.json experiment_id CMIP6_experiment_id.html
        args = shlex.split('python ./json_to_html.py')
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='./')

        args = shlex.split(''.join(['git commit -am ',commitMessage]))
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='./')

del(jsonName, jsonDict, outFile)
gc.collect()

# Validate - only necessary if files are not written by json module
