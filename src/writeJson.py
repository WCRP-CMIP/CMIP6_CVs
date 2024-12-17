#!/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# import pdb
from CMIP6Lib import (
    ascertainVersion,
    cleanString,
    dictDepth,
    entryCheck,
    getFileHistory,
    versionHistoryUpdate,
)
from durolib import readJsonCreateDict
import calendar
import datetime
import gc
import json
import os
import pdb
import platform
import re
import shlex
import sys
import subprocess
import time


# %% additional import statements
try:
    from urllib2 import urlopen  # py2
except ImportError:
    from urllib.request import urlopen  # py3

"""
Created on Mon Jul 11 14:12:21 2016

Paul J. Durack 11th July 2016

This script generates all controlled vocabulary (CV) json files
residing in this subdirectory
"""
"""2016-2021
https://github.com/WCRP-CMIP/CMIP6_CVs/blob/0048ecd216d31fc52afd0177788eeb0707a2289e/src/writeJson.py#L33-L560
"""
"""2022
https://github.com/WCRP-CMIP/CMIP6_CVs/blob/0fdb15e67d01b941b71b63ddacfaf47a2ad8a9d3/src/writeJson.py#L44-L119
"""
"""2023-2024
PJD 21 Feb 2023    - Revised CanESM5-1 source_id license history https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1148
PJD 21 Feb 2023    - Updated subprocess call with space for -r optional arg; Corrected CanESM5-1 license_info entry to include source_specific_info
PJD 21 Feb 2023    - Revised E3SM-2-0 source_id license history https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1127 corrected missing source_specific_info
PJD 22 Feb 2023    - Updated html sources to latest 1.12.1 -> 1.13.2; 3.6.0 -> 3.6.3
PJD 23 Feb 2023    - Deregistered source_id NorESM2-MH https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1079
PJD 13 Mar 2023    - Update contact for source_id MPI-ESM-1-2-HAM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1188
PJD 21 Mar 2023    - Registered source_id E3SM-2-0-NARRM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1190
PJD 21 Jun 2023    - Deregistered source_id IPSL-CM6A-MR025 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1078
PJD 26 Jul 2023    - Revised E3SM-2-0-NARRM source_id license history https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1190
PJD 25 Aug 2023    - Revised CAS-ESM2-0 source_id to add CDRMIP activity https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1201
PJD 16 Nov 2023    - Revised GISS-E2-1-G-CC and GISS-E2-2-H activity participation https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1207
PJD 16 Nov 2023    - Revised CESM2-FV2 and CESM2-WACCM-FV2 activity participation https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1208
PJD 21 Nov 2023    - Revised CNRM-ESM2-1 activity participation https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1211
PJD 27 Nov 2023    - Revised TaiESM1 activity participation https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1213
PJD 25 Jan 2024    - Registered source_id AWI-ESM-1-REcoM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1215
PJD 25 Jan 2024    - Registered source_id E3SM-2-1 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1218
PJD 28 Mar 2024    - Revised source_id EC-Earth3-GrIS https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1223
PJD 28 Mar 2024    - Registered source_id EC-Earth3-ESM-1 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1222
PJD 28 Mar 2024    - Revised source_id GISS-E2-1-H https://github.com/WCRP-CMIP/CMIP6_CVs/issues/177
PJD 28 Mar 2024    - Revised source_id GISS-E2-2-H https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1018
PJD  1 May 2024    - Revised source_id IPSL-CM6A-MR1 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1078
PJD  3 Jul 2024    - Added CITATION.cff version management
PJD 29 Jul 2024    - Revised source_id AWI-ESM-1-REcoM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1220
PJD  2 Aug 2024    - Deregistered source_id AWI-ESM-2-1-LR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1220#issuecomment-2265990964
PJD  2 Aug 2024    - Revise multiple AWI source_id entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1236
PJD 16 Aug 2024    - Revise CMCC-CM2-SR5 source_id entry https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1239
PJD 16 Aug 2024    - Revise GISS-E2-1-H source_id entry https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1240
PJD 16 Aug 2024    - Revise IPSL-CM6A-LR source_id entry https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1241
PJD 17 Dec 2024    - Revise EC-Earth3-Veg source_id entry https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1246
                     - TODO: Review all start/end_year pairs for experiments https://github.com/WCRP-CMIP/CMIP6_CVs/issues/845
                     - TODO: Generate table_id from dataRequest https://github.com/WCRP-CMIP/CMIP6_CVs/issues/166

@author: durack1
"""

# %% Set commit message and author info
commitMessage = '"Revise EC-Earth3-Veg source_id entry"'
# author = 'Matthew Mizielinski <matthew.mizielinski@metoffice.gov.uk>'
# author_institution_id = 'MOHC'
author = "Paul J. Durack <durack1@llnl.gov>"
author_institution_id = "PCMDI"

# %% List target controlled vocabularies (CVs)
masterTargets = [
    "activity_id",
    "DRS",
    "experiment_id",
    "frequency",
    "grid_label",
    "institution_id",
    "license",
    "mip_era",
    "nominal_resolution",
    "realm",
    "required_global_attributes",
    "source_id",
    "source_type",
    "sub_experiment_id",
    "table_id",
]

# %% Activities
activity_id = {
    "AerChemMIP": "Aerosols and Chemistry Model Intercomparison Project",
    "C4MIP": "Coupled Climate Carbon Cycle Model Intercomparison Project",
    "CDRMIP": "Carbon Dioxide Removal Model Intercomparison Project",
    "CFMIP": "Cloud Feedback Model Intercomparison Project",
    "CMIP": "CMIP DECK: 1pctCO2, abrupt4xCO2, amip, esm-piControl, esm-historical, historical, and piControl experiments",
    "CORDEX": "Coordinated Regional Climate Downscaling Experiment",
    "DAMIP": "Detection and Attribution Model Intercomparison Project",
    "DCPP": "Decadal Climate Prediction Project",
    "DynVarMIP": "Dynamics and Variability Model Intercomparison Project",
    "FAFMIP": "Flux-Anomaly-Forced Model Intercomparison Project",
    "GMMIP": "Global Monsoons Model Intercomparison Project",
    "GeoMIP": "Geoengineering Model Intercomparison Project",
    "HighResMIP": "High-Resolution Model Intercomparison Project",
    "ISMIP6": "Ice Sheet Model Intercomparison Project for CMIP6",
    "LS3MIP": "Land Surface, Snow and Soil Moisture",
    "LUMIP": "Land-Use Model Intercomparison Project",
    "OMIP": "Ocean Model Intercomparison Project",
    "PAMIP": "Polar Amplification Model Intercomparison Project",
    "PMIP": "Palaeoclimate Modelling Intercomparison Project",
    "RFMIP": "Radiative Forcing Model Intercomparison Project",
    "SIMIP": "Sea Ice Model Intercomparison Project",
    "ScenarioMIP": "Scenario Model Intercomparison Project",
    "VIACSAB": "Vulnerability, Impacts, Adaptation and Climate Services Advisory Board",
    "VolMIP": "Volcanic Forcings Model Intercomparison Project",
}

# %% DRS - directory and filename templates
DRS = {}
DRS["directory_path_template"] = (
    "<mip_era>/<activity_id>/<institution_id>/<source_id>/<experiment_id>/<member_id>/<table_id>/<variable_id>/<grid_label>/<version>"
)
DRS["directory_path_example"] = (
    "CMIP6/CMIP/MOHC/HadGEM3-GC31-MM/historical/r1i1p1f3/Amon/tas/gn/v20191207/"
)
DRS["directory_path_sub_experiment_example"] = (
    "CMIP6/DCPP/MOHC/HadGEM3-GC31-MM/dcppA-hindcast/s1960-r1i1p1f2/Amon/tas/gn/v20200417/"
)
DRS["filename_template"] = (
    "<variable_id>_<table_id>_<source_id>_<experiment_id >_<member_id>_<grid_label>[_<time_range>].nc"
)
DRS["filename_example"] = (
    "tas_Amon_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_185001-186912.nc"
)
DRS["filename_sub_experiment_example"] = (
    "tas_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s1960-r1i1p1f2_gn_196011-196012.nc"
)

# %% Experiments
tmp = [
    [
        "experiment_id",
        "https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_experiment_id.json",
    ]
]
experiment_id = readJsonCreateDict(tmp)
experiment_id = experiment_id.get("experiment_id")
# Fudge to extract duplicate level
experiment_id = experiment_id.get("experiment_id")
del tmp

# Fix issues

