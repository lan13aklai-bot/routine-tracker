"""
Utility functions for Daily Routine Tracker
Helper functions for backups, file operations, and misc tasks
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
import config

class FileManager:
    @staticmethod
    def backup_all_data():
        """Backup all data files"""
        backup_dir = config.BACKUPS_DIR / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_dir.mkdir(exist_ok=True)
        
        files_to_backup = [
            config.ROUTINES_FILE,
            config.COMPLETION_FILE,
            config.LOG_FILE,
            config.ACHIEVEMENTS_FILE
        ]
        
        for file_path in files_to_backup:
            if file_path.exists():
                shutil.copy(file_path, backup_dir / file_path.name)
        
        return backup_dir
    
    @staticmethod
    def restore_backup(backup_path):
        """Restore from a backup"""
        if not backup_path.exists():
            return False
        
        for file_path in backup_path.glob("*"):
            shutil.copy(file_path, config.DATA_DIR / file_path.name)
        
        return True
    
    @staticmethod
    def export_to_json(filename=None):
        """Export all data to JSON"""
        if not filename:
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {}
        
        # Export routines
        if config.ROUTINES_FILE.exists():
            with open(config.ROUTINES_FILE, 'r') as f:
                export_data['routines'] = json.load(f)
        
        # Export completion data
        if config.COMPLETION_FILE.exists():
            with open(config.COMPLETION_FILE, 'r') as f:
                export_data['completion_data'] = json.load(f)
        
        # Export activity log
        if config.LOG_FILE.exists():
            with open(config.LOG_FILE, 'r') as f:
                export_data['activity_log'] = json.load(f)
        
        # Export achievements
        if config.ACHIEVEMENTS_FILE.exists():
            with open(config.ACHIEVEMENTS_FILE, 'r') as f:
                export_data['achievements'] = json.load(f)
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filename
    
    @staticmethod
    def import_from_json(filename):
        """Import data from JSON"""
        try:
            with open(filename, 'r') as f:
                import_data = json.load(f)
            
            # Import routines
            if 'routines' in import_data:
                with open(config.ROUTINES_FILE, 'w') as f:
                    json.dump(import_data['routines'], f, indent=2)
            
            # Import completion data
            if 'completion_data' in import_data:
                with open(config.COMPLETION_FILE, 'w') as f:
                    json.dump(import_data['completion_data'], f, indent=2)
            
            # Import activity log
            if 'activity_log' in import_data:
                with open(config.LOG_FILE, 'w') as f:
                    json.dump(import_data['activity_log'], f, indent=2)
            
            # Import achievements
            if 'achievements' in import_data:
                with open(config.ACHIEVEMENTS_FILE, 'w') as f:
                    json.dump(import_data['achievements'], f, indent=2)
            
            return True
        except Exception as e:
            print(f"{config.COLORS['error']}Import failed: {e}{config.COLORS['reset']}")
            return False
    
    @staticmethod
    def clear_old_backups(max_backups=10):
        """Clear old backups, keeping only the most recent"""
        backups = sorted(config.BACKUPS_DIR.glob("backup_*"), key=lambda x: x.stat().st_ctime, reverse=True)
        
        for backup in backups[max_backups:]:
            shutil.rmtree(backup)

class ProgressBar:
    @staticmethod
    def draw(current, total, width=30):
        """Draw a progress bar"""
        percent = current / total if total > 0 else 0
        filled = int(width * percent)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {percent * 100:.1f}%"
    
    @staticmethod
    def draw_horizontal(value, max_value=100, width=40):
        """Draw a horizontal progress bar"""
        filled = int((value / max_value) * width) if max_value > 0 else 0
        bar = "█" * filled + "░" * (width - filled)
        return f"{bar} {value}/{max_value}"

class ColoredText:
    @staticmethod
    def success(text):
        """Print success text"""
        return f"{config.COLORS['success']}{text}{config.COLORS['reset']}"
    
    @staticmethod
    def error(text):
        """Print error text"""
        return f"{config.COLORS['error']}{text}{config.COLORS['reset']}"
    
    @staticmethod
    def warning(text):
        """Print warning text"""
        return f"{config.COLORS['warning']}{text}{config.COLORS['reset']}"
    
    @staticmethod
    def info(text):
        """Print info text"""
        return f"{config.COLORS['info']}{text}{config.COLORS['reset']}"
    
    @staticmethod
    def primary(text):
        """Print primary color text"""
        return f"{config.COLORS['primary']}{text}{config.COLORS['reset']}"

class DataValidator:
    @staticmethod
    def validate_time_format(time_str):
        """Validate time format HH:MM"""
        try:
            parts = time_str.split(':')
            if len(parts) != 2:
                return False
            hour, minute = int(parts[0]), int(parts[1])
            return 0 <= hour < 24 and 0 <= minute < 60
        except:
            return False
    
    @staticmethod
    def validate_priority(priority):
        """Validate priority level"""
        return priority in ["high", "medium", "low"]
    
    @staticmethod
    def validate_routine_name(name):
        """Validate routine name"""
        return len(name.strip()) > 0 and len(name) <= 50
    
    @staticmethod
    def validate_task_name(name):
        """Validate task name"""
        return len(name.strip()) > 0 and len(name) <= 100
    
    @staticmethod
    def validate_time_estimate(time):
        """Validate time estimate"""
        try:
            return 0 < int(time) <= 480  # Max 8 hours
        except:
            return False

class Calculator:
    @staticmethod
    def calculate_total_routine_time(tasks):
        """Calculate total time for all tasks in a routine"""
        return sum(task.get('time', 0) if isinstance(task, dict) else 0 for task in tasks)
    
    @staticmethod
    def calculate_completion_percentage(completed, total):
        """Calculate completion percentage"""
        return (completed / total * 100) if total > 0 else 0
    
    @staticmethod
    def calculate_time_efficiency(estimated, actual):
        """Calculate time efficiency percentage"""
        if estimated == 0:
            return 0
        efficiency = (estimated / actual) * 100
        return min(200, efficiency)  # Cap at 200%
    
    @staticmethod
    def calculate_daily_xp(tasks_completed, perfect_day=False):
        """Calculate daily XP"""
        xp = tasks_completed * config.GAMIFICATION["xp_per_task"]
        if perfect_day:
            xp += config.GAMIFICATION["xp_per_routine"]
        return xp
    
    @staticmethod
    def calculate_streak_bonus(streak_count):
        """Calculate streak bonus XP"""
        return streak_count * config.GAMIFICATION["streak_bonus"]

class TimeHelper:
    @staticmethod
    def get_time_remaining_today():
        """Get time remaining until midnight"""
        now = datetime.now()
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        remaining = tomorrow - now
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    
    @staticmethod
    def format_time_spent(minutes):
        """Format minutes to readable time"""
        hours = minutes // 60
        mins = minutes % 60
        if hours > 0:
            return f"{hours}h {mins}m"
        return f"{mins}m"
    
    @staticmethod
    def get_time_until_routine(scheduled_time):
        """Get time until a scheduled routine"""
        try:
            target = datetime.strptime(scheduled_time, "%H:%M").time()
            now = datetime.now()
            target_datetime = datetime.combine(now.date(), target)
            
            if target_datetime < now:
                target_datetime = target_datetime.replace(day=target_datetime.day + 1)
            
            remaining = target_datetime - now
            return remaining.seconds
        except:
            return None

def print_header(text):
    """Print a formatted header"""
    print(f"\n{config.COLORS['primary']}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{config.COLORS['reset']}")

def print_section(text):
    """Print a section header"""
    print(f"\n{config.COLORS['info']}--- {text} ---{config.COLORS['reset']}")

def print_error(text):
    """Print error message"""
    print(f"{config.COLORS['error']}✗ {text}{config.COLORS['reset']}")

def print_success(text):
    """Print success message"""
    print(f"{config.COLORS['success']}✓ {text}{config.COLORS['reset']}")

def print_warning(text):
    """Print warning message"""
    print(f"{config.COLORS['warning']}⚠ {text}{config.COLORS['reset']}")

def clear_screen():
    """Clear terminal screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

from datetime import timedelta
