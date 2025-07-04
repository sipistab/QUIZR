
## **Introduction**

This program is a command-line interface (CLI) tool designed to quiz users based on either textual or image prompts. It emphasizes clarity of definition, precise user responses, and long-term retention through spaced repetition. Users can interact entirely from the terminal environment and manage the files simply by editing them with a text editor or adding files to the folder.

### Data Model and Content Management

#### 1. Folder-Based Structure

Questions are grouped into named folders. Each folder acts as a logical unit or topic area. Folders can contain other folders or individual quiz items. This structure allows users to focus on specific subjects or skill sets by selecting a folder to practice from.
ew
#### 2. Question Entry Format

Each quiz item should include the following fields:

- `prompt`: a string of text displaying the question.
- `answer`: a string representing the expected correct answer.
-  `iamge`: a string representing the filename of the image to be opened from /images.

  ```yaml
# Port_Numbers.yaml
# Quiz items for the topic "Port Numbers" in Network+

q_000:
  prompt: "What is the default port number for HTTP?"
  answer: "80"
  strict: true #indicating if fuzzy should be enabled, if this is present, no fuzzy, if stict is not set, fuzzy is on.

q_001:
  prompt: "What is the default port for HTTPS?"
  answer: "443"
  strict: true

q_002:
  image: "network_diagram.png"        # Image located in /images/
  prompt: "Which port does the SSH service use in this diagram?"
  answer: "22"

q_003:
  prompt: "Name the protocol that uses port 53."
  answer: "DNS"

q_004:
  image: "phishing_example.png"
  prompt: "Which port is commonly exploited in this attack vector?"
  answer: "445"

q_005:
  prompt: "Which port is used by SMTP?"
  answer: "25"
  yaml```

The quiz data can be stored in YAML files. One file for each quiz.

### Quiz Logic and Execution

#### 1. Prompt Display

For text prompts, the content is printed directly in the terminal.  
For image prompts, the image is opened using the system’s default image viewer, while the program waits for input, just like when there is no image. The logic is always, first print the prompt then show the image and await for answer string.

#### 2. User Input and Evaluation

After viewing the prompt, the user enters a response in the terminal. The response is compared against the expected answer using exact or fuzzy matching, depending on configuration. The program records whether the response was correct or incorrect and updates the item’s review metadata accordingly. If the user has   strict: true, that means the fuzzy is not used. Fuzzy is 90% and should be tweaked by the config file.

#### 3. Spaced Repetition Logic

Each question is scheduled for review based on spaced repetition principles. An algorithm such as SM-2 or a simplified Leitner system is used to determine the `next_due_date` based on:

- Performance history for the question
- Time since last review
- Number of successful attempts

Only questions that are "due" should be presented during normal review sessions unless the user explicitly requests otherwise.

### Progress Tracking and Reporting

#### 1. Folder-Level Metrics

Each folder should report:

- Total number of questions in folders/exercises
- Number of questions seen
-  Number of questions answered correctly
- Percentage of questions completed

Store all progress data in a single centralized file like `progress.yaml` in the root folder to simplify management, aggregation, and persistence.

#folderOutputExample
Root/
├── images/
│   ├── network_diagram.png
│   ├── phishing_example.png
│   └── hardware_photo.png
└── CompTIA/
    ├── Network+/
    │   ├── Port_Numbers.yaml
    │   ├── Network_Definitions.yaml
    │   └── Protocols.yaml
    ├── Security+/
    │   ├── Threats.yaml
    │   ├── Cryptography.yaml
    │   └── Risk_Management.yaml
    └── A+/
        ├── Hardware.yaml
        ├── Operating_Systems.yaml
        └── Troubleshooting.yaml

Details:

- Each topic folder (e.g., Network+) can contain multiple YAML files.
- Each YAML file corresponds to a specific exercise or drill category (e.g., Port_Numbers.yaml).
- This removes the extra folder layer and keeps the structure flat and simple.
- All quiz data for that category is inside its respective YAML file.
- Images are still centralized in the root-level images/ folder.
- - In the YAML files, image prompts will only store the image file name, for example:

  ```yaml
  prompt: "Identify this attack type from the image"
  type: image
  image: phishing_example.png
  answer: "Phishing"
  yaml```
  
The program’s logic will automatically prepend or resolve the fixed root images/ folder path internally when loading images. Do not print the file name in the CLI, additionally, file names should be not as descriptive as the example, as user will be able to tell the answer, so it should rather be ExersizeX_Q1.png

This means no relative paths need to be stored in YAML, simplifying data entry and reducing errors.
If the program fails to find the image in the root images/ folder, it will:

	Log a clear error message to the console indicating the missing image and the question it belongs to.

#### 2. Global Metrics

Across all folders, the program should track:

- Total questions and reviews
- Aggregate completion percentage
- Daily activity log
- Historical error rate

All metrics should be available through a command in the CLI and optionally written to a log or stats file.

