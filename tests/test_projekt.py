#Dieser code wurde mit Hilfe von KI erzeugt
import pytest
from unittest.mock import patch
from src.projekt import Project


def test_project_erstellung():
    test_project = Project(5, "KI Fallstudie", "Gruppenprojekt", "2025-11-20", "2025-12-01", "niedrig")

    assert test_project.project_id == 5
    assert test_project.name == "KI Fallstudie"
    assert test_project.description == "Gruppenprojekt"
    assert test_project.date_start == "2025-11-20"
    assert test_project.date_due == "2025-12-01"
    assert test_project.priority == "niedrig"
    assert test_project.working_by_person == {}
    assert test_project.working_by_task == {}


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


@patch("src.projekt.read")
def test_project_exists(mock_read, mock_project_data):
    mock_read.return_value = mock_project_data

    assert Project.project_exists("Altes Projekt") is True
    assert Project.project_exists("altes projekt") is True
    assert Project.project_exists("Unbekanntes Projekt") is False


@patch("src.projekt.write")
@patch("src.projekt.read")
@patch("src.projekt.validate_date_format")
def test_create_project_success(mock_validate, mock_read, mock_write, mock_project_data):
    mock_read.return_value = mock_project_data
    mock_validate.return_value = True

    result = Project.create_project(
        "Neues Projekt",
        "Eine Beschreibung",
        "2025-01-01",
        "2025-06-30",
        "2"
    )

    assert result == "Neues Projekt"
    mock_write.assert_called_once()

    saved_data = mock_write.call_args[0][1]
    new_project = saved_data[-1]

    assert new_project["name"] == "Neues Projekt"
    assert new_project["description"] == "Eine Beschreibung"
    assert new_project["project_id"] == 2
    assert new_project["date_start"] == "2025-01-01"
    assert new_project["date_due"] == "2025-06-30"
    assert new_project["priority"] == "mittel"
    assert new_project["working_by_person"] == {}
    assert new_project["working_by_task"] == {}


@patch("src.projekt.write")
@patch("src.projekt.read")
def test_create_project_duplicate(mock_read, mock_write, mock_project_data):
    mock_read.return_value = mock_project_data

    result = Project.create_project(
        "Altes Projekt",
        "Andere Beschreibung",
        "2025-01-01",
        "2025-06-30",
        "1"
    )

    assert result is None
    mock_write.assert_not_called()


@patch("src.projekt.write")
@patch("src.projekt.read")
@patch("src.projekt.Project.validate_existence")
def test_assign_member_to_project_without_task(mock_validate, mock_read, mock_write, mock_project_data):
    mock_read.return_value = mock_project_data
    mock_validate.return_value = True

    Project.assign_member_to_project("Altes Projekt", "Dave")

    mock_write.assert_called_once()
    updated_project = mock_write.call_args[0][1][0]

    assert "Dave" in updated_project["working_by_person"]
    assert updated_project["working_by_person"]["Dave"] == {}
