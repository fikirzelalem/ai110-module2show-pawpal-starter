# PawPal+ Project Reflection

## 1. System Design
### Core User Actions

1. Add a pet to the system.
2. Schedule a task (feeding, walk, medication) for a pet.
3. View a sorted daily schedule of the tasks.

**a. Initial design**

My initial UML design included four main classes: Owner, Pet, Task, and Scheduler.

The Owner class stores the owner’s name and the list of pets. It is responsible for adding pets and retrieving all of the tasks across each pets.

The Pet class stores a pet’s name and the species, along with a list of the tasks. It is responsible for adding new tasks and retrieving its tasks.

The Task class represents a single care activity. It stores the title, the duration in minutes, its priority level, the scheduled time, and the completion status. It includes a method to mark a task as complete.

The Scheduler class acts as the system’s logic layer. It retrieves tasks from the Owner and provides functionality to sort tasks by time, sort tasks by priority, and it detects if there are any scheduling conflicts.

This specific structure separates responsibilities clearly and follows object oriented design principles.

**b. Design changes**

During implementation, I refined my design to focus on the core scheduling behaviors that are required by the project. 
Copilot suggested linking Task to Pet and improving conflict detection to handle overlapping durations. I evaluated these suggestions but chose not to implement them because the current design satisfies the project requirements and tests pass. I documented these as potential future improvements.
Initially, I considered adding more advanced features such as recurring tasks and additional metadata, however, I decided to simplify the system to keep the logic clean and aligned with the minimum requirements. This made the system easier to test and maintain while still demonstrating algorithmic scheduling behavior.


**c. What I changed**

- **Code:** I implemented class skeletons and basic logic in `pawpal_system.py` for `Owner`, `Pet`, `Task`, and `Scheduler` following the UML design.
- **Tests:** I updated `tests/test_pawpal.py` to match the current constructors and field names; tests now use `datetime` for `scheduled_time` and cover sorting by time, conflict detection, and `mark_complete()` behavior.
- **Doc:** I then added this summary for implementation choices and the collaboration with Copilot AI during design and refactoring.


---
## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers three main constraints:

1. **Time** - The tasks are organized by scheduled_time (datetime) to help owners see what happens next chronologically
2. **Priority** - the tasks have priority levels (low, medium, high) to ensure critical activities like medication not being missed
3. **Recurrence** - The tasks can repeat daily or on custom intervals, automating routine care activities

**How I decided which constraints mattered most:**

I prioritized **time** as the primary constraint because pet care is time sensitive (eg. morning walks, feeding schedules, medication windows). The `sort_by_time()` method provides the foundation for daily planning.

**Priority** became the secondary constraint after analyzing the scenario: some tasks (medication and vet appointments) are more critical than others (playtime, grooming). The `get_tasks_by_priority()` method elevates overdue high-priority tasks to the top.

I did NOT implement constraints like "owner availability windows" or "pet preferences" because the assignment focused on demonstrating algorithmic logic with the core OOP classes (Owner, Pet, Task, Scheduler) and these features would require additional complexity beyond the project scope.

**b. Tradeoffs**

My conflict detection algorithm only checks for exact time matches (e.g., two tasks both scheduled at 9:00 AM) rather than detecting overlapping durations.
For example, if one task is scheduled at 9:00 AM for 30 minutes and another at 9:15 AM, my system won't flag this as a conflict even though they overlap in real time.

This tradeoff is reasonable for PawPal+ because
1. The Task class doesn't include a duration field but only a scheduled_time
2. Checking exact time matches is simple (O(n log n)) and catches the most obvious scheduling conflicts
3. For a pet care app, the owners can manage minor overlaps between activities
4. Adding duration based overlap detection would require restructuring the Task class and implementing O(n²) comparison logic, which adds complexity without much benefit for this usecase

---

## 3. AI Collaboration

**a. How you used AI**

I used VS Code Copilot throughout the project in different modes:

**Design Phase:**
- Used Copilot Chat to brainstorm the initial UML class structure
- Asked for help translating UML into Python dataclass skeletons
- Requested Mermaid.js diagram suggestions for visualizing class relationships

**Implementation Phase:**
- Used Inline Chat to implement sorting algorithms with lambda functions
- Asked Copilot to explain how to use `timedelta` for calculating recurring task dates
- Used Agent Mode to help structure the recurring task automation logic

