import json
import os
import sys

INPUT_FILE = "LESSONSYSTEM_DATA_INPUT.json"


def load_data(filepath):
    # ta funkcja ma wczytać dane i zwrocić (tutors, students, rooms, intents)

    if not os.path.exists(filepath):
        print(f" BŁĄD KRYTYCZNY: Nie znaleziono pliku '{filepath}'!")
        return None, None, None, None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        resources = data.get("resources", {})

        tutors = resources.get("tutors", {})
        students = resources.get("students", {})
        rooms = resources.get("rooms", {})

        intents = data.get("intentions", [])

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


def generate_schedule(tutors, students, rooms, intents):
    # To bedzie serce programu. Z początku prosta pętla dobierająca wolną godzinę

    print("\n -----Planowanie----")
    grafik = []
    zrealizowane = 0

    for intent in intents:
        s_id = str(intent["student_id"])
        subject_id = intent["subject_id"]
        needed = intent.get(
            "weekly_sessions", 1
        )  # na wszelki wypadek niech wpisze 1, [] bo dane są trudne
        possible_tutors = intent.get("possible_tutors_ids", [])

        if s_id not in students:
            print(f"  Pominięto zgłoszenie: Brak ucznia ID {s_id} w bazie.")
            continue

        student_schedule = students[
            s_id
        ]  # "wskaznik" na danego ucznia by nie działac ciagle na students
        lekcje_umowione_dla_ucznia = 0

        # Pętla po nauczycielach
        for t_id_raw in possible_tutors:
            if lekcje_umowione_dla_ucznia >= needed:
                break

            t_id = str(t_id_raw)
            if t_id not in tutors:
                continue  # Tego nauczyciela nie ma w bazie, sprawdzamy następnego

            tutor_schedule = tutors[t_id]

            for dzien in range(1, 8):
                if lekcje_umowione_dla_ucznia >= needed:
                    break
                dzien_str = str(dzien)

                # Pobieramy dostępność na dany dzień
                t_day = tutor_schedule.get(dzien_str, {})
                s_day = student_schedule.get(dzien_str, {})

                #Wprowadzenie atrakcyjnosci godziny jesli sasiaduje z zajeta przez nauczyciela godzina i jest wczesna
                wszystkie_godziny =list(t_day.keys())
               
             ##################################################################################
                def ocena_atrakcyjnosci(godz):
                    punkty = 0 
                    try:
                            h_int = int(godz.split(':')[0])
                            punkty += (24 - h_int) * 10  
                    except:
                            pass
                    idx = wszystkie_godziny.index(godz)
                     
                    for i in [-1,1]:
                        check_idx = i + idx 
                        if 0 <= check_idx < len(wszystkie_godziny):
                            sasiad_h = wszystkie_godziny[check_idx]
                            stan_sasiada = t_day[sasiad_h]
                            if stan_sasiada == "ZAJETE":
                                punkty += 500  
                            elif stan_sasiada is False:
                                punkty +=-10
                    return punkty
                ###################################################################################
                godziny_posortowane = sorted(wszystkie_godziny, key=ocena_atrakcyjnosci, reverse=True)

                for godzina in godziny_posortowane:
                    if lekcje_umowione_dla_ucznia >= needed: break
                    t_available = t_day[godzina]

                    if t_available is not True: continue      
                    if s_day.get(godzina) is not True: continue
                
                    wolna_sala_id = None

                    pref_room = str(intent.get('preferred_room_id'))
                    lista_sal = list(rooms.keys())

                    if pref_room and pref_room in lista_sal:
                        lista_sal.remove(pref_room)
                        lista_sal.insert(0, pref_room)
            
                    for r_id in lista_sal:
                        if rooms[r_id][str(dzien)][godzina] is True:
                            wolna_sala_id = r_id
                            break
                    # print(wolna_sala_obj)
                    if wolna_sala_id:
                        # sukces, zapisanie lekcji
                        grafik.append(
                            {
                                "Dzien": dzien,
                                "Godzina": godzina,
                                "Przedmiot": subject_id,
                                "Uczeń": s_id,
                                "Nauczyciel": t_id,
                                "Sala": wolna_sala_id,
                            }
                        )

                        # Zajecie zasobow
                        t_day[godzina] = "ZAJETE"
                        s_day[godzina] = False
                        rooms[wolna_sala_id][str(dzien)][godzina] = False

                        lekcje_umowione_dla_ucznia += 1
                        zrealizowane += 1

    return grafik, zrealizowane


def main():
    tutors, students, rooms, intents = load_data(INPUT_FILE)
    if not tutors:
        sys.exit(1)

    grafik, sukcesy = generate_schedule(tutors, students, rooms, intents)

    print(f"\nZAKOŃCZONO PLANOWANIE.")
    print(f"   Umówiono lekcji: {sukcesy}")

    if len(grafik) > 0:
        print("\nPrzykładowe 5 lekcji:")
        for lekcja in grafik[:5]:
            print(lekcja)
    else:
        print("  Nie udało się umówić żadnej lekcji.")


if __name__ == "__main__":
    main()
