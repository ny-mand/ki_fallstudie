#Dieser code wurde mit Hilfe von KI erzeugt
from src.projekt import Project
import pytest
from unittest.mock import patch
def test_project_erstellung():
    test_project = Project(5,"KI Fallstudie", "Gruppenprojekt", "2025-11-20", "2025-12-01", "niedrig" )

    assert test_project.name == "KI Fallstudie"
    assert test_project.description == "Gruppenprojekt"
    assert test_project.date_start == "2025-11-20"
    assert test_project.date_due == "2025-12-01"
    assert test_project.priority == "niedrig"





# --- Fixture für Testdaten ---
@pytest.fixture
def mock_project_data():
    return [
        {
            "project_id": 1,
            "name": "Altes Projekt",
            "description": "Beschreibung",
            "date_start": "2024-01-01",
            "date_due": "2024-12-31",
            "priority": "hoch",
            "working_by_person": {
                "Alice": ["Task1"],
                "Bob": ["Task2", "Task1"],
                "Charlie": []
            },
            "working_by_task": {
                "Task1": ["Alice", "Bob"],
                "Task2": ["Bob"]
            }
        }
    ]


# --- Bestehende Tests ---

@patch('src.projekt.read')
def test_project_exists(mock_read, mock_project_data):
    mock_read.return_value = mock_project_data
    assert Project.project_exists("Altes Projekt") is True
    assert Project.project_exists("Unbekanntes Projekt") is False


@patch('src.projekt.write') # simuliert/mockt einen write (speicherfunktion) ohne eine echte datei
@patch('src.projekt.read') # simuliert/mockt das lesen einer datei (ohne einer echten datei)
@patch('src.projekt.get_non_empty_input') # simuliert/mockt inputs (automatische Antworten)
@patch('src.projekt.validate_date_format') # mockt datumsvalidierung (macht test einfacher)
def test_create_project(mock_validate, mock_get_input, mock_read, mock_write, mock_project_data):
    mock_read.return_value = mock_project_data #Wenn read aufgerufen wird gibt er Testdaten wider welche vorher erstellt wurden (keine datei wird gelesen)
    mock_validate.return_value = True #Wenn Datumsvalidierung aufgerufen wird, gibt er immer true zurück

    mock_get_input.side_effect = [ #Simulation des Inputs
        "Neues Projekt",
        "Eine Beschreibung",
        "2025-01-01",
        "2025-06-30",
        "2"
    ]

    Project.create_project() #Wahre create_project Funktion wird aufgerufen mit den Inputwerten

    mock_write.assert_called_once() #Überprüft ob write aufgerufen wurde
    saved_data = mock_write.call_args[0][1] # speichert die Daten welche er speichern wollte (aber durch die mocks nicht getan hat) unter saved_date
    new_project = saved_data[-1] #speichert aus den Daten den letzten Wert (unser neues Projekt) unter new_project
    assert new_project['name'] == "Neues Projekt" #prüft ob unser neues Projekt korrekt übernommen wurde
    assert new_project['project_id'] == 2 #prüft ob die ID korrekt ist


@patch('src.projekt.write')
@patch('src.projekt.read')
@patch('src.projekt.Project.validate_existence')
@patch('builtins.input')
@patch('src.projekt.get_non_empty_input')
def test_assign_member_to_project(mock_get_input, mock_input, mock_validate, mock_read, mock_write, mock_project_data):
    mock_read.return_value = mock_project_data
    mock_validate.return_value = True

    mock_input.return_value = "j"
    mock_get_input.return_value = "Task3"

    Project.assign_member_to_project("Altes Projekt", "Dave")

    mock_write.assert_called_once()
    updated_project = mock_write.call_args[0][1][0]

    assert "Dave" in updated_project['working_by_person']
    assert updated_project['working_by_person']["Dave"] == ["Task3"]
    assert "Task3" in updated_project['working_by_task']
    assert "Dave" in updated_project['working_by_task']["Task3"]


# --- NEUE TESTS für remove_member und remove_task ---

@patch('src.projekt.write')
@patch('src.projekt.read')
@patch('src.projekt.Project.project_exists')
@patch('src.projekt.TeamMember.member_exists')
def test_remove_member_from_project(mock_member_exists, mock_proj_exists, mock_read, mock_write, mock_project_data):
    mock_read.return_value = mock_project_data
    mock_proj_exists.return_value = True
    mock_member_exists.return_value = True

    result = Project.remove_member_from_project("Altes Projekt", "Bob")

    assert result is True
    mock_write.assert_called_once()

    updated_project = mock_write.call_args[0][1][0]
    assert "Bob" not in updated_project['working_by_person']
    assert "Bob" not in updated_project['working_by_task']['Task1']
    assert "Task2" not in updated_project['working_by_task']
    assert "Alice" in updated_project['working_by_task']['Task1']


@patch('src.projekt.write')
@patch('src.projekt.read')
@patch('src.projekt.Project.project_exists')
def test_remove_task_from_member(mock_proj_exists, mock_read, mock_write, mock_project_data):
    mock_read.return_value = mock_project_data
    mock_proj_exists.return_value = True

    result = Project.remove_task_from_member("Altes Projekt", "Bob", "Task1")

    assert result is True
    mock_write.assert_called_once()

    updated_project = mock_write.call_args[0][1][0]
    bobs_tasks = updated_project['working_by_person']['Bob']
    assert "Task1" not in bobs_tasks
    assert "Task2" in bobs_tasks

    task1_members = updated_project['working_by_task']['Task1']
    assert "Bob" not in task1_members
    assert "Alice" in task1_members


@patch('src.projekt.write')
@patch('src.projekt.read')
@patch('src.projekt.Project.project_exists')
def test_remove_last_task_removes_member(mock_proj_exists, mock_read, mock_write, mock_project_data):
    mock_read.return_value = mock_project_data
    mock_proj_exists.return_value = True

    Project.remove_task_from_member("Altes Projekt", "Alice", "Task1")

    updated_project = mock_write.call_args[0][1][0]
    assert "Alice" not in updated_project['working_by_person']


@patch('src.projekt.read')
@patch('src.projekt.Project.project_exists')
@patch('builtins.print')
def test_remove_member_not_in_project(mock_print, mock_proj_exists, mock_read, mock_project_data):
    mock_read.return_value = mock_project_data
    mock_proj_exists.return_value = True

    with patch('src.projekt.TeamMember.member_exists', return_value=True):
        result = Project.remove_member_from_project("Altes Projekt", "Zorro")

        assert result is False
        mock_print.assert_called_with("'Zorro' ist nicht Teil des Projekts 'Altes Projekt'.")
