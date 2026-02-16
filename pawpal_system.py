from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, date, timedelta
from uuid import uuid4


@dataclass
class Task:
    """Represents a pet care task (feeding, walk, medication, appointment)."""
    title: str
    description: str
    category: str  # e.g., "feeding", "walk", "medication", "appointment"
    scheduled_time: datetime
    task_id: str = field(default_factory=lambda: str(uuid4())[:8])
    is_completed: bool = False
    recurrence_days: int = 0  # 0 = no recurrence, >0 = recurring every N days
    priority: str = "medium"  # "low", "medium", "high"

    def mark_complete(self) -> Optional['Task']:
        """Mark this task as completed.

        If the task is recurring (recurrence_days > 0), automatically creates
        and returns a new Task for the next occurrence.

        Returns:
            Optional[Task]: New task for next occurrence if recurring, None otherwise.
        """
        self.is_completed = True

        if self.recurrence_days > 0:
            next_time = self.get_next_occurrence()
            if next_time:
                # Create a new task with same properties but new scheduled time
                new_task = Task(
                    title=self.title,
                    description=self.description,
                    category=self.category,
                    scheduled_time=next_time,
                    recurrence_days=self.recurrence_days,
                    priority=self.priority
                )
                return new_task

        return None

    def mark_incomplete(self):
        """Mark this task as incomplete."""
        self.is_completed = False

    def is_overdue(self) -> bool:
        """Check if the task is overdue."""
        return not self.is_completed and self.scheduled_time < datetime.now()

    def get_next_occurrence(self) -> Optional[datetime]:
        """Get the next occurrence if task is recurring."""
        if self.recurrence_days == 0:
            return None
        return self.scheduled_time + timedelta(days=self.recurrence_days)


@dataclass
class Pet:
    """Represents a pet owned by an owner."""
    name: str
    species: str  # e.g., "dog", "cat", "rabbit"
    breed: str
    date_of_birth: date
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task for this pet."""
        self.tasks.append(task)

    def remove_task(self, task_id: str):
        """Remove a task by task ID."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def get_age(self) -> int:
        """Calculate and return the pet's age in years."""
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age


@dataclass
class Owner:
    """Represents a pet owner."""
    name: str
    email: str
    phone: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str):
        """Remove a pet by name."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_pets(self) -> List[Pet]:
        """Retrieve all pets owned by this owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """Manages and organizes tasks for the pet care system."""

    def __init__(self):
        """Initialize the scheduler with an empty task list."""
        self.all_tasks: List[Task] = []

    def add_task(self, task: Task):
        """Add a task to the scheduler."""
        self.all_tasks.append(task)

    def remove_task(self, task_id: str):
        """Remove a task by task ID."""
        self.all_tasks = [t for t in self.all_tasks if t.task_id != task_id]

    def sort_by_time(self) -> List[Task]:
        """Return tasks sorted by scheduled time."""
        return sorted(self.all_tasks, key=lambda task: task.scheduled_time)

    def sort_by_priority(self) -> List[Task]:
        """Sort tasks by priority (high > medium > low)."""
        priority_order = {"high": 3, "medium": 2, "low": 1}
        return sorted(
            self.all_tasks,
            key=lambda task: priority_order.get(task.priority, 0),
            reverse=True
        )

    def get_tasks_by_priority(self) -> List[Task]:
        """Return tasks sorted by priority (overdue first, then by category)."""
        # Separate overdue and non-overdue tasks
        overdue_tasks = [t for t in self.all_tasks if t.is_overdue()]
        other_tasks = [t for t in self.all_tasks if not t.is_overdue()]
        
        # Sort each group by priority
        overdue_tasks.sort(key=lambda t: {"high": 3, "medium": 2, "low": 1}.get(t.priority, 0), reverse=True)
        other_tasks.sort(key=lambda t: {"high": 3, "medium": 2, "low": 1}.get(t.priority, 0), reverse=True)
        
        return overdue_tasks + other_tasks

    def get_today_tasks(self) -> List[Task]:
        """Get all tasks scheduled for today."""
        today = date.today()
        return [
            t for t in self.all_tasks
            if t.scheduled_time.date() == today
        ]

    def detect_conflicts(self) -> List[str]:
        """Detect scheduling conflicts (e.g., overlapping tasks within same pet)."""
        warnings = []
        times_seen = {}

        for task in sorted(self.all_tasks, key=lambda t: t.scheduled_time):
            task_time = task.scheduled_time.time()
            if task_time in times_seen:
                warnings.append(
                    f"⚠️  Conflict detected at {task_time} between '{times_seen[task_time].title}' and '{task.title}'"
                )
            else:
                times_seen[task_time] = task

        return warnings

    def schedule_recurring_task(self, task: Task, recurrence_days: int):
        """Schedule a recurring task with a specified interval."""
        task.recurrence_days = recurrence_days
        self.add_task(task)

    def get_upcoming_tasks(self, days: int) -> List[Task]:
        """Get all tasks scheduled for the next N days."""
        today = date.today()
        end_date = today + timedelta(days=days)
        return [
            t for t in self.all_tasks
            if today <= t.scheduled_time.date() <= end_date
        ]

    def complete_task_and_reschedule(self, task_id: str, pet: Optional['Pet'] = None) -> Optional[Task]:
        """Mark a task complete and automatically create next occurrence if recurring.

        This method handles the complete workflow for recurring tasks:
        1. Finds the task by ID
        2. Marks it complete (which may create a new task)
        3. Adds the new task to the scheduler
        4. Optionally adds the new task to the pet's task list

        Args:
            task_id: The ID of the task to complete
            pet: Optional Pet object to add the new recurring task to

        Returns:
            Optional[Task]: The new recurring task if created, None otherwise
        """
        # Find the task in the scheduler
        task = next((t for t in self.all_tasks if t.task_id == task_id), None)

        if not task:
            return None

        # Mark complete (returns new task if recurring)
        new_task = task.mark_complete()

        # If a new recurring task was created, add it to scheduler and pet
        if new_task:
            self.add_task(new_task)
            if pet:
                pet.add_task(new_task)

        return new_task
