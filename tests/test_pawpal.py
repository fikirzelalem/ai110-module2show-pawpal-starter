import sys
import os
import pytest
from datetime import datetime, date

# Ensure project root is on sys.path so tests can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pawpal_system import Owner, Pet, Task, Scheduler


def test_sort_by_time():
    owner = Owner(name="TestOwner", email="test@example.com", phone="123")
    pet = Pet(name="Buddy", species="dog", breed="Beagle", date_of_birth=date(2020, 1, 1))
    owner.add_pet(pet)

    task1 = Task(
        title="Walk",
        description="Morning walk",
        category="walk",
        scheduled_time=datetime(2026, 2, 15, 9, 0),
        priority="high",
    )
    task2 = Task(
        title="Feed",
        description="Breakfast",
        category="feeding",
        scheduled_time=datetime(2026, 2, 15, 8, 0),
        priority="medium",
    )

    pet.add_task(task1)
    pet.add_task(task2)

    scheduler = Scheduler()
    # scheduler manages tasks directly; add owner's tasks to scheduler
    for t in owner.get_all_tasks():
        scheduler.add_task(t)

    sorted_tasks = scheduler.sort_by_time()

    assert sorted_tasks[0].title == "Feed"
    assert sorted_tasks[1].title == "Walk"


def test_conflict_detection():
    owner = Owner(name="TestOwner", email="test@example.com", phone="123")
    pet = Pet(name="Buddy", species="dog", breed="Beagle", date_of_birth=date(2020, 1, 1))
    owner.add_pet(pet)

    task1 = Task(
        title="Walk",
        description="Morning walk",
        category="walk",
        scheduled_time=datetime(2026, 2, 15, 9, 0),
        priority="high",
    )
    task2 = Task(
        title="Feed",
        description="Breakfast",
        category="feeding",
        scheduled_time=datetime(2026, 2, 15, 9, 0),
        priority="medium",
    )

    pet.add_task(task1)
    pet.add_task(task2)

    scheduler = Scheduler()
    for t in owner.get_all_tasks():
        scheduler.add_task(t)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    # ensure both task titles are mentioned in the conflict message
    assert "Walk" in conflicts[0]
    assert "Feed" in conflicts[0]


def test_mark_complete():
    task = Task(
        title="Walk",
        description="Evening walk",
        category="walk",
        scheduled_time=datetime(2026, 2, 15, 18, 0),
        priority="high",
    )

    task.mark_complete()

    assert task.is_completed is True

def test_task_addition_to_pet():
    pet = Pet(
        name="Buddy",
        species="dog",
        breed="Beagle",
        date_of_birth=date(2020, 1, 1)
    )

    task = Task(
        title="Feed",
        description="Dinner",
        category="feeding",
        scheduled_time=datetime(2026, 2, 15, 18, 0),
        priority="medium",
    )

    initial_count = len(pet.tasks)
    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1


def test_recurring_task_auto_creation():
    """Test that marking a recurring task complete automatically creates the next occurrence."""
    pet = Pet(
        name="Buddy",
        species="dog",
        breed="Beagle",
        date_of_birth=date(2020, 1, 1)
    )

    # Create a daily recurring task
    recurring_task = Task(
        title="Daily Walk",
        description="Morning walk",
        category="walk",
        scheduled_time=datetime(2026, 2, 15, 8, 0),
        recurrence_days=1,  # Daily recurrence
        priority="high",
    )

    pet.add_task(recurring_task)

    scheduler = Scheduler()
    scheduler.add_task(recurring_task)

    # Initial state: 1 task in scheduler
    assert len(scheduler.all_tasks) == 1
    assert not recurring_task.is_completed

    # Complete the task (should auto-create next occurrence)
    new_task = scheduler.complete_task_and_reschedule(recurring_task.task_id, pet)

    # Verify original task is marked complete
    assert recurring_task.is_completed

    # Verify new task was created and added
    assert new_task is not None
    assert len(scheduler.all_tasks) == 2
    assert len(pet.tasks) == 2

    # Verify new task has correct properties
    assert new_task.title == "Daily Walk"
    assert new_task.scheduled_time == datetime(2026, 2, 16, 8, 0)  # Next day
    assert new_task.recurrence_days == 1
    assert not new_task.is_completed


def test_non_recurring_task_no_auto_creation():
    """Test that marking a non-recurring task complete does NOT create a new task."""
    scheduler = Scheduler()

    task = Task(
        title="One-time Task",
        description="Non-recurring",
        category="appointment",
        scheduled_time=datetime(2026, 2, 15, 10, 0),
        recurrence_days=0,  # No recurrence
        priority="medium",
    )

    scheduler.add_task(task)

    # Complete the task
    new_task = scheduler.complete_task_and_reschedule(task.task_id)

    # Verify no new task was created
    assert new_task is None
    assert len(scheduler.all_tasks) == 1
    assert task.is_completed