"""
# xlsx import
# Fields
# Alpha/json order, xlsx column old, xlsx column new, type, value
# 1  0  0  str  experiment_id string
# 2  1  1  list activity_id list
# 3  8  7  list additional_allowed_model_components list
# 4  13 12 str  description string
# 5  10 10 str  end_year string
# 6  2  2  str  experiment string
# 7  11 11 str  min_number_yrs_per_sim string
# 8  12 5  list parent_activity_id list
# 9  6  6  list parent_experiment_id list
# 10 7  8  list required_model_components list
# 11 9  9  str  start_year string
# 12 5  -  -    sub_experiment string
# 13 4  4  list sub_experiment_id string
# 14 3  3  str tier string

os.chdir('/sync/git/CMIP6_CVs/src')
inFiles = ['180421_1927_DavidKeller_CMIP6-CDRMIP-ExpList.xlsx',
           '180421_1927_DougSmith_CMIP6-PAMIP-ExpList.xlsx']
for inFile in inFiles:
    data = pyx.get_data(inFile)
    data = data['Sheet1']
    headers = data[3]
    #experiment_id = {} ; Already defined and loaded
    for count in range(4,len(data)): # Start on 5th row, headers
        if data[count] == []:
            #print count,'blank field'
            continue
        row = data[count]
        key = row[0] ; #replace(row[0],'_ ','_')
        experiment_id[key] = {}
        for count2,entry in enumerate(headers):
            #if count2 == 5:
            #    continue ; # Skip sub_experiment - removed in update
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
                experiment_id[key][entry] = ' '.join(value)
            elif value == None:
                experiment_id[key][entry] = '' ; # changed from none to preserve blank entries
            elif type(value) == float:
                #print 'elif type(value):',value
                value = str(int(value))
                experiment_id[key][entry] = value
            else:
                #print 'else:',value
                value = replace(value,'    ',' ') ; # replace whitespace
                value = replace(value,'   ',' ') ; # replace whitespace
                value = replace(value,'  ',' ') ; # replace whitespace
                experiment_id[key][entry] = unidecode(value) ; #replace(unidecode(value),' ','')
                try:
                    #print 'try:',value
                    unidecode(value)
                except:
                    print count,count2,key,entry,value
            # Now sort by type
            if count2 in [1,4,6,7,8]:
                experiment_id[key][entry] = list(value)
            elif count2 == 5:
                experiment_id[key][entry] = list([value])
    del(inFile,data,headers,count,row,key,entry,value) ; gc.collect()
"""
# ==============================================================================
# Example new experiment_id entry
# key = 'ssp119'
# experiment_id[key] = {}
# experiment_id[key]['activity_id'] = ['ScenarioMIP']
# experiment_id[key]['additional_allowed_model_components'] = ['AER','CHEM','BGC']
# experiment_id[key]['description'] = 'Future scenario with low radiative forcing throughout reaching about 1.9 W/m2 in 2100 based on SSP1. Concentration-driven'
# experiment_id[key]['end_year'] = '2100'
# experiment_id[key]['experiment'] = 'low-end scenario reaching 1.9 W m-2, based on SSP1'
# experiment_id[key]['experiment_id'] = key
# experiment_id[key]['min_number_yrs_per_sim'] = '86'
# experiment_id[key]['parent_activity_id'] = ['CMIP']
# experiment_id[key]['parent_experiment_id'] = ['historical']
# experiment_id[key]['required_model_components'] = ['AOGCM']
# experiment_id[key]['start_year'] = '2015'
# experiment_id[key]['sub_experiment_id'] = ['none']
# experiment_id[key]['tier'] = '2'
# Rename
# experiment_id['land-noShiftCultivate'] = experiment_id.pop('land-noShiftcultivate')
# Remove
# experiment_id.pop('land-noShiftcultivate')

# %% Frequencies
frequency = {
    "1hr": "sampled hourly",
    "1hrCM": "monthly-mean diurnal cycle resolving each day into 1-hour means",
    "1hrPt": "sampled hourly, at specified time point within an hour",
    "3hr": "3 hourly mean samples",
    "3hrPt": "sampled 3 hourly, at specified time point within the time period",
    "6hr": "6 hourly mean samples",
    "6hrPt": "sampled 6 hourly, at specified time point within the time period",
    "day": "daily mean samples",
    "dec": "decadal mean samples",
    "fx": "fixed (time invariant) field",
    "mon": "monthly mean samples",
    "monC": "monthly climatology computed from monthly mean samples",
    "monPt": "sampled monthly, at specified time point within the time period",
    "subhrPt": "sampled sub-hourly, at specified time point within an hour",
    "yr": "annual mean samples",
    "yrPt": "sampled yearly, at specified time point within the time period",
}

# %% Grid labels
grid_label = {
    "gm": "global mean data",
    "gn": "data reported on a model's native grid",
    "gna": "data reported on a native grid in the region of Antarctica",
    "gng": "data reported on a native grid in the region of Greenland",
    "gnz": "zonal mean data reported on a model's native latitude grid",
    "gr": "regridded data reported on the data provider's preferred target grid",
    "gr1": "regridded data reported on a grid other than the native grid and other than the preferred target grid",
    "gr1a": "regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
    "gr1g": "regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
    "gr1z": "regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
    "gr2": "regridded data reported on a grid other than the native grid and other than the preferred target grid",
    "gr2a": "regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
    "gr2g": "regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
    "gr2z": "regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
    "gr3": "regridded data reported on a grid other than the native grid and other than the preferred target grid",
    "gr3a": "regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
    "gr3g": "regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
    "gr3z": "regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
    "gr4": "regridded data reported on a grid other than the native grid and other than the preferred target grid",
    "gr4a": "regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
    "gr4g": "regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
    "gr4z": "regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
    "gr5": "regridded data reported on a grid other than the native grid and other than the preferred target grid",
    "gr5a": "regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
    "gr5g": "regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
    "gr5z": "regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
    "gr6": "regridded data reported on a grid other than the native grid and other than the preferred target grid",
    "gr6a": "regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
    "gr6g": "regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
    "gr6z": "regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
    "gr7": "regridded data reported on a grid other than the native grid and other than the preferred target grid",
    "gr7a": "regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
    "gr7g": "regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
    "gr7z": "regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
    "gr8": "regridded data reported on a grid other than the native grid and other than the preferred target grid",
    "gr8a": "regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
    "gr8g": "regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
    "gr8z": "regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
    "gr9": "regridded data reported on a grid other than the native grid and other than the preferred target grid",
    "gr9a": "regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
    "gr9g": "regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
    "gr9z": "regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
    "gra": "regridded data in the region of Antarctica reported on the data provider's preferred target grid",
    "grg": "regridded data in the region of Greenland reported on the data provider's preferred target grid",
    "grz": "regridded zonal mean data reported on the data provider's preferred latitude target grid",
}

