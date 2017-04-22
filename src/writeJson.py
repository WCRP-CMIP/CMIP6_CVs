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
PJD  2 Nov 2016    - Update deforest-globe experiment_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/97
PJD  2 Nov 2016    - Remove RFMIP experiment_ids piClim-aerO3x0p1 and piClim-aerO3x2 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/79
PJD  2 Nov 2016    - Revise RFMIP experiment_ids hist-all-spAerO3 and hist-spAerO3 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/80
PJD  2 Nov 2016    - Revise RFMIP experiment_ids capitalization https://github.com/WCRP-CMIP/CMIP6_CVs/issues/81
PJD  2 Nov 2016    - Revise RFMIP experiment_ids spAerO3 -> spAer https://github.com/WCRP-CMIP/CMIP6_CVs/issues/82
PJD  2 Nov 2016    - Revise experiment_id ssp370 to include activity_id AerChemMIP https://github.com/WCRP-CMIP/CMIP6_CVs/issues/77
PJD  2 Nov 2016    - Revise experiment_id volc-cluster-mill https://github.com/WCRP-CMIP/CMIP6_CVs/issues/75
PJD  2 Nov 2016    - Revise experiment_id instances of LND -> LAND https://github.com/WCRP-CMIP/CMIP6_CVs/issues/74
PJD  2 Nov 2016    - Add experiment_id ism-ctrl-std https://github.com/WCRP-CMIP/CMIP6_CVs/issues/103
PJD  2 Nov 2016    - Add experiment_id ism-asmb-std https://github.com/WCRP-CMIP/CMIP6_CVs/issues/104
PJD  2 Nov 2016    - Add experiment_id ism-bsmb-std https://github.com/WCRP-CMIP/CMIP6_CVs/issues/105
PJD  3 Nov 2016    - Deal with invalid source_type syntax, rogue ","
PJD  8 Nov 2016    - Add CNRM to institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/129
PJD  8 Nov 2016    - Revise source_type https://github.com/WCRP-CMIP/CMIP6_CVs/issues/131
PJD 15 Nov 2016    - Remove coordinate, formula_terms and grids from repo https://github.com/WCRP-CMIP/CMIP6_CVs/issues/139
PJD 15 Nov 2016    - Rename grid_resolution to nominal_resolution and add new entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/141
PJD 15 Nov 2016    - Add MESSy-Consortium to institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/138
PJD 16 Nov 2016    - Revise AerChemMIP experiment model configurations https://github.com/WCRP-CMIP/CMIP6_CVs/issues/78
PJD 16 Nov 2016    - Add source_id VRESM-1-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/101
PJD 17 Nov 2016    - Revise grid_label to include Antarctica and Greenland https://github.com/WCRP-CMIP/CMIP6_CVs/issues/130
PJD 21 Nov 2016    - Revise institution_id NCC https://github.com/WCRP-CMIP/CMIP6_CVs/issues/83
PJD 21 Nov 2016    - Revise experiment_id 1pctCO2Ndep https://github.com/WCRP-CMIP/CMIP6_CVs/issues/73
PJD 21 Nov 2016    - Register source_id BNU-ESM-1-1 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/99
PJD 21 Nov 2016    - Register source_id EC-Earth-3 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/91
PJD 21 Nov 2016    - Register source_id EC-Earth-3-HR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/92
PJD 21 Nov 2016    - Register source_id EC-Earth-3-LR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/93
PJD 21 Nov 2016    - source_id cleanup, particularly for IITM-ESM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/96
PJD 21 Nov 2016    - Register institution_id CNRM-CERFACS https://github.com/WCRP-CMIP/CMIP6_CVs/issues/115
PJD 28 Nov 2016    - Register source_id NorESM2-LME https://github.com/WCRP-CMIP/CMIP6_CVs/issues/84
PJD 28 Nov 2016    - Register source_id NorESM2-MH https://github.com/WCRP-CMIP/CMIP6_CVs/issues/85
PJD 28 Nov 2016    - Register source_id NorESM2-LMEC https://github.com/WCRP-CMIP/CMIP6_CVs/issues/86
PJD 28 Nov 2016    - Register source_id NorESM2-HH https://github.com/WCRP-CMIP/CMIP6_CVs/issues/87
PJD 28 Nov 2016    - Register source_id NorESM2-MM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/88
PJD 28 Nov 2016    - Register source_id NorESM2-LM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/156
PJD 28 Nov 2016    - Revise multiple source_id NorESM* https://github.com/WCRP-CMIP/CMIP6_CVs/issues/156
PJD  7 Dec 2016    - Update activity_id for experiment_id ssp370 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/169#issuecomment-264726036
PJD  7 Dec 2016    - Add experiment_id 1pctCO2-4xext https://github.com/WCRP-CMIP/CMIP6_CVs/issues/170
PJD  7 Dec 2016    - Add institution_id html https://github.com/WCRP-CMIP/CMIP6_CVs/issues/172
PJD 14 Dec 2016    - Add frequency_id 1hr https://github.com/WCRP-CMIP/CMIP6_CVs/issues/178
PJD 14 Dec 2016    - Add source_id GISS-E2-1 variants https://github.com/WCRP-CMIP/CMIP6_CVs/issues/177
PJD  3 Jan 2017    - Add institution_id NERC https://github.com/WCRP-CMIP/CMIP6_CVs/issues/183
PJD  3 Jan 2017    - Update source_id EC-Earth-3-LR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/93
PJD  3 Jan 2017    - Register source_id EC-Earth-3-CC https://github.com/WCRP-CMIP/CMIP6_CVs/issues/94
PJD  3 Jan 2017    - Register source_ids HadGEM3*4 and UKESM1*2 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/184
PJD  3 Jan 2017    - Revise CMIP6 license text https://github.com/WCRP-CMIP/CMIP6_CVs/issues/133
PJD  3 Jan 2017    - Register source_ids CNRM-ESM2*2 and CNRM-CM6*2 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/115
PJD  5 Jan 2017    - Revise multiple CNRM source_ids atmospheric chemistry entry https://github.com/WCRP-CMIP/CMIP6_CVs/issues/115
PJD  5 Jan 2017    - Register multiple EC-Earth3 source_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/191
PJD  5 Jan 2017    - Update DCPP experiment_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1#issuecomment-268357110
PJD 10 Jan 2017    - Register multiple EC-Earth3 source_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/195, 196, 197
PJD 13 Jan 2017    - Update table_id to reflect Data Request V1.0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/199
PJD 18 Jan 2017    - Update experiment_id highres-future start_year https://github.com/WCRP-CMIP/CMIP6_CVs/issues/201
PJD 18 Jan 2017    - Add experiment_id spinup-1950 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/202
PJD 19 Jan 2017    - Update institution_id FIO -> FIO-SOA https://github.com/WCRP-CMIP/CMIP6_CVs/issues/205
PJD 21 Jan 2017    - Register institution_id AWI https://github.com/WCRP-CMIP/CMIP6_CVs/issues/207
PJD 21 Jan 2017    - Register source_id AWI-CM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/210
PJD 23 Jan 2017    - Update institution_id FIO-SOA -> FIO-RONM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/209
PJD 23 Jan 2017    - Register source_id MRI-ESM2-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/208
PJD 23 Jan 2017    - Revise experiment_id values for ISMIP https://github.com/WCRP-CMIP/CMIP6_CVs/issues/168
PJD 23 Jan 2017    - Revise source_id MRI-ESM2-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/208
PJD 30 Jan 2017    - Register source_id EMAC-2-53-AerChem https://github.com/WCRP-CMIP/CMIP6_CVs/issues/217
PJD 31 Jan 2017    - Revise source_id EMAC-2-53-AerChem https://github.com/WCRP-CMIP/CMIP6_CVs/issues/217
PJD  6 Feb 2017    - Revise license details
PJD  6 Feb 2017    - Register source_id AWI-CM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/210
PJD  6 Feb 2017    - Revise multiple EC-Earth3 source_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/191
PJD 27 Feb 2017    - Update license info
PJD 27 Feb 2017    - Register institution_id THU https://github.com/WCRP-CMIP/CMIP6_CVs/issues/225
PJD 27 Feb 2017    - Register source_id CIESM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/226
PJD  3 Mar 2017    - Register source_id MRI-ESM2-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/234
PJD  3 Mar 2017    - Register source_id MIROC6 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/229
PJD  3 Mar 2017    - Update all source_id cohort entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/230
PJD  7 Mar 2017    - Register source_id EMAC-2-53-Vol https://github.com/WCRP-CMIP/CMIP6_CVs/issues/231
PJD  7 Mar 2017    - Register source_ids MIROC-ES and NICAM variants https://github.com/WCRP-CMIP/CMIP6_CVs/pull/238
PJD  7 Mar 2017    - Update experiment_id from external xlsx https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1, 61, 136, 137
PJD 14 Mar 2017    - Update source_id ACCESS-1-0 template
PJD 17 Mar 2017    - Cleanup required_global_attributes https://github.com/WCRP-CMIP/CMIP6_CVs/issues/250
PJD 17 Mar 2017    - Augment source_id info request https://github.com/WCRP-CMIP/CMIP6_CVs/issues/249
PJD 20 Mar 2017    - Register institution_id CAMS https://github.com/WCRP-CMIP/CMIP6_CVs/issues/245
PJD 22 Mar 2017    - Revise experiment_id names and details for 2 RFMIP experiments https://github.com/WCRP-CMIP/CMIP6_CVs/issues/258
PJD 29 Mar 2017    - Revise experiment_id piClim-aer https://github.com/WCRP-CMIP/CMIP6_CVs/issues/261
PJD  5 Apr 2017    - Remove deprecated table_id entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/266
PJD  5 Apr 2017    - Convert experiment_id parent* entries to list https://github.com/WCRP-CMIP/CMIP6_CVs/issues/267
PJD  7 Apr 2017    - Register GFDL source_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/244
PJD  7 Apr 2017    - Register source_id CAMS_CSM1-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/246
PJD  8 Apr 2017    - Update multiple NorESM source_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/259
PJD  8 Apr 2017    - Update html markup https://github.com/WCRP-CMIP/CMIP6_CVs/issues/248
PJD 10 Apr 2017    - Revise source_id NorESM2-MH https://github.com/WCRP-CMIP/CMIP6_CVs/issues/259
PJD 12 Apr 2017    - Revise frequency to include yrClim https://github.com/WCRP-CMIP/CMIP6_CVs/issues/281
PJD 12 Apr 2017    - Add missing activity_id values https://github.com/WCRP-CMIP/CMIP6_CVs/issues/276
PJD 17 Apr 2017    - Register institution_id INPE https://github.com/WCRP-CMIP/CMIP6_CVs/issues/286
PJD 17 Apr 2017    - Register institution_id CMCC https://github.com/WCRP-CMIP/CMIP6_CVs/issues/284
PJD 17 Apr 2017    - Update realm format https://github.com/WCRP-CMIP/CMIP6_CVs/issues/285
PJD 18 Apr 2017    - Reconfigure source_id format to reflect all model components https://github.com/WCRP-CMIP/CMIP6_CVs/issues/264
PJD 18 Apr 2017    - Reconfigure json_to_html to deal with new source_id format
PJD 20 Apr 2017    - Revise AWI-CM source_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/210
PJD 21 Apr 2017    -  Clean up None instances in source_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/301
                   - TODO: Generate table_id from dataRequest https://github.com/WCRP-CMIP/CMIP6_CVs/issues/166
                   - TODO: Redirect sources to CMIP6_CVs master files (not cmip6-cmor-tables) ; coordinate, formula_terms, grids
                   - TODO: Generate function for json compositing

