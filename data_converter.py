SLOTS = ["12:00", "13:05", "14:10", "15:15", "16:35", "17:40", "18:45"]
lesson_duration = 60


def time_to_min(t_str):
    if not t_str:
        return None

    h, m = map(int, t_str.split(":"))
    return h * 60 + m


def availability_grid(raw_data, field_name):
    grid = {}
    all_ids = set(item[field_name] for item in raw_data)

    for id in all_ids:
        grid[id] = {day: {slot: False for slot in SLOTS} for day in range(1, 8)}

    for item in raw_data:
        id = item[field_name]
        day = item["weekday"]
        start_min = time_to_min(item["time_start"])
        end_min = time_to_min(item["time_end"])

        for slot in SLOTS:
            lesson_time = time_to_min(slot)
            if start_min <= lesson_time and end_min >= (lesson_time + lesson_duration):
                grid[id][day][slot] = True

    return grid


def load_tutor_subject(f_path):
    tutor_subjcets = {}
    try:
        with open(f_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

            for line in lines[1:]:
                parts = line.strip().split(",")
                if not parts or not parts[0]:
                    continue

                tutor_id = int(parts[0])
                subjects = []
                for s in parts[1:]:
                    if s.strip():
                        subjects.append(int(s))
                tutor_subjcets[tutor_id] = subjects
    except FileNotFoundError:
        print(f"Błąd nie ma pliku {f_path}")

    return tutor_subjcets

def create_rooms_grid(rooms_data):
    grid = {}
    for room in rooms_data:
        room_id = room['id']
        grid[room_id] = {
            {day: {slot: True for slot in SLOTS} for day in range(1, 8)}
        }
    return grid



def main():
    test = [{"student_id": 1, "weekday": 1, "time_start": "14:00", "time_end": "16:00"}]

    print("Sprawdzam dostępność dla ucznia ID = 1...")
    print("-" * 40)

    result = availability_grid(test, "student_id")
    poniedzialek = result[1][1]

    for slot, is_ok in poniedzialek.items():
        if is_ok:
            print(f"{slot} PASUJE")
        else:
            print(f"{slot} NIE PASUJE")

    tutor_test = load_tutor_subject("Import/tutors_subject.csv")

    if tutor_test:
        for i, (t_id, sub) in enumerate(tutor_test.items()):
            if i < 3:
                print(f"T id = {t_id} uczy {sub}")
    else:
        print("Nie wczytani plikow")


if __name__ == "__main__":
    main()
