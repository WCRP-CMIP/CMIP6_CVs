#!/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 14:12:21 2016

Paul J. Durack 11th July 2016

This script generates all controlled vocabulary (CV) json files residing this this subdirectory

PJD 11 Jul 2016    - Started
PJD 12 Jul 2016    - Read experiments from https://github.com/PCMDI/cmip6-cmor-tables/blob/CMIP6_CV/Tables/CMIP6_CV.json
PJD 12 Jul 2016    - Format tweaks and typo corrections
PJD 12 Jul 2016    - Added source_id ('GFDL-CM2-1': 'GFDL CM2.1' as example)
PJD 12 Jul 2016    - Corrected mip_era to be CMIP6-less
PJD 12 Jul 2016    - Indent/format cleanup
PJD 13 Jul 2016    - Further tweaks to cleanup experiment json
PJD 13 Jul 2016    - Added required_global_attributes (Denis Nadeau)
PJD 13 Jul 2016    - Further tweaks to resolve specifics https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1
PJD 13 Jul 2016    - Updating institution following https://github.com/WCRP-CMIP/CMIP6_CVs/issues/3
PJD 13 Jul 2016    - Further tweaks to institution
PJD 14 Jul 2016    - Updated source_id to include institution https://github.com/WCRP-CMIP/CMIP6_CVs/issues/8
PJD 14 Jul 2016    - Renamed experiment to experiment_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/10
PJD 14 Jul 2016    - Renamed institution to institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/12
PJD 14 Jul 2016    - Added coordinate https://github.com/WCRP-CMIP/CMIP6_CVs/issues/7
PJD 14 Jul 2016    - Added grid https://github.com/WCRP-CMIP/CMIP6_CVs/issues/6
PJD 14 Jul 2016    - Added formula_terms https://github.com/WCRP-CMIP/CMIP6_CVs/issues/5
PJD 15 Jul 2016    - Added further cleanup of imported dictionaries
PJD 20 Jul 2016    - Updated VolMIP experiment info https://github.com/WCRP-CMIP/CMIP6_CVs/issues/19
PJD 11 Aug 2016    - Added readJsonCreateDict function
PJD 11 Aug 2016    - Converted experiment_id source from github
PJD 11 Aug 2016    - Updated frequency to include 1hrClimMon https://github.com/WCRP-CMIP/CMIP6_CVs/issues/24
PJD 11 Aug 2016    - Updated LUMIP experiment names https://github.com/WCRP-CMIP/CMIP6_CVs/issues/27
PJD 15 Aug 2016    - Update experiment_id to be self-consistent (LUMIP renames complete)
PJD 15 Aug 2016    - Converted readJsonCreateDict to source from durolib
PJD 15 Aug 2016    - Further tweaks to LUMIP experiment_id @dlawrenncar https://github.com/WCRP-CMIP/CMIP6_CVs/issues/27
PJD 25 Aug 2016    - Added license https://github.com/WCRP-CMIP/CMIP6_CVs/issues/35
PJD 25 Aug 2016    - Updated source_id contents and format https://github.com/WCRP-CMIP/CMIP6_CVs/issues/34
PJD 25 Aug 2016    - Add CV name to json structure https://github.com/WCRP-CMIP/CMIP6_CVs/issues/36
PJD 26 Aug 2016    - Add repo version/metadata https://github.com/WCRP-CMIP/CMIP6_CVs/issues/28
PJD 31 Aug 2016    - Added mip_era to source_id
PJD 31 Aug 2016    - Correct repo user info
PJD 31 Aug 2016    - Remove CMIP6_variable.json from repo https://github.com/WCRP-CMIP/CMIP6_CVs/issues/45
PJD  1 Sep 2016    - Updated version info to per file (was repo) https://github.com/WCRP-CMIP/CMIP6_CVs/issues/28
PJD  1 Sep 2016    - Automated update of html
PJD 15 Sep 2016    - Further tweaks to version info https://github.com/WCRP-CMIP/CMIP6_CVs/issues/28
PJD 15 Sep 2016    - Updated source_id to maintain consistency with ES-DOCs https://github.com/WCRP-CMIP/CMIP6_CVs/issues/53
PJD 28 Sep 2016    - Correct activity_id to MIP -> CMIP typo https://github.com/WCRP-CMIP/CMIP6_CVs/issues/57
PJD 28 Sep 2016    - Add new grid_label entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/49
PJD  3 Oct 2016    - Added "cohort" to source_id ACCESS-1-0 example https://github.com/WCRP-CMIP/CMIP6_CVs/issues/64
PJD  3 Oct 2016    - Added institution_id NUIST https://github.com/WCRP-CMIP/CMIP6_CVs/issues/63
PJD  4 Oct 2016    - Added institution_id NIMS-KMA https://github.com/WCRP-CMIP/CMIP6_CVs/issues/67
PJD  4 Oct 2016    - Revised tiers for AerChemMIP experiments https://github.com/WCRP-CMIP/CMIP6_CVs/issues/69
PJD  4 Oct 2016    - Added AerChemMIP experiments piClim-SO2 piClim-OC piClim-NH3 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/68
PJD  1 Nov 2016    - Update to upstream sources; Convert to per-file commits
PJD  1 Nov 2016    - Add PCMDI-test-1-0 to source_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/102
PJD  2 Nov 2016    - Add CSIR to institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/100
PJD  2 Nov 2016    - Update BNU institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/98
PJD  2 Nov 2016    - Add EC-Earth-Consortium to institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/90
PJD  2 Nov 2016    - Update MIROC institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/89
PJD  2 Nov 2016    - Add CCCR-IITM to institution_id and IITM-ESM to source_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/96
PJD  2 Nov 2016    - Update deforest-globe experiment_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/97
PJD  2 Nov 2016    - Remove RFMIP experiment_ids piClim-aerO3x0p1 and piClim-aerO3x2 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/79
PJD  2 Nov 2016    - Revise RFMIP experiment_ids hist-all-spAerO3 and hist-spAerO3 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/80
PJD  2 Nov 2016    - Revise RFMIP experiment_ids capitalization https://github.com/WCRP-CMIP/CMIP6_CVs/issues/81
PJD  2 Nov 2016    - Revise RFMIP experiment_ids spAerO3 -> spAer https://github.com/WCRP-CMIP/CMIP6_CVs/issues/82
PJD  2 Nov 2016    - Revise experiment_id ssp370 to include activity_id AerChemMIP https://github.com/WCRP-CMIP/CMIP6_CVs/issues/77
PJD  2 Nov 2016    - Revise experiment_id volc-cluster-mill https://github.com/WCRP-CMIP/CMIP6_CVs/issues/75
PJD  2 Nov 2016    - Revise experiment_id instances of LND -> LAND https://github.com/WCRP-CMIP/CMIP6_CVs/issues/74
PJD  2 Nov 2016    - Add experiment_id ism-ctrl-std https://github.com/WCRP-CMIP/CMIP6_CVs/issues/103
PJD  2 Nov 2016    - Add experiment_id ism-asmb-std https://github.com/WCRP-CMIP/CMIP6_CVs/issues/104
PJD  2 Nov 2016    - Add experiment_id ism-bsmb-std https://github.com/WCRP-CMIP/CMIP6_CVs/issues/105
PJD  3 Nov 2016    - Deal with invalid source_type syntax, rogue ","
PJD  8 Nov 2016    - Add CNRM to institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/129
PJD  8 Nov 2016    - Revise source_type https://github.com/WCRP-CMIP/CMIP6_CVs/issues/131
PJD 15 Nov 2016    - Remove coordinate, formula_terms and grids from repo https://github.com/WCRP-CMIP/CMIP6_CVs/issues/139
PJD 15 Nov 2016    - Rename grid_resolution to nominal_resolution and add new entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/141
PJD 15 Nov 2016    - Add MESSy-Consortium to institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/138
PJD 16 Nov 2016    - Revise AerChemMIP experiment model configurations https://github.com/WCRP-CMIP/CMIP6_CVs/issues/78
PJD 16 Nov 2016    - Add source_id VRESM-1-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/101
PJD 17 Nov 2016    - Revise grid_label to include Antarctica and Greenland https://github.com/WCRP-CMIP/CMIP6_CVs/issues/130
PJD 21 Nov 2016    - Revise institution_id NCC https://github.com/WCRP-CMIP/CMIP6_CVs/issues/83
PJD 21 Nov 2016    - Revise experiment_id 1pctCO2Ndep https://github.com/WCRP-CMIP/CMIP6_CVs/issues/73
PJD 21 Nov 2016    - Register source_id BNU-ESM-1-1 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/99
PJD 21 Nov 2016    - Register source_id EC-Earth-3 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/91
PJD 21 Nov 2016    - Register source_id EC-Earth-3-HR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/92
PJD 21 Nov 2016    - Register source_id EC-Earth-3-LR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/93
PJD 21 Nov 2016    - source_id cleanup, particularly for IITM-ESM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/96
PJD 21 Nov 2016    - Register institution_id CNRM-CERFACS https://github.com/WCRP-CMIP/CMIP6_CVs/issues/115
PJD 28 Nov 2016    - Register source_id NorESM2-LME https://github.com/WCRP-CMIP/CMIP6_CVs/issues/84
PJD 28 Nov 2016    - Register source_id NorESM2-MH https://github.com/WCRP-CMIP/CMIP6_CVs/issues/85
PJD 28 Nov 2016    - Register source_id NorESM2-LMEC https://github.com/WCRP-CMIP/CMIP6_CVs/issues/86
PJD 28 Nov 2016    - Register source_id NorESM2-HH https://github.com/WCRP-CMIP/CMIP6_CVs/issues/87
PJD 28 Nov 2016    - Register source_id NorESM2-MM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/88
PJD 28 Nov 2016    - Register source_id NorESM2-LM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/156
PJD 28 Nov 2016    - Revise multiple source_id NorESM* https://github.com/WCRP-CMIP/CMIP6_CVs/issues/156
PJD  7 Dec 2016    - Update activity_id for experiment_id ssp370 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/169#issuecomment-264726036
PJD  7 Dec 2016    - Add experiment_id 1pctCO2-4xext https://github.com/WCRP-CMIP/CMIP6_CVs/issues/170
PJD  7 Dec 2016    - Add institution_id html https://github.com/WCRP-CMIP/CMIP6_CVs/issues/172
PJD 14 Dec 2016    - Add frequency_id 1hr https://github.com/WCRP-CMIP/CMIP6_CVs/issues/178
PJD 14 Dec 2016    - Add source_id GISS-E2-1 variants https://github.com/WCRP-CMIP/CMIP6_CVs/issues/177
PJD  3 Jan 2017    - Add institution_id NERC https://github.com/WCRP-CMIP/CMIP6_CVs/issues/183
PJD  3 Jan 2017    - Update source_id EC-Earth-3-LR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/93
PJD  3 Jan 2017    - Register source_id EC-Earth-3-CC https://github.com/WCRP-CMIP/CMIP6_CVs/issues/94
PJD  3 Jan 2017    - Register source_ids HadGEM3*4 and UKESM1*2 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/184
PJD  3 Jan 2017    - Revise CMIP6 license text https://github.com/WCRP-CMIP/CMIP6_CVs/issues/133
PJD  3 Jan 2017    - Register source_ids CNRM-ESM2*2 and CNRM-CM6*2 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/115
PJD  5 Jan 2017    - Revise multiple CNRM source_ids atmospheric chemistry entry https://github.com/WCRP-CMIP/CMIP6_CVs/issues/115
PJD  5 Jan 2017    - Register multiple EC-Earth3 source_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/191
PJD  5 Jan 2017    - Update DCPP experiment_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1#issuecomment-268357110
PJD 10 Jan 2017    - Register multiple EC-Earth3 source_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/195, 196, 197
PJD 13 Jan 2017    - Update table_id to reflect Data Request V1.0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/199
PJD 18 Jan 2017    - Update experiment_id highres-future start_year https://github.com/WCRP-CMIP/CMIP6_CVs/issues/201
PJD 18 Jan 2017    - Add experiment_id spinup-1950 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/202
PJD 19 Jan 2017    - Update institution_id FIO -> FIO-SOA https://github.com/WCRP-CMIP/CMIP6_CVs/issues/205
PJD 21 Jan 2017    - Register institution_id AWI https://github.com/WCRP-CMIP/CMIP6_CVs/issues/207
PJD 21 Jan 2017    - Register source_id AWI-CM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/210
PJD 23 Jan 2017    - Update institution_id FIO-SOA -> FIO-RONM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/209
PJD 23 Jan 2017    - Register source_id MRI-ESM2-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/208
PJD 23 Jan 2017    - Revise experiment_id values for ISMIP https://github.com/WCRP-CMIP/CMIP6_CVs/issues/168
PJD 23 Jan 2017    - Revise source_id MRI-ESM2-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/208
PJD 30 Jan 2017    - Register source_id EMAC-2-53-AerChem https://github.com/WCRP-CMIP/CMIP6_CVs/issues/217
PJD 31 Jan 2017    - Revise source_id EMAC-2-53-AerChem https://github.com/WCRP-CMIP/CMIP6_CVs/issues/217
PJD  6 Feb 2017    - Revise license details
PJD  6 Feb 2017    - Register source_id AWI-CM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/210
PJD  6 Feb 2017    - Revise multiple EC-Earth3 source_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/191
PJD 27 Feb 2017    - Update license info
PJD 27 Feb 2017    - Register institution_id THU https://github.com/WCRP-CMIP/CMIP6_CVs/issues/225
PJD 27 Feb 2017    - Register source_id CIESM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/226
PJD  3 Mar 2017    - Register source_id MRI-ESM2-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/234
PJD  3 Mar 2017    - Register source_id MIROC6 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/229
PJD  3 Mar 2017    - Update all source_id cohort entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/230
PJD  7 Mar 2017    - Register source_id EMAC-2-53-Vol https://github.com/WCRP-CMIP/CMIP6_CVs/issues/231
PJD  7 Mar 2017    - Register source_ids MIROC-ES and NICAM variants https://github.com/WCRP-CMIP/CMIP6_CVs/pull/238
PJD  7 Mar 2017    - Update experiment_id from external xlsx https://github.com/WCRP-CMIP/CMIP6_CVs/issues/1, 61, 136, 137
PJD 14 Mar 2017    - Update source_id ACCESS-1-0 template
PJD 17 Mar 2017    - Cleanup required_global_attributes https://github.com/WCRP-CMIP/CMIP6_CVs/issues/250
PJD 17 Mar 2017    - Augment source_id info request https://github.com/WCRP-CMIP/CMIP6_CVs/issues/249
PJD 20 Mar 2017    - Register institution_id CAMS https://github.com/WCRP-CMIP/CMIP6_CVs/issues/245
PJD 22 Mar 2017    - Revise experiment_id names and details for 2 RFMIP experiments https://github.com/WCRP-CMIP/CMIP6_CVs/issues/258
PJD 29 Mar 2017    - Revise experiment_id piClim-aer https://github.com/WCRP-CMIP/CMIP6_CVs/issues/261
PJD  5 Apr 2017    - Remove deprecated table_id entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/266
PJD  5 Apr 2017    - Convert experiment_id parent* entries to list https://github.com/WCRP-CMIP/CMIP6_CVs/issues/267
PJD  7 Apr 2017    - Register GFDL source_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/244
PJD  7 Apr 2017    - Register source_id CAMS_CSM1-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/246
PJD  8 Apr 2017    - Update multiple NorESM source_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/259
PJD  8 Apr 2017    - Update html markup https://github.com/WCRP-CMIP/CMIP6_CVs/issues/248
PJD 10 Apr 2017    - Revise source_id NorESM2-MH https://github.com/WCRP-CMIP/CMIP6_CVs/issues/259
PJD 12 Apr 2017    - Revise frequency to include yrClim https://github.com/WCRP-CMIP/CMIP6_CVs/issues/281
PJD 12 Apr 2017    - Add missing activity_id values https://github.com/WCRP-CMIP/CMIP6_CVs/issues/276
PJD 17 Apr 2017    - Register institution_id INPE https://github.com/WCRP-CMIP/CMIP6_CVs/issues/286
PJD 17 Apr 2017    - Register institution_id CMCC https://github.com/WCRP-CMIP/CMIP6_CVs/issues/284
PJD 17 Apr 2017    - Update realm format https://github.com/WCRP-CMIP/CMIP6_CVs/issues/285
PJD 18 Apr 2017    - Reconfigure source_id format to reflect all model components https://github.com/WCRP-CMIP/CMIP6_CVs/issues/264
PJD 18 Apr 2017    - Reconfigure json_to_html to deal with new source_id format
PJD 20 Apr 2017    - Revise AWI-CM source_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/210
PJD 21 Apr 2017    - Clean up None instances in source_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/301
PJD 21 Apr 2017    - Register source_id CMCC-CM2-SR5 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/292
PJD 21 Apr 2017    - Register source_id CMCC-CM2-HR5 and correct ocean entry for CMCC-CM2-SR5 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/293
PJD 21 Apr 2017    - Register source_id CMCC-CM2-HR4 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/294
PJD 21 Apr 2017    - Register source_id CMCC-CM2-VHR4 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/295
PJD 21 Apr 2017    - Register source_id CMCC-ESM2-SR5 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/296
PJD 21 Apr 2017    - Register source_id CMCC-ESM2-HR5 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/297
PJD 21 Apr 2017    - Revise CMCC source_id atmos entries (issues 292-294)
PJD 24 Apr 2017    - Revise source_id EMAC-2-53-AerChem https://github.com/WCRP-CMIP/CMIP6_CVs/issues/257
PJD 24 Apr 2017    - Revise source_id Revise source_id BNU-ESM-1-1 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/99
PJD 25 Apr 2017    - Register source_id BESM-2-7 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/287
PJD 26 Apr 2017    - Revise source_id CIESM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/226
PJD 26 Apr 2017    - Revise source_id BESM-2-7 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/287
PJD 11 May 2017    - Revise GFDL source_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/318
PJD 11 May 2017    - Revise source_id AWI-CM-1-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/319
PJD 11 May 2017    - Register multiple AWI source_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/320-322
PJD 17 May 2017    - Revise source_id EMAC-2-53-Vol https://github.com/WCRP-CMIP/CMIP6_CVs/issues/231
PJD 27 May 2017    - Rename and revise sspxy to ssp119 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/329
PJD 27 May 2017    - Revise source_id CanESM5 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/330
PJD 30 May 2017    - Revise institution_id NCAR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/335
PJD 30 May 2017    - Remove frequency 3hrClim https://github.com/WCRP-CMIP/CMIP6_CVs/issues/334
PJD  6 Jun 2017    - Revise multiple CNRM source_ids and CNRM-CERFACS institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/115
PJD 14 Jun 2017    - Revise multiple EC-EARTH3 source_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/191
PJD 14 Jun 2017    - Revise frequency decadal to dec https://github.com/WCRP-CMIP/CMIP6_CVs/issues/338
PJD 14 Jun 2017    - Rename experiment_id highresSST-4co2 -> highresSST-4xCO2 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/341
PJD 14 Jun 2017    - Update frequency format with identifiers -> highresSST-4xCO2 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/342
PJD 14 Jun 2017    - Rename experiment_id lfmip-pdL-princeton -> lfmip-pdLC-princeton https://github.com/WCRP-CMIP/CMIP6_CVs/issues/344
PJD 15 Jun 2017    - Correct experiment_id typo AeroChemMIP -> AerChemMIP in EC-Earth3-AerChem https://github.com/WCRP-CMIP/CMIP6_CVs/issues/352
PJD 15 Jun 2017    - Revise source_id MRI-ESM2-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/351
PJD 15 Jun 2017    - Revise multiple NASA-GISS source_id values https://github.com/WCRP-CMIP/CMIP6_CVs/issues/177
PJD 19 Jun 2017    - Revise INM institution_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/357
PJD 26 Jun 2017    - Register source_id INM-CM5-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/358
PJD 26 Jun 2017    - Register source_id INM-CM4-8 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/359
PJD 26 Jun 2017    - Register source_id INM-CM5-H https://github.com/WCRP-CMIP/CMIP6_CVs/issues/361
PJD 27 Jun 2017    - Revise multiple MOHC source_id entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/184, 343
PJD 27 Jun 2017    - Fix INM source_id formatting https://github.com/WCRP-CMIP/CMIP6_CVs/issues/358, 359, 361
PJD 27 Jun 2017    - Correct source_type BGCM to BGC https://github.com/WCRP-CMIP/CMIP6_CVs/issues/366
PJD 27 Jun 2017    - Remove unregistered institution_id entries (no source_id registrations) https://github.com/WCRP-CMIP/CMIP6_CVs/issues/362
PJD 29 Jun 2017    - Revise source_id IITM-ESM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/96
PJD 29 Jun 2017    - Revise multiple CNRM source_id values https://github.com/WCRP-CMIP/CMIP6_CVs/issues/115
PJD 29 Jun 2017    - Revise multiple MPI source_id values https://github.com/WCRP-CMIP/CMIP6_CVs/issues/197
PJD 29 Jun 2017    - Delete source_type ESM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/370
PJD 29 Jun 2017    - Correct source_id UKESM1-0-LL activity_participation error https://github.com/WCRP-CMIP/CMIP6_CVs/issues/371
PJD  5 Jul 2017    - Revise source_id CNRM-CM6-1 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/115
PJD 10 Jul 2017    - Revise multiple MPI source_id values https://github.com/WCRP-CMIP/CMIP6_CVs/issues/197
PJD 12 Jul 2017    - Revise multiple MOHC source_id values https://github.com/WCRP-CMIP/CMIP6_CVs/issues/184
PJD 17 Jul 2017    - Revise EC-EARTH3-HR source_id ocean description https://github.com/WCRP-CMIP/CMIP6_CVs/issues/191
PJD 26 Jul 2017    - Revise multiple MIROC source_id values https://github.com/WCRP-CMIP/CMIP6_CVs/issues/229
PJD 26 Jul 2017    - Register institution_id SNU https://github.com/WCRP-CMIP/CMIP6_CVs/issues/386
PJD 26 Jul 2017    - Register source_id SAM0-UNICON https://github.com/WCRP-CMIP/CMIP6_CVs/issues/387
PJD 27 Jul 2017    - Revise MIROC and SNU source_id values https://github.com/WCRP-CMIP/CMIP6_CVs/pull/385#issuecomment-318256867,
                     https://github.com/WCRP-CMIP/CMIP6_CVs/issues/387#issuecomment-318308002
