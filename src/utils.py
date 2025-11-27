import datetime as dt
# AI assisted
def validate_date_format(date_string):
    try:
        dt.datetime.strptime(date_string, '%Y-%m-%d')  # Erwartetes Format YYYY-MM-DD
        return True
    except ValueError:
        return False

# AI assisted
def format_to_german_date(date_string):
    if validate_date_format(date_string):
        date = dt.datetime.strptime(date_string, '%Y-%m-%d')
        return date.strftime('%d.%m.%Y')  # Ausgabe: DD.MM.YYYY
    return "Ungültiges Format. Bitte YYYY-MM-DD verwenden."


def get_non_empty_input(prompt):
# AI assisted
# stellt sicher, dass die Eingabe nicht leer ist
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("Eingabe darf nicht leer sein. Bitte versuche es erneut.")

