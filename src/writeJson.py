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
PJD  1 Sep 2016    - Updated version info to per file (was repo) https://github.com/WCRP-CMIP/CMIP6_CVs/issues/28
PJD  1 Sep 2016    - Automated update of html
PJD 15 Sep 2016    - Further tweaks to version info https://github.com/WCRP-CMIP/CMIP6_CVs/issues/28
PJD 15 Sep 2016    - Updated source_id to maintain consistency with ES-DOCs https://github.com/WCRP-CMIP/CMIP6_CVs/issues/53
PJD 28 Sep 2016    - Correct activity_id to MIP -> CMIP typo https://github.com/WCRP-CMIP/CMIP6_CVs/issues/57
PJD 28 Sep 2016    - Add new grid_label entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/49
PJD  3 Oct 2016    - Added "cohort" to source_id ACCESS-1-0 example https://github.com/WCRP-CMIP/CMIP6_CVs/issues/64
PJD  3 Oct 2016    - Added institution_id NUIST https://github.com/WCRP-CMIP/CMIP6_CVs/issues/63
PJD  4 Oct 2016    - Added institution_id NIMS-KMA https://github.com/WCRP-CMIP/CMIP6_CVs/issues/67
PJD  4 Oct 2016    - Revised tiers for AerChemMIP experiments https://github.com/WCRP-CMIP/CMIP6_CVs/issues/69
PJD  4 Oct 2016    - Added AerChemMIP experiments piClim-SO2 piClim-OC piClim-NH3 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/68
PJD  1 Nov 2016    - Update to upstream sources; Convert to per-file commits
PJD  1 Nov 2016    - Add PCMDI-test-1-0 to source_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/102
PJD  2 Nov 2016    - Add CSIR to institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/100
PJD  2 Nov 2016    - Update BNU institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/98
PJD  2 Nov 2016    - Add EC-Earth-Consortium to institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/90
PJD  2 Nov 2016    - Update MIROC institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/89
PJD  2 Nov 2016    - Add CCCR-IITM to institution_id and IITM-ESM to source_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/96
                   - TODO: Redirect sources to CMIP6_CVs master files (not cmip6-cmor-tables) ; coordinate, formula_terms, grids
                   - TODO: Redirect source_id to CMIP6_CVs master file
                   - TODO: Generate function for json compositing

