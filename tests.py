"""
Unit tests for Daily Routine Tracker
Tests for core functionality and features
"""

import unittest
import json
import tempfile
from pathlib import Path
from datetime import datetime
import config
from utils import DataValidator, Calculator, ProgressBar, ColoredText
from gamification import GamificationSystem
from analytics import Analytics

class TestDataValidator(unittest.TestCase):
    """Test data validation functions"""
    
    def test_validate_time_format_valid(self):
        """Test valid time format"""
        self.assertTrue(DataValidator.validate_time_format("07:00"))
        self.assertTrue(DataValidator.validate_time_format("23:59"))
        self.assertTrue(DataValidator.validate_time_format("00:00"))
    
    def test_validate_time_format_invalid(self):
        """Test invalid time format"""
        self.assertFalse(DataValidator.validate_time_format("25:00"))
        self.assertFalse(DataValidator.validate_time_format("07:60"))
        self.assertFalse(DataValidator.validate_time_format("7:0"))
        self.assertFalse(DataValidator.validate_time_format("invalid"))
    
    def test_validate_priority_valid(self):
        """Test valid priorities"""
        self.assertTrue(DataValidator.validate_priority("high"))
        self.assertTrue(DataValidator.validate_priority("medium"))
        self.assertTrue(DataValidator.validate_priority("low"))
    
    def test_validate_priority_invalid(self):
        """Test invalid priorities"""
        self.assertFalse(DataValidator.validate_priority("urgent"))
        self.assertFalse(DataValidator.validate_priority(""))
    
    def test_validate_routine_name_valid(self):
        """Test valid routine names"""
        self.assertTrue(DataValidator.validate_routine_name("Morning"))
        self.assertTrue(DataValidator.validate_routine_name("Study Routine"))
    
    def test_validate_routine_name_invalid(self):
        """Test invalid routine names"""
        self.assertFalse(DataValidator.validate_routine_name(""))
        self.assertFalse(DataValidator.validate_routine_name("   "))
    
    def test_validate_time_estimate_valid(self):
        """Test valid time estimates"""
        self.assertTrue(DataValidator.validate_time_estimate("10"))
        self.assertTrue(DataValidator.validate_time_estimate("60"))
        self.assertTrue(DataValidator.validate_time_estimate("480"))
    
    def test_validate_time_estimate_invalid(self):
        """Test invalid time estimates"""
        self.assertFalse(DataValidator.validate_time_estimate("0"))
        self.assertFalse(DataValidator.validate_time_estimate("481"))
        self.assertFalse(DataValidator.validate_time_estimate("invalid"))

class TestCalculator(unittest.TestCase):
    """Test calculator functions"""
    
    def test_calculate_completion_percentage(self):
        """Test completion percentage calculation"""
        self.assertEqual(Calculator.calculate_completion_percentage(5, 10), 50.0)
        self.assertEqual(Calculator.calculate_completion_percentage(10, 10), 100.0)
        self.assertEqual(Calculator.calculate_completion_percentage(0, 10), 0.0)
    
    def test_calculate_completion_percentage_zero_total(self):
        """Test completion percentage with zero total"""
        self.assertEqual(Calculator.calculate_completion_percentage(0, 0), 0)
    
    def test_calculate_time_efficiency(self):
        """Test time efficiency calculation"""
        self.assertEqual(Calculator.calculate_time_efficiency(30, 30), 100.0)
        self.assertEqual(Calculator.calculate_time_efficiency(30, 15), 200.0)
        self.assertEqual(Calculator.calculate_time_efficiency(30, 60), 50.0)
    
    def test_calculate_daily_xp(self):
        """Test daily XP calculation"""
        xp = Calculator.calculate_daily_xp(3, False)
        self.assertEqual(xp, 30)  # 3 * 10
        
        xp = Calculator.calculate_daily_xp(3, True)
        self.assertGreater(xp, 30)
    
    def test_calculate_total_routine_time(self):
        """Test total routine time calculation"""
        tasks = [
            {"task": "Task 1", "time": 10},
            {"task": "Task 2", "time": 20},
            {"task": "Task 3", "time": 30}
        ]
        total = Calculator.calculate_total_routine_time(tasks)
        self.assertEqual(total, 60)

