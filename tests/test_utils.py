#Dieser code wurde mit Hilfe von KI erzeugt
from unittest.mock import patch
from src.utils import validate_date_format, format_to_german_date, get_non_empty_input


# --- Tests für validate_date_format ---

def test_validate_date_format_valid():
    # Gültiges Datum (YYYY-MM-DD)
    assert validate_date_format("2023-12-31") is True
    assert validate_date_format("2024-02-29") is True  # Schaltjahr-Test


def test_validate_date_format_invalid():
    # Ungültige Formate oder Inhalte
    assert validate_date_format("31.12.2023") is False  # Falsches Format
    assert validate_date_format("2023/12/31") is False  # Falsches Trennzeichen
    assert validate_date_format("Hallo") is False  # Kein Datum
    assert validate_date_format("2023-02-30") is False  # Datum gibt es nicht (30. Feb)
    assert validate_date_format("") is False  # Leerstring


# --- Tests für format_to_german_date ---

def test_format_to_german_date_valid():
    # Gültige Umwandlung: YYYY-MM-DD -> DD.MM.YYYY
    assert format_to_german_date("2023-12-31") == "31.12.2023"
    assert format_to_german_date("2024-01-05") == "05.01.2024"


def test_format_to_german_date_invalid():
    # Sollte Fehlermeldung zurückgeben
    expected_msg = "Ungültiges Format. Bitte YYYY-MM-DD verwenden."
    assert format_to_german_date("31.12.2023") == expected_msg
    assert format_to_german_date("kein datum") == expected_msg


# --- Tests für get_non_empty_input ---

@patch('builtins.input')
@patch('builtins.print')  # Um die Fehlermeldung in der Konsole zu unterdrücken
def test_get_non_empty_input_success_first_try(mock_print, mock_input):
    # Szenario: Benutzer gibt sofort etwas Gültiges ein
    mock_input.return_value = "Gültige Eingabe"

    result = get_non_empty_input("Gib was ein:")

    assert result == "Gültige Eingabe"
    mock_print.assert_not_called()  # Keine Fehlermeldung gedruckt


@patch('builtins.input')
@patch('builtins.print')
def test_get_non_empty_input_retry(mock_print, mock_input):
    # Szenario:
    # 1. Benutzer drückt Enter (leer) -> Loop läuft weiter
    # 2. Benutzer drückt Leertasten (leer nach strip) -> Loop läuft weiter
    # 3. Benutzer gibt "Endlich" ein -> Success

    mock_input.side_effect = ["", "   ", "Endlich"]

    result = get_non_empty_input("Gib was ein:")

    assert result == "Endlich"

    # Wurde die Fehlermeldung gedruckt? (2x für die ersten beiden Fehlversuche)
    assert mock_print.call_count == 2
    args, _ = mock_print.call_args
    assert "Eingabe darf nicht leer sein" in args[0]