# %% Institutions
institution_id = {
    "AER": "Research and Climate Group, Atmospheric and Environmental Research, 131 Hartwell Avenue, Lexington, MA 02421, USA",
    "AS-RCEC": "Research Center for Environmental Changes, Academia Sinica, Nankang, Taipei 11529, Taiwan",
    "AWI": "Alfred Wegener Institute, Helmholtz Centre for Polar and Marine Research, Am Handelshafen 12, 27570 Bremerhaven, Germany",
    "BCC": "Beijing Climate Center, Beijing 100081, China",
    "CAMS": "Chinese Academy of Meteorological Sciences, Beijing 100081, China",
    "CAS": "Chinese Academy of Sciences, Beijing 100029, China",
    "CCCR-IITM": "Centre for Climate Change Research, Indian Institute of Tropical Meteorology Pune, Maharashtra 411 008, India",
    "CCCma": "Canadian Centre for Climate Modelling and Analysis, Environment and Climate Change Canada, Victoria, BC V8P 5C2, Canada",
    "CMCC": "Fondazione Centro Euro-Mediterraneo sui Cambiamenti Climatici, Lecce 73100, Italy",
    "CNRM-CERFACS": "".join(
        [
            "CNRM (Centre National de Recherches Meteorologiques, Toulouse 31057, France), CERFACS (Centre Europeen de Recherche ",
            "et de Formation Avancee en Calcul Scientifique, Toulouse 31057, France)",
        ]
    ),
    "CSIRO": "Commonwealth Scientific and Industrial Research Organisation, Aspendale, Victoria 3195, Australia",
    "CSIRO-ARCCSS": " ".join(
        [
            "CSIRO (Commonwealth Scientific and Industrial Research Organisation, Aspendale, Victoria 3195, Australia),",
            "ARCCSS (Australian Research Council Centre of Excellence for Climate System Science).",
            "Mailing address: CSIRO, c/o Simon J. Marsland,",
            "107-121 Station Street, Aspendale, Victoria 3195, Australia",
        ]
    ),
    "CSIRO-COSIMA": " ".join(
        [
            "CSIRO (Commonwealth Scientific and Industrial Research Organisation, Australia),",
            "COSIMA (Consortium for Ocean-Sea Ice Modelling in Australia).",
            "Mailing address: CSIRO, c/o Simon J. Marsland,",
            "107-121 Station Street, Aspendale, Victoria 3195, Australia",
        ]
    ),
    "DKRZ": "Deutsches Klimarechenzentrum, Hamburg 20146, Germany",
    "DWD": "Deutscher Wetterdienst, Offenbach am Main 63067, Germany",
    "E3SM-Project": "".join(
        [
            "LLNL (Lawrence Livermore National Laboratory, Livermore, CA 94550, USA); ",
            "ANL (Argonne National Laboratory, Argonne, IL 60439, USA); ",
            "BNL (Brookhaven National Laboratory, Upton, NY 11973, USA); ",
            "LANL (Los Alamos National Laboratory, Los Alamos, NM 87545, USA); ",
            "LBNL (Lawrence Berkeley National Laboratory, Berkeley, CA 94720, USA); ",
            "ORNL (Oak Ridge National Laboratory, Oak Ridge, TN 37831, USA); ",
            "PNNL (Pacific Northwest National Laboratory, Richland, WA 99352, USA); ",
            "SNL (Sandia National Laboratories, Albuquerque, NM 87185, USA). ",
            "Mailing address: LLNL Climate Program, c/o David C. Bader, ",
            "Principal Investigator, L-103, 7000 East Avenue, Livermore, CA 94550, USA",
        ]
    ),
    "EC-Earth-Consortium": "".join(
        [
            "AEMET, Spain; BSC, Spain; CNR-ISAC, Italy; DMI, Denmark; ENEA, Italy; FMI, Finland; Geomar, Germany; ICHEC, ",
            "Ireland; ICTP, Italy; IDL, Portugal; IMAU, The Netherlands; IPMA, Portugal; KIT, Karlsruhe, Germany; KNMI, ",
            "The Netherlands; Lund University, Sweden; Met Eireann, Ireland; NLeSC, The Netherlands; NTNU, Norway; Oxford ",
            "University, UK; surfSARA, The Netherlands; SMHI, Sweden; Stockholm University, Sweden; Unite ASTR, Belgium; ",
            "University College Dublin, Ireland; University of Bergen, Norway; University of Copenhagen, Denmark; ",
            "University of Helsinki, Finland; University of Santiago de Compostela, Spain; Uppsala University, Sweden; ",
            "Utrecht University, The Netherlands; Vrije Universiteit Amsterdam, the Netherlands; Wageningen University, ",
            "The Netherlands. Mailing address: EC-Earth consortium, Rossby Center, Swedish Meteorological and Hydrological ",
            "Institute/SMHI, SE-601 76 Norrkoping, Sweden",
        ]
    ),
    "ECMWF": "European Centre for Medium-Range Weather Forecasts, Reading RG2 9AX, UK",
    "FIO-QLNM": "".join(
        [
            "FIO (First Institute of Oceanography, Ministry of Natural Resources, Qingdao 266061, China), ",
            "QNLM (Qingdao National Laboratory for Marine Science and Technology, Qingdao 266237, China)",
        ]
    ),
    "HAMMOZ-Consortium": "".join(
        [
            "ETH Zurich, Switzerland; Max Planck Institut fur Meteorologie, Germany; Forschungszentrum Julich, ",
            "Germany; University of Oxford, UK; Finnish Meteorological Institute, Finland; Leibniz Institute for Tropospheric ",
            "Research, Germany; Center for Climate Systems Modeling (C2SM) at ETH Zurich, Switzerland",
        ]
    ),
    "INM": "Institute for Numerical Mathematics, Russian Academy of Science, Moscow 119991, Russia",
    "IPSL": "Institut Pierre Simon Laplace, Paris 75252, France",
    "KIOST": "Korea Institute of Ocean Science and Technology, Busan 49111, Republic of Korea",
    "LLNL": " ".join(
        [
            "Lawrence Livermore National Laboratory, Livermore,",
            "CA 94550, USA. Mailing address: LLNL Climate Program,",
            "c/o Stephen A. Klein, Principal Investigator, L-103,",
            "7000 East Avenue, Livermore, CA 94550, USA",
        ]
    ),
    "MESSy-Consortium": "".join(
        [
            "The Modular Earth Submodel System (MESSy) Consortium, represented by the Institute for Physics of the Atmosphere, ",
            "Deutsches Zentrum fur Luft- und Raumfahrt (DLR), Wessling, Bavaria 82234, Germany",
        ]
    ),
    "MIROC": "".join(
        [
            "JAMSTEC (Japan Agency for Marine-Earth Science and Technology, Kanagawa 236-0001, Japan), ",
            "AORI (Atmosphere and Ocean Research Institute, The University of Tokyo, Chiba 277-8564, Japan), ",
            "NIES (National Institute for Environmental Studies, Ibaraki 305-8506, Japan), ",
            "and R-CCS (RIKEN Center for Computational Science, Hyogo 650-0047, Japan)",
        ]
    ),
    "MOHC": "Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK",
    "MPI-M": "Max Planck Institute for Meteorology, Hamburg 20146, Germany",
    "MRI": "Meteorological Research Institute, Tsukuba, Ibaraki 305-0052, Japan",
    "NASA-GISS": "Goddard Institute for Space Studies, New York, NY 10025, USA",
    "NASA-GSFC": "NASA Goddard Space Flight Center, Greenbelt, MD 20771, USA",
    "NCAR": "National Center for Atmospheric Research, Climate and Global Dynamics Laboratory, 1850 Table Mesa Drive, Boulder, CO 80305, USA",
    "NCC": "".join(
        [
            "NorESM Climate modeling Consortium consisting of ",
            "CICERO (Center for International Climate and Environmental Research, Oslo 0349), ",
            "MET-Norway (Norwegian Meteorological Institute, Oslo 0313), ",
            "NERSC (Nansen Environmental and Remote Sensing Center, Bergen 5006), ",
            "NILU (Norwegian Institute for Air Research, Kjeller 2027), ",
            "UiB (University of Bergen, Bergen 5007), ",
            "UiO (University of Oslo, Oslo 0313) ",
            "and UNI (Uni Research, Bergen 5008), Norway. Mailing address: NCC, c/o MET-Norway, ",
            "Henrik Mohns plass 1, Oslo 0313, Norway",
        ]
    ),
    "NERC": "Natural Environment Research Council, STFC-RAL, Harwell, Oxford, OX11 0QX, UK",
    "NIMS-KMA": " ".join(
        [
            "National Institute of Meteorological Sciences/Korea",
            "Meteorological Administration, Climate Research",
            "Division, Seoho-bukro 33, Seogwipo-si, Jejudo 63568,",
            "Republic of Korea",
        ]
    ),
    "NIWA": "National Institute of Water and Atmospheric Research, Hataitai, Wellington 6021, New Zealand",
    "NOAA-GFDL": "National Oceanic and Atmospheric Administration, Geophysical Fluid Dynamics Laboratory, Princeton, NJ 08540, USA",
    "NTU": "National Taiwan University, Taipei 10650, Taiwan",
    "NUIST": "Nanjing University of Information Science and Technology, Nanjing, 210044, China",
    "PCMDI": "Program for Climate Model Diagnosis and Intercomparison, Lawrence Livermore National Laboratory, Livermore, CA 94550, USA",
    "PNNL-WACCEM": "PNNL (Pacific Northwest National Laboratory), Richland, WA 99352, USA",
    "RTE-RRTMGP-Consortium": "".join(
        [
            "AER (Atmospheric and Environmental Research, Lexington, MA 02421, USA); UColorado (University of Colorado, ",
            "Boulder, CO 80309, USA). Mailing address: AER c/o Eli Mlawer, 131 Hartwell Avenue, Lexington, MA 02421, USA",
        ]
    ),
    "RUBISCO": "".join(
        [
            "ORNL (Oak Ridge National Laboratory, Oak Ridge, TN 37831, USA); ANL (Argonne National Laboratory, Argonne, IL 60439, USA); ",
            "BNL (Brookhaven National Laboratory, Upton, NY 11973, USA); LANL (Los Alamos National Laboratory, Los Alamos, NM 87545); ",
            "LBNL (Lawrence Berkeley National Laboratory, Berkeley, CA 94720, USA); NAU (Northern Arizona University, Flagstaff, AZ 86011, USA); ",
            "NCAR (National Center for Atmospheric Research, Boulder, CO 80305, USA); UCI (University of California Irvine, Irvine, CA 92697, USA); ",
            "UM (University of Michigan, Ann Arbor, MI 48109, USA). Mailing address: ORNL Climate Change Science Institute, c/o Forrest M. Hoffman, ",
            "Laboratory Research Manager, Building 4500N Room F106, 1 Bethel Valley Road, Oak Ridge, TN 37831-6301, USA",
        ]
    ),
    "SNU": "Seoul National University, Seoul 08826, Republic of Korea",
    "THU": "Department of Earth System Science, Tsinghua University, Beijing 100084, China",
    "UA": "Department of Geosciences, University of Arizona, Tucson, AZ 85721, USA",
    "UCI": "Department of Earth System Science, University of California Irvine, Irvine, CA 92697, USA",
    "UCSB": "".join(
        [
            "Bren School of Environmental Science and Management, University of California, Santa Barbara. Mailing address: ",
            "c/o Samantha Stevenson, 2400 Bren Hall, University of California Santa Barbara, Santa Barbara, CA 93106, USA",
        ]
    ),
    "UHH": "Universitat Hamburg, Hamburg 20148, Germany",
}

