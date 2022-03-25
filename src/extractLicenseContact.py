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
                     TODO: add iterator counter to version_data/writeJson to indicate completion stats
                     TODO: grid_info also needs to have realms - ala nominal_resolution
                     TODO: convert compareDicts test block to dealWithDuplicateEntry
                     TODO: debug ScenarioMIP seg fault - reproducible? v20190306/tauvo_Omon_CanESM5_ssp126_r5i1p1f1_gn_201501-210012.nc",  # 527759 ScenarioMIP
                     TODO: update to use joblib, parallel calls, caught with sqlite database for concurrent reads
                     TODO: update getDrs for CMIP5 and CMIP3


@author: durack1
"""

# %% imports
import argparse

import cdms2
import datetime
import json
import numpy as np
import os
import pdb
from os import scandir
import subprocess
import sys
import time
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
                    val1 = tmp1
                    tmp1 = {}
                    tmp1[val1] = {}
                    tmp1[val1]["keys"] = []
                    tmp1[val1]["keys"].append(key1)
                    tmp1[val1]["count"] = 1
                    tmp1[tmp2] = {}
                    tmp1[tmp2]["keys"] = []
                    tmp1[tmp2]["keys"].append(key2)
                    tmp1[tmp2]["count"] = 1
                elif isinstance(tmp1, dict):
                    print("catch new entry in existing dictionary")
                    # if key already exists append
                    if tmp2 in list(tmp1.keys()):
                        # print("tmp2 == key"); pdb.set_trace()
                        tmp1[tmp2]["keys"].append(key2)
                        tmp1[tmp2]["count"] = tmp1[tmp2]["count"] + 1
                    # if key doesn't exist add new
                    else:
                        # print("else"); pdb.set_trace()
                        tmp1[tmp2] = {}
                        tmp1[tmp2]["keys"] = [key2]
                        tmp1[tmp2]["count"] = 1
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


def dealWithDuplicateEntry(key, dict1, val1, id1, dict2, val2, id2):
    """
    dealWithDuplicateEntry(key, dic1, id1, dic2, id2):

    Checks first argument to find second argument
    """


def getAxes(d, varName):
    """
    ###getAxes(var, fileHandle)
    getAxes(d, varName)

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

    # get coord dict
    axisIds = list(d._coord_names)
    varShape = eval(".".join(["d", varName, "shape"]))
    heightVarName = d._coord_names - set(
        ["time", "lat", "latitude", "lon", "longitude"]
    )
    try:
        print("enter try")
        if len(varShape) == 1:
            print("no valid grid")
            latLen, lat0, latN = ["x" for _ in range(3)]
            lonLen, lon0, lonN = ["x" for _ in range(3)]
            heightLen, height0, heightN, heightUnit = ["x" for _ in range(4)]
        ###elif var.getAxisIds() in [["ygre", "xgre"], ["yant", "xant"]]:
        elif axisIds in [["ygre", "xgre"], ["yant", "xant"]]:
            print("hit ice-sheet grid, exiting")
            pass
        else:
            ###lat = var.getLatitude()
            lat = d.lat.data
            ###lon = var.getLongitude()
            lon = d.lon.data
            # test for None
            if not [x for x in (lat, lon) if x is None]:
                raise Exception("Attribute Error")
            # create strings
            latLen = str(len(lat))
            lat0 = str(np.min(lat))  # str(lat[0])
            latN = str(np.max(lat))  # str(lat[-1])
            if len(lon.shape) == 2:
                lonLen = str(lon.shape[1])
            else:
                lonLen = str(len(lon))
            lon0 = str(np.min(lon))  # str(lon[0])
            lonN = str(np.max(lon))  # str(lon[-1])
            # get height conditional on shape
            ###if len(var.shape) > 3 and "height" in var.getAxisIds():
            if len(varShape) > 3 and "height" in axisIds:
                heightVar = eval(".".join(["d", heightVarName, "data"]))
                heightLen = str(len(heightVar))
                height0 = str(heightVar[0])
                heightN = str(heightVar[-1])
                heightUnit = heightVar.units
            else:
                heightLen, height0, heightN, heightUnit = ["x" for _ in range(4)]

    # deal with i,j index grids
    except Exception as error:
        print("getAxes: enter except", error)
        ###axes = var.getAxisIds()
        # test for var shape
        if "site" in axisIds:
            # assume a time, site variable (no lat/lon)
            return tmp
            raise Exception("site variable, skipping")
        elif axisIds[0] == "time" and varShape == 3:
            # assume time, lat, lon
            axInd = 1
        elif len(varShape) == 4:
            # assume time, height, lat, lon
            axInd = 2
        elif len(varShape) == 2:
            # assume lat, lon (fx field)
            axInd = 0
        try:
            print("enter try2")
            # pdb.set_trace()
            latVar = d.lat.data
            latLen = str(len(latVar))
            lat0 = str(np.min(latVar))
            print("lat0")
            print(lat0)
            latN = str(np.max(latVar))
            lonVar = d.lon.data
            lon = str(len(lonVar))
            lon0 = str(np.min(lonVar))
            lonN = str(np.max(lonVar))
            if len(varShape) == 4:
                heightVar = eval(".".join(["d", heightVarName, "data"]))
                heightLen = str(len(heightVar))
                height0 = str(heightVar[0])
                heightN = str(heightVar[-1])
                heightUnit = heightVar.units
            else:
                heightLen, height0, heightN = ["x" for _ in range(3)]
        except Exception as error:
            print("getAxes: try2, no valid dims", error)

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


