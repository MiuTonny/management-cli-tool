# 🧭 Management CLI Tool

A Python-based **Command-Line Interface (CLI)** application to manage **Users, Projects, and Tasks** — built with object-oriented programming, data persistence, and modern CLI design.

---

## 📂 Project Overview

This tool allows you to:
- Create users with a name and email  
- Create projects for each user (with descriptions and due dates)  
- Add tasks under specific projects  
- Mark tasks as complete  
- Persist all data in local JSON files  

---

## 🧠 Features Implemented

### ✅ CLI Entry
- Built using **`argparse`**
- Subcommands implemented:
  - `add-user` → create a user
  - `create-project` → create a project for a user
  - `add-task` → add a task to a project
  - `list-projects` → list all projects
  - `complete-task` → mark a task as complete  

---

### ✅ Object Model
| Class | Attributes | Relationships |
|--------|-------------|----------------|
| **User** | `name`, `email` | Has many Projects |
| **Project** | `title`, `description`, `due_date`, `status` | Has many Tasks, belongs to User |
| **Task** | `title`, `status`, `assigned_to` | Belongs to Project |

- Uses `__init__`, `__repr__`, and `__str__` for clean display  
- Includes instance and class methods (`create`, `all`, `find_by_name`, etc.)
- Demonstrates one-to-many relationships:
  - `User → Projects`
  - `Project → Tasks`

---

### ✅ Object-Oriented Programming Features
- Uses **`@property`** and setters for validation (`email`, `due_date`, `title`)
- Uses **class attributes** for auto-incrementing IDs
- Implements inheritance: `Person → User`
- Encapsulation and data validation applied

---

### ✅ Data Persistence
- Saves and loads all objects (`User`, `Project`, `Task`) using **JSON**
- Handles missing or malformed files with `try/except`
- File I/O handled in `utils/helpers.py`
- JSON files stored under `/data/`:
  - `users.json`
  - `projects.json`
  - `tasks.json`

---

### ✅ External Package
- Uses **[`rich`](https://pypi.org/project/rich/)** for colorful, styled CLI output
- Dependencies tracked in `requirements.txt`

---

## 🧰 File Structure

management-cli-tool/
│
├── main.py # CLI entry point
├── requirements.txt # External dependencies
│
├── models/
│ └── user.py # Contains User, Project, and Task classes
│
├── utils/
│ └── helpers.py # Load/save JSON helpers
│
├── data/
│ ├── users.json
│ ├── projects.json
│ └── tasks.json
│
└── test_models.py # Test script for verifying models and persistence

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone git@github.com:MiuTonny/management-cli-tool.git
cd management-cli-tool

Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate
Install dependencies
pip install -r requirements.txt

Running Tests
python test_models.py