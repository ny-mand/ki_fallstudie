#Dieser code wurde mit Hilfe von KI erzeugt
import pytest
from unittest.mock import patch


from src.filter import filter_projects


# --- Testdaten Fixture ---
@pytest.fixture
def mock_projects():
    return [
        {
            "project_id": 1,
            "name": "Projekt A",
            "priority": "hoch",
            "date_start": "2024-01-01",
            "date_due": "2024-12-31",
            "description": "Wichtiges Projekt"
        },
        {
            "project_id": 2,
            "name": "Projekt B",
            "priority": "niedrig",
            "date_start": "2023-05-01",
            "date_due": "2023-10-01",
            "description": "Nebenprojekt"
        },
        {
            "project_id": 3,
            "name": "Projekt C",
            "priority": "mittel",
            "date_start": "2024-06-01",
            "date_due": "2024-08-01",
            "description": "Mittelwichtig"
        }
    ]


# --- Test 1: Filter nach Priorität (Option 1) ---
@patch('src.filter.read')
@patch('src.filter.get_non_empty_input')
@patch('builtins.print')
def test_filter_priority_hoch(mock_print, mock_get_input, mock_read, mock_projects):
    mock_read.return_value = mock_projects

    # Eingabe: "1" (Menü: Priorität), dann "3" (Priorität: hoch)
    mock_get_input.side_effect = ["1", "3"]

    filter_projects()

    # Wir prüfen, ob die Erfolgsmeldung "1 Projekte gefunden" gedruckt wurde
    # und ob der Name "Projekt A" (das einzige hohe) gedruckt wurde

    # Alle gedruckten Strings sammeln
    printed_text = " ".join([str(c[0][0]) for c in mock_print.call_args_list])

    assert "1 Projekte gefunden" in printed_text
    assert "Projekt A" in printed_text
    assert "Projekt B" not in printed_text  # Niedrig darf nicht dabei sein


# --- Test 2: Filter nach Startdatum (Option 2) ---
@patch('src.filter.read')
@patch('src.filter.get_non_empty_input')
@patch('src.filter.validate_date_format')  # Wichtig: Validierung mocken!
@patch('builtins.print')
def test_filter_start_date(mock_print, mock_validate, mock_get_input, mock_read, mock_projects):
    mock_read.return_value = mock_projects
    mock_validate.return_value = True

    # Eingabe: "2" (Menü: Datum), dann "2024-01-01"
    # Filterlogik ist: date_start >= target_date
    # Projekt A (2024-01-01) -> Treffer
    # Projekt B (2023-05-01) -> Kein Treffer (zu alt)
    # Projekt C (2024-06-01) -> Treffer
    mock_get_input.side_effect = ["2", "2024-01-01"]

    filter_projects()

    printed_text = " ".join([str(c[0][0]) for c in mock_print.call_args_list])

    assert "2 Projekte gefunden" in printed_text
    assert "Projekt A" in printed_text
    assert "Projekt C" in printed_text
    assert "Projekt B" not in printed_text


# --- Test 3: Sortieren nach Fälligkeitsdatum (Option 3) ---
@patch('src.filter.read')
@patch('src.filter.get_non_empty_input')
@patch('builtins.print')
def test_sort_due_date(mock_print, mock_get_input, mock_read, mock_projects):
    mock_read.return_value = mock_projects

    # Eingabe: "3" (Sortieren nach Due Date)
    mock_get_input.side_effect = ["3"]

    filter_projects()


    printed_text = " "
