#!/bin/env python

"""
To run conversion:
(uvcdat)duro@ocean:[src]:[master]:[1168]> json_to_html.py ../CMIP6_experiment_id.json experiment_id CMIP6_experiment_id.html
{u'note': u'Correct getGitInfo call', u'author': u'Paul J. Durack <durack1@llnl.gov>', u'creation_date': u'Wed Aug 31 16:36:15 2016 -0700', u'institution_id': u'PCMDI', u'commit': u'43c311fab67ef26acadbe81f22868691c1357f12', u'latest_tag_point': u'None'}
Notes:
http://stackoverflow.com/questions/6551446/can-i-run-html-files-directly-from-github-instead-of-just-viewing-their-source

"""
"""2017-2022
PJD 18 Apr 2017    - Reconfigure source_id format to reflect all model components https://github.com/WCRP-CMIP/CMIP6_CVs/issues/264
PJD 31 Jul 2018    - Update to include version info in html head
PJD  7 Aug 2018    - Update version format
PJD 25 Apr 2019    - Updated sources to latest 1.10.13 -> 1.10.18; 3.2.1 -> 3.3.1
PJD 25 Sep 2019    - Updated to redirect contents from rawgit.com to github pages (https://wcrp-cmip.github.io/CMIP6_CVs/)
PJD 30 Apr 2020    - Updated jquery 3.3.1 -> 3.5.0, dataTables 1.10.18 -> 1.10.20 to deal with
                     jquery security advisories https://github.com/WCRP-CMIP/CMIP6_CVs/issues/916
                   - Download file from https://jquery.com/download/ - select "Download the compressed, production jQuery 3.5.0 slim build"
                   - Download files from https://datatables.net/download/ [jQuery 3 and dataTables selected, minified];
                     copy css/jquery.dataTables.min.css and js/jquery.dataTables.min.js (updating *dataTables* -> *dataTables-1.10.20*)
                   - Update jquery.dataTables-1.10.20.min.js line 156 update ,aLengthMenu:[10,25,50,100], ->
                     ,aLengthMenu:[5,10,25,50,100,150,200,250,300,350,400], (use jquery.dataTables.js for location lookup [non-minified])
PJD 13 Nov 2020    - Updated for Py3
PJD 13 Nov 2020    - Updated to include line breaks experiment_id
PJD 14 Nov 2020    - Further tweaks to meet strict HTML format conventions
PJD 16 Nov 2020    - Further updates to CMIP6_CVs content to meet strict html standards
                    https://www.w3.org/International/questions/qa-html-encoding-declarations
                    https://validator.w3.org/check
PJD 29 Sep 2021    - Add googleAnalyticsTag.js call
PJD 17 Feb 2022    - Updated sources to latest 1.10.20 -> 1.11.4; 3.5.0 -> 3.6.0
                   - Update jquery.dataTables-1.11.4.min.js line 163-164 update
                   ,aLengthMenu:[10,25,50,100], ->
                   ,aLengthMenu:[5,10,25,50,100,150,200,250,300,350,400],
                   - macOS update files to remove
                   extended attributes "$ xattr -c jquery-3.6.0.slim.min.js", "$ xattr -c jquery.dataTables-1.11*"
                   file permissions "$ chmod 644 jquery.dataTables-1.11*"
                   - Update dataTables styling
                   <table id="table_id" class="display"> ->
                   <table id="table_id" class="display compact" style="width:100%">
MSM 24 May 2022    - Add code for license table
PJD 22 Jun 2022    - Updated dataTable libraries to latest 1.11.4 -> 1.12.1;
                   - Update jquery.dataTables-1.12.1.min.js line 167 update
                   ,aLengthMenu:[10,25,50,100], ->
                   ,aLengthMenu:[5,10,25,50,100,150,200,250,300,350]
                   - macOS update files to remove
                   extended attributes "$ xattr -c jquery.dataTables-1.12*"
                   file permissions "$ chmod 644 jquery.dataTables-1.12*"
                   - TODO: Update default page lengths
MSM 06 Dec 2022    - Add citation data (retrieved from citation service if -r option provided) and add links to each page at the top
"""
"""2023
PJD 21 Feb 2023    - Updated args var to argDict, conflict issue with calling function
PJD 22 Feb 2023    - Updated sources to latest 1.12.1 -> 1.13.2; 3.6.0 -> 3.6.3
                   - Update jquery.dataTables-1.13.2.min.js line 71576 update
                   ,aLengthMenu:[10,25,50,100], ->
                   ,aLengthMenu:[5,10,25,50,100,150,200,250,300,350,400],
                   - macOS update files to remove
                   extended attributes "$ xattr -c jquery-3.6.3.slim.min.js", "$ xattr -c jquery.dataTables-1.13*", "$ xattr -c 230222_DataTables-1p13p3.zip"
                   file permissions "$ chmod 644 jquery.dataTables-1.13*"
                   - Update dataTables styling
                   <table id="table_id" class="display"> ->
                   <table id="table_id" class="display compact" style="width:100%">
PJD 21 Jun 2023    - Updated to point to PCMDI/assets jquery (3.7.0) and dataTables (1.13.4) libraries
PJD 26 Jun 2023    - updated github.com/pcmdi/assets to separate jquery/dataTables source - see https://github.com/PCMDI/assets/pull/5
"""
# This script takes the json file and turns it into a nice jquery/data-tabled html doc
import argparse
from collections import defaultdict
import gzip
import json
import os
import re
import requests
import sys


