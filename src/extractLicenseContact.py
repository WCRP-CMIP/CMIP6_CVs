#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 14:41:24 2022

Paul J. Durack 8th February 2022

This script polls all CMIP6 data and extracts license and contact information

PJD  9 Feb 2022     - Updated to validate and catch inconsistencies
PJD  9 Feb 2022     - Updated to get alertError working
PJD  9 Feb 2022     - Added incremental saving
PJD  9 Feb 2022     - Added np.ndarray washing to list
PJD  9 Feb 2022     - Updated to deal with nested dictionaries of errors
PJD  9 Feb 2022     - Debugging nested errors CanESM5
PJD 14 Feb 2022     - Updated to deal with multiple nominal_resolution entries per realm
PJD 15 Feb 2022     - Added lat/lon/depth/height scour
PJD 15 Feb 2022     - Extended debugging to ascertain valid grid (lat/lon pairs)
PJD 15 Feb 2022     - Update alertError output
PJD 15 Feb 2022     - Added try wrap to deal with nospam.llnl.gov timeouts
PJD 15 Feb 2022     - Update to run for CMIP6/CMIP (complete archive later)
PJD 16 Feb 2022     - Updated getGlobalAtts to deal with cdms2.open error - see https://github.com/CDAT/cdms/issues/442
PJD 16 Feb 2022     - Updated compareDicts so that "original" key is updated to $table_id_$variable_id
PJD 16 Feb 2022     - Updated getAxes to remove get* calls in second tier
PJD 17 Feb 2022     - Turned off alertError reporting
PJD 18 Feb 2022     - Switched getGlobalAtts to using variable_id key (CMIP6)
PJD 19 Feb 2022     - Add loop timer to gauge slowdowns
PJD 19 Feb 2022     - Added to cdmsBadFiles
PJD 20 Feb 2022     - Added getCalendar
PJD 20 Feb 2022     - Update getAxes with fileHandle additional arg
PJD 23 Feb 2022     - Updated getAxes to deal with site axes - now returns empty dictionary
PJD 23 Feb 2022     - Updated getGlobalAtts to try both varname and tmp["variable_name"]
PJD 25 Feb 2022     - Added to badFiles CMIP 47148
PJD 25 Feb 2022     - Tweak getGlobalAtts to deal with cdms2.open SystemError
PJD 26 Feb 2022     - Updated getGlobalAtts to only return valid calendar; updated getCalendar getAxisList -> getAxisIds
PJD 28 Feb 2022     - Added argparse for activity_id/path scan
PJD 28 Feb 2022     - Updated compareDicts to truncate duplicate values, adding a counter for times returned
PJD  5 Mar 2022     - Added OMIP to activity list
PJD  7 Mar 2022     - Added RFMIP to activity list
PJD  7 Mar 2022     - Added to badFiles ScenarioMIP 527759
PJD  7 Mar 2022     - Added CMIP6 search option - all MIPs
PJD  8 Mar 2022     - Added to badFiles CMIP6 669356
PJD  9 Mar 2022     - Added to badFiles ScenarioMIP 5543227
PJD  9 Mar 2022     - Updated getGlobalAtt to catch OSError and report file as string
PJD 10 Mar 2022     - Updated getGlobalAtt to catch SystemError ("UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb0 in position 11: invalid start byte")
PJD 10 Mar 2022     - Update to remove cdmsBadFiles list - update filename
PJD 14 Mar 2022     - Update getGlobalAtt to catch edge case of OSError/cdms read fail
PJD 15 Mar 2022     - Add RFMIP badFileList output to file end
PJD 16 Mar 2022     - Rewrote IO around xarray data = dataset.open_dataset(f) - getGlobalAtt/getCalendar
PJD 17 Mar 2022     - Update to finalize xarray IO; Add new ValueError to open try statement (new for xarray)
PJD 19 Mar 2022     - Updated getGlobalAtt with additional excludeVars, add AttributeError to try
PJD 24 Mar 2022     - Started work on readData to abstract open calls to function, so library used can be tweaked in one place
PJD 29 Mar 2022     - readData working
PJD 30 Mar 2022     - writeJson debugging, as np.int64 types not caught by numpyEncoder class
PJD 30 Mar 2022     - Updated compareDicts to ensure that dictionary keys are all str types (not np.ndarray or np.int64 types)
                      TypeError: '>' not supported between instances of 'numpy.ndarray' and 'str'
PJD 30 Mar 2022     - Update getAxes to deal with lev.shape == () error
                     5184 CMIP6 /p/css03/esgf_publish/CMIP6/ISMIP6/NASA-GISS/GISS-E2-1-G/1pctCO2-4xext/r1i1p1f1/Emon/cSoilAbove1m/gn/v20181022/cSoilAbove1m_Emon_GISS-E2-1-G_1pctCO2-4xext_r1i1p1f1_gn_192001-195012.nc
PJD 30 Mar 2022     - Updated readData to capture errX and errC and save these to badFileList for trapping
PJD 31 Mar 2022     - Updated readData to deal with xarray open_dataset read error; tweaked cdm.getLatitude()._data call to try - numpy.core._exceptions._UFuncBinaryResolutionError: ufunc 'subtract' cannot use operands with types dtype('O') and dtype('<m8[ns]')
                     122915 CMIP6 /p/css03/esgf_publish/CMIP6/PMIP/CAS/FGOALS-g3/lig127k/r1i1p1f1/Amon/phalf/gn/v20191030/phalf_Amon_FGOALS-g3_lig127k_r1i1p1f1_gn_076001-076912-clim.nc - KeyError no T axis
PJD  1 Apr 2022     - Updated readData to deal with xarray open_dataset read error; tweaked cdm.getLat/Lon calls to check they exist
                     452910 CMIP6 /p/css03/esgf_publish/CMIP6/PMIP/IPSL/IPSL-CM6A-LR/midPliocene-eoi400/r1i1p1f1/AERmonZ/o3/grz/v20190118/o3_AERmonZ_IPSL-CM6A-LR_midPliocene-eoi400_r1i1p1f1_grz_185001-204912.nc - KeyError: "No results found for 'Y'."
PJD  1 Apr 2022     - Wrapped for x loop in try and except - alertError; updated readData to preallocate errors in case of ncdump error
PJD  1 Apr 2022     - Found DRS vs fileName variable error - leads to numpy.core._exceptions._UFuncBinaryResolutionError, <class 'cdms2.error.CDMSError'>
                     717815 CMIP6 /p/css03/esgf_publish/CMIP6/HighResMIP/MOHC/HadGEM3-GC31-HM/highresSST-present/r1i1p1f1/6hrPlevPt/wbptemp7h/gn/v20170831/wbptemp_6hrPlevPt_HadGEM3-GC31-HM_highresSST-present_r1i1p1f1_gn_199307010000-199309301800.nc
PJD  6 Apr 2022     - Updated readData to deal with xarray RuntimeError
                     4512180 CMIP6 /p/css03/esgf_publish/CMIP6/ScenarioMIP/EC-Earth-Consortium/EC-Earth3/ssp245/r3i1p1f1/SImon/siu/gn/v20210517/siu_SImon_EC-Earth3_ssp245_r3i1p1f1_gn_203301-203312.nc
PJD  6 Apr 2022     - Added restartLog input argument to allow a restart from the last saved state; updated writeJson for shorter output filename
PJD  7 Apr 2022     - Updated readData to correct output args on error
                     4512180 CMIP6 /p/css03/esgf_publish/CMIP6/ScenarioMIP/EC-Earth-Consortium/EC-Earth3/ssp245/r3i1p1f1/SImon/siu/gn/v20210517/siu_SImon_EC-Earth3_ssp245_r3i1p1f1_gn_203301-203312.nc - Caught unexpected error: <class 'ValueError'>
