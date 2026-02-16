from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner
owner = Owner(name="Jordan", email="jordan@email.com", phone="123-456-7890")

# Create pets
dog = Pet(name="Mochi", species="dog", breed="Shiba Inu", date_of_birth=date(2020, 5, 10))
cat = Pet(name="Luna", species="cat", breed="Siamese", date_of_birth=date(2021, 8, 15))

# Add pets to owner
owner.add_pet(dog)
owner.add_pet(cat)

# Create tasks with different times
task1 = Task(
    title="Morning Walk",
    description="Take Mochi for a 20-minute walk",
    category="walk",
    scheduled_time=datetime.now().replace(hour=8, minute=0, second=0),
    priority="high"
)

task2 = Task(
    title="Feed Mochi",
    description="Give Mochi breakfast",
    category="feeding",
    scheduled_time=datetime.now().replace(hour=7, minute=30, second=0),
    priority="medium"
)

task3 = Task(
    title="Feed Luna",
    description="Give Luna breakfast",
    category="feeding",
    scheduled_time=datetime.now().replace(hour=7, minute=45, second=0),
    priority="high"
)

# Add tasks to pets
dog.add_task(task1)
dog.add_task(task2)
cat.add_task(task3)

# Create scheduler
scheduler = Scheduler()

# Add tasks from owner to scheduler
for task in owner.get_all_tasks():
    scheduler.add_task(task)

print("\n--- Today's Schedule (Sorted by Time) ---")
for task in scheduler.sort_by_time():
    print(f"{task.scheduled_time.strftime('%H:%M')} - {task.title} ({task.priority})")

print("\n--- Conflicts ---")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("No conflicts detected.")
