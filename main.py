import argparse
from models import User, Task, Project
from utils.helpers import save_all, load_all
from rich.console import Console

console = Console()

# handlers

def add_user(args):
    """Create a new user (name, email)."""
    existing = User.find_by_name(args.name)
    if existing:
        console.print(f"[yellow] User '{args.name}' already exists:[/yellow] {existing}")
        return
    u = User(args.name, args.email)
    console.print(f"[green] Created user:[/green] {u}")

def list_projects(args):
    """List all projects in the system."""
    projects = Project.all()
    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return
    console.print("[bold cyan]Projects:[/bold cyan]")
    for p in projects:
        console.print(f"• {p}")

def complete_task(args):
    """Mark a user's task (by title) as complete."""
    u = User.find_by_name(args.user)
    if not u:
        console.print(f"[red] User '{args.user}' not found.[/red]")
        return
    task = u.get_task_by_title(args.title)
    if not task:
        console.print(f"[red] Task '{args.title}' not found for user '{args.user}'.[/red]")
        return
    task.complete()
    console.print("[green] Task completion recorded.[/green]")

# create a project for a user
def create_project(args):
    """Create a project for a given user (title, optional description & due_date)."""
    u = User.find_by_name(args.user)
    if not u:
        console.print(f"[red] User '{args.user}' not found.[/red]")
        return
    p = u.create_project(args.title, description=args.description or "", due_date=args.due_date)
    console.print(f"[green] Created project:[/green] {p}")

# add a task to a user's project
def add_task(args):
    """Add a task (title) to an existing project owned by a given user."""
    u = User.find_by_name(args.user)
    if not u:
        console.print(f"[red] User '{args.user}' not found.[/red]")
        return
    t = u.add_task_to_project(args.title, args.project)
    if t:
        console.print(f"[green] Created task:[/green] {t}")

# CLI entry

def main():
    # Load data at startup
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

    #create-project
    cp = subparsers.add_parser("create-project", help="Create a project for a user")
    cp.add_argument("user", help="User name")
    cp.add_argument("title", help="Project title")
    cp.add_argument("--description", default="", help="Project description")
    cp.add_argument("--due-date", dest="due_date", default=None, help="Due date YYYY-MM-DD")
    cp.set_defaults(func=create_project)

    #add-task
    at = subparsers.add_parser("add-task", help="Add a task to a user's project")
    at.add_argument("user", help="User name")
    at.add_argument("project", help="Project title")
    at.add_argument("title", help="Task title")
    at.set_defaults(func=add_task)

    args = parser.parse_args()

    try:
        args.func(args)
    finally:
        # Save after every command
        save_all()

if __name__ == "__main__":
    main()

