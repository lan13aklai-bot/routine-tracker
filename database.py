"""
Database module for Daily Routine Tracker
Handles SQLite database operations for persistence
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import config

class Database:
    def __init__(self, db_path=config.DB_PATH):
        self.db_path = db_path
        self.connection = None
        self.init_database()
    
    def connect(self):
        """Connect to database"""
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def disconnect(self):
        """Disconnect from database"""
        if self.connection:
            self.connection.close()
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Routines table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS routines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                routine_id INTEGER NOT NULL,
                task_name TEXT NOT NULL,
                estimated_time INTEGER,
                priority TEXT DEFAULT 'medium',
                scheduled_time TEXT,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (routine_id) REFERENCES routines(id)
            )
        ''')
        
        # Completions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                completed_date DATE NOT NULL,
                actual_time INTEGER,
                completed BOOLEAN DEFAULT FALSE,
                completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES tasks(id)
            )
        ''')
        
        # Activity log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                routine_id INTEGER,
                task_name TEXT,
                routine_name TEXT,
                time_spent INTEGER,
                activity_date DATE,
                activity_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES tasks(id),
                FOREIGN KEY (routine_id) REFERENCES routines(id)
            )
        ''')
        
        # Achievements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                achievement_key TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                icon TEXT,
                points INTEGER,
                unlocked_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Streaks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS streaks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                streak_date DATE NOT NULL UNIQUE,
                streak_count INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User stats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_xp INTEGER DEFAULT 0,
                current_level INTEGER DEFAULT 1,
                total_tasks_completed INTEGER DEFAULT 0,
                total_routines_completed INTEGER DEFAULT 0,
                perfect_days INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        self.disconnect()
    
    def add_routine(self, name, description=""):
        """Add a new routine"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO routines (name, description)
                VALUES (?, ?)
            ''', (name, description))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            self.disconnect()
    
    def add_task(self, routine_id, task_name, estimated_time, priority="medium", scheduled_time="N/A", category=""):
        """Add a task to a routine"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO tasks (routine_id, task_name, estimated_time, priority, scheduled_time, category)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (routine_id, task_name, estimated_time, priority, scheduled_time, category))
            conn.commit()
            return cursor.lastrowid
        finally:
            self.disconnect()
    
    def mark_task_complete(self, task_id, actual_time):
        """Mark a task as completed"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute('''
                INSERT INTO completions (task_id, completed_date, actual_time, completed, completed_at)
                VALUES (?, ?, ?, TRUE, CURRENT_TIMESTAMP)
            ''', (task_id, today, actual_time))
            conn.commit()
            return cursor.lastrowid
        finally:
            self.disconnect()
    
    def log_activity(self, routine_id, task_id, routine_name, task_name, time_spent):
        """Log an activity"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute('''
                INSERT INTO activity_log (routine_id, task_id, routine_name, task_name, time_spent, activity_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (routine_id, task_id, routine_name, task_name, time_spent, today))
            conn.commit()
        finally:
            self.disconnect()
    
    def get_routine_by_name(self, name):
        """Get routine by name"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM routines WHERE name = ?', (name,))
        result = cursor.fetchone()
        self.disconnect()
        return result
    
    def get_all_routines(self):
        """Get all routines"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM routines')
        results = cursor.fetchall()
        self.disconnect()
        return results
    
    def get_tasks_by_routine(self, routine_id):
        """Get all tasks for a routine"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tasks WHERE routine_id = ?', (routine_id,))
        results = cursor.fetchall()
        self.disconnect()
        return results
    
    def get_completions_by_date(self, date):
        """Get completions for a specific date"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.*, t.task_name, r.name as routine_name
            FROM completions c
            JOIN tasks t ON c.task_id = t.id
            JOIN routines r ON t.routine_id = r.id
            WHERE c.completed_date = ?
        ''', (date,))
        results = cursor.fetchall()
        self.disconnect()
        return results
    
    def get_daily_completion_rate(self, date):
        """Get completion rate for a date"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as total, SUM(CASE WHEN completed = TRUE THEN 1 ELSE 0 END) as completed
            FROM completions
            WHERE completed_date = ?
        ''', (date,))
        result = cursor.fetchone()
        self.disconnect()
        return result
    
    def add_achievement(self, achievement_key, name, description, icon, points):
        """Add an achievement"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO achievements (achievement_key, name, description, icon, points, unlocked_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (achievement_key, name, description, icon, points))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        finally:
            self.disconnect()
    
    def update_user_stats(self, xp, level, tasks_completed, routines_completed, perfect_days, current_streak, longest_streak):
        """Update user statistics"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_stats 
            SET total_xp = ?, current_level = ?, total_tasks_completed = ?,
                total_routines_completed = ?, perfect_days = ?, 
                current_streak = ?, longest_streak = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
        ''', (xp, level, tasks_completed, routines_completed, perfect_days, current_streak, longest_streak))
        
        if cursor.rowcount == 0:
            cursor.execute('''
                INSERT INTO user_stats (total_xp, current_level, total_tasks_completed,
                    total_routines_completed, perfect_days, current_streak, longest_streak)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (xp, level, tasks_completed, routines_completed, perfect_days, current_streak, longest_streak))
        
        conn.commit()
        self.disconnect()
    
    def get_user_stats(self):
        """Get user statistics"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user_stats WHERE id = 1')
        result = cursor.fetchone()
        self.disconnect()
        return result
    
    def export_to_json(self, filename):
        """Export database to JSON"""
        conn = self.connect()
        cursor = conn.cursor()
        
        export_data = {}
        
        # Export routines
        cursor.execute('SELECT * FROM routines')
        export_data['routines'] = [dict(row) for row in cursor.fetchall()]
        
        # Export tasks
        cursor.execute('SELECT * FROM tasks')
        export_data['tasks'] = [dict(row) for row in cursor.fetchall()]
        
        # Export completions
        cursor.execute('SELECT * FROM completions')
        export_data['completions'] = [dict(row) for row in cursor.fetchall()]
        
        # Export achievements
        cursor.execute('SELECT * FROM achievements')
        export_data['achievements'] = [dict(row) for row in cursor.fetchall()]
        
        self.disconnect()
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        return filename
    
    def backup(self):
        """Create a backup of the database"""
        import shutil
        backup_path = config.BACKUPS_DIR / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy(self.db_path, backup_path)
        return backup_path
