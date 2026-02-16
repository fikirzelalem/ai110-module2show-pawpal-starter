


from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner
owner = Owner(name="Jordan")

# Create pets
dog = Pet(name="Mochi", species="dog")
cat = Pet(name="Luna", species="cat")

# Add pets to owner
owner.add_pet(dog)
owner.add_pet(cat)

# Create tasks
task1 = Task(title="Morning Walk", duration_minutes=20, priority="high", time="08:00")
task2 = Task(title="Feed Mochi", duration_minutes=10, priority="medium", time="07:30")
task3 = Task(title="Feed Luna", duration_minutes=5, priority="high", time="07:30")

# Add tasks to pets
dog.add_task(task1)
dog.add_task(task2)
cat.add_task(task3)

# Create scheduler
scheduler = Scheduler(owner)

print("---- Sorted by Time ----")
for task in scheduler.sort_by_time():
    print(f"{task.time} - {task.title} ({task.priority})")

print("\n---- Sorted by Priority ----")
for task in scheduler.sort_by_priority():
    print(f"{task.title} - {task.priority}")

print("\n---- Conflict Detection ----")
for warning in scheduler.detect_conflicts():
    print(warning)