Example:
 ```yaml
__meta__:
  total_questions_seen: 45
  total_reviews: 102
  first_use: 2025-06-20
  last_session: 2025-06-25
  daily_log:
    2025-06-24: 32
    2025-06-25: 18

CompTIA:
  Network+:
    Port_Numbers.yaml:
      q_000:
        attempts: 3
        correct: 2
        last_review: 2025-06-25
        last_correct: 2025-06-23
      q_001:
        attempts: 1
        correct: 0
        last_review: 2025-06-25
      q_002:
        attempts: 0
        correct: 0
    Network_Definitions.yaml:
      q_000:
        attempts: 2
        correct: 2
        last_review: 2025-06-24
        last_correct: 2025-06-24
  Security+:
    Threats.yaml:
      q_000:
        attempts: 4
        correct: 3
        last_review: 2025-06-25
        last_correct: 2025-06-25
         yaml```
Example, commented:
 ```yaml
__meta__:                         # Global metadata for tracking user-wide progress stats
  total_questions_seen: 45       # Total number of unique questions attempted at least once
  total_reviews: 102             # Total number of question attempts, including repeats (correct or not)
  first_use: 2025-06-20          # Date the program was first run by the user
  last_session: 2025-06-25       # Timestamp of the most recent review session
  daily_log:                     # Optional tracking of review activity per date
    2025-06-24: 32               # On June 24, 32 questions were reviewed
    2025-06-25: 18               # On June 25, 18 questions were reviewed

CompTIA:                         # Root topic/folder grouping
  Network+:                      # Subtopic or course section (folder in filesystem)
    Port_Numbers.yaml:           # Specific YAML file under Network+ (an exercise category)
      q_000:                     # Question ID within the YAML file
        attempts: 3              # Number of times this question has been shown to the user
        correct: 2              # Number of times the user answered it correctly
        last_review: 2025-06-25  # Last time the question was shown (correct or incorrect)
        last_correct: 2025-06-23 # Last time the question was answered correctly
      q_001:
        attempts: 1
        correct: 0
        last_review: 2025-06-25 # Incorrect answer, so no last_correct recorded
      q_002:
        attempts: 0             # Not yet shown to the user
        correct: 0              # Still unattempted (correct is technically zero)
    Network_Definitions.yaml:
      q_000:
        attempts: 2
        correct: 2
        last_review: 2025-06-24
        last_correct: 2025-06-24

  Security+:
    Threats.yaml:
      q_000:
        attempts: 4
        correct: 3
        last_review: 2025-06-25
        last_correct: 2025-06-25
     yaml```
### CLI Command System

The program should accept the following commands from the terminal. Each command should be accompanied by clear, structured help output.

- `list`  
  Lists all available folders containing question sets.

- `start [folder_name]`  or  `start [file_name]`
  Begins a review session for the specified folder  or specified exercise file. All items are included by default. Have three variables shuffle, quick and spaced, default is spaced. Spaced is spaced repetition, starting by the empty or oldest reviewed items going up to the youngest correctly answered. 
 
- `progress [folder_name]`  
  Displays metrics for a specific folder or file, based on global metrics.

- `!quit` or `!abort`  
  Ends the current session immediately. Shows the results of current session. Time spent, questions answered. Wrong questions and answers are printed by folder.

### Storage and Persistence

The system must store all user data persistently. 
- File-based: each folder is a directory containing individual YAML files per question.
### Optional Features

The following features may be considered for future versions:

- Fuzzy answer matching with 90% threshold.
- Support for multiple correct answers per question.
- Configurable scoring system and weighting of question difficulty.
- Import/export of folders and question sets in a standard format.
- Tag-based filtering and searching within folders.
- Multi-user profiles and progress separation.
- Notification system for reminders or scheduled reviews.

### Summary

This is a terminal-first, image- and text-based drill and recall system. It combines precision testing, flexible organization, and intelligent review scheduling. The design emphasizes clarity, extensibility, and full user control over data and session management. The interface must remain responsive and self-explanatory, relying entirely on CLI commands for interaction.



## **Start-up / Menu**


 On launch, the program enters an idle state, displaying a static set of available commands:

 LIST | START | MANAGE | PROGRESS | QUIT

 No action is taken until the user enters one of these commands. Each command corresponds to a core function of the program and leads into a specific operational mode.

---

### LIST

 This command inspects the root data directory. It identifies folders and their contained exercises. These exercises are the basic units of review. The output is organized hierarchically. This command does not perform any action beyond visual inspection. It prepares the user to target a folder or exercise for further commands. It just sends #folderOutputExample

---

### START

 This command launches a review session. It expects a path-like argument that points to a valid folder or exercise. Once invoked, the program loads the data structure associated with the argument. Prompts are filtered for readiness using spaced repetition criteria. Prompts are then delivered sequentially. If a prompt is an image, the system opens it using the default viewer and pauses. If the prompt is text, it is shown directly in the terminal. The user responds with an exact text input. The program checks this input for correctness and logs the outcome. The repetition schedule is updated based on success or failure. The session ends when all relevant prompts are exhausted or the user enters a stop command.
Session Duration starts when start command is sent correctly and exercise started, when the session ends in abort, quit or by finishing the last question this variable will be used for result screen.

