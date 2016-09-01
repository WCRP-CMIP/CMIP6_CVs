#!/bin/env python

'''
To run conversion:
(uvcdat)duro@ocean:[src]:[master]:[1168]> json_to_html.py ../CMIP6_experiment_id.json experiment_id CMIP6_experiment_id.html
{u'note': u'Correct getGitInfo call', u'author': u'Paul J. Durack <durack1@llnl.gov>', u'creation_date': u'Wed Aug 31 16:36:15 2016 -0700', u'institution_id': u'PCMDI', u'commit': u'43c311fab67ef26acadbe81f22868691c1357f12', u'latest_tag_point': u'None'}
Notes:
http://stackoverflow.com/questions/6551446/can-i-run-html-files-directly-from-github-instead-of-just-viewing-their-source
'''

# This script takes the json file and turns it into a nice
# jquery/data-tabled html doc
import json
import sys

f = open(sys.argv[1])
dict = json.load(f)
dict1 = dict.get(sys.argv[2]) ; # Fudge to extract duplicate level
dict2 = dict.get('version')
print dict2
#print dict.keys()

if len(sys.argv) > 2:
    fout = sys.argv[3]
else:
    fout = sys.argv[1][:-4] + "html"
    fout = fout.split('/')[-1] ; # Write to local directory
fo = open(fout, "w")

print >> fo, """<html>
<head>
<link rel="stylesheet" type="text/css" href="http://cdn.datatables.net/1.10.12/css/jquery.dataTables.css">
<script type="text/javascript" src="http://code.jquery.com/jquery-1.12.4.js"></script>
<script type="text/javascript" charset="utf8" src="http://rawgit.com/WCRP-CMIP/CMIP6_CVs/master/src/jquery.dataTables.js"></script>
<script>
$(document).ready( function () {
    $('#table_id').DataTable();
    } );
</script>
</head>
<body>
<table id="table_id" class="display">"""

dictOrder = [
'experiment_id','activity_id','description','start_year','end_year','sub_experiment','parent_experiment_id',
'parent_activity_id','experiment','additional_allowed_model_components','required_model_components','tier',
'min_number_yrs_per_sim','sub_experiment_id'
]
dictOrderK = [
'activity_id','experiment','tier','sub_experiment_id','sub_experiment','parent_experiment_id',
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
        if isinstance(st, (list, tuple)):
            st = " ".join(st)
        print >> fo, "<td>%s</td>" % st
    print >> fo, "</tr>"
print >> fo, "</table>"

print >> fo, """
</body>
</html>
"""
