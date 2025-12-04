"""
Script to check if signal processing has any scheduled jobs
"""
import sys
import os
import json

# Add parent directory to path to import backend modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core import database, models

def check_signal_schedule():
    """Check if signal processing has any active scheduled jobs"""
    db = database.SessionLocal()
    try:
        # Check for active schedules for signal_process
        schedules = (
            db.query(models.JobSchedule)
            .filter(
                models.JobSchedule.job_type == "signal_process",
                models.JobSchedule.is_active == True
            )
            .all()
        )
        
        if schedules:
            print(f"⚠️  Found {len(schedules)} active schedule(s) for signal processing:")
            for schedule in schedules:
                print(f"\n   Schedule ID: {schedule.id}")
                print(f"   Type: {schedule.schedule_type}")
                print(f"   Value: {schedule.schedule_value}")
                print(f"   Next run: {schedule.next_run_at}")
                print(f"   Last run: {schedule.last_run_at}")
            return True
        else:
            print("✅ No active scheduled jobs for signal processing")
            return False
    finally:
        db.close()

if __name__ == "__main__":
    check_signal_schedule()

