"""
Configuration module for Daily Routine Tracker
Central location for all configuration constants and settings.
"""

from pathlib import Path
from typing import Dict, List, Any

# ==================== PATHS ====================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
BACKUPS_DIR = BASE_DIR / "backups"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Create directories if they don't exist
for directory in [DATA_DIR, BACKUPS_DIR, TEMPLATES_DIR, STATIC_DIR]:
    directory.mkdir(exist_ok=True)

# ==================== DATABASE ====================
DB_PATH: Path = DATA_DIR / "routine_tracker.db"

# ==================== DATA FILES ====================
ROUTINES_FILE: Path = DATA_DIR / "routines.json"
COMPLETION_FILE: Path = DATA_DIR / "completion.json"
LOG_FILE: Path = DATA_DIR / "activity_log.json"
ACHIEVEMENTS_FILE: Path = DATA_DIR / "achievements.json"

# ==================== COLOR SCHEME ====================
COLORS: Dict[str, str] = {
    'reset': '\033[0m',
    'primary': '\033[94m',      # Blue
    'success': '\033[92m',      # Green
    'warning': '\033[93m',      # Yellow
    'error': '\033[91m',        # Red
    'info': '\033[96m',         # Cyan
    'header': '\033[95m',       # Magenta
}

# ==================== DEFAULT ROUTINES ====================
DEFAULT_ROUTINES: Dict[str, List[Dict[str, Any]]] = {
    "Morning": [
        {
            "task": "Review daily goals",
            "time": 10,
            "priority": "high",
            "scheduled_time": "06:00",
            "category": "planning",
        },
        {
            "task": "Exercise/Stretch",
            "time": 20,
            "priority": "high",
            "scheduled_time": "06:15",
            "category": "health",
        },
        {
            "task": "Healthy breakfast",
            "time": 20,
            "priority": "medium",
            "scheduled_time": "06:40",
            "category": "nutrition",
        },
        {
            "task": "Shower and groom",
            "time": 15,
            "priority": "high",
            "scheduled_time": "07:00",
            "category": "personal",
        },
    ],
    "Afternoon": [
        {
            "task": "Lunch break",
            "time": 30,
            "priority": "medium",
            "scheduled_time": "12:00",
            "category": "nutrition",
        },
        {
            "task": "Walk/Fresh air",
            "time": 15,
            "priority": "low",
            "scheduled_time": "12:35",
            "category": "wellness",
        },
        {
            "task": "Afternoon review",
            "time": 10,
            "priority": "medium",
            "scheduled_time": "12:50",
            "category": "planning",
        },
    ],
    "Evening": [
        {
            "task": "Dinner",
            "time": 30,
            "priority": "medium",
            "scheduled_time": "18:00",
            "category": "nutrition",
        },
        {
            "task": "Tidy workspace",
            "time": 15,
            "priority": "low",
            "scheduled_time": "18:30",
            "category": "organization",
        },
        {
            "task": "Reflect on day",
            "time": 15,
            "priority": "medium",
            "scheduled_time": "20:00",
            "category": "reflection",
        },
        {
            "task": "Prepare for tomorrow",
            "time": 10,
            "priority": "high",
            "scheduled_time": "20:15",
            "category": "planning",
        },
        {
            "task": "Wind down routine",
            "time": 20,
            "priority": "high",
            "scheduled_time": "20:25",
            "category": "wellness",
        },
    ],
    "Study": [
        {
            "task": "Review previous notes",
            "time": 15,
            "priority": "medium",
            "scheduled_time": "N/A",
            "category": "learning",
        },
        {
            "task": "Focus study session",
            "time": 45,
            "priority": "high",
            "scheduled_time": "N/A",
            "category": "learning",
        },
        {
            "task": "Practice problems",
            "time": 30,
            "priority": "high",
            "scheduled_time": "N/A",
            "category": "practice",
        },
        {
            "task": "Summarize learnings",
            "time": 15,
            "priority": "medium",
            "scheduled_time": "N/A",
            "category": "reflection",
        },
    ],
}

# ==================== GAMIFICATION ====================
GAMIFICATION: Dict[str, int | float] = {
    "xp_per_task": 10,
    "xp_per_routine": 50,
    "xp_perfect_day": 100,
    "streak_bonus": 5,
    "levels": 100,
    "level_multiplier": 1.5,
    "initial_xp_for_level": 100,
}

