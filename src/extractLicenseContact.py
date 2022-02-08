#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 14:41:24 2022

Paul J. Durack 8th February 2022

This script polls all CMIP6 data and extracts license and contact information

@author: durack1
"""

# %% imports
import cdms2
import json
from os import scandir

# %% function defs


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

    for entry in scandir.walk(path):
        # yield directory if there are any files in it
        if (entry[2] != []):
            yield entry[0] + '/'


# %% define search facets
searchKeys = ['activity_id', 'experiment_id', 'institution_id', 'source_id']
globalAtts = ['activity_id', 'branch_method', 'branch_time_in_child', 'branch_time_in_parent',
              'contact', 'experiment_id', 'forcing_index', 'frequency', 'further_info_url',
              'initialization_index', 'institution_id', 'license', 'mip_era', 'nominal_resolution',
              'parent_activity_id', 'parent_experiment_id', 'parent_mip_era', 'parent_source_id',
              'parent_time_uits', 'parent_variant_label', 'physics_index', 'realization_index',
              'realm', 'source_id', 'table_id', 'variable_id', 'variant_label',
              'version', 'cmor_version', 'tracking_id', 'license']

# %% define path
hostPath = '/p/css03/esgf_publish/CMIP6/'
testPath = '/p/css03/esgf_publish/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r1i1p1f1/Amon'

# %% loop over files and build index
x = scantree(testPath)
cmip6 = {}
for count, filePath in x:
    print(count, filePath)
