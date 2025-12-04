"""
Script to check if signal data processing is NOT running
"""
import sys
import os

# Add parent directory to path to import backend modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core import database, models

def check_signal_not_running():
    """Check if signal processing job is NOT running"""
    db = database.SessionLocal()
    try:
        # Check for running signal_process jobs
        running_job = (
            db.query(models.AdminJob)
            .filter(
                models.AdminJob.job_type == "signal_process",
                models.AdminJob.status == "running"
            )
            .first()
        )
        
        if running_job:
            print(f"❌ Signal processing IS running!")
            print(f"   Job ID: {running_job.id}")
            print(f"   Started at: {running_job.started_at}")
            print(f"   Triggered by: {running_job.triggered_by}")
            return False
        else:
            print("✅ Signal processing is NOT running")
            
            # Show last job status if available
            last_job = (
                db.query(models.AdminJob)
                .filter(models.AdminJob.job_type == "signal_process")
                .order_by(models.AdminJob.started_at.desc())
                .first()
            )
            
            if last_job:
                print(f"\n   Last job status: {last_job.status}")
                print(f"   Last job started: {last_job.started_at}")
                if last_job.finished_at:
                    print(f"   Last job finished: {last_job.finished_at}")
            else:
                print("\n   No previous signal processing jobs found")
            
            return True
    finally:
        db.close()

if __name__ == "__main__":
    is_not_running = check_signal_not_running()
    sys.exit(0 if is_not_running else 1)