ACHIEVEMENTS: Dict[str, Dict[str, str | int]] = {
    "early_bird": {
        "name": "Early Bird",
        "description": "Complete morning routine 5 days in a row",
        "icon": "🌅",
        "points": 50,
    },
    "night_owl": {
        "name": "Night Owl",
        "description": "Complete evening routine 7 days in a row",
        "icon": "🌙",
        "points": 50,
    },
    "scholar": {
        "name": "Productive Scholar",
        "description": "Complete study routine 14 days in a row",
        "icon": "📚",
        "points": 100,
    },
    "consistency_10": {
        "name": "Consistency Starter",
        "description": "10-day perfect streak",
        "icon": "🔥",
        "points": 75,
    },
    "consistency_30": {
        "name": "Consistency Master",
        "description": "30-day perfect streak",
        "icon": "⭐",
        "points": 150,
    },
    "consistency_100": {
        "name": "Unstoppable",
        "description": "100-day perfect streak",
        "icon": "💪",
        "points": 300,
    },
    "consistency_365": {
        "name": "Marathon Runner",
        "description": "365-day perfect streak",
        "icon": "🏆",
        "points": 500,
    },
    "level_10": {
        "name": "Rising Star",
        "description": "Reach level 10",
        "icon": "⬆️",
        "points": 100,
    },
    "level_50": {
        "name": "Mid-Level Master",
        "description": "Reach level 50",
        "icon": "📈",
        "points": 250,
    },
    "level_100": {
        "name": "Ultimate Legend",
        "description": "Reach level 100",
        "icon": "👑",
        "points": 500,
    },
    "perfect_day": {
        "name": "Perfect Day",
        "description": "Complete all tasks in a day",
        "icon": "✨",
        "points": 50,
    },
}

# ==================== NOTIFICATIONS ====================
NOTIFICATIONS: Dict[str, bool | int] = {
    "sound_enabled": True,
    "desktop_enabled": True,
    "reminder_before_minutes": 5,
    "show_level_up": True,
    "show_achievement": True,
    "show_streak_milestone": True,
    "show_perfect_day": True,
}

# ==================== APPLICATION SETTINGS ====================
DEFAULT_SETTINGS: Dict[str, str | int | bool] = {
    "app_host": "127.0.0.1",
    "app_port": 5000,
    "app_debug": True,
    "app_secret_key": "dev-secret-key-change-in-production",
    "timezone": "UTC",
    "date_format": "%Y-%m-%d",
    "time_format": "%H:%M",
    "backup_enabled": True,
    "backup_frequency": 7,
    "max_backups": 10,
}

# ==================== UI CONSTANTS ====================
MENU_WIDTH: int = 60
PROGRESS_BAR_WIDTH: int = 30
TABLE_PADDING: int = 2

# ==================== VALIDATION RULES ====================
VALIDATION: Dict[str, Any] = {
    "routine_name_max_length": 50,
    "task_name_max_length": 100,
    "max_time_estimate_minutes": 480,
    "min_time_estimate_minutes": 1,
    "valid_priorities": ["high", "medium", "low"],
}

# ==================== ANALYTICS ====================
ANALYTICS: Dict[str, int] = {
    "default_period_days": 7,
    "monthly_report_days": 30,
    "yearly_report_days": 365,
}

# ==================== PRIORITY LEVELS ====================
PRIORITY_LEVELS: Dict[str, Dict[str, Any]] = {
    "high": {"value": 1, "icon": "🔴", "color": COLORS["error"]},
    "medium": {"value": 2, "icon": "🟡", "color": COLORS["warning"]},
    "low": {"value": 3, "icon": "🟢", "color": COLORS["success"]},
}

# ==================== TASK CATEGORIES ====================
TASK_CATEGORIES: Dict[str, str] = {
    "planning": "📋",
    "health": "💪",
    "nutrition": "🍎",
    "personal": "🚿",
    "wellness": "🧘",
    "organization": "📁",
    "reflection": "🤔",
    "learning": "📚",
    "practice": "✏️",
}

# ==================== VERSION ====================
VERSION: str = "1.0.0"
AUTHOR: str = "L.A. B0T"
CREATED_DATE: str = "2026-09-06"

# ==================== LOGGING ====================
LOG_LEVEL: str = "INFO"
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
