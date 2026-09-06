"""
Gamification system for Daily Routine Tracker.
Handles achievements, XP, levels, and badges.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

import config

logger = logging.getLogger(__name__)


class GamificationSystem:
    """Manage user achievements, XP, levels, and badges."""

    def __init__(self, achievements_file: Path = config.ACHIEVEMENTS_FILE):
        """Initialize gamification system.
        
        Args:
            achievements_file: Path to achievements data file.
        """
        self.achievements_file = achievements_file
        self.achievements_data = self.load_achievements()
        self.level = self.calculate_level()

    def load_achievements(self) -> Dict[str, Any]:
        """Load user achievements from file.
        
        Returns:
            Dict containing achievements data.
        """
        if self.achievements_file.exists():
            try:
                with open(self.achievements_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to load achievements: {e}")
                return self.initialize_achievements()
        return self.initialize_achievements()

    def initialize_achievements(self) -> Dict[str, Any]:
        """Initialize empty achievements data structure.
        
        Returns:
            Dict with initialized achievements data.
        """
        return {
            "total_xp": 0,
            "level": 1,
            "unlocked_achievements": [],
            "badges": [],
            "statistics": {
                "total_tasks_completed": 0,
                "total_routines_completed": 0,
                "perfect_days": 0,
                "current_streak": 0,
                "longest_streak": 0,
                "tasks_completed_faster": 0,
                "routines_created": 0,
                "tasks_created": 0,
            },
        }

    def save_achievements(self) -> None:
        """Save achievements data to file."""
        config.DATA_DIR.mkdir(exist_ok=True)
        try:
            with open(self.achievements_file, 'w') as f:
                json.dump(self.achievements_data, f, indent=2)
            logger.info("Achievements saved successfully")
        except IOError as e:
            logger.error(f"Failed to save achievements: {e}")

    def add_xp(self, amount: int, reason: str = "") -> Dict[str, Any]:
        """Add XP to user account.
        
        Args:
            amount: Amount of XP to add.
            reason: Optional reason for adding XP.
            
        Returns:
            Dict with leveling information.
        """
        self.achievements_data["total_xp"] += amount
        old_level = self.achievements_data["level"]
        self.achievements_data["level"] = self.calculate_level()

        self.save_achievements()

        # Check if leveled up
        if self.achievements_data["level"] > old_level:
            logger.info(f"Level up! Now level {self.achievements_data['level']}")
            return {
                "leveled_up": True,
                "new_level": self.achievements_data["level"],
                "xp_gained": amount,
            }
        return {"leveled_up": False, "xp_gained": amount}

    def calculate_level(self) -> int:
        """Calculate level based on total XP.
        
        Returns:
            int: Current level.
        """
        total_xp = self.achievements_data["total_xp"]
        base_xp = config.GAMIFICATION["initial_xp_for_level"]
        multiplier = config.GAMIFICATION["level_multiplier"]
        
        level = 1
        xp_needed = base_xp
        current_xp = 0
        
        while current_xp + xp_needed <= total_xp:
            current_xp += xp_needed
            level += 1
            xp_needed = int(base_xp * (multiplier ** (level - 1)))
        
        return min(level, config.GAMIFICATION["levels"])

    def get_xp_to_next_level(self) -> int:
        """Calculate XP needed to reach next level.
        
        Returns:
            int: XP required for next level.
        """
        current_level = self.achievements_data["level"]
        if current_level >= config.GAMIFICATION["levels"]:
            return 0
        
        base_xp = config.GAMIFICATION["initial_xp_for_level"]
        multiplier = config.GAMIFICATION["level_multiplier"]
        next_level_xp = int(base_xp * (multiplier ** current_level))
        
        current_xp = self.achievements_data["total_xp"]
        xp_for_current_level = sum(
            int(base_xp * (multiplier ** (i - 1)))
            for i in range(1, current_level)
        )
        
        return max(0, next_level_xp - (current_xp - xp_for_current_level))

    def unlock_achievement(self, achievement_key: str) -> bool:
        """Unlock a new achievement.
        
        Args:
            achievement_key: Key of achievement to unlock.
            
        Returns:
            bool: True if achievement was unlocked, False if already unlocked.
        """
        if achievement_key not in config.ACHIEVEMENTS:
            logger.warning(f"Unknown achievement: {achievement_key}")
            return False
        
        # Check if already unlocked
        for achievement in self.achievements_data["unlocked_achievements"]:
            if achievement["key"] == achievement_key:
                return False

        achievement_data = config.ACHIEVEMENTS[achievement_key]
        
        self.achievements_data["unlocked_achievements"].append({
            "key": achievement_key,
            "name": achievement_data["name"],
            "description": achievement_data["description"],
            "icon": achievement_data["icon"],
            "points": achievement_data["points"],
            "unlocked_at": datetime.now().isoformat(),
        })

        # Add points as XP
        points = achievement_data["points"]
        self.add_xp(points, f"Achievement: {achievement_key}")
        self.save_achievements()
        
        logger.info(f"Achievement unlocked: {achievement_key}")
        return True

    def add_badge(self, badge_name: str) -> bool:
        """Add a badge to user profile.
        
        Args:
            badge_name: Name of badge to add.
            
        Returns:
            bool: True if badge was added, False if already exists.
        """
        if badge_name not in self.achievements_data["badges"]:
            self.achievements_data["badges"].append(badge_name)
            self.save_achievements()
            return True
        return False

    def update_statistic(self, stat_name: str, increment: int = 1) -> None:
        """Update a tracked statistic.
        
        Args:
            stat_name: Name of statistic to update.
            increment: Amount to increment by.
        """
        if stat_name in self.achievements_data["statistics"]:
            self.achievements_data["statistics"][stat_name] += increment
            self.save_achievements()

    def check_achievement_triggers(self, tracker: Any) -> List[str]:
        """Check if any achievements should be unlocked.
        
        Args:
            tracker: Routine tracker instance for context.
            
        Returns:
            List of newly unlocked achievement keys.
        """
        unlocked = []
        stats = self.achievements_data["statistics"]
        current_streak = tracker.completion_data.get("current_streak", 0)

        # Early bird achievement
        if current_streak >= 5 and self.unlock_achievement("early_bird"):
            unlocked.append("early_bird")

        # Night owl achievement
        if current_streak >= 7 and self.unlock_achievement("night_owl"):
            unlocked.append("night_owl")

        # Scholar achievement
        if current_streak >= 14 and self.unlock_achievement("scholar"):
            unlocked.append("scholar")

        # Consistency achievements
        if current_streak >= 10 and self.unlock_achievement("consistency_10"):
            unlocked.append("consistency_10")

        if current_streak >= 30 and self.unlock_achievement("consistency_30"):
            unlocked.append("consistency_30")

        if current_streak >= 100 and self.unlock_achievement("consistency_100"):
            unlocked.append("consistency_100")

        if current_streak >= 365 and self.unlock_achievement("consistency_365"):
            unlocked.append("consistency_365")

        # Perfect day
        if tracker.completion_data.get("perfect_day", False):
            if self.unlock_achievement("perfect_day"):
                unlocked.append("perfect_day")
            stats["perfect_days"] += 1

        # Level achievements
        current_level = self.achievements_data["level"]
        if current_level >= 10 and self.unlock_achievement("level_10"):
            unlocked.append("level_10")

        if current_level >= 50 and self.unlock_achievement("level_50"):
            unlocked.append("level_50")

        if current_level >= 100 and self.unlock_achievement("level_100"):
            unlocked.append("level_100")

        return unlocked

    def get_progress_to_next_level(self) -> float:
        """Calculate progress percentage to next level.
        
        Returns:
            float: Progress percentage (0-100).
        """
        base_xp = config.GAMIFICATION["initial_xp_for_level"]
        multiplier = config.GAMIFICATION["level_multiplier"]
        current_level = self.achievements_data["level"]
        current_xp = self.achievements_data["total_xp"]

        xp_for_current_level = sum(
            int(base_xp * (multiplier ** (i - 1)))
            for i in range(1, current_level)
        )
        
        xp_for_next_level = int(base_xp * (multiplier ** (current_level - 1)))
        xp_into_current = current_xp - xp_for_current_level

        progress = (xp_into_current / xp_for_next_level) * 100
        return min(100, max(0, progress))

    def get_summary(self) -> Dict[str, Any]:
        """Get complete gamification summary.
        
        Returns:
            Dict with all gamification data.
        """
        return {
            "level": self.achievements_data["level"],
            "total_xp": self.achievements_data["total_xp"],
            "xp_to_next_level": self.get_xp_to_next_level(),
            "progress_percentage": self.get_progress_to_next_level(),
            "achievements_count": len(self.achievements_data["unlocked_achievements"]),
            "badges": self.achievements_data["badges"],
            "statistics": self.achievements_data["statistics"],
        }

    def display_achievements(self) -> None:
        """Display all unlocked achievements in terminal."""
        print(f"\n{config.COLORS['header']}{'='*60}")
        print(f"🏆 YOUR ACHIEVEMENTS")
        print(f"{'='*60}{config.COLORS['reset']}")

        if not self.achievements_data["unlocked_achievements"]:
            print(f"{config.COLORS['warning']}No achievements unlocked yet. Keep going!{config.COLORS['reset']}")
            return

        for achievement in self.achievements_data["unlocked_achievements"]:
            print(f"\n{achievement['icon']} {config.COLORS['success']}{achievement['name']}{config.COLORS['reset']}")
            print(f"   {achievement['description']}")
            print(f"   +{achievement['points']} XP")

    def display_level_progress(self) -> None:
        """Display level and progress bar in terminal."""
        level = self.achievements_data["level"]
        xp = self.achievements_data["total_xp"]
        progress = self.get_progress_to_next_level()
        xp_next = self.get_xp_to_next_level()

        bar_length = 30
        filled = int(bar_length * progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        print(f"\n{config.COLORS['info']}{'='*60}")
        print(f"⭐ LEVEL {level}")
        print(f"{'='*60}{config.COLORS['reset']}")
        print(f"Total XP: {xp}")
        print(f"Next Level: {xp_next} XP needed")
        print(f"Progress: [{bar}] {progress:.1f}%")
