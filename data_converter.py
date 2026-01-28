import os
import json

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
        room_id = room["id"]
        grid[room_id] = {day: {slot: True for slot in SLOTS} for day in range(1, 8)}
    return grid


def main():
    print("GENEROWANIE PLIKU")

    path_students = os.path.join("Import", "students_abavilities.json")
    path_tutors = os.path.join("Import", "tutor_avabilities.json")
    path_rooms = os.path.join("Import", "rooms.json")
    path_intentions = os.path.join("Import", "student_intentions.json")
    path_csv = os.path.join("Import", "tutors_subject.csv")

    try:
        with open(path_students, "r", encoding="utf-8") as f:
            d = json.load(f)
            students_data = d.get("data", d)
        with open(path_tutors, "r", encoding="utf-8") as f:
            d = json.load(f)
            tutors_data = d.get("data", d)
        with open(path_rooms, "r", encoding="utf-8") as f:
            d = json.load(f)
            rooms_data = d.get("data", d)
        with open(path_intentions, "r", encoding="utf-8") as f:
            d = json.load(f)
            intentions_data = d.get("data", d)
        tutor_subjects = load_tutor_subject(path_csv)

        print("Generowanie grafików")
        students_grid = availability_grid(students_data, "student_id")
        tutors_grid = availability_grid(tutors_data, "tutor_id")
        rooms_grid = create_rooms_grid(rooms_data)

        print("Łączenie intencji")
        intentions = []

        for intention in intentions_data:
            try:
                sub_id = int(intention["subject_id"])
                stu_id = int(intention["student_id"])

                if stu_id not in students_grid:
                    print(
                        f"Pominięto intencję ID {intention['id']} Uczeń {stu_id} brak dostępności"
                    )
                    continue

                possible_tutors = []
                for t_id, sub in tutor_subjects.items():
                    if sub_id in sub and t_id in tutors_grid:
                        possible_tutors.append(t_id)

                pref_loc = intention.get("preferred_location_id")
                notes = intention.get("notes", "")

                new_intention = {
                    "id": intention["id"],
                    "student_id": stu_id,
                    "subject_id": sub_id,
                    "weekly_sessions": intention.get("weekly_sessions", 1),
                    "possible_tutors_ids": possible_tutors,
                    "preferred_location_id": pref_loc,
                    "notes": notes,
                }
                intentions.append(new_intention)
            except (ValueError, KeyError):
                continue

        output = {
            "intentions": intentions,
            "resources": {
                "students": students_grid,
                "tutors": tutors_grid,
                "rooms": rooms_grid,
            },
        }

        with open("LESSONSYSTEM_DATA_INPUT.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)

        print("-" * 40)
        print("Utworzono plik LESSONSYSTEM_DATA_INPUT.json")
    except Exception as e:
        print(f"Błąd {e}")


if __name__ == "__main__":
    main()
