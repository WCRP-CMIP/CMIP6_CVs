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
PJD 28 Apr 2022     - Updated input 220427 -> 220428_CMIP6_metaData_restartedInd-8243000 (1204)
PJD 29 Apr 2022     - Updated input 220428 -> 220429_CMIP6_metaData_restartedInd-8243000 (0916)
PJD 30 Apr 2022     - Updated input 220429 -> 220430_CMIP6_metaData_restartedInd-8243000 (0920)
PJD  1 May 2022     - Updated input 220430 -> 220501_CMIP6_metaData_restartedInd-8243000 (0817)
PJD  2 May 2022     - Updated input 220501 -> 220502_CMIP6_metaData_restartedInd-8243000 (1034)
PJD  3 May 2022     - Updated input 220502 -> 220503_CMIP6_metaData_restartedInd-8243000 (1034)
PJD  4 May 2022     - Updated fileDate -> fileName; 220503 -> 220504 (restarted; 0849, 1915)
PJD  5 May 2022     - Updated input 220504 -> 220505_CMIP6_metaData_restartedInd-8243000 (0919)
PJD  7 May 2022     - Updated 220505 -> 220507_CMIP6_metaData_restartedInd-23634000.json (0837)
PJD  8 May 2022     - Updated 220507 -> 220507_8MIP6_metaData_restartedInd-23634000.json (0837)
PJD  9 May 2022     - Updated 220508 -> 220509_8MIP6_metaData_restartedInd-23634000.json (0913)
PJD 10 May 2022     - Updated 220509 -> 220510_CMIP6_metaData_restartedInd-24949000.json (1615)
PJD 11 May 2022     - Updated 220510 -> 220511_CMIP6_metaData_restartedInd-24949000.json (1130, 1700, 2147)
PJD 12 May 2022     - Updated 220511 -> 220512_CMIP6_metaData_restartedInd-24949000.json (0718)
PJD 13 May 2022     - Updated 220512 -> 220513_CMIP6_metaData_restartedInd-24949000.json (0829)
PJD 14 May 2022     - Updated 220513 -> 220514_CMIP6_metaData_restartedInd-24949000.json (0837)
PJD 15 May 2022     - Updated 220514 -> 220514_CMIP6_metaData_restartedInd-24949000.json (1140, finalized)
PJD 16 May 2022     - Updated to write "rights" output per model
PJD 17 May 2022     - Added omitted model "TaiESM1-TIMCOM2"
PJD 18 May 2022     - Updated "rights" -> "license", cleaned up identifiers
PJD 18 May 2022     - Updated "license" -> "license_file" for the file-extracted identifier
                      https://github.com/WCRP-CMIP/CMIP6_CVs/pull/1066#issuecomment-1130243936
PJD 18 May 2022     - Updated "license" - "license_info"; Updated UKESM* latest license; code cleanup
PJD 19 May 2022     - Updated HadGEM3* entries to follow same license update info as UKESM*
PJD 19 May 2022     - Updated HadGEM3* contacts
                      https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1050#issuecomment-1036191330
PJD 24 May 2022     - Updated to deal with UKESM1-0-MMh removal https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1067
                    TODO: finish extract netcdf-harvested info
                     