def retrieve_citation_data_models(source_ids, regen=False):
    """
    Retrieve citation information from either the citation service or
    a cached JSON file.

    Parameters
    ----------
    source_id
        List of source ids to check for
    granularity
        either 'model' or 'experiment'
    regen
        If false return data from cached file, if false query citation service

    Returns a dictionary of the form {source_id: {DRS_ID: DOI_URL}}
    """
    CITATION_DATA_SOURCE = "https://www.wdc-climate.de/ui/cerarest/cmip6search?mipEra=CMIP6&sourceId={}&granularity=model"
    REQUIRED_FIELDS = ["DOI", "LICENSE"]
    citation_data_cache_file = os.path.join(
        os.path.dirname(__file__), "citation.json.gz"
    )
    # Open cached data in case of api failure
    if os.path.exists(citation_data_cache_file):
        with gzip.open(citation_data_cache_file) as fh:
            cached_citation_data = json.load(fh)
    else:
        cached_citation_data = {}

    citation_data = defaultdict(lambda: defaultdict(dict))
    if regen:
        for source_id in source_ids:
            print("Retrieving data for {}".format(source_id))
            request_object = requests.get(CITATION_DATA_SOURCE.format(source_id))

            # If request successful
            if request_object.status_code == 200:
                citation_data_raw = request_object.json()
                if "error" in citation_data_raw:
                    raise RuntimeError(
                        "Received following from citation service: {}".format(
                            json.dumps(citation_data_raw)
                        )
                    )
                # pick out DOI from data reference and DRS id and build a dictionary

                for entry in citation_data_raw:
                    data_to_store = {i: entry[i] for i in REQUIRED_FIELDS}
                    data_to_store[
                        "SHORT_DATA_REFERENCE"
                    ] = "{SHORT_AUTHORS} ({PUBLICATION_YEAR}). {TITLE}. {PUBLISHER}. doi:{DOI}".format(
                        **entry
                    )
                    citation_data[source_id][entry["INSTITUTION_ID"]][
                        entry["ACTIVITY_ID"]
                    ] = data_to_store

            else:
                try:
                    citation_data[source_id] = cached_citation_data[source_id]
                except KeyError:
                    pass
        # write data to citation_data_cache_file
        with gzip.open(citation_data_cache_file, "w") as fh:
            # cludge to avoid issues with encoding
            fh.write(
                json.dumps(citation_data, indent=2, sort_keys=True).encode("utf-8")
            )
    else:
        citation_data = cached_citation_data

    return citation_data