Example:
`start comptia` --> will start all exercises in: 
└── CompTIA/
    ├── Network+/
    │   ├── Port_Numbers.yaml
    │   ├── Network_Definitions.yaml
    │   └── Protocols.yaml
    ├── Security+/
    │   ├── Threats.yaml
    │   ├── Cryptography.yaml
    │   └── Risk_Management.yaml
    └── A+/
        ├── Hardware.yaml
        ├── Operating_Systems.yaml
        └── Troubleshooting.yaml
`start network+` ---> will strart: 
    │   ├── Port_Numbers.yaml
    │   ├── Network_Definitions.yaml
    │   └── Protocols.yaml
`start Port_Numbers` --> will only start Port_Numbers.yaml


This command takes three arguments: 'shuffle'; 'quick' and 'spaced'

shuffle will randomize the question ID-s, so that questions does not come in the same sequence every time. 

quick will select 10 questions at random from the selection and ask only those

spaced will apply spaced repetition - this is the only argument that passes the spaced repetition results forward, the rest need only be logged into their own tracking files.

example syntax1:  start network+ spaced
example syntax2: start comptia quick

---

### PROGRESS

 This command displays learning metrics. It supports arguments targeting a specific folder, a specific exercise, or the global dataset. The intent is diagnostic. It does not modify data. It reports on completion rates, error rates, and history. For folders, this command aggregates data across all exercises. For exercises, it limits scope to a single prompt set. Global mode performs a full scan and aggregation across all stored content.

Examples:

 `progress` or `progress global` --> default is global if simply typed progress  
  ```yaml
Progress: All Topics
----------------------------------------------------
Total Folders         : 3
Total Exercises       : 9
Total Questions       : 204
Questions Seen        : 158 (77.5%)
Correct Answers       : 129
Accuracy Rate         : 81.9%
Streak (days)         : 5
First Use Date        : 2025-06-20
Last Session Date     : 2025-06-25
Active Day Streak     : 6
----------------------------------------------------
This month
Total Questions       : 6
Total Correct Answers : 6
----------------------------------------------------
yaml```

 `progress Network+` 
   ```yaml
Progress: CompTIA/Network+/
----------------------------------------------------
Total Exercises       : 3
Total Questions       : 71
Questions Answered    : 53 (74.6%)
Correct Answers       : 42
Accuracy Rate         : 79.2%
Last Session Date     : 2025-06-25
----------------------------------------------------
Exercises:
  • Port_Numbers.yaml         — 68% seen | 82.3% answered correctly
  • Network_Definitions.yaml  — 87.5% seen | 78.0% answered correctly
  • Protocols.yaml            — 68% seen | 77.0% answered correctly
----------------------------------------------------
yaml```

`progress Port_Numbers` 
   ```yaml
Progress: CompTIA/Network+/Port_Numbers.yaml
----------------------------------------------------
Total Questions       : 25
Questions Answered    : 17 (68%)
Correct Answers       : 14
Accuracy Rate         : 82.3%
Correct Answer Rate   : 82.3%
Last Session Date     : 2025-06-25
Last Question Answered: q_016
First Seen Date       : 2025-06-20
----------------------------------------------------
yaml```
---
### QUIT

 This command exits the program. It is available from any state and terminates all active processes. Before quitting, the program flushes any unsaved state and closes resources. There is no autosave on crash or external sync.

   ```yaml
Exercise Complete: CompTIA/Network+/
====================================================
Mode                  : spaced
Total Exercises       : 3
Total Questions       : 71
Questions Attempted   : 30
Correct Answers       : 26
Correct Answers %     : 86.7%
Session Duration      : 00:18:07

Exercises Reviewed:
  • Port_Numbers.yaml         — 10/25 | correct answer % = 80.0%
  • Network_Definitions.yaml  — 12/26 | correct answer % = 91.7%
  • Protocols.yaml            — 8/20  | correct answer % = 87.5%

----------------------------------------------------
Note: If the mode is not `quick`, all questions are expected to be reviewed unless the session was aborted early. The above example session, was a group and was aborted early. 
yaml```

   ```yaml
Exercise Complete: CompTIA/Network+/Port_Numbers.yaml
====================================================
Mode                  : quick
Total Questions       : 25
Questions Attempted   : 10
Correct Answers       : 8
Correct Answers %     : 80.0%
Session Duration      : 00:06:23

----------------------------------------------------
Note: In `quick` mode, only a subset of questions is attempted. The session ended by answering the last question, completing the exercise.
yaml```
---

### Additional Notes

 All prompts and progress data are stored locally in a structured format. This can be either a database or flat files. Prompts are atomic and versioned by timestamp. Every modification is logged. There is no network dependency. The user has full ownership of their data. All program logic is deterministic and traceable. No operations involve randomness or opaque scheduling. All state transitions are logged, inspectable, and reversible if required.

 The interface is intended to be stable, scriptable, and extensible. All output is formatted for readability and parsability. No styling, color, or animation is used. The purpose is mastery, not stimulation.
