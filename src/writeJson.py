#!/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 14:12:21 2016

Paul J. Durack 11th July 2016

This script generates all controlled vocabulary (CV) json files residing this this subdirectory

PJD 11 Jul 2016    - Started
PJD 12 Jul 2016    - Read experiments from https://github.com/PCMDI/cmip6-cmor-tables/blob/CMIP6_CV/Tables/CMIP6_CV.json
PJD 12 Jul 2016    - Format tweaks and typo corrections
PJD 12 Jul 2016    - Added source_id ('GFDL-CM2-1': 'GFDL CM2.1' as example)
PJD 12 Jul 2016    - Corrected mip_era to be CMIP6-less
PJD 12 Jul 2016    - Indent/format cleanup
PJD 13 Jul 2016    - Further tweaks to cleanup experiment json
PJD 13 Jul 2016    - Added required_global_attributes (Denis Nadeau)
PJD 13 Jul 2016    - Further tweaks to resolve specifics https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1
PJD 13 Jul 2016    - Updating institution following https://github.com/WCRP-CMIP/CMIP6_CVs/issues/3
PJD 13 Jul 2016    - Further tweaks to institution
PJD 14 Jul 2016    - Updated source_id to include institution https://github.com/WCRP-CMIP/CMIP6_CVs/issues/8
PJD 14 Jul 2016    - Renamed experiment to experiment_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/10
PJD 14 Jul 2016    - Renamed institution to institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/12
PJD 14 Jul 2016    - Added coordinate https://github.com/WCRP-CMIP/CMIP6_CVs/issues/7
PJD 14 Jul 2016    - Added grid https://github.com/WCRP-CMIP/CMIP6_CVs/issues/6
PJD 14 Jul 2016    - Added formula_terms https://github.com/WCRP-CMIP/CMIP6_CVs/issues/5
PJD 15 Jul 2016    - Added further cleanup of imported dictionaries
PJD 20 Jul 2016    - Updated VolMIP experiment info https://github.com/WCRP-CMIP/CMIP6_CVs/issues/19
PJD 11 Aug 2016    - Added readJsonCreateDict function
PJD 11 Aug 2016    - Converted experiment_id source from github
PJD 11 Aug 2016    - Updated frequency to include 1hrClimMon https://github.com/WCRP-CMIP/CMIP6_CVs/issues/24
PJD 11 Aug 2016    - Updated LUMIP experiment names https://github.com/WCRP-CMIP/CMIP6_CVs/issues/27
PJD 15 Aug 2016    - Update experiment_id to be self-consistent (LUMIP renames complete)
PJD 15 Aug 2016    - Converted readJsonCreateDict to source from durolib
PJD 15 Aug 2016    - Further tweaks to LUMIP experiment_id @dlawrenncar https://github.com/WCRP-CMIP/CMIP6_CVs/issues/27
PJD 25 Aug 2016    - Added license https://github.com/WCRP-CMIP/CMIP6_CVs/issues/35
PJD 25 Aug 2016    - Updated source_id contents and format https://github.com/WCRP-CMIP/CMIP6_CVs/issues/34
PJD 25 Aug 2016    - Add CV name to json structure https://github.com/WCRP-CMIP/CMIP6_CVs/issues/36
PJD 26 Aug 2016    - Add repo version/metadata https://github.com/WCRP-CMIP/CMIP6_CVs/issues/28
PJD 31 Aug 2016    - Added mip_era to source_id
PJD 31 Aug 2016    - Correct repo user info
PJD 31 Aug 2016    - Remove CMIP6_variable.json from repo https://github.com/WCRP-CMIP/CMIP6_CVs/issues/45
                   - TODO: Redirect sources to CMIP6_CVs master files (not cmip6-cmor-tables) ; coordinate, formula_terms, grids
                   - TODO: Redirect source_id to CMIP6_CVs master file
                   - TODO: Generate function for json compositing