# %% CMIP6 License
license = {}
license["license"] = "".join(
    [
        "CMIP6 model data produced by <Your Institution; see CMIP6_institution_id.json> is ",
        "licensed under a <Creative Commons; select and insert a license_id; see below> License ",
        "(<insert the matching license_url; see below>). Consult ",
        "https://pcmdi.llnl.gov/CMIP6/TermsOfUse for terms of use governing CMIP6 output, ",
        "including citation requirements and proper acknowledgment. Further information about ",
        "this data, including some limitations, can be found via the further_info_url (recorded ",
        "as a global attribute in this file)[ and at <some URL maintained by modeling group>]. ",
        "The data producers and data providers make no warranty, either express or implied, ",
        "including, but not limited to, warranties of merchantability and fitness for a ",
        "particular purpose. All liabilities arising from the supply of the information ",
        "(including any liability arising in negligence) are excluded to the fullest extent ",
        "permitted by law.",
    ]
)
license["license_options"] = {}
license["license_options"]["CC0 1.0"] = {}
license["license_options"]["CC0 1.0"][
    "license_id"
] = "Creative Commons CC0 1.0 Universal Public Domain Dedication"
license["license_options"]["CC0 1.0"][
    "license_url"
] = "https://creativecommons.org/publicdomain/zero/1.0/"
license["license_options"]["CC BY 4.0"] = {}
license["license_options"]["CC BY 4.0"][
    "license_id"
] = "Creative Commons Attribution 4.0 International"
license["license_options"]["CC BY 4.0"][
    "license_url"
] = "https://creativecommons.org/licenses/by/4.0/"
license["license_options"]["CC BY-SA 4.0"] = {}
license["license_options"]["CC BY-SA 4.0"][
    "license_id"
] = "Creative Commons Attribution-ShareAlike 4.0 International"
license["license_options"]["CC BY-SA 4.0"][
    "license_url"
] = "https://creativecommons.org/licenses/by-sa/4.0/"
license["license_options"]["CC BY-NC-SA 4.0"] = {}
license["license_options"]["CC BY-NC-SA 4.0"][
    "license_id"
] = "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International"
license["license_options"]["CC BY-NC-SA 4.0"][
    "license_url"
] = "https://creativecommons.org/licenses/by-nc-sa/4.0/"

# %% MIP eras
mip_era = ["CMIP1", "CMIP2", "CMIP3", "CMIP5", "CMIP6"]

# %% Nominal resolutions
nominal_resolution = [
    "0.5 km",
    "1 km",
    "10 km",
    "100 km",
    "1000 km",
    "10000 km",
    "1x1 degree",
    "2.5 km",
    "25 km",
    "250 km",
    "2500 km",
    "5 km",
    "50 km",
    "500 km",
    "5000 km",
]

# %% Realms
realm = {
    "aerosol": "Aerosol",
    "atmos": "Atmosphere",
    "atmosChem": "Atmospheric Chemistry",
    "land": "Land Surface",
    "landIce": "Land Ice",
    "ocean": "Ocean",
    "ocnBgchem": "Ocean Biogeochemistry",
    "seaIce": "Sea Ice",
}

# %% Required global attributes
required_global_attributes = [
    "Conventions",
    "activity_id",
    "creation_date",
    "data_specs_version",
    "experiment",
    "experiment_id",
    "forcing_index",
    "frequency",
    "further_info_url",
    "grid",
    "grid_label",
    "initialization_index",
    "institution",
    "institution_id",
    "license",
    "mip_era",
    "nominal_resolution",
    "physics_index",
    "product",
    "realization_index",
    "realm",
    "source",
    "source_id",
    "source_type",
    "sub_experiment",
    "sub_experiment_id",
    "table_id",
    "tracking_id",
    "variable_id",
    "variant_label",
]

# %% Source identifiers
tmp = [
    [
        "source_id",
        "https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_source_id.json",
    ]
]
source_id = readJsonCreateDict(tmp)
source_id = source_id.get("source_id")
source_id = source_id.get("source_id")  # Fudge to extract duplicate level
del tmp

# Fix issues
# License

key = "EC-Earth3-Veg"
source_id[key]["activity_participation"].append("PMIP")
source_id[key]["activity_participation"].sort()

# Example fresh publication, no previous data
# key = "CanESM5-1"
# print("processing:", key)
# licenseId = "CC BY 4.0"
# source_id[key]["cohort"] = ["Published"]
# source_id[key]["license_info"]["exceptions_contact"] = "@ec.gc.ca <- f.cccma.info-info.ccmac.f"
# source_id[key]["license_info"]["history"] = "2022-12-02: initially published under CC BY 4.0"
# source_id[key]["license_info"]["id"] = licenseId
# licenseStr = license["license_options"][licenseId]["license_id"]
# licenseUrl = license["license_options"][licenseId]["license_url"]
# source_id[key]["license_info"]["license"] = "".join(
#     [licenseStr, " (", licenseId, "; ", licenseUrl, ")"])
# source_id[key]["license_info"]["source_specific_info"] = ""
# source_id[key]["license_info"]["url"] = licenseUrl

# Example license update, including email
# source_ids_to_relax_list = [
#     "E3SM-1-0",
#     "E3SM-1-1",
#     "E3SM-1-1-ECA",
# ]
#
# for key in source_ids_to_relax_list:
#     print("processing:", key)
#     licenseId = "CC BY 4.0"
#     source_id[key]["cohort"] = ["Published"]
#     source_id[key]["license_info"]["exceptions_contact"] = "@llnl.gov <- e3sm-data-support"
#     source_id[key]["license_info"]["history"] += "; 2022-06-15: relaxed to CC BY 4.0"
#     source_id[key]["license_info"]["id"] = licenseId
#     licenseStr = license["license_options"][licenseId]["license_id"]
#     licenseUrl = license["license_options"][licenseId]["license_url"]
#     source_id[key]["license_info"]["license"] = "".join(
#         [licenseStr, " (", licenseId, "; ", licenseUrl, ")"])
#     source_id[key]["license_info"]["source_specific_info"] = ""
#     source_id[key]["license_info"]["url"] = licenseUrl

