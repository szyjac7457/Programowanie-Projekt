import json
import os
import sys

INPUT_FILE = "LESSONSYSTEM_DATA_INPUT.json"


def load_data(filepath):
    #ta funkcja ma wczytać dane i zwrocić (tutors, students, rooms, intents)

    if not os.path.exists(filepath):
        print(f" BŁĄD KRYTYCZNY: Nie znaleziono pliku '{filepath}'!")
        return None, None, None, None

    try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            resources = data.get('resources', {})

            tutors = resources.get('tutors', {})
            students = resources.get('students', {})
            rooms = resources.get('rooms', {})

            intents = data.get('intentions', [])


            print(f"✅ Sukces! Załadowano:")
            print(f"   - Nauczyciele: {len(tutors)}")
            print(f"   - Uczniowie:   {len(students)}")
            print(f"   - Sale:        {len(rooms)}")
            print(f"   - Zgłoszenia:  {len(intents)}")
            
            return tutors, students, rooms, intents
    except json.JSONDecodeError:
        print(f" BŁĄD: Plik '{filepath}' nie jest poprawnym JSON-em!")
        return None, None, None, None
    except Exception as e:
        print(f" BŁĄD NIEOCZEKIWANY: {e}")
        return None, None, None, None
    

def main():
    print("--------GENERATOR GRAFIKU------")
    
  
    tutors_map, students_map, rooms_map, intentions_list = load_data(INPUT_FILE)

    
    if not tutors_map or not intentions_list:
        print("  Brak danych do przetwarzania. Zamykam program.")
        sys.exit(1)

    

if __name__ == "__main__":
    main()