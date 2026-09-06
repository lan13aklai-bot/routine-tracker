import json
import os
from datetime import datetime
from colorama import Fore, Style, init
import time
from pathlib import Path

# Initialize colorama for colored output
init(autoreset=True)

# File paths
DATA_FILE = "routine_data.json"
LOG_FILE = "routine_log.json"

# Default routine structure
DEFAULT_ROUTINES = {
    "Morning": [
        {"task": "Review daily tasks", "time": 10, "priority": "high", "scheduled_time": "07:00"},
        {"task": "Pack school bag", "time": 15, "priority": "high", "scheduled_time": "07:15"},
        {"task": "30-min reading", "time": 30, "priority": "medium", "scheduled_time": "07:45"}
    ],
    "Study": [
        {"task": "Complete homework", "time": 60, "priority": "high", "scheduled_time": "15:00"},
        {"task": "Review class notes", "time": 30, "priority": "medium", "scheduled_time": "16:15"},
        {"task": "Practice problems", "time": 45, "priority": "medium", "scheduled_time": "17:00"}
    ],
    "Evening": [
        {"task": "Organize study desk", "time": 15, "priority": "low", "scheduled_time": "20:00"},
        {"task": "Log daily achievements", "time": 10, "priority": "medium", "scheduled_time": "20:20"},
        {"task": "Set phone to Do Not Disturb", "time": 5, "priority": "high", "scheduled_time": "21:00"}
    ]
}

