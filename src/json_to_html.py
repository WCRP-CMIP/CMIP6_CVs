# This script takes the json file and turns it into a nice
# jquery/data-tabled html doc
import json
import sys

f = open(sys.argv[1])
dic = json.load(f)

#print dic

if len(sys.argv) > 2:
    fout = sys.argv[2]
else:
    fout = sys.argv[1][:-4] + "html"
fo = open(fout, "w")

print >> fo, """<html><head>
<link rel="stylesheet" type="text/css" href="http://cdn.datatables.net/1.10.12/css/jquery.dataTables.css">
<script type="text/javascript" src="https://code.jquery.com/jquery-1.12.4.js"></script>
<script type="text/javascript" charset="utf8" src="http://cdn.datatables.net/1.10.12/js/jquery.dataTables.js"></script>
<script>
$(document).ready( function () {
    $('#table_id').DataTable();
    } );
</script>
</head><body>
<table id="table_id" class="display">"""

first_row = False
for exp in dic.keys():
    exp_dict = dic[exp]
    if not first_row:
        ids = exp_dict.keys()
        for hf in ["thead", "tfoot"]:
            print >> fo, "<%s><tr><th>experiment id</th>" % hf
            for i in ids:
                print >>fo, "<th>%s</th>" % i
            print >>fo, "</tr></%s>" % hf
    first_row = True
    print >> fo, "<tr><td>%s</td>" % exp
    for k in ids:
        st = exp_dict[k]
        if isinstance(st, (list, tuple)):
            st = " ".join(st)
        print >>fo, "<td>%s</td>" % st
    print >>fo, "</tr>"
print >>fo, "</table>"

print >>fo, """
</body></html>
"""
