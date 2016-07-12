#!/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 14:12:21 2016

Paul J. Durack 11th July 2016

This script generates all controlled vocabulary (CV) json files residing this this subdirectory

PJD 11 Jul 2016     - Started
PJD 12 Jul 2016     - Read experiments from https://github.com/PCMDI/cmip6-cmor-tables/blob/CMIP6_CV/Tables/CMIP6_CV.json
PJD 12 Jul 2016     - Format tweaks and typo corrections

@author: durack1
"""

#%% Import statements
import json,os,ssl,urllib2

#%% List target controlled vocabularies (CVs)
masterTargets = [
 'activity_id',
 'experiment',
 'frequency',
 'grid_label',
 'grid_resolution',
 'institution',
 'mip_era',
 'realm',
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

#%% Experiments
expSource   = 'https://raw.githubusercontent.com/PCMDI/cmip6-cmor-tables/CMIP6_CV/Tables/CMIP6_CV.json'
outFile     = 'CMIP6_CV.json'
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
jsonOutput  = urllib2.urlopen(expSource, context=ctx)
# Check file exists
if os.path.exists(outFile):
    print 'File existing, purging:',outFile
    os.remove(outFile)
f = open(outFile,'w')
f.write(jsonOutput.read())
f.close()
jsonOutput.close()
# Open and read data
exps        = json.load(open(outFile,'r'))
os.remove(outFile)
experiment  = exps['CV']['experiment_ids'] ;
# Fix issues
experiment['1pctCO2Ndep']['experiment']             = '1 percent per year increasing CO2 experiment with increasing N-deposition'
experiment['amip-piForcing']['experiment']          = 'AMIP SSTs with pre-industrial anthropogenic and natural forcing'
experiment['dcppC-amv-extrop-minus']['experiment']  = 'idealized negative extratropical AMV anomaly pattern'
experiment['esm-piControl-spinup']['experiment']    = 'pre-industrial control simulation with CO2 concentration calculated (spin-up)'
experiment['hist-all-spAerO3']['experiment']        = 'historical simulations with specified anthropogenic aerosols'
experiment['hist-spAerO3']['experiment']            = 'historical simulations with specified anthropogenic aerosols, no other forcings'
experiment['histSST-1950HC']['experiment']          = 'historical SSTs and historical forcing, but with 1950 halocarbon concentrations'
experiment['omip1'] = experiment.pop('omipv1')
experiment['omip1-spunup'] = experiment.pop('omipv1-spunup')
experiment['omip2'] = experiment.pop('omipv2')
experiment['omip2-spunup'] = experiment.pop('omipv2-spunup')
experiment['piClim-NTCF']['experiment']             = 'pre-industrial climatological SSTs and forcing, but with 2014 NTCF emissions'
experiment['piSST']['experiment']                   = 'experiment forced with pre-industrial SSTs, sea ice and atmospheric constituents'
experiment['piSST-4xCO2-solar']['experiment']       = 'preindustrial control SSTs with quadrupled CO2 and solar reduction'
experiment['rad-irf']['experiment']                 = 'offline assessment of radiative transfer parameterizations in clear skies'

#%% Frequencies
frequency = ['3hr', '6hr', 'day', 'decadal', 'fx', 'mon', 'monClim', 'subhr', 'yr'] ;

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
institution = {
 'BCC': 'Beijing Climate Center, China Meteorological Administration, China',
 'BNU': 'GCESS, BNU, Beijing, China',
 'CCCma': 'Canadian Centre for Climate Modelling and Analysis, Victoria, BC, Canada',
 'CMCC': 'Centro Euro-Mediterraneo per i Cambiamenti Climatici, Bologna, Italy',
 'CNRM-CERFACS': 'Centre National de Recherches Meteorologiques, Meteo-France, Toulouse, France) and CERFACS (Centre Europeen de Recherches et de Formation Avancee en Calcul Scientifique, Toulouse, France',
 'COLA-CFS': 'Center for Ocean-Land-Atmosphere Studies, Calverton, MD, USA',
 'CSIRO-BOM': 'Commonwealth Scientific and Industrial Research Organisation, Australia, and Bureau of Meteorology, Melbourne, Australia',
 'CSIRO-QCCCE': 'Australian Commonwealth Scientific and Industrial Research Organization (CSIRO) Marine and Atmospheric Research (Melbourne, Australia) in collaboration with the Queensland Climate Change Centre of Excellence (QCCCE) (Brisbane, Australia)',
 'FIO': 'The First Institution of Oceanography (SOA), Qingdao, China',
 'ICHEC': 'European Earth System Model',
 'INM': 'Institute for Numerical Mathematics, Moscow, Russia',
 'IPSL': 'Institut Pierre Simon Laplace, Paris, France',
 'LASG-CESS': 'Institute of Atmospheric Physics, Chinese Academy of Sciences, Beijing, China and Tsinghua University',
 'LASG-IAP': 'Institute of Atmospheric Physics, Chinese Academy of Sciences, Beijing, China',
 'MIROC': 'JAMSTEC (Japan Agency for Marine-Earth Science and Technology, Kanagawa, Japan), AORI (Atmosphere and Ocean Research Institute, The University of Tokyo, Chiba, Japan), and NIES (National Institute for Environmental Studies, Ibaraki, Japan)',
 'MOHC': 'Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK',
 'MPI-M': 'Max Planck Institute for Meteorology, Germany',
 'MRI': 'Meteorological Research Institute, Tsukuba, Japan',
 'NASA-GISS': 'Goddard Institute for Space Studies, New York, NY, USA',
 'NASA-GMAO': 'Global Modeling and Assimilation Office, NASA Goddard Space Flight Center, Greenbelt, MD, USA',
 'NCAR': 'National Center for Atmospheric Research, Boulder, CO, USA',
 'NCC': 'Norwegian Climate Centre, Bergen, Norway',
 'NICAM': 'Nonhydrostatic Icosahedral Atmospheric Model (NICAM) Group (RIGC-JAMSTEC/AORI-U.Tokyo/AICS-RIKEN, Japan)',
 'NIMR-KMA': 'National Institute of Meteorological Research, Seoul, South Korea',
 'NOAA-GFDL': 'NOAA GFDL, 201 Forrestal Rd, Princeton, NJ, USA',
 'NOAA-NCEP': 'National Centers for Environmental Prediction, Camp Springs, MD, USA',
 'NSF-DOE-NCAR': 'NSF/DOE NCAR (National Center for Atmospheric Research) Boulder, CO, USA',
 'NSF-DOE-PNNL-NCAR': 'PNNL (Pacific Northwest National Laboratory) Richland, WA, USA/NCAR (National Center for Atmospheric Research) Boulder, CO, USA',
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
    # Clean formats
    for key, value in experiment.iteritems():
        for values in value.iteritems():
            string = experiment[key][values[0]]
            string = string.strip() ; # Remove whitespace
            string = string.strip(',.') ; # Remove trailing characters
            experiment[key][values[0]] = string.replace(' + ',' and ')  ; # Replace +
    # Write file
    outFile = ''.join(['../CMIP6_',jsonName,'.json'])
    # Check file exists
    if os.path.exists(outFile):
        print 'File existing, purging:',outFile
        os.remove(outFile)
    fH = open(outFile,'w')
    json.dump(eval(jsonName),fH,ensure_ascii=True,sort_keys=True,indent=4,separators=(',',':'),encoding="utf-8")
    fH.close()

     # Validate - only necessary if files are not written by json module
