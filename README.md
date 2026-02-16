# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

PawPal+ includes intelligent algorithmic features to help pet owners manage their pets' care routines:

### Core Features

**📊 Sorting & Filtering**
- **Sort by Time**: Tasks are organized chronologically to see what needs to happen next
- **Sort by Priority**: High-priority tasks (medication, appointments) are displayed first
- **Filter by Status**: View only pending tasks or see completed tasks for the day
- **Filter by Date Range**: See upcoming tasks for the next N days

**⚠️ Conflict Detection**
- Automatically detects when two tasks are scheduled at the exact same time
- Displays clear warning messages to help owners reschedule conflicting tasks
- Uses efficient O(n log n) algorithm with time-based hash lookup

**🔄 Recurring Task Automation**
- Daily, weekly, or custom interval task support
- When a recurring task is marked complete, the next occurrence is automatically created
- Maintains all task properties (priority, category, description) for the new occurrence
- Seamlessly adds new tasks to both the scheduler and pet's task list

**🎯 Priority-Based Scheduling**
- Tasks are categorized by priority levels: Low, Medium, High
- Overdue tasks are automatically surfaced to the top of the schedule
- Helps owners focus on the most important care activities first

### Technical Implementation

The scheduling logic is powered by the `Scheduler` class in `pawpal_system.py`, which provides:
- Efficient task sorting and filtering algorithms
- Lightweight conflict detection without complex overlap calculations
- Automatic recurring task generation through the `complete_task_and_reschedule()` method

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

### Running Tests

To run the automated test suite:

```bash
python -m pytest
```

For verbose output with test names:

```bash
python -m pytest -v
```

### Test Coverage

The test suite verifies the following core behaviors:

✅ **Sorting Correctness** (`test_sort_by_time`): Ensures tasks are returned in chronological order

✅ **Conflict Detection** (`test_conflict_detection`): Verifies that tasks scheduled at the same time are flagged

✅ **Task Completion** (`test_mark_complete`): Confirms that marking a task complete updates its status correctly

✅ **Task Addition** (`test_task_addition_to_pet`): Validates that adding tasks to pets increases their task count

✅ **Recurring Task Automation** (`test_recurring_task_auto_creation`): Verifies that completing a recurring task automatically creates the next occurrence

✅ **Non-Recurring Task Behavior** (`test_non_recurring_task_no_auto_creation`): Ensures one-time tasks don't duplicate when completed

### Confidence Level

**⭐⭐⭐⭐ (4/5 stars)** - The system's core scheduling logic is reliable and tested.

The test suite covers the most critical workflows (sorting, conflicts, recurring tasks) and all 6 tests pass consistently. Edge cases like empty task lists, invalid task IDs, and timezone handling would be tested next with more time.
