#Dieser code wurde mit Hilfe von KI erzeugt
import pytest
from unittest.mock import patch
from src.teammitglied import TeamMember


# 1. Testdaten vorbereiten (Fixture)
# Das stellt sicher, dass jeder Test saubere Daten bekommt
@pytest.fixture
def mock_member_data():
    return [
        {
            "member_id": 1,
            "name": "Alice",
            "job_title": "Developer",
            "active_since": "2020-01-01"
        },
        {
            "member_id": 2,
            "name": "Bob",
            "job_title": "Designer",
            "active_since": "2021-03-15"
        }
    ]


# 2. Test für member_exists
# Wir mocken 'read', damit keine echte Datei geöffnet wird
@patch('src.teammitglied.read')
def test_member_exists(mock_read, mock_member_data):
    mock_read.return_value = mock_member_data

    # Positiv-Tests
    assert TeamMember.member_exists("Alice") is True
    assert TeamMember.member_exists("alice") is True  # Case-insensitive

    # Negativ-Test
    assert TeamMember.member_exists("Charlie") is False


# 3. Test für add_member (Erfolgsfall)
@patch('src.teammitglied.write')
@patch('src.teammitglied.read')
@patch('src.teammitglied.get_non_empty_input')
@patch('src.teammitglied.validate_date_format')
@patch('builtins.input')
def test_add_member_success(mock_input, mock_validate, mock_get_input, mock_read, mock_write, mock_member_data):
    # Mock-Setup
    mock_read.return_value = mock_member_data
    mock_validate.return_value = True

    # Eingaben simulieren:
    # 1. Name: "Charlie"
    # 2. Job: "Tester"
    mock_get_input.side_effect = ["Charlie", "Tester"]

    # Datumseingabe (optional): "2023-01-01"
    mock_input.return_value = "2023-01-01"

    # Funktion ausführen
    TeamMember.add_member()

    # Prüfungen (Assertions)
    mock_write.assert_called_once()  # Wurde gespeichert?

    # Was wurde genau gespeichert?
    saved_data = mock_write.call_args[0][1]
    new_member = saved_data[-1]

    assert new_member['name'] == "Charlie"
    assert new_member['job_title'] == "Tester"
    assert new_member['member_id'] == 3  # Automatische ID-Erhöhung (2+1)
    assert new_member['active_since'] == "2023-01-01"


# 4. Test für add_member (Duplikat-Fall)
@patch('src.teammitglied.write')
@patch('src.teammitglied.read')
@patch('src.teammitglied.get_non_empty_input')
def test_add_member_duplicate(mock_get_input, mock_read, mock_write, mock_member_data):
    mock_read.return_value = mock_member_data

    # Benutzer gibt einen Namen ein, den es schon gibt ("Alice")
    mock_get_input.return_value = "Alice"

    TeamMember.add_member()

    mock_write.assert_not_called()



