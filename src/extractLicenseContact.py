#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 14:41:24 2022

Paul J. Durack 8th February 2022

This script polls all CMIP6 data and extracts license and contact information

PJD  9 Feb 2022     - Updated to validate and catch inconsistencies
PJD  9 Feb 2022     - Updated to get alertError working

@author: durack1
"""

# %% imports
import cdms2
import datetime
import json
import pdb
from os import scandir

# %% function defs
def alertError():
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
    message = "Subject: {}\n\n{}".format(subject, body)
    with smtplib.SMTP(smtp_server) as server:
        server.sendmail(sender_email, to, message)
def compareDicts(dict1, dict2):
    """
    compareDicts(dict1, dict2)

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
                "Key: {}, Value 1: {}, Value 2: {}".format(key, dict1[key], dict2[key])
            )
            pdb.set_trace()
            # set(globalAtts).difference(chkGlobalAtts)
            # {'frequency', 'realm', 'table_id', 'tracking_id', 'variable_id'}
            key2 = ".".join([dict2["table_id"], dict2["variable_id"]])
            dict1[key][key2] = dict2[key]
            update = True
        else:
            update = False

    return update, dict1


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
    tmp = {}
    fH = cdms2.open(filePath)
    for cnt, globalAtt in enumerate(globalAtts):
        try:
            val = eval("".join(["fH.", globalAtt]))
            print("get:", globalAtt, val)
        except:
            print("No entry:", globalAtt)
            val = ""
        tmp[globalAtt] = val
    # add list of non-queried globalAtts
    tmp["unvalidated"] = list(set(fH.attributes).difference(globalAtts))
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
    "/p/css03/esgf_publish/CMIP6"
)

# %% loop over files and build index
x = scantree(testPath)
cmip = {}
cmip["version_metadata"] = {}
startTime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
cmip["version_metadata"]["start_time"] = startTime
for cnt1, filePath in enumerate(x):
    # deal with multiple files - e.g. Omon
    if cnt1 == 0:
        firstPath = "/".join(filePath.path.split("/")[0:-1])
    if firstPath not in filePath.path:
        firstPath = "/".join(filePath.path.split("/")[0:-1])
        # print(count, filePath.name)  # filename only
        print(cnt1, filePath.path)  # path and filename complete
        # build DRS institution_id.source_id.activity_id.experiment_id.variant_label
        key = getDrs(filePath.path)
        if key in cmip:
            # pull global atts and compare, note if different
            dic2 = getGlobalAtts(filePath.path)
            dic1 = cmip[key]
            update, newDic = compareDicts(dic1, dic2)
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

# %% write out results to local file
# get time
timeNow = datetime.datetime.now()
timeFormat = timeNow.strftime("%Y-%m-%d")
timeFormatDir = timeNow.strftime("%y%m%d")
endTime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
cmip["version_metadata"]["end_time"] = endTime
# Write output
outFile = "_".join([timeFormatDir, "CMIP6-metaData.json"])
fH = open(outFile, "w")
json.dump(
    cmip, fH, ensure_ascii=True, sort_keys=True, indent=4, separators=(",", ":")
)  # , encoding="utf-8")
fH.close()
