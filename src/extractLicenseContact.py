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

@author: durack1
"""

# %% imports
import cdms2
import datetime
import json
import numpy as np
import os
import pdb
from os import scandir

# %% function defs


def alertError(count, filePath, key2):
    """
    alertError()

    Sends an email alerting that a condition has been reached

    Based on:
        https://realpython.com/python-send-email/#sending-your-plain-text-email
        https://stackoverflow.com/questions/28328222/smtplib-of-python-not-working

    """
    import smtplib

    smtp_server = "nospam.llnl.gov"
    sender_email = "error@durack1"
    receivers_email = ["pauldurack@gmail.com", "pauldurack@llnl.gov"]
    to = ", ".join(receivers_email)
    subject = "extractLicenseContact.py error"
    body = "This message is sent from Python"
    message = "Subject: {}\ncount: {}\nfilePath: {}\nkey2: {}\n\n{}".format(
        subject, count, filePath, key2, body
    )
    with smtplib.SMTP(smtp_server) as server:
        server.sendmail(sender_email, to, message)


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
            key2 = ".".join([dict2["table_id"], dict2["variable_id"]])
            tmp1 = dict1[key]
            tmp2 = dict2[key]
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
                    tmp1[dict1Realm]["original"] = val1
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
                    val1 = tmp1[key]
                    tmp1[key] = {}
                    tmp1["original"] = val1
                    tmp1[key2] = tmp2
                elif isinstance(tmp1, dict):
                    tmp1[key2] = tmp2
                # assign new tmp1 dictionary to key
                dict1[key] = tmp1
                pdb.set_trace()
            update = True
            alertError(count, filePath, key2)
        else:
            update = False

    return update, dict1


def getAxes(var):
    """
    getAxes(var)

    Extracts grid info dependent on input
    """
    # preallocate
    latLen, lat0, latN = ["x" for _ in range(3)]
    lonLen, lon0, lonN = ["x" for _ in range(3)]
    heightLen, height0, heightN, heightUnit = ["x" for _ in range(4)]

    try:
        print("enter try")
        if len(var.shape) == 1:
            print("no valid grid")
            latLen, lat0, latN = ["x" for _ in range(3)]
            lonLen, lon0, lonN = ["x" for _ in range(3)]
            heightLen, height0, heightN, heightUnit = ["x" for _ in range(4)]
        elif var.getAxisIds() in [["ygre", "xgre"], ["yant", "xant"]]:
            print("hit ice-sheet grid, exiting")
            pass
        else:
            lat = var.getLatitude()
            lon = var.getLongitude()
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
            if len(var.shape) > 3 and "height" in var.getAxisIds():
                heightVar = var.getLevel()
                heightLen = str(len(heightVar))
                height0 = str(heightVar[0])
                heightN = str(heightVar[-1])
                heightUnit = heightVar.units
            else:
                heightLen, height0, heightN, heightUnit = ["x" for _ in range(4)]

    # deal with i,j index grids
    except (AttributeError):
        print("enter except")
        axes = var.getAxisList()
        # test for var shape
        if axes[0].id == "time" and var.shape == 3:
            # assume time, lat, lon
            axInd = 1
        elif len(var.shape) == 4:
            # assume time, height, lat, lon
            axInd = 2
        elif len(var.shape) == 2:
            # assume lat, lon (fx field)
            axInd = 0
        try:
            print("enter try2")
            latLen = str(len(axes[axInd]))
            latVar = var.getLatitude()  # fH["latitude"]
            lat0 = str(np.min(latVar))
            print("lat0")
            print(lat0)
            latN = str(np.max(latVar))
            lon = str(len(axes[axInd + 1]))
            lonVar = var.getLongitude()  # fH["longitude"]
            lon0 = str(np.min(lonVar))
            lonN = str(np.max(lonVar))
            if len(var.shape) == 4:
                heightLen = str(len(axes[1]))
                heightVar = var.getLevel()
                height0 = str(heightVar[0])
                heightN = str(heightVar[-1])
                heightUnit = heightVar.units
            else:
                heightLen, height0, heightN = ["x" for _ in range(3)]
        except:
            print("no valid dims")

    # create grid_info dictionary
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
        "b",
        "b_bnds",
        "basin",
        "bnds",
        "d2",
        "depth",
        "depth_bnds",
        "landuse",
        "lat",
        "lat_bnds",
        "latitude",
        "lev",
        "lev_bnds",
        "lon",
        "lon_bnds",
        "longitude",
        "height",
        "height_bnds",
        "hist_interval",
        "p0",
        "ps",
        "sector",
        "strlen",
        "time_bnds",
        "type",
        "ygre",
        "xgre",
    ]

    tmp = {}
    fH = cdms2.open(filePath)
    for cnt, globalAtt in enumerate(globalAtts):
        try:
            val = eval("".join(["fH.", globalAtt]))
            if isinstance(val, np.ndarray):
                val = val.tolist()
            ###print("get:", globalAtt, val)
        except:
            ###print("No entry:", globalAtt)
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
        == ""
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
    ):
        pdb.set_trace()
    # debug close
    varNames = fH.variables
    # deal with ps var
    if "/Amon/ps" in filePath:
        excludeVars.remove("ps")
    varName = "".join(set(varNames) - set(excludeVars))
    var = fH[varName]
    tmp["grid_info"] = getAxes(var)
    # print("grid_info")
    # print(tmp["grid_info"])

    # add list of non-queried globalAtts
    tmp["||_unvalidated"] = list(set(fH.attributes).difference(globalAtts))
    fH.close()

    return tmp


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


# %% define path
hostPath = "/p/css03/esgf_publish/CMIP6/"
testPath = (
    # "/p/css03/esgf_publish/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r1i1p1f1/Omon"
    # "/p/css03/esgf_publish/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r1i1p1f1"
    # "/p/css03/esgf_publish/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical"
    # "/p/css03/esgf_publish/CMIP6/PMIP/CAS/FGOALS-f3-L/lig127k/r1i1p1f1/SImon/"  # i, j index checks
    "/p/css03/esgf_publish/CMIP6"
)

# %% loop over files and build index
x = scantree(testPath)
cmip = {}
cmip["version_metadata"] = {}
cmip["version_metadata"]["author"] = "Paul J. Durack <durack1@llnl.gov>"
cmip["version_metadata"]["institution_id"] = "PCMDI"
startTime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
cmip["version_metadata"]["start_time"] = startTime
for cnt, filePath in enumerate(x):
    # debug start
    indStart = -1
    if cnt < indStart:
        continue
    elif cnt == indStart:
        firstPath = "/".join(filePath.path.split("/")[0:-1])
    # debug end
    # deal with multiple files - e.g. Omon
    if cnt == 0:
        firstPath = "/".join(filePath.path.split("/")[0:-1])
    if firstPath not in filePath.path:
        firstPath = "/".join(filePath.path.split("/")[0:-1])
        # print(count, filePath.name)  # filename only
        print(cnt, filePath.path)  # path and filename complete
        # build DRS institution_id.source_id.activity_id.experiment_id.variant_label
        key = getDrs(filePath.path)
        if key in cmip:
            # pull global atts and compare, note if different
            dic2 = getGlobalAtts(filePath.path)
            dic1 = cmip[key]
            update, newDic = compareDicts(dic1, dic2, cnt, filePath.path)
            # if difference found, update new entry
            if update:
                cmip[key] = newDic
        else:
            # pull global atts for new entry
            cmip[key] = {}
            tmp = getGlobalAtts(filePath.path)
            cmip[key] = tmp
    elif firstPath in filePath.path:
        pass
        # print('dupe files, skipping')

    # %% iteratively write out results to local file
    if not cnt % 1000:
        if os.path.exists("*CMIP6-metaData.json"):
            os.remove("*CMIP6-metaData.json")
        # get time
        timeNow = datetime.datetime.now()
        timeFormat = timeNow.strftime("%Y-%m-%d")
        timeFormatDir = timeNow.strftime("%y%m%d")
        endTime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        cmip["version_metadata"]["end_time  "] = endTime
        # Write output
        print("")
        outFile = "_".join([timeFormatDir, "CMIP6-metaData.json"])
        print(
            "writing:",
        )
        print("")
        fH = open(outFile, "w")
        json.dump(
            cmip, fH, ensure_ascii=True, sort_keys=True, indent=4, separators=(",", ":")
        )
        fH.close()

# %% and write out final file
# get time
timeNow = datetime.datetime.now()
timeFormat = timeNow.strftime("%Y-%m-%d")
timeFormatDir = timeNow.strftime("%y%m%d")
endTime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
cmip["version_metadata"]["end_time  "] = endTime
# Write output
outFile = "_".join([timeFormatDir, "CMIP6-metaData.json"])
fH = open(outFile, "w")
json.dump(
    cmip, fH, ensure_ascii=True, sort_keys=True, indent=4, separators=(",", ":")
)  # , encoding="utf-8")
fH.close()
