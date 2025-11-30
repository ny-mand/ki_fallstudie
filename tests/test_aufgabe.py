#Dieser code wurde mit Hilfe von KI erzeugt
import pytest
from unittest.mock import patch
from src.aufgabe import Task


# Fixture für wiederkehrende Testdaten (Task-Datenstruktur)
@pytest.fixture
def mock_task_data():
    return [
        {
            "task_id": 1,
            "name": "Alte Aufgabe",
            "description": "Beschreibung",
            "priority": "hoch",
            "date_due": "2024-12-31",
            "date_created": "2024-01-01"
        }
    ]


# Test für task_exists (statische Methode)
@patch('src.aufgabe.read')
def test_task_exists(mock_read, mock_task_data):
    mock_read.return_value = mock_task_data

    # Teste existierende Aufgabe (case-insensitive)
    assert Task.task_exists("Alte Aufgabe") is True
    assert Task.task_exists("alte aufgabe") is True

    # Teste nicht existierende Aufgabe
    assert Task.task_exists("Neue Aufgabe") is False

    # Teste None-Input (Sicherheitscheck)
    assert Task.task_exists(None) is False


# Test für create_task (simuliert kompletten User-Dialog)
@patch('src.aufgabe.write')
@patch('src.aufgabe.read')
@patch('src.aufgabe.get_non_empty_input')
@patch('src.aufgabe.validate_date_format')
def test_create_task(mock_validate, mock_get_input, mock_read, mock_write, mock_task_data):
    # Setup
    mock_read.return_value = mock_task_data
    mock_validate.return_value = True  # Wir nehmen an, das Datum ist gültig

    # Szenario: Benutzer gibt gültige Daten für eine neue Aufgabe ein
    # Reihenfolge der Inputs: Name, Beschreibung, Priorität, Fälligkeitsdatum
    mock_get_input.side_effect = [
        "Neue Aufgabe",  # Name
        "Wichtige Deadline",  # Beschreibung
        "3",  # Priorität (hoch)
        "2025-12-24"  # Fälligkeitsdatum
    ]

    # Ausführen
    Task.create_task()

    # Überprüfungen
    mock_write.assert_called_once()

    # Wir holen uns die Daten, die an write übergeben wurden
    # call_args[0][1] greift auf das zweite Argument (die Datenliste) zu
    saved_data = mock_write.call_args[0][1]
    new_task = saved_data[-1]  # Das letzte Element ist das neue

    # Detaillierte Checks
    assert new_task['name'] == "Neue Aufgabe"
    assert new_task['description'] == "Wichtige Deadline"
    assert new_task['priority'] == "hoch"  # "3" wurde zu "hoch" konvertiert
    assert new_task['date_due'] == "2025-12-24"
    assert new_task['task_id'] == 2  # ID sollte hochgezählt sein (1 + 1)

    # Prüfen, ob ein Erstellungsdatum automatisch gesetzt wurde
    assert 'date_created' in new_task
    assert isinstance(new_task['date_created'], str)


# Test für Fehlerfall: Aufgabe existiert bereits
@patch('src.aufgabe.write')
@patch('src.aufgabe.read')
@patch('src.aufgabe.get_non_empty_input')
def test_create_task_duplicate(mock_get_input, mock_read, mock_write, mock_task_data):
    mock_read.return_value = mock_task_data

    # Benutzer versucht, eine bereits existierende Aufgabe zu erstellen
    mock_get_input.return_value = "Alte Aufgabe"

    Task.create_task()

    # Es darf NICHT gespeichert werden
    mock_write.assert_not_called()