**Testing Phase:**
- Used "Generate tests" smart action to draft initial test cases
- Asked Copilot to explain pytest assertions that I didn't understand
- Used Chatgpt to identify edge cases I should test

**Most helpful prompts:**
- "Based on #file:pawpal_system.py, suggest a test plan for the scheduler"
- "How can I use a lambda function to sort tasks by scheduled_time?"
- "Explain why this test is failing and whether the bug is in my test or in my logic"

**b. Judgment and verification**

When implementing conflict detection, Copilot initially suggested tracking task durations and checking for overlapping time ranges (e.g., a 30-minute walk from 9:00-9:30 overlapping with 9:15 feeding).

**I rejected this suggestion** because:
1. My Task class doesn't have a duration field
2. Duration-based overlap detection would require O(n²) comparisons
3. For a pawpal, exact time matching catches the most obvious conflicts without added complexity

**How I evaluated it:**
I asked Copilot to compare the complexity tradeoffs between "exact time matching" vs "duration overlap detection." After seeing that duration detection would require restructuring my Task class and implementing nested loops, I decided the simpler approach was better aligned with the project requirements and my current architecture.

Starting a new chat session for each phase (for Designing, Implementation, and Testing) helped me stay focused and prevented Copilot from suggesting solutions from earlier contexts that no longer applied to the current one.
---

## 4. Testing and Verification

**a. What you tested**

I tested six core behaviors in the PawPal+ system:

1. **Sorting by Time** - this verifies tasks are ordered chronologically which is essential for owners to see what needs to happen next
2. **Conflict Detection** - this mmakes sure that the scheduler flags tasks scheduled at the same time which prevents double booking
3. **Task Completion** - Confirms the `mark_complete()` method properly updates task status
4. **Task Addition to Pets** - Validates that adding tasks correctly increases a pet's task count
5. **Recurring Task Automation** - Tests that completing a daily task automatically creates the next occurrence
6. **Non-Recurring Task Behavior** - Ensures one-time tasks don't duplicate when marked complete

These tests are important because they verify the "brain" of the scheduling system. If sorting or conflict detection fails, the entire app becomes unreliable. The recurring task tests are critical because they validate the most complex algorithmic feature.

**b. Confidence**

I am **very confident (4/5 stars)** that my scheduler works correctly for the core workflows.

All six tests pass consistentlyy, and I've verified the behavior through both automated tests and the CLI demo script (`main.py`). The Streamlit UI successfully integrates with the backend logic.

**Edge cases I would test next:**

1. **Empty task lists** - What happens when a pet has no tasks or the scheduler is empty?
2. **Invalid task IDs** - How does `complete_task_and_reschedule()` handle a task ID that doesnt exist?
3. **Multiple pets with overlapping tasks** - Does conflict detection work across different pets?
4. **Tasks scheduled in the past** - How does the system handle overdue tasks that are weeks old?
5. **Weekly/monthly recurrence** - Testing recurring tasks with `recurrence_days=7` or `recurrence_days=30`

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the **recurring task automation feature**. The design is clean that `Task.mark_complete()` returns a new task if recurring, and `Scheduler.complete_task_and_reschedule()` handles the workflow automatically. This separation of concerns keeps the Task class simple while giving the Scheduler the intelligence to manage recurring tasks.

The CLI-first workflow (building `main.py` before connecting to Streamlit) was also very effective. It let me verify the logic worked correctly before dealing with UI state management which made debugging so much easier.

**b. What you would improve**

I would

1. **Add data persistence** - Save Owner, Pet, and Task data to JSON so the app remembers data between sessions
2. **Improve conflict detection** - Add a "suggested reschedule time" feature that finds the next available slot when conflicts are detected
3. **Implement duration tracking** - Add a duration field to tasks and calculate true overlapping conflicts
4. **Enhance the UML diagram** - Create a final visual diagram showing the actual method signatures and relationships

**c. Key takeaway**

The most important thing I learned is that **AI is a thought partner and not a replacement for architectural decisions.**

Copilot was good at generating codes for me, suggesting algorithms, and drafting tests but when it came to designing tradeoffs (like exact-time vs. duration based conflict detection), I had to be the "lead architect" and make the calls based on the project requirements, complexity tradeoffs, and my existing class structure.

