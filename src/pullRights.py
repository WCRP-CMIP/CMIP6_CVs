#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 15:26:53 2022

Paul J. Durack 2nd March 2022

This script pulls information from multiple sources to generate rights info
for source_id entries

PJD  2 Mar 2022     - started
PJD  2 Mar 2022     - awaiting CMIP6/CMIP metadata scour to complete
PJD  2 Mar 2022     - started logic to extract info from metadata; added platform independent paths
PJD  3 Mar 2022     - added pathlib Path call
PJD  4 Mar 2022     - first pass at merging info
PJD 31 Mar 2022     - Updated input 220302_CMIP6-CMIP_metaData -> 220315_CMIP6-no-cdmsBadFiles_metaData
PJD  5 Apr 2022     - Updated input 220315 -> 220405_CMIP6-no-cdmsBadFiles_metadata
PJD 12 Apr 2022     - Updated input 220405 -> 220412_CMIP6_metaData_restartedInd-8243000
PJD 14 Apr 2022     - Updated input 220412 -> 220414_CMIP6_metaData_restartedInd-8243000 (1053)
PJD 20 Apr 2022     - Updated input 220414 -> 220420_CMIP6_metaData_restartedInd-8243000 (1230)
PJD 21 Apr 2022     - Updated input 220420 -> 220421_CMIP6_metaData_restartedInd-8243000 (0942)
PJD 22 Apr 2022     - Updated input 220421 -> 220422_CMIP6_metaData_restartedInd-8243000 (1206)
PJD 23 Apr 2022     - Updated input 220422 -> 220423_CMIP6_metaData_restartedInd-8243000 (0926)
PJD 25 Apr 2022     - Updated input 220423 -> 220425_CMIP6_metaData_restartedInd-8243000 (1109)
PJD 26 Apr 2022     - Updated input 220425 -> 220426_CMIP6_metaData_restartedInd-8243000 (2015)
PJD 27 Apr 2022     - Updated input 220426 -> 220427_CMIP6_metaData_restartedInd-8243000 (0849, 2051)
                     TODO: finish extract netcdf-harvested info