def retrieve_citation_data_expts(source_ids, regen=False):
    """
    Retrieve citation information from either the citation service or
    a cached JSON file.

    Parameters
    ----------
    source_id
        List of source ids to check for
    regen
        If false return data from cached file, if false query citation service

    Returns a dictionary of the form {source_id: {DRS_ID: DOI_URL}}
    """
    CITATION_DATA_SOURCE = "https://www.wdc-climate.de/ui/cerarest/cmip6search?mipEra=CMIP6&sourceId={}&granularity=exp"
    REQUIRED_FIELDS = ["DOI", "LICENSE"]
    citation_data_cache_file = os.path.join(
        os.path.dirname(__file__), "citation_expts.json.gz"
    )
    # Open cached data in case of api failure
    if os.path.exists(citation_data_cache_file):
        with gzip.open(citation_data_cache_file) as fh:
            cached_citation_data = json.load(fh)
    else:
        cached_citation_data = {}

    citation_data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    if regen:
        for source_id in source_ids:
            print("Retrieving data for {}".format(source_id))
            request_object = requests.get(CITATION_DATA_SOURCE.format(source_id))

            # If request successful
            if request_object.status_code == 200:
                citation_data_raw = request_object.json()
                if "error" in citation_data_raw:
                    raise RuntimeError(
                        "Received following from citation service: {}".format(
                            json.dumps(citation_data_raw)
                        )
                    )
                # pick out DOI from data reference and DRS id and build a dictionary

                for entry in citation_data_raw:
                    data_to_store = {i: entry[i] for i in REQUIRED_FIELDS}
                    data_to_store[
                        "SHORT_DATA_REFERENCE"
                    ] = "{SHORT_AUTHORS} ({PUBLICATION_YEAR}). {TITLE} {EXPERIMENT_ID}. {PUBLISHER}. doi:{DOI}".format(
                        **entry
                    )

                    citation_data[source_id][entry["INSTITUTION_ID"]][
                        entry["ACTIVITY_ID"]
                    ][entry["EXPERIMENT_ID"]] = data_to_store

            else:
                try:
                    citation_data[source_id] = cached_citation_data[source_id]
                except KeyError:
                    pass
        # write data to citation_data_cache_file
        with gzip.open(citation_data_cache_file, "wb") as fh:
            fh.write(
                json.dumps(citation_data, indent=2, sort_keys=True).encode("utf-8")
            )
    else:
        citation_data = cached_citation_data

    return citation_data


# %% Create generic header
header = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<meta name="author" content="Paul J. Durack" />
<meta name="description" content="Controlled vocabulary for CMIP6" />
<meta name="keywords" content="HTML, CSS, JavaScript" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="stylesheet" type="text/css" charset="utf-8" href="https://pcmdi.github.io/assets/dataTables/jquery.dataTables.min.css" />
<script type="text/javascript" charset="utf-8" src="https://pcmdi.github.io/assets/jquery/jquery.slim.min.js"></script>
<script type="text/javascript" charset="utf-8" src="https://pcmdi.github.io/assets/dataTables/jquery.dataTables.min.js"></script>
<!-- Global site tag (gtag.js) - Google Analytics -->
<script type="text/javascript" src="https://pcmdi.github.io/assets/google/googleAnalyticsTag.js" ></script>
<script type="text/javascript">
//<![CDATA[
$(document).ready( function () {
    $('#table_id').DataTable();
    } );
//]]>
</script>\n"""

links_to_all = """
<h4>
<a href='CMIP6_experiment_id.html'>Experiment IDs</a> |
<a href='CMIP6_institution_id.html'>Institution IDs</a> |
<a href='CMIP6_source_id.html'>Source IDs</a> |
<a href='CMIP6_source_id_licenses.html'>Source IDs (incl licenses)</a> |
<a href='CMIP6_source_id_citation.html'>Citations by (Source ID, Institution Id, Activity ID)</a> |
<a href='CMIP6_source_id_experiment_citation.html'>Citations by (Source ID, Institution Id, Activity ID, Experiment ID)</a> |
</h4>
"""

# 190425 Updates below fail
# <script type="text/javascript">
# //<![CDATA[
# $(document).ready( function () {
#    $('#table_id').DataTable( {
#      "pageLength": 50,
#      "lengthMenu": [ [5,10,25,50,100,150,200,250,300,-1], [5,10,25,50,100,150,200,250,300,"All"] ]
#    } );
# //]]>
# </script>"""

