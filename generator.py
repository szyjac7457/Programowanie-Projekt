import json
import os
import sys
import copy
import random
from tqdm import tqdm
from rich.console import Console
from rich.table import Table

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

    # print("\n -----Planowanie----")
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

            dni_tygodnia = [1, 2, 3, 4, 5, 6, 7]
            random.shuffle(
                dni_tygodnia
            )  # wprowadzenie losowania zeby nie zaczynal od poniedziałku

            for dzien in dni_tygodnia:
                if lekcje_umowione_dla_ucznia >= needed:
                    break
                dzien_str = str(dzien)

                # Pobieramy dostępność na dany dzień
                t_day = tutor_schedule.get(dzien_str, {})
                s_day = student_schedule.get(dzien_str, {})

                # Wprowadzenie atrakcyjnosci godziny jesli sasiaduje z zajeta przez nauczyciela godzina i jest wczesna
                wszystkie_godziny_nauczyciela = list(t_day.keys())

                ##################################################################################
                def ocena_atrakcyjnosci(godz):
                    punkty = 0

                    idx = wszystkie_godziny_nauczyciela.index(godz)

                    for i in [-1, 1]:
                        check_idx = i + idx
                        if 0 <= check_idx < len(wszystkie_godziny_nauczyciela):
                            sasiad_h = wszystkie_godziny_nauczyciela[check_idx]
                            stan_sasiada = t_day[sasiad_h]
                            if stan_sasiada == "ZAJETE":
                                punkty += 500
                            elif stan_sasiada is False:
                                punkty += -10
                    return punkty

                ###################################################################################
                godziny_posortowane = sorted(
                    wszystkie_godziny_nauczyciela, key=ocena_atrakcyjnosci, reverse=True
                )

                for godzina in godziny_posortowane:
                    if lekcje_umowione_dla_ucznia >= needed:
                        break
                    t_available = t_day[godzina]

                    if t_available is not True:
                        continue
                    if s_day.get(godzina) is not True:
                        continue

                    wolna_sala_id = None

                    pref_room = str(intent.get("preferred_room_id"))
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
    base_tutors, base_students, base_rooms, base_intents = load_data(INPUT_FILE)
    if not base_tutors:
        sys.exit(1)

    best_grafik = []
    best_score = 0

    LICZBA_PROB = 1000

    print(f"\nStart dla  ({LICZBA_PROB} prób)...")

    for i in tqdm(range(LICZBA_PROB), colour="green", desc="Szukanie"):
        curr_tutors = copy.deepcopy(base_tutors)
        curr_students = copy.deepcopy(base_students)
        curr_rooms = copy.deepcopy(base_rooms)

        curr_intents = base_intents.copy()
        random.shuffle(curr_intents)

        grafik, wynik = generate_schedule(
            curr_tutors, curr_students, curr_rooms, curr_intents
        )

        if wynik > best_score:
            best_score = wynik
            best_grafik = grafik

    def wyswietl_wyniki(grafik, wynik):
        console = Console()
        print(f"\nNajlepszy znaleziony wynik: {wynik} lekcji.")

        if len(grafik) > 0:
            # Tworzymy tabelę Rich
            table = Table(title=f"Zoptymalizowany Plan Lekcji (Wynik: {wynik})")

            table.add_column("Dzień", style="cyan", justify="right")
            table.add_column("Godzina", style="green")
            table.add_column("Przedmiot", style="white")
            table.add_column("Uczeń", style="yellow")
            table.add_column("Nauczyciel", style="blue")
            table.add_column("Sala", style="red")

            # Sortujemy wiersze
            grafik_sorted = sorted(
                grafik, key=lambda x: (int(x["Dzien"]), x["Godzina"])
            )

            for lekcja in grafik_sorted:
                table.add_row(
                    str(lekcja["Dzien"]),
                    str(lekcja["Godzina"]),
                    str(lekcja["Przedmiot"]),
                    str(lekcja["Uczeń"]),
                    str(lekcja["Nauczyciel"]),
                    str(lekcja["Sala"]),
                )
            console.print(table)
        else:
            print("Nie udało się ułożyć planu.")

    wyswietl_wyniki(best_grafik, best_score)


if __name__ == "__main__":
    main()