# Example source_id registration
# key = "E3SM-2-0"
# source_id[key] = {}
# source_id[key]["activity_participation"] = [
#     "CFMIP",
#     "CMIP",
#     "DAMIP",
#     "RFMIP",
#     "ScenarioMIP",
# ]
# source_id[key]["cohort"] = [
#     "Registered",
# ]
# source_id[key]["institution_id"] = [
#     "E3SM-Project",
# ]
# source_id[key]["label"] = "E3SM 2.0"
# source_id[key]["label_extended"] = "E3SM 2.0 (Energy Exascale Earth System Model)"
# source_id[key]["model_component"] = {}
# source_id[key]["model_component"]["aerosol"] = {}
# source_id[key]["model_component"]["aerosol"]["description"] = " ".join(["MAM4 with new resuspension,",
#                                                                        "marine organics, secondary organics,",
#                                                                         "and dust (atmos grid)"])
# source_id[key]["model_component"]["aerosol"]["native_nominal_resolution"] = "100 km"
# source_id[key]["model_component"]["atmos"] = {}
# source_id[key]["model_component"]["atmos"]["description"] = " ".join(["EAM (v2.0, cubed sphere spectral-element grid;",
#                                                                       "5400 elements, 30x30 per cube face. Dynamics:",
#                                                                       "degree 3 (p=3) polynomials within each spectral",
#                                                                       "element, 112 km average resolution. Physics: 2x2",
#                                                                       "finite volume cells within each spectral element,",
#                                                                       "1.5 degree (168 km) average grid spacing; 72",
#                                                                       "vertical layers; top level 60 km)"])
# source_id[key]["model_component"]["atmos"]["native_nominal_resolution"] = "100 km"
# source_id[key]["model_component"]["atmosChem"] = {}
# source_id[key]["model_component"]["atmosChem"]["description"] = " ".join(["Troposphere specified oxidants (except",
#                                                                           "passive ozone with the lower boundary sink)",
#                                                                           "for aerosols. Stratosphere linearized",
#                                                                           "interactive ozone (LINOZ v2) (atmos grid)"])
# source_id[key]["model_component"]["atmosChem"]["native_nominal_resolution"] = "100 km"
# source_id[key]["model_component"]["land"] = {}
# source_id[key]["model_component"]["land"]["description"] = " ".join(["ELM (v1.0, satellite phenology mode, atmos grid),",
#                                                                      "MOSART (v1.0, 0.5 degree latitude/longitude)"])
# source_id[key]["model_component"]["land"]["native_nominal_resolution"] = "100 km"
# source_id[key]["model_component"]["landIce"] = {}
# source_id[key]["model_component"]["landIce"]["description"] = 'none'
# source_id[key]["model_component"]["landIce"]["native_nominal_resolution"] = 'none'
# source_id[key]["model_component"]["ocean"] = {}
# source_id[key]["model_component"]["ocean"]["description"] = " ".join(["MPAS-Ocean (E3SMv2.0, EC30to60E2r2 unstructured",
#                                                                       "SVTs mesh with 236853 cells, 719506 edges,",
#                                                                       "variable resolution 60 to 30 km; 60 levels;",
#                                                                       "top grid cell 0-10 m)"])
# source_id[key]["model_component"]["ocean"]["native_nominal_resolution"] = "50 km"
# source_id[key]["model_component"]["ocnBgchem"] = {}
# source_id[key]["model_component"]["ocnBgchem"]["description"] = 'none'
# source_id[key]["model_component"]["ocnBgchem"]["native_nominal_resolution"] = 'none'
# source_id[key]["model_component"]["seaIce"] = {}
# source_id[key]["model_component"]["seaIce"]["description"] = " ".join(["MPAS-Seaice (E3SMv2.0, ocean grid,",
#                                                                        "variable resolution 60 to 30 km; 5 ice",
#                                                                        "categories; 7 ice, 5 snow layers)"])
# source_id[key]["model_component"]["seaIce"]["native_nominal_resolution"] = "50 km"
# source_id[key]["release_year"] = "2022"
# source_id[key]["source_id"] = key
# # License info
# licenseId = "CC BY 4.0"
# source_id[key]["license_info"] = {}
# source_id[key]["license_info"]["exceptions_contact"] = "@llnl.gov <- e3sm-data-support"
# source_id[key]["license_info"]["history"] = "" #"2022-xx-xx: initially published under CC BY 4.0"
# source_id[key]["license_info"]["id"] = licenseId
# licenseStr = license["license_options"][licenseId]["license_id"]
# licenseUrl = license["license_options"][licenseId]["license_url"]
# source_id[key]["license_info"]["license"] = "".join(
# [licenseStr, " (", licenseId, "; ", licenseUrl, ")"])
# source_id[key]["license_info"]["url"] = licenseUrl

# Rename
# source_id[key2] = source_id.pop(key1)
# Remove
# source_id.pop(key1)

"""
Apply a check on the length of source ids. Raise a RuntimeError if any are found.
"""
MAX_SOURCE_ID_LENGTH = 25
MAX_SOURCE_ID_MSG_TEMPLATE = (
    'Source id "{}" is {} characters long which is above the limit of {}'
)
# Check all source ids for length
long_source_ids = [i for i in source_id if len(i) > MAX_SOURCE_ID_LENGTH]
errors = [
    MAX_SOURCE_ID_MSG_TEMPLATE.format(i, len(i), MAX_SOURCE_ID_LENGTH)
    for i in long_source_ids
]
# Raise exception if any found
if errors:
    raise RuntimeError(". ".join(errors))

del (long_source_ids, errors)

"""
Apply a check on the length of the source (generated in cmip6-cmor-tables/Tables/cmip6_CV.json)
Raise a runtime error if this string is >1024 characters
https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1129
https://github.com/PCMDI/cmip6-cmor-tables/issues/377
"""
MAX_SOURCE_LENGTH = 1023
MAX_SOURCE_MSG_TEMPLATE = 'source "{}" is {} characters long, above the {} limit'
# Create concatenated string
test_source_ids = [i for i in source_id]
errors = []
for key in test_source_ids:
    source = (
        source_id[key]["label"]
        + " ("
        + source_id[key]["release_year"]
        + "): "
        + chr(10)
    )
    for realm_test in source_id[key]["model_component"].keys():
        if (
            source_id[key]["model_component"][realm_test]["description"].find("None")
            == -1
        ):
            source += realm_test + ": "
            source += source_id[key]["model_component"][realm_test][
                "description"
            ] + chr(10)
    source = source.rstrip()
    if len(source) > MAX_SOURCE_LENGTH:
        errors.append(
            [MAX_SOURCE_MSG_TEMPLATE.format(key, len(source), MAX_SOURCE_LENGTH)]
        )
    elif key == "ENTER working key":
        print("\n\n*****")
        print(key, "len(source):", len(source), "limit:", MAX_SOURCE_LENGTH)
        print("*****\n\n")
        # print(source)
        pdb.set_trace()
# Raise exception if any found
if errors:
    raise RuntimeError(errors)
# cleanup
del (source, key, test_source_ids, errors, realm_test)

"""
CMIP5 Descriptors were documented in http://pcmdi.github.io/projects/cmip5/CMIP5_output_metadata_requirements.pdf?id=76
Format defined following AR5 Table 9.A.1 http://www.climatechange2013.org/images/report/WG1AR5_Chapter09_FINAL.pdf#page=114
"""

# %% Source types
source_type = {
    "AER": "aerosol treatment in an atmospheric model where concentrations are calculated based on emissions, transformation, and removal processes (rather than being prescribed or omitted entirely)",
    "AGCM": "atmospheric general circulation model run with prescribed ocean surface conditions and usually a model of the land surface",
    "AOGCM": "coupled atmosphere-ocean global climate model, additionally including explicit representation of at least the land and sea ice",
    "BGC": "biogeochemistry model component that at the very least accounts for carbon reservoirs and fluxes in the atmosphere, terrestrial biosphere, and ocean",
    "CHEM": "chemistry treatment in an atmospheric model that calculates atmospheric oxidant concentrations (including at least ozone), rather than prescribing them",
    "ISM": "ice-sheet model that includes ice-flow",
    "LAND": "land model run uncoupled from the atmosphere",
    "OGCM": "ocean general circulation model run uncoupled from an AGCM but, usually including a sea-ice model",
    "RAD": "radiation component of an atmospheric model run 'offline'",
    "SLAB": "slab-ocean used with an AGCM in representing the atmosphere-ocean coupled system",
}

# %% Sub experiment ids
sub_experiment_id = {}
sub_experiment_id["none"] = "none"
sub_experiment_id["s1910"] = "initialized near end of year 1910"
sub_experiment_id["s1920"] = "initialized near end of year 1920"
sub_experiment_id["s1950"] = "initialized near end of year 1950"
for yr in range(1960, 2030):
    sub_experiment_id["".join(["s", str(yr)])] = " ".join(
        ["initialized near end of year", str(yr)]
    )
del yr

# %% Table ids
table_id = [
    "3hr",
    "6hrLev",
    "6hrPlev",
    "6hrPlevPt",
    "AERday",
    "AERhr",
    "AERmon",
    "AERmonZ",
    "Amon",
    "CF3hr",
    "CFday",
    "CFmon",
    "CFsubhr",
    "E1hr",
    "E1hrClimMon",
    "E3hr",
    "E3hrPt",
    "E6hrZ",
    "Eday",
    "EdayZ",
    "Efx",
    "Emon",
    "EmonZ",
    "Esubhr",
    "Eyr",
    "IfxAnt",
    "IfxGre",
    "ImonAnt",
    "ImonGre",
    "IyrAnt",
    "IyrGre",
    "LImon",
    "Lmon",
    "Oclim",
    "Oday",
    "Odec",
    "Ofx",
    "Omon",
    "Oyr",
    "SIday",
    "SImon",
    "day",
    "fx",
]