# %% Argparse extract
# Matching version format 6.2.11.2
# verTest = re.compile(r'[6][.][2][.][0-9]+[.][0-9]+')
verTest = re.compile(r"[6][.][2][.][0-9]+[.][0-9]")
parser = argparse.ArgumentParser()
parser.add_argument(
    "ver",
    metavar="str",
    type=str,
    help="For e.g. '6.2.11.2' as a command line argument will ensure version information is written to the html output",
)
parser.add_argument(
    "-r",
    "--regen_citation",
    action="store_true",
    help="Regenerate citation information",
)
argDict = parser.parse_args()
if re.search(verTest, argDict.ver):
    version = argDict.ver  # 1 = make files
    print("** HTML Write mode - ", version, " will be written **")
else:
    print("** Version: ", version, " invalid, exiting")
    sys.exit()

# %% Set global arguments
destDir = "../docs/"

# %% Process experiment_id
infile = "../CMIP6_experiment_id.json"
f = open(infile)
exp_dict = json.load(f)
exp_dict1 = exp_dict.get("experiment_id")  # Fudge to extract duplicate level
exp_dict2 = exp_dict.get("version")
print(exp_dict2)
# print(dict.keys())
fout = "".join([destDir, infile[:-4].replace("../", ""), "html"])
print("processing", fout)
# fout = fout.split('/')[-1] ; # Write to local directory
fo = open(fout, "w")

# Old remote references
# <link rel="stylesheet" type="text/css" href="http://cdn.datatables.net/1.10.12/css/jquery.dataTables.css">
# <script type="text/javascript" src="http://code.jquery.com/jquery-1.12.4.js"></script>
# <script type="text/javascript" charset="utf8" src="http://rawgit.com/WCRP-CMIP/CMIP6_CVs/master/src/jquery.dataTables.js"></script>

fo.write(
    "".join(
        [
            header,
            "\n<title>CMIP6 experiment_id values</title>\n</head>\n<body>"
            "<p><h1>WCRP-CMIP CMIP6_CVs version: ",
            version,
            "</h1></p>",
            links_to_all,
            '<table id="table_id" class="display compact" style="width:100%">\n',
        ]
    )
)

dictOrder = [
    "experiment_id",
    "activity_id",
    "description",
    "start_year",
    "end_year",
    "parent_experiment_id",
    "parent_activity_id",
    "experiment",
    "additional_allowed_model_components",
    "required_model_components",
    "tier",
    "min_number_yrs_per_sim",
    "sub_experiment_id",
]
dictOrderK = [
    "activity_id",
    "experiment",
    "tier",
    "sub_experiment_id",
    "parent_experiment_id",
    "required_model_components",
    "additional_allowed_model_components",
    "start_year",
    "end_year",
    "min_number_yrs_per_sim",
    "parent_activity_id",
    "description",
]

first_row = False
for exp in exp_dict1.keys():
    exp_dict = exp_dict1[exp]
    if not first_row:
        # ids = exp_dict.keys()
        ids = dictOrderK  # Overwrite ordering
        for hf in ["thead", "tfoot"]:
            # print >> fo, "<%s><tr><th>experiment_id</th>" % hf
            fo.write("<%s>\n<tr>\n<th>experiment_id</th>\n" % hf)
            for i in ids:
                i = i.replace("_", " ")  # Remove '_' from table titles
                # print >>fo, "<th>%s</th>" % i
                fo.write("<th>%s</th>\n" % i)
            # print >> fo, "</tr></%s>" % hf
            fo.write("</tr>\n</%s>\n" % hf)
    first_row = True
    # print >> fo, "<tr><td>%s</td>" % exp
    fo.write("<tr><td>%s</td>\n" % exp)
    for k in ids:
        st = exp_dict[k]
        # print st
        if isinstance(st, (list, tuple)):
            st = " ".join(st)
        # print >> fo, "<td>%s</td>" % st
        fo.write("<td>%s</td>\n" % st)
    # print >> fo, "</tr>"
    fo.write("</tr>\n")
# print >> fo, "</table>"
fo.write("</table>")

# print >> fo, """
fo.write("""\n</body>\n</html>\n""")

