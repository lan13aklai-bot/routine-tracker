"""
Configuration file for Daily Routine Tracker
Stores all settings, themes, and customizable options
"""

import os
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
BACKUPS_DIR = BASE_DIR / "backups"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
BACKUPS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Database settings
DB_PATH = DATA_DIR / "routine_tracker.db"
BACKUP_PATH = BACKUPS_DIR / "backup.json"

# File paths
ROUTINES_FILE = DATA_DIR / "routines.json"
COMPLETION_FILE = DATA_DIR / "completion.json"
LOG_FILE = DATA_DIR / "activity.json"
CONFIG_FILE = DATA_DIR / "settings.json"
ACHIEVEMENTS_FILE = DATA_DIR / "achievements.json"

# Default theme colors
COLORS = {
    "primary": "\033[36m",      # Cyan
    "success": "\033[32m",      # Green
    "warning": "\033[33m",      # Yellow
    "error": "\033[31m",        # Red
    "info": "\033[34m",         # Blue
    "purple": "\033[35m",       # Magenta
    "reset": "\033[0m"          # Reset
}

# Priority colors
PRIORITY_COLORS = {
    "high": "\033[31m",         # Red
    "medium": "\033[33m",       # Yellow
    "low": "\033[32m"           # Green
}

# Default settings
DEFAULT_SETTINGS = {
    "theme": "dark",
    "notifications_enabled": True,
    "email_notifications": False,
    "daily_reset_time": "00:00",
    "language": "en",
    "units": "metric",
    "week_starts_on": "Monday",
    "streak_display": True,
    "analytics_enabled": True,
    "backup_enabled": True,
    "backup_frequency": "daily"
}

# Default routines (same as before)
DEFAULT_ROUTINES = {
    "Morning": [
        {"task": "Review daily tasks", "time": 10, "priority": "high", "scheduled_time": "07:00", "category": "planning"},
        {"task": "Pack school bag", "time": 15, "priority": "high", "scheduled_time": "07:15", "category": "preparation"},
        {"task": "30-min reading", "time": 30, "priority": "medium", "scheduled_time": "07:45", "category": "education"}
    ],
    "Study": [
        {"task": "Complete homework", "time": 60, "priority": "high", "scheduled_time": "15:00", "category": "education"},
        {"task": "Review class notes", "time": 30, "priority": "medium", "scheduled_time": "16:15", "category": "education"},
        {"task": "Practice problems", "time": 45, "priority": "medium", "scheduled_time": "17:00", "category": "education"}
    ],
    "Evening": [
        {"task": "Organize study desk", "time": 15, "priority": "low", "scheduled_time": "20:00", "category": "organization"},
        {"task": "Log daily achievements", "time": 10, "priority": "medium", "scheduled_time": "20:20", "category": "reflection"},
        {"task": "Set phone to Do Not Disturb", "time": 5, "priority": "high", "scheduled_time": "21:00", "category": "wellness"}
    ]
}

# Gamification settings
GAMIFICATION = {
    "xp_per_task": 10,
    "xp_per_routine": 50,
    "streak_bonus": 5,
    "level_threshold": 100,
    "daily_challenge_xp": 25
}

# Achievements configuration
ACHIEVEMENTS = {
    "first_task": {"name": "First Step", "description": "Complete your first task", "icon": "👣", "points": 10},
    "streak_3": {"name": "On Fire", "description": "Complete 3 consecutive days", "icon": "🔥", "points": 25},
    "streak_7": {"name": "Week Warrior", "description": "Complete 7 consecutive days", "icon": "⚔️", "points": 50},
    "streak_30": {"name": "Monthly Master", "description": "Complete 30 consecutive days", "icon": "👑", "points": 200},
    "perfect_day": {"name": "Perfect Day", "description": "Complete all tasks in a day", "icon": "✨", "points": 50},
    "all_priority": {"name": "Priority Master", "description": "Complete high priority task", "icon": "⭐", "points": 15},
    "time_efficient": {"name": "Speed Runner", "description": "Complete task faster than estimate", "icon": "⚡", "points": 20},
    "collector": {"name": "Collector", "description": "Create 5 routines", "icon": "📚", "points": 50},
    "task_master": {"name": "Task Master", "description": "Create 20 tasks", "icon": "🎯", "points": 75},
    "level_10": {"name": "Legendary", "description": "Reach level 10", "icon": "🌟", "points": 150}
}

# Notification settings
NOTIFICATIONS = {
    "reminder_before_minutes": 5,
    "sound_enabled": True,
    "desktop_notifications": True,
    "email_on_streak_break": True
}

# Analytics settings
ANALYTICS = {
    "track_completion_time": True,
    "track_productivity": True,
    "track_trends": True,
    "chart_type": "ascii"  # Can be 'ascii' or 'web'
}

# Web server settings
WEB_SERVER = {
    "host": "127.0.0.1",
    "port": 5000,
    "debug": True,
    "threaded": True
}

# Backup settings
BACKUP = {
    "auto_backup": True,
    "backup_frequency": "daily",
    "max_backups": 10,
    "compression": True
}
