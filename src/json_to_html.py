#!/bin/env python

'''
To run conversion:
(uvcdat)duro@ocean:[src]:[master]:[1168]> json_to_html.py ../CMIP6_experiment_id.json experiment_id CMIP6_experiment_id.html
{u'note': u'Correct getGitInfo call', u'author': u'Paul J. Durack <durack1@llnl.gov>', u'creation_date': u'Wed Aug 31 16:36:15 2016 -0700', u'institution_id': u'PCMDI', u'commit': u'43c311fab67ef26acadbe81f22868691c1357f12', u'latest_tag_point': u'None'}
Notes:
http://stackoverflow.com/questions/6551446/can-i-run-html-files-directly-from-github-instead-of-just-viewing-their-source

PJD 18 Apr 2017    - Reconfigure source_id format to reflect all model components https://github.com/WCRP-CMIP/CMIP6_CVs/issues/264
PJD 31 Jul 2018    - Update to include version info in html head
PJD  7 Aug 2018    - Update version format

'''
# This script takes the json file and turns it into a nice jquery/data-tabled html doc
import argparse,json,re,sys

#%% Create generic header
header = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<meta name="author" content="Paul J. Durack" />
<meta name="description" content="Controlled vocabulary for CMIP6" />
<meta name="keywords" content="HTML, CSS, JavaScript" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="stylesheet" type="text/css" charset="UTF-8" href="jquery.dataTables-1.10.13.min.css" />
<script type="text/javascript" charset="UTF-8" src="jquery-3.2.1.slim.min.js"></script>
<script type="text/javascript" charset="UTF-8" src="jquery.dataTables-1.10.13.min.js"></script>
<script type="text/javascript">
//<![CDATA[
$(document).ready( function () {
    $('#table_id').DataTable();
    } );
