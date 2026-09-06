"""
Analytics and reporting system for Daily Routine Tracker
Generates charts, statistics, and productivity insights
"""

import json
from datetime import datetime, timedelta
from collections import defaultdict
import config

class Analytics:
    def __init__(self, log_file=config.LOG_FILE, completion_file=config.COMPLETION_FILE):
        self.log_file = log_file
        self.completion_file = completion_file
        self.log_data = self.load_log()
        self.completion_data = self.load_completion()
    
    def load_log(self):
        """Load activity log"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def load_completion(self):
        """Load completion data"""
        if self.completion_file.exists():
            try:
                with open(self.completion_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def get_completion_rate(self, days=7):
        """Get completion rate for last N days"""
        completion_rates = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            if date in self.completion_data:
                total = 0
                completed = 0
                for routine, tasks in self.completion_data[date].items():
                    for task_data in tasks.values():
                        total += 1
                        if task_data.get("completed"):
                            completed += 1
                
                if total > 0:
                    rate = (completed / total) * 100
                    completion_rates.append({"date": date, "rate": rate})
        
        return sorted(completion_rates, key=lambda x: x["date"])
    
    def get_most_productive_hour(self):
        """Get the most productive hour of the day"""
        hour_productivity = defaultdict(int)
        
        for date, activities in self.log_data.items():
            if isinstance(activities, list):
                for activity in activities:
                    if "timestamp" in activity:
                        hour = datetime.fromisoformat(activity["timestamp"]).hour
                        hour_productivity[hour] += 1
        
        if not hour_productivity:
            return None
        
        return max(hour_productivity.items(), key=lambda x: x[1])
    
    def get_task_time_analysis(self):
        """Analyze actual vs estimated time"""
        analysis = defaultdict(lambda: {"estimated": 0, "actual": 0, "count": 0})
        
        for date, activities in self.log_data.items():
            if isinstance(activities, list):
                for activity in activities:
                    task = activity.get("task", "Unknown")
                    actual = activity.get("time_spent", 0)
                    analysis[task]["actual"] += actual
                    analysis[task]["count"] += 1
        
        return analysis
    
    def get_routine_completion_stats(self):
        """Get completion stats per routine"""
        stats = defaultdict(lambda: {"total": 0, "completed": 0})
        
        for date, routines in self.completion_data.items():
            for routine_name, tasks in routines.items():
                if isinstance(tasks, dict):
                    for task_data in tasks.values():
                        stats[routine_name]["total"] += 1
                        if task_data.get("completed"):
                            stats[routine_name]["completed"] += 1
        
        return stats
    
    def get_weekly_summary(self):
        """Get weekly summary statistics"""
        week_data = []
        
        for i in range(6, -1, -1):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            day_name = (datetime.now() - timedelta(days=i)).strftime("%A")
            
            tasks_completed = 0
            if date in self.log_data and isinstance(self.log_data[date], list):
                tasks_completed = len(self.log_data[date])
            
            week_data.append({
                "date": date,
                "day": day_name,
                "tasks_completed": tasks_completed
            })
        
        return week_data
    
    def get_monthly_summary(self):
        """Get monthly summary statistics"""
        month_data = defaultdict(int)
        
        for date, activities in self.log_data.items():
            if isinstance(activities, list):
                month = date[:7]  # YYYY-MM
                month_data[month] += len(activities)
        
        return sorted(month_data.items())
    
    def get_productivity_trend(self, days=30):
        """Get productivity trend over time"""
        trends = []
        
        for i in range(days, 0, -1):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            
            if date in self.log_data and isinstance(self.log_data[date], list):
                tasks = len(self.log_data[date])
                time_spent = sum(t.get("time_spent", 0) for t in self.log_data[date])
                trends.append({
                    "date": date,
                    "tasks": tasks,
                    "time": time_spent
                })
        
        return trends
    
    def draw_ascii_chart(self, data, title, height=10):
        """Draw ASCII bar chart"""
        if not data:
            return f"No data available for {title}"
        
        max_value = max(d.get("value", 0) for d in data) if data else 1
        
        chart = f"\n{config.COLORS['info']}{title}{config.COLORS['reset']}\n"
        chart += "┌" + "─" * 58 + "┐\n"
        
        for item in data[-height:]:
            label = str(item.get("label", ""))[:8]
            value = item.get("value", 0)
            bar_width = int((value / max_value) * 40) if max_value > 0 else 0
            bar = "█" * bar_width
            
            chart += f"│ {label:8} │{bar:40}│ {value}\n"
        
        chart += "└" + "─" * 58 + "┘"
        return chart
    
    def display_weekly_report(self):
        """Display weekly analytics"""
        print(f"\n{config.COLORS['purple']}{'='*60}")
        print(f"📊 WEEKLY ANALYTICS")
        print(f"{'='*60}{config.COLORS['reset']}")
        
        weekly = self.get_weekly_summary()
        total_tasks = sum(d["tasks_completed"] for d in weekly)
        avg_tasks = total_tasks / len(weekly) if weekly else 0
        
        for day in weekly:
            bar_width = day["tasks_completed"] * 2
            bar = "█" * bar_width
            print(f"{day['day']:10} {bar} {day['tasks_completed']} tasks")
        
        print(f"\n{config.COLORS['success']}Total: {total_tasks} tasks")
        print(f"Average: {avg_tasks:.1f} tasks/day{config.COLORS['reset']}")
    
    def display_routine_stats(self):
        """Display routine completion statistics"""
        print(f"\n{config.COLORS['purple']}{'='*60}")
        print(f"📈 ROUTINE COMPLETION STATISTICS")
        print(f"{'='*60}{config.COLORS['reset']}")
        
        stats = self.get_routine_completion_stats()
        
        for routine, data in stats.items():
            if data["total"] > 0:
                percentage = (data["completed"] / data["total"]) * 100
                print(f"\n{config.COLORS['info']}{routine}{config.COLORS['reset']}")
                print(f"  Completed: {data['completed']}/{data['total']} ({percentage:.1f}%)")
    
    def display_productivity_insights(self):
        """Display productivity insights"""
        print(f"\n{config.COLORS['purple']}{'='*60}")
        print(f"🎯 PRODUCTIVITY INSIGHTS")
        print(f"{'='*60}{config.COLORS['reset']}")
        
        # Most productive hour
        most_productive = self.get_most_productive_hour()
        if most_productive:
            hour, count = most_productive
            print(f"\n⏰ Most Productive Hour: {hour:02d}:00 ({count} tasks)")
        
        # Completion rates
        rates = self.get_completion_rate(7)
        if rates:
            avg_rate = sum(r["rate"] for r in rates) / len(rates)
            print(f"📊 Average Completion Rate (7 days): {avg_rate:.1f}%")
        
        # Time analysis
        print(f"\n📋 Time Accuracy (Estimated vs Actual):")
        time_analysis = self.get_task_time_analysis()
        
        for task, data in list(time_analysis.items())[:5]:
            avg_time = data["actual"] / data["count"] if data["count"] > 0 else 0
            print(f"  {task}: {avg_time:.1f} min (completed {data['count']} times)")
    
    def export_monthly_report(self, filename=None):
        """Export monthly report to file"""
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y-%m')}.txt"
        
        with open(filename, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write(f"MONTHLY ANALYTICS REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            # Weekly summary
            f.write("WEEKLY SUMMARY\n")
            f.write("-" * 60 + "\n")
            weekly = self.get_weekly_summary()
            for day in weekly:
                f.write(f"{day['day']:10} - {day['tasks_completed']} tasks completed\n")
            
            # Routine stats
            f.write("\n\nROUTINE STATISTICS\n")
            f.write("-" * 60 + "\n")
            stats = self.get_routine_completion_stats()
            for routine, data in stats.items():
                if data["total"] > 0:
                    percentage = (data["completed"] / data["total"]) * 100
                    f.write(f"{routine}: {data['completed']}/{data['total']} ({percentage:.1f}%)\n")
            
            # Productivity insights
            f.write("\n\nPRODUCTIVITY INSIGHTS\n")
            f.write("-" * 60 + "\n")
            most_productive = self.get_most_productive_hour()
            if most_productive:
                hour, count = most_productive
                f.write(f"Most Productive Hour: {hour:02d}:00\n")
        
        return filename
