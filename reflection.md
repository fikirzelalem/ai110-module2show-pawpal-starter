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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

My conflict detection algorithm only checks for exact time matches (e.g., two tasks both scheduled at 9:00 AM) rather than detecting overlapping durations.

For example, if one task is scheduled at 9:00 AM for 30 minutes and another at 9:15 AM, my system won't flag this as a conflict even though they overlap in real time.

This tradeoff is reasonable for PawPal+ because:
1. The Task class doesn't include a duration field, only a scheduled_time
2. Checking exact time matches is simple (O(n log n)) and catches the most obvious scheduling conflicts
3. For a pet care app, owners can mentally manage minor overlaps between activities
4. Adding duration-based overlap detection would require restructuring the Task class and implementing O(n²) comparison logic, which adds complexity without much benefit for this use case

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
