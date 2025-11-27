import json
from pathlib import Path #wichtig für Nutzung in anderen Modulen

def read(file_path):
    try:
        with open(file_path, 'r') as file: #JSON-Datei öffnen zum Lesen
            return json.load(file)
    except FileNotFoundError: #falls Datei nicht existiert leere Liste zurückgeben, um Programmabbruch zu vermeiden
        return []

def write(file_path, data):
    with open(file_path, 'w') as file: #JSON-Datei öffnen zum Schreiben
        json.dump(data, file, indent=2)