# %% Process institution_id
infile = "../CMIP6_institution_id.json"
f = open(infile)
exp_dict = json.load(f)
exp_dict1 = exp_dict.get("institution_id")  # Fudge to extract duplicate level
exp_dict2 = exp_dict.get("version")
print(exp_dict2)
# print(dict.keys())
fout = "".join([destDir, infile[:-4].replace("../", ""), "html"])
print("processing", fout)
# fout = fout.split('/')[-1] ; # Write to local directory
fo = open(fout, "w")

# print >> fo, ''.join([header, """
fo.write(
    "".join(
        [
            header,
            "<title>CMIP6 institution_id values</title>\n</head>\n<body>",
            "<p><h1>WCRP-CMIP CMIP6_CVs version: ",
            version,
            "</h1></p>",
            links_to_all,
            '<table id="table_id" class="display compact" style="width:100%">\n',
        ]
    )
)

dictOrder = ["institution_id"]

first_row = False
for exp in exp_dict1.keys():
    exp_dict = exp_dict1[exp]
    if not first_row:
        ids = dictOrder  # Overwrite ordering
        for hf in ["thead", "tfoot"]:
            # print >> fo, "<%s><tr><th>institution_id</th>" % hf
            fo.write("<%s>\n<tr>\n<th>institution_id</th>\n" % hf)
            for i in ids:
                # print >>fo, "<th>Description</th>"
                fo.write("<th>Description</th>\n")
            # print >> fo, "</tr></%s>" % hf
            fo.write("</tr>\n</%s>\n" % hf)
    first_row = True
    # print >> fo, "<tr><td>%s</td>" % exp
    fo.write("<tr>\n<td>%s</td>\n" % exp)
    # print >> fo, "<td>%s</td>" % exp_dict
    fo.write("<td>%s</td>\n" % exp_dict)
    # print >> fo, "</tr>"
    fo.write("</tr>\n")
# print >> fo, "</table>"
fo.write("</table>")

# print >> fo, """
fo.write("""\n</body>\n</html>\n""")

# %% Process source_id
infile = "../CMIP6_source_id.json"
f = open(infile)
exp_dict = json.load(f)
exp_dict1 = exp_dict.get("source_id")  # Fudge to extract duplicate level
exp_dict2 = exp_dict.get("version")
print(exp_dict2)
# print(dict.keys())
fout = "".join([destDir, infile[:-4].replace("../", ""), "html"])
print("processing", fout)
# fout = fout.split('/')[-1] ; # Write to local directory
fo = open(fout, "w")

# print >> fo, ''.join([header, """
fo.write(
    "".join(
        [
            header,
            "<title>CMIP6 source_id values</title>\n</head>\n<body>",
            "<p><h1>WCRP-CMIP CMIP6_CVs version: ",
            version,
            "</h1></p>",
            links_to_all,
            '<table id="table_id" class="display compact" style="width:100%">\n',
        ]
    )
)

dictOrder = [
    "label_extended",
    "atmospheric_chemistry",
    "atmosphere",
    "ocean_biogeochemistry",
    "release_year",
    "cohort",
    "sea_ice",
    "label",
    "institution_id",
    "land_surface",
    "aerosol",
    "source_id",
    "ocean",
    "land_ice",
    "activity_participation",
    "native_nominal_resolution_atmos",
    "native_nominal_resolution_landIce",
    "native_nominal_resolution_ocean",
]
dictOrderKold = [
    "institution_id",
    "release_year",
    "activity_participation",
    "atmosphere",
    "nominal_resolution_atmos",
    "ocean",
    "nominal_resolution_ocean",
    "aerosol",
    "atmospheric_chemistry",
    "cohort",
    "label",
    "label_extended",
    "land_ice",
    "nominal_resolution_landIce",
    "land_surface",
    "ocean_biogeochemistry",
    "sea_ice",
]
dictOrderK = [
    "institution_id",
    "release_year",
    "activity_participation",
    "cohort",
    "label",
    "label_extended",
    "atmos",
    "natNomRes_atmos",
    "ocean",
    "natNomRes_ocean",
    "landIce",
    "natNomRes_landIce",
    "aerosol",
    "atmosChem",
    "land",
    "ocnBgchem",
    "seaIce",
]
dictRealmKeys = [
    "atmos",
    "ocean",
    "aerosol",
    "landIce",
    "atmosChem",
    "land",
    "ocnBgchem",
    "seaIce",
]
dictNomResKeys = ["natNomRes_atmos", "natNomRes_ocean", "natNomRes_landIce"]