@author: durack1
"""

#%% Import statements
import gc
import json
import os
import ssl
import urllib2
from durolib import readJsonCreateDict
from durolib import getGitInfo
#import pdb

#%% Create urllib2 context to deal with lab/LLNL web certificates
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
    'license',
    'mip_era',
    'realm',
    'required_global_attributes',
    'source_id',
    'source_type',
    'table_id'
]

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
]

#%% Coordinate
# Read web file
sourceFile = 'https://raw.githubusercontent.com/PCMDI/cmip6-cmor-tables/master/Tables/CMIP6_Amon.json'
jsonOutput = urllib2.urlopen(sourceFile, context=ctx)
tmp = jsonOutput.read()
jsonOutput.close()
# Write local json
if os.path.exists('tmp.json'):
    os.remove('tmp.json')
tmpFile = open('tmp.json', 'w')
tmpFile.write(tmp)
tmpFile.close()
# Read local json
tmp = json.load(open('tmp.json', 'r'))
os.remove('tmp.json')
del(jsonOutput)
gc.collect()
# Extract coordinates
coordinate = tmp.get('axis_entry')
del(tmp, sourceFile)
gc.collect()

#%% Experiments
tmp = [['experiment_id','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_experiment_id.json']
      ] ;
experiment_id = readJsonCreateDict(tmp)
experiment_id = experiment_id.get('experiment_id')
experiment_id = experiment_id.get('experiment_id') ; # Fudge to extract duplicate level

# Fix issues
#==============================================================================
#experiment_id['land-noShiftCultivate'] = experiment_id.pop('land-noShiftcultivate')

#print experiment_id['deforest-globe']['min_number_yrs_per_sim']
#experiment_id['deforest-globe']['min_number_yrs_per_sim'] = '81'
#print experiment_id['deforest-globe']['start_year']
#experiment_id['deforest-globe']['start_year'] = ''
#print experiment_id['land-cClim']['description']
#experiment_id['land-cClim']['description'] = 'Same as land-hist except with climate held constant'
#print experiment_id['land-crop-noIrrigFert']['description']
#experiment_id['land-crop-noIrrigFert']['description'] = 'Same as land-hist except with plants in cropland area utilizing at least some form of crop management (e.g., planting and harvesting) rather than simulating cropland vegetation as a natural grassland. Irrigated area and fertilizer area/use should be held constant'
#print experiment_id['land-crop-noIrrigFert']['experiment']
#experiment_id['land-crop-noIrrigFert']['experiment'] = 'historical land-only with managed crops but with irrigation and fertilization held constant'
#print experiment_id['land-noShiftcultivate']['description']
#experiment_id['land-noShiftcultivate']['description'] = 'Same as land-hist except shifting cultivation turned off. An additional LUC transitions dataset will be provided as a data layer within LUMIP LUH2 dataset with shifting cultivation deactivated'
#print experiment_id['land-noShiftcultivate']['experiment']
#experiment_id['land-noShiftcultivate']['experiment'] = 'historical land-only with shifting cultivation turned off'

#experiment_id['land-hist-altLu1'] = {}
#experiment_id['land-hist-altLu1']['activity_id'] = 'LUMIP'
#experiment_id['land-hist-altLu1']['additional_allowed_model_components'] = ''
#experiment_id['land-hist-altLu1']['description'] = 'Land only simulations'
#experiment_id['land-hist-altLu1']['end_year'] = '2014'
#experiment_id['land-hist-altLu1']['experiment'] = 'historical land-only alternate land-use history'
#experiment_id['land-hist-altLu1']['min_number_yrs_per_sim'] = '165'
#experiment_id['land-hist-altLu1']['parent_activity_id'] = ''
#experiment_id['land-hist-altLu1']['parent_experiment_id'] = ''
#experiment_id['land-hist-altLu1']['required_model_components'] = ['LND']
#experiment_id['land-hist-altLu1']['start_year'] = '1850 or 1700'
#experiment_id['land-hist-altLu1']['sub_experiment'] = 'none'
#experiment_id['land-hist-altLu1']['sub_experiment_id'] = 'none'
#experiment_id['land-hist-altLu1']['tier'] = '2'
#experiment_id['land-hist-altLu2'] = {}
#experiment_id['land-hist-altLu2']['activity_id'] = 'LUMIP'
#experiment_id['land-hist-altLu2']['additional_allowed_model_components'] = ''
#experiment_id['land-hist-altLu2']['description'] = 'Land only simulations'
#experiment_id['land-hist-altLu2']['end_year'] = '2014'
#experiment_id['land-hist-altLu2']['experiment'] = 'historical land-only alternate land use history'
#experiment_id['land-hist-altLu2']['min_number_yrs_per_sim'] = '165'
#experiment_id['land-hist-altLu2']['parent_activity_id'] = ''
#experiment_id['land-hist-altLu2']['parent_experiment_id'] = ''
#experiment_id['land-hist-altLu2']['required_model_components'] = ['LND']
#experiment_id['land-hist-altLu2']['start_year'] = '1850 or 1700'
#experiment_id['land-hist-altLu2']['sub_experiment'] = 'none'
#experiment_id['land-hist-altLu2']['sub_experiment_id'] = 'none'
#experiment_id['land-hist-altLu2']['tier'] = '2'

#experiment_id['control-slab']['tier'] = '3'
#experiment_id['volc-long-hlS']['description'] = 'Idealized Southern Hemisphere high-latitude eruption emitting 28.1 Tg of SO2. Experiment initialized from PiControl'
#experiment_id['volc-pinatubo-full']['description'] = '1991 Pinatubo forcing as used in the CMIP6 historical simulations. Requires special diagnostics of radiative and latent heating rates. A large number of ensemble members is required to address internal atmospheric variability'
#experiment_id['volc-pinatubo-ini']['start_year'] = '2015'
#experiment_id['volc-pinatubo-strat']['description'] = 'As volc-pinatubo-full, but with prescribed perturbation to the total (LW+SW) radiative heating rates'
#experiment_id['volc-pinatubo-surf']['description'] = 'As volc-pinatubo-full, but with prescribed perturbation to the shortwave flux to mimic the attenuation of solar radiation by volcanic aerosols'
#experiment_id['histSST-1950HC']['experiment'] = 'historical SSTs and historical forcing, but with 1950 halocarbon concentrations'
#experiment_id['omip1'] = experiment.pop('omipv1')
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
tmpFile = open('tmp.json', 'w')
tmpFile.write(tmp)
tmpFile.close()
# Read local json
tmp = json.load(open('tmp.json', 'r'))
os.remove('tmp.json')
del(jsonOutput)
gc.collect()
# Extract coordinates
tmp = tmp.get('variable_entry')
formula_terms = {}
for count, key in enumerate(['a', 'ps']):
    formula_terms[key] = tmp[key]
del(sourceFile, tmp, count, key)
gc.collect()

#%% Frequencies
frequency = [
    '1hrClimMon',
    '3hr',
    '3hrClim',
    '6hr',
    'day',
    'decadal',
    'fx',
    'mon',
    'monClim',
    'subhr',
    'yr']

#%% Grid
# Read web file
sourceFile = 'https://raw.githubusercontent.com/PCMDI/cmip6-cmor-tables/master/Tables/CMIP6_grids.json'
jsonOutput = urllib2.urlopen(sourceFile, context=ctx)
tmp = jsonOutput.read()
jsonOutput.close()
# Write local json
if os.path.exists('tmp.json'):
    os.remove('tmp.json')
tmpFile = open('tmp.json', 'w')
tmpFile.write(tmp)
tmpFile.close()
# Read local json
tmp = json.load(open('tmp.json', 'r'))
os.remove('tmp.json')
del(jsonOutput)
gc.collect()
# Extract coordinates
grid = tmp.get('axis_entry')
del(tmp, sourceFile)
gc.collect()

#%% Grid labels
grid_label = [
    'gn',
    'gr',
    'gr1',
    'gr2',
    'gr3',
    'gr4',
    'gr5',
    'gr6',
    'gr7',
    'gr8',
    'gr9']

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
]

#%% Institutions
institution_id = {
    'BNU': 'GCESS, BNU, Beijing, China',
    'CCCma': 'Canadian Centre for Climate Modelling and Analysis, Victoria, BC V8P 5C2, Canada',
    'CMCC': 'Centro Euro-Mediterraneo per i Cambiamenti Climatici, Bologna 40127, Italy',
    'COLA-CFS': 'Center for Ocean-Land-Atmosphere Studies, Fairfax, VA 22030, USA',
    'CSIRO-BOM': 'Commonwealth Scientific and Industrial Research Organisation and Bureau of Meteorology, Melbourne, Victoria 3208, Australia',
    'FIO': 'The First Institution of Oceanography (SOA), Qingdao, China',
    'INM': 'Institute for Numerical Mathematics, Moscow 119991, Russia',
    'IPSL': 'Institut Pierre Simon Laplace, Paris 75252, France',
    'LASG-IAP': 'Institute of Atmospheric Physics, Chinese Academy of Sciences, Beijing 100029, China',
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
}

#%% CMIP6 License
license = [
    'CMIP6 model data produced by <YourCentreName> is licensed under a Creative Commons Attribution "[*] Share Alike" 4.0 International License (http://creativecommons.org/licenses/by/4.0/). Use of the data should be acknowledged following guidelines found at https://pcmdi.llnl.gov/home/CMIP6/citation.html. [Permissions beyond the scope of this license may be available at <some URL maintained by modeling group>.] Further information about this data, including some limitations, can be found via the further_info_url (recorded as a global attribute in data files)[and at <some URL maintained by modeling group>]. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law.'
]

#%% MIP eras
mip_era = ['CMIP1', 'CMIP2', 'CMIP3', 'CMIP5', 'CMIP6']

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
]

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
]

#%% Source identifiers
source_id = {}
source_id['ACCESS-1-0'] = {}
source_id['ACCESS-1-0']['aerosol'] = 'CLASSIC'
source_id['ACCESS-1-0']['atmosphere'] = 'HadGAM2 (r1.1); 192 x 145 N96; 38 levels; top level 39255m'
source_id['ACCESS-1-0']['atmospheric_chemistry'] = 'None'
source_id['ACCESS-1-0']['glacier'] = 'None'
source_id['ACCESS-1-0']['institution_id'] = ['CSIRO-BOM']
source_id['ACCESS-1-0']['land_surface'] = 'MOSES2.2'
source_id['ACCESS-1-0']['mip_era'] = 'CMIP5'
source_id['ACCESS-1-0']['ocean'] = 'ACCESS-OM (MOM4p1); tripolar primarily 1deg latitude/longitude; 50 levels; top grid cell 0-10m'
source_id['ACCESS-1-0']['ocean_biogeochemistry'] = 'None'
source_id['ACCESS-1-0']['release_year'] = '2011' ; # When this model version was first used in a scientific application
source_id['ACCESS-1-0']['sea_ice'] = 'CICE4.1'
source_id['ACCESS-1-0']['source'] = 'ACCESS 1.0'
'''
Descriptors were documented in http://pcmdi.github.io/projects/cmip5/CMIP5_output_metadata_requirements.pdf?id=76
Information above can be found in AR5 Table 9.A.1 http://www.climatechange2013.org/images/report/WG1AR5_Chapter09_FINAL.pdf#page=114
'''

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
]

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
]

#%% Get repo metadata
path = os.path.realpath(__file__)
print path.replace('/src/writeJson.py','').replace('/export_temp','/export')
versionInfo = getGitInfo(path.replace('/src/writeJson.py','').replace('/export_temp','/export'))
version = {}
version['author'] = versionInfo[4].replace('author: ','')
version['commit'] = versionInfo[0].replace('commit: ','')
version['creation_date'] = versionInfo[3].replace('date: ','')
version['institution_id'] = 'PCMDI'
version['latest_tag_point'] = versionInfo[2].replace('latest_tagPoint: ','')
version['note'] = versionInfo[1].replace('note: ','')
del(versionInfo)

#%% Write variables to files
for jsonName in masterTargets:
    # Clean experiment formats
    if jsonName in ['coordinate', 'experiment_id', 'formula_terms', 'grid']:
        dictToClean = eval(jsonName)
        for key, value in dictToClean.iteritems():
            for values in value.iteritems():
                string = dictToClean[key][values[0]]
                #pdb.set_trace()
                #if key == 'alt16':
                #    print key,values,string,type(string)
                if not isinstance(string, list):
                    string = string.strip()  # Remove trailing whitespace
                    string = string.strip(',.')  # Remove trailing characters
                    string = string.replace(' + ', ' and ')  # Replace +
                    string = string.replace(' & ', ' and ')  # Replace +
                    string = string.replace(
                        'anthro ', 'anthropogenic ')  # Replace anthro
                    string = string.replace(
                        'piinatubo', 'pinatubo')  # Replace piinatubo
                    string = string.replace('   ', ' ')  # Replace '  ', '   '
                    string = string.replace('  ', ' ')  # Replace '  ', '   '
                dictToClean[key][values[0]] = string
        vars()[jsonName] = dictToClean
    # Write file
    if jsonName == 'mip_era':
        outFile = ''.join(['../', jsonName, '.json'])
    else:
        outFile = ''.join(['../CMIP6_', jsonName, '.json'])
    # Check file exists
    if os.path.exists(outFile):
        print 'File existing, purging:', outFile
        os.remove(outFile)
    # Create host dictionary
    jsonDict = {}
    jsonDict[jsonName] = eval(jsonName)
    # Append repo version/metadata
    jsonDict['version'] = version
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

del(jsonName, jsonDict, outFile)
gc.collect()

# Validate - only necessary if files are not written by json module
