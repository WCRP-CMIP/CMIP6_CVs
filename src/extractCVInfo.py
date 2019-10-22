#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 10:30:15 2019

Script generated to extract information out of the CVs for aggregated use

@author: durack1
"""
#%% imports and path config
import csv,datetime,json,os
homePath = '/sync/git/CMIP6_CVs'
os.chdir(homePath)
timeNow = datetime.datetime.now();
timeFormat = timeNow.strftime("%y%m%dT%H%M%S")

#%% Load experiment_id information
'''
f = 'CMIP6_experiment_id.json'
expId = json.load(open(f))
expId.keys()
expIds = expId.get('experiment_id')
verInfo = expId.get('version_metadata')
'''

#%% Extract all activity_id entries
'''
actIds = []
for exp in expIds.keys():
    actId = expIds[exp]['activity_id']
    if len(actId) == 1:
        if actId not in actIds:
            actIds.append(expIds[exp]['activity_id'][0])
    else:
        for actId in enumerate(len(actId)):
            if actId not in actIds:
                actIds.append(expIds[exp]['activity_id'][0])
'''
#%% Aggregate activity_id intentions from models
# Load source_id CV
f = 'CMIP6_source_id.json'
srcId = json.load(open(f))
srcId.keys()
srcIds = srcId.get('source_id')
srcIds.keys()
verInfo = srcId.get('version_metadata')
# Load activity_id CV
f = 'CMIP6_activity_id.json'
actId = json.load(open(f))
actIds = actId.get('activity_id')
actIds.keys()
# Initialize actIdCounter
for act in enumerate(actIds.keys()):
    print('act:',act[-1])
    vars()[act[-1]] = 0
# Loop through instances and collect activity_id intentions
for model in enumerate(srcIds.keys()):
    print('model:',model[-1])
    actIdVals = srcIds[model[-1]]['activity_participation']
    for act in enumerate(actIdVals):
        print(act[-1])
        vars()[act[-1]] = vars()[act[-1]]+1
# Write out results to csv
outFile = os.path.join(homePath,'src','_'.join([timeFormat,'activity_participation.csv']))
print(outFile)
with open(outFile,'w') as actParticipFile:
    actWriter = csv.writer(actParticipFile,delimiter=',',quotechar='"',
                           quoting=csv.QUOTE_MINIMAL)
    for act in enumerate(actIds.keys()):
        print('{:02d}'.format(act[0]+1),act[-1],vars()[act[-1]])
        actWriter.writerow(['{:02d}'.format(act[0]+1),act[-1],vars()[act[-1]]])
