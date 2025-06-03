import os

from denver import load_json, remove_json_files, save_json


def create_collection(cmip6_collection_name, universe_dd_name, lower=True):
    os.makedirs(f"./{cmip6_collection_name}", exist_ok=True)
    remove_json_files(f"./{cmip6_collection_name}")
    json_dic = load_json(f"./_archive/CMIP6_{cmip6_collection_name}.json")
    items_dic = json_dic[cmip6_collection_name]
    # SPECIFICS ISSUES that need to be address
    if cmip6_collection_name == "license":
        # in license a dico level added ? for what reason ?
        items_dic = json_dic["license"]["license_options"]

    for k, _ in items_dic.items():
        id = k.lower().replace(" ", "_") if lower else k
        dico = {"@context": "000_context.jsonld", "id": id, "type": universe_dd_name}
        save_json(f"./{cmip6_collection_name}/{id}.json", dico)
    print(f"All JSON files have been created in ./{cmip6_collection_name}")


def create_collection_from_list(cmip6_collection_name, universe_dd_name, lower=True):
    os.makedirs(f"./{cmip6_collection_name}", exist_ok=True)
    remove_json_files(f"./{cmip6_collection_name}")
    json_dic = load_json(f"./_archive/CMIP6_{cmip6_collection_name}.json")
    items_list = json_dic[cmip6_collection_name]
    for k in items_list:
        id = k.lower().replace(" ", "") if lower else k
        dico = {"@context": "000_context.jsonld", "id": id, "type": universe_dd_name}
        save_json(f"./{cmip6_collection_name}/{id}.json", dico)
    print(f"All JSON files have been created in ./{cmip6_collection_name}")


def main():
    create_collection("activity_id", "activity")
    create_collection("experiment_id", "experiment")
    create_collection(
        "frequency", "frequency", False
    )  # ids in universe are not lowered
    create_collection("grid_label", "grid")
    create_collection("institution_id", "organisation")
    create_collection("license", "license")
    create_collection_from_list("nominal_resolution", "resolution")
    create_collection("realm", "realm", False)
    create_collection("source_id", "source")
    create_collection_from_list("sub_experiment_id", "sub_experiment")
    create_collection_from_list("table_id", "table", False)


if __name__ == "__main__":
    # create_activity()
    # create_experiment()
    # main()
    create_collection_from_list("source_type", "source_type")
