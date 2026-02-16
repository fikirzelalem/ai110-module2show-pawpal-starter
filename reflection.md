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

During implementation, I refined my design to focus on the core scheduling behaviors that are required by the project. Initially, I considered adding more advanced features such as recurring tasks and additional metadata, however, I decided to simplify the system to keep the logic clean and aligned with the minimum requirements. This made the system easier to test and maintain while still demonstrating algorithmic scheduling behavior.


**c. What I changed**

- **Code:** Implemented class skeletons and basic logic in `pawpal_system.py` for `Owner`, `Pet`, `Task`, and `Scheduler` following the UML design.
- **Tests:** Updated `tests/test_pawpal.py` to match the current constructors and field names; tests now use `datetime` for `scheduled_time` and cover sorting by time, conflict detection, and `mark_complete()` behavior.
- **Doc:** Added this summary to `reflection.md` to document implementation choices and the collaboration with AI during design and refactoring.
- **Notes:** Tests include a small `sys.path` insertion for local test discovery; consider removing or replacing with a package-friendly import when publishing.

---
## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