class RoutineTracker:
    def __init__(self):
        self.routines = self.load_routines()
        self.completion_data = self.load_completion_data()
        self.log_data = self.load_log_data()
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.initialize_today()

    def load_routines(self):
        """Load routines from file or use defaults"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    return json.load(f)
            except:
                return DEFAULT_ROUTINES
        return DEFAULT_ROUTINES

    def load_completion_data(self):
        """Load task completion data"""
        if os.path.exists("completion_data.json"):
            try:
                with open("completion_data.json", 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def load_log_data(self):
        """Load historical log data"""
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_routines(self):
        """Save routines to file"""
        with open(DATA_FILE, 'w') as f:
            json.dump(self.routines, f, indent=2)

    def save_completion_data(self):
        """Save completion data"""
        with open("completion_data.json", 'w') as f:
            json.dump(self.completion_data, f, indent=2)

    def save_log_data(self):
        """Save log data"""
        with open(LOG_FILE, 'w') as f:
            json.dump(self.log_data, f, indent=2)

    def initialize_today(self):
        """Initialize today's completion data"""
        if self.today not in self.completion_data:
            self.completion_data[self.today] = {}
            for routine_name in self.routines:
                self.completion_data[self.today][routine_name] = {}
                for i, task in enumerate(self.routines[routine_name]):
                    self.completion_data[self.today][routine_name][str(i)] = {
                        "completed": False,
                        "time_spent": 0,
                        "timestamp": None
                    }
            self.save_completion_data()

    def display_routine(self, routine_name, tasks):
        """Display a routine with colored output and completion status"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}{routine_name.upper()} ROUTINE")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        for index, task in enumerate(tasks):
            task_name = task['task'] if isinstance(task, dict) else task
            priority = task.get('priority', 'low') if isinstance(task, dict) else 'low'
            time_est = task.get('time', 0) if isinstance(task, dict) else 0
            scheduled = task.get('scheduled_time', 'N/A') if isinstance(task, dict) else 'N/A'
            
            is_completed = self.completion_data[self.today][routine_name][str(index)]["completed"]
            
            # Color based on priority
            if priority == "high":
                priority_color = Fore.RED
            elif priority == "medium":
                priority_color = Fore.YELLOW
            else:
                priority_color = Fore.GREEN
            
            # Status indicator
            status = f"{Fore.GREEN}✓" if is_completed else f"{Fore.RED}✗"
            
            print(f"  [{index + 1}] {status}{Style.RESET_ALL} {task_name}")
            print(f"      ⏱  {time_est} min | {priority_color}Priority: {priority}{Style.RESET_ALL} | Scheduled: {scheduled}")

    def mark_task_complete(self):
        """Mark a task as complete"""
        self.display_all_routines()
        
        try:
            routine_choice = int(input(f"\n{Fore.CYAN}Enter routine number (0 to cancel): {Style.RESET_ALL}")) - 1
            if routine_choice == -1:
                return
            
            routine_names = list(self.routines.keys())
            if routine_choice < 0 or routine_choice >= len(routine_names):
                print(f"{Fore.RED}Invalid routine!{Style.RESET_ALL}")
                return
            
            routine_name = routine_names[routine_choice]
            self.display_routine(routine_name, self.routines[routine_name])
            
            task_choice = int(input(f"\n{Fore.CYAN}Enter task number (0 to cancel): {Style.RESET_ALL}")) - 1
            if task_choice == -1:
                return
            
            if task_choice < 0 or task_choice >= len(self.routines[routine_name]):
                print(f"{Fore.RED}Invalid task!{Style.RESET_ALL}")
                return
            
            time_spent = int(input(f"{Fore.CYAN}Time spent on this task (minutes): {Style.RESET_ALL}"))
            
            self.completion_data[self.today][routine_name][str(task_choice)]["completed"] = True
            self.completion_data[self.today][routine_name][str(task_choice)]["time_spent"] = time_spent
            self.completion_data[self.today][routine_name][str(task_choice)]["timestamp"] = datetime.now().isoformat()
            
            self.save_completion_data()
            self.log_completion(routine_name, task_choice, time_spent)
            print(f"{Fore.GREEN}✓ Task marked as complete!{Style.RESET_ALL}")
        
        except ValueError:
            print(f"{Fore.RED}Invalid input!{Style.RESET_ALL}")

    def log_completion(self, routine_name, task_index, time_spent):
        """Log task completion to history"""
        if self.today not in self.log_data:
            self.log_data[self.today] = []
        
        task_name = self.routines[routine_name][task_index]['task']
        self.log_data[self.today].append({
            "routine": routine_name,
            "task": task_name,
            "time_spent": time_spent,
            "timestamp": datetime.now().isoformat()
        })
        
        self.save_log_data()

    def display_all_routines(self):
        """Display all routines"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"AVAILABLE ROUTINES")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        for i, routine_name in enumerate(self.routines, 1):
            print(f"  [{i}] {Fore.CYAN}{routine_name}{Style.RESET_ALL}")

    def add_routine(self):
        """Add a new routine"""
        routine_name = input(f"{Fore.CYAN}Enter new routine name: {Style.RESET_ALL}")
        if routine_name in self.routines:
            print(f"{Fore.RED}Routine already exists!{Style.RESET_ALL}")
            return
        
        self.routines[routine_name] = []
        self.completion_data[self.today][routine_name] = {}
        self.save_routines()
        self.save_completion_data()
        print(f"{Fore.GREEN}✓ Routine '{routine_name}' added!{Style.RESET_ALL}")

    def remove_routine(self):
        """Remove a routine"""
        self.display_all_routines()
        try:
            choice = int(input(f"\n{Fore.CYAN}Enter routine number to remove (0 to cancel): {Style.RESET_ALL}")) - 1
            if choice == -1:
                return
            
            routine_names = list(self.routines.keys())
            if choice < 0 or choice >= len(routine_names):
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
                return
            
            routine_name = routine_names[choice]
            del self.routines[routine_name]
            self.save_routines()
            print(f"{Fore.GREEN}✓ Routine '{routine_name}' removed!{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid input!{Style.RESET_ALL}")

    def add_task(self):
        """Add a task to a routine"""
        self.display_all_routines()
        try:
            routine_choice = int(input(f"\n{Fore.CYAN}Enter routine number: {Style.RESET_ALL}")) - 1
            routine_names = list(self.routines.keys())
            
            if routine_choice < 0 or routine_choice >= len(routine_names):
                print(f"{Fore.RED}Invalid routine!{Style.RESET_ALL}")
                return
            
            routine_name = routine_names[routine_choice]
            task_name = input(f"{Fore.CYAN}Enter task name: {Style.RESET_ALL}")
            time_est = int(input(f"{Fore.CYAN}Time estimate (minutes): {Style.RESET_ALL}"))
            priority = input(f"{Fore.CYAN}Priority (high/medium/low): {Style.RESET_ALL}").lower()
            scheduled_time = input(f"{Fore.CYAN}Scheduled time (HH:MM) [optional]: {Style.RESET_ALL}") or "N/A"
            
            if priority not in ["high", "medium", "low"]:
                priority = "medium"
            
            new_task = {
                "task": task_name,
                "time": time_est,
                "priority": priority,
                "scheduled_time": scheduled_time
            }
            
            self.routines[routine_name].append(new_task)
            self.completion_data[self.today][routine_name][str(len(self.routines[routine_name]) - 1)] = {
                "completed": False,
                "time_spent": 0,
                "timestamp": None
            }
            
            self.save_routines()
            self.save_completion_data()
            print(f"{Fore.GREEN}✓ Task '{task_name}' added to '{routine_name}'!{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid input!{Style.RESET_ALL}")

    def remove_task(self):
        """Remove a task from a routine"""
        self.display_all_routines()
        try:
            routine_choice = int(input(f"\n{Fore.CYAN}Enter routine number: {Style.RESET_ALL}")) - 1
            routine_names = list(self.routines.keys())
            
            if routine_choice < 0 or routine_choice >= len(routine_names):
                print(f"{Fore.RED}Invalid routine!{Style.RESET_ALL}")
                return
            
            routine_name = routine_names[routine_choice]
            self.display_routine(routine_name, self.routines[routine_name])
            
            task_choice = int(input(f"\n{Fore.CYAN}Enter task number to remove (0 to cancel): {Style.RESET_ALL}")) - 1
            if task_choice == -1:
                return
            
            if task_choice < 0 or task_choice >= len(self.routines[routine_name]):
                print(f"{Fore.RED}Invalid task!{Style.RESET_ALL}")
                return
            
            removed_task = self.routines[routine_name].pop(task_choice)
            self.save_routines()
            print(f"{Fore.GREEN}✓ Task '{removed_task['task']}' removed!{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid input!{Style.RESET_ALL}")

    def search_task(self):
        """Search for a task across routines"""
        search_term = input(f"{Fore.CYAN}Enter task name to search: {Style.RESET_ALL}").lower()
        found = False
        
        for routine_name, tasks in self.routines.items():
            for i, task in enumerate(tasks):
                if search_term in task['task'].lower():
                    is_completed = self.completion_data[self.today][routine_name][str(i)]["completed"]
                    status = f"{Fore.GREEN}✓" if is_completed else f"{Fore.RED}✗"
                    print(f"\n{status}{Style.RESET_ALL} Found in {Fore.CYAN}{routine_name}{Style.RESET_ALL}: {task['task']}")
                    found = True
        
        if not found:
            print(f"{Fore.YELLOW}No tasks found matching '{search_term}'{Style.RESET_ALL}")

    def show_statistics(self):
        """Show completion statistics for today and streaks"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"COMPLETION STATISTICS - {self.today}")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        total_tasks = 0
        completed_tasks = 0
        total_time = 0
        
        for routine_name, tasks in self.completion_data[self.today].items():
            routine_completed = sum(1 for task in tasks.values() if task["completed"])
            routine_total = len(tasks)
            total_tasks += routine_total
            completed_tasks += routine_completed
            
            time_spent = sum(task["time_spent"] for task in tasks.values())
            total_time += time_spent
            
            percentage = (routine_completed / routine_total * 100) if routine_total > 0 else 0
            print(f"\n{Fore.CYAN}{routine_name}:{Style.RESET_ALL}")
            print(f"  Completion: {routine_completed}/{routine_total} ({percentage:.1f}%)")
            print(f"  Time spent: {time_spent} minutes")
        
        overall_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"OVERALL TODAY:")
        print(f"  Total completion: {completed_tasks}/{total_tasks} ({overall_percentage:.1f}%)")
        print(f"  Total time spent: {total_time} minutes")
        
        # Calculate streak
        streak = self.calculate_streak()
        print(f"  Current streak: {Fore.GREEN}{streak} days{Style.RESET_ALL}")
        print(f"{'='*60}{Style.RESET_ALL}")

    def calculate_streak(self):
        """Calculate consecutive days of 100% completion"""
        streak = 0
        current_date = datetime.now()
        
        while True:
            date_str = current_date.strftime("%Y-%m-%d")
            if date_str not in self.log_data:
                break
            
            # Check if all routines were completed on this date
            total_tasks = sum(len(tasks) for routine, tasks in self.routines.items())
            completed_on_date = len(self.log_data[date_str])
            
            if completed_on_date == total_tasks:
                streak += 1
                current_date = datetime.strptime(date_str, "%Y-%m-%d")
                current_date = current_date.replace(day=current_date.day - 1)
            else:
                break
        
        return streak

    def generate_report(self):
        """Generate a report of activities"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"ACTIVITY REPORT")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        if self.today in self.log_data:
            print(f"\n{Fore.CYAN}{self.today}:{Style.RESET_ALL}")
            for entry in self.log_data[self.today]:
                timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%H:%M")
                print(f"  [{timestamp}] {entry['routine']}: {entry['task']} ({entry['time_spent']} min)")
        else:
            print(f"{Fore.YELLOW}No activities logged for {self.today}{Style.RESET_ALL}")
        
        # Weekly report
        print(f"\n{Fore.CYAN}Weekly Summary:{Style.RESET_ALL}")
        for i in range(6, -1, -1):
            date = datetime.now()
            date = date.replace(day=date.day - i)
            date_str = date.strftime("%Y-%m-%d")
            
            if date_str in self.log_data:
                count = len(self.log_data[date_str])
                print(f"  {date_str}: {count} tasks completed")

    def export_report(self):
        """Export report to file"""
        filename = f"routine_report_{self.today}.txt"
        with open(filename, 'w') as f:
            f.write(f"ROUTINE TRACKER REPORT\n")
            f.write(f"Date: {self.today}\n")
            f.write(f"{'='*60}\n\n")
            
            for routine_name, tasks in self.completion_data[self.today].items():
                f.write(f"{routine_name}:\n")
                for i, task_data in tasks.items():
                    task_info = self.routines[routine_name][int(i)]
                    status = "✓ Completed" if task_data["completed"] else "✗ Pending"
                    f.write(f"  [{status}] {task_info['task']} - Time: {task_data['time_spent']} min\n")
                f.write("\n")
            
            if self.today in self.log_data:
                f.write(f"Activity Log:\n")
                for entry in self.log_data[self.today]:
                    f.write(f"  {entry['routine']}: {entry['task']} ({entry['time_spent']} min)\n")
        
        print(f"{Fore.GREEN}✓ Report exported to {filename}{Style.RESET_ALL}")

    def run_scheduled_check(self):
        """Check and alert for scheduled routines"""
        current_time = datetime.now().strftime("%H:%M")
        print(f"\n{Fore.MAGENTA}Checking scheduled routines for {current_time}...{Style.RESET_ALL}")
        
        for routine_name, tasks in self.routines.items():
            for i, task in enumerate(tasks):
                if task.get('scheduled_time') == current_time:
                    print(f"\n{Fore.YELLOW}⏰ REMINDER: Time for '{task['task']}' in {routine_name} routine!{Style.RESET_ALL}")

    def cli_command(self, command):
        """Handle command-line arguments"""
        parts = command.lower().split()
        
        if parts[0] == "complete" and len(parts) > 1:
            routine_name = " ".join(parts[1:]).title()
            if routine_name in self.routines:
                print(f"Marking all tasks in '{routine_name}' as complete...")
                for i in range(len(self.routines[routine_name])):
                    self.completion_data[self.today][routine_name][str(i)]["completed"] = True
                    self.completion_data[self.today][routine_name][str(i)]["time_spent"] = self.routines[routine_name][i]['time']
                self.save_completion_data()
                print(f"{Fore.GREEN}✓ All tasks completed!{Style.RESET_ALL}")
        
        elif parts[0] == "view" and len(parts) > 1:
            routine_name = " ".join(parts[1:]).title()
            if routine_name in self.routines:
                self.display_routine(routine_name, self.routines[routine_name])
        
        elif parts[0] == "stats":
            self.show_statistics()

    def main_menu(self):
        """Main interactive menu"""
        while True:
            print(f"\n{Fore.MAGENTA}{'='*60}")
            print(f"DAILY ROUTINE TRACKER")
            print(f"{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}1.{Style.RESET_ALL} View all routines")
            print(f"{Fore.CYAN}2.{Style.RESET_ALL} Mark task complete")
            print(f"{Fore.CYAN}3.{Style.RESET_ALL} Add new routine")
            print(f"{Fore.CYAN}4.{Style.RESET_ALL} Remove routine")
            print(f"{Fore.CYAN}5.{Style.RESET_ALL} Add task to routine")
            print(f"{Fore.CYAN}6.{Style.RESET_ALL} Remove task from routine")
            print(f"{Fore.CYAN}7.{Style.RESET_ALL} Search task")
            print(f"{Fore.CYAN}8.{Style.RESET_ALL} View statistics")
            print(f"{Fore.CYAN}9.{Style.RESET_ALL} Generate report")
            print(f"{Fore.CYAN}10.{Style.RESET_ALL} Export report to file")
            print(f"{Fore.CYAN}11.{Style.RESET_ALL} Check scheduled routines")
            print(f"{Fore.CYAN}0.{Style.RESET_ALL} Exit")
            
            choice = input(f"\n{Fore.CYAN}Enter your choice: {Style.RESET_ALL}")
            
            if choice == "1":
                for routine_name in self.routines:
                    self.display_routine(routine_name, self.routines[routine_name])
            elif choice == "2":
                self.mark_task_complete()
            elif choice == "3":
                self.add_routine()
            elif choice == "4":
                self.remove_routine()
            elif choice == "5":
                self.add_task()
            elif choice == "6":
                self.remove_task()
            elif choice == "7":
                self.search_task()
            elif choice == "8":
                self.show_statistics()
            elif choice == "9":
                self.generate_report()
            elif choice == "10":
                self.export_report()
            elif choice == "11":
                self.run_scheduled_check()
            elif choice == "0":
                print(f"\n{Fore.GREEN}Goodbye! Keep up your routines! 🎯{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")

def main():
    """Main entry point"""
    import sys
    
    tracker = RoutineTracker()
    
    # Check for command-line arguments
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])
        tracker.cli_command(command)
    else:
        tracker.main_menu()

if __name__ == "__main__":
    main()