//]]>
</script>"""

#%% Argparse extract
verTest = re.compile(r'[6][.][2][.][0-9]+[.][0-9]+') ; # Matching version format 6.2.11.2
parser = argparse.ArgumentParser()
parser.add_argument('ver',metavar='str',type=str,help='For e.g. \'6.2.11.2\' as a command line argument will ensure version information is written to the html output')
args = parser.parse_args()
if re.search(verTest,args.ver):
   version = args.ver ; # 1 = make files
   print "** HTML Write mode - ",version," will be written **"
else:
    print "** Version: ",version," invalid, exiting"
    sys.exit()

#%% Process experiment_id
infile = '../CMIP6_experiment_id.json'
f = open(infile)
dict = json.load(f)
dict1 = dict.get('experiment_id') ; # Fudge to extract duplicate level
dict2 = dict.get('version')
print dict2
#print dict.keys()
fout = infile[:-4] + 'html'
fout = fout.split('/')[-1] ; # Write to local directory
fo = open(fout, 'w')

# Old remote references
#<link rel="stylesheet" type="text/css" href="http://cdn.datatables.net/1.10.12/css/jquery.dataTables.css">
#<script type="text/javascript" src="http://code.jquery.com/jquery-1.12.4.js"></script>
#<script type="text/javascript" charset="utf8" src="http://rawgit.com/WCRP-CMIP/CMIP6_CVs/master/src/jquery.dataTables.js"></script>

print >> fo, ''.join([header, """
<title>CMIP6 experiment_id values</title>
</head>
<body>
<p>WCRP-CMIP CMIP6_CVs version: """,version,"""</p>
<table id="table_id" class="display">"""])

dictOrder = [
'experiment_id','activity_id','description','start_year','end_year','parent_experiment_id',
'parent_activity_id','experiment','additional_allowed_model_components','required_model_components','tier',
'min_number_yrs_per_sim','sub_experiment_id'
]
dictOrderK = [
'activity_id','experiment','tier','sub_experiment_id','parent_experiment_id',
'required_model_components','additional_allowed_model_components','start_year','end_year',
'min_number_yrs_per_sim','parent_activity_id','description'
]

first_row = False
for exp in dict1.keys():
    exp_dict = dict1[exp]
    if not first_row:
        #ids = exp_dict.keys()
        ids = dictOrderK ; # Overwrite ordering
        for hf in ["thead", "tfoot"]:
            print >> fo, "<%s><tr><th>experiment_id</th>" % hf
            for i in ids:
                i = i.replace('_',' ') ; # Remove '_' from table titles
                print >>fo, "<th>%s</th>" % i
            print >> fo, "</tr></%s>" % hf
    first_row = True
    print >> fo, "<tr><td>%s</td>" % exp
    for k in ids:
        st = exp_dict[k]
        #print st
        if isinstance(st, (list, tuple)):
            st = " ".join(st)
        print >> fo, "<td>%s</td>" % st
    print >> fo, "</tr>"
print >> fo, "</table>"

print >> fo, """
</body>
</html>
"""

#%% Process institution_id
infile = '../CMIP6_institution_id.json'
f = open(infile)
dict = json.load(f)
dict1 = dict.get('institution_id') ; # Fudge to extract duplicate level
dict2 = dict.get('version')
print dict2
#print dict.keys()
fout = infile[:-4] + 'html'
fout = fout.split('/')[-1] ; # Write to local directory
fo = open(fout, 'w')

print >> fo, ''.join([header, """
<title>CMIP6 institution_id values</title>
</head>
<body>
<p>WCRP-CMIP CMIP6_CVs version: """,version,"""</p>
<table id="table_id" class="display">"""])

dictOrder = [
'institution_id'
]

first_row = False
for exp in dict1.keys():
    exp_dict = dict1[exp]
    if not first_row:
        ids = dictOrder ; # Overwrite ordering
        for hf in ["thead", "tfoot"]:
            print >> fo, "<%s><tr><th>institution_id</th>" % hf
            for i in ids:
                print >>fo, "<th>Description</th>"
            print >> fo, "</tr></%s>" % hf
    first_row = True
    print >> fo, "<tr><td>%s</td>" % exp
    print >> fo, "<td>%s</td>" % exp_dict
    print >> fo, "</tr>"
print >> fo, "</table>"

print >> fo, """
</body>
</html>
"""

#%% Process source_id
infile = '../CMIP6_source_id.json'
f = open(infile)
dict = json.load(f)
dict1 = dict.get('source_id') ; # Fudge to extract duplicate level
dict2 = dict.get('version')
print dict2
#print dict.keys()
fout = infile[:-4] + 'html'
fout = fout.split('/')[-1] ; # Write to local directory
fo = open(fout, 'w')

print >> fo, ''.join([header, """
<title>CMIP6 source_id values</title>
</head>
<body>
<p>WCRP-CMIP CMIP6_CVs version: """,version,"""</p>
<table id="table_id" class="display">"""])

dictOrder = [
'label_extended','atmospheric_chemistry','atmosphere','ocean_biogeochemistry',
'release_year','cohort','sea_ice','label','institution_id','land_surface',
'aerosol','source_id','ocean','land_ice','activity_participation',
'native_nominal_resolution_atmos','native_nominal_resolution_landIce',
'native_nominal_resolution_ocean']
dictOrderKold = [
'institution_id','release_year','activity_participation','atmosphere',
'nominal_resolution_atmos','ocean','nominal_resolution_ocean','aerosol',
'atmospheric_chemistry','cohort','label','label_extended','land_ice',
'nominal_resolution_landIce','land_surface','ocean_biogeochemistry','sea_ice']
dictOrderK = [
'institution_id','release_year','activity_participation','cohort','label',
'label_extended','atmos','natNomRes_atmos','ocean','natNomRes_ocean','landIce',
'natNomRes_landIce','aerosol','atmosChem','land','ocnBgchem','seaIce']
dictRealmKeys = [
'atmos','ocean','aerosol','landIce','atmosChem','land','ocnBgchem','seaIce']
dictNomResKeys = ['natNomRes_atmos','natNomRes_ocean','natNomRes_landIce']

first_row = False
for exp in dict1.keys():
    exp_dict = dict1[exp]
    # Create table columns
    if not first_row:
        ids = dictOrderK ; # Overwrite ordering
        for hf in ["thead", "tfoot"]:
            print >> fo, "<%s><tr><th>source_id</th>" % hf
            for i in ids:
                i = i.replace('_',' ') ; # Remove '_' from table titles
                print >>fo, "<th>%s</th>" % i
            print >> fo, "</tr></%s>" % hf
    first_row = True
    print >> fo, "<tr><td>%s</td>" % exp
    # Fill columns with values
    for k in ids:
        # Deal with embeds
        if k in dictRealmKeys:
            st = exp_dict['model_component'][k]['description']
        elif k in dictNomResKeys:
            keyVal = k.replace('natNomRes_','')
            st = exp_dict['model_component'][keyVal]['native_nominal_resolution']
        else:
            st = exp_dict[k]
        if isinstance(st, (list, tuple)):
            st = " ".join(st)
        print >> fo, "<td>%s</td>" % st
    print >> fo, "</tr>"
print >> fo, "</table>"
print >> fo, """
</body>
</html>
"""
