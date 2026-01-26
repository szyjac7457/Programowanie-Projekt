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


            print(f" Sukces! Załadowano:")
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

    
def generate_schedule(tutors,students,rooms,intents):
    #To bedzie serce programu. Z początku prosta pętla dobierająca wolną godzinę

    print("\n -----Planowanie----")
    grafik = []

    for intent in intents:
        s_id = str(intent['student_id'])
        subject_id = intent['subject_id']
        needed = intent.get('weekly_sessions', 1) # na wszelki wypadek niech wpisze 1, [] bo dane są trudne
        possible_tutors = intent.get('possible_tutors_ids', [])

        if s_id not in students:
            print(f"  Pominięto zgłoszenie: Brak ucznia ID {s_id} w bazie.")
            continue

        student_schedule = students[s_id] #"wskaznik" na danego ucznia by nie działac ciagle na students
        lekcje_umowione_dla_ucznia = 0


    #  Pętla po nauczycielach
        for t_id_raw in possible_tutors:
            if lekcje_umowione_dla_ucznia >= needed:
                break 
            
            t_id = str(t_id_raw)
            if t_id not in tutors: 
                continue # Tego nauczyciela nie ma w bazie, sprawdzamy następnego
            
            tutor_schedule = tutors[t_id]






if __name__ == "__main__":
    main()