def getCalendar(var):
    """
    getCalendar(var)

    Extracts calendar info from variable time axis
    """
    ###axisIds = var.getAxisIds()
    axisIds = var._coord_names
    if "time" in axisIds:
        ###timeAx = var.getTime()
        ###calendar = timeAx.calendar
        if "calendar" in var.time.encoding.keys():
            calendar = var.time.encoding["calendar"]
    else:
        calendar = ""

    return calendar


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


def getGlobalAtts(filePath):
    """
    getGlobalAtts(filePath)

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

    tmp = {}
    # deal with SystemError - CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2 data
    # https://github.com/CDAT/cdms/issues/442
    try:
        ###fH = cdms2.open(filePath) # OSError, SystemError, UnicodeDecodeError,
        fH = dataset.open_dataset(filePath)  # Attribute, ValueError
    except (
        np.core._exceptions._UFuncBinaryResolutionError,
        AttributeError,
        OSError,
        SystemError,
        UnicodeDecodeError,
        ValueError,
    ) as error:
        print("")
        print("getGlobalAtts: badFile:", filePath)
        print("Error:", error)
        print("")
        return [filePath, error]
    # extract globalAtts
    globalAttDic = fH.attrs
    for cnt, globalAtt in enumerate(globalAtts):
        try:
            ###val = eval("".join(["fH.", globalAtt]))
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
    # get grid info
    # debug start
    if (
        filePath
        ==
        # "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r1i1p1f2/CFmon/clisccp/gr/v20180705/clisccp_CFmon_CNRM-CM6-1_abrupt-4xCO2_r1i1p1f2_gr_185001-199912.nc"  # 14134 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r1i1p1f2/CFmon/clcalipso/gr/v20180705/clcalipso_CFmon_CNRM-CM6-1_abrupt-4xCO2_r1i1p1f2_gr_185001-199912.nc"  # 14128 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r3i1p1f2/Eday/rivo/gn/v20181012/rivo_Eday_CNRM-CM6-1_abrupt-4xCO2_r3i1p1f2_gn_18500501-18591231.nc"  # 13589 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1-HR/amip/r1i1p1f2/Emon/mrsol/gr/v20191202/mrsol_Emon_CNRM-CM6-1-HR_amip_r1i1p1f2_gr_197901-201412.nc"  # 12166 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1-HR/historical/r1i1p1f2/6hrPlevPt/zg500/gr/v20191021/zg500_6hrPlevPt_CNRM-CM6-1-HR_historical_r1i1p1f2_gr_196001010600-197001010000.nc"  # 8009 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1-HR/abrupt-4xCO2/r1i1p1f2/Ofx/basin/gn/v20191021/basin_Ofx_CNRM-CM6-1-HR_abrupt-4xCO2_r1i1p1f2_gn.nc"  # 5777 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1-HR/abrupt-4xCO2/r1i1p1f2/Ofx/masscello/gn/v20191021/masscello_Ofx_CNRM-CM6-1-HR_abrupt-4xCO2_r1i1p1f2_gn.nc"  # 5775 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1-HR/abrupt-4xCO2/r1i1p1f2/Ofx/areacello/gn/v20191021/areacello_Ofx_CNRM-CM6-1-HR_abrupt-4xCO2_r1i1p1f2_gn.nc"  # 5774 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/THU/CIESM/abrupt-4xCO2/r1i1p1f1/Amon/hur/gr/v20200417/hur_Amon_CIESM_abrupt-4xCO2_r1i1p1f1_gr_000101-015012.nc"  # 3040 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/THU/CIESM/abrupt-4xCO2/r1i1p1f1/SImon/sispeed/gn/v20200420/sispeed_SImon_CIESM_abrupt-4xCO2_r1i1p1f1_gn_010101-015012.nc"  # 2977 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/THU/CIESM/abrupt-4xCO2/r1i1p1f1/SImon/siflsenstop/gn/v20200420/siflsenstop_SImon_CIESM_abrupt-4xCO2_r1i1p1f1_gn_005101-010012.nc"  # 2860 CMIP
        # "/p/css03/esgf_publish/CMIP6/VolMIP/MIROC/MIROC-ES2L/volc-pinatubo-strat/r3i1p1f2/Ofx/sftof/gn/v20210118/sftof_Ofx_MIROC-ES2L_volc-pinatubo-strat_r3i1p1f2_gn.nc"  # 41746 complete
        # "/p/css03/esgf_publish/CMIP6/VolMIP/CCCma/CanESM5/volc-long-eq/r29i1p2f1/Amon/cl/gn/v20190429/cl_Amon_CanESM5_volc-long-eq_r29i1p2f1_gn_181504-187003.nc"  # 25636
        # "/p/css03/esgf_publish/CMIP6/VolMIP/CCCma/CanESM5/volc-long-eq/r29i1p2f1/Omon/epcalc100/gn/v20190429/epcalc100_Omon_CanESM5_volc-long-eq_r29i1p2f1_gn_181504-187003.nc"  # 25509
        # "/p/css03/esgf_publish/CMIP6/VolMIP/NASA-GISS/GISS-E2-1-G/volc-pinatubo-full/r5i9p1f1/Amon/ps/gn/v20190903/ps_Amon_GISS-E2-1-G_volc-pinatubo-full_r5i9p1f1_gn_808301-808512.nc"  # 5646
        # "/p/css03/esgf_publish/CMIP6/VolMIP/NASA-GISS/GISS-E2-1-G/volc-pinatubo-full/r8i2p1f1/Amon/ps/gn/v20190903/ps_Amon_GISS-E2-1-G_volc-pinatubo-full_r8i2p1f1_gn_824801-825012.nc"  # 5480
        # "/p/css03/esgf_publish/CMIP6/ISMIP6/NASA-GISS/GISS-E2-1-G/1pctCO2-4xext/r1i1p1f1/Amon/clw/gn/v20180906/clw_Amon_GISS-E2-1-G_1pctCO2-4xext_r1i1p1f1_gn_192001-195012.nc"  # 5320
        # "/p/css03/esgf_publish/CMIP6/ISMIP6/NASA-GISS/GISS-E2-1-G/1pctCO2-4xext/r1i1p1f1/Amon/ps/gn/v20180906/ps_Amon_GISS-E2-1-G_1pctCO2-4xext_r1i1p1f1_gn_192001-195012.nc"  # 5286
        # "/p/css03/esgf_publish/CMIP6/ISMIP6/NASA-GISS/GISS-E2-1-G/1pctCO2-4xext/r1i1p1f1/Amon/vas/gn/v20180906/vas_Amon_GISS-E2-1-G_1pctCO2-4xext_r1i1p1f1_gn_192001-195012.nc"  # 5248
        # "/p/css03/esgf_publish/CMIP6/ISMIP6/NASA-GISS/GISS-E2-1-G/1pctCO2-4xext/r1i1p1f1/Emon/cSoilAbove1m/gn/v20181022/cSoilAbove1m_Emon_GISS-E2-1-G_1pctCO2-4xext_r1i1p1f1_gn_192001-195012.nc"  # 5184
        # "/p/css03/esgf_publish/CMIP6/ISMIP6/NASA-GISS/GISS-E2-1-G/1pctCO2-4xext/r1i1p1f1/Omon/sltovgyre/gn/v20180906/sltovgyre_Omon_GISS-E2-1-G_1pctCO2-4xext_r1i1p1f1_gn_192001-195012.nc"  #4981
        # "/p/css03/esgf_publish/CMIP6/ISMIP6/NCAR/CESM2/ssp585-withism/r1i1p1f1/IfxGre/hfgeoubed/gn/v20210513/hfgeoubed_IfxGre_CESM2_ssp585-withism_r1i1p1f1_gn.nc"
        # "/p/css03/esgf_publish/CMIP6/ISMIP6/NCAR/CESM2/ssp585-withism/r1i1p1f1/Emon/nwdFracLut/gn/v20210513/nwdFracLut_Emon_CESM2_ssp585-withism_r1i1p1f1_gn_224901-229912.nc"
        # "/p/css03/esgf_publish/CMIP6/ISMIP6/NCAR/CESM2/ssp585-withism/r1i1p1f1/Omon/thetaoga/gn/v20210513/thetaoga_Omon_CESM2_ssp585-withism_r1i1p1f1_gn_201501-206412.nc"
        # "/p/css03/esgf_publish/CMIP6/ISMIP6/NCAR/CESM2/ssp585-withism/r1i1p1f1/Omon/thetaoga/gn/v20210513/thetaoga_Omon_CESM2_ssp585-withism_r1i1p1f1_gn_201501-206412.nc"
        # "/p/css03/esgf_publish/CMIP6/ISMIP6/NCAR/CESM2/ssp585-withism/r1i1p1f1/Ofx/areacello/gr/v20191120/areacello_Ofx_CESM2_ssp585-withism_r1i1p1f1_gr.nc"
        # "/p/css03/esgf_publish/CMIP6/ISMIP6/NCAR/CESM2/ssp585-withism/r1i1p1f1/Ofx/sftof/gn/v20210513/sftof_Ofx_CESM2_ssp585-withism_r1i1p1f1_gn.nc"
        # "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r1i1p1f2/Emon/cropFracC4/gr/v20180705/cropFracC4_Emon_CNRM-CM6-1_abrupt-4xCO2_r1i1p1f2_gr_185001-199912.nc"  # 14439 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r1i1p1f2/Emon/thetaot/gn/v20180705/thetaot_Emon_CNRM-CM6-1_abrupt-4xCO2_r1i1p1f2_gn_185001-194912.nc"  # 14451 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/historical/r3i1p1f2/CFsubhr/prc/gn/v20190125/prc_CFsubhr_CNRM-CM6-1_historical_r3i1p1f2_gn_18500101003000-20150101000000.nc"  # 17588 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/historical/r3i1p1f2/Emon/parasolRefl/gr/v20190125/parasolRefl_Emon_CNRM-CM6-1_historical_r3i1p1f2_gr_185001-200912.nc"  # 18897 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/amip/r1i1p1f2/E3hrPt/clmisr/gr/v20181203/clmisr_E3hrPt_CNRM-CM6-1_amip_r1i1p1f2_gr_200801010300-200901010000.nc"  # 45899 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/amip/r1i1p1f2/E3hrPt/jpdftaureicemodis/gr/v20181203/jpdftaureicemodis_E3hrPt_CNRM-CM6-1_amip_r1i1p1f2_gr_200801010300-200901010000.nc"  # 46048 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/BCC/BCC-ESM1/abrupt-4xCO2/r1i1p1f1/SImon/siitdconc/gn/v20190611/siitdconc_SImon_BCC-ESM1_abrupt-4xCO2_r1i1p1f1_gn_185001-200012.nc"  # 78614 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/BCC/BCC-ESM1/abrupt-4xCO2/r1i1p1f1/Amon/o3/gn/v20190613/o3_Amon_BCC-ESM1_abrupt-4xCO2_r1i1p1f1_gn_185001-185012-clim.nc"  # 78745 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/BCC/BCC-ESM1/historical/r1i1p1f1/AERmon/od550so4/gn/v20190918/od550so4_AERmon_BCC-ESM1_historical_r1i1p1f1_gn_185001-201412.nc"  # 79752 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/NCAR/CESM2-WACCM/abrupt-4xCO2/r1i1p1f1/Omon/zooc/gr/v20190425/zooc_Omon_CESM2-WACCM_abrupt-4xCO2_r1i1p1f1_gr_005001-009912.nc"  # 91678 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/MOHC/UKESM1-0-LL/abrupt-4xCO2/r1i1p1f2/CFmon/clwc/gn/v20190406/clwc_CFmon_UKESM1-0-LL_abrupt-4xCO2_r1i1p1f2_gn_190001-194912.nc"  # 405162 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/abrupt-4xCO2/r1i1p1f1/Omon/msftyz/gn/v20180701/msftyz_Omon_GFDL-ESM4_abrupt-4xCO2_r1i1p1f1_gn_006101-008012.nc"  # 811631 CMIP
        # "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/amip/r1i1p1f2/CFsubhr/prc/gn/v20181203/prc_CFsubhr_CNRM-CM6-1_amip_r1i1p1f2_gn_19790101003000-20150101000000.nc"  # 47438 CMIP
        ""
    ):
        pdb.set_trace()
    # debug close
    ###varNames = fH.variables
    varNames = []
    for a, b in enumerate(fH.data_vars.keys()):
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
    # pdb.set_trace()
    var = eval(".".join(["fH", tmp["variable_id"], "data"]))
    if var is None:
        # if variable_id not set, try loading ascertained varName
        ###var = fH[varName]
        var = eval(".".join(["fH", varName, "data"]))
    if var is None:
        tmp["grid_info"] = "x"
        tmp["calendar"] = "x"
    else:
        tmp["grid_info"] = getAxes(fH, varName)
        ###calendar = getCalendar(var)
        calendar = getCalendar(fH)
        if calendar != "":
            tmp["calendar"] = calendar

    # add list of non-queried globalAtts
    ###tmp["||_unvalidated"] = list(set(fH.attributes).difference(globalAtts))
    tmp["||_unvalidated"] = list(set(fH.attrs).difference(globalAtts))
    fH.close()

    return tmp


def readData(filePath, varName):
    """
    read netcdf file using xarray or cdms2 and return file and coordinate
    attributes

    102799 /p/css03/esgf_publish/CMIP6/PMIP/NCAR/CESM2/midPliocene-eoi400/r1i1p1f1/SImon/sistremax/gn/v20200110/sistremax_SImon_CESM2_midPliocene-eoi400_r1i1p1f1_gn_115101-120012.nc
    https://stackoverflow.com/questions/17322208/multiple-try-codes-in-one-block

    """
    # read data - validate with ncdump that valid data, then try open and read
    cmd = subprocess.Popen(
        ["ncdump", "-h", filePath],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, errors = cmd.communicate()
    cmd.wait()
    if errors != b"":
        print("output:", output)
        print("errors:", errors)
        err = [filePath, errors]
        # try xarray read
        try:
            fH = open_dataset(filePath)
            # Extract stuff
            attDic = fH.attrs
            calendar = fH.time.encoding["calendar"]
            lev = fH[fH.cf.axes["Z"]].z.data
            lat = fH[fH.cf.axes["Y"]].y.data
            lon = fH[fH.cf.axes["X"]].x.data
        except (
            np.core._exceptions._UFuncBinaryResolutionError,
            AttributeError,
            ValueError,
        ) as error:
            print("")
            print("readData: badFile xarray:", filePath)
            print("Error:", error)
            print("")
            err = [filePath, error]
            # try cdms2
            try:
                fH = cdms2.open(filePath)
                # Extract stuff
                attDic = fH.attributes
                d = fH(varName, time=slice(0, 1))
                calendar = d.getTime().calendar
                lev = d.getLevel().getData()
                lat = d.getLatitude().data
                lon = d.getLongitude().data
                fH.close()
            except (
                OSError,
                SystemError,
                UnicodeDecodeError,
            ) as error:
                print("")
                print("readData: badFile cdms2:", filePath)
                print("Error:", error)
                print("")
                err = [filePath, error]
        finally:
            if err == None:
                return attDic, calendar, lev, lat, lon
            else:
                return err


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
        # yield directory if there are any files in it
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            yield entry


def writeJson(dic, testPath, count, endTime):
    """
    writeJson(dic, testPath, count, endTime)

    Takes dictionary, path, count and endTime and writes out to json file
    """
    # get time info
    timeNow = datetime.datetime.now()
    timeFormatDir = timeNow.strftime("%y%m%d")
    cmip["version_metadata"]["end_time  "] = endTime
    # get path
    pathInfo = testPath.replace("/p/css03/esgf_publish/", "").replace("/", "-")
    if pathInfo == "CMIP6-":
        pathInfo = "CMIP6-no-cdmsBadFiles"
    # get count
    cmip["version_metadata"]["file_processed_count"] = str(count)
    # Write output
    print("")
    outFile = "_".join([timeFormatDir, pathInfo, "metaData.json"])
    if os.path.exists(outFile):
        os.remove(outFile)
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
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r5i1p1f2/Emon/wtd/gn/v20181012/wtd_Emon_CNRM-CM6-1_abrupt-4xCO2_r5i1p1f2_gn_185009-185912.nc",  # 14916 CMIP + more try/except added
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r5i1p1f2/fx/areacellr/gn/v20181012/areacellr_fx_CNRM-CM6-1_abrupt-4xCO2_r5i1p1f2_gn.nc",  # 14917 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/MOHC/HadGEM3-GC31-MM/historical/r1i1p1f3/CFday/clivi/gn/v20191207/clivi_CFday_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_19200101-19241230.nc",  # 513159 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/NCC/NorESM2-MM/historical/r3i1p1f1/SImon/siarean/gn/v20200702/siarean_SImon_NorESM2-MM_historical_r3i1p1f1_gn_186001-186912.nc",  # 7176050 CMIP, netcdf fail
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/amip/r1i1p1f2/Eday/rivo/gn/v20181203/rivo_Eday_CNRM-CM6-1_amip_r1i1p1f2_gn_19790101-20141231.nc",  # 47148 CMIP, cdms.open fail utf-8 decode
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r1i1p1f2/Eday/rivo/gn/v20180705/rivo_Eday_CNRM-CM6-1_abrupt-4xCO2_r1i1p1f2_gn_19000101-19491231.nc",  # 14308 CMIP, cdms open fail utf-8
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r1i1p1f2/Eday/rivo/gn/v20180705/rivo_Eday_CNRM-CM6-1_abrupt-4xCO2_r1i1p1f2_gn_18500101-18991231.nc",  # 14309 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r1i1p1f2/Eday/rivo/gn/v20180705/rivo_Eday_CNRM-CM6-1_abrupt-4xCO2_r1i1p1f2_gn_19500101-19991231.nc",  # Proactive
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r2i1p1f2/Eday/rivo/gn/v20181012/rivo_Eday_CNRM-CM6-1_abrupt-4xCO2_r2i1p1f2_gn_18500301-18591231.nc",  # 15108 CMIP
    "/p/css03/esgf_publish/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r2i1p1f2/Emon/wtd/gn/v20181012/wtd_Emon_CNRM-CM6-1_abrupt-4xCO2_r2i1p1f2_gn_185003-185912.nc",  # 15201 CMIP
    "/p/css03/esgf_publish/CMIP6/ScenarioMIP/CCCma/CanESM5/ssp126/r5i1p1f1/Omon/tauvo/gn/v20190306/tauvo_Omon_CanESM5_ssp126_r5i1p1f1_gn_201501-210012.nc",  # 527759 ScenarioMIP
    "/p/css03/esgf_publish/CMIP6/HighResMIP/CAS/FGOALS-f3-H/highres-future/r1i1p1f1/Omon/tosga/gn/v20201225/tosga_Omon_FGOALS-f3-H_highres-future_r1i1p1f1_gn_201501-205012.nc",  # 669356 CMIP6
    "/p/css03/esgf_publish/CMIP6/ScenarioMIP/MRI/MRI-ESM2-0/ssp119/r5i1p1f1/Emon/cldnci/gn/v20210907/cldnci_Emon_MRI-ESM2-0_ssp119_r5i1p1f1_gn_201501-210012.nc",  # 5543227 ScenarioMIP
    "/p/css03/esgf_publish/CMIP6/HighResMIP/CAS/FGOALS-f3-H/highres-future/r1i1p1f1/Omon/tosga/gn/v20201225/tosga_Omon_FGOALS-f3-H_highres-future_r1i1p1f1_gn_201501-205012.nc",  # 669xxx
    "/p/css03/esgf_publish/CMIP6/VolMIP/MIROC/MIROC-ES2L/volc-pinatubo-strat/r3i1p1f2/Omon/zooc/gn/v20210118/zooc_Omon_MIROC-ES2L_volc-pinatubo-strat_r3i1p1f2_gn_185006-185312.nc",  # CMIP6 42348, AttributeError
)

# %% loop over files and build index
parser = argparse.ArgumentParser(description="Process some CMIPx data")
parser.add_argument(
    "activityId", metavar="S", type=str, help="an activity_id to build the search from"
)
args = parser.parse_args()
if args.activityId in ["CMIP", "OMIP", "RFMIP", "ScenarioMIP"]:
    actId = args.activityId
elif args.activityId == "CMIP6":
    actId = ""
else:
    print("Invalid path, ", args.activityId, "exiting")
    sys.exit()

# create testpath
testPath = os.path.join(testPath, actId)
print("Processing testPath:", testPath)

# create variable to catch bad files
badFileList = []

# use iterator to start scan
x = scantree(testPath)
cmip = {}
cmip["version_metadata"] = {}
cmip["version_metadata"]["author"] = "Paul J. Durack <durack1@llnl.gov>"
cmip["version_metadata"]["institution_id"] = "PCMDI"
startTime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
cmip["version_metadata"]["start_time"] = startTime
for cnt, filePath in enumerate(x):
    # start timer
    startTime = time.time()
    # debug start
    if cnt == "none":
        endTime = time.time()
        timeTaken = "{:07.3f}".format(endTime - startTime)
        # writeJson(cmip, testPath, cnt, timeTaken)
        # os.system("cp 220220_CMIP6-CMIP_metaData.json dupe.json")
        print("catching dictionary, pre-crash")
        pdb.set_trace()
    indStart = (
        # 669000  # HighResMIP
        # 6547960 ScenarioMIP
        # 42345  # CMIP6 42348
        -1
    )
    if cnt < indStart:
        print(cnt, filePath.path)
        continue
    elif cnt == indStart:
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
        if key in cmip:
            print("if key in cmip")
            # pull global atts and compare, note if different
            dic2 = getGlobalAtts(filePath.path)
            print("dic2:", dic2)
            # catch file open error
            if isinstance(dic2, list):
                badFileList.append(dic2)
                continue  # skip file, proceed to next in loop
            elif dic2 == {}:
                continue  # skip file, proceed to next in loop
            dic1 = cmip[key]
            print("call compareDicts")
            update, newDic = compareDicts(dic1, dic2, cnt, filePath.path)
            # if difference found, update new entry
            if update:
                cmip[key] = newDic
        else:
            # pull global atts for new entry
            tmp = getGlobalAtts(filePath.path)
            if isinstance(tmp, list):
                badFileList.append(tmp)
                continue  # skip file, proceed to next in loop
            elif tmp == {}:
                print("if key in cmip - else")
                continue  # skip file, proceed to next in loop
            cmip[key] = tmp
    elif firstPath in filePath.path:
        pass
        # print('dupe files, skipping')

    # %% iteratively write out results to local file
    # end timer
    endTime = time.time()
    timeTaken = "{:07.3f}".format(endTime - startTime)
    print("cnt:", cnt, "time:", timeTaken)
    if not cnt % 1000:
        writeJson(cmip, testPath, cnt, timeTaken)

# %% and write out final file
# end timer
endTime = time.time()
timeTaken = "{:07.3f}".format(endTime - startTime)
print("cnt:", cnt, "time:", timeTaken)
writeJson(cmip, testPath, cnt, timeTaken)
print("badFileList:")
for count, filename in enumerate(badFileList):
    print("{:04d}".format(count), badFileList[count])


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