@author: durack1
"""

#%% Import statements
import gc
import json
import os
import shlex
import ssl
import subprocess
import urllib2
from durolib import readJsonCreateDict
from durolib import getGitInfo
#import pdb

#%% Set commit message
commitMessage = '\"Add institution_id CCCR-IITM\"'

#%% Define functions
# Get repo metadata
def getFileHistory(filePath):
    # Call getGitInfo
    versionInfo = getGitInfo(filePath)
    version_metadata = {}
    version_metadata['author'] = versionInfo[4].replace('author: ','')
    version_metadata['creation_date'] = versionInfo[3].replace('date: ','')
    version_metadata['institution_id'] = 'PCMDI'
    version_metadata['latest_tag_point'] = versionInfo[2].replace('latest_tagPoint: ','')
    version_metadata['note'] = versionInfo[1].replace('note: ','')
    version_metadata['previous_commit'] = versionInfo[0].replace('commit: ','')

    return version_metadata

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
    'CMIP',
    'DAMIP',
    'DCPP',
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
#experiment_id['piClim-SO2'] = {}
#experiment_id['piClim-SO2']['activity_id'] = 'AerChemMIP'
#experiment_id['piClim-SO2']['additional_allowed_model_components'] = ['AGCM','CHEM']
#experiment_id['piClim-SO2']['description'] = 'Perturbation from 1850 control using 2014 SO2 emissions'
#experiment_id['piClim-SO2']['end_year'] = ''
#experiment_id['piClim-SO2']['experiment'] = 'pre-industrial climatological SSTs and forcing, but with 2014 SO2 emissions'
#experiment_id['piClim-SO2']['min_number_yrs_per_sim'] = '30'
#experiment_id['piClim-SO2']['parent_activity_id'] = ''
#experiment_id['piClim-SO2']['parent_experiment_id'] = ''
#experiment_id['piClim-SO2']['required_model_components'] = ['AGCM','AER']
#experiment_id['piClim-SO2']['start_year'] = ''
#experiment_id['piClim-SO2']['sub_experiment'] = 'none'
#experiment_id['piClim-SO2']['sub_experiment_id'] = 'none'
#experiment_id['piClim-SO2']['tier'] = '3'
#
#experiment_id['piClim-OC'] = {}
#experiment_id['piClim-OC']['activity_id'] = 'AerChemMIP'
#experiment_id['piClim-OC']['additional_allowed_model_components'] = ['AGCM','CHEM']
#experiment_id['piClim-OC']['description'] = 'Perturbation from 1850 control using 2014 OC emissions'
#experiment_id['piClim-OC']['end_year'] = ''
#experiment_id['piClim-OC']['experiment'] = 'pre-industrial climatological SSTs and forcing, but with 2014 organic carbon emissions'
#experiment_id['piClim-OC']['min_number_yrs_per_sim'] = '30'
#experiment_id['piClim-OC']['parent_activity_id'] = ''
#experiment_id['piClim-OC']['parent_experiment_id'] = ''
#experiment_id['piClim-OC']['required_model_components'] = ['AGCM','AER']
#experiment_id['piClim-OC']['start_year'] = ''
#experiment_id['piClim-OC']['sub_experiment'] = 'none'
#experiment_id['piClim-OC']['sub_experiment_id'] = 'none'
#experiment_id['piClim-OC']['tier'] = '3'
#
#experiment_id['piClim-NH3'] = {}
#experiment_id['piClim-NH3']['activity_id'] = 'AerChemMIP'
#experiment_id['piClim-NH3']['additional_allowed_model_components'] = ['AGCM','CHEM']
#experiment_id['piClim-NH3']['description'] = 'Perturbation from 1850 control using 2014 NH3 emissions'
#experiment_id['piClim-NH3']['end_year'] = ''
#experiment_id['piClim-NH3']['experiment'] = 'pre-industrial climatological SSTs and forcing, but with 2014 ammonia emissions'
#experiment_id['piClim-NH3']['min_number_yrs_per_sim'] = '30'
#experiment_id['piClim-NH3']['parent_activity_id'] = ''
#experiment_id['piClim-NH3']['parent_experiment_id'] = ''
#experiment_id['piClim-NH3']['required_model_components'] = ['AGCM','AER']
#experiment_id['piClim-NH3']['start_year'] = ''
#experiment_id['piClim-NH3']['sub_experiment'] = 'none'
#experiment_id['piClim-NH3']['sub_experiment_id'] = 'none'
#experiment_id['piClim-NH3']['tier'] = '3'

#experiment_id['piClim-CH4']['tier'] = '1'
#experiment_id['piClim-HC']['tier'] = '1'
#experiment_id['ssp370SST-lowAer']['tier'] = '2'
#experiment_id['ssp370SST-lowBC']['tier'] = '2'
#experiment_id['ssp370SST-lowO3']['tier'] = '2'

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
    'gm',
    'gn',
    'gnz',
    'gr',
    'gr1',
    'gr1z',
    'gr2',
    'gr2z',
    'gr3',
    'gr3z',
    'gr4',
    'gr4z',
    'gr5',
    'gr5z',
    'gr6',
    'gr6z',
    'gr7',
    'gr7z',
    'gr8',
    'gr8z',
    'gr9',
    'gr9z',
    'grz'
]

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
    'BNU': 'Beijing Normal University, Beijing 100875, China',
    'CCCR-IITM': 'Centre for Climate Change Research, Indian Institute of Tropical Meteorology Pune, Maharashtra 411 008, India',
    'CCCma': 'Canadian Centre for Climate Modelling and Analysis, Victoria, BC V8P 5C2, Canada',
    'CMCC': 'Centro Euro-Mediterraneo per i Cambiamenti Climatici, Bologna 40127, Italy',
    'COLA-CFS': 'Center for Ocean-Land-Atmosphere Studies, Fairfax, VA 22030, USA',
    'CSIR-CSIRO': 'CSIR (Council for Scientific and Industrial Research - Natural Resources and the Environment, Pretoria, 0001, South Africa), CSIRO (Commonwealth Scientific and Industrial Research Organisation and Bureau of Meteorology, Melbourne, Victoria 3208, Australia)',
    'CSIRO-BOM': 'Commonwealth Scientific and Industrial Research Organisation and Bureau of Meteorology, Melbourne, Victoria 3208, Australia',
    'EC-Earth-Consortium': 'KNMI, The Netherlands; SMHI, Sweden; DMI, Denmark; AEMET, Spain; Met Éireann, Ireland; CNR-ISAC, Italy; Instituto de Meteorologia, Portugal; FMI, Finland; BSC, Spain; Centro de Geofisica, University of Lisbon, Portugal; ENEA, Italy; Geomar, Germany; Geophysical Institute, University of Bergen, Norway; ICHEC, Ireland; ICTP, Italy; IMAU, The Netherlands; IRV, Sweden;  Lund University, Sweden; Meteorologiska Institutionen, Stockholms University, Sweden; Niels Bohr Institute, University of Copenhagen, Denmark; NTNU, Norway; SARA, The Netherlands; Unité ASTR, Belgium; Universiteit Utrecht, The Netherlands; Universiteit Wageningen, The Netherlands; University College Dublin, Ireland; Vrije Universiteit Amsterdam, the Netherlands; University of Helsinki, Finland; KIT, Karlsruhe, Germany; USC, University of Santiago de Compostela, Spain; Uppsala Universitet, Sweden; NLeSC, Netherlands eScience Center, The Netherlands',
    'FIO': 'The First Institution of Oceanography (SOA), Qingdao, China',
    'INM': 'Institute for Numerical Mathematics, Moscow 119991, Russia',
    'IPSL': 'Institut Pierre Simon Laplace, Paris 75252, France',
    'LASG-IAP': 'Institute of Atmospheric Physics, Chinese Academy of Sciences, Beijing 100029, China',
    'MIROC': 'JAMSTEC (Japan Agency for Marine-Earth Science and Technology, Kanagawa 236-0001, Japan), AORI (Atmosphere and Ocean Research Institute, The University of Tokyo, Chiba 277-8564, Japan), NIES (National Institute for Environmental Studies, Ibaraki 305-8506, Japan), and AICS (RIKEN Advanced Institute for Computational Science, Hyogo 650-0047, Japan)',
    'MOHC': 'Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK',
    'MPI-M': 'Max Planck Institute for Meteorology, Hamburg 20146, Germany',
    'MRI': 'Meteorological Research Institute, Tsukuba, Ibaraki 305-0052, Japan',
    'NASA-GISS': 'Goddard Institute for Space Studies, New York, NY 10025, USA',
    'NCAR': 'National Center for Atmospheric Research, Boulder, CO 80307, USA',
    'NCC': 'UNI Bjerknes Centre for Climate Research, Norwegian Climate Centre, Bergen 5007, Norway',
    'NIMS-KMA': 'National Institute of Meteorological Sciences/Korea Meteorological Administration, Climate Research Division, Seoho-bukro 33, Seogwipo-si, Jejudo 63568, Republic of Korea',
    'NOAA-GFDL': 'National Oceanic and Atmospheric Administration, Geophysical Fluid Dynamics Laboratory, Princeton, NJ 08540, USA',
    'NOAA-NCEP': 'National Oceanic and Atmospheric Administration, National Centers for Environmental Prediction, Camp Springs, MD 20746, USA',
    'NUIST': 'Nanjing University of Information Science & Technology, Nanjing, 210044, China',
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
tmp = [['source_id','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_source_id.json']
      ] ;
source_id = readJsonCreateDict(tmp)
source_id = source_id.get('source_id')
source_id = source_id.get('source_id') ; # Fudge to extract duplicate level

# Fix issues
source_id['IITM-ESM'] = {}
source_id['IITM-ESM']['aerosol'] = 'unnamed (prescribed MAC-v2)'
source_id['IITM-ESM']['atmosphere'] = 'GFS (192 x 94 T62; 64 levels; top level 0.2 mb)'
source_id['IITM-ESM']['atmospheric_chemistry'] = ''
source_id['IITM-ESM']['cohort'] = ['CMIP6']
source_id['IITM-ESM']['institution_id'] = ['CCCR-IITM']
source_id['IITM-ESM']['label'] = 'IITM-ESM'
source_id['IITM-ESM']['label_extended'] = 'IITM-ESM'
source_id['IITM-ESM']['land_ice'] = 'Noah LSM'
source_id['IITM-ESM']['land_surface'] = 'Earth1.0'
source_id['IITM-ESM']['ocean'] = 'MOM4p1 (tripolar, 360x200; 50 levels; top grid cell 5m)'
source_id['IITM-ESM']['ocean_biogeochemistry'] = 'TOPAZ'
source_id['IITM-ESM']['release_year'] = '2015'
source_id['IITM-ESM']['sea_ice'] = 'SIS'
source_id['IITM-ESM']['source_id'] = 'IITM-ESM'

#==============================================================================
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
    # Get repo version/metadata
    path = os.path.realpath(__file__)
    outFileTest = outFile.replace('../',path.replace('src/writeJson.py',''))
    versionInfo = getFileHistory(outFileTest)
    # Test for update

    # Check file exists
    if os.path.exists(outFile):
        print 'File existing, purging:', outFile
        os.remove(outFile)
    # Create host dictionary
    jsonDict = {}
    jsonDict[jsonName] = eval(jsonName)
    # Append repo version/metadata
    jsonDict['version_metadata'] = versionInfo
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

    # If experiment_id generate revised html
    if jsonName == 'experiment_id':
        #json_to_html.py ../CMIP6_experiment_id.json experiment_id CMIP6_experiment_id.html
        args = shlex.split('python ./json_to_html.py ../CMIP6_experiment_id.json experiment_id CMIP6_experiment_id.html')
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='./')

del(jsonName, jsonDict, outFile)
gc.collect()

# Validate - only necessary if files are not written by json module
