from models import User, Project, Task
from utils.helpers import save_all, load_all

u = User("Carlos", "Carlos@example.com")
p = u.create_project("CLI Tool", "Management CLI project", "2025-11-15")
u.add_task_to_project("Add argparse commands", "CLI Tool")

save_all()
load_all()

print(User.all())
print(Project.all())
print(Task.all())
