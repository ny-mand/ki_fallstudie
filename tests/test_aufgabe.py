#Dieser code wurde mit Hilfe von KI erzeugt
import pytest
from unittest.mock import patch
from src.aufgabe import Task


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


@patch("src.aufgabe.read")
def test_task_exists(mock_read, mock_task_data):
    mock_read.return_value = mock_task_data

    assert Task.task_exists("Alte Aufgabe") is True
    assert Task.task_exists("alte aufgabe") is True
    assert Task.task_exists("Neue Aufgabe") is False
    assert Task.task_exists(None) is False


@patch("src.aufgabe.write")
@patch("src.aufgabe.read")
@patch("src.aufgabe.validate_date_format")
def test_create_task_success(mock_validate, mock_read, mock_write, mock_task_data):
    mock_read.return_value = mock_task_data
    mock_validate.return_value = True

    Task.create_task("Neue Aufgabe", "Wichtige Deadline", "3", "2025-12-24", "2025-01-01")

    mock_write.assert_called_once()
    saved_data = mock_write.call_args[0][1]
    new_task = saved_data[-1]

    assert new_task["name"] == "Neue Aufgabe"
    assert new_task["description"] == "Wichtige Deadline"
    assert new_task["priority"] == "hoch"
    assert new_task["date_due"] == "2025-12-24"
    assert new_task["task_id"] == 2
    assert new_task["date_created"] == "2025-01-01"


@patch("src.aufgabe.write")
@patch("src.aufgabe.read")
def test_create_task_duplicate(mock_read, mock_write, mock_task_data):
    mock_read.return_value = mock_task_data

    Task.create_task("Alte Aufgabe", "Andere Beschreibung", "2", "2025-12-24")

    mock_write.assert_not_called()


def test_task_constructor():
    task = Task(7, "API bauen", "REST-Endpunkte", "2025-10-10", "mittel", "2025-05-01")

    assert task.task_id == 7
    assert task.name == "API bauen"
    assert task.description == "REST-Endpunkte"
    assert task.date_due == "2025-10-10"
    assert task.priority == "mittel"
    assert task.date_created == "2025-05-01"
