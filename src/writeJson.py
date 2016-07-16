#!/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 14:12:21 2016

Paul J. Durack 11th July 2016

This script generates all controlled vocabulary (CV) json files residing this this subdirectory

PJD 11 Jul 2016     - Started
PJD 12 Jul 2016     - Read experiments from https://github.com/PCMDI/cmip6-cmor-tables/blob/CMIP6_CV/Tables/CMIP6_CV.json
PJD 12 Jul 2016     - Format tweaks and typo corrections
PJD 12 Jul 2016     - Added source_id ('GFDL-CM2-1': 'GFDL CM2.1' as example)
PJD 12 Jul 2016     - Corrected mip_era to be CMIP6-less
PJD 12 Jul 2016     - Indent/format cleanup
PJD 13 Jul 2016     - Further tweaks to cleanup experiment json
PJD 13 Jul 2016     - Added required_global_attributes (Denis Nadeau)
PJD 13 Jul 2016     - Further tweaks to resolve specifics https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1
PJD 13 Jul 2016     - Updating institution following https://github.com/WCRP-CMIP/CMIP6_CVs/issues/3
PJD 13 Jul 2016     - Further tweaks to institution
PJD 14 Jul 2016     - Updated source_id to include institution https://github.com/WCRP-CMIP/CMIP6_CVs/issues/8
PJD 14 Jul 2016     - Renamed experiment to experiment_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/10
PJD 14 Jul 2016     - Renamed institution to institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/12
PJD 14 Jul 2016     - Added coordinate https://github.com/WCRP-CMIP/CMIP6_CVs/issues/7
PJD 14 Jul 2016     - Added grid https://github.com/WCRP-CMIP/CMIP6_CVs/issues/6
PJD 14 Jul 2016     - Added formula_terms https://github.com/WCRP-CMIP/CMIP6_CVs/issues/5
PJD 15 Jul 2016     - Added further cleanup of imported dictionaries