@author: durack1
"""

#%% Import statements
#import copy ; # Useful for copy.deepcopy() of dictionaries
import datetime
import gc
import json
import os
import shlex
import ssl
import subprocess
from durolib import readJsonCreateDict
from durolib import getGitInfo
#import pyexcel_xlsx as pyx ; # requires openpyxl ('pip install openpyxl'), pyexcel-io ('git clone https://github.com/pyexcel/pyexcel-io')
# pyexcel-xlsx ('git clone https://github.com/pyexcel/pyexcel-xlsx'), and unidecode ('conda install unidecode')
#from string import replace
#from unidecode import unidecode
#import pdb

#%% Set commit message
commitMessage = '\"Clean up None instances in source_id\"'

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
tmp = [['experiment_id','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_experiment_id.json']
      ] ;
experiment_id = readJsonCreateDict(tmp)
experiment_id = experiment_id.get('experiment_id')
experiment_id = experiment_id.get('experiment_id') ; # Fudge to extract duplicate level

# Fix issues
#==============================================================================
# Example new experiment_id entry
#experiment_id['ism-bsmb-std'] = {}
#experiment_id['ism-bsmb-std']['activity_id'] = ['ISMIP6']
#experiment_id['ism-bsmb-std']['additional_allowed_model_components'] = ['']
#experiment_id['ism-bsmb-std']['description'] = 'Offline ice sheet simulation with synthetic oceanic dataset to explore the uncertainty in sea level due to ice sheet initialization'
#experiment_id['ism-bsmb-std']['end_year'] = ''
#experiment_id['ism-bsmb-std']['experiment'] = 'offline ice sheet forced by initMIP synthetic oceanic experiment'
#experiment_id['ism-bsmb-std']['min_number_yrs_per_sim'] = '100'
#experiment_id['ism-bsmb-std']['parent_activity_id'] = ['ISMIP']
#experiment_id['ism-bsmb-std']['parent_experiment_id'] = ['']
#experiment_id['ism-bsmb-std']['required_model_components'] = ['ISM']
#experiment_id['ism-bsmb-std']['start_year'] = ''
#experiment_id['ism-bsmb-std']['sub_experiment'] = 'none'
#experiment_id['ism-bsmb-std']['sub_experiment_id'] = 'none'
#experiment_id['ism-bsmb-std']['tier'] = '1'
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
    '3hrClim',
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
    'NCAR': 'National Center for Atmospheric Research, Boulder, CO 80307, USA',
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
tmp = [['source_id','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_source_id.json']
      ] ;
source_id = readJsonCreateDict(tmp)
source_id = source_id.get('source_id')
source_id = source_id.get('source_id') ; # Fudge to extract duplicate level

# Fix issues
#==============================================================================
#key = 'AWI-CM-1-0'
#source_id[key]['activity_participation'] = [
# 'CMIP',
# 'CORDEX',
# 'HighResMIP',
# 'OMIP',
# 'PMIP',
# 'SIMIP',
# 'ScenarioMIP',
# 'VIACSAB'
#]
#source_id[key]['cohort'] = ['Registered']
#source_id[key]['institution_id'] = ['AWI']
#source_id[key]['label'] = 'AWI-CM 1.0'
#source_id[key]['label_extended'] = 'AWI-CM 1.0'
#source_id[key]['model_component']['aerosol']['description'] = 'None'
#source_id[key]['model_component']['aerosol']['nominal_resolution'] = 'None'
#source_id[key]['model_component']['atmos']['description'] = 'ECHAM6.3.02p4 (T127L95 native atmosphere T127 gaussian grid; 384 x 192 longitude/latitude; 95 levels; top level 80 km)'
#source_id[key]['model_component']['atmos']['nominal_resolution'] = '100 km'
#source_id[key]['model_component']['atmosChem']['description'] = 'None'
#source_id[key]['model_component']['atmosChem']['nominal_resolution'] = 'None'
#source_id[key]['model_component']['land']['description'] = 'JSBACH 3.10'
#source_id[key]['model_component']['land']['nominal_resolution'] = ' 100 km'
#source_id[key]['model_component']['landIce']['description'] = 'None'
#source_id[key]['model_component']['landIce']['nominal_resolution'] = 'None'
#source_id[key]['model_component']['ocean']['description'] = 'FESOM 1.4 (unstructured grid in the horizontal with 830305 wet nodes; 46 levels; top grid cell 0-5 m)'
#source_id[key]['model_component']['ocean']['nominal_resolution'] = '25 km'
#source_id[key]['model_component']['ocnBgchem']['description'] = 'None'
#source_id[key]['model_component']['ocnBgchem']['nominal_resolution'] = 'None'
#source_id[key]['model_component']['seaIce']['description'] = 'FESOM 1.4'
#source_id[key]['model_component']['seaIce']['nominal_resolution'] = '25 km'
#source_id[key]['release_year'] = '2017'
#source_id[key]['source_id'] = key
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
                    print 'elif list'
                    print values[1],values[0]
                    new = []
                    for count in range(0,len(values[1])):
                        print key,count
                        #print type(values[1][count])
                        string = values[1][count]
                        string = cleanString(string) ; # Clean string
                        new += [string]
                        print new
                    dictToClean[key][values[0]] = new
                elif type(values[1]) is dict:
                    print 'elif dict'
                    # determine dict depth
                    pdepth = dictDepth(values[1])
                    keys1 = values[1].keys()
                    for d1Key in keys1:
                        keys2 = values[1][d1Key].keys()
                        for d2Key in keys2:
                            print d1Key,d2Key
                            string = dictToClean[key][values[1]][d1Key][d2Key]
                            string = cleanString(string) ; # Clean string
                            dictToClean[key][values[1]][d1Key][d2Key] = string
                elif type(values[0]) in [str,unicode]:
                    print 'elif str unicode',type(values[0])
                    string = dictToClean[key][values[0]]
                    string = cleanString(string) ; # Clean string
                    dictToClean[key][values[0]] = string

#                string = dictToClean[key][values[0]]
#                string = cleanString(string) ; # Clean string
#                dictToClean[key][values[0]] = string
                
                #if not isinstance(values,str)
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
    #versionInfo = None ; # Used to add a new file
    if versionInfo == None:
        versionInfo = {}
        versionInfo['author'] = 'Paul J. Durack <durack1@llnl.gov>'
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
        #p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='./')

del(jsonName, jsonDict, outFile)
gc.collect()

# Validate - only necessary if files are not written by json module
