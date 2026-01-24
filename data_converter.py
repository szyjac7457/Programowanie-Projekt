import json
import csv
import pandas as pd

SLOTS = ["12:00", "13:05", "14:10", "15:15", "16:35", "17:40", "18:45"]
lesson_duration = 60

def time_to_min(t_str):
    if not t_str: return None

    h, m = map(int, t_str.split(':'))
    return h * 60 + m

def availability_grid(raw_data, field_name):
    grid = {}
    all_ids = set(item[field_name] for item in raw_data)

    for id in all_ids:
        grid[id] = {
            day: {slot: False for slot in SLOTS}
            for day in range (1, 8)
        }

    for item in raw_data:
        id = item[field_name]
        day = item['weekday']
        start_min = time_to_min(item['time_start'])
        end_min = time_to_min(item['time_end'])

        for slot in SLOTS:
            lesson_time = time_to_min(slot)
            if start_min <= lesson_time and end_min >= (lesson_time + lesson_duration):
                grid[id][day][slot] = True
    
    return grid

def main():
    test = [
        {
            "student_id": 1,
            "weekday": 1,
            "time_start": "14:00",
            "time_end": "16:00"
        }
    ]

    print("Sprawdzam dostępność dla ucznia ID = 1...")
    print("-" * 40)

    result = availability_grid(test, "student_id")
    poniedzialek = result[1][1]

    for slot, is_ok in poniedzialek.items():
        if is_ok:
            print(f"{slot} PASUJE")
        else:
            print(f"{slot}NIE PASUJE")


if __name__ == "__main__":
    main()