PJD  7 Apr 2022     - Converted badFileList to cmip[dict] - persist error logs through restarts
PJD  7 Apr 2022     - Updated readData errX and errC to wash error types class -> str
PJD  8 Apr 2022     - Correct type DRSError variable error filePath -> filePath.path
                     578998 CMIP6 /p/css03/esgf_publish/CMIP6/HighResMIP/CNRM-CERFACS/CNRM-CM6-1-HR/highresSST-present/r1i1p1f2/Amon/ta/gr/v20190311/ta_Amon_CNRM-CM6-1-HR_highresSST-present_r1i1p1f2_gr_199001-199912.nc - Caught unexpected error: <class 'TypeError'>
PJD  9 Apr 2022     - Updated 'DRSError variable error' to list [file, error] to match other error formats
PJD  3 May 2022     - Added input4MIPs, test (and scatch) to CMIP6 subdir exclusion list
PJD  9 May 2022     - Added cdms2.error.CDMSError to readData function
                     249xxxxx CMIP6 /p/css03/esgf_publish/CMIP6/FAFMIP/MPI-M/MPI-ESM1-2-LR/faf-passiveheat/r1i1p1f1/Omon/epcalc100/gn/v20210901/epcalc100_Omon_MPI-ESM1-2-LR_faf-passiveheat_r1i1p1f1_gn_187001-188912.nc
PJD 12 May 2022     - Added "creation_date", "forcing" (CM5: HadGEM2-CC) and "history" globalAtt to getGlobalAtts (good for CMIP3, 5, and 6 timestamp harvest)

                     TODO: deal with multiple restart_ entries, use append to add info if it already exists
                     TODO: grid_info also needs to have realms - ala nominal_resolution
                     TODO: update to use joblib, parallel calls, caught with sqlite database for concurrent reads
                     TODO: update getDrs and getGlobalAtts for CMIP5 and CMIP3
                     
                     
22706354 /p/css03/esgf_publish/CMIP6/LUMIP/MPI-M/MPI-ESM1-2-LR/land-hist-altLu2/r1i1p1f1/Amon/tasmax/gn/v20190815/tasmax_Amon_MPI-ESM1-2-LR_land-hist-altLu2_r1i1p1f1_gn_193001-194912.nc
xarray load complete
tmp
{'lat': 'len: (96,) first: -88.57216851400727 last: 88.57216851400727', 'lon': 'len: (192,) first: 0.0 last: 358.125', 'height': 'len: x first: x last: x units: x'}
Key: nominal_resolution,
Value 1: {'aerosol': '', 'atmos': '250 km', 'atmosChem': '', 'land': '250 km', 'landIce': '', 'ocean': '', 'ocnBgchem': '', 'seaIce': ''},
Value 2: {'aerosol': '', 'atmos': '250 km', 'atmosChem': '', 'land': '', 'landIce': '', 'ocean': '', 'ocnBgchem': '', 'seaIce': ''}
cnt: 22706354 time: 000.138
cnt: 22706355 time: 000.000
cnt: 22706356 time: 000.000
cnt: 22706357 time: 000.000
cnt: 22706358 time: 000.000
cnt: 22706359 time: 000.000
cnt: 22706360 time: 000.000
cnt: 22706361 time: 000.000
cnt: 22706362 time: 000.000
22706363 /p/css03/esgf_publish/CMIP6/input4MIPs/UofMD/UofMD-landState-MAGPIE-ssp585-2-1-f/yr/multiple-transitions/gn/v20171019/multiple-transitions_input4MIPs_landState_ScenarioMIP_UofMD-MAGPIE-ssp585-2-1-f_gn_2015-2100.nc
Caught unexpected error: <class 'IndexError'>
                     

@author: durack1
"""

# %% imports
import argparse

import cdms2 as cdm
import datetime
import json
import numpy as np
import os
import pdb
import subprocess
import sys
import time
from os import scandir
from xcdat import open_dataset

# %% function defs


class numpyEncoder(json.JSONEncoder):
    """
    After https://stackoverflow.com/questions/50916422/python-typeerror-object-of-type-int64-is-not-json-serializable
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(numpyEncoder, self).default(obj)


def alertError(count, filePath, key2):
    """
    alertError()

    Sends an email alerting that a condition has been reached

    Based on:
        https://realpython.com/python-send-email/#sending-your-plain-text-email
        https://stackoverflow.com/questions/28328222/smtplib-of-python-not-working

    """
    # pdb.set_trace()
    import smtplib

    smtp_server = "nospam.llnl.gov"
    sender_email = "error@durack1"
    receivers_email = ["pauldurack@gmail.com", "pauldurack@llnl.gov"]
    to = ", ".join(receivers_email)
    subject = "extractLicenseContact.py error"
    body = "This message is sent from Python"
    body = "count   : {}\nfilePath: {}\nkey2    : {}\n\n{}".format(
        count, filePath, key2, body
    )
    # print("body:")
    # print(body)
    message = "Subject: {}\n\n{}".format(subject, body)
    # print("message:")
    # print(message)
    # pdb.set_trace()
    try:
        with smtplib.SMTP(smtp_server) as server:
            server.sendmail(sender_email, to, message)
    except (ConnectionResetError):
        print("")
        print("nospam.llnl.gov blocked connection")
        print("")


def compareDicts(dict1, dict2, count, filePath):
    """
    compareDicts(dict1, dict2, count)

    Compares entries in two dictionaries using key:value lookups, and returns
    inconsistencies

    Based on:
        https://stackoverflow.com/questions/27302694/comparing-two-dictionaries-in-python-by-identifying-sets-with-same-key-but-diffe
    """
    # create lookup variant_label consistent information
    chkGlobalAtts = [
        "activity_id",
        "branch_method",
        "branch_time_in_child",
        "branch_time_in_parent",
        "contact",
        "experiment_id",
        "forcing_index",
        "further_info_url",
        "initialization_index",
        "institution_id",
        "license",
        "mip_era",
        "nominal_resolution",
        "parent_activity_id",
        "parent_experiment_id",
        "parent_mip_era",
        "parent_source_id",
        "parent_time_units",
        "parent_variant_label",
        "physics_index",
        "realization_index",
        "source_id",
        "variant_label",
        "version",
        "cmor_version",
        "license",
    ]
    # pdb.set_trace()
    sharedKeys = set(dict1.keys()).intersection(dict2.keys())
    for key in sharedKeys:
        if dict1[key] != dict2[key] and key in chkGlobalAtts:
            print(
                "Key: {},\nValue 1: {},\nValue 2: {}".format(
                    key, dict1[key], dict2[key]
                )
            )
            # 25509 /p/css03/esgf_publish/CMIP6/VolMIP/CCCma/CanESM5/volc-long-eq/r29i1p2f1/Omon/epcalc100/gn/v20190429/epcalc100_Omon_CanESM5_volc-long-eq_r29i1p2f1_gn_181504-187003.nc
            # 25510 /p/css03/esgf_publish/CMIP6/VolMIP/CCCma/CanESM5/volc-long-eq/r29i1p2f1/Omon/tos/gn/v20190429/tos_Omon_CanESM5_volc-long-eq_r29i1p2f1_gn_181504-187003.nc
            # set(globalAtts).difference(chkGlobalAtts)
            # {'frequency', 'realm', 'table_id', 'tracking_id', 'variable_id'}
            key1 = ".".join([dict1["table_id"], dict1["variable_id"]])
            key2 = ".".join([dict2["table_id"], dict2["variable_id"]])
            tmp1 = dict1[key]  # value for dict1
            tmp2 = dict2[key]  # value for dict2
            # check if value already logged

            # convert block below to dealWithDuplicateEntry function
            # if any([True for k,v in word_freq.items() if v == value]):
            # deal with nominal_resolution nested dictionary
            if key == "nominal_resolution":
                # extract nominal_resolution keys
                dict1Realm = tmp1[dict1["realm"]]
                dict2Realm = dict2["realm"]
                # check for match, if no match write
                if dict1Realm != dict2Realm:
                    tmp1[dict2Realm] = tmp2[dict2Realm]
                # if match, create dictionary and append
                elif dict1Realm == dict2Realm and not isinstance(dict1Realm, dict):
                    val1 = tmp1[dict1Realm]
                    tmp1[dict1Realm] = {}
                    tmp1[dict1Realm][key1] = val1  # updated from "original"
                    tmp1[dict1Realm][key2] = tmp2[dict2Realm]
                # if match, and dictionary, deal with secondary case, append only
                elif dict1Realm == dict2Realm and isinstance(dict1Realm, dict):
                    tmp1[dict1Realm][key2] = tmp2[dict2Realm]
                # assign new tmp1 dictionary to key
                dict1[key] = tmp1
            # deal with all other entries
            else:
                print("new key:", key)
                # if tmp1 != tmp2 and not dictionary
                if not isinstance(tmp1, dict):
                    # catch new entry in new dictionary
                    print("catch new entry in new dictionary")
                    val1 = str(washTypes(tmp1))
                    tmp1 = {}
                    tmp1[val1] = {}
                    tmp1[val1]["keys"] = []
                    tmp1[val1]["keys"].append(key1)
                    tmp1[val1]["count"] = 1
                    val2 = str(washTypes(tmp2))
                    tmp1[val2] = {}
                    tmp1[val2]["keys"] = []
                    tmp1[val2]["keys"].append(key2)
                    tmp1[val2]["count"] = 1
                elif isinstance(tmp1, dict):
                    print("catch new entry in existing dictionary")
                    # if key already exists append
                    val2 = str(washTypes(tmp2))
                    if tmp2 in list(tmp1.keys()):
                        # print("tmp2 == key"); pdb.set_trace()
                        tmp1[val2]["keys"].append(key2)
                        tmp1[val2]["count"] = tmp1[tmp2]["count"] + 1
                    # if key doesn't exist add new
                    else:
                        # print("else"); pdb.set_trace()
                        tmp1[val2] = {}
                        tmp1[val2]["keys"] = [key2]
                        tmp1[val2]["count"] = 1
                else:
                    # catch case unmatched
                    print("catch case unmatched")
                    pdb.set_trace()
                # assign new tmp1 dictionary to key
                dict1[key] = tmp1
            update = True
            # alertError(count, filePath, key2)

        else:
            update = False

    return update, dict1


