#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 12:24:53 2018

@author: durack1
"""
import json,os

#%% 180223 1129 - latest versions below
#CMIP6_activity_id.json Thu Sep 7 10:30:00 2017 -0700 'Issue397 durack1 augment activity_id with description (#400)' https://github.com/WCRP-CMIP/CMIP6_CVs/commit/c28217095e8ca770b6cd63fa97b8d022ca52aea7
#CMIP6_experiment_id.json Wed Nov 8 10:26:00 2017 -0700 'Issue423 durack1 correct experiment_id components LUMIP LS3MIP (#437)' https://github.com/WCRP-CMIP/CMIP6_CVs/commit/3bbbc883bfaf7a8f99cd50603bbf3199491d7c49
#CMIP6_frequency.json Fri Oct 27 14:03:00 2017 -0700 'Issue414 durack1 revise frequency 1hrCM definition (#418)' https://github.com/WCRP-CMIP/CMIP6_CVs/commit/62129c480e970cf22a5ca31b169bca2e21cb2b9d
#CMIP6_grid_label.json Fri Sep 8 18:12:00 2017 -0700 'Issue395 durack1 augment grid_label with description (#401)' https://github.com/WCRP-CMIP/CMIP6_CVs/commit/d5ab3b13221bad7abe52def13689062886366b9b
#CMIP6_institution_id.json Thu Feb 22 16:04:00 2018 -0700 'Issue459 durack1 register institution_id AER (#462)' https://github.com/WCRP-CMIP/CMIP6_CVs/commit/eacd16e330d985ae8694a6cb738b253a7d265611
#CMIP6_license.json Mon Feb 27 10:30:00 2017 -0700 'Issue225 durack1 add institution_id THU (#232)' https://github.com/WCRP-CMIP/CMIP6_CVs/commit/7917f3bc2fc4739808f5fa05870ab35411bd4f44
#CMIP6_nominal_resolution.json Tues Nov 15 16:04:00 2016 -0700 'Issue141 durack1 update grid_resolution to nominal_resolution (#143)' https://github.com/WCRP-CMIP/CMIP6_CVs/commit/c45c83d65814fa3caaa965554f0d7eb74b80a186
#CMIP6_realm.json Tues Apr 18 12:03:00 2017 -0700 'Issue285 durack1 update realm format (#290)' https://github.com/WCRP-CMIP/CMIP6_CVs/commit/7de3c77a3cf91dd6c34509024d5493e40b1c8d9d
#CMIP6_required_global_attributes.json Thu Mar 16 12:59:00 2017 -0700 'deleted trailing comma from list' https://github.com/WCRP-CMIP/CMIP6_CVs/commit/534fa1b7ac02a92c6b7e2e770f4e34d73ae94d4c
#CMIP6_source_id.json Fri Feb 23 11:20:00 2018 -0700 'Issue457 durack1 revise source_id entries HadGEM3 and UKESM1 (#464)' https://github.com/WCRP-CMIP/CMIP6_CVs/commit/c35e10ff690a1e36ac20f4ef3f5b73374fd440ec
#CMIP6_source_type.json Fri Sep 8 17:57:00 2017 -0700 'Issue396 durack1 augment source_type with description (#399)' https://github.com/WCRP-CMIP/CMIP6_CVs/commit/fa3f07e9c215b35e0a54737acba2c2a9f6b8901f
#CMIP6_sub_experiment_id.json Wed Mar 8 11:27:00 2017 -0700 'Issue1 durack1 update experiment_id from spreadsheet (MIP-chair review) (#241)' https://github.com/WCRP-CMIP/CMIP6_CVs/commit/af9202b7e26d357aa988c1741b7a25f90fdedbfd
#CMIP6_table_id.json Fri Jan 13 09:27:00 2017 -0700 'Issue199 durack1 update table_id to Data Request v1.0 (#200)' https://github.com/WCRP-CMIP/CMIP6_CVs/commit/f4a9fc202b7bea32038d92791cbce95af75022ab
#README.md Wed Mar 22 09:46:00 2017 -0700 'shortened through minor edits' https://github.com/WCRP-CMIP/CMIP6_CVs/commit/412f96f8df75be49b77bb9b55455fab7c7b260b4
#mip_era.json Thu Aug 25 17:21:00 2016 -0700 'Fix #36 - Add CV name to json structure' https://github.com/WCRP-CMIP/CMIP6_CVs/commit/317f9e6b0a8ea1dbd85a61a5a1420c1972a6d12b
#"version_metadata":{
# "author":"Paul J. Durack <durack1@llnl.gov>",
# "creation_date":"Tue Feb 13 09:37:18 2018 -0800",
# "institution_id":"PCMDI",
# "latest_tag_point":"3.3.0 (27; gf660143)",
# "note":"Revise institution_id NCAR",
# "previous_commit":"ba68f67c7773020ef7b8a5b67e68add47f0f6de3"
# }

#%% Create versionHistory
versionHistory = {}
# Initialize all version history
versionHistory['versions'] = {}
versionHistory['versions']['versionMIPEra'] = 6 ; # CMIP6
versionHistory['versions']['versionCVStructure'] = 2 ; # Aligns with http://goo.gl/v1drZl (CMIP6 Global Attributes, DRS, Filenames, Directory Structure, and CV’s)
versionHistory['versions']['versionCVContent'] = 1 ; # Initialize auto-versioning using 1, updates 6.2.0.11
versionHistory['versions']['versionCVCommit'] = 0
# versionMIPEra - CMIP6 id - The first integer is “6”, indicating the CV collection is for use in CMIP6
# versionCVStructure - Incremented when the structure/format of CV’s changes or a new CV is added
# versionCVContent - Incremented when a change to existing content is made other than “source_id” or “institution_id”
# versionCVCommit - Incremented whenever a new source_id and/or institution_id is added or amended
# Initialize all CV history
key = 'activity_id'
versionHistory[key] = {}
versionHistory[key]['timeStamp'] = 'Thu Sep 7 10:30:00 2017 -0700'
versionHistory[key]['commitMessage'] = 'Issue397 durack1 augment activity_id with description (#400)'
versionHistory[key]['URL'] = 'https://github.com/WCRP-CMIP/CMIP6_CVs/commit/c28217095e8ca770b6cd63fa97b8d022ca52aea7'
versionHistory[key]['MD5'] = 'c28217095e8ca770b6cd63fa97b8d022ca52aea7'
key = 'experiment_id'
versionHistory[key] = {}
versionHistory[key]['timeStamp'] = 'Wed Nov 8 10:26:00 2017 -0700'
versionHistory[key]['commitMessage'] = 'Issue423 durack1 correct experiment_id components LUMIP LS3MIP (#437)'
versionHistory[key]['URL'] = 'https://github.com/WCRP-CMIP/CMIP6_CVs/commit/3bbbc883bfaf7a8f99cd50603bbf3199491d7c49'
versionHistory[key]['MD5'] = '3bbbc883bfaf7a8f99cd50603bbf3199491d7c49'
key = 'frequency'
versionHistory[key] = {}
versionHistory[key]['timeStamp'] = 'Fri Oct 27 14:03:00 2017 -0700'
versionHistory[key]['commitMessage'] = 'Issue414 durack1 revise frequency 1hrCM definition (#418)'
versionHistory[key]['URL'] = 'https://github.com/WCRP-CMIP/CMIP6_CVs/commit/62129c480e970cf22a5ca31b169bca2e21cb2b9d'
versionHistory[key]['MD5'] = '62129c480e970cf22a5ca31b169bca2e21cb2b9d'
key = 'grid_label'
versionHistory[key] = {}
versionHistory[key]['timeStamp'] = 'Fri Sep 8 18:12:00 2017 -0700'
versionHistory[key]['commitMessage'] = 'Issue395 durack1 augment grid_label with description (#401)'
versionHistory[key]['URL'] = 'https://github.com/WCRP-CMIP/CMIP6_CVs/commit/d5ab3b13221bad7abe52def13689062886366b9b'
versionHistory[key]['MD5'] = 'd5ab3b13221bad7abe52def13689062886366b9b'
key = 'institution_id'
versionHistory[key] = {}
versionHistory[key]['timeStamp'] = 'Thu Feb 22 16:04:00 2018 -0700'
versionHistory[key]['commitMessage'] = 'Issue459 durack1 register institution_id AER (#462)'
versionHistory[key]['URL'] = 'https://github.com/WCRP-CMIP/CMIP6_CVs/commit/eacd16e330d985ae8694a6cb738b253a7d265611'
versionHistory[key]['MD5'] = 'eacd16e330d985ae8694a6cb738b253a7d265611'
key = 'license'
versionHistory[key] = {}
versionHistory[key]['timeStamp'] = 'Mon Feb 27 10:30:00 2017 -0700'
versionHistory[key]['commitMessage'] = 'Issue225 durack1 add institution_id THU (#232)'
versionHistory[key]['URL'] = 'https://github.com/WCRP-CMIP/CMIP6_CVs/commit/7917f3bc2fc4739808f5fa05870ab35411bd4f44'
versionHistory[key]['MD5'] = '7917f3bc2fc4739808f5fa05870ab35411bd4f44'
key = 'nominal_resolution'
versionHistory[key] = {}
versionHistory[key]['timeStamp'] = 'Tues Nov 15 16:04:00 2016 -0700'
versionHistory[key]['commitMessage'] = 'Issue141 durack1 update grid_resolution to nominal_resolution (#143)'
versionHistory[key]['URL'] = 'https://github.com/WCRP-CMIP/CMIP6_CVs/commit/c45c83d65814fa3caaa965554f0d7eb74b80a186'
versionHistory[key]['MD5'] = 'c45c83d65814fa3caaa965554f0d7eb74b80a186'
key = 'realm'
versionHistory[key] = {}
versionHistory[key]['timeStamp'] = 'Tues Apr 18 12:03:00 2017 -0700'
versionHistory[key]['commitMessage'] = 'Issue285 durack1 update realm format (#290)'
versionHistory[key]['URL'] = 'https://github.com/WCRP-CMIP/CMIP6_CVs/commit/7de3c77a3cf91dd6c34509024d5493e40b1c8d9d'
versionHistory[key]['MD5'] = '7de3c77a3cf91dd6c34509024d5493e40b1c8d9d'
key = 'required_global_attributes'
versionHistory[key] = {}
versionHistory[key]['timeStamp'] = 'Thu Mar 16 12:59:00 2017 -0700'
versionHistory[key]['commitMessage'] = 'deleted trailing comma from list'
versionHistory[key]['URL'] = 'https://github.com/WCRP-CMIP/CMIP6_CVs/commit/534fa1b7ac02a92c6b7e2e770f4e34d73ae94d4c'
versionHistory[key]['MD5'] = '534fa1b7ac02a92c6b7e2e770f4e34d73ae94d4c'
key = 'source_id'
versionHistory[key] = {}
versionHistory[key]['timeStamp'] = 'Fri Feb 23 11:20:00 2018 -0700'
versionHistory[key]['commitMessage'] = 'Issue457 durack1 revise source_id entries HadGEM3 and UKESM1 (#464)'
versionHistory[key]['URL'] = 'https://github.com/WCRP-CMIP/CMIP6_CVs/commit/c35e10ff690a1e36ac20f4ef3f5b73374fd440ec'
versionHistory[key]['MD5'] = 'c35e10ff690a1e36ac20f4ef3f5b73374fd440ec'
key = 'source_type'
versionHistory[key] = {}
versionHistory[key]['timeStamp'] = 'Fri Sep 8 17:57:00 2017 -0700'
versionHistory[key]['commitMessage'] = 'Issue396 durack1 augment source_type with description (#399)'
versionHistory[key]['URL'] = 'https://github.com/WCRP-CMIP/CMIP6_CVs/commit/fa3f07e9c215b35e0a54737acba2c2a9f6b8901f'
versionHistory[key]['MD5'] = 'fa3f07e9c215b35e0a54737acba2c2a9f6b8901f'
key = 'sub_experiment_id'
versionHistory[key] = {}
versionHistory[key]['timeStamp'] = 'Wed Mar 8 11:27:00 2017 -0700'
versionHistory[key]['commitMessage'] = 'Issue1 durack1 update experiment_id from spreadsheet (MIP-chair review) (#241)'
versionHistory[key]['URL'] = 'https://github.com/WCRP-CMIP/CMIP6_CVs/commit/af9202b7e26d357aa988c1741b7a25f90fdedbfd'
versionHistory[key]['MD5'] = 'af9202b7e26d357aa988c1741b7a25f90fdedbfd'
key = 'table_id'
versionHistory[key] = {}
versionHistory[key]['timeStamp'] = 'Fri Jan 13 09:27:00 2017 -0700'
versionHistory[key]['commitMessage'] = 'Issue199 durack1 update table_id to Data Request v1.0 (#200)'
versionHistory[key]['URL'] = 'https://github.com/WCRP-CMIP/CMIP6_CVs/commit/f4a9fc202b7bea32038d92791cbce95af75022ab'
versionHistory[key]['MD5'] = 'f4a9fc202b7bea32038d92791cbce95af75022ab'
key = 'mip_era'
versionHistory[key] = {}
versionHistory[key]['timeStamp'] = 'Thu Aug 25 17:21:00 2016 -0700'
versionHistory[key]['commitMessage'] = 'Fix #36 - Add CV name to json structure'
versionHistory[key]['URL'] = 'https://github.com/WCRP-CMIP/CMIP6_CVs/commit/317f9e6b0a8ea1dbd85a61a5a1420c1972a6d12b'
versionHistory[key]['MD5'] = 'f9e6b0a8ea1dbd85a61a5a1420c1972a6d12b'

# Create host dictionary
jsonDict = {}
jsonDict['versionHistory'] = versionHistory
outFile = 'versionHistory.json'
if os.path.exists(outFile):
    os.remove(outFile)
fH = open(outFile, 'w')
json.dump(
    jsonDict,
    fH,
    ensure_ascii=True,
    sort_keys=True,
    indent=4,
    separators=(
        ',',
        ':'),
    encoding="utf-8")
fH.close()