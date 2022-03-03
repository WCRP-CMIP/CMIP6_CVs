#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 15:26:53 2022

Paul J. Durack 2nd March 2022

This script pulls information from multiple sources to generate rights info
for source_id entries

PJD  2 Mar 2022     - started
PJD  2 Mar 2022     - awaiting CMIP6/CMIP metadata scour to complete

@author: durack1
"""

# %% imports

import csv
import json
import os

# %% set start dir
os.chdir("/Volumes/durack1ml/Users/durack1/sync/git/CMIP6_CVs/src")

# %% create output dictionary
out = {}
''' goal
"UKESM1-0-LL":{
      "dkrz":"CC BY-SA 4.0",
      "rights":"",
      "contact":"",
      "version":"",
      },
'''

# %% create default entries in dictionary
with open("/Volumes/durack1ml/Users/durack1/sync/git/CMIP6_CVs/CMIP6_source_id.json") as jsonFile:
    tmp = json.load(jsonFile)
    for count, key in enumerate(tmp["source_id"].keys()):
        print()
        print("count:", count, "source_id:", key)
        out[key] = {}
del(tmp, count, key, jsonFile)

# %% read Martina's info
# IPCC-AR6_CMIP6;INM-CM5-0;9;INM-CM5-0;Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0);http://creativecommons.org/licenses/by-sa/4.0/;CC BY-SA 4.0
with open("220208_MartinaStockhause_source_id_license_20220208.csv", newline="") as csvFile:
    martina = csv.reader(csvFile, delimiter=";")
    for row in martina:
        # deal with header, footer
        if row[1] in ["MODEL_ACRONYM", "--------------------------------------------------------------------------------", ";", ""]:
            continue
        # deal with input4MIPs data
        if row[0] == "CMIP6_input4MIPs":
            continue
        # deal with deprecated models
        if row[1] in ["CMCC-CM2-HR5", "CMCC-ESM2-HR5", "CMCC-ESM2-SR5", "IPSL-CM7A-ATM-HR", "IPSL-CM7A-ATM-LR"]:
            # IPSL-CM6A-ATM-LR-REPROBUS missing
            continue
        print()
        print("source_id:", row[1], "license:", row[6])
        # out[row[1]] = {}  # create source_id entry
        out[row[1]]['dkrz'] = row[6]
del(martina, row, csvFile)

# %% extract netcdf-harvested info
with open("/Volumes/durack1ml/Users/durack1/sync/git/CMIP6_CVs/src/220302_CMIP6-CMIP_metaData.json") as jsonFile:
    tmp = json.load(jsonFile)
    for count, key in enumerate(tmp.keys()):
        # deal with version_info
        if key == "version_metadata":
            continue
        pass
        # source_id
        # all versions
        # all contacts
        # all licenses

# %% populate netcdf-harvested info
for src in out.keys():
    # standard identifier (make sure DKRZ == metadata, if not query Martina on date)
    out[src]["rights_identifier"] = ""
    out[src]["rights"] = ""  # standard string
    out[src]["rights_info"] = ""  # standard url
    out[src]["exceptions_contact"] = ""  # contact info
    out[src]["source_specific_info"] = ""  # likely empty to start
    # first version date: initially published under CC BY-SA 4.0 (CMOR3 default is most common)
    out[src]["history"] = ""

# %% populate UKESM1-0* provided input
for src in ["UKESM1-0-LL", "UKESM1-0-MMh", "UKESM1-0-ice-LL"]:
    out[src]["rights_identifier"] = "CC BY 4.0"
    out[src][
        "rights"] = "Data is made available under the Creative Commons Attribution 4.0 International License (CC by 4.0; https://creativecommons.org/licenses/by/4.0/)"
    out[src]["rights_info"] = "https://creativecommons.org/licenses/by/4.0/"
    out[src]["exceptions_contact"] = "@metoffice.gov.uk <-cmip6.ukesm1"
    out[src]["source_specific_info"] = "https://ukesm.ac.uk/licensing-of-met-office-nerc-and-niwa-cmip6-data/"
    out[src]["history"] = "2018-03-01: initially published under CC BY-SA 4.0; 2021-11-15: relaxed to CC BY 4.0"

# %% write json
