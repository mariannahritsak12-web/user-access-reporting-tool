## User Access Reporter

This tool parses system logs to generate a comprehensive audit of user activity. It tracks which users are active on specific machines within a defined time window and calculates the total duration of completed sessions.

### Core functionality
* **Chronological audit:** processes machine logins and logouts in order of occurance 
* **Session Durations:** Calculates total time spent active on each machine

### Key enhancements
* **Audit logic** - tracks historical state to show everyone who accessed the system
* **Duration tracking** - implemented to report total active time per user
* **Error handling** - uses try-except blocks and collections defualtDict module to handle dirty data gracefully
* **Formatted output** - generated a structured .txt report 

### Usage
`python3 script.py`
**Input:** `events.csv` | **Output:** `user_access_report.txt`

---
## Background
This project originated as final assignments in the **Google IT Automation professional certificate** on Coursera
  
> **Note:** this version have been significantly refactored and optimized.
