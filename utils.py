"""
Utility functions for Daily Routine Tracker.
Helper functions for backups, file operations, formatting, and calculations.
"""

import json
import logging
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

import config

logger = logging.getLogger(__name__)


# ==================== FILE MANAGEMENT ====================
class FileManager:
    """Handle file operations including backups, imports, and exports."""

    @staticmethod
    def backup_all_data() -> Path:
        """Create a backup of all data files.
        
        Returns:
            Path: Directory containing the backup files.
        """
        backup_dir = config.BACKUPS_DIR / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_dir.mkdir(exist_ok=True)

        files_to_backup = [
            config.ROUTINES_FILE,
            config.COMPLETION_FILE,
            config.LOG_FILE,
            config.ACHIEVEMENTS_FILE,
        ]

        for file_path in files_to_backup:
            if file_path.exists():
                shutil.copy(file_path, backup_dir / file_path.name)
                logger.info(f"Backed up {file_path.name}")

        return backup_dir

    @staticmethod
    def restore_backup(backup_path: Path) -> bool:
        """Restore data from a backup directory.
        
        Args:
            backup_path: Path to the backup directory.
            
        Returns:
            bool: True if restore was successful, False otherwise.
        """
        if not backup_path.exists():
            logger.error(f"Backup path does not exist: {backup_path}")
            return False

        try:
            for file_path in backup_path.glob("*"):
                shutil.copy(file_path, config.DATA_DIR / file_path.name)
            logger.info(f"Successfully restored backup from {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to restore backup: {e}")
            return False

    @staticmethod
    def export_to_json(filename: Optional[str] = None) -> str:
        """Export all data to a JSON file.
        
        Args:
            filename: Optional custom filename for export.
            
        Returns:
            str: Path to the exported file.
        """
        if not filename:
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        export_data: Dict[str, Any] = {}

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

        logger.info(f"Data exported to {filename}")
        return filename

    @staticmethod
    def import_from_json(filename: str) -> bool:
        """Import data from a JSON file.
        
        Args:
            filename: Path to the JSON file to import.
            
        Returns:
            bool: True if import was successful, False otherwise.
        """
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

            logger.info(f"Successfully imported data from {filename}")
            return True
        except Exception as e:
            logger.error(f"Import failed: {e}")
            return False

    @staticmethod
    def clear_old_backups(max_backups: int = 10) -> None:
        """Clear old backups, keeping only the most recent.
        
        Args:
            max_backups: Maximum number of backups to retain.
        """
        backups = sorted(
            config.BACKUPS_DIR.glob("backup_*"),
            key=lambda x: x.stat().st_ctime,
            reverse=True
        )

        for backup in backups[max_backups:]:
            shutil.rmtree(backup)
            logger.info(f"Removed old backup: {backup.name}")


# ==================== PROGRESS VISUALIZATION ====================
class ProgressBar:
    """Generate progress bar visualizations."""

    @staticmethod
    def draw(current: int, total: int, width: int = 30) -> str:
        """Draw a percentage-based progress bar.
        
        Args:
            current: Current progress value.
            total: Total value (100%).
            width: Width of the progress bar in characters.
            
        Returns:
            str: Formatted progress bar string.
        """
        percent = current / total if total > 0 else 0
        filled = int(width * percent)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {percent * 100:.1f}%"

    @staticmethod
    def draw_horizontal(value: int, max_value: int = 100, width: int = 40) -> str:
        """Draw a horizontal progress bar with ratio.
        
        Args:
            value: Current value.
            max_value: Maximum value.
            width: Width of the progress bar in characters.
            
        Returns:
            str: Formatted progress bar with ratio.
        """
        filled = int((value / max_value) * width) if max_value > 0 else 0
        bar = "█" * filled + "░" * (width - filled)
        return f"{bar} {value}/{max_value}"


# ==================== TEXT FORMATTING ====================
class ColoredText:
    """Generate colored terminal text output."""

    @staticmethod
    def success(text: str) -> str:
        """Format text as success (green)."""
        return f"{config.COLORS['success']}{text}{config.COLORS['reset']}"

    @staticmethod
    def error(text: str) -> str:
        """Format text as error (red)."""
        return f"{config.COLORS['error']}{text}{config.COLORS['reset']}"

    @staticmethod
    def warning(text: str) -> str:
        """Format text as warning (yellow)."""
        return f"{config.COLORS['warning']}{text}{config.COLORS['reset']}"

    @staticmethod
    def info(text: str) -> str:
        """Format text as info (cyan)."""
        return f"{config.COLORS['info']}{text}{config.COLORS['reset']}"

    @staticmethod
    def primary(text: str) -> str:
        """Format text as primary (blue)."""
        return f"{config.COLORS['primary']}{text}{config.COLORS['reset']}"