# %% Prepare experiment_id and source_id for comparison
for jsonName in ["experiment_id", "source_id"]:
    if jsonName in ["experiment_id", "source_id"]:
        dictToClean = eval(jsonName)
        # for key, value in dictToClean.iteritems(): # Py2
        for key, value in iter(dictToClean.items()):  # Py3
            # for values in value.iteritems(): # values is a tuple # Py2
            for values in iter(value.items()):  # values is a tuple # Py3
                # test for dictionary
                if type(values[1]) is list:
                    new = []
                    for count in range(0, len(values[1])):
                        string = values[1][count]
                        string = cleanString(string)  # Clean string
                        new += [string]
                    # print 'new',new
                    # new.sort() ; # Sort all lists - not experiment_id model components
                    # print 'sort',new
                    dictToClean[key][values[0]] = new
                elif type(values[1]) is dict:
                    # determine dict depth
                    pdepth = dictDepth(values[1])
                    keyInd = values[0]
                    keys1 = values[1].keys()
                    if pdepth == 1:
                        # deal with flat dict "rights"
                        for d1Key in keys1:
                            string = dictToClean[key][keyInd][d1Key]
                            string = cleanString(string)  # Clean string
                            dictToClean[key][keyInd][d1Key] = string
                    else:
                        # deal with nested dict "model_components"
                        for d1Key in keys1:
                            # print("d1Key:", d1Key)
                            keys2 = values[1][d1Key].keys()
                            for d2Key in keys2:
                                string = dictToClean[key][keyInd][d1Key][d2Key]
                                string = cleanString(string)  # Clean string
                                dictToClean[key][keyInd][d1Key][d2Key] = string
                elif type(values[0]) == str:  # Py3
                    string = dictToClean[key][values[0]]
                    string = cleanString(string)  # Clean string
                    dictToClean[key][values[0]] = string
        vars()[jsonName] = dictToClean
del (
    jsonName,
    dictToClean,
    key,
    value,
    values,
    new,
    count,
    string,
    pdepth,
    keyInd,
    keys1,
    d1Key,
    keys2,
    d2Key,
)

# %% Validate source_id and experiment_id entries
RFMIPOnlyList = [
    "4AOP-v1-5",
    "ARTS-2-3",
    "GFDL-GLOBAL-LBL",
    "GFDL-GRTCODE",
    "GFDL-RFM-DISORT",
    "LBLRTM-12-8",
    "RRTMG-LW-4-91",
    "RRTMG-SW-4-02",
    "RTE-RRTMGP-181204",
]

# source_id
for key in source_id.keys():
    # Validate source_id format
    if not entryCheck(key):
        print("Invalid source_id format for entry:", key, "- aborting")
        sys.exit()
    if len(key) > 16:
        if key == "CESM1-1-CAM5-CMIP5":
            print(key, "skipped checks - continue")
            break
        print("Invalid source_id format for entry (too many chars):", key, "- aborting")
        sys.exit()
    # Validate activity_participation/activity_id
    val = source_id[key]["activity_participation"]
    # print key,val
    if "CMIP" not in val:
        if key in RFMIPOnlyList:
            print(key, "RFMIP only - continue")
        elif (
            "AerChemMIP" in val
        ):  # Case AerChemMIP only - IPSL-CM6A-LR-INCA, IPSL-CM5A2-INCA
            print(key, "AerChemMIP no CMIP required - continue")
        elif "FAFMIP" in val:  # Case FAFMIP only - GFDL-ESM2M
            print(key, "OMIP no CMIP required - continue")
        elif "HighResMIP" in val:  # Case HighResMIP only
            print(key, "HighResMIP no CMIP required - continue")
        elif "ISMIP6" in val:  # Case ISMIP6 only
            print(key, "ISMIP6 no CMIP required - continue")
        elif "OMIP" in val:  # Case OMIP only
            print(key, "OMIP no CMIP required - continue")
        elif "PAMIP" in val:  # Case PAMIP only - CESM1-WACCM-sc
            print(key, "PAMIP no CMIP required - continue")
        else:
            print(
                "Invalid activity_participation for entry:",
                key,
                "no CMIP listed - aborting",
            )
            sys.exit()
    for act in val:
        if act not in activity_id:
            print(
                "Invalid activity_participation for entry:", key, ":", act, "- aborting"
            )
            sys.exit()
    # Validate institution_id
    vals = source_id[key]["institution_id"]
    for val in vals:
        if val not in institution_id:
            print("Invalid institution_id for entry:", key, ";", val, "- aborting")
            sys.exit()
        if len(val) > 21:
            print(
                "Invalid institution_id format for entry (too many chars):",
                key,
                "- aborting",
            )
            sys.exit()
    # Validate nominal resolution
    vals = source_id[key]["model_component"].keys()
    for val1 in vals:
        val2 = source_id[key]["model_component"][val1]["native_nominal_resolution"]
        if val2 == "none":
            pass
        elif val2 not in nominal_resolution:
            print(
                "Invalid native_nominal_resolution for entry:",
                key,
                val1,
                val2,
                "- aborting",
            )
            sys.exit()
    # Validate source_id
    val = source_id[key]["source_id"]
    if key != val:
        print("Invalid source_id for entry:", val, "not equal", key, "- aborting")
        sys.exit()
# experiment_ids
experiment_id_keys = experiment_id.keys()
for key in experiment_id_keys:
    # Validate source_id format
    if not entryCheck(key):
        print("Invalid experiment_id format for entry:", key, "- aborting")
        sys.exit()
    # Validate internal key
    val = experiment_id[key]["experiment_id"]
    if not val == key:
        print("Invalid experiment_id for entry:", key, "- aborting")
        sys.exit()
    # Validate activity_id
    val = experiment_id[key]["activity_id"]
    for act in val:
        if act not in activity_id:
            print("Invalid activity_participation for entry:", key, act, "- aborting")
            sys.exit()
    # Validate additional_allowed_model_components
    vals = experiment_id[key]["additional_allowed_model_components"]
    for val in vals:
        if val == "":
            pass
        elif val not in source_type:
            print(
                "Invalid additional_allowed_model_components for entry:",
                key,
                val,
                "- aborting",
            )
            sys.exit()
    # Validate required_model_components
    vals = experiment_id[key]["required_model_components"]
    for val in vals:
        if val not in source_type:
            print(
                "Invalid required_model_components for entry:", key, val, "- aborting"
            )
            sys.exit()
    # Validate parent_activity_id
    vals = experiment_id[key]["parent_activity_id"]
    for val in vals:
        if val == "no parent":
            pass
        elif val not in activity_id:
            print("Invalid parent_activity_id for entry:", key, val, "- aborting")
            sys.exit()
    # Validate parent_experiment_id
    vals = experiment_id[key]["parent_experiment_id"]
    for val in vals:
        if val == "no parent":
            pass
        elif val not in experiment_id_keys:
            print("Invalid experiment_id_keys for entry:", key, val, "- aborting")
            sys.exit()

