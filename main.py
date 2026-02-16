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

print("\n--- Testing Recurring Tasks ---")
# Create a daily recurring task
recurring_task = Task(
    title="Daily Medication",
    description="Give Mochi daily medication",
    category="medication",
    scheduled_time=datetime.now().replace(hour=9, minute=0, second=0),
    recurrence_days=1,  # Daily recurrence
    priority="high"
)

dog.add_task(recurring_task)
scheduler.add_task(recurring_task)

print(f"Created recurring task: '{recurring_task.title}' at {recurring_task.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
print(f"  - Recurrence: Every {recurring_task.recurrence_days} day(s)")
print(f"  - Task ID: {recurring_task.task_id}")

# Mark the recurring task complete (should auto-create next occurrence)
print(f"\nMarking '{recurring_task.title}' as complete...")
new_task = scheduler.complete_task_and_reschedule(recurring_task.task_id, dog)

if new_task:
    print(f"✓ Task completed! New occurrence auto-created:")
    print(f"  - Next occurrence: {new_task.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"  - New Task ID: {new_task.task_id}")
    print(f"  - Added to scheduler and pet's task list")
else:
    print("Task completed (no recurrence)")

# Show updated schedule
print("\n--- Updated Schedule (with recurring task) ---")
for task in scheduler.sort_by_time():
    status = "✓ Complete" if task.is_completed else "Pending"
    recur = f" (Recurs every {task.recurrence_days} days)" if task.recurrence_days > 0 else ""
    print(f"{task.scheduled_time.strftime('%Y-%m-%d %H:%M')} - {task.title} [{status}]{recur}")
