"""
Gamification system for Daily Routine Tracker
Handles achievements, XP, levels, and badges
"""

import json
from datetime import datetime
from pathlib import Path
import config

class GamificationSystem:
    def __init__(self):
        self.achievements_file = config.ACHIEVEMENTS_FILE
        self.achievements_data = self.load_achievements()
        self.level = self.calculate_level()
        
    def load_achievements(self):
        """Load user achievements from file"""
        if self.achievements_file.exists():
            try:
                with open(self.achievements_file, 'r') as f:
                    return json.load(f)
            except:
                return self.initialize_achievements()
        return self.initialize_achievements()
    
    def initialize_achievements(self):
        """Initialize achievements data"""
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
                "tasks_created": 0
            }
        }
    
    def save_achievements(self):
        """Save achievements to file"""
        config.DATA_DIR.mkdir(exist_ok=True)
        with open(self.achievements_file, 'w') as f:
            json.dump(self.achievements_data, f, indent=2)
    
    def add_xp(self, amount, reason=""):
        """Add XP to user"""
        self.achievements_data["total_xp"] += amount
        old_level = self.achievements_data["level"]
        self.achievements_data["level"] = self.calculate_level()
        
        self.save_achievements()
        
        # Check if leveled up
        if self.achievements_data["level"] > old_level:
            return {
                "leveled_up": True,
                "new_level": self.achievements_data["level"],
                "xp_gained": amount
            }
        return {"leveled_up": False, "xp_gained": amount}
    
    def calculate_level(self):
        """Calculate level based on total XP"""
        total_xp = self.achievements_data["total_xp"]
        level = 1 + (total_xp // config.GAMIFICATION["level_threshold"])
        return level
    
    def get_xp_to_next_level(self):
        """Get XP needed to reach next level"""
        current_xp = self.achievements_data["total_xp"]
        xp_for_current_level = (self.achievements_data["level"] - 1) * config.GAMIFICATION["level_threshold"]
        xp_to_next = config.GAMIFICATION["level_threshold"] - (current_xp - xp_for_current_level)
        return xp_to_next
    
    def unlock_achievement(self, achievement_key):
        """Unlock an achievement"""
        if achievement_key not in self.achievements_data["unlocked_achievements"]:
            self.achievements_data["unlocked_achievements"].append({
                "key": achievement_key,
                "name": config.ACHIEVEMENTS[achievement_key]["name"],
                "description": config.ACHIEVEMENTS[achievement_key]["description"],
                "icon": config.ACHIEVEMENTS[achievement_key]["icon"],
                "points": config.ACHIEVEMENTS[achievement_key]["points"],
                "unlocked_at": datetime.now().isoformat()
            })
            
            # Add points
            points = config.ACHIEVEMENTS[achievement_key]["points"]
            self.add_xp(points, f"Achievement: {achievement_key}")
            self.save_achievements()
            return True
        return False
    
    def add_badge(self, badge_name):
        """Add a badge to user"""
        if badge_name not in self.achievements_data["badges"]:
            self.achievements_data["badges"].append(badge_name)
            self.save_achievements()
            return True
        return False
    
    def update_statistic(self, stat_name, increment=1):
        """Update a statistic"""
        if stat_name in self.achievements_data["statistics"]:
            self.achievements_data["statistics"][stat_name] += increment
            self.save_achievements()
    
    def check_achievement_triggers(self, tracker):
        """Check if any achievements should be unlocked"""
        unlocked = []
        stats = self.achievements_data["statistics"]
        
        # First task
        if stats["total_tasks_completed"] == 1:
            if self.unlock_achievement("first_task"):
                unlocked.append("first_task")
        
        # Streaks
        if tracker.completion_data.get("current_streak", 0) >= 3:
            if self.unlock_achievement("streak_3"):
                unlocked.append("streak_3")
        
        if tracker.completion_data.get("current_streak", 0) >= 7:
            if self.unlock_achievement("streak_7"):
                unlocked.append("streak_7")
        
        if tracker.completion_data.get("current_streak", 0) >= 30:
            if self.unlock_achievement("streak_30"):
                unlocked.append("streak_30")
        
        # Perfect day
        if tracker.completion_data.get("perfect_day", False):
            if self.unlock_achievement("perfect_day"):
                unlocked.append("perfect_day")
            stats["perfect_days"] += 1
        
        # Collections
        if stats["routines_created"] >= 5:
            if self.unlock_achievement("collector"):
                unlocked.append("collector")
        
        if stats["tasks_created"] >= 20:
            if self.unlock_achievement("task_master"):
                unlocked.append("task_master")
        
        # Level achievements
        if self.achievements_data["level"] >= 10:
            if self.unlock_achievement("level_10"):
                unlocked.append("level_10")
        
        return unlocked
    
    def get_progress_to_next_level(self):
        """Get progress percentage to next level"""
        xp_needed = config.GAMIFICATION["level_threshold"]
        xp_for_current = (self.achievements_data["level"] - 1) * xp_needed
        xp_current = self.achievements_data["total_xp"] - xp_for_current
        
        progress = (xp_current / xp_needed) * 100
        return min(100, max(0, progress))
    
    def get_summary(self):
        """Get gamification summary"""
        return {
            "level": self.achievements_data["level"],
            "total_xp": self.achievements_data["total_xp"],
            "xp_to_next_level": self.get_xp_to_next_level(),
            "progress_percentage": self.get_progress_to_next_level(),
            "achievements_count": len(self.achievements_data["unlocked_achievements"]),
            "badges": self.achievements_data["badges"],
            "statistics": self.achievements_data["statistics"]
        }
    
    def display_achievements(self):
        """Display all unlocked achievements"""
        print(f"\n{config.COLORS['purple']}{'='*60}")
        print(f"🏆 YOUR ACHIEVEMENTS")
        print(f"{'='*60}{config.COLORS['reset']}")
        
        if not self.achievements_data["unlocked_achievements"]:
            print(f"{config.COLORS['warning']}No achievements unlocked yet. Keep going!{config.COLORS['reset']}")
            return
        
        for achievement in self.achievements_data["unlocked_achievements"]:
            print(f"\n{achievement['icon']} {config.COLORS['success']}{achievement['name']}{config.COLORS['reset']}")
            print(f"   {achievement['description']}")
            print(f"   +{achievement['points']} XP")
    
    def display_level_progress(self):
        """Display level and progress"""
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