PJD  2 Aug 2017    - Start work on per file versioning
PJD 10 Aug 2017    - Register source_id IPSL-CM6A-LR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/392
PJD  7 Sep 2017    - Augment activity_id format with description https://github.com/WCRP-CMIP/CMIP6_CVs/issues/397
PJD  8 Sep 2017    - Augment source_type format with description https://github.com/WCRP-CMIP/CMIP6_CVs/issues/396
PJD  8 Sep 2017    - Augment grid_label format with description https://github.com/WCRP-CMIP/CMIP6_CVs/issues/395
PJD  8 Sep 2017    - Revise frequency entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/345
PJD 21 Sep 2017    - Register institution_id HAMMOZ-Consortium https://github.com/WCRP-CMIP/CMIP6_CVs/issues/402
PJD 21 Sep 2017    - Register institution_id BCC https://github.com/WCRP-CMIP/CMIP6_CVs/issues/405
PJD 26 Sep 2017    - Register source_id MPIESM-1-2-HAM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/403
PJD 26 Sep 2017    - Register source_id MRI-AGCM3-2 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/410
PJD  4 Oct 2017    - Add frequency monPt https://github.com/WCRP-CMIP/CMIP6_CVs/issues/413
PJD  8 Oct 2017    - Revise multiple GFDL source_id values https://github.com/WCRP-CMIP/CMIP6_CVs/issues/318
PJD 27 Oct 2017    - Further minor tweaks https://github.com/WCRP-CMIP/CMIP6_CVs/issues/318
PJD 27 Oct 2017    - Revise frequency 1hrCM definition https://github.com/WCRP-CMIP/CMIP6_CVs/issues/414#issuecomment-335032399
PJD 27 Oct 2017    - Revise MPI source_id values https://github.com/WCRP-CMIP/CMIP6_CVs/issues/195, 196, 197
PJD 27 Oct 2017    - Register multiple BCC source_id values https://github.com/WCRP-CMIP/CMIP6_CVs/issues/404, 406, 407
PJD 30 Oct 2017    - Register institution_id NIWA and add to UKESM1-0-LL https://github.com/WCRP-CMIP/CMIP6_CVs/issues/421
PJD  2 Nov 2017    - Register source_id HadGEM3-GC31-MH https://github.com/WCRP-CMIP/CMIP6_CVs/issues/424
PJD  6 Nov 2017    - Register institution_id CAS https://github.com/WCRP-CMIP/CMIP6_CVs/issues/426
PJD  7 Nov 2017    - Update missing nominal_resolution information for multiple source_id entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/431
PJD  7 Nov 2017    - Further minor tweaks to GFDL-ESM2M https://github.com/WCRP-CMIP/CMIP6_CVs/issues/318
PJD  8 Nov 2017    - Correct model components for various LS3MIP/LUMIP experiments https://github.com/WCRP-CMIP/CMIP6_CVs/issues/423
PJD 15 Nov 2017    - Register multiple CAS source_id values FGOALS* https://github.com/WCRP-CMIP/CMIP6_CVs/issues/427, 428, 436
PJD  7 Dec 2017    - Revise THU source_id CIESM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/439
PJD 14 Dec 2017    - Update activity_participation for multiple MOHC source_id entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/442
PJD 19 Dec 2017    - Update institution_id for HadGEM3-GC31-H* entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/441
PJD 19 Dec 2017    - Update experiment_id AerChemMIP and AMIP additional_allowed_model_components https://github.com/WCRP-CMIP/CMIP6_CVs/issues/438
PJD  8 Jan 2018    - Register institution_id DWD https://github.com/WCRP-CMIP/CMIP6_CVs/issues/446
PJD 10 Jan 2018    - Revise MPI-M source_id MPIESM-1-2-HR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/196
PJD 16 Jan 2018    - Register institution_id UHH https://github.com/WCRP-CMIP/CMIP6_CVs/issues/450
PJD 13 Feb 2018    - Revise institution_id NCAR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/456
PJD 22 Feb 2018    - Register institution_id AER https://github.com/WCRP-CMIP/CMIP6_CVs/issues/459
PJD 22 Feb 2018    - Remove source_id ACCESS-1-0, update PCMDI-test-1-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/454
PJD 22 Feb 2018    - Revise descriptions for HadGEM3 and UKESM1 source_id entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/457
PJD 23 Feb 2018    - Convert versioning for internal consistency https://github.com/WCRP-CMIP/CMIP6_CVs/issues/28
PJD 23 Feb 2018    - Added tag generation for each new version
PJD 23 Feb 2018    - Validate source_id entries against CVs https://github.com/WCRP-CMIP/CMIP6_CVs/issues/378
PJD 23 Feb 2018    - Register institution_id KIOST https://github.com/WCRP-CMIP/CMIP6_CVs/issues/469
PJD  5 Mar 2018    - Updated versionHistory to be obtained from the repo https://github.com/WCRP-CMIP/CMIP6_CVs/issues/468
PJD  5 Mar 2018    - Register source_id KIOST-ESM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/469
PJD  5 Mar 2018    - Update activity_participation for source_id CNRM-CM6-1 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/471
PJD  5 Mar 2018    - Update activity_participation entries to include CMIP https://github.com/WCRP-CMIP/CMIP6_CVs/issues/468
PJD  5 Mar 2018    - Update activity_id to include CDRMIP and PAMIP https://github.com/WCRP-CMIP/CMIP6_CVs/issues/455
PJD  5 Mar 2018    - Updated versionHistory to be obtained from the repo https://github.com/WCRP-CMIP/CMIP6_CVs/issues/468
PJD  5 Mar 2018    - Update README.md to include version badge https://github.com/WCRP-CMIP/CMIP6_CVs/issues/468
PJD  7 Mar 2018    - Register source_id CAS-ESM1-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/479
PJD  8 Mar 2018    - Revise source_id VRESM-1-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/101
PJD 12 Mar 2018    - Register UHH source_id ARTS-2-3 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/452
PJD 12 Mar 2018    - Register AER source_id LBLRTM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/460
PJD 12 Mar 2018    - Revise source_id GFDL-ESM4 to include CDRMIP https://github.com/WCRP-CMIP/CMIP6_CVs/issues/483
PJD 12 Mar 2018    - Add CMIP6 doc reference in version history https://github.com/WCRP-CMIP/CMIP6_CVs/issues/482
PJD  3 Apr 2018    - Register source_id NESM3 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/488
PJD  3 Apr 2018    - Register institution_id IIASA https://github.com/WCRP-CMIP/CMIP6_CVs/issues/490
PJD  3 Apr 2018    - Revise OMIP JRA55-do entry https://github.com/WCRP-CMIP/CMIP6_CVs/issues/493
PJD  3 Apr 2018    - Revise OMIP allowed_components https://github.com/WCRP-CMIP/CMIP6_CVs/issues/491
PJD  3 Apr 2018    - Revise years in experiment_id entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/489
PJD  3 Apr 2018    - Revise MPI-ESM1-2-HR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/196
PJD  3 Apr 2018    - Revise ICON-ESM-LR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/197
PJD  3 Apr 2018    - Revise MPI-ESM-1-2-HAM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/403
PJD  4 Apr 2018    - Revise CAS FGOALS* activity_participation https://github.com/WCRP-CMIP/CMIP6_CVs/issues/427
PJD  4 Apr 2018    - Revise NASA-GISS source_id entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/177
PJD  4 Apr 2018    - Register source_id GISS-E2-1-MA-G https://github.com/WCRP-CMIP/CMIP6_CVs/issues/506
PJD  4 Apr 2018    - Register source_id GISS-E3-G https://github.com/WCRP-CMIP/CMIP6_CVs/issues/507
PJD  4 Apr 2018    - Register institution_id UofT, source_id UofT-CCSM4 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/511 + 512
PJD  6 Apr 2018    - Revise MOHC source_id entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/494
PJD  6 Apr 2018    - Revise source_id MPI-ESM-1-2-LR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/195
PJD 20 Apr 2018    - Revise source_id BNU-ESM-1-1 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/99
PJD 20 Apr 2018    - Revise experiment_id deforest-globe https://github.com/WCRP-CMIP/CMIP6_CVs/issues/489#issuecomment-380183402
PJD 20 Apr 2018    - Revise institution_id EC-Earth-Consortium https://github.com/WCRP-CMIP/CMIP6_CVs/issues/515
PJD 20 Apr 2018    - Revise MIROC source_ids https://github.com/WCRP-CMIP/CMIP6_CVs/issues/517
PJD 20 Apr 2018    - Revise institution_id MIROC https://github.com/WCRP-CMIP/CMIP6_CVs/issues/518
PJD 20 Apr 2018    - Add experiment_id values for CDRMIP and PAMIP https://github.com/WCRP-CMIP/CMIP6_CVs/issues/455
PJD 24 Apr 2018    - Register source_id CESM2 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/525
PJD 28 Apr 2018    - Revise CESM2 activity_participation https://github.com/WCRP-CMIP/CMIP6_CVs/issues/525
PJD  3 May 2018    - Revise institution_id NCC https://github.com/WCRP-CMIP/CMIP6_CVs/issues/83
PJD 21 May 2018    - Revise source_id UKESM1-0-LL https://github.com/WCRP-CMIP/CMIP6_CVs/issues/531
PJD 21 May 2018    - Register source_id KACE-1-0-G https://github.com/WCRP-CMIP/CMIP6_CVs/issues/532
PJD 21 May 2018    - Register institution_id E3SM-Project https://github.com/WCRP-CMIP/CMIP6_CVs/issues/533
PJD 22 May 2018    - Register institution_id UTAS https://github.com/WCRP-CMIP/CMIP6_CVs/issues/535
PJD 22 May 2018    - Revise institution_id CSIRO-ARCCSS-BoM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/540
PJD 22 May 2018    - Register institution_id CSIRO https://github.com/WCRP-CMIP/CMIP6_CVs/issues/546
PJD 22 May 2018    - Register source_id GFDL-CM4C192 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/537
PJD 22 May 2018    - Register source_id ACCESS-ESM1-5 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/538
PJD 22 May 2018    - Register source_id ACCESS-CM2 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/539
PJD 22 May 2018    - Register source_id E3SM-1-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/534
PJD 22 May 2018    - Revise AWI source_id entries https://github.com/WCRP-CMIP/CMIP6_CVs/issues/526
PJD 23 May 2018    - Register source_id CSIRO-Mk3L-1-3 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/536
PJD 23 May 2018    - Revise source_id INM-CM4-8 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/359
PJD 23 May 2018    - Revise source_id E3SM-1-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/534
PJD 23 May 2018    - Register source_id GFDL-OM4p5B https://github.com/WCRP-CMIP/CMIP6_CVs/issues/554
PJD 29 May 2018    - Revise source_id CSIRO-Mk3L-1-3 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/536
PJD  6 Jun 2018    - Register 3 additional source_id entries for EC-Earth-Consortia https://github.com/WCRP-CMIP/CMIP6_CVs/issues/559
PJD 12 Jun 2018    - Revise source_id EC-Earth3P-HR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/559
PJD 12 Jun 2018    - Register institution_id DKRZ https://github.com/WCRP-CMIP/CMIP6_CVs/issues/561
PJD 12 Jun 2018    - Register source_id IPSL-CM6A-ATM-HR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/562
PJD 25 Jun 2018    - Update for py3
PJD 25 Jun 2018    - Register institution_id UA https://github.com/WCRP-CMIP/CMIP6_CVs/issues/566
PJD 25 Jun 2018    - Register source_id MCM-UA-1-0 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/568
PJD 27 Jun 2018    - Deregister institution_id IIASA https://github.com/WCRP-CMIP/CMIP6_CVs/issues/490
PJD 27 Jun 2018    - Register institution_id ECMWF https://github.com/WCRP-CMIP/CMIP6_CVs/issues/566
PJD 27 Jun 2018    - Register source_id ECMWF-IFS-LR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/571
PJD 27 Jun 2018    - Register source_id ECMWF-IFS-HR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/573
PJD 27 Jun 2018    - Register source_id ECMWF-IFS-MR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/574
PJD 27 Jun 2018    - Revise source_id MPI-ESM1-2-HR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/575
PJD 17 Jul 2018    - Revise institution_id FIO-RONM -> FIO-QLNM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/582
PJD 17 Jul 2018    - Register source_id FIO-ESM-2-0 -> FIO-QLNM https://github.com/WCRP-CMIP/CMIP6_CVs/issues/583
PJD 17 Jul 2018    - Revise experiment_id G7cirrus https://github.com/WCRP-CMIP/CMIP6_CVs/issues/584
PJD 17 Jul 2018    - Revise experiment_id land-future https://github.com/WCRP-CMIP/CMIP6_CVs/issues/567
PJD 25 Jul 2018    - Revise LS3MIP experiment_ids, add land-ssp126 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/567
PJD 26 Jul 2018    - Revise source_id MIROC6 https://github.com/WCRP-CMIP/CMIP6_CVs/issues/590
PJD 31 Jul 2018    - Revise multiple GFDL source_id values - release_year https://github.com/WCRP-CMIP/CMIP6_CVs/issues/318
PJD 31 Jul 2018    - Revise piClim experiment_ids allowed components - release_year https://github.com/WCRP-CMIP/CMIP6_CVs/issues/592
PJD 15 Aug 2018    - Rename nominal_resolution -> native_nominal_resolution in source_id https://github.com/WCRP-CMIP/CMIP6_CVs/issues/597
PJD 22 Aug 2018    - Revise CDRMIP experiment_id start_years and num years https://github.com/WCRP-CMIP/CMIP6_CVs/issues/594
PJD 12 Sep 2018    - Revise source_id BCC-CSM2-HR https://github.com/WCRP-CMIP/CMIP6_CVs/issues/407, 600
PJD 14 Sep 2018    - Revise multiple GFDL source_id values https://github.com/WCRP-CMIP/CMIP6_CVs/issues/318
PJD 25 Sep 2018    - Revise multiple NICAM source_id values https://github.com/WCRP-CMIP/CMIP6_CVs/issues/606
PJD 25 Sep 2018    - Register source_id AWI-ESM-1-1-LR, amend AWI-CM-1-1-LR https://github.com/WCRP-CMIP/CMIP6_CVs/pull/608
PJD 17 Jul 2018    - Revise experiment_id esm-ssp534-over https://github.com/WCRP-CMIP/CMIP6_CVs/issues/607
                   - TODO: Generate table_id from dataRequest https://github.com/WCRP-CMIP/CMIP6_CVs/issues/166

