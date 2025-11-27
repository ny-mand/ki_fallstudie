import datetime
# AI assisted
def validate_date_format(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')  # Erwartetes Format YYYY-MM-DD
        return True
    except ValueError:
        return False

# AI assisted
def format_to_german_date(date_string):
    if validate_date_format(date_string):
        dt = datetime.strptime(date_string, '%Y-%m-%d')
        return dt.strftime('%d.%m.%Y')  # Ausgabe: DD.MM.YYYY
    return "Ungültiges Format. Bitte YYYY-MM-DD verwenden."