"""
    # Validate start/end years
    excludeList = [
            'aqua-p4K',
            'dcppA-assim', # start = before 1961
            'dcppA-hindcast',
            'dcppA-hindcast-niff',
            'dcppA-historical-niff',
            'dcppB-forecast',
            'dcppC-amv-neg',
            'dcppC-atl-pacemaker',
            'dcppC-atl-spg',
            'dcppC-forecast-addAgung',
            'dcppC-forecast-addElChichon',
            'dcppC-forecast-addPinatubo',
            'dcppC-hindcast-noAgung',
            'dcppC-hindcast-noElChichon',
            'dcppC-hindcast-noPinatubo',
            'dcppC-ipv-pos',
            'dcppC-ipv-NexTrop-pos',
            'dcppC-pac-control',
            'dcppC-pac-pacemaker',
            'esm-bell-1000PgC',
            'esm-bell-2000PgC',
            'esm-hist-ext', # end_year = present
            'faf-all',
            'futSST-pdSIC',
            'G6SST1', # Should be 2020 start
            'historical-ext', # end_year present
            'ism-1pctCO2to4x-self',
            'ism-piControl-self',
            'modelSST-futArcSIC',
            'modelSST-pdSIC',
            'pa-futAntSIC', # PAMIP start/end 2000/2001 should be min_num 2 not 1
            'pa-futArcSIC',
            'pa-pdSIC',
            'pa-piArcSIC',
            'pa-piAntSIC',
            'pdSST-futAntSIC',
            'pdSST-futArcSIC',
            'pdSST-futArcSICSIT',
            'pdSST-futBKSeasSIC',
            'pdSST-futOkhotskSIC',
            'pdSST-pdSIC',
            'pdSST-pdSICSIT',
            'pdSST-piAntSIC',
            'pdSST-piArcSIC',
            'piClim-2xDMS',
            'piClim-NH3',
            'piSST-4xCO2',
            'piSST-4xCO2-solar',
            'piSST-pdSIC',
            'piSST-piSIC'
            ]
"""
"""     LUMIP
            'land-cClim', # start_year 1850 or 1700
            'land-cCO2',
            'land-crop-grass',
            'land-crop-noFert',
            'land-crop-noIrrig',
            'land-crop-noIrrigFert',
            'land-hist',
            'land-hist-altLu1',
            'land-hist-altLu2',
            'land-hist-altStartYear',
            'land-noFire',
            'land-noLu',
            'land-noPasture',
            'land-noShiftCultivate',
            'land-noWoodHarv',
        Not sure
            'piControl-spinup-cmip5',
        No values in 3 fields
            'rad-irf'
"""
"""
    if key in excludeList:
        print('Skipping start/end_year test for:',key)
        continue
    #print('Start/end_year test for',key)
    valStart = experiment_id[key]['start_year']
    valEnd = experiment_id[key]['end_year']
    minNumYrsSim = experiment_id[key]['min_number_yrs_per_sim']
    if valStart == '' and valEnd == '':
        print('Start/end_year blank, skipping for:',key)
        continue
    # Deal with all LUMIP simulations
    if valStart == '1850 or 1700':
        valStart = 1850
        #print('land-* experiment identified, continuing')
    elif valStart: # Falsy test https://stackoverflow.com/questions/9573244/how-to-check-if-the-string-is-empty
        valStart = int(valStart)
    # Deal with all sspxxx simulations
    if valEnd == '2100 or 2300':
        valEnd = 2100
        #print('sspxxx experiment, skipping')
    elif valEnd:
        valEnd = int(valEnd)
    if minNumYrsSim:
        minNumYrsSim = int(minNumYrsSim)
    if valStart and valEnd and minNumYrsSim:
        pass
    else:
        print('Test values failed')
        print('start_year:',valStart,'end_year:',valEnd,'min_number_yrs_per_sim:',minNumYrsSim)
        sys.exit()
    #print('valStart:',valStart,type(valStart))
    #print('valEnd:',valEnd,type(valEnd))
    test = (int(valEnd)+1)-int(valStart)
    if int(minNumYrsSim) != test:
        print('Invalid start/end_year pair for entry:',key,'- aborting')
        print('start_year:',valStart,'end_year:',valEnd)
        print('min_number_yrs_per_sim:',test,minNumYrsSim)
        sys.exit()

del(experiment_id_keys,key,act,val,val1,val2,vals,valStart,valEnd,minNumYrsSim,test)
"""

del (experiment_id_keys, key, act, val, val1, val2, vals)
"""
print('***FINISH***')
sys.exit() ; # Turn back on to catch errors prior to running commit
"""

# %% Load remote repo versions for comparison - generate version identifier
for jsonName in masterTargets:
    target = "".join(["test", jsonName])
    testVal = "".join(["testVal_", jsonName])
    if jsonName == "mip_era":
        url = "".join(
            [
                "https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/",
                jsonName,
                ".json",
            ]
        )
    else:
        url = "".join(
            [
                "https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_",
                jsonName,
                ".json",
            ]
        )
    # composite components
    tmp = [[jsonName, url]]
    print("url:", url)
    # Create input list and load from web
    # force add DRS to repo
    # if jsonName == "DRS":
    #    testVal_DRS = {}
    #    testDRS = {}
    # continue with existing entries
    # else:
    vars()[target] = readJsonCreateDict(tmp)
    vars()[target] = eval(target).get(jsonName)
    # Fudge to extract duplicate level
    vars()[target] = eval(target).get(jsonName)
    # Test for updates
    # print(eval(target))
    # print(eval(jsonName))
    # print('---')
    # print(platform.python_version())
    # print(platform.python_version().split('.')[0])
    if platform.python_version().split(".")[0] == "3":
        vars()[testVal] = not (eval(target) == eval(jsonName))  # Py3
        # print(platform.python_version())
    # print(not(eval(target) == eval(jsonName)))
    # print('---')
    del (vars()[target], target, testVal, url, tmp)
del jsonName
# Use binary test output to generate
versionId = ascertainVersion(
    testVal_activity_id,
    testVal_DRS,
    testVal_experiment_id,
    testVal_frequency,
    testVal_grid_label,
    testVal_institution_id,
    testVal_license,
    testVal_mip_era,
    testVal_nominal_resolution,
    testVal_realm,
    testVal_required_global_attributes,
    testVal_source_id,
    testVal_source_type,
    testVal_sub_experiment_id,
    testVal_table_id,
    commitMessage,
)
versionHistory = versionId[0]
versionId = versionId[1]
print("Version:", versionId)
# sys.exit() ; # Use to evaluate changes

# %% Validate UTF-8 encoding - catch omip2 error https://github.com/WCRP-CMIP/CMIP6_CVs/issues/726
for jsonName in masterTargets:
    testDict = eval(jsonName)
    # print(jsonName,type(testDict))
    try:
        if platform.python_version().split(".")[0] == "2":
            if type(testDict) is list:
                # print('enter list')
                "".join(testDict).decode("utf-8")
            else:
                for key1, val1 in testDict.items():
                    # print('type key1:',type(key1))
                    key1.decode("utf-8")
                    if type(val1) is dict:
                        for key2, val2 in val1.items():
                            key2.decode("utf-8")
                            if type(val2) is list:
                                # Deal with list types
                                "".join(val2).decode("utf-8")
                            elif type(val2) is dict:
                                for key3, val3 in val2.items():
                                    if type(val3) is list:
                                        # Deal with list types
                                        "".join(val3).decode("utf-8")
                                    elif type(val3) is dict:
                                        for key4, val4 in val3.items():
                                            val4.decode("utf-8")
                                    else:
                                        val3.decode("utf-8")
                            else:
                                val2.decode("utf-8")
                    else:
                        val1.decode("utf-8")
        elif platform.python_version().split(".")[0] == "3":
            if type(testDict) is list:
                # print('enter list')
                "".join(testDict).encode("utf-8")
            else:
                for key1, val1 in testDict.items():
                    # print('type key1:',type(key1))
                    key1.encode("utf-8")
                    if type(val1) is dict:
                        for key2, val2 in val1.items():
                            key2.encode("utf-8")
                            if type(val2) is list:
                                # Deal with list types
                                "".join(val2).encode("utf-8")
                            elif type(val2) is dict:
                                for key3, val3 in val2.items():
                                    if type(val3) is list:
                                        # Deal with list types
                                        "".join(val3).encode("utf-8")
                                    elif type(val3) is dict:
                                        for key4, val4 in val3.items():
                                            val4.encode("utf-8")
                                    else:
                                        val3.encode("utf-8")
                            else:
                                val2.encode("utf-8")
                    else:
                        val1.encode("utf-8")
    except UnicodeEncodeError:
        # If left as UnicodeDecodeError - prints traceback
        print("UTF-8 failure for:", jsonName, "exiting")
        sys.exit()

# %% Write variables to files
timeNow = datetime.datetime.now().strftime("%c")
offset = (
    (calendar.timegm(time.localtime()) - calendar.timegm(time.gmtime())) / 60 / 60
)  # Convert seconds to hrs
# offset = ''.join(['{:03d}'.format(offset),'00']) # Pad with 00 minutes # Py2
offset = "".join(["{:03d}".format(int(offset)), "00"])  # Pad with 00 minutes # Py3
timeStamp = "".join([timeNow, " ", offset])
del (timeNow, offset)

for jsonName in masterTargets:
    # Write file
    if jsonName == "mip_era":
        outFile = "".join(["../", jsonName, ".json"])
    else:
        outFile = "".join(["../CMIP6_", jsonName, ".json"])
    # Get repo version/metadata - from src/writeJson.py

    # Extract last recorded commit for src/writeJson.py
    # print(os.path.realpath(__file__))
    versionInfo1 = getFileHistory(os.path.realpath(__file__))
    versionInfo = {}
    versionInfo["author"] = author
    versionInfo["institution_id"] = author_institution_id
    versionInfo["CV_collection_modified"] = timeStamp
    versionInfo["CV_collection_version"] = versionId

    # force DRS addition
    # if jsonName == "DRS":
    #     versionInfo['_'.join([jsonName, 'CV_modified'])
    #                 ] = timeStamp
    #     versionInfo['_'.join([jsonName, 'CV_note'])
    #                 ] = commitMessage
    # else:
    versionInfo["_".join([jsonName, "CV_modified"])] = versionHistory[jsonName][
        "timeStamp"
    ]
    versionInfo["_".join([jsonName, "CV_note"])] = versionHistory[jsonName][
        "commitMessage"
    ]

    versionInfo["previous_commit"] = versionInfo1.get("previous_commit")
    versionInfo["specs_doc"] = "v6.2.7 (10th September 2018; https://goo.gl/v1drZl)"
    del versionInfo1

    # Check file exists
    if os.path.exists(outFile):
        print("File existing, purging:", outFile)
        os.remove(outFile)
    # Create host dictionary
    jsonDict = {}
    jsonDict[jsonName] = eval(jsonName)
    # Append repo version/metadata
    jsonDict["version_metadata"] = versionInfo
    fH = open(outFile, "w")
    if platform.python_version().split(".")[0] == "2":
        json.dump(
            jsonDict,
            fH,
            ensure_ascii=True,
            sort_keys=True,
            indent=4,
            separators=(",", ":"),
            encoding="utf-8",
        )
    elif platform.python_version().split(".")[0] == "3":
        json.dump(
            jsonDict,
            fH,
            ensure_ascii=True,
            sort_keys=True,
            indent=4,
            separators=(",", ":"),
        )
    fH.close()