# ==================== DATA VALIDATION ====================
class DataValidator:
    """Validate user input and data integrity."""

    @staticmethod
    def validate_time_format(time_str: str) -> bool:
        """Validate time string in HH:MM format.
        
        Args:
            time_str: Time string to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            parts = time_str.split(':')
            if len(parts) != 2:
                return False
            hour, minute = int(parts[0]), int(parts[1])
            return 0 <= hour < 24 and 0 <= minute < 60
        except (ValueError, IndexError):
            return False

    @staticmethod
    def validate_priority(priority: str) -> bool:
        """Validate priority level.
        
        Args:
            priority: Priority to validate.
            
        Returns:
            bool: True if valid priority, False otherwise.
        """
        return priority in config.VALIDATION['valid_priorities']

    @staticmethod
    def validate_routine_name(name: str) -> bool:
        """Validate routine name.
        
        Args:
            name: Routine name to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        max_len = config.VALIDATION['routine_name_max_length']
        return len(name.strip()) > 0 and len(name) <= max_len

    @staticmethod
    def validate_task_name(name: str) -> bool:
        """Validate task name.
        
        Args:
            name: Task name to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        max_len = config.VALIDATION['task_name_max_length']
        return len(name.strip()) > 0 and len(name) <= max_len

    @staticmethod
    def validate_time_estimate(time: str) -> bool:
        """Validate time estimate in minutes.
        
        Args:
            time: Time estimate to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            minutes = int(time)
            max_min = config.VALIDATION['max_time_estimate_minutes']
            min_min = config.VALIDATION['min_time_estimate_minutes']
            return min_min <= minutes <= max_min
        except ValueError:
            return False


# ==================== CALCULATIONS ====================
class Calculator:
    """Perform calculations for routines and gamification."""

    @staticmethod
    def calculate_total_routine_time(tasks: List[Dict[str, Any]]) -> int:
        """Calculate total time for all tasks in a routine.
        
        Args:
            tasks: List of task dictionaries.
            
        Returns:
            int: Total time in minutes.
        """
        return sum(
            task.get('time', 0) if isinstance(task, dict) else 0
            for task in tasks
        )

    @staticmethod
    def calculate_completion_percentage(completed: int, total: int) -> float:
        """Calculate completion percentage.
        
        Args:
            completed: Number of completed items.
            total: Total number of items.
            
        Returns:
            float: Completion percentage (0-100).
        """
        return (completed / total * 100) if total > 0 else 0

    @staticmethod
    def calculate_time_efficiency(estimated: int, actual: int) -> float:
        """Calculate time efficiency percentage.
        
        Args:
            estimated: Estimated time in minutes.
            actual: Actual time spent in minutes.
            
        Returns:
            float: Efficiency percentage (capped at 200%).
        """
        if estimated == 0:
            return 0
        efficiency = (estimated / actual) * 100
        return min(200, efficiency)

    @staticmethod
    def calculate_daily_xp(tasks_completed: int, perfect_day: bool = False) -> int:
        """Calculate daily XP earned.
        
        Args:
            tasks_completed: Number of tasks completed.
            perfect_day: Whether all tasks were completed.
            
        Returns:
            int: Total XP earned.
        """
        xp = tasks_completed * config.GAMIFICATION["xp_per_task"]
        if perfect_day:
            xp += config.GAMIFICATION["xp_perfect_day"]
        return xp

    @staticmethod
    def calculate_streak_bonus(streak_count: int) -> int:
        """Calculate streak bonus XP.
        
        Args:
            streak_count: Number of consecutive days.
            
        Returns:
            int: Bonus XP for streak.
        """
        return streak_count * config.GAMIFICATION["streak_bonus"]


# ==================== TIME UTILITIES ====================
class TimeHelper:
    """Handle time-related calculations and formatting."""

    @staticmethod
    def get_time_remaining_today() -> str:
        """Get time remaining until midnight.
        
        Returns:
            str: Formatted time remaining (e.g., "5h 30m").
        """
        now = datetime.now()
        tomorrow = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        remaining = tomorrow - now
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60
        return f"{hours}h {minutes}m"

    @staticmethod
    def format_time_spent(minutes: int) -> str:
        """Format minutes to readable time.
        
        Args:
            minutes: Time in minutes.
            
        Returns:
            str: Formatted time (e.g., "1h 30m" or "45m").
        """
        hours = minutes // 60
        mins = minutes % 60
        if hours > 0:
            return f"{hours}h {mins}m"
        return f"{mins}m"

    @staticmethod
    def get_time_until_routine(scheduled_time: str) -> Optional[int]:
        """Get seconds until a scheduled routine.
        
        Args:
            scheduled_time: Scheduled time in HH:MM format.
            
        Returns:
            int: Seconds until routine, or None if invalid time.
        """
        try:
            target = datetime.strptime(scheduled_time, "%H:%M").time()
            now = datetime.now()
            target_datetime = datetime.combine(now.date(), target)

            if target_datetime < now:
                target_datetime += timedelta(days=1)

            remaining = target_datetime - now
            return remaining.seconds
        except ValueError:
            logger.error(f"Invalid time format: {scheduled_time}")
            return None


# ==================== CONSOLE OUTPUT ====================
def print_header(text: str) -> None:
    """Print a formatted header with borders.
    
    Args:
        text: Header text to display.
    """
    print(f"\n{config.COLORS['primary']}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{config.COLORS['reset']}")


def print_section(text: str) -> None:
    """Print a section header with dashes.
    
    Args:
        text: Section text to display.
    """
    print(f"\n{config.COLORS['info']}--- {text} ---{config.COLORS['reset']}")


def print_error(text: str) -> None:
    """Print an error message with icon.
    
    Args:
        text: Error message to display.
    """
    print(f"{config.COLORS['error']}✗ {text}{config.COLORS['reset']}")


def print_success(text: str) -> None:
    """Print a success message with icon.
    
    Args:
        text: Success message to display.
    """
    print(f"{config.COLORS['success']}✓ {text}{config.COLORS['reset']}")


def print_warning(text: str) -> None:
    """Print a warning message with icon.
    
    Args:
        text: Warning message to display.
    """
    print(f"{config.COLORS['warning']}⚠ {text}{config.COLORS['reset']}")


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