def getAxes(lev, levUnits, lat, lon):
    """
    getAxes(lev, levUnits, lat, lon)

    Extracts grid info dependent on input
    """
    # preallocate
    latLen, lat0, latN = ["x" for _ in range(3)]
    lonLen, lon0, lonN = ["x" for _ in range(3)]
    heightLen, height0, heightN, heightUnit = ["x" for _ in range(4)]
    # create placeholder grid_info dictionary
    tmp = {}
    tmp["lat"] = " ".join(["len:", latLen, "first:", lat0, "last:", latN])
    tmp["lon"] = " ".join(["len:", lonLen, "first:", lon0, "last:", lonN])
    tmp["height"] = " ".join(
        [
            "len:",
            heightLen,
            "first:",
            height0,
            "last:",
            heightN,
            "units:",
            heightUnit,
        ]
    )

    # create strings
    if lat is not None:
        latLen = str(lat.shape)
        lat0 = str(np.min(np.min(lat)))
        latN = str(np.max(np.max(lat)))
    if lon is not None:
        lonLen = str(lon.shape)
        lon0 = str(np.min(np.min(lon)))
        lonN = str(np.max(np.max(lon)))
    if (lev is not None) and (lev.shape != ()):
        heightLen = str(lev.shape)
        height0 = str(lev[0])
        heightN = str(lev[-1])
        if levUnits is not None:
            heightUnit = levUnits

    # update grid_info dictionary
    tmp = {}
    tmp["lat"] = " ".join(["len:", latLen, "first:", lat0, "last:", latN])
    tmp["lon"] = " ".join(["len:", lonLen, "first:", lon0, "last:", lonN])
    tmp["height"] = " ".join(
        [
            "len:",
            heightLen,
            "first:",
            height0,
            "last:",
            heightN,
            "units:",
            heightUnit,
        ]
    )
    print("tmp")
    print(tmp)

    return tmp


def getDrs(path):
    """
    getDrs(path)

    Extracts DRS components following CMIP6 specs
    """
    pathBits = path.split("/")
    cmipInd = pathBits.index("CMIP6")
    # CMIP6 DRS
    # /p/css03/esgf_publish/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r1i1p1f1/Omon/msftmz/gn/v20191115/msftmz
    actId = pathBits[cmipInd + 1]
    expId = pathBits[cmipInd + 4]
    instId = pathBits[cmipInd + 2]
    ripfId = pathBits[cmipInd + 5]
    srcId = pathBits[cmipInd + 3]
    gridId = pathBits[cmipInd + 8]
    verId = pathBits[cmipInd + 9]

    # validate activity_id is correct
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
    if actId not in activity_id.keys():
        print("invalid activity_id:", actId, "exiting")
        return ""
    else:
        return ".".join(["CMIP6", instId, srcId, actId, expId, ripfId, gridId, verId])


def getGlobalAtts(globalAttDic, calendar, lon, lat, lev, levUnits):
    """
    getGlobalAtts(globalAttDic, calendar, lev, levUnits, lat, lon)

    Attempts to extract a list of global attributes from a netcdf file and returns
    this as a dictionary key: value pairs
    """
    # define search facets
    globalAtts = [
        "activity_id",
        "branch_method",
        "branch_time_in_child",
        "branch_time_in_parent",
        "contact",
        "experiment_id",
        "forcing_index",
        "frequency",
        "further_info_url",
        "initialization_index",
        "institution_id",
        "license",
        "mip_era",
        "nominal_resolution",
        "parent_activity_id",
        "parent_experiment_id",
        "parent_mip_era",
        "parent_source_id",
        "parent_time_units",
        "parent_variant_label",
        "physics_index",
        "realization_index",
        "realm",
        "source_id",
        "table_id",
        "variable_id",
        "variant_label",
        "version",
        "cmor_version",
        "tracking_id",
        "license",
        "history",
        "creation_date",
        "forcing",
    ]
    realms = {
        "aerosol": "Aerosol",
        "atmos": "Atmosphere",
        "atmosChem": "Atmospheric Chemistry",
        "land": "Land Surface",
        "landIce": "Land Ice",
        "ocean": "Ocean",
        "ocnBgchem": "Ocean Biogeochemistry",
        "seaIce": "Sea Ice",
    }

    tmp = {}
    # iterate through global attribute dictionary
    for cnt, globalAtt in enumerate(globalAttDic):
        try:
            val = globalAttDic[globalAtt]
            # catch case of numpy branch info
            if isinstance(val, np.ndarray) and len(val) == 1:
                val = str(val.tolist()[0])
        except Exception as error:
            print("getGlobalAtts: No entry:", globalAtt, error)
            val = ""
        tmp[globalAtt] = val
    # assign nominal resolution per realm
    val = tmp["nominal_resolution"]
    tmp["nominal_resolution"] = {}
    for realmVal in realms:
        tmp["nominal_resolution"][realmVal] = ""
    tmp["nominal_resolution"][tmp["realm"]] = val

    # get grid_info
    gridInfo = getAxes(lev, levUnits, lat, lon)
    if gridInfo != None:
        tmp["grid_info"] = gridInfo
    else:
        tmp["grid_info"] = ""

    # get calendar
    if calendar != None:
        tmp["calendar"] = calendar
    else:
        tmp["calendar"] = ""

    # add list of non-queried globalAtts
    ###tmp["||_unvalidated"] = list(set(fH.attributes).difference(globalAtts))
    tmp["||_unvalidated"] = list(set(globalAttDic).difference(globalAtts))

    return tmp


