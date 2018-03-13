#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 13:09:26 2018

PJD 12 Mar 2018     - Added 'specs_doc' attribute to version metadata upstream

@author: durack1
"""
#%% imports
import re
from durolib import getGitInfo,readJsonCreateDict

#%% Get repo metadata
def ascertainVersion(testVal_activity_id,testVal_experiment_id,testVal_frequency,
                     testVal_grid_label,testVal_institution_id,testVal_license,
                     testVal_mip_era,testVal_nominal_resolution,testVal_realm,
                     testVal_required_global_attributes,testVal_source_id,
                     testVal_source_type,testVal_sub_experiment_id,testVal_table_id,
                     commitMessage):
    # Load current history direct from repo master
    tmp = [['versionHistory','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/src/versionHistory.json']
      ] ;
    versionHistory = readJsonCreateDict(tmp)
    versionHistory = versionHistory.get('versionHistory')
    versionHistory = versionHistory.get('versionHistory') ; # Fudge to extract duplicate level
    del(tmp)
    versionMIPEra = versionHistory['versions'].get('versionMIPEra')
    versionCVStructure = versionHistory['versions'].get('versionCVStructure')
    versionCVContent = versionHistory['versions'].get('versionCVContent')
    versionCVCommit = versionHistory['versions'].get('versionCVCommit')

    # Deal with commitMessage formatting
    commitMessage = commitMessage.replace('\"','')

    # versionMIPEra - CMIP6 id - The first integer is “6”, indicating the CV collection is for use in CMIP6
    versionMIPEra = versionHistory['versions'].get('versionMIPEra')
    # versionCVStructure - Incremented when the structure/format of CV’s changes or a new CV is added
    versionCVStructure = versionHistory['versions'].get('versionCVStructure')
    # versionCVContent - Incremented when a change to existing content is made other than “source_id” or “institution_id”
    test1 = [testVal_activity_id,testVal_experiment_id,testVal_frequency,
            testVal_grid_label,testVal_license,testVal_mip_era,
            testVal_nominal_resolution,testVal_realm,
            testVal_required_global_attributes,testVal_source_type,
            testVal_sub_experiment_id,testVal_table_id]
    test2 = [testVal_institution_id,testVal_source_id]
    if any(test1):
        versionCVContent = versionHistory['versions'].get('versionCVContent') + 1
        versionCVCommit = 0
        # Now update versionHistory - can use list entries, as var names aren't locatable
        if testVal_activity_id:
            versionHistory['activity_id']['commitMessage'] = commitMessage
        if testVal_experiment_id:
            versionHistory['experiment_id']['commitMessage'] = commitMessage
        if testVal_frequency:
            versionHistory['frequency']['commitMessage'] = commitMessage
        if testVal_grid_label:
            versionHistory['grid_label']['commitMessage'] = commitMessage
        if testVal_license:
            versionHistory['license']['commitMessage'] = commitMessage
        if testVal_mip_era:
            versionHistory['mip_era']['commitMessage'] = commitMessage
        if testVal_nominal_resolution:
            versionHistory['nominal_resolution']['commitMessage'] = commitMessage
        if testVal_realm:
            versionHistory['realm']['commitMessage'] = commitMessage
        if testVal_required_global_attributes:
            versionHistory['required_global_attributes']['commitMessage'] = commitMessage
        if testVal_source_type:
            versionHistory['source_type']['commitMessage'] = commitMessage
        if testVal_sub_experiment_id:
            versionHistory['sub_experiment_id']['commitMessage'] = commitMessage
        if testVal_table_id:
            versionHistory['table_id']['commitMessage'] = commitMessage
    # versionCVCommit - Incremented whenever a new source_id and/or institution_id is added or amended
    elif any(test2):
        versionCVCommit = versionHistory['versions'].get('versionCVCommit') + 1
        # Now update versionHistory - can use list entries, as var names aren't locatable
        if testVal_institution_id:
            versionHistory['institution_id']['commitMessage'] = commitMessage
        if testVal_source_id:
            versionHistory['source_id']['commitMessage'] = commitMessage

    # versions - Update
    versionHistory['versions']['versionMIPEra'] = versionMIPEra
    versionHistory['versions']['versionCVStructure'] = versionCVStructure
    versionHistory['versions']['versionCVContent'] = versionCVContent
    versionHistory['versions']['versionCVCommit'] = versionCVCommit
    versions = '.'.join(str(x) for x in [versionMIPEra,versionCVStructure,versionCVContent,versionCVCommit])

    return [versionHistory,versions]


def entryCheck(entry,search=re.compile(r'[^a-zA-Z0-9-]').search):
    return not bool(search(entry))


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

def versionHistoryUpdate(key,commitMessage,timeStamp,MD5,versionHistory):
    url = 'https://github.com/WCRP-CMIP/CMIP6_CVs/commit/'
    commitMessage = commitMessage.replace('\"','') ; # Wash out extraneous\" characters
    versionHistory[key]['commitMessage'] = commitMessage
    versionHistory[key]['timeStamp'] = timeStamp
    versionHistory[key]['URL'] = ''.join([url,MD5])
    versionHistory[key]['MD5'] = MD5

    return versionHistory


#%% Clean functions
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
        string = string.replace('abrupt4xCO2','abrupt-4xCO2')
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


''' Notes

#import pyexcel_xlsx as pyx ; # requires openpyxl ('pip install openpyxl'), pyexcel-io ('git clone https://github.com/pyexcel/pyexcel-io')
# pyexcel-xlsx ('git clone https://github.com/pyexcel/pyexcel-xlsx'), and unidecode ('conda install unidecode')
#from string import replace
#from unidecode import unidecode
#import pdb

#import copy ; # Useful for copy.deepcopy() of dictionaries

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