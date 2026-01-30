# System Planowania Lekcji

Aplikacja automatyzuje proces układania grafiku korepetycji, generując harmonogram w formacie Excel.

**Autorzy:**
* Szymon Jachimowicz
* Mikołaj Szyra

## Funkcjonalności
1. **Agregacja danych:** Pobieranie dostępności uczniów, nauczycieli i sal z plików JSON/CSV.
2. **Algorytm planowania:** Inteligentne dopasowanie terminów, minimalizacja okienek.
3. **Eksport wyników:** Generowanie czytelnego kalendarza w formacie `.xlsx` (Excel).
4. **Interfejs:** Obsługa z poziomu terminala z paskiem postępu.

## Instalacja i Wymagania
Projekt wymaga Pythona 3.8+ oraz bibliotek zewnętrznych.

1. Pobierz repozytorium.
2. Zainstaluj wymagane biblioteki:
   ```bash
   pip install -r requirements.txt
   ```

## Uruchomienie
Aby uruchomić cały system (konwersja -> planowanie -> eksport), wpisz:

```bash
python run_system.py
