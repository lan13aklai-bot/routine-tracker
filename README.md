````markdown
# 🎯 Daily Routine Tracker

A comprehensive Python application for tracking daily routines, building streaks, and gamifying productivity. Features a command-line interface and web dashboard with analytics, achievements, and real-time notifications.

## ✨ Features

### 📋 Routine Management
- **Pre-configured Routines**: Morning, Afternoon, Evening, and Study routines
- **Custom Routines**: Create personalized routines with tasks
- **Task Organization**: Organize tasks by priority (high, medium, low)
- **Time Estimation**: Track estimated vs actual time spent
- **Scheduled Tasks**: Set specific times for routine execution

### 🎮 Gamification System
- **Experience Points (XP)**: Earn XP for completing tasks
- **Leveling System**: Progress through 100+ levels
- **Achievements**: Unlock badges for milestones
- **Streaks**: Build daily completion streaks with bonus rewards
- **Leaderboards**: Track personal statistics and records
- **Perfect Days**: Special bonus for completing all tasks

### 📊 Advanced Analytics
- **Weekly Summary**: Visual representation of daily completions
- **Completion Rates**: Track routine completion percentages
- **Time Analysis**: Compare estimated vs actual time
- **Productivity Insights**: Find your most productive hours
- **Monthly Reports**: Generate comprehensive monthly reports
- **Trend Analysis**: Track productivity over time

### 🔔 Smart Notifications
- **Desktop Alerts**: Real-time task and achievement notifications
- **Routine Reminders**: Get reminded before routines start
- **Streak Warnings**: Alerts when your streak is at risk
- **Achievement Unlocks**: Celebrate milestone achievements
- **Perfect Day Celebration**: Special notification for perfect days

### 💾 Data Management
- **Persistent Storage**: SQLite database for reliability
- **JSON Export**: Export all data for backup
- **Automatic Backups**: Scheduled backup system
- **Data Import**: Restore from backup files
- **Activity Logging**: Complete activity history

### 🌐 Web Dashboard
- **Beautiful UI**: Modern, responsive web interface
- **Real-time Updates**: Live progress tracking
- **Analytics Visualization**: Charts and statistics
- **Quick Actions**: One-click task completion
- **API Endpoints**: Full REST API for integrations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/routine-tracker.git
   cd routine-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   
   **CLI Mode:**
   ```bash
   python main.py
   ```
   
   **Web Mode:**
   ```bash
   python app.py
   ```
   Then open `http://localhost:5000` in your browser

## 📚 Usage

### CLI Commands

#### Start Your Day
```bash
python main.py start
```

#### View Routines
```bash
python main.py routines
```

#### Mark Task Complete
```bash
python main.py complete <routine_name> <task_index>
```

#### View Analytics
```bash
python main.py analytics
```

#### Check Achievements
```bash
python main.py achievements
```

#### View Statistics
```bash
python main.py stats
```

#### Backup Data
```bash
python main.py backup
```

### Web Interface

Access the web dashboard at `http://localhost:5000`:
- **Home**: Today's progress and summary
- **Routines**: Manage and execute routines
- **Analytics**: View detailed statistics and charts
- **Gamification**: Track level, XP, and achievements
- **API**: RESTful API endpoints for integration

## 📁 Project Structure

```
routine-tracker/
├── main.py              # CLI entry point
├── app.py               # Flask web application
├── config.py            # Configuration and constants
├── tracker.py           # Core routine tracking logic
├── gamification.py      # Gamification system
├── analytics.py         # Analytics and reporting
├── notifications.py     # Notification system
├── database.py          # SQLite database operations
├── utils.py             # Utility functions
├── tests.py             # Unit tests
├── requirements.txt     # Python dependencies
├── data/                # Data directory
│   ├── routines.json    # User routines
│   ├── completion.json  # Completion records
│   ├── achievements.json# Achievement data
│   └── activity.json    # Activity log
├── backups/             # Backup storage
└── templates/           # HTML templates (web)
    ├── index.html
    ├── routines.html
    ├── analytics.html
    └── gamification.html
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Default routines
DEFAULT_ROUTINES = {
    "Morning": [...],
    "Afternoon": [...],
    "Evening": [...],
    "Study": [...]
}

# Gamification settings
GAMIFICATION = {
    "xp_per_task": 10,
    "xp_per_routine": 50,
    "levels": 100,
    "level_multiplier": 1.5
}

# Notification settings
NOTIFICATIONS = {
    "sound_enabled": True,
    "reminder_before_minutes": 5
}
```

## 🎮 Gamification Details

### XP System
- Complete a task: **10 XP**
- Complete a routine: **50 XP**
- Perfect day (all tasks): **100 XP bonus**
- Streak milestone (10 days): **200 XP bonus**

