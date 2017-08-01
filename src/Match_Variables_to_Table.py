#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 17:42:04 2017

@author: musci2

THIS CODE TAKES THE PATH OF INTEREST, LOOKS UP ALL OF THE VARIABLES IN THAT PATH, AND THEN CHECKS TO SEE IF EACH OF THOSE VARIABLES
ARE IN ANY OF THE CMIP6___.JSON TABLES (AMON,OMON,SIMON,LMON). IF SO, THEY ARE PASSED TO A DICTIONARY THAT IS THEN FED INTO THE
BIG_KAHUNA SCRIPT, ALLOWING SAID VARIABLE TO BE REPROCESSED. IF THERE IS NO MATCH FOUND IN ANY OF THE CMIP6___ TABLES, THE VARIABLE
IS MARKED AS MISSING
"""

import cmor, gc, json, sys, os, shutil
import cdms2 as cdm
import cdutil as cdu
import numpy as np

#specify where tables are located 
tablepath = '/export/musci2/git/cmip6-cmor-tables/Tables/'

#specify where the data to be re-analyzed is
#AMIP Data
pathin= '/oldCMIPs/PJG_StorageRetrieval/AMIP2-STORAGE/mo/'
#CMIP Data
pathinCMIP = '/oldCMIPs/PJG_StorageRetrieval/CMIP6-STORAGE/mo/'

#specify where output is saved
savepath = '/export/musci2/git/cmip6-cmor-tables/'

Matches = list()
Missings = list()
Errors = list()
VarsAndTables = {}

# open the monthly tales so that their variables can be compared to those in the directory being re-analysed
Amon = json.load(open('/export/musci2/git/cmip6-cmor-tables/Tables/CMIP6_Amon.json'))
Omon = json.load(open('/export/musci2/git/cmip6-cmor-tables/Tables/CMIP6_Omon.json'))
SImon = json.load(open('/export/musci2/git/cmip6-cmor-tables/Tables/CMIP6_SImon.json'))
Lmon = json.load(open('/export/musci2/git/cmip6-cmor-tables/Tables/CMIP6_Lmon.json'))

Possible_Variables_Amon = Amon['variable_entry'].keys()
Possible_Variables_Omon = Omon['variable_entry'].keys()
Possible_Variables_SImon = SImon['variable_entry'].keys()
Possible_Variables_Lmon = Lmon['variable_entry'].keys()

Provided_Variables = os.listdir(pathin)
Provided_Variables_CMIP = os.listdir(pathinCMIP)


for var in Provided_Variables:
    if var in Possible_Variables_Amon:
        print 'matched'
        Matches.append(var)
        VarsAndTables[var]=['Amon']
    elif var in Possible_Variables_Omon:
        print 'matched'
        Matches.append(var) 
        VarsAndTables[var]=['Omon']        
    elif var in Possible_Variables_SImon:
        print 'matched'
        Matches.append(var) 
        VarsAndTables[var]=['SImon']         
    elif var in Possible_Variables_Lmon:
        print 'matched'
        Matches.append(var) 
        VarsAndTables[var]=['Lmon']     
    else:
        print 'no match'
        Missings.append(var)
        VarsAndTables[var]=['Missing']
# These variables were compared by hand


#for var in Provided_Variables_CMIP:
#    if var in Possible_Variables_Amon:
#        print 'matched'
#        Matches.append(var)
#    else:
#        print 'no match'
#        if var in Missings:
#            print 'matched a miss'
#        else:
#            print 'another miss'
#            Missings.append(var)

#CMIP_varbs = ["cl","prec_ls","mrsos","mrso","mrro","mpuua","mptta","rss","rls","rltcrfm2","rlns","snw","rsns","prl","rstcrfm2","rsnt","sit","sic","rldscd",
#                    "prs","tauvgwd","tauugwd","mrros","water","tntsw","tntmc","tntlw","tntlsp","tnmrc","tnmmvgwd","tnmmugwd","stfgif","snow","prsm"]
#for varb in CMIP_varbs:
#    if varb in Missings:
#        print 'matched a miss'
#    else:
#        print 'another miss'
#        Missings.append(varb)

j = json.dumps(Missings, sort_keys=True, indent=4, ensure_ascii=True,separators=(',',':'))
completePath=os.path.join(savepath,'AmonTable_MissingVariables.json')
f = open(completePath, 'w')
print >> f, j
f.close()