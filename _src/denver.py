import os
import glob
import json

def yield_json_files(directory):
    """
    Yields each JSON file from the specified directory.

    :param directory: Path to the directory to search for JSON files.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"{directory} is not a valid directory")

    # Use glob to find all *.json files in the directory
    for file_path in glob.iglob(os.path.join(directory, "*.json")):
        yield file_path

def load_json(file_path):
    """
    Loads and returns the content of a JSON file.

    :param file_path: Path to the JSON file.
    :return: Parsed content of the JSON file.
    """
    if not os.path.isfile(file_path):
        raise ValueError(f"{file_path} is not a valid file")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON from {file_path}: {e}")

def save_json(file_path, data):
    """
    Saves a dictionary to a JSON file.

    :param file_path: Path to the JSON file to save.
    :param data: Dictionary to save as JSON.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        raise ValueError(f"Failed to save JSON to {file_path}: {e}")


def remove_json_files(directory):
    """
    Remove all JSON files from the specified directory.

    Parameters:
        directory (str): The path to the directory where JSON files should be removed.

    Returns:
        None
    """
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        return

    try:
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                file_path = os.path.join(directory, filename)
                os.remove(file_path)
        print("All JSON files have been removed.")
    except Exception as e:
        print(f"An error occurred: {e}")

def list_json_files(directory):
    """
    List all JSON files in the specified directory.

    Parameters:
        directory (str): The path to the directory to search for JSON files.

    Returns:
        list: A list of JSON file names in the directory.
    """
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        return []

    try:
        json_files = [file for file in os.listdir(directory) if file.endswith('.json')]
        return json_files
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