first_row = False
for exp in exp_dict1.keys():
    exp_dict = exp_dict1[exp]
    # Create table columns
    if not first_row:
        ids = dictOrderK  # Overwrite ordering
        for hf in ["thead", "tfoot"]:
            # print >> fo, "<%s><tr><th>source_id</th>" % hf
            fo.write("<%s>\n<tr>\n<th>source_id</th>\n" % hf)
            for i in ids:
                i = i.replace("_", " ")  # Remove '_' from table titles
                # print >>fo, "<th>%s</th>" % i
                fo.write("<th>%s</th>\n" % i)
            # print >> fo, "</tr></%s>" % hf
            fo.write("</tr>\n</%s>\n" % hf)
    first_row = True
    # print >> fo, "<tr><td>%s</td>" % exp
    fo.write("<tr>\n<td>%s</td>\n" % exp)
    # Fill columns with values
    for k in ids:
        # Deal with embeds
        if k in dictRealmKeys:
            st = exp_dict["model_component"][k]["description"]
        elif k in dictNomResKeys:
            keyVal = k.replace("natNomRes_", "")
            st = exp_dict["model_component"][keyVal]["native_nominal_resolution"]
        else:
            st = exp_dict[k]
        if isinstance(st, (list, tuple)):
            st = " ".join(st)
        # print >> fo, "<td>%s</td>" % st
        fo.write("<td>%s</td>\n" % st)
    # print >> fo, "</tr>"
    fo.write("</tr>\n")
# print >> fo, "</table>"
fo.write("</table>")
# print >> fo, """
fo.write("""\n</body>\n</html>\n""")

# %% Process source_id licenses
infile = "../CMIP6_source_id.json"
with open(infile) as fh:
    source_id_json = json.load(fh)

source_id_table = source_id_json.get("source_id")
version_data = source_id_json.get("version")
print(version_data)
fout = os.path.join(destDir, "CMIP6_source_id_licenses.html")
print("processing", fout)

with open(fout, "w") as fh_license:
    fh_license.write(
        """{}
        <title>CMIP6 source_id license details</title>\n</head>\n<body>
        <p><h1>WCRP-CMIP CMIP6_CVs version: {}</h1></p>
        {}
        <table id="table_id" class="display compact" style="width:100%">\n
        """.format(
            header, version, links_to_all
        )
    )
    simple_headings = [
        "source_id",
        "institution_id",
        "release_year",
        "cohort",
        "label",
        "label_extended",
    ]
    license_headings = [
        "license",
        "exceptions_contact",
        "history",
        "source specific info",
    ]
    first_row = [i.replace("_", " ") for i in simple_headings + license_headings]
    # write header and footer rows for table
    for i in ["head", "foot"]:
        fh_license.write(
            "<t{}><tr>\n".format(i)
            + "\n".join(["<th>{}</th>".format(heading) for heading in first_row])
            + "\n</tr></t{}>\n".format(i)
        )

    for source_id, source_id_data in sorted(source_id_table.items()):
        row = []
        for heading in simple_headings:
            cell_data = source_id_data[heading]
            if isinstance(cell_data, list):
                cell_data = "<br>".join(cell_data)
            row.append(cell_data)
        # try to get license header, otherwise leave blanks
        try:
            license_data = source_id_data["license_info"]
            license1 = '<a href="{url}">{id}</a>'.format(**license_data)
            contact = license_data["exceptions_contact"]
            history = license_data["history"]
            specific_info = license_data["source_specific_info"]
            if specific_info.startswith("http"):
                specific_info = '<a href="{0}">{0}</a>'.format(specific_info)
            row += [license1, contact, history, specific_info]

        except KeyError:
            row += [""] * len(license_headings)

        citation_entry = []
        mips = source_id_data["activity_participation"]
        institutions = source_id_data["institution_id"]

        fh_license.write(
            "<tr>\n" + "\n".join(["<td>{}</td>".format(i) for i in row]) + "\n</tr>\n"
        )

    fh_license.write("</table>\n</body>\n</html>\n")

