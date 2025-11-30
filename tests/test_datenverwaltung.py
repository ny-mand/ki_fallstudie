#Dieser code wurde mit Hilfe von KI erzeugt
from unittest.mock import patch, mock_open
from src.dateiverwaltung import read, write


# --- Tests für read() ---

def test_read_success():
    # Simulierter Datei-Inhalt (JSON)
    mock_content = '[{"id": 1, "name": "Test"}]'

    # mock_open simuliert das Öffnen einer Datei
    with patch("builtins.open", mock_open(read_data=mock_content)) as mocked_file:
        result = read("dummy.json")

        # Prüfung 1: Wurde die Datei geöffnet?
        mocked_file.assert_called_once_with("dummy.json", "r")

        # Prüfung 2: Wurden die Daten korrekt als Python-Objekt zurückgegeben?
        assert result == [{"id": 1, "name": "Test"}]


def test_read_file_not_found():
    # Wir simulieren, dass open() einen FileNotFoundError wirft
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read("nicht_existent.json")

        # Erwartung: Leere Liste wird zurückgegeben (wie in deinem Code definiert)
        assert result == []




# --- Tests für write() ---

@patch("json.dump")
def test_write_success(mock_json_dump):
    data_to_write = [{"id": 1, "name": "Neu"}]

    # Wir mocken open(), damit keine echte Datei entsteht
    with patch("builtins.open", mock_open()) as mocked_file:
        write("output.json", data_to_write)

        # Prüfung 1: Wurde Datei im Schreibmodus ('w') geöffnet?
        mocked_file.assert_called_once_with("output.json", 'w')

        # Prüfung 2: Wurde json.dump mit den richtigen Daten aufgerufen?
        # Wir prüfen die Argumente, die an json.dump übergeben wurden
        # call_args[0] sind die positionalen Args: (data, file_obj)
        # call_args[1] sind die Keyword Args: {indent: 2}

        args, kwargs = mock_json_dump.call_args
        assert args[0] == data_to_write  # Das Daten-Objekt
        assert kwargs['indent'] == 2  # Die Formatierung


@patch("builtins.print")  # Wir wollen die Fehlermeldung abfangen
def test_write_file_not_found(mock_print):
    # Szenario: Datei kann nicht geöffnet werden (z.B. fehlende Berechtigung oder Pfad)
    # Dein Code fängt FileNotFoundError ab.

    with patch("builtins.open", side_effect=FileNotFoundError):
        write("invalid/path/output.json", [])

        # Prüfung: Wurde die Fehlermeldung gedruckt?
        mock_print.assert_called()
        assert "nicht gefunden" in mock_print.call_args[0][0]
