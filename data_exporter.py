import json
import pandas as pd
import os
import sys

INPUT_F = "SCHEDULE_OUTPUT.json"
OUTPUT_EXCEL = "Plan_Zajec.xlsx"


def create_visual_schedule():
    """
    Wczytuje wynik algorytmu z json i generuje plik xlsx

    Funkcja tworzy tabelę (godziny x dni tygodnia), wpisuje lekcje do komórek
    i aplikuje style (zawijanie tekstu, ramki) przy użyciu XlsxWriter
    """
    print("Rozpoczynam generowanie excela")
    if not os.path.exists(INPUT_F):
        print("Błąd! Brak pliku {INPUT_F}, uruchom napierw generator.py")
        sys.exit(1)

    try:
        with open(INPUT_F, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Błąd przy zczytywaniu danych {e}")
        sys.exit(1)

    if not data:
        print("Plik SCHEDULE_OUTPUT.json jest pusty, nie da się utworzyć pliku")
        return

    SLOTS = ["12:00", "13:05", "14:10", "15:15", "16:35", "17:40", "18:45"]
    DAYS = ["1", "2", "3", "4", "5", "6", "7"]

    df = pd.DataFrame(index=SLOTS, columns=DAYS)
    df = df.fillna("")

    count = 0
    for lesson in data:
        dzien = str(lesson.get("Dzien"))
        godzina = lesson.get("Godzina")

        tekst = (
            f"{lesson.get('Przedmiot')}\n"
            f"Sala: {lesson.get('Sala')}\n"
            f"N: {lesson.get('Nauczyciel')}\n"
            f"U: {lesson.get('Uczeń')}\n"
        )

        if godzina in df.index and dzien in df.columns:
            if df.at[godzina, dzien]:
                df.at[godzina, dzien] += "\n\n" + tekst
            else:
                df.at[godzina, dzien] = tekst
            count += 1

    days_map = {
        "1": "Poniedziałek",
        "2": "Wtorek",
        "3": "Środa",
        "4": "Czwartek",
        "5": "Piątek",
        "6": "Sobota",
        "7": "Niedziela",
    }
    df.rename(columns=days_map, inplace=True)

    try:
        with pd.ExcelWriter(OUTPUT_EXCEL, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Grafik")

            workbook = writer.book
            worksheet = writer.sheets["Grafik"]

            cell_format = workbook.add_format(
                {"text_wrap": True, "valign": "top", "border": 1}
            )

            worksheet.set_column("A:A", 15)
            worksheet.set_column("B:H", 25, cell_format)

        print(f"SUKCES Wykonano plik: {OUTPUT_EXCEL}")
        print(f"Dla liczby lekcji: {count}")

    except Exception as e:
        print(f"Błąd! {e}")
        print("Czy plik Excela nie jest otwarty w innym programie?")


if __name__ == "__main__":
    create_visual_schedule()
