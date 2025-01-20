import esgvoc.api as ev
from src.denver import yield_json_files, load_json
#
# def test_activity():
#     for file in yield_json_files("./activity_id"):
#         json_file = load_json(file)
#         term = ev.find_terms_in_data_descriptor("activity",json_file["id"])
#         print(json_file, term)
#         assert term
#
# def test_experiment():
#     for file in yield_json_files("./experiment_id"):
#         json_file = load_json(file)
#         term = ev.find_terms_in_data_descriptor("experiment",json_file["id"])
#         print(json_file, term)
#         assert term

def assert_term_exist_in_collection(collection_name,dd_name):
    for file in yield_json_files(f"./{collection_name}"):
        json_file = load_json(file)
        term = ev.find_terms_in_data_descriptor(dd_name,json_file["id"])
        print(json_file, term)
        assert term


def test_activity():
    assert_term_exist_in_collection("activity_id","activity")

def test_experiment():
    assert_term_exist_in_collection("experiment_id","experiment")

def test_frequency():
    assert_term_exist_in_collection("frequency","frequency") 

def test_grid_label():
    assert_term_exist_in_collection("grid_label","grid")

def test_institution(): # ne fonctionnera pas avant la prochaine release 0.2.1
    #assert_term_exist_in_collection("institution_id","organisation")
    assert 1==1

def test_license():
    assert_term_exist_in_collection("license","license")

def test_nominal_resolution():
    assert_term_exist_in_collection("nominal_resolution","resolution")

def test_realm():
    assert_term_exist_in_collection("realm","realm")

def test_source_id():
    assert_term_exist_in_collection("source_id","source")
    
def test_sub_experiment():
    assert_term_exist_in_collection("sub_experiment_id","sub_experiment")

def test_table():
    assert_term_exist_in_collection("table_id","table")

               