### Achievements
- **Early Bird**: Complete morning routine 5 days in a row
- **Night Owl**: Complete evening routine 7 days in a row
- **Productive Scholar**: Complete study routine 14 days in a row
- **Consistency Master**: 30-day perfect streak
- **Unstoppable**: 100-day perfect streak
- **Marathon Runner**: 365-day perfect streak

### Levels
- Progress through 100 levels
- XP requirement increases with each level
- Level-up bonuses and rewards
- Special milestones at levels 10, 25, 50, 75, 100

## 📊 Analytics Features

### Completion Rates
- Track completion percentage by day
- Weekly and monthly trends
- Routine-specific completion rates

### Productivity Analysis
- Most productive hours of the day
- Average time per task
- Time estimation accuracy
- Efficiency metrics

### Reports
- Weekly summary reports
- Monthly analytics exports
- Historical data trends
- Performance benchmarks

## 🔔 Notifications

### Types
- ✅ Task completion notifications
- 📋 Routine availability alerts
- ⏰ Time reminder notifications
- 🏆 Achievement unlock notifications
- ⭐ Level-up notifications
- 🔥 Streak milestone notifications
- ⚠️ Streak break warnings

### Configuration
- Enable/disable notifications
- Adjust reminder timing
- Customize notification sounds
- Email notification support (optional)

## 💾 Data Persistence

### Storage Options
- **SQLite Database**: Recommended for reliability
- **JSON Files**: Alternative storage
- **Automatic Backups**: Scheduled backups
- **Manual Exports**: Export to JSON

### Backup
```bash
python main.py backup
```

### Restore
```bash
python main.py restore <backup_path>
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python tests.py
```

Tests include:
- Data validation
- Calculator functions
- Analytics calculations
- Gamification system
- Routine data integrity
- Achievement configuration

## 📈 Statistics Tracked

### Personal Stats
- Total tasks completed
- Total routines completed
- Perfect days count
- Current streak length
- Longest streak
- Total XP earned
- Current level

### Routine Stats
- Completion percentage per routine
- Average time per routine
- Most frequent routine
- Least frequent routine

### Daily Stats
- Tasks completed today
- Time spent on tasks
- Completion rate
- Streak status
- XP earned

## 🌐 REST API Endpoints

### Routines
- `GET /api/routines` - Get all routines
- `GET /api/routine/<name>` - Get specific routine
- `POST /api/routine` - Create new routine

### Tasks
- `POST /api/task/<routine>/<index>/complete` - Mark task complete

### Analytics
- `GET /api/analytics/weekly` - Weekly summary
- `GET /api/analytics/completion-rate` - Completion rates

### Gamification
- `GET /api/gamification/summary` - Summary data
- `GET /api/gamification/achievements` - Achievements list

### Data
- `GET /api/export` - Export all data

## 🎨 Color Scheme

The CLI uses a vibrant color scheme:
- 🟦 Primary: Information displays
- 🟩 Success: Completed actions
- 🟨 Warning: Important notices
- 🟥 Error: Errors and failures
- 🟪 Purple: Headers and sections

## 🔐 Security Notes

- Store sensitive data in environment variables
- Use strong secrets for web sessions
- Regularly backup your data
- Keep dependencies updated

## 🐛 Troubleshooting

### Notifications Not Working
```bash
pip install plyer
```

### Database Errors
```bash
# Backup and reset database
python main.py backup
rm data/routines.db
python main.py
```

### Port Already in Use
Edit `config.py` and change `app_port`

## 📝 Example Workflows

### Morning Routine
1. Start the app: `python main.py`
2. Select "Morning" routine
3. Complete tasks one by one
4. View progress and XP gained
5. Check if you earned any achievements

### Weekly Review
1. Open web dashboard: `http://localhost:5000`
2. Go to Analytics tab
3. Review completion rates and productivity
4. Check achievement progress
5. Export report if needed

### Backup Your Data
1. Run: `python main.py backup`
2. Data saved to `backups/` directory
3. Schedule automatic backups weekly

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built with Python and Flask
- SQLite for data persistence
- Inspired by productivity systems and gamification

## 📧 Contact & Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review the FAQ section

## 🎯 Roadmap

### v1.1
- [ ] Mobile app (React Native)
- [ ] Cloud sync
- [ ] Team/family routines
- [ ] Advanced scheduling

### v1.2
- [ ] AI-powered insights
- [ ] Habit recommendations
- [ ] Social leaderboards
- [ ] Integration with calendar apps

### v2.0
- [ ] Desktop app (Electron)
- [ ] Multi-user support
- [ ] Advanced reporting
- [ ] Custom themes

## ⭐ If you find this helpful, please star the repository!

---

**Made with ❤️ by L.A. B0T**

Happy Tracking! 🚀
````