# %% Process source_id citation
html_file = "CMIP6_source_id_citation.html"
heading = "CMIP6 Source ID Citation details"
first_row = [
    "Source ID",
    "Institution ID",
    "Activity ID",
    "Data Reference",
    "License",
    "DOI",
]
column_styles = {
    "Data Reference": 'style="max-width: 40%;"',
    "Source ID": 'style="min-width: 100px;"',
}
# Load citation_data
citation_data = retrieve_citation_data_models(
    list(source_id_table.keys()), regen=argDict.regen_citation
)

fout = os.path.join(destDir, html_file)
print("processing", fout)

with open(fout, "w", encoding="utf-8") as fh_citation:
    fh_citation.write(
        """{}
        <title>{} details</title>\n</head>\n<body>
        <p><h1>WCRP-CMIP CMIP6_CVs version: {}</h1></p>
        {}
        <table id="table_id" class="display compact" style="width:100%">\n
        """.format(
            header, heading, version, links_to_all
        )
    )
    # write header and footer rows for table
    for i in ["head", "foot"]:
        fh_citation.write(
            "<t{}><tr>\n".format(i)
            + "\n".join(
                [
                    "<th {} >{}</th>".format(column_styles.get(heading), heading)
                    for heading in first_row
                ]
            )
            + "\n</tr></t{}>\n".format(i)
        )

    for source_id, source_id_entry in sorted(citation_data.items()):
        for institution_id, institution_id_entry in sorted(source_id_entry.items()):
            for activity_id, entry in sorted(institution_id_entry.items()):
                row = [source_id, institution_id, activity_id]
                row += [entry["SHORT_DATA_REFERENCE"], entry["LICENSE"]]
                row += ['<a href="{0}">{0}</a>'.format(entry["DOI"])]

                fh_citation.write(
                    "<tr>\n"
                    + "\n".join(["<td>{}</td>".format(i) for i in row])
                    + "\n</tr>\n"
                )

    fh_citation.write("</table>\n</body>\n</html>\n")

# %% Process source_id per experiment citation
html_file = "CMIP6_source_id_experiment_citation.html"
heading = "CMIP6 Source ID Citation details by experiment"
first_row = [
    "Source ID",
    "Institution ID",
    "Activity ID",
    "Experiment",
    "Data Reference",
    "License",
    "DOI",
]
column_styles = {
    "Data Reference": 'style="max-width: 40%;"',
    "Source ID": 'style="min-width: 100px;"',
}
# Load citation_data
citation_data = retrieve_citation_data_expts(
    list(source_id_table.keys()), regen=argDict.regen_citation
)

fout = os.path.join(destDir, html_file)
print("processing", fout)

with open(fout, "w", encoding="utf-8") as fh_citation:
    fh_citation.write(
        """{}
        <title>{} details</title>\n</head>\n<body>
        <p><h1>WCRP-CMIP CMIP6_CVs version: {}</h1></p>
        {}
        <table id="table_id" class="display compact" style="width:100%">\n
        """.format(
            header, heading, version, links_to_all
        )
    )
    # write header and footer rows for table
    for i in ["head", "foot"]:
        fh_citation.write(
            "<t{}><tr>\n".format(i)
            + "\n".join(
                [
                    "<th {}>{}</th>".format(column_styles.get(heading), heading)
                    for heading in first_row
                ]
            )
            + "\n</tr></t{}>\n".format(i)
        )

    for source_id, source_id_entry in sorted(citation_data.items()):
        for institution_id, institution_id_entry in sorted(source_id_entry.items()):
            for activity_id, activity_entry in sorted(institution_id_entry.items()):
                for experiment_id, entry in sorted(activity_entry.items()):
                    row = [source_id, institution_id, activity_id, experiment_id]
                    row += [entry["SHORT_DATA_REFERENCE"], entry["LICENSE"]]
                    row += ['<a href="{0}">{0}</a>'.format(entry["DOI"])]

                    fh_citation.write(
                        "<tr>\n"
                        + "\n".join(["<td>{}</td>".format(i) for i in row])
                        + "\n</tr>\n"
                    )

    fh_citation.write("</table>\n</body>\n</html>\n")