class TestProgressBar(unittest.TestCase):
    """Test progress bar functions"""
    
    def test_draw_progress_bar(self):
        """Test drawing progress bar"""
        bar = ProgressBar.draw(5, 10, width=10)
        self.assertIn("[", bar)
        self.assertIn("]", bar)
        self.assertIn("50.0%", bar)
    
    def test_draw_progress_bar_zero(self):
        """Test progress bar with zero"""
        bar = ProgressBar.draw(0, 10, width=10)
        self.assertIn("0.0%", bar)
    
    def test_draw_progress_bar_full(self):
        """Test progress bar at 100%"""
        bar = ProgressBar.draw(10, 10, width=10)
        self.assertIn("100.0%", bar)

class TestColoredText(unittest.TestCase):
    """Test colored text functions"""
    
    def test_success_text(self):
        """Test success text coloring"""
        text = ColoredText.success("Success")
        self.assertIn("Success", text)
        self.assertIn(config.COLORS['success'], text)
    
    def test_error_text(self):
        """Test error text coloring"""
        text = ColoredText.error("Error")
        self.assertIn("Error", text)
        self.assertIn(config.COLORS['error'], text)
    
    def test_warning_text(self):
        """Test warning text coloring"""
        text = ColoredText.warning("Warning")
        self.assertIn("Warning", text)
        self.assertIn(config.COLORS['warning'], text)

class TestGamification(unittest.TestCase):
    """Test gamification system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.gamification = GamificationSystem()
    
    def test_add_xp(self):
        """Test adding XP"""
        initial_xp = self.gamification.achievements_data["total_xp"]
        result = self.gamification.add_xp(50)
        self.assertEqual(self.gamification.achievements_data["total_xp"], initial_xp + 50)
    
    def test_calculate_level(self):
        """Test level calculation"""
        self.gamification.achievements_data["total_xp"] = 0
        self.assertEqual(self.gamification.calculate_level(), 1)
        
        self.gamification.achievements_data["total_xp"] = 100
        self.assertGreaterEqual(self.gamification.calculate_level(), 1)
    
    def test_get_xp_to_next_level(self):
        """Test getting XP to next level"""
        self.gamification.achievements_data["total_xp"] = 0
        self.gamification.achievements_data["level"] = 1
        xp_needed = self.gamification.get_xp_to_next_level()
        self.assertGreater(xp_needed, 0)

class TestAnalytics(unittest.TestCase):
    """Test analytics functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analytics = Analytics()
    
    def test_get_weekly_summary(self):
        """Test getting weekly summary"""
        summary = self.analytics.get_weekly_summary()
        self.assertEqual(len(summary), 7)
    
    def test_get_monthly_summary(self):
        """Test getting monthly summary"""
        summary = self.analytics.get_monthly_summary()
        self.assertIsInstance(summary, list)
    
    def test_calculate_completion_rate(self):
        """Test completion rate calculation"""
        rates = self.analytics.get_completion_rate(7)
        self.assertIsInstance(rates, list)

class TestRoutineData(unittest.TestCase):
    """Test routine data structure"""
    
    def test_default_routines_structure(self):
        """Test default routines have correct structure"""
        routines = config.DEFAULT_ROUTINES
        
        for routine_name, tasks in routines.items():
            self.assertIsInstance(routine_name, str)
            self.assertIsInstance(tasks, list)
            
            for task in tasks:
                self.assertIn("task", task)
                self.assertIn("time", task)
                self.assertIn("priority", task)
                self.assertIn("scheduled_time", task)
    
    def test_priority_values_valid(self):
        """Test all priorities are valid"""
        routines = config.DEFAULT_ROUTINES
        valid_priorities = ["high", "medium", "low"]
        
        for routine_name, tasks in routines.items():
            for task in tasks:
                self.assertIn(task["priority"], valid_priorities)
    
    def test_time_format_valid(self):
        """Test all scheduled times are valid"""
        routines = config.DEFAULT_ROUTINES
        
        for routine_name, tasks in routines.items():
            for task in tasks:
                if task["scheduled_time"] != "N/A":
                    self.assertTrue(DataValidator.validate_time_format(task["scheduled_time"]))

class TestAchievements(unittest.TestCase):
    """Test achievements configuration"""
    
    def test_achievements_have_required_fields(self):
        """Test all achievements have required fields"""
        for key, achievement in config.ACHIEVEMENTS.items():
            self.assertIn("name", achievement)
            self.assertIn("description", achievement)
            self.assertIn("icon", achievement)
            self.assertIn("points", achievement)
    
    def test_achievement_points_positive(self):
        """Test all achievements have positive points"""
        for key, achievement in config.ACHIEVEMENTS.items():
            self.assertGreater(achievement["points"], 0)

def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)

if __name__ == '__main__':
    run_tests()