ATSIGNauthor: durack1
"""

# %% imports

import csv
import datetime
import json
import os
import pdb
import platform
import re
import time
from pathlib import Path

# %%
fileName = "220514_CMIP6_metaData_restartedInd-24949000.json"

# %% define functions


def emailGarble(emailAddress):
    """
    emailGarble(emailAddress)

    Reformats email address to prevent spam usage
    """
    emailAddress = emailAddress.rstrip()  # Fix MCM-UA-1-0
    atInd = emailAddress.find("ATSIGN")
    emailAddressGarbled = " <- ".join(
        [emailAddress[atInd:], emailAddress[0:atInd]])
    emailAddressGarbled = emailAddressGarbled.replace("ATSIGN", "@")

    return emailAddressGarbled


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


def matchLicense(mod, licStr):
    """
    matchLicense(mod, licStr)

    matches file assigned license with identifier
    """
    # define license options
    rights = {}
    rights["CC0 1.0"] = {}
    rights["CC0 1.0"]["id"] = "Creative Commons CC0 1.0 Universal Public Domain Dedication"
    rights["CC0 1.0"]["url"] = "https://creativecommons.org/publicdomain/zero/1.0/"
    rights["CC BY 3.0"] = {}
    rights["CC BY 3.0"]["id"] = "Creative Commons Attribution 3.0 Unported"
    rights["CC BY 3.0"]["url"] = "https://creativecommons.org/licenses/by/3.0/"
    rights["CC BY 4.0"] = {}
    rights["CC BY 4.0"]["id"] = "Creative Commons Attribution 4.0 International"
    rights["CC BY 4.0"]["url"] = "https://creativecommons.org/licenses/by/4.0/"
    rights["CC BY-SA 4.0"] = {}
    rights["CC BY-SA 4.0"]["id"] = "Creative Commons Attribution-ShareAlike 4.0 International"
    rights["CC BY-SA 4.0"]["url"] = "https://creativecommons.org/licenses/by-sa/4.0/"
    rights["CC BY-NC-SA 4.0"] = {}
    rights["CC BY-NC-SA 4.0"]["id"] = "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International"
    rights["CC BY-NC-SA 4.0"]["url"] = "https://creativecommons.org/licenses/by-nc-sa/4.0/"

    # loop through options
    licId = ""
    # fix common [] issue with licStr
    # CESM1-1-CAM5-CMIP5, ?
    licStr = licStr.replace("tion-[]Share", "tion-Share")
    licStr = licStr.replace("tion-[*]Share", "tion-Share")  # MCM-UA-1-0
    for count, key in enumerate(rights.keys()):
        if not licStr.find(rights[key]["id"]):
            #print(mod, licStr, key)
            licId = key

    return rights, licId


def verToCal(verString):
    """
    verToCal(verString)

    Reformat ESGF version to parseable hyphenated format
    """
    # validate string - v20220516
    if re.match("^v[0-9]{8}$", verString):
        verStringFormatted = "-".join([verString[1:5],
                                      verString[5:7], verString[7:9]])
    else:
        print('version format invalid, exiting..', verString)
        verStringFormatted = None

    return verStringFormatted


# %% set start dir
homePath = str(Path.home())
if "macOS" in platform.platform():
    os.chdir(os.path.join(homePath, "sync/git/CMIP6_CVs/src"))
elif "Linux" in platform.platform():
    os.chdir(os.path.join(homePath, "git/CMIP6_CVs/src"))

# %% create default entries in dictionary
print("get list of registered source_id entries from CMIP6_CVs...")
# create output dictionary
out = {}
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
        if row[1] in ["CMCC-CM2-HR5", "CMCC-ESM2-HR5", "CMCC-ESM2-SR5",
                      "IPSL-CM7A-ATM-HR", "IPSL-CM7A-ATM-LR", "UKESM1-0-MMh"]:
            # IPSL-CM6A-ATM-LR-REPROBUS missing
            continue
        print("source_id:", row[1], "license:", row[6])
        # out[row[1]] = {}  # create source_id entry
        out[row[1]]['dkrz'] = row[6]
del(martina, row, csvFile)

# %% extract netcdf-harvested info
print("process netcdf-file harvested info...")
time.sleep(1)
with open(fileName) as jsonFile:
    tmp1 = json.load(jsonFile)
    for count, key1 in enumerate(tmp1.keys()):
        # deal with version_info
        if key1 in ["_badFileList", "version_metadata", "restart_badFileList"]:
            continue
        #print('key1:', key1)
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
            out[srcId]["license_file"] = []
            out[srcId]["versions"] = []
        elif srcId in out.keys() and "versions" not in out[srcId].keys():
            out[srcId]["contact"] = []
            out[srcId]["license_file"] = []
            out[srcId]["versions"] = []
        # add info
        # assume license doesn't change
        out[srcId]["license_file"].append(licExt)
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
        if tmp[0] == "v1":
            # fix CAMS-CSM1-0
            out[key]["versions"] = [tmp[1], tmp[-1], len(tmp)]
        else:
            out[key]["versions"] = [tmp[0], tmp[-1], len(tmp)]
    else:
        print("no version info:", key)
    if "license_file" in out[key].keys():
        tmp = out[key]["license_file"]
        print("in license:", len(tmp))
        tmp = list(set(tmp))
        tmp.sort()
        print("out license:", len(tmp))
        out[key]["license_file"] = tmp
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

# %% Check for missing entries
counter = 1
print('------ Missing models ------')
for count, mod in enumerate(out.keys()):
    if len(out[mod]) == 1:
        if mod == "PCMDI-test-1-0":
            print("PCMDI-test-1-0 found skipping")
            continue
        print(counter, mod)
        counter = counter + 1

# %% Generate direct inputs for CMIP6_CVs

for count, mod in enumerate(out.keys()):
    print(count, mod)
    # check for entries
    if "contact" in out[mod].keys():
        # extract info - versions
        versions = out[mod]["versions"]
        firstVer = verToCal(versions[0])
        lastVer = verToCal(versions[1])
        countVer = versions[2]
        # version complete
        # extract info - contact
        contact = out[mod]["contact"]
        if len(contact) == 1 and contact[0].find("(") < 0 and contact[0].find("@")\
                > 0 and contact[0].find("Please send any") < 0 and contact[0].find('metoffice.gov.uk') < 0:
            contact = contact[0].replace("@", "ATSIGN")
            contact = emailGarble(contact)
        # deal with case by case
        elif mod in ["ACCESS-OM2", "ACCESS-OM2-025"]:
            contact = emailGarble("access_csiroATSIGNcsiro.au")
        elif mod == "ARTS-2-3":
            contact = emailGarble("oliver.lemkeATSIGNuni-hamburg.de")
        elif mod in ["AWI-CM-1-1-HR", "AWI-CM-1-1-LR", "AWI-CM-1-1-MR", "AWI-ESM-1-1-LR"]:
            contact = emailGarble("tido.semmlerATSIGNawi.de")
        elif mod in ["BCC-CSM2-HR", "BCC-CSM2-MR", "BCC-ESM1"]:
            contact = emailGarble("twwuATSIGNcma.gov.cn")
        elif mod == "CAMS-CSM1-0":
            contact = emailGarble("rongxyATSIGNcma.gov.cn")
        elif mod == "CAS-ESM2-0":
            contact = emailGarble("zhangheATSIGNmail.iap.ac.cn")
        elif mod == "CESM1-1-CAM5-CMIP5":
            contact = emailGarble("cesm_cmip6ATSIGNucar.edu")
        elif mod == "CIESM":
            contact = emailGarble("yanluanATSIGNtsinghua.edu.cn")
        elif mod in ["CMCC-CM2-HR4", "CMCC-CM2-SR5", "CMCC-CM2-VHR4", "CMCC-ESM2"]:
            contact = emailGarble("piergiuseppe.fogliATSIGNcmcc.it")
        elif mod == "CMCC-ESM2-SR5":
            print(mod, "invalid data, skip..")
            continue
        elif mod in ["CNRM-CM6-1", "CNRM-CM6-1-HR", "CNRM-ESM2-1", "CNRM-ESM2-1-HR"]:
            contact = emailGarble("contact.cmip6ATSIGNcerfacs.fr")
        elif mod in ["E3SM-1-0", "E3SM-1-1", "E3SM-1-1-ECA"]:
            contact = emailGarble("bader2ATSIGNllnl.gov")
        elif mod in ["EC-Earth3", "EC-Earth3-AerChem", "EC-Earth3-LR", "EC-Earth3-Veg",
                     "EC-Earth3-Veg-LR", "EC-Earth3P", "EC-Earth3P-HR", "EC-Earth3P-VHR"]:
            contact = emailGarble("cmip6-dataATSIGNec-earth.org")
        elif mod in ["FGOALS-f3-H", "FGOALS-f3-L", "FGOALS-g3"]:
            contact = emailGarble("linpfATSIGNmail.iap.ac.cn")
        elif mod == "FIO-ESM-2-0":
            contact = emailGarble("songroyATSIGNfio.org.cn")
        elif mod in ["GFDL-GRTCODE", "GFDL-RFM-DISORT"]:
            contact = emailGarble("gfdl.climate.model.infoATSIGNnoaa.gov")
        elif mod in ["GISS-E2-1-G", "GISS-E2-1-G-CC", "GISS-E2-1-H", "GISS-E2-2-G",
                     "GISS-E2-2-H", "GISS-E3-G"]:
            contact = emailGarble("cmip-giss-lATSIGNlists.nasa.gov")
        elif mod in ["HadGEM3-GC31-HH", "HadGEM3-GC31-HM", "HadGEM3-GC31-LL",
                     "HadGEM3-GC31-LM", "HadGEM3-GC31-MH", "HadGEM3-GC31-MM"]:
            contact = emailGarble("cmip6.hadgem3ATSIGNmetoffice.gov.uk")
        elif mod in ["HiRAM-SIT-HR", "HiRAM-SIT-LR"]:
            contact = emailGarble("cytuATSIGNgate.sinica.edu.tw")
        elif mod in ["INM-CM4-8", "INM-CM5-0", "INM-CM5-H"]:
            contact = emailGarble("volodinevATSIGNgmail.com")
        elif mod in ["4AOP-v1-5", "IPSL-CM5A2-INCA", "IPSL-CM6A-ATM-HR", "IPSL-CM6A-LR",
                     "IPSL-CM6A-LR-INCA"]:
            contact = emailGarble("ipsl-cmip6ATSIGNlistes.ipsl.fr")
        elif mod == "KACE-1-0-G":
            contact = emailGarble("yoonjin.limATSIGNkorea.kr")
        elif mod == "KIOST-ESM":
            contact = emailGarble("yhokimATSIGNpknu.ac.kr")
        elif mod in ["LBLRTM-12-8", "RRTMG-LW-4-91", "RRTMG-SW-4-02", "RTE-RRTMGP-181204"]:
            contact = emailGarble("rpernakATSIGNaer.com")
        elif mod == "MCM-UA-1-0":
            contact = emailGarble("GEOS-CMIPATSIGNemail.arizona.edu")
        elif mod in ["MIROC-ES2H", "MIROC-ES2H-NB", "MIROC-ES2L", "MIROC6", "NICAM16-7S",
                     "NICAM16-8S", "NICAM16-9S"]:
            contact = emailGarble("onumaATSIGNiis.u-tokyo.ac.jp")
        elif mod in ["MPI-ESM-1-2-HAM", "MPI-ESM1-2-HR", "MPI-ESM1-2-LR", "MPI-ESM1-2-XR"]:
            contact = emailGarble("cmip6-mpi-esmATSIGNdkrz.de")
        elif mod in ["MRI-AGCM3-2-H", "MRI-AGCM3-2-S", "MRI-ESM2-0"]:
            contact = emailGarble("yukimotoATSIGNmri-jma.go.jp")
        elif mod == "NorCPM1":
            contact = emailGarble("norcpmATSIGNuib.no")
        elif mod in ["NorESM1-F", "NorESM2-LM", "NorESM2-MM"]:
            contact = emailGarble("noresm-nccATSIGNmet.no")
        elif mod == "SAM0-UNICON":
            contact = emailGarble("sjh11556ATSIGNsnu.ac.kr")
        elif mod == "TaiESM1":
            contact = emailGarble("leelupinATSIGNgate.sinica.edu.tw")
        elif mod in ["TaiESM1-TIMCOM", "TaiESM1-TIMCOM2"]:
            contact = emailGarble("tsengyhATSIGNntu.edu.tw")
        elif mod in ["UKESM1-0-LL", "UKESM1-0-MMh", "UKESM1-ice-LL"]:
            contact = emailGarble("cmip6.ukesm1ATSIGNmetoffice.gov.uk")
    else:
        print("no contact info:", mod, "continuing..")
        continue
        # contact complete
    # extract info - license
    if "license_file" in out[mod].keys():
        licStr = out[mod]["license_file"]
    else:
        print("no license info:", mod, "continuing..")
        continue
    if len(licStr) == 1 and not licStr == "":
        #print("mod:", mod, "licStr:", licStr[0])
        rights, licId = matchLicense(mod, licStr[0])
        rightsId = licId
        rightsStr = rights[rightsId]["id"]
        rightsUrl = rights[rightsId]["url"]
    elif mod == "CanESM5":
        rights, licId = matchLicense(mod, licStr[1])
        rightsId = licId
        rightsStr = rights[rightsId]["id"]
        rightsUrl = rights[rightsId]["url"]
    elif mod == "E3SM-1-1":
        rights, licId = matchLicense(mod, licStr[0])
        rightsId = licId
        rightsStr = rights[rightsId]["id"]
        rightsUrl = rights[rightsId]["url"]
    elif mod in ["GFDL-AM4", "GFDL-CM4"]:
        rights, licId = matchLicense(mod, licStr[1])
        rightsId = licId
        rightsStr = rights[rightsId]["id"]
        rightsUrl = rights[rightsId]["url"]
    elif mod in ["GISS-E2-1-G", "GISS-E2-1-G-CC", "GISS-E2-2-G"]:
        rights, licId = matchLicense(
            mod, "Creative Commons Attribution-ShareAlike 4.0 International License")
        rightsId = licId
        rightsStr = rights[rightsId]["id"]
        rightsUrl = rights[rightsId]["url"]
    elif mod == "HadGEM3-GC31-LL":
        rights, licId = matchLicense(mod, licStr[1])
        rightsId = licId
        rightsStr = rights[rightsId]["id"]
        rightsUrl = rights[rightsId]["url"]
    elif mod == "IPSL-CM6A-LR":
        rights, licId = matchLicense(mod, licStr[0])
        rightsId = licId
        rightsStr = rights[rightsId]["id"]
        rightsUrl = rights[rightsId]["url"]
    elif mod == "MIROC6":
        rights, licId = matchLicense(mod, licStr[1])
        rightsId = licId
        rightsStr = rights[rightsId]["id"]
        rightsUrl = rights[rightsId]["url"]
    elif mod == "MPI-ESM1-2-LR":
        rights, licId = matchLicense(
            mod, "Creative Commons Attribution-ShareAlike 4.0 International License")
        rightsId = licId
        rightsStr = rights[rightsId]["id"]
        rightsUrl = rights[rightsId]["url"]
    else:
        print("no license info:", mod, "continuing..")
        continue
    # rights complete
    # process info
    out[mod]["license_info"] = {}
    out[mod]["license_info"]["id"] = rightsId
    out[mod]["license_info"]["license"] = "".join(
        [rightsStr, " (", rightsId, "; ", rightsUrl, ")"])
    out[mod]["license_info"]["url"] = rightsUrl
    out[mod]["license_info"]["exceptions_contact"] = contact
    # default entries
    out[mod]["license_info"]["source_specific_info"] = ""
    out[mod]["license_info"]["history"] = "".join(
        [firstVer, ": initially published under ", rightsId])
    # conditional on group input
    # MOHC HadGEM3* and UKESM1*
    if mod in ["HadGEM3-GC31-HH", "HadGEM3-GC31-HM", "HadGEM3-GC31-LL",
               "HadGEM3-GC31-LM", "HadGEM3-GC31-MH", "HadGEM3-GC31-MM",
               "UKESM1-0-LL", "UKESM1-0-MMh", "UKESM1-ice-LL"]:
        out[mod]["license_info"]["source_specific_info"] =\
            "https://ukesm.ac.uk/licensing-of-met-office-nerc-and-niwa-cmip6-data/"
        out[mod]["license_info"]["history"] = ''.join(
            [out[mod]["license_info"]["history"], "; 2021-11-15: relaxed to CC BY 4.0"])
        # update to current
        out[mod]["license_info"]["id"] = "CC BY 4.0"
        out[mod]["license_info"][
            "license"] =\
            "Creative Commons Attribution 4.0 International License (CC BY 4.0; https://creativecommons.org/licenses/by/4.0/)"
        out[mod]["license_info"]["url"] = "https://creativecommons.org/licenses/by/4.0/"
    # NASA-GISS GISS-E*
    if mod in ["GISS-E2-1-G", "GISS-E2-1-G-CC", "GISS-E2-1-H", "GISS-E2-2-G",
               "GISS-E2-2-H", "GISS-E3-G"]:
        out[mod]["license_info"]["source_specific_info"] =\
            "https://data.giss.nasa.gov/modelE/cmip6/#datalicense"
        print(mod, out[mod]["license_info"]["history"])
        out[mod]["license_info"]["history"] = ''.join(
            [out[mod]["license_info"]["history"], "; 2021-12-01: relaxed to CC0 1.0"])
        # update to current
        out[mod]["license_info"]["id"] = "CC0 1.0"
        out[mod]["license_info"][
            "license"] =\
            "Creative Commons CC0 1.0 Universal Public Domain Dedication (CC0 1.0; https://creativecommons.org/publicdomain/zero/1.0/)"
        out[mod]["license_info"]["url"] = "https://creativecommons.org/publicdomain/zero/1.0/"


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
