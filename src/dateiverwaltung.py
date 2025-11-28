import json
from pathlib import Path #wichtig für Nutzung in anderen Modulen

def read(file_path):
    try:
        with open(file_path, 'r') as file: #JSON-Datei öffnen zum Lesen
            return json.load(file)
    except FileNotFoundError: #falls Datei nicht existiert leere Liste zurückgeben, um Programmabbruch zu vermeiden
        return []
    except json.JSONDecodeError:
        print(f"Warnung: Datei ist beschädigt, ungültig oder leer.")
        return []

def write(file_path, data):
    try:
        with open(file_path, 'w') as file: #JSON-Datei öffnen zum Schreiben
            json.dump(data, file, indent=2)
    except FileNotFoundError:
        print(f"Fehler: Datei {file_path} nicht gefunden.\nAktion konnte nicht ausgeführt werden.")
        return