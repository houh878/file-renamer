import os
import datetime
import re

folder_path = "c:\\Users\\ajeel\\OneDrive\\Desktop\\files_to_name"

# Prüft ob der Dateiname bereits im korrekten Format ist
def is_date_formatted(filename):
    # Entferne Dateierweiterung und mögliche Nummerierung
    base_name = filename.replace('.txt', '')
    # Prüfe ob es das Format DD-MM-YYYY oder DD-MM-YYYY_N hat
    pattern = r'^\d{2}-\d{2}-\d{4}(_\d+)?$'
    return bool(re.match(pattern, base_name))

# Findet den nächsten verfügbaren Dateinamen
def get_next_available_name(base_path, date_str):
    new_name = f"{date_str}.txt"
    if not os.path.exists(os.path.join(base_path, new_name)):
        return new_name
    
    # Finde die höchste existierende Nummer
    max_num = 0
    for file in os.listdir(base_path):
        if file.startswith(date_str):
            match = re.search(r'_(\d+)\.txt$', file)
            if match:
                num = int(match.group(1))
                max_num = max(max_num, num)
    
    # Inkrementiere die höchste Nummer um 1
    next_num = max_num + 1
    new_name = f"{date_str}_{next_num}.txt"
    
    # Stelle sicher, dass der neue Name nicht existiert
    while os.path.exists(os.path.join(base_path, new_name)):
        next_num += 1
        new_name = f"{date_str}_{next_num}.txt"
    
    return new_name

for item in os.listdir(folder_path):
    if item.endswith(".txt"):
        try:
            # Prüfe ob die Datei bereits im korrekten Format ist
            if is_date_formatted(item):
                print(f"Datei {item} wurde bereits umbenannt.")
                continue

            # ...existing code...
            old_name = os.path.join(folder_path, item)
            creation_time = os.path.getctime(old_name)
            date_created = datetime.datetime.fromtimestamp(creation_time).strftime("%d-%m-%Y")
            new_name = get_next_available_name(folder_path, date_created)
            new_path = os.path.join(folder_path, new_name)

            # Benenne Datei um
            os.rename(old_name, new_path)
            print(f"Datei {item} wurde erfolgreich in {new_name} umbenannt.")

        #Fängt exceptions ab, die beim Umbenennen auftreten können
        except PermissionError as pe:
            print(f"PermissionError: {pe}. Überspringe Datei {item}.")
            continue
        except Exception as e:
            print(f"Fehler beim Umbenennen von {item}: {str(e)}")
            continue





