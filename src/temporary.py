from denver import load_json, save_json, remove_json_files, list_json_files
from esgvoc.core.db.models.universe import sa



files = list_json_files("./table_id")
for f in files: 
    dico = {
    "@context": "000_context.jsonld",
    "id": f.split(".")[0],
    "type": "table",
    "product": "model-output",
    "table_date": "2023-11-16",
    "variable_entry": [
           ],
    "drs_name": f.split(".")[0]
    }
    save_json(f"./table_id_universe/{f}",dico)



