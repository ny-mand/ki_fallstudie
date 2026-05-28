#Dieser code wurde mit Hilfe von KI erzeugt
import pytest
from unittest.mock import patch
from src.teammitglied import TeamMember


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


@patch("src.teammitglied.read")
def test_member_exists(mock_read, mock_member_data):
    mock_read.return_value = mock_member_data

    assert TeamMember.member_exists("Alice") is True
    assert TeamMember.member_exists("alice") is True
    assert TeamMember.member_exists("Charlie") is False


@patch("src.teammitglied.write")
@patch("src.teammitglied.read")
@patch("src.teammitglied.validate_date_format")
def test_add_member_success(mock_validate, mock_read, mock_write, mock_member_data):
    mock_read.return_value = mock_member_data
    mock_validate.return_value = True

    TeamMember.add_member("Charlie", "Tester", "2023-01-01")

    mock_write.assert_called_once()
    saved_data = mock_write.call_args[0][1]
    new_member = saved_data[-1]

    assert new_member["name"] == "Charlie"
    assert new_member["job_title"] == "Tester"
    assert new_member["member_id"] == 3
    assert new_member["active_since"] == "2023-01-01"


@patch("src.teammitglied.write")
@patch("src.teammitglied.read")
def test_add_member_duplicate(mock_read, mock_write, mock_member_data):
    mock_read.return_value = mock_member_data

    TeamMember.add_member("Alice", "Architect", "2024-01-01")

    mock_write.assert_not_called()


def test_teammember_constructor():
    member = TeamMember("Mila", "QA", "2024-05-01")

    assert member.name == "Mila"
    assert member.job_title == "QA"
    assert member.active_since == "2024-05-01"



