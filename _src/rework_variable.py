import json
import os
from pathlib import Path

import esgvoc.api as ev
import requests

# Directory of CMOR Table to retrieve variable_id
table_dir_url = "https://api.github.com/repos/PCMDI/cmip6-cmor-tables/contents/Tables"

# Directory where the JSON files will be saved
save_dir = "variable_id"

# Create the directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)


# Function to fetch and load JSON data from a URL
def fetch_json(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    return response.json()


variables_list = []
data = fetch_json(table_dir_url)
for item in data:
    json_data = fetch_json(item["download_url"])
    print(item["name"])
    # print(json_data.keys())
    if "variable_entry" in json_data.keys():
        variables_list.append(list(json_data["variable_entry"].keys()))
        # print(json_data["variable_entry"].keys())
    else:
        if "variable_entry" in json_data[list(json_data.keys())[0]]:
            # print(json_data[list(json_data.keys())[0]]["variable_entry"].keys())

            variables_list.append(
                list(json_data[list(json_data.keys())[0]]["variable_entry"].keys())
            )


def flatten(xss):
    return [x for xs in xss for x in xs]


def remove_duplicate(ll):
    return list(set(ll))


variables_list_flat = remove_duplicate(flatten(variables_list[:-1]))
print(variables_list_flat)


known_variables_in_universe = ev.get_all_terms_in_data_descriptor("variable")
for item in variables_list_flat:
    found_item = None
    for sour in known_variables_in_universe:
        if sour.drs_name == item:
            found_item = sour
            break

    if found_item is None:
        print(
            item, "NOT found in universe"
        )  # No more ! if there is, need to add them in the Universe first
    else:
        # Create json file
        dict_to_save = {
            "@context": "000_context.jsonld",
            "id": found_item.id,
            "type": found_item.type,
        }
        print(dict_to_save)
        with open(Path(save_dir) / f"{found_item.id}.json", "w") as f:
            json.dump(dict_to_save, f, indent=4)
