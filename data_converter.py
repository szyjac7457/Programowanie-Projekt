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