@author: durack1
"""

# %% imports

import csv
import datetime
import json
import os
import pdb
import platform
import time
from pathlib import Path

# %% define functions


def findRightsTxt(licStr):
    """
    findRightsTxt(licStr)

    Extracts license rights info assuming standard blurb is followed
    """
    strStart = "licensed under a "
    strEnd = (" (https://creativecommons.org/licenses")
    #strEnd = (" (https://creativecommons.org/licenses). Consult ")
    # strEnd = (" (https://creativecommons.org/licenses). Consult " +
    #          "https://pcmdi.llnl.gov/CMIP6/TermsOfUse for terms of use " +
    #          "governing CMIP6 output, including citation requirements " +
    #          "and proper acknowledgment.")
    rightsStartInd = licStr.find(strStart) + len(strStart)
    rightsEndInd = licStr.find(strEnd)
    licExt = licStr[rightsStartInd:rightsEndInd]

    # fudge typos
    if licExt == 'Creative Commons Attribution ShareAlike 4.0 International License':
        licExt = licExt.replace('tion Share', 'tion-Share')

    return licExt


# %% set start dir
homePath = str(Path.home())
if "macOS" in platform.platform():
    os.chdir(os.path.join(homePath, "sync/git/CMIP6_CVs/src"))
elif "Linux" in platform.platform():
    os.chdir(os.path.join(homePath, "git/CMIP6_CVs/src"))

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
print("get list of registered source_id entries from CMIP6_CVs...")
time.sleep(1)
with open("../CMIP6_source_id.json") as jsonFile:
    tmp = json.load(jsonFile)
    for count, key in enumerate(tmp["source_id"].keys()):
        print("count:", count, "source_id:", key)
        out[key] = {}
del(tmp, count, key, jsonFile)

# %% read Martina's info
print("read license info from Martina's citation service entries...")
time.sleep(1)
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
        print("source_id:", row[1], "license:", row[6])
        # out[row[1]] = {}  # create source_id entry
        out[row[1]]['dkrz'] = row[6]
del(martina, row, csvFile)

# %% extract netcdf-harvested info
print("process netcdf-file harvested info...")
time.sleep(1)
with open("220427_CMIP6_metaData_restartedInd-8243000.json") as jsonFile:
    tmp1 = json.load(jsonFile)
    for count, key1 in enumerate(tmp1.keys()):
        # deal with version_info
        if key1 in ["_badFileList", "version_metadata"]:
            continue
        keyBits = key1.split(".")
        instId = keyBits[1]
        srcId = keyBits[2]
        ver = keyBits[7]
        if "contact" in tmp1[key1].keys():
            contact = tmp1[key1]["contact"]
        else:
            contact = ""
        # cleanup blank entries
        if isinstance(contact, list):
            print(key1, "contact is list")
            pdb.set_trace()
            contact.remove("")
        # validate and process contact
        if isinstance(contact, dict):
            contact = list(set(contact.keys()))
        # validate and process license
        licInfo = tmp1[key1]["license"]
        if isinstance(licInfo, dict):
            tmp3 = []
            for count, key2 in enumerate(licInfo.keys()):
                licExt = findRightsTxt(key2)
                tmp3.append(licExt)
            if len(set(tmp3)) == 1:
                licExt = tmp3[0]
            else:
                print("more than one unique value")
                pdb.set_trace()
        else:
            licExt = findRightsTxt(licInfo)
        # Drop values into dictionary
        if srcId not in out.keys():
            out[srcId] = {}
            out[srcId]["contact"] = []
            out[srcId]["license"] = []
            out[srcId]["versions"] = []
        elif srcId in out.keys() and "versions" not in out[srcId].keys():
            out[srcId]["contact"] = []
            out[srcId]["license"] = []
            out[srcId]["versions"] = []
        # add info
        out[srcId]["license"].append(licExt)  # assume license doesn't change
        out[srcId]["versions"].append(ver)
        # and cleanup contact
        if contact != "" and not isinstance(contact, list):
            out[srcId]["contact"].append(contact)
        elif isinstance(contact, list) and "" in contact:
            contact.remove("")
            if len(contact) == 1:
                out[srcId]["contact"].append(contact[0])

# cleanup versions using sets
for key in out.keys():
    print("cleanup:", key)
    if "versions" in out[key].keys():
        tmp = out[key]["versions"]
        print("in ver:", len(tmp))
        tmp = list(set(tmp))
        tmp.sort()
        print("out ver:", len(tmp))
        out[key]["versions"] = [tmp[0], tmp[-1], len(tmp)]
    else:
        print("no version info:", key)
    if "license" in out[key].keys():
        tmp = out[key]["license"]
        print("in license:", len(tmp))
        tmp = list(set(tmp))
        tmp.sort()
        print("out license:", len(tmp))
        out[key]["license"] = tmp
    else:
        print("no license info:", key)
    if "contact" in out[key].keys():
        tmp = out[key]["contact"]
        print("in contact:", len(tmp))
        tmp = list(set(tmp))
        tmp.sort()
        print("out contact:", len(tmp))
        out[key]["contact"] = tmp
    else:
        print("no contact info:", key)

# %% populate MOHC UKESM1-0* provided input
for src in ["UKESM1-0-LL", "UKESM1-0-MMh", "UKESM1-ice-LL"]:
    out[src]["rights_identifier"] = "CC BY 4.0"
    out[src][
        "rights"] = "Data is made available under the Creative Commons Attribution 4.0 International License (CC by 4.0; https://creativecommons.org/licenses/by/4.0/)"
    out[src]["rights_info"] = "https://creativecommons.org/licenses/by/4.0/"
    out[src]["exceptions_contact"] = "@metoffice.gov.uk <-cmip6.ukesm1"
    out[src]["source_specific_info"] = "https://ukesm.ac.uk/licensing-of-met-office-nerc-and-niwa-cmip6-data/"
    out[src]["history"] = "2018-03-01: initially published under CC BY-SA 4.0; 2021-11-15: relaxed to CC BY 4.0"

# %% populate NASA-GISS provided input
for src in ["GISS-E2-1-G", "GISS-E2-1-G-CC", "GISS-E2-1-H", "GISS-E2-2-G", "GISS-E2-2-H", "GISS-E3-G"]:
    out[src]["rights_identifier"] = "CC0"
    out[src][
        "rights"] = "Creative Commons CC0 1.0 Universal Public Domain Dedication (CC0; https://creativecommons.org/publicdomain/zero/1.0/)"
    out[src]["rights_info"] = "https://creativecommons.org/publicdomain/zero/1.0/"
    out[src]["exceptions_contact"] = "@lists.nasa.gov <-cmip-giss-l"
    out[src]["source_specific_info"] = "https://data.giss.nasa.gov/modelE/cmip6/#datalicense"
    out[src]["history"] = "XX2018-09-06XX: initially published under CC BY-SA 4.0; 2021-12-01: relaxed to CC0"

# %% write json
timeNow = datetime.datetime.now()
timeFormatDir = timeNow.strftime('%y%m%d')
outFile = '_'.join([timeFormatDir, 'CMIP6-CMIP_mergedMetadata.json'])
if os.path.exists(outFile):
    os.remove(outFile)
with open(outFile, "w") as jsonFile:
    json.dump(
        out, jsonFile, ensure_ascii=True, sort_keys=True, indent=4, separators=(",", ":")
    )

# %% populate netcdf-harvested info
"""
for src in out.keys():
    # standard identifier (make sure DKRZ == metadata, if not query Martina on date)
    out[src]["rights_identifier"] = ""
    out[src]["rights"] = ""  # standard string
    out[src]["rights_info"] = ""  # standard url
    out[src]["exceptions_contact"] = ""  # contact info
    out[src]["source_specific_info"] = ""  # likely empty to start
    # first version date: initially published under CC BY-SA 4.0 (CMOR3 default is most common)
    out[src]["history"] = ""
"""

# %% compare strings
"""
cases = [(first, second)]
for a, b in cases:
    print('{} => {}'.format(a, b))
    for i, s in enumerate(difflib.ndiff(first, second)):
        if s[0] == ' ':
            continue
        elif s[0] == '-':
            print(u'Delete "{}" from position {}'.format(s[-1], i))
        elif s[0] == '+':
            print(u'Add "{}" to position {}'.format(s[-1], i))
"""
