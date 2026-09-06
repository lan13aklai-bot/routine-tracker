"""
Notifications system for Daily Routine Tracker
Handles desktop alerts, reminders, and notifications
"""

import threading
import time
from datetime import datetime
import config

try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

class NotificationSystem:
    def __init__(self):
        self.notifications_enabled = config.DEFAULT_SETTINGS.get("notifications_enabled", True)
        self.sound_enabled = config.NOTIFICATIONS.get("sound_enabled", True)
        self.reminder_before = config.NOTIFICATIONS.get("reminder_before_minutes", 5)
        self.notification_queue = []
    
    def send_desktop_notification(self, title, message, duration=5):
        """Send desktop notification"""
        if not self.notifications_enabled:
            return
        
        if PLYER_AVAILABLE:
            try:
                notification.notify(
                    title=title,
                    message=message,
                    timeout=duration,
                    app_icon=None
                )
            except Exception as e:
                print(f"{config.COLORS['warning']}Notification failed: {e}{config.COLORS['reset']}")
        else:
            self.print_notification(title, message)
    
    def print_notification(self, title, message):
        """Print notification to console"""
        print(f"\n{config.COLORS['warning']}{'='*60}")
        print(f"🔔 {title}")
        print(f"{'='*60}{config.COLORS['reset']}")
        print(f"{message}")
    
    def schedule_reminder(self, task_name, routine_name, scheduled_time):
        """Schedule a reminder for a task"""
        if not self.notifications_enabled:
            return
        
        # Run reminder in background thread
        thread = threading.Thread(
            target=self._reminder_worker,
            args=(task_name, routine_name, scheduled_time),
            daemon=True
        )
        thread.start()
    
    def _reminder_worker(self, task_name, routine_name, scheduled_time):
        """Worker thread for reminders"""
        try:
            # Parse scheduled time
            target_hour, target_minute = map(int, scheduled_time.split(':'))
            
            while True:
                now = datetime.now()
                
                # Check if it's time to remind
                if now.hour == target_hour and now.minute == (target_minute - self.reminder_before):
                    title = f"⏰ Routine Reminder"
                    message = f"{routine_name}: {task_name}\nStarting in {self.reminder_before} minutes!"
                    self.send_desktop_notification(title, message)
                    break
                
                # Check every minute
                time.sleep(60)
        except Exception as e:
            print(f"{config.COLORS['error']}Reminder error: {e}{config.COLORS['reset']}")
    
    def notify_task_completed(self, task_name, routine_name, xp_gained=0):
        """Notify when task is completed"""
        title = "✅ Task Completed!"
        message = f"{routine_name}\n{task_name}"
        
        if xp_gained > 0:
            message += f"\n+{xp_gained} XP"
        
        self.send_desktop_notification(title, message, duration=3)
    
    def notify_achievement_unlocked(self, achievement_name, icon):
        """Notify when achievement is unlocked"""
        title = f"🏆 Achievement Unlocked!"
        message = f"{icon} {achievement_name}"
        
        self.send_desktop_notification(title, message, duration=5)
    
    def notify_level_up(self, new_level):
        """Notify when user levels up"""
        title = "⭐ Level Up!"
        message = f"Congratulations! You reached level {new_level}"
        
        self.send_desktop_notification(title, message, duration=5)
    
    def notify_streak(self, streak_count):
        """Notify streak milestone"""
        title = "🔥 Streak Milestone!"
        message = f"Amazing! You have a {streak_count}-day streak!"
        
        self.send_desktop_notification(title, message, duration=5)
    
    def notify_perfect_day(self):
        """Notify perfect day completion"""
        title = "✨ Perfect Day!"
        message = "You completed all tasks today! Amazing work!"
        
        self.send_desktop_notification(title, message, duration=5)
    
    def notify_routine_available(self, routine_name, scheduled_time):
        """Notify when routine is available"""
        title = f"📋 Time for {routine_name}"
        message = f"Your {routine_name} routine is ready to start!"
        
        self.send_desktop_notification(title, message, duration=5)
    
    def send_email_notification(self, recipient, subject, body):
        """Send email notification (stub for future implementation)"""
        if not config.DEFAULT_SETTINGS.get("email_notifications", False):
            return
        
        # TODO: Implement email sending with smtplib
        print(f"{config.COLORS['info']}Email notification stub: {subject}{config.COLORS['reset']}")
    
    def notify_streak_break_warning(self):
        """Notify about potential streak break"""
        title = "⚠️  Streak at Risk!"
        message = "Complete your tasks today to keep your streak alive!"
        
        self.send_desktop_notification(title, message, duration=5)
    
    def check_and_send_reminders(self, routines):
        """Check all routines and send reminders"""
        current_time = datetime.now().strftime("%H:%M")
        reminder_time = datetime.now()
        reminder_time = reminder_time.replace(minute=reminder_time.minute + self.reminder_before)
        reminder_str = reminder_time.strftime("%H:%M")
        
        for routine_name, tasks in routines.items():
            for task in tasks:
                if task.get('scheduled_time') == reminder_str:
                    self.schedule_reminder(task['task'], routine_name, task['scheduled_time'])
    
    def display_notification_status(self):
        """Display notification settings"""
        print(f"\n{config.COLORS['info']}{'='*60}")
        print(f"🔔 NOTIFICATION SETTINGS")
        print(f"{'='*60}{config.COLORS['reset']}")
        print(f"Notifications Enabled: {self.notifications_enabled}")
        print(f"Sound Enabled: {self.sound_enabled}")
        print(f"Reminder Before (minutes): {self.reminder_before}")
        
        if not PLYER_AVAILABLE:
            print(f"{config.COLORS['warning']}Note: Desktop notifications not available (install plyer){config.COLORS['reset']}")