@author: durack1
"""

#%% Import statements
from __future__ import print_function
import calendar
import datetime
import gc
import json
import os
import shlex
import subprocess
import sys
import time
import urllib
sys.path.insert(0,'/sync/git/durolib/lib') ; # trustym
from durolib import readJsonCreateDict
from CMIP6Lib import ascertainVersion,cleanString,dictDepth,entryCheck,getFileHistory,versionHistoryUpdate
#import pyexcel_xlsx as pyx
#from string import replace
#from unidecode import unidecode

#%% Set commit message
commitMessage = '\"Revise experiment_id esm-ssp534-over\"'

#%% List target controlled vocabularies (CVs)
masterTargets = [
    'activity_id',
    'experiment_id',
    'frequency',
    'grid_label',
    'institution_id',
    'license',
    'mip_era',
    'nominal_resolution',
    'realm',
    'required_global_attributes',
    'source_id',
    'source_type',
    'sub_experiment_id',
    'table_id'
]

#%% Activities
activity_id = {
    'AerChemMIP': 'Aerosols and Chemistry Model Intercomparison Project',
    'C4MIP': 'Coupled Climate Carbon Cycle Model Intercomparison Project',
    'CDRMIP': 'Carbon Dioxide Removal Model Intercomparison Project',
    'CFMIP': 'Cloud Feedback Model Intercomparison Project',
    'CMIP': 'CMIP DECK: 1pctCO2, abrupt4xCO2, amip, esm-piControl, esm-historical, historical, and piControl experiments',
    'CORDEX': 'Coordinated Regional Climate Downscaling Experiment',
    'DAMIP': 'Detection and Attribution Model Intercomparison Project',
    'DCPP': 'Decadal Climate Prediction Project',
    'DynVarMIP': 'Dynamics and Variability Model Intercomparison Project',
    'FAFMIP': 'Flux-Anomaly-Forced Model Intercomparison Project',
    'GMMIP': 'Global Monsoons Model Intercomparison Project',
    'GeoMIP': 'Geoengineering Model Intercomparison Project',
    'HighResMIP': 'High-Resolution Model Intercomparison Project',
    'ISMIP6': 'Ice Sheet Model Intercomparison Project for CMIP6',
    'LS3MIP': 'Land Surface, Snow and Soil Moisture',
    'LUMIP': 'Land-Use Model Intercomparison Project',
    'OMIP': 'Ocean Model Intercomparison Project',
    'PAMIP': 'Polar Amplification Model Intercomparison Project',
    'PMIP': 'Palaeoclimate Modelling Intercomparison Project',
    'RFMIP': 'Radiative Forcing Model Intercomparison Project',
    'SIMIP': 'Sea Ice Model Intercomparison Project',
    'ScenarioMIP': 'Scenario Model Intercomparison Project',
    'VIACSAB': 'Vulnerability, Impacts, Adaptation and Climate Services Advisory Board',
    'VolMIP': 'Volcanic Forcings Model Intercomparison Project'
}

#%% Experiments
tmp = [['experiment_id','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_experiment_id.json']
      ] ;
experiment_id = readJsonCreateDict(tmp)
experiment_id = experiment_id.get('experiment_id')
experiment_id = experiment_id.get('experiment_id') ; # Fudge to extract duplicate level
del(tmp)

# Fix issues
'''
# xlsx import
# Fields
# Alpha/json order, xlsx column old, xlsx column new, type, value
# 1  0  0  str  experiment_id string
# 2  1  1  list activity_id list
# 3  8  7  list additional_allowed_model_components list
# 4  13 12 str  description string
# 5  10 10 str  end_year string
# 6  2  2  str  experiment string
# 7  11 11 str  min_number_yrs_per_sim string
# 8  12 5  list parent_activity_id list
# 9  6  6  list parent_experiment_id list
# 10 7  8  list required_model_components list
# 11 9  9  str  start_year string
# 12 5  -  -    sub_experiment string
# 13 4  4  list sub_experiment_id string
# 14 3  3  str tier string

os.chdir('/sync/git/CMIP6_CVs/src')
inFiles = ['180421_1927_DavidKeller_CMIP6-CDRMIP-ExpList.xlsx',
           '180421_1927_DougSmith_CMIP6-PAMIP-ExpList.xlsx']
for inFile in inFiles:
    data = pyx.get_data(inFile)
    data = data['Sheet1']
    headers = data[3]
    #experiment_id = {} ; Already defined and loaded
    for count in range(4,len(data)): # Start on 5th row, headers
        if data[count] == []:
            #print count,'blank field'
            continue
        row = data[count]
        key = row[0] ; #replace(row[0],'_ ','_')
        experiment_id[key] = {}
        for count2,entry in enumerate(headers):
            #if count2 == 5:
            #    continue ; # Skip sub_experiment - removed in update
            entry = replace(entry,'_ ','_') ; # clean up spaces
            entry = replace(entry,' ', '_') ; # replace spaces with underscores
            if count2 >= len(row):
                experiment_id[key][entry] = ''
                continue
            value = row[count2]
            if count2 in [1,4,6,7,8,12]:
                if value == None:
                    pass
                elif value == 'no parent':
                    pass
                elif 'no parent,' in value:
                    value = ['no parent',replace(value,'no parent,','').strip()] ; # deal with multiple entries (including 'no parent')
                    pass
                else:
                    value = replace(value,',','') ; # remove ','
                    value = value.split() ; # Change type to list
                    #print value
            if type(value) == long:
                experiment_id[key][entry] = str(value) ; #replace(str(value),' ','')
            elif type(value) == list:
                experiment_id[key][entry] = ' '.join(value)
            elif value == None:
                experiment_id[key][entry] = '' ; # changed from none to preserve blank entries
            elif type(value) == float:
                #print 'elif type(value):',value
                value = str(int(value))
                experiment_id[key][entry] = value
            else:
                #print 'else:',value
                value = replace(value,'    ',' ') ; # replace whitespace
                value = replace(value,'   ',' ') ; # replace whitespace
                value = replace(value,'  ',' ') ; # replace whitespace
                experiment_id[key][entry] = unidecode(value) ; #replace(unidecode(value),' ','')
                try:
                    #print 'try:',value
                    unidecode(value)
                except:
                    print count,count2,key,entry,value
            # Now sort by type
            if count2 in [1,4,6,7,8]:
                experiment_id[key][entry] = list(value)
            elif count2 == 5:
                experiment_id[key][entry] = list([value])
    del(inFile,data,headers,count,row,key,entry,value) ; gc.collect()
'''

key = 'esm-ssp534-over'
experiment_id[key]['parent_activity_id'] = ['C4MIP']
experiment_id[key]['parent_experiment_id'] = ['esm-ssp585']
experiment_id[key]['start_year'] = '2040'
experiment_id[key]['min_number_yrs_per_sim'] = '61'
key = 'ssp534-over'
experiment_id[key]['description'] = ''.join(['21st century overshoot scenario relative to SSP5_34. ',
                                             'Branches from SSP5_85 at 2040 with emissions reduced to ',
                                             'zero by 2070 and negative thereafter. This simulation ',
                                             'should optionally be extended to year 2300'])

#==============================================================================
# Example new experiment_id entry
#key = 'ssp119'
#experiment_id[key] = {}
#experiment_id[key]['activity_id'] = ['ScenarioMIP']
#experiment_id[key]['additional_allowed_model_components'] = ['AER','CHEM','BGC']
#experiment_id[key]['description'] = 'Future scenario with low radiative forcing throughout reaching about 1.9 W/m2 in 2100 based on SSP1. Concentration-driven'
#experiment_id[key]['end_year'] = '2100'
#experiment_id[key]['experiment'] = 'low-end scenario reaching 1.9 W m-2, based on SSP1'
#experiment_id[key]['experiment_id'] = key
#experiment_id[key]['min_number_yrs_per_sim'] = '86'
#experiment_id[key]['parent_activity_id'] = ['CMIP']
#experiment_id[key]['parent_experiment_id'] = ['historical']
#experiment_id[key]['required_model_components'] = ['AOGCM']
#experiment_id[key]['start_year'] = '2015'
#experiment_id[key]['sub_experiment_id'] = ['none']
#experiment_id[key]['tier'] = '2'
# Rename
#experiment_id['land-noShiftCultivate'] = experiment_id.pop('land-noShiftcultivate')
# Remove
#experiment_id.pop('land-noShiftcultivate')

#%% Frequencies
frequency = {
    '1hr': 'sampled hourly',
    '1hrCM': 'monthly-mean diurnal cycle resolving each day into 1-hour means',
    '1hrPt': 'sampled hourly, at specified time point within an hour',
    '3hr': 'sampled every 3 hours',
    '3hrPt': 'sampled 3 hourly, at specified time point within the time period',
    '6hr': 'sampled every 6 hours',
    '6hrPt': 'sampled 6 hourly, at specified time point within the time period',
    'day': 'daily mean samples',
    'dec': 'decadal mean samples',
    'fx': 'fixed (time invariant) field',
    'mon': 'monthly mean samples',
    'monC': 'monthly climatology computed from monthly mean samples',
    'monPt': 'sampled monthly, at specified time point within the time period',
    'subhrPt': 'sampled sub-hourly, at specified time point within an hour',
    'yr': 'annual mean samples',
    'yrPt': 'sampled yearly, at specified time point within the time period'
}

#%% Grid labels
grid_label = {
    'gm': 'global mean data',
    'gn': 'data reported on a model\'s native grid',
    'gna': 'data reported on a native grid in the region of Antarctica',
    'gng': 'data reported on a native grid in the region of Greenland',
    'gnz': 'zonal mean data reported on a model\'s native latitude grid',
    'gr': 'regridded data reported on the data provider\'s preferred target grid',
    'gr1': 'regridded data reported on a grid other than the native grid and other than the preferred target grid',
    'gr1a': 'regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid',
    'gr1g': 'regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid',
    'gr1z': 'regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid',
    'gr2': 'regridded data reported on a grid other than the native grid and other than the preferred target grid',
    'gr2a': 'regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid',
    'gr2g': 'regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid',
    'gr2z': 'regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid',
    'gr3': 'regridded data reported on a grid other than the native grid and other than the preferred target grid',
    'gr3a': 'regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid',
    'gr3g': 'regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid',
    'gr3z': 'regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid',
    'gr4': 'regridded data reported on a grid other than the native grid and other than the preferred target grid',
    'gr4a': 'regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid',
    'gr4g': 'regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid',
    'gr4z': 'regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid',
    'gr5': 'regridded data reported on a grid other than the native grid and other than the preferred target grid',
    'gr5a': 'regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid',
    'gr5g': 'regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid',
    'gr5z': 'regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid',
    'gr6': 'regridded data reported on a grid other than the native grid and other than the preferred target grid',
    'gr6a': 'regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid',
    'gr6g': 'regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid',
    'gr6z': 'regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid',
    'gr7': 'regridded data reported on a grid other than the native grid and other than the preferred target grid',
    'gr7a': 'regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid',
    'gr7g': 'regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid',
    'gr7z': 'regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid',
    'gr8': 'regridded data reported on a grid other than the native grid and other than the preferred target grid',
    'gr8a': 'regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid',
    'gr8g': 'regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid',
    'gr8z': 'regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid',
    'gr9': 'regridded data reported on a grid other than the native grid and other than the preferred target grid',
    'gr9a': 'regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid',
    'gr9g': 'regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid',
    'gr9z': 'regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid',
    'gra': 'regridded data in the region of Antarctica reported on the data provider\'s preferred target grid',
    'grg': 'regridded data in the region of Greenland reported on the data provider\'s preferred target grid',
    'grz': 'regridded zonal mean data reported on the data provider\'s preferred latitude target grid'
}

#%% Institutions
institution_id = {
    'AER': 'Research and Climate Group, Atmospheric and Environmental Research, 131 Hartwell Avenue, Lexington, MA 02421, USA',
    'AWI': 'Alfred Wegener Institute, Helmholtz Centre for Polar and Marine Research, Am Handelshafen 12, 27570 Bremerhaven, Germany',
    'BCC': 'Beijing Climate Center, Beijing 100081, China',
    'BNU': 'Beijing Normal University, Beijing 100875, China',
    'CAMS': 'Chinese Academy of Meteorological Sciences, Beijing 100081, China',
    'CAS': 'Chinese Academy of Sciences, Beijing 100029, China',
    'CCCR-IITM': 'Centre for Climate Change Research, Indian Institute of Tropical Meteorology Pune, Maharashtra 411 008, India',
    'CCCma': 'Canadian Centre for Climate Modelling and Analysis, Victoria, BC V8P 5C2, Canada',
    'CMCC': 'Fondazione Centro Euro-Mediterraneo sui Cambiamenti Climatici, Lecce 73100, Italy',
    'CNRM-CERFACS': 'CNRM (Centre National de Recherches Meteorologiques, Toulouse 31057, France), CERFACS (Centre Europeen de Recherche et de Formation Avancee en Calcul Scientifique, Toulouse 31057, France)',
    'CSIR-CSIRO': 'CSIR (Council for Scientific and Industrial Research - Natural Resources and the Environment, Pretoria, 0001, South Africa), CSIRO (Commonwealth Scientific and Industrial Research Organisation and Bureau of Meteorology, Melbourne, Victoria 3208, Australia)',
    'CSIRO': 'Commonwealth Scientific and Industrial Research Organisation, Aspendale, Victoria 3195, Australia',
    'CSIRO-ARCCSS-BoM': 'Commonwealth Scientific and Industrial Research Organisation, Australian Research Council Centre of Excellence for Climate System Science, and Bureau of Meteorology, Aspendale, Victoria 3195, Australia',
    'DKRZ': 'Deutsches Klimarechenzentrum, Hamburg 20146, Germany',
    'DWD': 'Deutscher Wetterdienst, Offenbach am Main 63067, Germany',
    'E3SM-Project': ''.join(['LLNL (Lawrence Livermore National Laboratory, Livermore, CA 94550, USA); ',
                             'ANL (Argonne National Laboratory, Argonne, IL 60439, USA); ',
                             'BNL (Brookhaven National Laboratory, Upton, NY 11973, USA); ',
                             'LANL (Los Alamos National Laboratory, Los Alamos, NM 87545, USA); ',
                             'LBNL (Lawrence Berkeley National Laboratory, Berkeley, CA 94720, USA); ',
                             'ORNL (Oak Ridge National Laboratory, Oak Ridge, TN 37831, USA); ',
                             'PNNL (Pacific Northwest National Laboratory, Richland, WA 99352, USA); ',
                             'SNL (Sandia National Laboratories, Albuquerque, NM 87185, USA). ',
                             'Mailing address: LLNL Climate Program, c/o David C. Bader, ',
                             'Principal Investigator, L-103, 7000 East Avenue, Livermore, CA 94550, USA']),
    'EC-Earth-Consortium': ''.join(['AEMET, Spain; BSC, Spain; CNR-ISAC, Italy; DMI, Denmark; ENEA, Italy; FMI, Finland; Geomar, Germany; ICHEC, ',
                            'Ireland; ICTP, Italy; IDL, Portugal; IMAU, The Netherlands; IPMA, Portugal; KIT, Karlsruhe, Germany; KNMI, ',
                            'The Netherlands; Lund University, Sweden; Met Eireann, Ireland; NLeSC, The Netherlands; NTNU, Norway; Oxford ',
                            'University, UK; surfSARA, The Netherlands; SMHI, Sweden; Stockholm University, Sweden; Unite ASTR, Belgium; ',
                            'University College Dublin, Ireland; University of Bergen, Norway; University of Copenhagen, Denmark; ',
                            'University of Helsinki, Finland; University of Santiago de Compostela, Spain; Uppsala University, Sweden; ',
                            'Utrecht University, The Netherlands; Vrije Universiteit Amsterdam, the Netherlands; Wageningen University, ',
                            'The Netherlands. Mailing address: EC-Earth consortium, Rossby Center, Swedish Meteorological and Hydrological ',
                            'Institute/SMHI, SE-601 76 Norrkoping, Sweden']),
    'ECMWF': 'European Centre for Medium-Range Weather Forecasts, Reading RG2 9AX, UK',
    'FIO-QLNM': 'FIO (First Institute of Oceanography, State Oceanic Administration, Qingdao 266061, China), QNLM (Qingdao National Laboratory for Marine Science and Technology, Qingdao 266237, China)',
    'HAMMOZ-Consortium': 'ETH Zurich, Switzerland; Max Planck Institut fur Meteorologie, Germany; Forschungszentrum Julich, Germany; University of Oxford, UK; Finnish Meteorological Institute, Finland; Leibniz Institute for Tropospheric Research, Germany; Center for Climate Systems Modeling (C2SM) at ETH Zurich, Switzerland',
    'INM': 'Institute for Numerical Mathematics, Russian Academy of Science, Moscow 119991, Russia',
    'INPE': 'National Institute for Space Research, Cachoeira Paulista, SP 12630-000, Brazil',
    'IPSL': 'Institut Pierre Simon Laplace, Paris 75252, France',
    'KIOST': 'Korea Institute of Ocean Science & Technology, Busan 49111, Republic of Korea',
    'MESSy-Consortium': 'The Modular Earth Submodel System (MESSy) Consortium, represented by the Institute for Physics of the Atmosphere, Deutsches Zentrum fur Luft- und Raumfahrt (DLR), Wessling, Bavaria 82234, Germany',
    'MIROC': ''.join(['JAMSTEC (Japan Agency for Marine-Earth Science and Technology, Kanagawa 236-0001, Japan), ',
                      'AORI (Atmosphere and Ocean Research Institute, The University of Tokyo, Chiba 277-8564, Japan), ',
                      'NIES (National Institute for Environmental Studies, Ibaraki 305-8506, Japan), ',
                      'and R-CCS (RIKEN Center for Computational Science, Hyogo 650-0047, Japan)']),
    'MOHC': 'Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK',
    'MPI-M': 'Max Planck Institute for Meteorology, Hamburg 20146, Germany',
    'MRI': 'Meteorological Research Institute, Tsukuba, Ibaraki 305-0052, Japan',
    'NASA-GISS': 'Goddard Institute for Space Studies, New York, NY 10025, USA',
    'NCAR': 'National Center for Atmospheric Research, Climate and Global Dynamics Laboratory, 1850 Table Mesa Drive, Boulder, CO 80305, USA',
    'NCC': ''.join(['NorESM Climate modeling Consortium consisting of ',
                    'CICERO (Center for International Climate and Environmental Research, Oslo 0349), ',
                    'MET-Norway (Norwegian Meteorological Institute, Oslo 0313), ',
                    'NERSC (Nansen Environmental and Remote Sensing Center, Bergen 5006), ',
                    'NILU (Norwegian Institute for Air Research, Kjeller 2027), ',
                    'UiB (University of Bergen, Bergen 5007), ',
                    'UiO (University of Oslo, Oslo 0313) ',
                    'and UNI (Uni Research, Bergen 5008), Norway. Mailing address: NCC, c/o MET-Norway, ',
                    'Henrik Mohns plass 1, Oslo 0313, Norway']),
    'NERC': 'Natural Environment Research Council, STFC-RAL, Harwell, Oxford, OX11 0QX, UK',
    'NIMS-KMA': 'National Institute of Meteorological Sciences/Korea Meteorological Administration, Climate Research Division, Seoho-bukro 33, Seogwipo-si, Jejudo 63568, Republic of Korea',
    'NIWA': 'National Institute of Water and Atmospheric Research, Hataitai, Wellington 6021, New Zealand',
    'NOAA-GFDL': 'National Oceanic and Atmospheric Administration, Geophysical Fluid Dynamics Laboratory, Princeton, NJ 08540, USA',
    'NUIST': 'Nanjing University of Information Science and Technology, Nanjing, 210044, China',
    'PCMDI': 'Program for Climate Model Diagnosis and Intercomparison, Lawrence Livermore National Laboratory, Livermore, CA 94550, USA',
    'SNU': 'Seoul National University, Seoul 08826, Republic of Korea',
    'THU': 'Department of Earth System Science, Tsinghua University, Beijing 100084, China',
    'UA': 'Department of Geosciences, University of Arizona, Tucson, AZ 85721, USA',
    'UHH': 'Universitat Hamburg, Hamburg 20148, Germany',
    'UTAS': 'Institute for Marine and Antarctic Studies, University of Tasmania, Hobart, Tasmania 7001, Australia',
    'UofT': 'Department of Physics, University of Toronto, 60 St George Street, Toronto, ON M5S1A7, Canada'
}

#%% CMIP6 License
license = [
    'CMIP6 model data produced by <Your Centre Name> is licensed under a Creative Commons Attribution-[NonCommercial-]ShareAlike 4.0 International License (https://creativecommons.org/licenses). Consult https://pcmdi.llnl.gov/CMIP6/TermsOfUse for terms of use governing CMIP6 output, including citation requirements and proper acknowledgment. Further information about this data, including some limitations, can be found via the further_info_url (recorded as a global attribute in this file)[ and at <some URL maintained by modeling group>]. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law.'
]

#%% MIP eras
mip_era = ['CMIP1', 'CMIP2', 'CMIP3', 'CMIP5', 'CMIP6']

#%% Nominal resolutions
nominal_resolution = [
    '0.5 km',
    '1 km',
    '10 km',
    '100 km',
    '1000 km',
    '10000 km',
    '1x1 degree',
    '2.5 km',
    '25 km',
    '250 km',
    '2500 km',
    '5 km',
    '50 km',
    '500 km',
    '5000 km'
]

#%% Realms
realm = {
    'aerosol': 'Aerosol',
    'atmos': 'Atmosphere',
    'atmosChem': 'Atmospheric Chemistry',
    'land': 'Land Surface',
    'landIce': 'Land Ice',
    'ocean': 'Ocean',
    'ocnBgchem': 'Ocean Biogeochemistry',
    'seaIce': 'Sea Ice'
}

#%% Required global attributes
required_global_attributes = [
    'Conventions',
    'activity_id',
    'creation_date',
    'data_specs_version',
    'experiment',
    'experiment_id',
    'forcing_index',
    'frequency',
    'further_info_url',
    'grid',
    'grid_label',
    'initialization_index',
    'institution',
    'institution_id',
    'license',
    'mip_era',
    'nominal_resolution',
    'physics_index',
    'product',
    'realization_index',
    'realm',
    'source',
    'source_id',
    'source_type',
    'sub_experiment',
    'sub_experiment_id',
    'table_id',
    'tracking_id',
    'variable_id',
    'variant_label'
]

#%% Source identifiers
tmp = [['source_id','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_source_id.json']
      ] ;
source_id = readJsonCreateDict(tmp)
source_id = source_id.get('source_id')
source_id = source_id.get('source_id') ; # Fudge to extract duplicate level
del(tmp)

# Fix issues

#==============================================================================
#key = 'AWI-ESM-1-1-LR'
#source_id[key] = {}
#source_id[key]['activity_participation'] = [
# 'CMIP',
# 'PMIP'
#]
#source_id[key]['cohort'] = [
# 'Registered'
#]
#source_id[key]['institution_id'] = [
# 'AWI'
#]
#source_id[key]['label'] = 'AWI-ESM 1.1 LR'
#source_id[key]['label_extended'] = 'AWI-ESM 1.1 LR'
#source_id[key]['model_component'] = {}
#source_id[key]['model_component']['aerosol'] = {}
#source_id[key]['model_component']['aerosol']['description'] = 'none'
#source_id[key]['model_component']['aerosol']['native_nominal_resolution'] = 'none'
#source_id[key]['model_component']['atmos'] = {}
#source_id[key]['model_component']['atmos']['description'] = 'ECHAM6.3.04p1 (T63L47 native atmosphere T63 gaussian grid; 192 x 96 longitude/latitude; 47 levels; top level 80 km)'
#source_id[key]['model_component']['atmos']['native_nominal_resolution'] = '250 km'
#source_id[key]['model_component']['atmosChem'] = {}
#source_id[key]['model_component']['atmosChem']['description'] = 'none'
#source_id[key]['model_component']['atmosChem']['native_nominal_resolution'] = 'none'
#source_id[key]['model_component']['land'] = {}
#source_id[key]['model_component']['land']['description'] = 'JSBACH 3.20 with dynamic vegetation'
#source_id[key]['model_component']['land']['native_nominal_resolution'] = '250 km'
#source_id[key]['model_component']['landIce'] = {}
#source_id[key]['model_component']['landIce']['description'] = 'none'
#source_id[key]['model_component']['landIce']['native_nominal_resolution'] = 'none'
#source_id[key]['model_component']['ocean'] = {}
#source_id[key]['model_component']['ocean']['description'] = 'FESOM 1.4 (unstructured grid in the horizontal with 126859 wet nodes; 46 levels; top grid cell 0-5 m)'
#source_id[key]['model_component']['ocean']['native_nominal_resolution'] = '50 km'
#source_id[key]['model_component']['ocnBgchem'] = {}
#source_id[key]['model_component']['ocnBgchem']['description'] = 'none'
#source_id[key]['model_component']['ocnBgchem']['native_nominal_resolution'] = 'none'
#source_id[key]['model_component']['seaIce'] = {}
#source_id[key]['model_component']['seaIce']['description'] = 'FESOM 1.4'
#source_id[key]['model_component']['seaIce']['native_nominal_resolution'] = '50 km'
#source_id[key]['release_year'] = '2018'
#source_id[key]['source_id'] = key
'''
Descriptors were documented in http://pcmdi.github.io/projects/cmip5/CMIP5_output_metadata_requirements.pdf?id=76
Information above can be found in AR5 Table 9.A.1 http://www.climatechange2013.org/images/report/WG1AR5_Chapter09_FINAL.pdf#page=114
'''

#%% Source types
source_type = {
    'AER': 'aerosol treatment in an atmospheric model where concentrations are calculated based on emissions, transformation, and removal processes (rather than being prescribed or omitted entirely)',
    'AGCM': 'atmospheric general circulation model run with prescribed ocean surface conditions and usually a model of the land surface',
    'AOGCM': 'coupled atmosphere-ocean global climate model, additionally including explicit representation of at least the land and sea ice',
    'BGC': 'biogeochemistry model component that at the very least accounts for carbon reservoirs and fluxes in the atmosphere, terrestrial biosphere, and ocean',
    'CHEM': 'chemistry treatment in an atmospheric model that calculates atmospheric oxidant concentrations (including at least ozone), rather than prescribing them',
    'ISM': 'ice-sheet model that includes ice-flow',
    'LAND': 'land model run uncoupled from the atmosphere',
    'OGCM': 'ocean general circulation model run uncoupled from an AGCM but, usually including a sea-ice model',
    'RAD': 'radiation component of an atmospheric model run \'offline\'',
    'SLAB': 'slab-ocean used with an AGCM in representing the atmosphere-ocean coupled system'
}

#%% Sub experiment ids
sub_experiment_id = {}
sub_experiment_id['none'] = 'none'
sub_experiment_id['s1910'] = 'initialized near end of year 1910'
sub_experiment_id['s1950'] = 'initialized near end of year 1950'
for yr in range(1960,2030):
    sub_experiment_id[''.join(['s',str(yr)])] = ' '.join(['initialized near end of year',str(yr)])
del(yr)

#%% Table ids
table_id = [
    '3hr',
    '6hrLev',
    '6hrPlev',
    '6hrPlevPt',
    'AERday',
    'AERhr',
    'AERmon',
    'AERmonZ',
    'Amon',
    'CF3hr',
    'CFday',
    'CFmon',
    'CFsubhr',
    'E1hr',
    'E1hrClimMon',
    'E3hr',
    'E3hrPt',
    'E6hrZ',
    'Eday',
    'EdayZ',
    'Efx',
    'Emon',
    'EmonZ',
    'Esubhr',
    'Eyr',
    'IfxAnt',
    'IfxGre',
    'ImonAnt',
    'ImonGre',
    'IyrAnt',
    'IyrGre',
    'LImon',
    'Lmon',
    'Oclim',
    'Oday',
    'Odec',
    'Ofx',
    'Omon',
    'Oyr',
    'SIday',
    'SImon',
    'day',
    'fx'
]

#%% Prepare experiment_id and source_id for comparison
for jsonName in ['experiment_id','source_id']:
    if jsonName in ['experiment_id','source_id']:
        dictToClean = eval(jsonName)
        for key, value in dictToClean.iteritems():
            for values in value.iteritems(): # values is a tuple
                # test for dictionary
                if type(values[1]) is list:
                    new = []
                    for count in range(0,len(values[1])):
                        string = values[1][count]
                        string = cleanString(string) ; # Clean string
                        new += [string]
                    #print 'new',new
                    #new.sort() ; # Sort all lists - not experiment_id model components
                    #print 'sort',new
                    dictToClean[key][values[0]] = new
                elif type(values[1]) is dict:
                    # determine dict depth
                    pdepth = dictDepth(values[1])
                    keyInd = values[0]
                    keys1 = values[1].keys()
                    for d1Key in keys1:
                        keys2 = values[1][d1Key].keys()
                        for d2Key in keys2:
                            string = dictToClean[key][keyInd][d1Key][d2Key]
                            string = cleanString(string) ; # Clean string
                            dictToClean[key][keyInd][d1Key][d2Key] = string
                elif type(values[0]) in [str,unicode]:
                    string = dictToClean[key][values[0]]
                    string = cleanString(string) ; # Clean string
                    dictToClean[key][values[0]] = string
        vars()[jsonName] = dictToClean
del(jsonName,dictToClean,key,value,values,new,count,string,pdepth,keyInd,keys1,
    d1Key,keys2,d2Key)

#%% Validate source_id and experiment_id entries
# source_id
for key in source_id.keys():
    # Validate source_id format
    if not entryCheck(key):
        print('Invalid source_id format for entry:',key,'- aborting')
        sys.exit()
    # Validate activity_participation/activity_id
    val = source_id[key]['activity_participation']
    #print key,val
    if 'CMIP' not in val:
        if key in ['LBLRTM','ARTS-2-3']:
            print(key,'RFMIP only - continue')
        elif 'HighResMIP' in val: # Case HighResMIP only
            print(key,'HighResMIP no CMIP required - continue')
        elif 'OMIP' in val: # Case OMIP only
            print(key,'OMIP no CMIP required - continue')
        elif 'FAFMIP' in val: # Case FAFMIP only - GFDL-ESM2M
            print(key,'OMIP no CMIP required - continue')
        else:
            print('Invalid activity_participation for entry:',key,'no CMIP listed - aborting')
            sys.exit()
    for act in val:
        if act not in activity_id:
            print('Invalid activity_participation for entry:',key,':',act,'- aborting')
            sys.exit()
    # Validate institution_id
    vals = source_id[key]['institution_id']
    for val in vals:
        if val not in institution_id:
            print('Invalid institution_id for entry:',key,';',val,'- aborting')
            sys.exit()
    # Validate nominal resolution
    vals = source_id[key]['model_component'].keys()
    for val1 in vals:
        val2 = source_id[key]['model_component'][val1]['native_nominal_resolution']
        if val2 == 'none':
            pass
        elif val2 not in nominal_resolution:
            print('Invalid native_nominal_resolution for entry:',key,val1,val2,'- aborting')
            sys.exit()
    # Validate source_id
    val = source_id[key]['source_id']
    if key != val:
            print('Invalid source_id for entry:',val,'not equal',key,'- aborting')
            sys.exit()
# experiment_ids
experiment_id_keys = experiment_id.keys()
for key in experiment_id_keys:
    # Validate source_id format
    if not entryCheck(key):
        print('Invalid experiment_id format for entry:',key,'- aborting')
        sys.exit()
    # Validate internal key
    val = experiment_id[key]['experiment_id']
    if not val == key:
        print('Invalid experiment_id for entry:',key,'- aborting')
        sys.exit()
    # Validate activity_id
    val = experiment_id[key]['activity_id']
    for act in val:
        if act not in activity_id:
            print('Invalid activity_participation for entry:',key,act,'- aborting')
            sys.exit()
    # Validate additional_allowed_model_components
    vals = experiment_id[key]['additional_allowed_model_components']
    for val in vals:
        if val == '':
            pass
        elif val not in source_type:
            print('Invalid additional_allowed_model_components for entry:',key,val,'- aborting')
            sys.exit()
    # Validate required_model_components
    vals = experiment_id[key]['required_model_components']
    for val in vals:
        if val not in source_type:
            print('Invalid required_model_components for entry:',key,val,'- aborting')
            sys.exit()
    # Validate parent_activity_id
    vals = experiment_id[key]['parent_activity_id']
    for val in vals:
        if val == 'no parent':
            pass
        elif val not in activity_id:
            print('Invalid parent_activity_id for entry:',key,val,'- aborting')
            sys.exit()
    # Validate parent_experiment_id
    vals = experiment_id[key]['parent_experiment_id']
    for val in vals:
        if val == 'no parent':
            pass
        elif val not in experiment_id_keys:
            print('Invalid experiment_id_keys for entry:',key,val,'- aborting')
            sys.exit()

del(experiment_id_keys,key,act,val,val1,val2,vals)
#sys.exit() ; # Turn back on to catch errors prior to running commit

#%% Load remote repo versions for comparison - generate version identifier
for jsonName in masterTargets:
    target = ''.join(['test',jsonName])
    testVal = ''.join(['testVal_',jsonName])
    if jsonName == 'mip_era':
        url = ''.join(['https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/',jsonName,'.json'])
    else:
        url = ''.join(['https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_',jsonName,'.json'])
    # Create input list and load from web
    tmp = [[jsonName,url]] ;
    vars()[target] = readJsonCreateDict(tmp)
    vars()[target] = eval(target).get(jsonName)
    vars()[target] = eval(target).get(jsonName) ; # Fudge to extract duplicate level
    # Test for updates
    vars()[testVal] = cmp(eval(target),eval(jsonName))
    del(vars()[target],target,testVal,url,tmp)
del(jsonName)
# Use binary test output to generate
versionId = ascertainVersion(testVal_activity_id,testVal_experiment_id,
                             testVal_frequency,testVal_grid_label,
                             testVal_institution_id,testVal_license,
                             testVal_mip_era,testVal_nominal_resolution,
                             testVal_realm,testVal_required_global_attributes,
                             testVal_source_id,testVal_source_type,
                             testVal_sub_experiment_id,testVal_table_id,
                             commitMessage)
versionHistory = versionId[0]
versionId = versionId[1]
print('Version:',versionId)
#sys.exit() ; # Use to evaluate changes

#%% Write variables to files
timeNow = datetime.datetime.now().strftime('%c')
offset = (calendar.timegm(time.localtime()) - calendar.timegm(time.gmtime()))/60/60 ; # Convert seconds to hrs
offset = ''.join(['{:03d}'.format(offset),'00']) # Pad with 00 minutes
timeStamp = ''.join([timeNow,' ',offset])
del(timeNow,offset)

for jsonName in masterTargets:
    # Write file
    if jsonName == 'mip_era':
        outFile = ''.join(['../', jsonName, '.json'])
    else:
        outFile = ''.join(['../CMIP6_', jsonName, '.json'])
    # Get repo version/metadata - from src/writeJson.py

    # Extract last recorded commit for src/writeJson.py
    versionInfo1 = getFileHistory(os.path.realpath(__file__))
    versionInfo = {}
    versionInfo['author'] = 'Paul J. Durack <durack1@llnl.gov>'
    versionInfo['institution_id'] = 'PCMDI'
    versionInfo['CV_collection_modified'] = timeStamp
    versionInfo['CV_collection_version'] = versionId
    versionInfo['_'.join([jsonName,'CV_modified'])] = versionHistory[jsonName]['timeStamp']
    versionInfo['_'.join([jsonName,'CV_note'])] = versionHistory[jsonName]['commitMessage']
    versionInfo['previous_commit'] = versionInfo1.get('previous_commit')
    versionInfo['specs_doc'] = 'v6.2.6 (20th December 2017; https://goo.gl/v1drZl)'
    del(versionInfo1)

    # Check file exists
    if os.path.exists(outFile):
        print('File existing, purging:', outFile)
        os.remove(outFile)
    # Create host dictionary
    jsonDict = {}
    jsonDict[jsonName] = eval(jsonName)
    # Append repo version/metadata
    jsonDict['version_metadata'] = versionInfo
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

# Cleanup
del(jsonName,jsonDict,outFile)
del(activity_id,experiment_id,frequency,grid_label,institution_id,license,
    masterTargets,mip_era,nominal_resolution,realm,required_global_attributes,
    source_id,source_type,sub_experiment_id,table_id)
gc.collect()

#%% Update version info from new file/commit history
# Extract fresh recorded commit for src/writeJson.py
versionInfo1 = getFileHistory(os.path.realpath(__file__))
MD5 = versionInfo1.get('previous_commit')
# Now update versionHistory - can use list entries, as var names aren't locatable
if testVal_activity_id:
    key = 'activity_id'
    versionHistoryUpdate(key,commitMessage,timeStamp,MD5,versionHistory)
if testVal_experiment_id:
    key = 'experiment_id'
    versionHistoryUpdate(key,commitMessage,timeStamp,MD5,versionHistory)
if testVal_frequency:
    key = 'frequency'
    versionHistoryUpdate(key,commitMessage,timeStamp,MD5,versionHistory)
if testVal_grid_label:
    key = 'grid_label'
    versionHistoryUpdate(key,commitMessage,timeStamp,MD5,versionHistory)
if testVal_license:
    key = 'license'
    versionHistoryUpdate(key,commitMessage,timeStamp,MD5,versionHistory)
if testVal_mip_era:
    key = 'mip_era'
    versionHistoryUpdate(key,commitMessage,timeStamp,MD5,versionHistory)
if testVal_nominal_resolution:
    key = 'nominal_resolution'
    versionHistoryUpdate(key,commitMessage,timeStamp,MD5,versionHistory)
if testVal_realm:
    key = 'realm'
    versionHistoryUpdate(key,commitMessage,timeStamp,MD5,versionHistory)
if testVal_required_global_attributes:
    key = 'required_global_attributes'
    versionHistoryUpdate(key,commitMessage,timeStamp,MD5,versionHistory)
if testVal_source_type:
    key = 'source_type'
    versionHistoryUpdate(key,commitMessage,timeStamp,MD5,versionHistory)
if testVal_sub_experiment_id:
    key = 'sub_experiment_id'
    versionHistoryUpdate(key,commitMessage,timeStamp,MD5,versionHistory)
if testVal_table_id:
    key = 'table_id'
    versionHistoryUpdate(key,commitMessage,timeStamp,MD5,versionHistory)
if testVal_institution_id:
    key = 'institution_id'
    versionHistoryUpdate(key,commitMessage,timeStamp,MD5,versionHistory)
if testVal_source_id:
    key = 'source_id'
    versionHistoryUpdate(key,commitMessage,timeStamp,MD5,versionHistory)
# Test for changes and report
test = [testVal_activity_id,testVal_experiment_id,testVal_frequency,
        testVal_grid_label,testVal_license,testVal_mip_era,
        testVal_nominal_resolution,testVal_realm,
        testVal_required_global_attributes,testVal_source_type,
        testVal_sub_experiment_id,testVal_table_id,testVal_institution_id,
        testVal_source_id]
if any(test):
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
    print('versionHistory.json updated')
# Cleanup anyway
del(testVal_activity_id,testVal_experiment_id,testVal_frequency,testVal_grid_label,
    testVal_institution_id,testVal_license,testVal_mip_era,testVal_nominal_resolution,
    testVal_realm,testVal_required_global_attributes,testVal_source_id,
    testVal_source_type,testVal_sub_experiment_id,testVal_table_id)

#%% Generate revised html - process experiment_id, institution_id and source_id (alpha order)
#json_to_html.py ../CMIP6_experiment_id.json experiment_id CMIP6_experiment_id.html
args = shlex.split(''.join(['python ./json_to_html.py ',versionId]))
#print(args)
p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='./')
del(args,p)
gc.collect()

#%% Now all file changes are complete, update README.md, commit and tag
# Load master history direct from repo
tmp = [['versionHistory','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/src/versionHistory.json']
  ] ;
versionHistory = readJsonCreateDict(tmp)
versionHistory = versionHistory.get('versionHistory')
versionHistory = versionHistory.get('versionHistory') ; # Fudge to extract duplicate level
del(tmp)
# Test for version change and push tag
versions = versionHistory['versions']
versionOld = '.'.join([str(versions['versionMIPEra']),str(versions['versionCVStructure']),
                       str(versions['versionCVContent']),str(versions['versionCVCommit'])])
del(versionHistory)

if versionId != versionOld:
    #%% Now update Readme.md
    target_url = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/README.md'
    txt = urllib.urlopen(target_url).read()
    txt = txt.replace(versionOld,versionId)
    # Now delete existing file and write back to repo
    readmeH = '../README.md'
    os.remove(readmeH)
    fH = open(readmeH,'w')
    fH.write(txt)
    fH.close()
    print('README.md updated')
    del(target_url,txt,readmeH,fH)

# Commit all changes
args = shlex.split(''.join(['git commit -am ',commitMessage]))
p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='./')

'''
# Merging branches changes the checksum, so the below doesn't work, UNLESS it's a direct master push
if versionId != versionOld:
    # Generate composite command and execute
    cmd = ''.join(['git ','tag ','-a ',versionId,' -m',commitMessage])
    print cmd
    subprocess.call(cmd,shell=True) ; # Shell=True required for string
    # And push all new tags to remote
    subprocess.call(['git','push','--tags'])
    print 'tag created and pushed'
'''