#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 15:17:09 2017
7/10/17 BCM - modified code so that it would work in new oldCMIPS directory 1_1
7/10/17 BCM - took away xml creation section in order to just use old xmls created by peter 2
7/11/17 BCM - incresed robustness of QC and added QC methods like seasonal cycle test 2_2
7/12/17 BCM - modify code so that it works for all models, regardless of match 3
7/17/17 BCM - try to integrate variables with plev into script 4 ---all kinds of issues
7/19/17 BCM -WORKS FULLY FOR 3D VARIABLES. 4_2
7/19/17 BCM -Attempt to get it to work fully for 4D models 4_3
7/19/17 BCM - Attempt to solve issues caused by rogue or faulty xml files and porrly named xml files 4_4
7/20/17 BCM - Attempt to incorporate more 4D QC plots and outputs
7/24/17 BCM - integrate nka aliases and modify to be used for'per' and 'con' runs, added f.close() for read in json, added last cmor.close()
7/24/17 BCM - intergrate con and per loop into code 4_7
7/26/17 BCM - Attempt to modify code so that it can take AMIP data 5
7/31/17 BCM -attempt to solve plotting issues caused by so many AMIP aliases 6

---THIS SCRIPT TAKES OLD CMIP/AMIP DATA AND REPROCESS IT WITH CMOR324 TO PRODUCE IT IN THE FORMAT OF CMIP6---
THIS SCRIPT TAKES A SET OF OLD AMIP OR CMIP DATA (PATH SPECIFIED BY USER), CREATES THE REQUIRED USER_INPUT.JSON FILE BY ATTEMPTING
TO MATCH INFO FOR EACH ALIAS WITH THE INFO FROM THE IPCC TABLES AND OLD AMIP REPORTS. THE MATCHED INFO IS CALLED FROM THE 
AMIP1&2_SOURCE_ID.JSON AND CMIP1&2_SOURCE_ID.JSON FILES. IF NO MATCH IS FOUND DEFAULT/DUMMY INFO IS FILLED IN TO SATISFY CMOR.
THE CODE ALSO MAKES EXCEPTION FOR CERTAIN ALIASES AND VARIABLES THAT HAVE TROUBLESOME DATA. THE CODE WILL NOT RUN PROCESS A VARIABLE
THAT IT CAN NOT FIND A MATCH FOR IN ONE OF THE CMIP6____.JSON TABLES (EG: AMON, OMON, SIMON). IF NO VARIABLE MATCH IS FOUND, THE VARIABLE IS SKIPPED
AND NONE OF THE DATA IS REPROCESSED.
THE CODE THEN OBTAINS THE XMLS FROM THE INPUT DATA PATH AND USES THE INFO FOUND THERE TO LOAD THE CMOR TABLES AND AXIS REQUIRED TO
RUN CMOR_WRITE. IT THEN USING THE FUNCITON 'KLUDGERS' TO CORRECT UNIT ERRORS BROUGHT ABOUT BY THE INPUT DATA. EACH VARIABLE HAS A SET OF 
KNOWN EXCEPTIONS IN A DICTIONARY FOUND IN KLUDGERS, WHICH MUST BE UPDATED WHEN NEW UNITS ERRORS(OR CONVERSIONS) ARE FOUND.
THE NEW, REPROCESSED DATA IS THEN OUTPUT USING CMOR.
THIS DATA IS REOPENED AND QUALITY CONTROL IS PERFORMED. A SINGLE PDF OF SELECT PLOTS IS GENERATED FOR THE COLLECTION OF MODELS 
FOUND FOR EACH VARIABLE. A SINGLE JSON FILE OUTLINING ERRORS RAISED, UNITS ISSUES, AND PRE/POST CMOR DATA AVERAGES/MINS/MAXS FOR
EACH COLLECTION OF MODELS AS WELL
DIFFERENT PLOTS ARE GENERATED FOR 4D AND 3D DATA
@author: musci2
"""
import cmor, gc, json, sys, os, shutil, pylab, math, random, glob, difflib
#import vcs
import cdms2 as cdm
import cdutil as cdu
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from kludgers2 import kludgers
from matplotlib.backends.backend_pdf import PdfPages
gc.collect()
gc.collect()
#%% USER INPUTS

# Variables that are missing from the CMIP6_AMON table used for cmor writinr
MissingVariables = json.load(open('/export/musci2/git/cmip6-cmor-tables/AmonTable_MissingVariables.json'))

#specify run of interst: CONTROL or PERTURBED
for exp in ['AMIP']: #'con','per'

    #specify path where data to be reformatted is located
    #pathin1 = '/oldCMIPs/PJG_StorageRetrieval/CMIP6-STORAGE/mo/' ## PATH FOR CMIP INPUT DATA
    pathin1= '/oldCMIPs/PJG_StorageRetrieval/AMIP2-STORAGE/mo/'  ## PATH FOR MAIP INPUT DATA
    
    #specify where json files and tables needed are stored
    tablepath = '/export/musci2/git/cmip6-cmor-tables/Tables'
    
    # specify place where teh created inputjson files will be saved
    savepath = '/oldCMIPs/ben/'
    
    # specify place where output data is to be saved
    outpath = '/oldCMIPs/ben/CmorData/'+exp # NOT WORKING BECAUSE DON"T HAVE PROPER MOUNT, CODE CAN'T DELTE OLD FILES TO RUN CORRECTLY
    outpath = '/export/musci2/Cmor_Testing/CmorData/'+exp
    
    #grab variables of interest
    variables = glob.glob(pathin1+'*')
    variables.sort()
    #variables = ['/oldCMIPs/PJG_StorageRetrieval/CMIP6-STORAGE/mo/tas']
    
    for Vcount,i in enumerate(variables[114:135]): #84 = tas, #41 = pr, 113 = tos
        varb = variables[variables.index(i)].split('/')[5]
        print Vcount, varb
        if varb in MissingVariables:
            print 'Skipping variable b/c no matching varb in AMON table' 
            continue

        #%% INPUT JSON FILE CREATION WITH LOOP
        
        #create subdirectory path for variable
        pathin = pathin1+varb
    
        #check if autobounds is on, off, or on grid mode
        print cdm.getAutoBounds()
        
        # creates sub direc in users save path to store the large amount of cmor_input json files that will be created
        subdir='input_json_files'
        if not os.path.exists(savepath+subdir):
            os.makedirs(savepath+subdir)
        
        # get the aliases for the data that is to be re-formatted
        lst = os.listdir(pathin)
        lst.sort() ; # Sort alphabetically
        
        print 'Starting'
        #%%
        print ' '
        print 'CREATING USER INPUT JSON'
        # make QC dict
        QualCon = {}
        QualCon[varb]={}
        bounds = list()
        boundsSeas = list()
        models = list()
        GlblAvgs = list()
        LIST = list()
        LowPLevs = list()

        # Read the source json file into memory in order to acess the nested dictionary within
        #with open('/export/musci2/CMIP1&2_source_id.json', 'r') as f: # SOURCE ID FOR CMIP RUNS
        with open('/export/musci2/AMIP1&2_source_id.json', 'r') as f: # SOURCE ID FOR AMIP RUNS
             source_id = json.load(f)
             src_lst=source_id.keys()
             for mod in src_lst:#[0:1]:
                 LIST.append(source_id[mod]['aliases'][0])
        
        # loop through aliases and see if any match the aliases listed in the source_id.json file
             for count,alias in enumerate(lst):
#                 if count > 35:
#                     break
             #for alias in ['gfdl-c04a']:
                 print count,alias
                 if alias.split('-')[0] in ['mean','median']:
                     continue
                 common_user_input_dict={}
                 if alias in LIST:
                     ind = LIST.index(alias)
                     mod = src_lst[ind]
                     srcIDali= source_id[mod]['aliases']
                     print "Match"
                     print alias, srcIDali
                     common_user_input_dict['activity_id']=source_id[mod]['cohort'][0] # required by CMIP6_CV.json
                     activity_id = common_user_input_dict['activity_id']
                     common_user_input_dict['mip_era']= source_id[mod]['activity_participation'][0] # required by CMIP6_CV.json
                     mip_era = common_user_input_dict['mip_era']
                     common_user_input_dict['grid']=source_id[mod]['model_component']['atmos']['description'] # required by CMIP6_CV.json
                     common_user_input_dict['references']=source_id[mod]['reference'][0]
                     common_user_input_dict['source_id']= mod # required by CMIP6_CV.json
                     source_id_ = common_user_input_dict['source_id']
                 else:
                         
                     print alias, 'No Match'
                     common_user_input_dict['activity_id']='CMIP' # required by CMIP6_CV.json
                     activity_id = common_user_input_dict['activity_id']
                     common_user_input_dict['mip_era']= 'NoMatch' # required by CMIP6_CV.json
                     mip_era = common_user_input_dict['mip_era']
                     common_user_input_dict['grid']='NoMatch' # required by CMIP6_CV.json
                     common_user_input_dict['references']='NoMatch' 
                     common_user_input_dict['source_id']= alias # required by CMIP6_CV.json
                     source_id_ = common_user_input_dict['source_id']
                 
        
        
        # if there is an alias matching the alias listed in the source_id json we have a match and then
        # create a user input file with that match
        # create dict that will house the user input files
        #create dictionary that will house user input json files
                 var= os.path.basename(os.path.normpath(pathin)) # extracts variable name by taking it from the last part of the file path specified at the beginning of script       
                 common_user_input_dict['Conventions']='TBD' # required by CMIP6_CV.json
                 common_user_input_dict['calendar']='360_day' #set as 360_day to test, required by cmor
                 common_user_input_dict['_control_vocabulary_file']='CMIP6_CV.json'
                 common_user_input_dict['_AXIS_ENTRY_FILE']='CMIP6_coordinate.json'
                 common_user_input_dict['_FORMULA_VAR_FILE']='CMIP6_formula_terms.json'
                 common_user_input_dict['data_specs_version']='TBD' # required by CMIP6_CV.json
                 common_user_input_dict['frequency']='TBD' # required by CMIP6_CV.json
                 common_user_input_dict['further_info_url']='http://furtherinfo.es-doc.org/NOT_VALID_OUTPUT'#must be properly set, required by CMIP6_CV.json
                 common_user_input_dict['experiment']='TBD' # required by CMIP6_CV.json
                 common_user_input_dict['experiment_id']='TBD' # required by CMIP6_CV.json
                 experiment_id = common_user_input_dict['experiment_id']
                 common_user_input_dict['forcing_index']='0000'# must contain only characters 0 tol 9, required by CMIP6_CV.json
                 common_user_input_dict['grid_label']= 'grz' #MUST MATCH grid_lable options in CMIP6_CV.json set as grz for now, required by CMIP6_CV.json
                 grid_label = common_user_input_dict['grid_label']
                 common_user_input_dict['initialization_index']='0000'# must contain only characters 0 tol 9, required by CMIP6_CV.json
                 common_user_input_dict['nominal_resolution']='10000 km' #MUST MATCH grid_lable options in CMIP6_CV.json set as 10000 km for now, required by CMIP6_CV.json
                 common_user_input_dict['physics_index']='0000'# must contain only characters 0 tol 9, required by CMIP6_CV.json
                 common_user_input_dict['product']='model-output' #model-output is only thing accepted by CMIP6_CV.json file, required by CMIP6_CV.json
                 common_user_input_dict['realm']='Atmosphere' # required by CMIP6_CV.json -ATMOSPHERE FOR AMIP FOR SURE
                 common_user_input_dict['institution_id']='PCMDI' #MUST MATCH TO THE the list of institutions found in the CMIP6_CV.json, set as PCMDI for now, required by CMIP6_CV.json
                 institution_id = common_user_input_dict['institution_id']
                 common_user_input_dict['institution']='TBD' # required by CMIP6_CV.json
                 common_user_input_dict['realization_index']='0000' # must contain only characters 0 tol 9 required by CMIP6_CV.json
                 common_user_input_dict['source']= 'TBD' # required by CMIP6_CV.json
                 common_user_input_dict['source_type']='SLAB' #MUST MATCH source_type options in CMIP6_CV.json set as SLAB for now, required by CMIP6_CV.json
                 common_user_input_dict['sub_experiment']='TBD'# required by CMIP6_CV.json
                 common_user_input_dict['sub_experiment_id']='none' #MUST MATCH sub_exp_id options in CMIP6_CV.json set as none for now, required by CMIP6_CV.json
                 common_user_input_dict['table_id']='TBD' # required by CMIP6_CV.json
                 common_user_input_dict['tracking_prefix']='hdl:21.14100' # must be of this form so use FAKE ONE, required by CMIP6_CV.json
                 common_user_input_dict['variable_id']= var # required by CMIP6_CV.json
                 variable_id = common_user_input_dict['variable_id']
                 common_user_input_dict['variant_label']='r0i0p0f0' # must match a certain format, required by CMIP6_CV.json
                 member_id = common_user_input_dict['variant_label']
                 common_user_input_dict['creation_date']='TBD' # required by CMIP6_CV.json
                 common_user_input_dict['outpath']= outpath
                 common_user_input_dict['output_path_template']='<mip_era><activity_id><institution_id><source_id><experiment_id><_member_id><table><variable_id><grid_label><version>'
                 common_user_input_dict['output_file_template']='<variable_id><table><source_id><experiment_id><_member_id><grid_label>'
                 common_user_input_dict['license']='CMIP6 model data produced by Lawrence Livermore PCMDI is licensed under a Creative Commons Attribution ShareAlike 4.0 International License (https://creativecommons.org/licenses). Consult https://pcmdi.llnl.gov/CMIP6/TermsOfUse for terms of use governing CMIP6 output, including citation requirements and proper acknowledgment. Further information about this data, including some limitations, can be found via the further_info_url (recorded as a global attribute in this file) and at https:///pcmdi.llnl.gov/. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law.' # required by CMIP6_CV.json
                 
        
        
        # converts each dictionary into individual user_input_json files for the variable and each model inside the variable, saves to user specified folder
                 f.close() # close json file used to read in info
                 j = json.dumps(common_user_input_dict, sort_keys=True, indent=4, ensure_ascii=True,separators=(',',':'))
                 completePath=os.path.join(savepath,subdir,'user_input_'+var+'_'+exp+'_'+mod+'.json')
                 f = open(completePath, 'w')
                 print >> f, j
                 f.close()
                 print 'User_input.json created'
                 
                 #%% ADD EXCEPTIONS FOR VERY TROUBLESOME DATA AND REPORT IT TO QC FILE
                 print ' '
                 print 'CHECK TO SEE IF ALIAS OR VAR IS IN THE TROUBLESOME/EXCEPTION BUCKET -- SKIP IF SO'
                 if alias in ['derf-95a','mpi-96a']:
                     QualCon[var][alias]=['Error: axis longitude has bounds values spanning more than 360 degrees']
                     print 'Error: axis longitude has bounds values spanning more than 360 degrees'
                     continue
                 elif alias in ['ukmo-98b','ukmo-98d','ukmo-98e']: #ukmo-98b
                     QualCon[var][alias]= ['error time_bnds have gaps between them-setAutoBounds did not work. data gaps were in 1981(ukmo-98a) and 1983(ukmo-98d), netire yr of 1984 is missing(ukmo-98e)']
                     print 'Time bounds have gaps between them'
                     continue
                 elif alias in ['ncar-98a'] and var in ['ps']:
                     QualCon[var][alias]= ['when the data is read in from the xml only the latitude data makes it through, leaving the data of the shape (64,). Although netcdf files look ok (only looked at two though)']
                     continue
                 elif alias in ['ecpc-02a7'] and var in ['rlut']:
                     QualCon[var][alias]= ['error time_bnds have gaps between them-setAutoBounds did not work. data gaps is 1981, netcdf file for that year is missing']
                     print 'Time bounds have gaps between them'
                     continue
                 elif alias in ['derf-98a'] and var in ['ta']:
                     QualCon[var][alias]=['Error: axis longitude has bounds values spanning more than 360 degrees']
                     print 'Error: axis longitude has bounds values spanning more than 360 degrees'
                     continue
        
                 #%% ISOLATE the xml of interest
                 print ' '
                 print 'OBTAIN XML OF INTEREST'
                 lstall = ' '
                 del(lstall) # Create and delete a lstall at each loop so that if xml is not found, the old lstall is not used in next iteratio of loop
                 # Use the old xmls made from Peter's previous workk (possible only for CMIP data, AMIP xml had to be remade)
                 trapall = pathin+'/'+alias+'/*.xml'
                 lstall2 = glob.glob(trapall)
                 
                 if exp in ['con','per']:  
                     if var in ['hfss'] and alias in ['csiro-c97a']: # adding special excpetion because of faulty xml file
                         lstall = pathin+'/'+alias+'/BEN.xml'
                     else:
                         for count,i in enumerate(lstall2):
                             #print lstall2[count].split('/')[7]
                             print 'try'
                             if '_'+str(exp)+'.xml' in lstall2[count].split('/')[7]:
                                 gotEm = lstall2.index(i)
                                 lstall=lstall2[gotEm]
                                 print lstall
                             elif exp in ['con'] and '_'+str(alias)+'.xml' in lstall2[count].split('/')[7]:
                                 gotEm = lstall2.index(i)
                                 lstall=lstall2[gotEm]
                                 print lstall 
                 else:
                     xml = varb+'_'+alias+'_'+'BEN.xml'
                     try: 
                         lstall=lstall2[lstall2.index(pathin+'/'+alias+'/'+xml)]
                         skip = 'no'
                     except ValueError:
                         print 'NO XML file in this path'
                         skip ='yes'
                         continue
                     #lstall = lstall2[0]
                     #lstall = '/oldCMIPs/PJG_StorageRetrieval/AMIP2-STORAGE/mo/pr/bmrc-01a/BEN.xml'
                                
                 
                 #%% CMOR STUFF STARTS HERE
                 print ' '
                 print 'LOAD CMOR TABLE AND AXES'
                 
                 cmor.setup(inpath=tablepath,netcdf_file_action=cmor.CMOR_REPLACE_4)
                 #takes the json input file just created above and feeds it to CMOR, also converts from unicode to ascii string
                 cmor.dataset_json(completePath.encode('ascii','ignore')) 

                 # read the data into memory with cdms2
                 print 'Loading input file into memory'
                 try: 
                     f       = cdm.open(lstall,'r')
                     skip = 'no'
                 except NameError:
                     print "NO xml file in this path"
                     skip = 'yes'
                     continue
                 
                 print var
                 #d       = f(var.strip()) ; # [] creates a file variable, () loads the variable into memory
                 d=f(var.strip(),squeeze=1) # squeeze gets rid of all singleton dimensions)
                 print d.shape ;         
                
                 lat     = d.getLatitude()
                 lon     = d.getLongitude()
                 time    = d.getTime()
                 #print time.getBounds()
                 
                 if time.getBounds() == None:
                     cdm.setAutoBounds('on')
                     print 'time bounds could not be found, set auto bounds on'
                     BoundsIssue = 'Had to set AutoBounds = ON, b/c time bounds could not be found'                    
                 print time
                 
                 try:
                     lev = d.getLevel()
                     print lev
                 except AttributeError:
                     print '3D variable, no levels'
                     
                 # Force local file attribute as history
                 cmor.set_cur_dataset_attribute('history',f.history);
                 
                 #if 'sic' in varName:
                 #    table   = 'CMIP6_Amon.json'
                 #else:
                 #    table   = 'CMIP6_Omon.json'
                 table = 'CMIP6_Amon.json'
                 if "Amon" in table:
                     table_ = "Amon"
                 else:
                     table_ = "Omon"
                 cmor.load_table(table)
                 print 'table loaded'
                 #cdm.setAutoBounds(1)
                 #axes    = [ {'table_entry': 'time2',
                 axes    = [ {'table_entry': 'time',
                              ### NOT SURE HOW THIS CHANGE WILL PROPOGATE FOR ALL VARIABLES< NOTE THE CHANGE TO 'time.units !!!
                              'units': time.units},#'days since 1870-01-01'}, # Calendar specific
                            {'table_entry': 'latitude',
                             'units': 'degrees_north',
                             'coord_vals': lat[:],
                             'cell_bounds': lat.getBounds()}, ### was GIVING ERROR WHEN RUN WITH XML -- resolved by fixing path issue, need to read in xml from the folder it was generated in
                             {'table_entry': 'longitude',
                              'units': 'degrees_east',
                              'coord_vals': lon[:],
                              'cell_bounds': lon.getBounds()}
                              ]
                 
                 
                 if len(d.shape) > 3:
                     axes.append({'table_entry': 'plev19',#'plev19', # plev19
                                  ### NOT SURE HOW THIS CHANGE WILL PROPOGATE FOR ALL VARIABLES< NOTE THE CHANGE TO 'lev.units !!!
                                  'units': lev.units,#'Pa',
                                  'coord_vals': lev[:],
                                  'cell_bounds': lev.getBounds()})
                     print '!!!4D Variable!!!'
                     levUni = lev.units
                     if lev.units in ['','lev']:
                         lev.units = 'Pa'
                         levUni ="Had to force units to be Pa b/c they were blank or'lev' on input"
                         axes[3]['units']='Pa'
                     levLow = lev[0]
                 else:
                     levUni = ' '
                     levLow = ' '         
                 print 'Axis done'
                 axis_ids = list()
                 for axis in axes:
                     axis_id = cmor.axis(**axis)
                     axis_ids.append(axis_id)
                     #print axis
                     #axis_ids = ['time','latitude','longitude']
                     #axis_ids = [time,lat,lon]
                     #print axis_ids
                 print 'Axis id set'   
        
                 #%% DECLAR PER VARIABLE CASES --- KLUDGERS - should replace with function when gets too long
                 print ' '
                 print 'PERFOMRING KLUDGERS'
                 returns = kludgers(var, d, axis_ids, alias )
                 uniMsg = returns[0]
                 d.units = returns[1]
                 varid = returns[2]
                 Converter =returns[3]
                 oldUnits = returns[4]
                 print 'here', uniMsg, oldUnits, d.units, Converter
                 d=d*Converter
                 
                 
                 #%% OUTPUT CMOR
                 print ' '
                 print 'OUTPUTING CMOR FILE'
                 if len(d.shape) > 3:
                     d = d.swapaxes(1,3).swapaxes(1,2)
                 values  = np.array(d[:],np.float32)
                 cmor.set_deflate(varid,1,1,1) ; # shuffle=1,deflate=1,deflate_level=1 ; CMOR 3.0.6+
                 PreCmor = d[0,] #take first slice of preCMor data
                 if len(d.shape) > 3:
                     #AVGD ACROSS ALL LEVELS
                     cdm.setAutoBounds('on') # CANT FIND BOUNDS WHEN USING 4D VARIABLE, SO SET AUTO BOUNDS TO SOLVE ISSUE
                     PreGblAvg = cdu.averager(cdu.averager(cdu.averager(PreCmor,axis=0,weights=None),axis=0,weights=None),axis = 0, weights=None) # take global average of pre-cmor data;
                     BoundsIssue = 'Had to set AutoBounds = ON'
                     print 'AutoBounds ON'
                     #cdm.setAutoBounds('off')
                     #print 'truned aut bounds off and on' 
                 else:
                     PreGblAvg = cdu.averager(cdu.averager(PreCmor,axis=0,weights=None),axis=0,weights=None) # take global average of pre-cmor data;
                     BoundsIssue = ''
                     print '3D variable, no levels'
          
                 #specify path where the cmor output was placed
                 DUNNO = 'CMIP6'
                 readin = os.path.join(outpath,DUNNO,activity_id,institution_id,source_id_,experiment_id,member_id,table_,variable_id,grid_label)+'/'
                 tst = glob.glob(readin) # creates list of cmor output files found in the output path
                 #clean up old cmor outputs for each specific model and variable before writing newest output
                 #tst0=tst[0]
                 try:
                     shutil.rmtree(tst[0]) ; # Remove existing data
                 except IndexError: #list 'tst' will be empty if there is nothing there so a index error will be raised
                     print 'nothing to clean up'
                 
                 ## write out cmor output
                 cmor.write(varid,values,time_vals=time[:],time_bnds=time.getBounds())
                 print 'cmor file created'
                 f.close()
                 cmor.close()
                 
                 
                 #%% REOPEN CMOR OUTPUT FILE AND PERFROM QC ON THE DATA
                 print ' '
                 print 'REOPENING CMOR---QC'
                 
                 marker = ['s','v','d','4',',', '+', '.', 'o', '*','h','^','8']
                 random.shuffle(marker)
                 
                 #specify path where the cmor output was placed
                 readin2 = os.path.join(outpath,DUNNO,activity_id,institution_id,source_id_,experiment_id,member_id,table_,variable_id,grid_label)+'/*/*'
                 #readin2 = '/export/musci2/CMIP6/CMIP6/ISMIP6/PCMDI/PCMDI-test-1-0/piControl-withism/r11i1p1f1/Amon/'+var+'/gr/*/*' # path for aliases without a match
                 tst2 = glob.glob(readin2) # creates list of cmor output files found in the output path
                 tst20=tst2[0]
                 fff = cdm.open(tst20,'r')
                 ddd=fff(var)
                 
                 latCmor = ddd.getLatitude()
                 lonCmor = ddd.getLongitude()
                 timeCmor = ddd.getTime()
                 if len(d.shape) > 3:
                     levCmor = ddd.getLevel()
                     levCmorUni = levCmor.units
                     levCmorLow = levCmor[0]
                 else:
                     levCmorUni = ' '
                     levCmorLow = ' '
        
        ## SEASONAL ZONAL AVG         
                 # Set Spatial region of interest
                 #region = cdu.region.domain(latitude=(30,65.))
                 #selectr data from that region only
                 regddd = fff(var,latitude = (30, 65))
                 regddd = regddd[0:12] #takes first twleve slices in time of array
                 # obtain time series of reginally averaged variable
                 t = regddd.getTime()
                 c = t.asComponentTime()
                 MonDic = {}
                 SeasAvg =list()
                 Months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                 for i in Months:
                     MonDic[i] = list()
                 for k in xrange(len(t)):
                     #if k < 360: #359< k < 720:
                     j = c[k].month
                     MonDic[Months[j-1]].append(k)       
                 if len(d.shape) > 3:
                     #AVGD ACROSS ALL LEVELS
                     RegAvg = cdu.averager(cdu.averager(cdu.averager(regddd,axis=regddd.getAxisIds().index('lat'),weights=None),axis=regddd.getAxisIds().index('lon')-1,weights=None),axis = 1, weights=None)
                     # take reg avg over lowest pressure level
                     regdddLowP = regddd[:,0,:,:]
                     SeasRegAvgLowP = cdu.averager(cdu.averager(regdddLowP,axis=regdddLowP.getAxisIds().index('lat'),weights=None),axis=regdddLowP.getAxisIds().index('lon')-1,weights=None)
                 else:
                     RegAvg = cdu.averager(cdu.averager(regddd,axis=regddd.getAxisIds().index('lat'),weights=None),axis=regddd.getAxisIds().index('lon')-1,weights=None)
                 boundsSeas.append(max(RegAvg))
                 boundsSeas.append(min(RegAvg))
                 ## For SeasAvgs
                 xMon = range(1, 13)
                 plt.figure(4)
                 pylab.xticks(xMon, Months)
                 plt.plot(xMon,RegAvg.tolist(), marker = marker[0], linestyle='--', label = alias)
                 #plot Seasonal avg for the lowest pressure level 
                 if len(d.shape) > 3:
                     plt.figure(7)
                     pylab.xticks(xMon, Months)
                     plt.plot(xMon,SeasRegAvgLowP.tolist(), marker=marker[0], linestyle='--', label = alias)             
                 
        ## GLOBAL AVG        
                 # Generate first timestep value
                 CmorData = ddd[0,] #take first time slice of array
                 #cdutil.getAxisWeight()
                 ## THIS METHOD ONLY WORKS IF LON IS ALWAYS SECOND -- NEED TO MAKE MROE ROBUST -Take global avg of cmor output data
                 if len(d.shape) > 3:
                     #AVGD ACROSS ALL LEVELS
                     GblAvg = cdu.averager(cdu.averager(cdu.averager(CmorData,axis=CmorData.getAxisIds().index('lat'),weights=None),axis=CmorData.getAxisIds().index('lon')-1,weights=None), axis = 0, weights=None) ;
                     #Obtain glbl avg of vertical profile
                     VertGblAvg = cdu.averager(cdu.averager(CmorData,axis=CmorData.getAxisIds().index('lat'),weights=None),axis=CmorData.getAxisIds().index('lon')-1,weights=None)
                     plt.figure(6)
                     yVert = plt.plot(VertGblAvg.tolist(),levCmor[:].tolist(), marker='o', linestyle='--', label = alias )
                     plt.setp(yVert, linewidth =0.85)
                    
                 
                 else:
                     GblAvg = cdu.averager(cdu.averager(CmorData,axis=CmorData.getAxisIds().index('lat'),weights=None),axis=CmorData.getAxisIds().index('lon')-1,weights=None)
                 # extra arguemetns for axis above are to ensure that the axis for lat and lon are being taken even when a variable with levels is included
                 QualCon[var][alias]={}
                 QualCon[var][alias]['PreCMOR'] = ['Global Avg: '+str(PreGblAvg)+' '+oldUnits,'Min: '+ str(PreCmor.min()),'Max: ' + str(PreCmor.max()),' LowestLev: '+str(levLow)+' '+levUni,'  '+BoundsIssue]
                 QualCon[var][alias]['CMOR']=["Global Avg: " + str(GblAvg)+' '+ddd.units+' '+uniMsg, 'Min: ' + str(CmorData.min()), 'Max: ' + str(CmorData.max()),' LowestLev: '+str(levCmorLow)+' '+levCmorUni,'  '+BoundsIssue] ## Add global average and min max to QC dictionary
        
        ## ZONAL AVG -avgs across all longitudnal levels
                 if len(d.shape) > 3:
                     #AVGD ACROSS ALL LEVELS
                     dza = cdu.averager(cdu.averager(CmorData,axis=CmorData.getAxisIds().index('lon')),axis = 0) # take zonal average of one time slice
                     #AVGD ACROSS LOWEST P LEVEL
                     dzaLP=CmorData[0,]
                     dzaLowP = cdu.averager(dzaLP,axis=dzaLP.getAxisIds().index('lon'))
                 else:
                     dza = cdu.averager(CmorData,axis=CmorData.getAxisIds().index('lon')) # take zonal average of one time slice
                
                
                
                 
                
                 modelmax = 27.0
                 n = math.ceil(len(lst)/modelmax)
                 if count <= modelmax:
                     fignum = 1
                 elif modelmax*2 >= count > modelmax:
                     fignum = 2
                 elif modelmax*3 >= count >modelmax*2:
                     fignum = 3
                 #plot data for the zonal avg at one time slice
                 
                 plt.figure(1)
                 plt.figure(1,figsize=(10,20))
                 plt.plot(latCmor[:].tolist(), dza.tolist(), label = alias)
#                 if len(lst) < 30:
#                     plt.plot(latCmor[:].tolist(), dza.tolist(), label = alias)
#                 else:
#                     plt.subplot(n,1,fignum)
#                     plt.plot(latCmor[:].tolist(), dza.tolist(), label = alias)
#                     pylab.legend(loc='center left', bbox_to_anchor=(0.95, 0.5))
                     
                 if len(d.shape) > 3:
                     plt.figure(8)
                     plt.plot(latCmor[:].tolist(), dzaLowP.tolist(), label = alias)             
        
        
        
        
        
        
        
        ## DRIFT
                 if len(d.shape) > 3:
                     #AVGD ACROSS ALL LEVELS
                     drift = cdu.averager(cdu.averager(cdu.averager(ddd,axis=ddd.getAxisIds().index('lat'),weight='generate'),axis=ddd.getAxisIds().index('lon')-1,weight='generate'), axis = 1, weight='generate') # take global avergae for each time, get an array of glbl avg at each time
                 else:
                     drift = cdu.averager(cdu.averager(ddd,axis=ddd.getAxisIds().index('lat'),weight='generate'),axis=ddd.getAxisIds().index('lon')-1,weight='generate') # take global avergae for each time, get an array of glbl avg at each time             
                 bounds.append(drift.max())
                 bounds.append(drift.min())
                 # plot the data for the glbl avg vs time, aka drift
                 plt.figure(2)
                 y = plt.plot(timeCmor[:].tolist(), drift.tolist(), label = alias)
                 plt.setp(y, linewidth =0.85) # decrease linewidth
                 
        ## FOR BAR CHARTS
                 models.append(alias)
                 GlblAvgs.append(GblAvg)
                 if len(d.shape) > 3:
                     LowPLevs.append(levCmorLow)
                 
                 print ddd.units

                 cdm.setAutoBounds('grid') # Set this back to the default value
                 print "AutoBounds = 'grid'(default)"
                 fff.close()
                 cmor.close()
        #%% PLOTTING 
        print ' '
        print 'CREATING PLOTS FOR QC'
        mpl.rc('figure', figsize=(15,9))
        if skip == 'yes':
            print 'skipping variable b/c no xml'
            continue
        # Creates the plot of zonal mean for one time slice 
        ZonalAvg = plt.figure(1)
        plt.figure(1,figsize=(10,20))
        plt.ylabel(str(var)+' ('+ddd.units+')')
        plt.xlabel('long degrees north')
        plt.title(str(var)+' Zonal Average of one time slice')
        lgd2 = pylab.legend(loc='center left', bbox_to_anchor=(0.95, 0.5)) # create legend and put it outside of plot
        
        #Creates plot of global avg vs time -AKA DRIFT
        TimeDrift = plt.figure(2)
        plt.ylabel(str(var)+' ('+ddd.units+')')
        plt.xlabel('days since 1870-01-01')
        print bounds
        if max(bounds) > 1e17: #reomve missing data that shows up as a max
            remove = bounds.index(max(bounds))
            del bounds[remove]
            print "bounds removed"
            print bounds
        elif min(bounds) < -1e17:#reomve missing data that shows up as a min
            remove = bounds.index(min(bounds))
            del bounds[remove]
            print "bounds removed"
        ymax = max(bounds)+0.02*max(bounds) # set the plot bounds
        ymin = min(bounds)-0.02*min(bounds) 
        plt.ylim([ymin,ymax])
        plt.title(str(var)+' Global Average vs time')
        lgd = pylab.legend(loc='center left', bbox_to_anchor=(0.95, 0.5)) # create legend and put it outside of plot
        
        # Creates bar plot of global avgs to check units
        BarPlot = plt.figure(3)
        y_pos = np.arange(len(models))
        plt.barh(y_pos, GlblAvgs, align='center', alpha=0.5)
        plt.yticks(y_pos, models)
        plt.xlabel(str(var)+' '+ddd.units)
        plt.title('Global averages at one time slice')
        
       ## 4D Plotting
        if len(d.shape) > 3:
            ZonalAvgLowP = plt.figure(8)
            plt.ylabel(str(var)+' ('+ddd.units+')')
            plt.xlabel('long degrees north')
            plt.title(str(var)+' Lowest Plev -Zonal Average of one time slice')
            lgd6 = pylab.legend(loc='center left', bbox_to_anchor=(0.95, 0.5)) # create legend and put it outside of plot 
        
        ## Creates bar plot of lowest pressure levels for 4D variables    
            BarPlotPress = plt.figure(5)
            plt.barh(y_pos, LowPLevs, align='center', alpha=0.5)
            plt.yticks(y_pos, models)
            plt.xlabel('Lowest Pressure Level')
            plt.title('Lowest Pressure level for each model')
        
        ##Creates verticla profile of global average
            print 'setting labels for vert plot'    
            VertProfGblAvg = plt.figure(6)
            plt.gca().invert_yaxis()
            plt.ylabel('Pressure level in Pa??')
            plt.xlabel(str(var)+' ('+ddd.units+')')
            plt.title(str(var)+' -Vertical Profile of Global Avg')
            lgd4 = pylab.legend(loc='center left', bbox_to_anchor=(0.95, 0.5)) # create legend and put it outside of plot
            
            SeasClimateLowP = plt.figure(7)
            plt.ylabel(str(var)+' '+ddd.units)
            plt.title('Lowest Plev - Seasonal Zonal Avgs for 30N to 65N')
            lgd5 = pylab.legend(loc='center left', bbox_to_anchor=(0.95, 0.5))
        
        ##Creates plot of one seasonal cycle
        SeasonalClimate = plt.figure(4)
        plt.ylabel(str(var)+' '+ddd.units)
        plt.title('Seasonal Zonal Avgs for 30N to 65N')
        if max(boundsSeas) > 1e19: #reomve missing data that shows up as a max
            remove = boundsSeas.index(max(boundsSeas))
            del boundsSeas[remove]
        elif min(boundsSeas) < -1e17:
            remove = bounds.index(min(boundsSeas))
            del boundsSeas[remove]    
        ymax = max(boundsSeas)+0.02*max(boundsSeas) # set the plot bounds
        ymin = min(boundsSeas)-0.02*min(boundsSeas)
        plt.ylim([ymin,ymax])
        lgd3 = pylab.legend(loc='center left', bbox_to_anchor=(0.95, 0.5)) # create legend and put it outside of plot
        
        plt.show()
        
        #%% FILE CREATION
        print ' '
        print 'CREATING AND SAVING FILES' 
        # creates sub direc in output location for placing Quality cntrol items
        subdir='QC'
        if not os.path.exists(outpath+'/'+subdir):
            os.makedirs(outpath+'/'+subdir)
            
        # places gloabl averaging json files in QC folder
        jj = json.dumps(QualCon, sort_keys=True, indent=4, ensure_ascii=True,separators=(',',':'))
        completePath=os.path.join(outpath,subdir,var+'.json')
        ff = open(completePath, 'w')
        print >> ff, jj
        ff.close()
        print 'QC json created'

        # places plot files in QC folder
        pp = PdfPages(os.path.join(outpath,subdir,var+'.pdf'))
        pp.savefig(BarPlot, dpi = 400, transparent = True)
        pp.savefig(ZonalAvg, dpi = 400, bbox_extra_artists=(lgd2,), bbox_inches='tight', transparent = True)
        pp.savefig(TimeDrift, dpi = 400, bbox_extra_artists=(lgd,), bbox_inches='tight', transparent = True)
        pp.savefig(SeasonalClimate, dpi = 400, bbox_extra_artists=(lgd3,), bbox_inches='tight', transparent = True) # extra arguments make sure legend is not cropped off when saving
        if len(d.shape) > 3:
            pp.savefig(BarPlotPress, dpi = 400, transparent = True)
            pp.savefig(VertProfGblAvg, dpi = 400, bbox_extra_artists=(lgd4,), bbox_inches='tight', transparent = True)
            pp.savefig(SeasClimateLowP, dpi = 400, bbox_extra_artists=(lgd5,), bbox_inches='tight', transparent = True)
            pp.savefig(ZonalAvgLowP, dpi = 400, bbox_extra_artists=(lgd6,), bbox_inches='tight', transparent = True)
        pp.close()
        
        print 'done'
                 # Cleanup
                 #del(outFile,var,f,d,lat,lon,time) ; gc.collect()
                 #os.remove('tmp.json')
                 #os.remove('tmp.xml')


#
#t=d.getTime()
#
#c=t.asComponentTime()
#
#ttt = ddd.getTime()
#
#ccc=ttt.asComponentTime()
#
#t[0]
#Out[13]: 0.0
#
#ttt[0]
#Out[14]: 0.5
#
#t[1]
#Out[15]: 1.0
#
#ttt[1]
#Out[16]: 1.5
#
#c[0]
#Out[17]: 1600-1-1 0:0:0.0
#
#ccc[0]
#Out[18]: 1870-1-1 12:0:0.0
#
#c[1]
#Out[19]: 1600-2-1 0:0:0.0
#
#ccc[1]
#Out[20]: 1870-1-2 12:0:0.0
#
#c[0].year
#Out[21]: 1600
#
#ccc[0].year
#Out[22]: 1870
#
#c[0].month
#Out[23]: 1
#
#ccc[0].month
#Out[24]: 1
#
#c[1].month
#Out[25]: 2
#
#ccc[1].month
#Out[26]: 1
#
#d.shape
#Out[27]: (1200, 48, 96)
#
#ddd.shape
#Out[28]: (1200, 48, 96)
#
#d.getTime()
#Out[29]: 
#   id: time
#   Designated a time axis.
#   units:  months since 1600-1-1
#   Length: 1200
#   First:  0.0
#   Last:   1199.0
#   Other axis attributes:
#      calendar: noleap
#      axis: T
#      realtopology: linear
#   Python id:  0x7ff3c96a1c10
#
#ddd.getTime()
#Out[30]: 
#   id: time
#   Designated a time axis.
#   units:  days since 1870-01-01
#   Length: 1200
#   First:  0.5
#   Last:   1199.5
#   Other axis attributes:
#      realtopology: linear
#      long_name: time
#      standard_name: time
#      calendar: 360_day
#      axis: T
#   Python id:  0x7ff3c9675c90




