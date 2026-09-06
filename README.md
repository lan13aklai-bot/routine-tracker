# Daily Routine Tracker 🎯

A comprehensive Python command-line application to help structure daily habits, track progress, and build productive routines. Perfect for students and professionals managing multiple daily routines.

## Features ✨

### Core Functionality
- ✅ **Task Completion Tracking** - Mark tasks as done/incomplete with real-time checkboxes
- 💾 **Persistent Storage** - Save all data to JSON files (survives between sessions)
- 🔄 **Daily Auto-Reset** - Tasks automatically reset each day for fresh starts
- 🎨 **Color-Coded Output** - Visual distinction between priorities and completion status

### Interactive Management
- 📋 **Interactive Menu System** - Easy navigation with numbered options
- ➕ **Add/Edit Routines** - Create custom routines for different parts of your day
- ✏️ **Dynamic Task Management** - Add and remove tasks on the fly
- 🔍 **Search Functionality** - Find specific tasks across all routines

### Progress & Analytics
- 📊 **Completion Statistics** - View daily/routine completion percentages
- 🔥 **Streak Counter** - Track consecutive days of 100% completion
- 📈 **Activity Logging** - Historical log of all completed tasks with timestamps
- 📄 **Progress Reports** - Generate detailed reports and export to file

### Advanced Features
- ⏰ **Time Tracking** - Estimate and track actual time spent on each task
- 🚨 **Priority Levels** - Mark tasks as high/medium/low priority
- 🕐 **Scheduled Routines** - Set specific times for routines to remind you
- 💻 **Command-Line Arguments** - Run actions directly from terminal
- 📑 **PDF/Text Exports** - Save reports for record-keeping

## Default Routines

The app comes with three pre-configured routines:

### 🌅 Morning Routine
- Review daily tasks (10 min) - HIGH priority
- Pack school bag (15 min) - HIGH priority
- 30-min reading (30 min) - MEDIUM priority

### 📚 Study Routine
- Complete homework (60 min) - HIGH priority
- Review class notes (30 min) - MEDIUM priority
- Practice problems (45 min) - MEDIUM priority

### 🌙 Evening Routine
- Organize study desk (15 min) - LOW priority
- Log daily achievements (10 min) - MEDIUM priority
- Set phone to Do Not Disturb (5 min) - HIGH priority

## Installation

### Prerequisites
- Python 3.6+
- `colorama` library for colored terminal output

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lan13aklai-bot/routine-tracker.git
   cd routine-tracker
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install colorama
   ```

## Usage

### Running the Interactive Menu
```bash
python main.py
```

This launches the interactive menu where you can:
- View all routines
- Mark tasks complete
- Add/remove routines
- Add/remove tasks
- Search for tasks
- View statistics
- Generate reports

### Command-Line Arguments

Run specific actions directly from the terminal:

```bash
# Complete all tasks in a routine
python main.py complete morning

# View a specific routine
python main.py view evening

# Display statistics
python main.py stats
```

## File Structure

```
routine-tracker/
├── main.py                    # Core application
├── README.md                  # This file
├── routine_data.json          # Saved routines (auto-generated)
├── completion_data.json       # Today's task status (auto-generated)
├── routine_log.json           # Historical activity log (auto-generated)
└── routine_report_YYYY-MM-DD.txt  # Exported reports (generated on demand)
```

## How to Use - Step by Step

### 1. View Your Routines
Select option **1** from the menu to see all routines with their tasks, time estimates, priorities, and scheduled times.

### 2. Mark Tasks Complete
- Select option **2**
- Choose a routine
- Select the task you completed
- Enter the time you spent on it
- Task is marked complete ✓

### 3. Customize Your Routines
- **Add a new routine:** Option 3 (great for workout, meal prep, hobby time)
- **Add a task:** Option 5 (include time estimate, priority, and scheduled time)
- **Remove a task:** Option 6
- **Remove a routine:** Option 4

### 4. Search for Tasks
Select option **7** and type part of a task name to find it instantly across all routines.

### 5. Track Your Progress
- **View Statistics:** Option 8 to see completion %, time spent, and streak
- **View Activity Log:** Option 9 to see all completed tasks from today
- **Export Report:** Option 10 to save a text file of your progress

## Example Workflow

```
1. Open the app: python main.py
2. View routines (Option 1)
3. Mark tasks complete (Option 2) as you finish them
4. Check statistics (Option 8) at the end of the day
5. Export report (Option 10) for record-keeping
6. Tomorrow, repeat!
```

## Data Persistence

All your data is automatically saved to JSON files:

- **routine_data.json** - Your routines and their tasks
- **completion_data.json** - Today's completion status
- **routine_log.json** - Historical log of all completed tasks

These files are created automatically in your project directory and persist between sessions.

## Streak System

The app tracks consecutive days of **100% task completion**. Complete all tasks in all routines for a day to build your streak! This is a great motivator for consistency.

## Time Tracking

When marking a task complete, you can enter the actual time spent. This helps you:
- Understand how long tasks actually take
- Adjust future time estimates
- Track total time invested in routines

## Customization

Edit `DEFAULT_ROUTINES` in `main.py` to change the default routines, or simply use the interactive menu to add your own.

### Example: Add an Exercise Routine
```
Option 3: Add new routine
Enter routine name: Exercise
Option 5: Add task to routine
Enter task name: 20-min jog
Time estimate: 20
Priority: high
Scheduled time: 07:00
```

## Future Enhancements

- [ ] Desktop GUI version using Tkinter
- [ ] Mobile app sync
- [ ] Weekly/monthly analytics dashboard
- [ ] Integration with Google Calendar
- [ ] Reminders via email or SMS
- [ ] Collaborative routines (share with friends/family)
- [ ] Habit gamification (badges, achievements)

## Troubleshooting

**Issue: Colors not showing on Windows**
- Colors work best on Windows 10+ Terminal or Visual Studio Code
- For older Windows Command Prompt, install Windows Terminal

**Issue: colorama not found**
- Make sure to install it: `pip install colorama`

**Issue: Data not saving**
- Check file permissions in your project directory
- Ensure write access to the folder

## Tips for Success 💡

1. **Be realistic** with time estimates - track actual time to improve
2. **Start small** - begin with just one or two routines
3. **Review daily** - check stats each evening to stay motivated
4. **Adjust as needed** - modify routines based on what works
5. **Build streaks** - aim for consecutive days to build momentum
6. **Export reports** - save weekly/monthly reports to track long-term progress

## Contributing

Have ideas to improve the routine tracker? Feel free to:
- Fork the repository
- Make your changes
- Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues, please open a GitHub issue on the repository.

---

**Happy routine tracking! Remember: Small daily actions lead to big results over time. 🚀**
