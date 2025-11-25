import json
from pathlib import Path


def read(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)