# models/__init__.py

# models/user.py
# Single-file model module that defines Person → User, Project, Task
# attributes, relationships, class methods, OOP features, JSON helpers.
#READ: this project should have been divided into 3 files for each class.

from __future__ import annotations
from typing import Optional, List
import re


# Base class: Person

class Person:
    """Base entity with a name."""

    def __init__(self, name: str):
        self.name = name  

    def __str__(self) -> str:
        return f"Person(name='{self.name}')"

    __repr__ = __str__



# User: Person → User
#   - attributes: name, email
#   - relationships: one-to-many → projects, tasks
#   - registry & classmethods: create/all/find/clear
#   - JSON helpers: to_dict/from_dict
class User(Person):
    users: List["User"] = []   # class registry for all users
    _id_seq: int = 1           # class ID counter

    _email_re = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")  # basic email check

    def __init__(self, name: str, email: str):
        super().__init__(name)
        # assign unique id
        self.id: int = User._id_seq
        User._id_seq += 1

        # validate & set email through property
        self._email: Optional[str] = None
        self.email = email

        # relationships
        self.tasks: List[Task] = []
        self.projects: List[Project] = []

        # register
        User.users.append(self)

    # Properties
    @property
    def email(self) -> str:
        """Return validated email address."""
        return self._email or ""

    @email.setter
    def email(self, value: str) -> None:
        """Validate format before setting."""
        if not value or not User._email_re.match(value):
            raise ValueError("Invalid email format")
        self._email = value

    #Classmethods: collections & lookup
    @classmethod
    def create(cls, name: str, email: str) -> "User":
        """Factory that also registers the new user."""
        return cls(name, email)

    @classmethod
    def all(cls) -> List["User"]:
        """Return all users."""
        return list(cls.users)

    @classmethod
    def find_by_name(cls, name: str) -> Optional["User"]:
        """Find a user by name (case-sensitive)."""
        for u in cls.users:
            if u.name == name:
                return u
        return None

    @classmethod
    def clear(cls) -> None:
        """Clear the in-memory registry (used before load)."""
        cls.users.clear()
        cls._id_seq = 1

    #Relationship helpers
    def create_project(self, title: str, description: str = "", due_date: Optional[str] = None) -> "Project":
        """Create & link a new project for this user."""
        project = Project(title=title, description=description, due_date=due_date, status=False)
        self.projects.append(project)
        project.owner = self
        print(f"Project '{project.title}' was created for user {self.name}.")
        return project

    def add_task_to_project(self, title: str, project_title: str) -> Optional["Task"]:
        """Create a task (assigned to this user) under an existing project of this user."""
        project = self.get_project_by_title(project_title)
        if not project:
            print(f"Project '{project_title}' not found for user {self.name}.")
            return None
        task = Task(assigned_to=self.name, title=title, status=False)
        # link both sides
        self.tasks.append(task)
        project.tasks.append(task)
        task.project = project
        print(f"Task '{task.title}' was added to project '{project_title}' for user {self.name}.")
        return task

    #Instance lookups
    def get_task_by_title(self, title: str) -> Optional["Task"]:
        """Find this user's task by its title."""
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def get_project_by_title(self, title: str) -> Optional["Project"]:
        """Find this user's project by its title."""
        for project in self.projects:
            if project.title == title:
                return project
        return None

    #JSON helpers
    def to_dict(self) -> dict:
        """Serialize minimal fields (relationships restored on load)."""
        return {"id": self.id, "name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Create or reuse a user from saved data (id is ignored for simplicity)."""
        existing = cls.find_by_name(data["name"])
        if existing:
            # refresh email if needed
            existing.email = data.get("email", existing.email)
            return existing
        return cls.create(name=data["name"], email=data.get("email", ""))

    #Pretty printing
    def __str__(self) -> str:
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', projects={len(self.projects)}, tasks={len(self.tasks)})"

    __repr__ = __str__

# Project
#   - attributes: title, description, due_date, status
#   - relationships: owner (User), tasks (list[Task])
#   - properties: due_date (light 'YYYY-MM-DD' validation)
#   - registry & classmethods, JSON helpers
class Project:
    projects: List["Project"] = []  # class registry
    _id_seq: int = 1                # class ID counter

    def __init__(self, title: str, description: str = "", due_date: Optional[str] = None, status: bool = False):
        # ID
        self.id: int = Project._id_seq
        Project._id_seq += 1

        # core fields
        self.title = title
        self.description = description

        # validate via property
        self._due_date: Optional[str] = None
        self.due_date = due_date

        # status: False=incomplete, True=completed
        self.status = status

        # relationships
        self.tasks: List[Task] = []
        self.owner: Optional[User] = None

        # register
        Project.projects.append(self)

    # Properties
    @property
    def due_date(self) -> Optional[str]:
        """Return due date as 'YYYY-MM-DD' or None."""
        return self._due_date

    @due_date.setter
    def due_date(self, value: Optional[str]) -> None:
        """Light validation for date string; accept None."""
        if value is None:
            self._due_date = None
            return
        parts = str(value).split("-")
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            self._due_date = value
        else:
            raise ValueError("due_date must be 'YYYY-MM-DD' or None")

    # Classmethods: collections & lookup
    @classmethod
    def create(cls, title: str, description: str = "", due_date: Optional[str] = None,
               owner: Optional[User | str] = None, status: bool = False) -> "Project":
        """Factory that optionally links to an owner."""
        p = cls(title=title, description=description, due_date=due_date, status=status)
        if owner:
            # allow passing a User object or a user name string
            if isinstance(owner, User):
                p.owner = owner
                owner.projects.append(p)
            else:
                u = User.find_by_name(owner)
                if u:
                    p.owner = u
                    u.projects.append(p)
        return p

    @classmethod
    def all(cls) -> List["Project"]:
        return list(cls.projects)

    @classmethod
    def find_by_title(cls, title: str) -> Optional["Project"]:
        for p in cls.projects:
            if p.title == title:
                return p
        return None

    @classmethod
    def clear(cls) -> None:
        cls.projects.clear()
        cls._id_seq = 1

    #Relationship helpers
    def add_task(self, task: "Task") -> None:
        """Attach an existing task to this project."""
        self.tasks.append(task)
        task.project = self
        print(f"Task '{task.title}' added to project '{self.title}'.")

    def list_tasks(self) -> None:
        """Print all tasks under this project."""
        if not self.tasks:
            print(f"No tasks found for project '{self.title}'.")
        else:
            print(f"Tasks under project '{self.title}':")
            for task in self.tasks:
                print(f" - {task.title} (Assigned to: {task.assigned_to})")

    #Status helpers
    def mark_complete(self) -> None:
        """Manually mark the project as complete."""
        self.status = True
        print(f"Project '{self.title}' marked as complete.")

    def auto_check_status(self) -> None:
        """Auto-set status True if ALL tasks are complete and there is at least one task."""
        if all(task.status for task in self.tasks) and self.tasks:
            self.status = True
            print(f"Project '{self.title}' is completed.")
        else:
            self.status = False
            print(f"Project '{self.title}' is still incomplete.")

    #JSON helpers
    def to_dict(self) -> dict:
        """Serialize minimal fields; relationships are restored on load."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "status": self.status,
            "owner_name": self.owner.name if self.owner else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        """Recreate a project and link to its owner by name (if present)."""
        return cls.create(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date"),
            owner=data.get("owner_name"),
            status=data.get("status", False),
        )

    #Pretty printing
    def __str__(self) -> str:
        owner_name = self.owner.name if self.owner else "None"
        return (f"Project(id={self.id}, title='{self.title}', completed={self.status}, "
                f"owner='{owner_name}', tasks={len(self.tasks)}, due_date='{self.due_date}', "
                f"description='{self.description}')")

    __repr__ = __str__

# Task
#   - attributes: title, status, assigned_to (string: user's name)
#   - relationships: project (Project)
#   - properties: title (non-empty)
#   - registry & classmethods, JSON helpers
class Task:
    tasks: List["Task"] = []  # class registry
    _id_seq: int = 1          # class ID counter

    def __init__(self, assigned_to: str, title: str, status: bool = False):
        # ID
        self.id: int = Task._id_seq
        Task._id_seq += 1

        # assigned_to kept as user's name (string) for simple JSON
        self.assigned_to: str = assigned_to

        # title validated via property
        self._title: Optional[str] = None
        self.title = title  # triggers setter validation

        # status flag
        self.status: bool = status

        # back-reference to project (set when linked)
        self.project: Optional[Project] = None

        # register
        Task.tasks.append(self)

    # Properties
    @property
    def title(self) -> str:
        """Return task title (always non-empty)."""
        return self._title or ""

    @title.setter
    def title(self, value: str) -> None:
        """Enforce a non-empty title."""
        if not value or not str(value).strip():
            raise ValueError("Task title cannot be empty")
        self._title = str(value).strip()

    # Classmethods: collections & lookup
    @classmethod
    def create(cls, title: str, assigned_to: User | str,
               project: Project | str | None = None, status: bool = False) -> "Task":
        """Factory that links to a user (by object or name) and optional project."""
        user = assigned_to if isinstance(assigned_to, User) else User.find_by_name(assigned_to)
        t = cls(assigned_to=(user.name if isinstance(user, User) else str(assigned_to)), title=title, status=status)

        # link to user registry (so user.tasks reflects this task)
        if isinstance(user, User):
            user.tasks.append(t)

        # link to project (object or by title)
        if project:
            p = project if isinstance(project, Project) else Project.find_by_title(project)
            if p:
                p.tasks.append(t)
                t.project = p
        return t

    @classmethod
    def all(cls) -> List["Task"]:
        return list(cls.tasks)

    @classmethod
    def find_by_title(cls, title: str) -> Optional["Task"]:
        for t in cls.tasks:
            if t.title == title:
                return t
        return None

    @classmethod
    def clear(cls) -> None:
        cls.tasks.clear()
        cls._id_seq = 1

    #Instance helpers
    def show_assigned_to(self) -> None:
        """Print who this task is assigned to."""
        print(f"This task is assigned to: {self.assigned_to}")

    def show_title(self) -> None:
        """Print the task title."""
        print(f"Task title: {self.title}")

    def complete(self) -> None:
        """Mark task complete and auto-check its project status."""
        if not self.status:
            self.status = True
            print(f"Task '{self.title}' completed.")
            if self.project:
                self.project.auto_check_status()
        else:
            print(f"Task '{self.title}' is already completed.")

    def show_details(self) -> None:
        """Print a compact summary of this task."""
        project_name = self.project.title if self.project else "No project assigned"
        print(f"Task(id={self.id}, title='{self.title}', assigned_to='{self.assigned_to}', "
              f"project='{project_name}', done={self.status})")

    # JSON helpers
    def to_dict(self) -> dict:
        """Serialize minimal fields; relationships are restored on load."""
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "assigned_to_name": self.assigned_to,
            "project_title": self.project.title if self.project else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Recreate task and link to user/project by name/title."""
        return cls.create(
            title=data["title"],
            assigned_to=data.get("assigned_to_name", ""),
            project=data.get("project_title"),
            status=data.get("status", False),
        )

    # Pretty printing
    def __str__(self) -> str:
        project_name = self.project.title if self.project else "None"
        return f"Task(id={self.id}, title='{self.title}', assigned_to='{self.assigned_to}', project='{project_name}', done={self.status})"

    __repr__ = __str__
