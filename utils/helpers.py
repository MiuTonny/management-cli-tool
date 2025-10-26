import json
from json import JSONDecodeError
from pathlib import Path
from models import User, Project, Task

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_data(filename):
    """Load a list of dicts from a JSON file; return [] if missing or malformed."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except JSONDecodeError:
        print(f"Warning: '{filename}' is malformed. Loading empty list.")
        return []


def save_data(filename, data):
    """Write data (list of dicts) to a JSON file with indentation."""
    filepath = DATA_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def save_all():
    """Persist all Users, Projects, and Tasks to their respective JSON files."""
    save_data("users.json", [u.to_dict() for u in User.all()])
    save_data("projects.json", [p.to_dict() for p in Project.all()])
    save_data("tasks.json", [t.to_dict() for t in Task.all()])
    print("Saved users.json, projects.json, tasks.json")


def load_all():
    """Rebuild all Users, Projects, and Tasks from JSON into memory."""
    User.clear()
    Project.clear()
    Task.clear()

    for u in load_data("users.json") or []:
        User.from_dict(u)
    for p in load_data("projects.json") or []:
        Project.from_dict(p)
    for t in load_data("tasks.json") or []:
        Task.from_dict(t)

    print("Loaded users, projects, tasks from JSON")
