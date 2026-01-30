import subprocess
import sys
import time
import os

def run_step(script_name, step_desc):
    """
    Uruchamia podany skrypt jako podproces i monitoruje jego status
    
    Args:
        script_name (str): Nazwa pliku do uruchomienia
        step_desc (str): Opis kroku wyświetlany użytkownikowi
        
    Returns:
        bool: True lub false w zależności czy się udało czy nie
    """
    print(f"\n{'-'*60}")
    print(f"Etap: {step_desc}")
    print(f"Uruchamiam: {script_name}")
    print(f"\n{'-'*60}")

    if not os.path.exists(script_name):
        print(f"Błąd! Nie znaleziono pliku {script_name}")
        return False
    
    try:
        result = subprocess.run([sys.executable, script_name], check=False)
        if result.returncode == 0:
            print(f"\n  SUKCES: {step_desc} zakończony")
            time.sleep(1) 
            return True
        else:
            print(f"\n  BŁĄD! Skrypt {script_name} zwrócił kod błędu {result.returncode}")
            return False
            
    except Exception as e:
        print(f"\n  BŁĄD! Nie udało się uruchomić {script_name} - wyrzucił {e}")
        return False
    
def main():
    print(f"\n{'-'*60}")
    print(f"    SYSTEM PLANOWANIA ZAJĘĆ")
    print(f"\n{'-'*60}")

    if not run_step("data_converter.py", "1. Przygotowanie danych (JSON)"):
        print("Zatrzymano system z powodu błędu w kroku 1.")
        sys.exit(1)
    if not run_step("generator.py", "2. Algorytm planowania"):
        print("Zatrzymano system z powodu błędu w kroku 2.")
        sys.exit(1)
        
    print(f"\n{'-'*60}")
        
    while True:
        try:
            decyzja = input("Czy chcesz zapisać wygenerowany plan do pliku Excel (Plan_Zajec.xlsx)? [t/n]: ").strip().lower()
            
            if decyzja in ['t', 'tak', 'y', 'yes']:
                if run_step("data_exporter.py", "3. Generowanie wizualnego Excela"):
                    print("\n" + "-"*60)
                    print("   SUUKCES")
                    print("   Możesz otworzyć plik: Plan_Zajec.xlsx")
                else:
                    print("\nWystąpił problem podczas generowania Excela")
                break
                
            elif decyzja in ['n', 'nie', 'no']:
                print("\nAnulowano zapis do Excela. Dane pozostają tylko w pliku JSON.")
                print("Koniec programu")
                break
            
            else:
                print("Niepoprawny wybór. Wpisz 't' lub 'n'")
                
        except KeyboardInterrupt:
            print("\nPrzerwano przez użytkownika")
            sys.exit(0)

if __name__ == "__main__":
    main()