@author: durack1
"""

#%% Import statements
import gc,json,os,ssl,urllib2 # re,sys
import pyexcel_xlsx as pyx
from string import replace
from unidecode import unidecode

#%% urllib2 config
# Create urllib2 context to deal with lab certs
ctx                 = ssl.create_default_context()
ctx.check_hostname  = False
ctx.verify_mode     = ssl.CERT_NONE

#%% List target controlled vocabularies (CVs)
masterTargets = [
 'activity_id',
 'coordinate',
 'experiment_id',
 'formula_terms',
 'frequency',
 'grid',
 'grid_label',
 'grid_resolution',
 'institution_id',
 'mip_era',
 'realm',
 'required_global_attributes',
 'source_id',
 'source_type',
 'table_id'
 ] ;

#%% Activities
activity_id = [
 'AerChemMIP',
 'C4MIP',
 'CFMIP',
 'DAMIP',
 'DCPP',
 'FAFMIP',
 'GMMIP',
 'GeoMIP',
 'HighResMIP',
 'ISMIP6',
 'LS3MIP',
 'LUMIP',
 'MIP',
 'OMIP',
 'PMIP',
 'RFMIP',
 'ScenarioMIP',
 'VolMIP'
 ] ;

#%% Coordinate
# Read web file
sourceFile = 'https://raw.githubusercontent.com/PCMDI/cmip6-cmor-tables/master/Tables/CMIP6_Amon.json'
jsonOutput = urllib2.urlopen(sourceFile, context=ctx)
tmp = jsonOutput.read()
jsonOutput.close()
# Write local json
if os.path.exists('tmp.json'):
    os.remove('tmp.json')
tmpFile = open('tmp.json','w')
tmpFile.write(tmp)
tmpFile.close()
# Read local json
tmp = json.load(open('tmp.json','r'))
os.remove('tmp.json')
del(jsonOutput) ; gc.collect()
# Extract coordinates
coordinate = tmp.get('axis_entry')
del(tmp,sourceFile) ; gc.collect()

#%% Experiments
homePath        = os.path.join('/','/'.join(os.path.realpath(__file__).split('/')[0:-1]))
inFile          = os.path.join(homePath,'160713_CMIP6_expt_list.xlsx')
data            = pyx.get_data(inFile)
data            = data['Sheet1']
headers         = data[11]
masterList      = ['description','original label','mip','# of sub-expts.','min ens. size',
                   'start year','end year','min. # yrs/sim','tier','experiment_id','seg-1',
                   'seg-2','seg-3','sub_ experiment_ id','required model components',
                   'additional allowed model components','experiment label used in final version of GMD article',
                   'experiment title','sub_experiment (title)','parent_ experiment_id',
                   'parent_sub_ experiment_id','parent_activity_id','Questions/Comments/Notes',
                   'number of char.']
exclusionList   = ['original label','# of sub-expts.','min ens. size','seg-1','seg-2','seg-3',
                   'experiment label used in final version of GMD article','Questions/Comments/Notes',
                   'number of char.']
exclusionIndex  = [1,3,4,10,11,12,16,20,22,23]
convertToList   = [2,14,15,19,21] ; # activity_id,required_model_components,additional_allowed_model_components,parent_experiment_id,parent_activity_id
# Update headers
headers[2]      = 'activity_id'
headers[7]      = 'min number yrs per sim'
headers[17]     = 'experiment'
headers[18]     = 'sub_experiment'
experiment_id   = {}
for count in range(12,len(data)):
    row = data[count]
    if row[9] == None:
        continue
    key = replace(row[9],'_ ','_')
    experiment_id[key] = {}
    for count2,entry in enumerate(headers):
        if count2 in exclusionIndex:
            continue
        entry = replace(entry,'_ ','_')
        entry = replace(entry,' ','_')
        if count2 >= len(row):
            experiment_id[key][entry] = ''
            continue
        value = row[count2]
        if count2 == 9:
            continue
        else:
            if type(value) == int:
                experiment_id[key][entry] = str(value) ; #replace(str(value),' ','')
            elif value == None:
                experiment_id[key][entry] = ''
            else:
                if count2 in convertToList: # Case convertToList
                    tmp = ''.join(unidecode(value)).split()
                    if count2 == 19 and tmp == ['dcppA-assim']:
                        experiment_id[key][entry] = ['dcppA-assim','']
                    elif isinstance(tmp,list):
                        experiment_id[key][entry] = tmp
                    else:
                        experiment_id[key][entry] = list(tmp)
                else:
                    experiment_id[key][entry] = unidecode(value) ; #replace(unidecode(value),' ','')

del(homePath,inFile,data,headers,masterList,exclusionList,exclusionIndex,convertToList,
    count,row,key,count2,entry,value,tmp) ; gc.collect()

# Fix issues
#==============================================================================
# experiment['histSST-1950HC']['experiment']          = 'historical SSTs and historical forcing, but with 1950 halocarbon concentrations'
# experiment['omip1']                                 = experiment.pop('omipv1')
#==============================================================================

#%% Formula_terms
# Read web file
sourceFile = 'https://raw.githubusercontent.com/PCMDI/cmip6-cmor-tables/master/Tables/CMIP6_Amon.json'
jsonOutput = urllib2.urlopen(sourceFile, context=ctx)
tmp = jsonOutput.read()
jsonOutput.close()
# Write local json
if os.path.exists('tmp.json'):
    os.remove('tmp.json')
tmpFile = open('tmp.json','w')
tmpFile.write(tmp)
tmpFile.close()
# Read local json
tmp = json.load(open('tmp.json','r'))
os.remove('tmp.json')
del(jsonOutput) ; gc.collect()
# Extract coordinates
tmp = tmp.get('variable_entry')
formula_terms = {}
for count,key in enumerate(['a','ps']):
    formula_terms[key] = tmp[key]
del(sourceFile,tmp,count,key) ; gc.collect()

#%% Frequencies
frequency = ['3hr', '3hrClim', '6hr', 'day', 'decadal', 'fx', 'mon', 'monClim', 'subhr', 'yr'] ;

#%% Grid
# Read web file
sourceFile = 'https://raw.githubusercontent.com/PCMDI/cmip6-cmor-tables/master/Tables/CMIP6_grids.json'
jsonOutput = urllib2.urlopen(sourceFile, context=ctx)
tmp = jsonOutput.read()
jsonOutput.close()
# Write local json
if os.path.exists('tmp.json'):
    os.remove('tmp.json')
tmpFile = open('tmp.json','w')
tmpFile.write(tmp)
tmpFile.close()
# Read local json
tmp = json.load(open('tmp.json','r'))
os.remove('tmp.json')
del(jsonOutput) ; gc.collect()
# Extract coordinates
grid = tmp.get('axis_entry')
del(tmp,sourceFile) ; gc.collect()

#%% Grid labels
grid_label = ['gn', 'gr', 'gr1', 'gr2', 'gr3', 'gr4', 'gr5', 'gr6', 'gr7', 'gr8', 'gr9'] ;

#%% Grid resolutions
grid_resolution = [
 '10 km',
 '100 km',
 '1000 km',
 '10000 km',
 '1x1 degree',
 '25 km',
 '250 km',
 '2500 km',
 '5 km',
 '50 km',
 '500 km',
 '5000 km'
 ] ;

#%% Institutions
institution_id = {
 'BNU': 'GCESS, BNU, Beijing, China',
 'CCCma': 'Canadian Centre for Climate Modelling and Analysis, Victoria, BC V8P 5C2, Canada',
 'CMCC': 'Centro Euro-Mediterraneo per i Cambiamenti Climatici, Bologna 40127, Italy',
 'COLA-CFS':'Center for Ocean-Land-Atmosphere Studies, Fairfax, VA 22030, USA',
 'CSIRO-BOM': 'Commonwealth Scientific and Industrial Research Organisation and Bureau of Meteorology, Melbourne, Victoria 3208, Australia',
 'FIO': 'The First Institution of Oceanography (SOA), Qingdao, China',
 'INM': 'Institute for Numerical Mathematics, Moscow 119991, Russia',
 'IPSL': 'Institut Pierre Simon Laplace, Paris 75252, France',
 'LASG-IAP':'Institute of Atmospheric Physics, Chinese Academy of Sciences, Beijing 100029, China',
 'MIROC': 'JAMSTEC (Japan Agency for Marine-Earth Science and Technology, Kanagawa, Japan), AORI (Atmosphere and Ocean Research Institute, The University of Tokyo, Chiba, Japan), and NIES (National Institute for Environmental Studies, Ibaraki, Japan)',
 'MOHC': 'Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK',
 'MPI-M': 'Max Planck Institute for Meteorology, Hamburg 20146, Germany',
 'MRI': 'Meteorological Research Institute, Tsukuba, Ibaraki 305-0052, Japan',
 'NASA-GISS': 'Goddard Institute for Space Studies, New York, NY 10025, USA',
 'NCAR': 'National Center for Atmospheric Research, Boulder, CO 80307, USA',
 'NCC': 'UNI Bjerknes Centre for Climate Research, Norwegian Climate Centre, Bergen 5007, Norway',
 'NOAA-GFDL': 'National Oceanic and Atmospheric Administration, Geophysical Fluid Dynamics Laboratory, Princeton, NJ 08540, USA',
 'NOAA-NCEP': 'National Oceanic and Atmospheric Administration, National Centers for Environmental Prediction, Camp Springs, MD 20746, USA',
 'PCMDI': 'Program for Climate Model Diagnosis and Intercomparison, Lawrence Livermore National Laboratory, Livermore, CA 94550, USA'
 } ;

#%% MIP eras
mip_era = ['CMIP1', 'CMIP2', 'CMIP3', 'CMIP5', 'CMIP6'] ;

#%% Realms
realm = [
 'aerosol',
 'atmos',
 'atmosChem',
 'land',
 'landIce',
 'ocean',
 'ocnBgchem',
 'seaIce'
 ] ;

#%% Required global attributes
required_global_attributes = [
 'Conventions',
 'activity_id',
 'branch_method',
 'creation_date',
 'data_specs_version',
 'experiment',
 'experiment_id',
 'forcing_index',
 'frequency',
 'further_info_url',
 'grid',
 'grid_label',
 'grid_resolution',
 'initialization_index',
 'institution',
 'institution_id',
 'license',
 'mip_era',
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
 'variant_label',
 'variant_label'
 ] ;

#%% Source identifiers
source_id = {}
source_id['GFDL-CM2-1'] = {}
source_id['GFDL-CM2-1']['source'] = 'GFDL CM2.1'
source_id['GFDL-CM2-1']['institution_id'] = ['NOAA-GFDL'] ;

#%% Source types
source_type = [
 'AER',
 'AGCM',
 'AOGCM',
 'BGM',
 'CHEM',
 'EMIC',
 'ESD',
 'ESM',
 'ISM',
 'LAND',
 'OGCM',
 'RAD',
 'RCM',
 'SLAB'
 ] ;

#%% Table ids
table_id = [
 '3hr',
 '3hrpt',
 '6hr',
 '6hrpt',
 'Aday',
 'Amon',
 'LImon',
 'Lmon',
 'OImon',
 'Oclim',
 'Oday',
 'Odec',
 'Omon',
 'Oyr',
 'aero',
 'cfOff',
 'cfSites',
 'fx'
 ] ;

#%% Write variables to files
for jsonName in masterTargets:
    # Clean experiment formats
    if jsonName in ['coordinate','experiment_id','grid','formula_terms']:
        dictToClean = eval(jsonName)
        for key, value in dictToClean.iteritems():
            for values in value.iteritems():
                string = dictToClean[key][values[0]]
                if not isinstance(string, list):
                    string = string.strip() ; # Remove trailing whitespace
                    string = string.strip(',.') ; # Remove trailing characters
                    string = string.replace(' + ',' and ')  ; # Replace +
                    string = string.replace(' & ',' and ')  ; # Replace +
                    string = string.replace('   ',' ') ; # Replace '  ', '   '
                    string = string.replace('anthro ','anthropogenic ') ; # Replace anthro
                    string = string.replace('  ',' ') ; # Replace '  ', '   '
                dictToClean[key][values[0]] = string
        vars()[jsonName] = dictToClean
    # Write file
    if jsonName == 'mip_era':
        outFile = ''.join(['../',jsonName,'.json'])
    else:
        outFile = ''.join(['../CMIP6_',jsonName,'.json'])
    # Check file exists
    if os.path.exists(outFile):
        print 'File existing, purging:',outFile
        os.remove(outFile)
    fH = open(outFile,'w')
    json.dump(eval(jsonName),fH,ensure_ascii=True,sort_keys=True,indent=4,separators=(',',':'),encoding="utf-8")
    fH.close()

del(jsonName,outFile) ; gc.collect()

    # Validate - only necessary if files are not written by json module
