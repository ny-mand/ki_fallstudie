#Dieser code wurde mit Hilfe von KI erzeugt
import pytest
from unittest.mock import patch


from src.cli import run, create, assign, delete, delete_item, show_projects


@pytest.fixture
def mock_data():
    return {
        'projects': [{'project_id': 1, 'name': 'TestProjekt', 'description': 'Desc', 'priority': 'hoch',
                      'date_start': '2024-01-01', 'date_due': '2024-12-31'}],
        'members': [{'member_id': 1, 'name': 'Alice', 'job_title': 'Dev', 'active_since': '2024-01-01'}],
        'tasks': [
            {'task_id': 1, 'name': 'TestTask', 'description': 'Do it', 'priority': 'hoch', 'date_due': '2024-12-31',
             'date_created': '2024-01-01'}]
    }


# --- Test: run() Hauptmenü ---
@patch('src.cli.delete')  # NEU: Option 7
@patch('src.cli.show_projects')
@patch('src.cli.show_team_members')
@patch('src.cli.show_tasks')
@patch('src.cli.create')
@patch('src.cli.assign')
@patch('src.cli.filter_projects')
@patch('src.cli.get_non_empty_input')
@patch('builtins.input')
@patch('builtins.print')
def test_run_menu_navigation(mock_print, mock_builtin_input, mock_get_input, mock_filter, mock_assign, mock_create,
                             mock_show_tasks, mock_show_members, mock_show_projects, mock_delete):
    # Optionen 1 bis 7 und dann 0 (Ende)
    mock_get_input.side_effect = ["1", "2", "3", "4", "5", "6", "7", "0"]
    mock_builtin_input.return_value = ""

    run()

    assert mock_show_projects.called
    assert mock_show_members.called
    assert mock_show_tasks.called
    assert mock_create.called
    assert mock_assign.called
    assert mock_filter.called
    assert mock_delete.called  # Prüfen ob delete aufgerufen wurde


# --- Test: create() ---
@patch('src.cli.Project.create_project')
@patch('src.cli.TeamMember.add_member')
@patch('src.cli.Task.create_task')
@patch('src.cli.get_non_empty_input')
@patch('builtins.input')
@patch('builtins.print')
def test_create_menu(mock_print, mock_builtin_input, mock_get_input,
                     mock_create_task,mock_add_member,mock_create_project):
    # Fall 1: Projekt (1) -> Keine Mitglieder (n)
    mock_get_input.side_effect = ["1", "0", "0"]  # Extra Nullen für Sicherheit
    mock_builtin_input.side_effect = ["n", ""]
    mock_create_project.return_value = "P1"

    create()
    mock_create_project.assert_called_once()


# --- Test: assign() (Erweitertes Menü) ---
@patch('src.cli.Project.remove_member_from_project')  # NEU
@patch('src.cli.Project.remove_task_from_member')  # NEU
@patch('src.cli.Project.assign_task_to_member')
@patch('src.cli.Project.assign_member_to_project')
@patch('src.cli.Project.project_exists')  # Wichtig für Validierung
@patch('src.cli.get_non_empty_input')
@patch('builtins.input')
@patch('builtins.print')
def test_assign_menu(mock_print, mock_builtin_input, mock_get_input, mock_proj_exists, mock_assign_mem,
                     mock_assign_task, mock_rem_task, mock_rem_mem):
    mock_builtin_input.return_value = ""
    mock_proj_exists.return_value = True  # Wir tun so, als ob alle Projekte existieren

    # Szenario 1: Aufgabe zuweisen (1) -> Projekt, Mitglied, Aufgabe
    # Szenario 2: Aufgabe entfernen (2) -> Projekt, Mitglied, Aufgabe
    # Szenario 3: Mitglied zuweisen (3) -> Projekt, Anzahl(1), Name
    # Szenario 4: Mitglied entfernen (4) -> Projekt, Name
    # Szenario 5: Ende (0)

    mock_get_input.side_effect = [
        "1", "P1", "Alice", "Task1",  # Assign Task
        "2", "P1", "Alice", "Task1",  # Remove Task
        "3", "P1", "1", "Bob",  # Assign Member
        "4", "P1", "Charlie",  # Remove Member
        "0"  # Ende
    ]



    # --- Fall 1: Assign Task ---
    mock_get_input.side_effect = ["1", "P1", "Alice", "Task1"]
    assign()
    mock_assign_task.assert_called_with("P1", "Alice", "Task1")

    # --- Fall 2: Remove Task ---
    mock_get_input.side_effect = ["2", "P1", "Alice", "Task1"]
    assign()
    mock_rem_task.assert_called_with("P1", "Alice", "Task1")

    # --- Fall 3: Assign Member ---
    mock_get_input.side_effect = ["3", "P1", "1", "Bob"]
    assign()
    mock_assign_mem.assert_called_with("P1", "Bob")

    # --- Fall 4: Remove Member ---
    mock_get_input.side_effect = ["4", "P1", "Charlie"]
    assign()
    mock_rem_mem.assert_called_with("P1", "Charlie")


# --- Test: delete() Menü ---
@patch('src.cli.delete_item')
@patch('src.cli.get_non_empty_input')
@patch('builtins.print')
def test_delete_menu(mock_print, mock_get_input, mock_delete_item):
    # Teste Aufrufe: 1 (Projekt), 2 (Aufgabe), 3 (Mitglied), 0 (Ende)

    # Fall 1: Projekt
    mock_get_input.side_effect = ["1"]
    delete()
    mock_delete_item.assert_called_with("projekt")

    # Fall 2: Aufgabe
    mock_get_input.side_effect = ["2"]
    delete()
    mock_delete_item.assert_called_with("aufgabe")

    # Fall 3: Teammitglied
    mock_get_input.side_effect = ["3"]
    delete()
    mock_delete_item.assert_called_with("teammitglied")


# --- Test: delete_item() Logik ---
@patch('src.cli.write')
@patch('src.cli.read')
@patch('src.cli.Project.project_exists')
@patch('src.cli.get_non_empty_input')
@patch('builtins.print')
def test_delete_item_logic(mock_print, mock_get_input, mock_proj_exists, mock_read, mock_write, mock_data):
    # Wir testen das Löschen eines Projekts
    mock_read.return_value = mock_data['projects']  # Liste mit [{'name': 'TestProjekt', ...}]
    mock_proj_exists.return_value = True

    # Ablauf:
    # 1. Name eingeben -> "TestProjekt"
    # 2. Bestätigung -> "j"
    mock_get_input.side_effect = ["TestProjekt", "j"]

    delete_item("projekt")

    # Prüfung: Wurde write aufgerufen mit einer leeren Liste (weil das einzige Projekt gelöscht wurde)?
    mock_write.assert_called_once()
    args, _ = mock_write.call_args
    saved_data = args[1]
    assert len(saved_data) == 0  # Liste muss leer sein


# --- Test: show_projects (mit leerer Liste) ---
@patch('src.cli.read')
@patch('builtins.print')
def test_show_projects_empty(mock_print, mock_read):
    mock_read.return_value = []  # Keine Daten

    show_projects()

    # Prüfen ob "Keine Projekte gefunden" gedruckt wurde
    # Wir suchen in allen print-Aufrufen
    printed_msgs = [str(c[0][0]) for c in mock_print.call_args_list]
    assert any("Keine Projekte gefunden" in msg for msg in printed_msgs)



