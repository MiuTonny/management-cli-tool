import argparse
from models import User, Task, Project
from utils.helpers import save_all, load_all

# --- handlers ---
def add_user(args):
    # args.name, args.email
    existing = User.find_by_name(args.name) if hasattr(User, "find_by_name") else None
    if existing:
        print(f"ℹ️ User '{args.name}' already exists: {existing}")
        return
    u = User(args.name, args.email)
    print(f"✅ Created user: {u}")

def list_projects(args):
    projects = Project.all() if hasattr(Project, "all") else []
    if not projects:
        print("No projects found.")
        return
    print("Projects:")
    for p in projects:
        print(f"- {p}")

def complete_task(args):
    # args.user, args.title
    if not hasattr(User, "find_by_name"):
        print("User lookup not available.")
        return
    u = User.find_by_name(args.user)
    if not u:
        print(f"❌ User '{args.user}' not found.")
        return
    # your User class has get_task_by_title
    task = u.get_task_by_title(args.title)
    if not task:
        print(f"❌ Task '{args.title}' not found for user '{args.user}'.")
        return
    task.complete()
    print("✅ Task completion recorded.")

# --- CLI entry point ---
def main():
    # load at startup
    load_all()

    parser = argparse.ArgumentParser(description="Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add-user
    add_parser = subparsers.add_parser("add-user", help="Add a new user")
    add_parser.add_argument("name", help="User name")
    add_parser.add_argument("email", help="User email")
    add_parser.set_defaults(func=add_user)

    # list-projects
    list_projects_parser = subparsers.add_parser("list-projects", help="List all projects")
    list_projects_parser.set_defaults(func=list_projects)

    # complete-task
    complete_task_parser = subparsers.add_parser("complete-task", help="Mark a task as complete")
    complete_task_parser.add_argument("user", help="User name")
    complete_task_parser.add_argument("title", help="Task title")
    complete_task_parser.set_defaults(func=complete_task)

    args = parser.parse_args()

    try:
        args.func(args)
    finally:
        # save after every command
        save_all()

if __name__ == "__main__":
    main()