def getVarName(varList):
    excludeVars = [
        "a",
        "a_bnds",
        "alt16",
        "alt16_bnds",
        "alt16_bounds",
        "alt40",
        "alt40_bnds",
        "alt40_bounds",
        "ap",
        "ap_bnds",
        "area",
        "average_DT",
        "average_T1",
        "average_T2",
        "b",
        "b_bnds",
        "basin",
        "bnds",
        "bounds_lat",
        "bounds_latitude",
        "bounds_lon",
        "bounds_longitude",
        "bounds_nav_lat",
        "bounds_nav_lon",
        "climatology_bnds",
        "climatology_bounds",
        "d2",
        "dbze",
        "dbze_bnds",
        "dbze_bounds",
        "depth",
        "depth_c",
        "depth_bnds",
        "depth_bounds",
        "depth_layer",
        "effectRadIc",
        "effectRadIc_bnds",
        "effectRadIc_bounds",
        "effectRadLi",
        "effectRadLi_bnds",
        "effectRadLi_bounds",
        "eta",
        "geolat",
        "GEOLAT",
        "geolon",
        "GEOLON",
        "iceband_bnds",
        "iceband_bounds",
        "landuse",
        "lat",
        "lat_bnds",
        "lat_bounds",
        "latitude",
        "lev",
        "lev_bnds",
        "lev_bounds",
        "lev_partial_bnds",
        "lev_partial_bounds",
        "lev7c_bnds",
        "lev7c_bounds",
        "lon",
        "lon_bnds",
        "lon_bounds",
        "longitude",
        "height",
        "height_bnds",
        "height_bounds",
        "hist_interval",
        "nav_lat",
        "nav_lon",
        "nsigma",
        "olevel_bnds",
        "olevel_bounds",
        "orog",
        "p0",
        "p500",
        "p700",
        "p850",
        "pfttype",
        "plev",
        "plev_bnds",
        "plev_bounds",
        "plev7_bnds",
        "plev7_bounds",
        "plev7c_bnds",
        "plev7c_bounds",
        "ps",
        "ptop",
        "region",
        "rlat",
        "rlat_bnds",
        "rlat_bounds",
        "rlon",
        "rlon_bnds",
        "rlon_bounds",
        "scatratio",
        "scatratio_bnds",
        "scatratio_bounds",
        "sdepth",
        "sdepth_bnds",
        "sdepth_bounds",
        "sector",
        "sigma",
        "sigma_bnds",
        "strait",
        "strlen",
        "sza_bnds",
        "sza_bounds",
        "tau_bnds",
        "tau_bounds",
        "time_bnds",
        "time_bounds",
        "type",
        "vertices_latitude",
        "vertices_longitude",
        "wavelength",
        "y",
        "y_bnds",
        "y_bounds",
        "ygre",
        "x",
        "x_bnds",
        "x_bounds",
        "xgre",
        "zlev",
        "zlev_bnds",
    ]

    # deal with variables - for cmip5/3
    varNames = []
    for a, b in enumerate(varList):
        varNames.append(b)
    # deal with basin var
    if all(x in filePath for x in ["/basin/", "/basin"]):
        excludeVars.remove("basin")
    # deal with orog var
    if all(x in filePath for x in ["/orog/", "/orog"]):
        excludeVars.remove("orog")
    # deal with ps var
    if all(x in filePath for x in ["/ps/", "/ps"]):
        excludeVars.remove("ps")
    varName = "".join(set(varNames) - set(excludeVars))
    # compare variable_id with varName
    print("variable_id:", tmp["variable_id"], "varName:", varName)
    if tmp["variable_id"] is None:
        # if variable_id not set, use varName
        var = varName

    return var