# Cleanup
del (jsonName, jsonDict, outFile)
del (
    activity_id,
    DRS,
    experiment_id,
    frequency,
    grid_label,
    institution_id,
    license,
    masterTargets,
    mip_era,
    nominal_resolution,
    realm,
    required_global_attributes,
    source_id,
    source_type,
    sub_experiment_id,
    table_id,
)
gc.collect()

# %% Update version info from new file/commit history
# Extract fresh recorded commit for src/writeJson.py
versionInfo1 = getFileHistory(os.path.realpath(__file__))
MD5 = versionInfo1.get("previous_commit")
# Now update versionHistory - can use list entries, as var names aren't locatable
if testVal_activity_id:
    key = "activity_id"
    versionHistoryUpdate(key, commitMessage, timeStamp, MD5, versionHistory)
if testVal_DRS:
    key = "DRS"
    versionHistoryUpdate(key, commitMessage, timeStamp, MD5, versionHistory)
if testVal_experiment_id:
    key = "experiment_id"
    versionHistoryUpdate(key, commitMessage, timeStamp, MD5, versionHistory)
if testVal_frequency:
    key = "frequency"
    versionHistoryUpdate(key, commitMessage, timeStamp, MD5, versionHistory)
if testVal_grid_label:
    key = "grid_label"
    versionHistoryUpdate(key, commitMessage, timeStamp, MD5, versionHistory)
if testVal_license:
    key = "license"
    versionHistoryUpdate(key, commitMessage, timeStamp, MD5, versionHistory)
if testVal_mip_era:
    key = "mip_era"
    versionHistoryUpdate(key, commitMessage, timeStamp, MD5, versionHistory)
if testVal_nominal_resolution:
    key = "nominal_resolution"
    versionHistoryUpdate(key, commitMessage, timeStamp, MD5, versionHistory)
if testVal_realm:
    key = "realm"
    versionHistoryUpdate(key, commitMessage, timeStamp, MD5, versionHistory)
if testVal_required_global_attributes:
    key = "required_global_attributes"
    versionHistoryUpdate(key, commitMessage, timeStamp, MD5, versionHistory)
if testVal_source_type:
    key = "source_type"
    versionHistoryUpdate(key, commitMessage, timeStamp, MD5, versionHistory)
if testVal_sub_experiment_id:
    key = "sub_experiment_id"
    versionHistoryUpdate(key, commitMessage, timeStamp, MD5, versionHistory)
if testVal_table_id:
    key = "table_id"
    versionHistoryUpdate(key, commitMessage, timeStamp, MD5, versionHistory)
if testVal_institution_id:
    key = "institution_id"
    versionHistoryUpdate(key, commitMessage, timeStamp, MD5, versionHistory)
if testVal_source_id:
    key = "source_id"
    versionHistoryUpdate(key, commitMessage, timeStamp, MD5, versionHistory)
# Test for changes and report
test = [
    testVal_activity_id,
    testVal_DRS,
    testVal_experiment_id,
    testVal_frequency,
    testVal_grid_label,
    testVal_license,
    testVal_mip_era,
    testVal_nominal_resolution,
    testVal_realm,
    testVal_required_global_attributes,
    testVal_source_type,
    testVal_sub_experiment_id,
    testVal_table_id,
    testVal_institution_id,
    testVal_source_id,
]
if any(test):
    # Create host dictionary
    jsonDict = {}
    jsonDict["versionHistory"] = versionHistory
    outFile = "versionHistory.json"
    if os.path.exists(outFile):
        os.remove(outFile)
    fH = open(outFile, "w")
    if platform.python_version().split(".")[0] == "2":
        json.dump(
            jsonDict,
            fH,
            ensure_ascii=True,
            sort_keys=True,
            indent=4,
            separators=(",", ":"),
            encoding="utf-8",
        )
    elif platform.python_version().split(".")[0] == "3":
        json.dump(
            jsonDict,
            fH,
            ensure_ascii=True,
            sort_keys=True,
            indent=4,
            separators=(",", ":"),
        )
    fH.close()
    print("versionHistory.json updated")
# Cleanup anyway
del (
    testVal_activity_id,
    testVal_DRS,
    testVal_experiment_id,
    testVal_frequency,
    testVal_grid_label,
    testVal_institution_id,
    testVal_license,
    testVal_mip_era,
    testVal_nominal_resolution,
    testVal_realm,
    testVal_required_global_attributes,
    testVal_source_id,
    testVal_source_type,
    testVal_sub_experiment_id,
    testVal_table_id,
)

# %% Generate revised html - process experiment_id, institution_id and source_id (alpha order)
# json_to_html.py ../CMIP6_experiment_id.json experiment_id CMIP6_experiment_id.html
# -r option included to regenerate citation pages
args = shlex.split("".join(["python ./jsonToHtml.py ", versionId, " -r"]))
# print(args)
p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd="./")
stdOut, stdErr = p.communicate()
print("Returncode:", p.returncode)  # If not 0 there was an issue
print("stdOut:", stdOut)
print("stdErr:", stdErr)
if b"Traceback" in stdErr:  # Py3
    print("json_to_html failure:")
    print("Exiting..")
    sys.exit()
del (args, p)
gc.collect()

# %% Now all file changes are complete, update README.md, commit and tag
# Load master history direct from repo
tmp = [
    [
        "versionHistory",
        "https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/src/versionHistory.json",
    ]
]
versionHistory = readJsonCreateDict(tmp)
versionHistory = versionHistory.get("versionHistory")
# Fudge to extract duplicate level
versionHistory = versionHistory.get("versionHistory")
del tmp
# Test for version change and push tag
versions = versionHistory["versions"]
versionOld = ".".join(
    [
        str(versions["versionMIPEra"]),
        str(versions["versionCVStructure"]),
        str(versions["versionCVContent"]),
        str(versions["versionCVCommit"]),
    ]
)
del versionHistory

if versionId != versionOld:
    # %% update Readme.md
    target_url = (
        "https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/README.md"
    )
    txt = urlopen(target_url).read().decode("utf-8")
    txt = txt.replace(versionOld, versionId)
    # delete existing file and write back to repo
    readmeH = "../README.md"
    os.remove(readmeH)
    fH = open(readmeH, "w")
    fH.write(txt)
    fH.close()
    print("README.md updated")
    del (target_url, txt, readmeH, fH)

    # %% update CITATION.cff
    target_url = (
        "https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CITATION.cff"
    )
    txt = urlopen(target_url).read().decode("utf-8")
    # replace versionId
    txt = txt.replace(versionOld, versionId)
    # replace date-released
    timeNow = datetime.datetime.now().strftime("%Y-%m-%d")
    txt = re.sub("[0-9]{4}-[0-9]{2}-[0-9]{2}", timeNow, txt)
    # delete existing file and write back to repo
    citationH = "../CITATION.cff"
    os.remove(citationH)
    fH = open(citationH, "w")
    fH.write(txt)
    fH.close()
    print("CITATION.cff updated")
    del (target_url, txt, citationH, fH)

# Commit all changes

args = shlex.split("".join(["git commit -am ", commitMessage]))
print(args)
p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd="./")

"""
# Merging branches changes the checksum, so the below doesn't work, UNLESS it's a direct master push
if versionId != versionOld:
    # Generate composite command and execute
    cmd = ''.join(['git ','tag ','-a ',versionId,' -m',commitMessage])
    print cmd
    subprocess.call(cmd,shell=True) ; # Shell=True required for string
    # And push all new tags to remote
    subprocess.call(['git','push','--tags'])
    print 'tag created and pushed'
"""
