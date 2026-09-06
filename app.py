"""
Web application for Daily Routine Tracker
Flask-based web interface for managing routines and viewing analytics
"""

from flask import Flask, render_template, request, jsonify, session
from datetime import datetime, timedelta
import json
from pathlib import Path
import config
from tracker import RoutineTracker
from analytics import Analytics
from gamification import GamificationSystem
from notifications import NotificationSystem

app = Flask(__name__)
app.secret_key = config.DEFAULT_SETTINGS.get("app_secret_key", "dev-secret-key")

# Initialize systems
tracker = RoutineTracker()
analytics = Analytics()
gamification = GamificationSystem()
notifications = NotificationSystem()

@app.route('/')
def index():
    """Home page"""
    today = datetime.now().strftime("%Y-%m-%d")
    completion_data = tracker.completion_data.get(today, {})
    
    total_tasks = sum(len(tasks) for tasks in completion_data.values())
    completed_tasks = sum(
        1 for tasks in completion_data.values() 
        for task_data in tasks.values() 
        if task_data.get("completed")
    )
    
    context = {
        "today": today,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        "gamification": gamification.get_summary()
    }
    
    return render_template('index.html', **context)

@app.route('/routines')
def routines():
    """Routines page"""
    routines_data = tracker.routines
    routines_list = []
    
    for routine_name, tasks in routines_data.items():
        routines_list.append({
            "name": routine_name,
            "task_count": len(tasks),
            "total_time": sum(t.get("time", 0) for t in tasks),
            "tasks": tasks
        })
    
    return render_template('routines.html', routines=routines_list)

@app.route('/analytics')
def view_analytics():
    """Analytics page"""
    weekly_data = analytics.get_weekly_summary()
    completion_rates = analytics.get_completion_rate(7)
    routine_stats = analytics.get_routine_completion_stats()
    
    context = {
        "weekly_data": weekly_data,
        "completion_rates": completion_rates,
        "routine_stats": dict(routine_stats),
        "most_productive_hour": analytics.get_most_productive_hour()
    }
    
    return render_template('analytics.html', **context)

@app.route('/gamification')
def view_gamification():
    """Gamification page"""
    summary = gamification.get_summary()
    
    context = {
        "level": summary["level"],
        "total_xp": summary["total_xp"],
        "xp_to_next": summary["xp_to_next_level"],
        "progress": summary["progress_percentage"],
        "achievements_count": summary["achievements_count"],
        "badges": summary["badges"],
        "statistics": summary["statistics"]
    }
    
    return render_template('gamification.html', **context)

@app.route('/api/routines', methods=['GET'])
def api_get_routines():
    """API endpoint to get all routines"""
    routines_data = tracker.routines
    return jsonify(routines_data)

@app.route('/api/routine/<routine_name>', methods=['GET'])
def api_get_routine(routine_name):
    """API endpoint to get a specific routine"""
    if routine_name in tracker.routines:
        return jsonify({
            "name": routine_name,
            "tasks": tracker.routines[routine_name]
        })
    return jsonify({"error": "Routine not found"}), 404

@app.route('/api/routine', methods=['POST'])
def api_add_routine():
    """API endpoint to add a routine"""
    data = request.json
    routine_name = data.get("name")
    tasks = data.get("tasks", [])
    
    if not routine_name:
        return jsonify({"error": "Routine name required"}), 400
    
    result = tracker.add_routine(routine_name, tasks)
    
    if result:
        return jsonify({"success": True, "message": "Routine added"})
    return jsonify({"error": "Routine already exists"}), 400

@app.route('/api/task/<routine_name>/<int:task_index>/complete', methods=['POST'])
def api_complete_task(routine_name, task_index):
    """API endpoint to mark task as complete"""
    data = request.json
    time_spent = data.get("time_spent", 0)
    
    result = tracker.mark_task_complete(routine_name, task_index, time_spent)
    
    if result:
        # Trigger notifications and gamification
        task_name = tracker.routines[routine_name][task_index]["task"]
        
        # Add XP
        xp_result = gamification.add_xp(config.GAMIFICATION["xp_per_task"])
        
        # Check achievements
        achievements = gamification.check_achievement_triggers(tracker)
        
        return jsonify({
            "success": True,
            "xp_gained": config.GAMIFICATION["xp_per_task"],
            "leveled_up": xp_result.get("leveled_up", False),
            "achievements": achievements
        })
    
    return jsonify({"error": "Failed to complete task"}), 400

@app.route('/api/analytics/weekly', methods=['GET'])
def api_weekly_analytics():
    """API endpoint for weekly analytics"""
    weekly_data = analytics.get_weekly_summary()
    return jsonify(weekly_data)

@app.route('/api/analytics/completion-rate', methods=['GET'])
def api_completion_rate():
    """API endpoint for completion rate"""
    days = request.args.get("days", 7, type=int)
    rates = analytics.get_completion_rate(days)
    return jsonify(rates)

@app.route('/api/gamification/summary', methods=['GET'])
def api_gamification_summary():
    """API endpoint for gamification summary"""
    summary = gamification.get_summary()
    return jsonify(summary)

@app.route('/api/gamification/achievements', methods=['GET'])
def api_achievements():
    """API endpoint for achievements"""
    achievements = gamification.achievements_data.get("unlocked_achievements", [])
    return jsonify(achievements)

@app.route('/api/export', methods=['GET'])
def api_export():
    """API endpoint to export data"""
    export_format = request.args.get("format", "json")
    
    export_data = {
        "routines": tracker.routines,
        "completion_data": tracker.completion_data,
        "gamification": gamification.achievements_data,
        "exported_at": datetime.now().isoformat()
    }
    
    return jsonify(export_data)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

@app.before_request
def before_request():
    """Before each request"""
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=7)

def create_app(config_name="development"):
    """Create and configure the Flask app"""
    if config_name == "production":
        app.config['DEBUG'] = False
    else:
        app.config['DEBUG'] = True
    
    return app

if __name__ == '__main__':
    app.run(
        host=config.DEFAULT_SETTINGS.get("app_host", "127.0.0.1"),
        port=config.DEFAULT_SETTINGS.get("app_port", 5000),
        debug=config.DEFAULT_SETTINGS.get("app_debug", True)
    )