def readData(filePath, varName):
    """
    read netcdf file using xarray or cdms2 and return file and coordinate
    attributes

    good /p/css03/esgf_publish/CMIP6/PMIP/NCAR/CESM2/midPliocene-eoi400/r1i1p1f1/SImon/sistremax/gn/v20200110/sistremax_SImon_CESM2_midPliocene-eoi400_r1i1p1f1_gn_115101-120012.nc
    good /p/css03/esgf_publish/CMIP6/VolMIP/MIROC/MIROC-ES2L/volc-pinatubo-strat/r3i1p1f2/Omon/zooc/gn/v20210118/zooc_Omon_MIROC-ES2L_volc-pinatubo-strat_r3i1p1f2_gn_185006-185312.nc
    bad /p/css03/esgf_publish/CMIP6/CMIP/NCC/NorESM2-MM/historical/r3i1p1f1/SImon/siarean/gn/v20200702/siarean_SImon_NorESM2-MM_historical_r3i1p1f1_gn_186001-186912.nc
    good sites /p/css03/esgf_publish/CMIP6/RFMIP/MOHC/HadGEM3-GC31-LL/rad-irf/r1i1p1f2/Efx/rld/gn/v20190605/rld_Efx_HadGEM3-GC31-LL_rad-irf_r1i1p1f2_gn.nc
    good no Z /p/css03/esgf_publish/CMIP6/ISMIP6/NCAR/CESM2/ssp585-withism/r1i1p1f1/ImonGre/hfls/gn/v20191120/hfls_ImonGre_CESM2_ssp585-withism_r1i1p1f1_gn_206501-209912.nc
    bad /p/css03/esgf_publish/CMIP6/ISMIP6/NCAR/CESM2/ssp585-withism/r1i1p1f1/Omon/vo/gn/v20210513/vo_Omon_CESM2_ssp585-withism_r1i1p1f1_gn_215001-219912.nc cdms unboundLocalError, TypeError, ValueError
    bad /p/css03/esgf_publish/CMIP6/ISMIP6/NASA-GISS/GISS-E2-1-G/1pctCO2-4xext/r1i1p1f1/Emon/cSoilAbove1m/gn/v20181022/cSoilAbove1m_Emon_GISS-E2-1-G_1pctCO2-4xext_r1i1p1f1_gn_192001-195012.nc 5184 CMIP6 lev.shape == ()
    bad /p/css03/esgf_publish/CMIP6/PMIP/CAS/FGOALS-g3/lig127k/r1i1p1f1/Amon/phalf/gn/v20191030/phalf_Amon_FGOALS-g3_lig127k_r1i1p1f1_gn_076001-076912-clim.nc 122915 KeyError no T axis
    bad /p/css03/esgf_publish/CMIP6/PMIP/IPSL/IPSL-CM6A-LR/midPliocene-eoi400/r1i1p1f1/AERmonZ/o3/grz/v20190118/o3_AERmonZ_IPSL-CM6A-LR_midPliocene-eoi400_r1i1p1f1_grz_185001-204912.nc Error: 'units'
    bad /p/css03/esgf_publish/CMIP6/HighResMIP/CAS/FGOALS-f3-H/highres-future/r1i1p1f1/Omon/tosga/gn/v20201225/tosga_Omon_FGOALS-f3-H_highres-future_r1i1p1f1_gn_201501-205012.nc 669991 CMIP6 NetCDF: Unknown file format
    bad /p/css03/esgf_publish/CMIP6/HighResMIP/MOHC/HadGEM3-GC31-HM/highresSST-present/r1i1p1f1/6hrPlevPt/wbptemp7h/gn/v20170831/wbptemp_6hrPlevPt_HadGEM3-GC31-HM_highresSST-present_r1i1p1f1_gn_199307010000-199309301800.nc 717815 CMIP6 Error: ufunc 'subtract' cannot use operands with types dtype('O') and dtype('<m8[ns]')
    bad /p/css03/esgf_publish/CMIP6/ScenarioMIP/EC-Earth-Consortium/EC-Earth3/ssp245/r3i1p1f1/SImon/siu/gn/v20210517/siu_SImon_EC-Earth3_ssp245_r3i1p1f1_gn_203301-203312.nc 4512180 Caught unexpected error: <class 'RuntimeError'>
    timeProblem /p/css03/esgf_publish/CMIP6/ScenarioMIP/IPSL/IPSL-CM6A-LR/ssp534-over/r1i1p1f1/Omon/vmo/gn/v20190909/vmo_Omon_IPSL-CM6A-LR_ssp534-over_r1i1p1f1_gn_220101-230012.nc 8794418 CMIP6 lib/python3.10/site-packages/xarray/coding/times.py:673: SerializationWarning: Unable to decode time axis into full numpy.datetime64 objects, continuing using cftime.datetime objects instead, reason: dates out of range
    timeProblem /p/css03/esgf_publish/CMIP6/ScenarioMIP/IPSL/IPSL-CM6A-LR/ssp585/r1i1p1f1/SIday/siconc/gn/v20190903/siconc_SIday_IPSL-CM6A-LR_ssp585_r1i1p1f1_gn_21010101-23001231.nc 8797180
    https://stackoverflow.com/questions/17322208/multiple-try-codes-in-one-block

    """
    # preallocate error codes
    errX, errC = [None for _ in range(2)]
    # read data - validate with ncdump that valid data, then try open and read
    cmd = subprocess.Popen(
        ["ncdump", "-h", filePath],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, errors = cmd.communicate()
    cmd.wait()
    if errors == b'':
        # try xarray read
        try:
            fH = open_dataset(filePath)
            # Extract stuff
            globalAttDic = fH.attrs
            calendar, lev, levUnits, lat, lon = [None for _ in range(5)]
            axisList = fH.cf.axes.keys()
            if "T" in axisList:
                calendar = fH.time.encoding["calendar"]
            if "Z" in axisList:
                lev = fH[fH.cf.axes["Z"][0]].data
                if "units" in fH[[fH.cf.axes["Z"][0]]].attrs.keys():
                    levUnits = fH[[fH.cf.axes["Z"][0]]].units
            #print("xc: next Y")
            # pdb.set_trace()
            if "Y" in axisList:
                lat = fH[fH.cf.axes["Y"][0]].data
            if "X" in axisList:
                lon = fH[fH.cf.axes["X"][0]].data
            varList = []
            for a, b in enumerate(fH.data_vars.keys()):
                varList.append(b)
            fH.close()
            print("xarray load complete")
        except (
            np.core._exceptions._UFuncBinaryResolutionError,
            np.core._exceptions.UFuncTypeError,
            AttributeError,
            KeyError,
            RuntimeError,
            UnboundLocalError,
            ValueError,
        ) as error:
            print("")
            print("readData: badFile xarray:", filePath)
            print("Error:", error)
            print("")
            errX = ['xarray', filePath, str(error)]
            # try cdms2
            try:
                fH = cdm.open(filePath)
                # Extract stuff
                globalAttDic = fH.attributes
                calendar, lev, levUnits, lat, lon = [None for _ in range(5)]
                d = fH(varName, time=slice(0, 1))
                if d.getTime() is not None:
                    calendar = d.getTime().calendar
                if d.getLevel() is not None:
                    lev = d.getLevel().getData()
                    if "units" in d.getLevel().attributes:
                        levUnits = d.getLevel().units
                #print("xcd next lat/lon")
                # pdb.set_trace()
                try:
                    if d.getLatitude() is not None:
                        lat = d.getLatitude()._data
                    if d.getLongitude() is not None:
                        lon = d.getLongitude()._data
                except:
                    # 122916 CMIP6 '/p/css03/esgf_publish/CMIP6/PMIP/CAS/FGOALS-g3/lig127k/r1i1p1f1/Amon/phalf/gn/v20191030/phalf_Amon_FGOALS-g3_lig127k_r1i1p1f1_gn_076001-076912-clim.nc'
                    # 452910 CMIP6 '/p/css03/esgf_publish/CMIP6/PMIP/IPSL/IPSL-CM6A-LR/midPliocene-eoi400/r1i1p1f1/AERmonZ/o3/grz/v20190118/o3_AERmonZ_IPSL-CM6A-LR_midPliocene-eoi400_r1i1p1f1_grz_185001-204912.nc'
                    if d.getLatitude() is not None:
                        lat = d.getLatitude()._data_
                    if d.getLongitude() is not None:
                        lon = d.getLongitude()._data_
                varList = []
                for a, b in enumerate(fH.variables.keys()):
                    varList.append(b)
                fH.close()
                print('cdms2 load complete')
            except (
                cdm.error.CDMSError,
                OSError,
                SystemError,
                TypeError,
                UnboundLocalError,
                UnicodeDecodeError,
                ValueError,
            ) as error:
                print("")
                print("readData: badFile cdms2:", filePath)
                print("Error:", error)
                print("")
                errC = ['cdms2', filePath, str(error)]
        #print("bomb twice")
        # pdb.set_trace()
        # return file attributes
        if errX == None:
            return globalAttDic, calendar, lev, levUnits, lat, lon, varList, errX, errC
        elif errC == None:
            return globalAttDic, calendar, lev, levUnits, lat, lon, varList, errX, errC
        elif errX != None and errC != None:
            return errX, errC, None, None, None, None, None, None, None
        elif errX != None:
            return errX, None, None, None, None, None, None, None, None
        elif errC != None:
            return errC, None, None, None, None, None, None, None, None
    else:
        print("readData: badFile ncdump error:", filePath, errors)
        return [filePath, str(errors)], None, None, None, None, None, None, errX, errC,


def scantree(path):
    """
    scantree(path)

    This is an iterator method that recursively scans for directories that meet the
    following criteria:
        1. The directory has no sub-directories
        2. The directory contains files
    It is based on:
        https://stackoverflow.com/questions/33135038/how-do-i-use-os-scandir-to-return-direntry-objects-recursively-on-a-directory
    """

    for entry in scandir(path):
        # wrap function to catch permissionError
        try:
            # yield directory if there are any files in it
            if entry.is_dir(follow_symlinks=False):
                yield from scantree(entry.path)
            else:
                yield entry
        except (PermissionError) as error:
            print("scandir: Error, skipping..", error)
            continue


def walkWashDicList(dicOrList):
    """

    """
    # work on dictionaries
    if isinstance(dicOrList, dict):
        for dicKey1, dicVal1 in dicOrList.items():
            if isinstance(dicVal1, dict):
                for dicKey2, dicVal2 in dicVal1.items():
                    if isinstance(dicVal2, dict):
                        for dicKey3, dicVal3 in dicVal2.items():
                            if isinstance(dicVal3, dict):
                                for dicKey4, dicVal4 in dicVal3.items():
                                    if isinstance(dicVal4, dict):
                                        for dicKey5, dicVal5 in dicVal4.items():
                                            dicOrList[dicKey1][dicKey2][dicKey3][dicKey4][dicKey5] = washTypes(
                                                dicVal5)
                                    else:
                                        dicOrList[dicKey1][dicKey2][dicKey3][dicKey4] = washTypes(
                                            dicVal4)
                            else:
                                dicOrList[dicKey1][dicKey2][dicKey3] = washTypes(
                                    dicVal3)
                    else:
                        dicOrList[dicKey1][dicKey2] = washTypes(dicVal2)
            else:
                dicOrList[dicKey1] = washTypes(dicVal1)

    # work on lists
    elif isinstance(dicOrList, list):
        if any(isinstance(i1, list) for i1 in dicOrList):
            print("walkWashDicList 1")
            pdb.set_trace()
            for cnt1, val1 in enumerate(dicOrList):
                if any(isinstance(i2, list) for i2 in val1):
                    print("walkWashDicList 2")
                    pdb.set_trace()
                    for cnt2, val2 in enumerate(val1):
                        if any(isinstance(i3, list) for i3 in val2):
                            print("walkWashDicList 3")
                            pdb.set_trace()
                            for cnt3, val3 in enumerate(val2):
                                dicOrList[cnt1][cnt2][cnt3] = washTypes(val3)
                        else:
                            dicOrList[cnt1][cnt2] = washTypes(val2)
                else:
                    dicOrList[cnt1] = washTypes(val1)
        else:
            dicOrList = washTypes(dicOrList)

    return dicOrList


def washTypes(val):
    """

    """
    if isinstance(val, np.integer):
        val = int(val)
    if isinstance(val, np.floating):
        val = str(float(val))
    if isinstance(val, np.ndarray):
        val = val.tolist()

    return val


def writeJson(dic, testPath, count, endTime, fileNameAdd):
    """
    writeJson(dic, testPath, count, endTime)

    Takes dictionary, path, count and endTime and writes out to json file
    """
    # get time info
    timeNow = datetime.datetime.now()
    timeFormatDir = timeNow.strftime("%y%m%d")
    cmip["version_metadata"]["end_time  "] = endTime
    # get path
    pathInfo = testPath.replace("/p/css03/esgf_publish/", "")
    if pathInfo == "CMIP6/":
        pathInfo = pathInfo.replace("/", "")
    else:
        pathInfo = pathInfo.replace("/", "-")
    # get count
    cmip["version_metadata"]["file_processed_count"] = str(count)

    # Write output
    if fileNameAdd:
        outFile = "_".join(
            [timeFormatDir, pathInfo, "metaData", fileNameAdd])
        outFile = "".join([outFile, ".json"])
    else:
        outFile = "_".join([timeFormatDir, pathInfo, "metaData.json"])
    if os.path.exists(outFile):
        os.remove(outFile)
    print("")
    print("writing:")
    print("")
    fH = open(outFile, "w")
    json.dump(
        cmip,
        fH,
        ensure_ascii=True,
        sort_keys=True,
        indent=4,
        separators=(",", ":"),
        cls=numpyEncoder,
    )
    fH.close()


# %% define path
hostPath = "/p/css03/esgf_publish/CMIP6/"
testPath = (
    # "/p/css03/esgf_publish/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r1i1p1f1/Omon"
    # "/p/css03/esgf_publish/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r1i1p1f1"
    # "/p/css03/esgf_publish/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical"
    # "/p/css03/esgf_publish/CMIP6/PMIP/CAS/FGOALS-f3-L/lig127k/r1i1p1f1/SImon/"  # i, j index checks
    # "/p/css03/esgf_publish/CMIP6/CMIP"
    # "/p/css03/esgf_publish/CMIP6/ScenarioMIP"
    # "/p/css03/esgf_publish/CMIP6/HighResMIP/CAS/FGOALS-f3-H/highres-future/r1i1p1f1/Omon/tosga/gn/v20201225/"
    # "/p/css03/esgf_publish/CMIP6/HighResMIP/CAS/FGOALS-f3-H/highres-future"
    # "/p/css03/esgf_publish/CMIP6/ScenarioMIP/EC-Earth-Consortium/EC-Earth3/ssp245/r3i1p1f1/SImon"
    # "/p/css03/esgf_publish/CMIP6/ScenarioMIP/EC-Earth-Consortium/EC-Earth3/ssp245/r3i1p1f1"
    "/p/css03/esgf_publish/CMIP6"
)

# define bad files
cdmsBadFiles = ()
cdmsBadFiles2 = (
    "badFilesAreHere",
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r3i1p1f2/Eday/rivo/gn/v20181012/rivo_Eday_CNRM-CM6-1_abrupt-4xCO2_r3i1p1f2_gn_18500501-1859123.nc",
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r3i1p1f2/Eday/rivo/gn/v20181012/rivo_Eday_CNRM-CM6-1_abrupt-4xCO2_r3i1p1f2_gn_18500501-18591231.nc",
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r3i1p1f2/Emon/wtd/gn/v20181012/wtd_Emon_CNRM-CM6-1_abrupt-4xCO2_r3i1p1f2_gn_185005-185912.nc",
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r3i1p1f2/fx/areacellr/gn/v20181012/areacellr_fx_CNRM-CM6-1_abrupt-4xCO2_r3i1p1f2_gn.nc",  # 13681 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r4i1p1f2/Eday/rivo/gn/v20181012/rivo_Eday_CNRM-CM6-1_abrupt-4xCO2_r4i1p1f2_gn_18500701-18591231.nc",  # 13874 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r4i1p1f2/Emon/wtd/gn/v20181012/wtd_Emon_CNRM-CM6-1_abrupt-4xCO2_r4i1p1f2_gn_185007-185912.nc",  # 13966 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r4i1p1f2/fx/areacellr/gn/v20181012/areacellr_fx_CNRM-CM6-1_abrupt-4xCO2_r4i1p1f2_gn.nc",  # 13967 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r1i1p1f2/Eday/rivo/gn/v20180705/rivo_Eday_CNRM-CM6-1_abrupt-4xCO2_r1i1p1f2_gn_19500101-19991231.nc",  # 14307 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r1i1p1f2/Eday/rivo/gn/v20180705/rivo_Eday_CNRM-CM6-1_abrupt-4xCO2_r1i1p1f2_gn_19500101-19991231.nc",  # 14308 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r1i1p1f2/Emon/wtd/gn/v20180705/wtd_Emon_CNRM-CM6-1_abrupt-4xCO2_r1i1p1f2_gn_185001-199912.nc",  # 14476 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r1i1p1f2/fx/areacellr/gn/v20180705/areacellr_fx_CNRM-CM6-1_abrupt-4xCO2_r1i1p1f2_gn.nc",  # 14477 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r5i1p1f2/Eday/rivo/gn/v20181012/rivo_Eday_CNRM-CM6-1_abrupt-4xCO2_r5i1p1f2_gn_18500901-18591231.nc",  # 14824 CMIP
    # 14916 CMIP + more try/except added
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r5i1p1f2/Emon/wtd/gn/v20181012/wtd_Emon_CNRM-CM6-1_abrupt-4xCO2_r5i1p1f2_gn_185009-185912.nc",
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r5i1p1f2/fx/areacellr/gn/v20181012/areacellr_fx_CNRM-CM6-1_abrupt-4xCO2_r5i1p1f2_gn.nc",  # 14917 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/MOHC/HadGEM3-GC31-MM/historical/r1i1p1f3/CFday/clivi/gn/v20191207/clivi_CFday_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_19200101-19241230.nc",  # 513159 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/NCC/NorESM2-MM/historical/r3i1p1f1/SImon/siarean/gn/v20200702/siarean_SImon_NorESM2-MM_historical_r3i1p1f1_gn_186001-186912.nc",  # 7176050 CMIP, netcdf fail
    # 47148 CMIP, cdms.open fail utf-8 decode
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/amip/r1i1p1f2/Eday/rivo/gn/v20181203/rivo_Eday_CNRM-CM6-1_amip_r1i1p1f2_gn_19790101-20141231.nc",
    # 14308 CMIP, cdms open fail utf-8
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r1i1p1f2/Eday/rivo/gn/v20180705/rivo_Eday_CNRM-CM6-1_abrupt-4xCO2_r1i1p1f2_gn_19000101-19491231.nc",
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r1i1p1f2/Eday/rivo/gn/v20180705/rivo_Eday_CNRM-CM6-1_abrupt-4xCO2_r1i1p1f2_gn_18500101-18991231.nc",  # 14309 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r1i1p1f2/Eday/rivo/gn/v20180705/rivo_Eday_CNRM-CM6-1_abrupt-4xCO2_r1i1p1f2_gn_19500101-19991231.nc",  # Proactive
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r2i1p1f2/Eday/rivo/gn/v20181012/rivo_Eday_CNRM-CM6-1_abrupt-4xCO2_r2i1p1f2_gn_18500301-18591231.nc",  # 15108 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r2i1p1f2/Emon/wtd/gn/v20181012/wtd_Emon_CNRM-CM6-1_abrupt-4xCO2_r2i1p1f2_gn_185003-185912.nc",  # 15201 CMIP
    "/p/css03/esgf_publish/CMIP6/ScenarioMIP/CCCma/CanESM5/ssp126/r5i1p1f1/Omon/tauvo/gn/v20190306/tauvo_Omon_CanESM5_ssp126_r5i1p1f1_gn_201501-210012.nc",  # 527759 ScenarioMIP
    "/p/css03/esgf_publish/CMIP6/HighResMIP/CAS/FGOALS-f3-H/highres-future/r1i1p1f1/Omon/tosga/gn/v20201225/tosga_Omon_FGOALS-f3-H_highres-future_r1i1p1f1_gn_201501-205012.nc",  # 669356 CMIP6
    "/p/css03/esgf_publish/CMIP6/ScenarioMIP/MRI/MRI-ESM2-0/ssp119/r5i1p1f1/Emon/cldnci/gn/v20210907/cldnci_Emon_MRI-ESM2-0_ssp119_r5i1p1f1_gn_201501-210012.nc",  # 5543227 ScenarioMIP
    "/p/css03/esgf_publish/CMIP6/HighResMIP/CAS/FGOALS-f3-H/highres-future/r1i1p1f1/Omon/tosga/gn/v20201225/tosga_Omon_FGOALS-f3-H_highres-future_r1i1p1f1_gn_201501-205012.nc",  # 669xxx
    "/p/css03/esgf_publish/CMIP6/VolMIP/MIROC/MIROC-ES2L/volc-pinatubo-strat/r3i1p1f2/Omon/zooc/gn/v20210118/zooc_Omon_MIROC-ES2L_volc-pinatubo-strat_r3i1p1f2_gn_185006-185312.nc",  # CMIP6 42348, AttributeError
    # 102799 xarray numpy.core._exceptions._UFuncBinaryResolutionError
    "/p/css03/esgf_publish/CMIP6/PMIP/NCAR/CESM2/midPliocene-eoi400/r1i1p1f1/SImon/sistremax/gn/v20200110/sistremax_SImon_CESM2_midPliocene-eoi400_r1i1p1f1_gn_115101-120012.nc",
)

# %% loop over files and build index
parser = argparse.ArgumentParser(description="Process some CMIPx data")
parser.add_argument(
    "activityId", metavar="S", type=str, help="an activity_id to build the search from",
)
parser.add_argument(
    "fileNameAdd", nargs="?", default="", type=str, help="optional identifier to file testing",
)
parser.add_argument(
    "restartLog", nargs="?", default="", type=str, help="optional logfile to restart from",
)
parser.add_argument(
    "startInd", nargs="?", default=-1, type=int, help="optional index to start for loop",
)
args = parser.parse_args()
# Deal with MIP scan
if args.activityId in ["CMIP", "OMIP", "RFMIP", "ScenarioMIP"]:
    actId = args.activityId
elif args.activityId == "CMIP6":
    actId = ""
else:
    print("Invalid path, ", args.activityId, "exiting")
    sys.exit()
# Deal with fileNameAdd
if args.fileNameAdd != '':
    fileNameAdd = args.fileNameAdd
else:
    fileNameAdd = ''
# Deal with restartLog
startIndSet = False
restartLog = "blank"
if args.restartLog != "":
    restartLog = args.restartLog
    # test to see if file exists
    if os.path.exists(restartLog):
        # load json
        with open(restartLog) as f:
            cmip = json.load(f)
            startInd = int(cmip["version_metadata"]["file_processed_count"])
            fileNameAdd = ''.join(['restartedInd-', str(startInd)])
            startIndSet = True
if not startIndSet:
    # Deal with startInd
    if args.startInd != -1:
        startInd = args.startInd
    else:
        startInd = -1
print("actId:", actId)
print("restartLog:", restartLog)
print("startInd:", startInd)
print("fileNameAdd:", fileNameAdd)

# create testpath and reset startInd for testing
testPath = os.path.join(testPath, actId)
print("Processing testPath:", testPath)
###startInd = -1

# use iterator to start scan
# startTime = time.time()
# print('Create test path iterator')
# x = scantree(testPath)
# print('Iterator created, processing...')
# for fileCount, filePath in enumerate(x):
#     pass
# print('testPath:', testPath)
# print('fileCount:', fileCount)
# endTime = time.time()
# print('time taken:', "{:07.3f}".format(endTime - startTime))
# sys.exit()

# create dictionary to catch bad files
# badFileList = []  # convert to dictionary add to json
# wrap operation in try
try:
    x = scantree(testPath)
    if 'cmip' in locals():
        print('cmip dictionary loaded..')
        # reallocate to restart variables
        cmip["version_metadata"]["restart_index"] = startInd
        cmip["version_metadata"]["restart_start_time"] = cmip["version_metadata"]["start_time"]
        cmip["version_metadata"]["restart_testPath"] = cmip["version_metadata"]["testPath"]
        cmip["restart_badFileList"] = cmip["_badFileList"]
        # first run
        #cmip["_badFileList"] = {}
        # subsequent run
        cmip["_badFileList"] = cmip["_badFileList"]
        cmip["version_metadata"]["testPath"] = testPath
    else:
        cmip = {}
        cmip["version_metadata"] = {}
        cmip["version_metadata"]["author"] = "Paul J. Durack <durack1@llnl.gov>"
        cmip["version_metadata"]["institution_id"] = "PCMDI"
        cmip["version_metadata"]["testPath"] = testPath
        cmip["_badFileList"] = {}
    startTime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    cmip["version_metadata"]["start_time"] = startTime
    for cnt, filePath in enumerate(x):
        # catch case that scratch dir is encountered
        badDirs = ["/input4MIPs", "/scratch", "/test"]
        if any(x in filePath.path for x in badDirs):
            print("path invalid, skipping..")
            continue
        # start timer
        startTime = time.time()
        # debug start
        if cnt == "none":
            endTime = time.time()
            timeTaken = "{:07.3f}".format(endTime - startTime)
            # writeJson(cmip, testPath, cnt, timeTaken)
            # os.system("cp 220220_CMIP6-CMIP_metaData.json dupe.json")
            #print("catching dictionary, pre-crash")
            pdb.set_trace()
        if cnt < startInd:
            print(cnt, filePath.path)
            continue
        elif cnt == startInd:
            firstPath = "/".join(filePath.path.split("/")[0:-1])
        #    cmip = json.load(open("dupe.json"))
        # debug end
        # check for bad file - deprecated by try in getGlobalAtts
        # if filePath.path in cdmsBadFiles:
        #    print("bad file identified, skipping")
        #    continue  # skip file, proceed to next in loop
        # deal with multiple files - e.g. Omon
        if cnt == 0:
            firstPath = "/".join(filePath.path.split("/")[0:-1])
        if firstPath not in filePath.path:
            firstPath = "/".join(filePath.path.split("/")[0:-1])
            print(cnt, filePath.path)  # path and filename complete
            # build DRS institution_id.source_id.activity_id.experiment_id.variant_label.grid_label.version
            key = getDrs(filePath.path)
            pathBits = filePath.path.split("/")
            cmipInd = pathBits.index("CMIP6")
            varName = pathBits[cmipInd + 7]  # DRS
            varName2 = pathBits[-1].split('_')[0]  # filename
            if varName != varName2:
                #badFileList.append(['DRSError variable error', filePath])
                cmip["_badFileList"][str(cnt)] = [
                    filePath.path, 'DRSError variable error']
                varName = varName2
            if key in cmip:
                #print("if key in cmip", key)
                # pull global atts and compare, note if different
                globalAttDic, calendar, lev, levUnits, lat, lon, varList, errX, errC = readData(
                    filePath.path, varName)
                # catch file open error
                if isinstance(globalAttDic, list):
                    # badFileList.append(globalAttDic)
                    cmip["_badFileList"][str(cnt)] = globalAttDic
                    if isinstance(errX, list):
                        # badFileList.append(errX)
                        cmip["_badFileList"][str(cnt)] = errX
                    if isinstance(errC, list):
                        # badFileList.append(errC)
                        cmip["_badFileList"][str(cnt)] = errC
                    continue  # skip file, proceed to next in loop
                dic2 = getGlobalAtts(globalAttDic, calendar,
                                     lon, lat, lev, levUnits)
                if dic2 == {}:
                    continue  # skip file, proceed to next in loop
                dic1 = cmip[key]
                update, newDic = compareDicts(dic1, dic2, cnt, filePath.path)
                # wash types
                newDic = walkWashDicList(newDic)

                # if difference found, update new entry
                if update:
                    cmip[key] = newDic
            else:
                # pull global atts for new entry
                globalAttDic, calendar, lev, levUnits, lat, lon, varList, errX, errC = readData(
                    filePath.path, varName)
                # catch file open error
                if isinstance(globalAttDic, list):
                    # badFileList.append(globalAttDic)
                    cmip["_badFileList"][str(cnt)] = globalAttDic
                    if isinstance(errX, list):
                        # badFileList.append(errX)
                        cmip["_badFileList"][str(cnt)] = errX
                    if isinstance(errC, list):
                        # badFileList.append(errC)
                        cmip["_badFileList"][str(cnt)] = errC
                    continue  # skip file, proceed to next in loop
                tmp = getGlobalAtts(globalAttDic, calendar,
                                    lon, lat, lev, levUnits)
                if tmp == {}:
                    continue  # skip file, proceed to next in loop
                # wash types
                tmp = walkWashDicList(tmp)
                cmip[key] = tmp
        elif firstPath in filePath.path:
            # query a single file per directory
            pass

        # %% iteratively write out results to local file
        # end timer
        endTime = time.time()
        timeTaken = "{:07.3f}".format(endTime - startTime)
        print("cnt:", cnt, "time:", timeTaken)
        # cnt records every file, only interrogates the first in a single directory
        if not cnt % 1000:
            writeJson(cmip, testPath, cnt, timeTaken, fileNameAdd)

    # %% and write out final file
    # end timer
    endTime = time.time()
    timeTaken = "{:07.3f}".format(endTime - startTime)
    print("cnt:", cnt, "time:", timeTaken)
    writeJson(cmip, testPath, cnt, timeTaken, fileNameAdd)
    # print("badFileList:")
    # for count, filename in enumerate(badFileList):
    #    print("{:04d}".format(count), badFileList[count])

except:
    # catch error and send email alert
    print("Caught unexpected error:", sys.exc_info()[0])
    alertError("count", "filePath", sys.exc_info()[0])

# %% Notes
"""
Steve joblib demo

# imports
from joblib import Parallel, delayed
from tqdm import tqdm

# worker function
def paul(fn):
    . . .
    key = getDrs(filepath.path)
    tmp = getGlobalAtts(fn.path)
    return key, tmp

# call worker function in parallel
results = Parallel(n_jobs=5)(delayed(paul)(fn) for fn in tqdm(filelist))

# put results into a dictionary based on some rules
for row in result:
    if …:
        cmip[key] = tmp
    elif …:
        cmip[key] = tmp

(cdms315) bash-4.2$ python extractLicenseContact.py RFMIP
badFileList:
0000 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-CM6-1/piClim-ghg/r1i1p1f2/Eday/rivo/gn/v20190621/rivo_Eday_CNRM-CM6-1_piClim-ghg_r1i1p1f2_gn_18500101-18791231.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0001 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-CM6-1/piClim-ghg/r1i1p1f2/Emon/wtd/gn/v20190621/wtd_Emon_CNRM-CM6-1_piClim-ghg_r1i1p1f2_gn_185001-187912.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0002 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-CM6-1/piClim-control/r1i1p1f2/Eday/rivo/gn/v20190621/rivo_Eday_CNRM-CM6-1_piClim-control_r1i1p1f2_gn_18500101-18791231.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0003 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-CM6-1/piClim-control/r1i1p1f2/Emon/wtd/gn/v20190621/wtd_Emon_CNRM-CM6-1_piClim-control_r1i1p1f2_gn_185001-187912.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0004 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-CM6-1/piClim-anthro/r1i1p1f2/Eday/rivo/gn/v20190621/rivo_Eday_CNRM-CM6-1_piClim-anthro_r1i1p1f2_gn_18500101-18791231.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0005 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-CM6-1/piClim-anthro/r1i1p1f2/Emon/wtd/gn/v20190621/wtd_Emon_CNRM-CM6-1_piClim-anthro_r1i1p1f2_gn_185001-187912.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0006 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-CM6-1/piClim-4xCO2/r1i1p1f2/Eday/rivo/gn/v20190621/rivo_Eday_CNRM-CM6-1_piClim-4xCO2_r1i1p1f2_gn_18500101-18791231.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0007 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-CM6-1/piClim-4xCO2/r1i1p1f2/Emon/wtd/gn/v20190621/wtd_Emon_CNRM-CM6-1_piClim-4xCO2_r1i1p1f2_gn_185001-187912.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0008 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-CM6-1/piClim-aer/r1i1p1f2/Eday/rivo/gn/v20190621/rivo_Eday_CNRM-CM6-1_piClim-aer_r1i1p1f2_gn_18500101-18791231.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0009 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-CM6-1/piClim-aer/r1i1p1f2/Emon/wtd/gn/v20190621/wtd_Emon_CNRM-CM6-1_piClim-aer_r1i1p1f2_gn_185001-187912.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0010 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-ESM2-1/piClim-lu/r1i1p1f2/Eday/rivo/gn/v20190219/rivo_Eday_CNRM-ESM2-1_piClim-lu_r1i1p1f2_gn_18500101-18791231.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0011 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-ESM2-1/piClim-lu/r1i1p1f2/Emon/wtd/gn/v20190219/wtd_Emon_CNRM-ESM2-1_piClim-lu_r1i1p1f2_gn_185001-187912.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0012 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-ESM2-1/piClim-ghg/r1i1p1f2/Eday/rivo/gn/v20190621/rivo_Eday_CNRM-ESM2-1_piClim-ghg_r1i1p1f2_gn_18500101-18791231.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0013 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-ESM2-1/piClim-ghg/r1i1p1f2/Emon/wtd/gn/v20190621/wtd_Emon_CNRM-ESM2-1_piClim-ghg_r1i1p1f2_gn_185001-187912.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0014 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-ESM2-1/piClim-control/r1i1p1f2/Eday/rivo/gn/v20190219/rivo_Eday_CNRM-ESM2-1_piClim-control_r1i1p1f2_gn_18500101-18791231.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0015 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-ESM2-1/piClim-control/r1i1p1f2/Emon/wtd/gn/v20190219/wtd_Emon_CNRM-ESM2-1_piClim-control_r1i1p1f2_gn_185001-187912.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0016 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-ESM2-1/piClim-anthro/r1i1p1f2/Eday/rivo/gn/v20190621/rivo_Eday_CNRM-ESM2-1_piClim-anthro_r1i1p1f2_gn_18500101-18791231.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0017 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-ESM2-1/piClim-4xCO2/r1i1p1f2/Eday/rivo/gn/v20190621/rivo_Eday_CNRM-ESM2-1_piClim-4xCO2_r1i1p1f2_gn_18500101-18791231.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0018 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-ESM2-1/piClim-4xCO2/r1i1p1f2/Emon/wtd/gn/v20190621/wtd_Emon_CNRM-ESM2-1_piClim-4xCO2_r1i1p1f2_gn_185001-187912.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0019 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-ESM2-1/piClim-aer/r1i1p1f2/Eday/rivo/gn/v20190219/rivo_Eday_CNRM-ESM2-1_piClim-aer_r1i1p1f2_gn_18500101-18791231.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
0020 ['/p/css03/esgf_publish/CMIP6/RFMIP/CNRM-CERFACS/CNRM-ESM2-1/piClim-aer/r1i1p1f2/Emon/wtd/gn/v20190219/wtd_Emon_CNRM-ESM2-1_piClim-aer_r1i1p1f2_gn_185001-187912.nc', SystemError('<built-in function CdunifFile> returned a result with an error set')]
"""
