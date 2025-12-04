"""
Script to check why signal processing is failing
"""
import sys
import os

# Add parent directory to path to import backend modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core import database, models, log_db

def check_signal_error():
    """Check error details from the last failed signal processing job"""
    db = database.SessionLocal()
    try:
        # Get the last failed job
        last_job = (
            db.query(models.AdminJob)
            .filter(models.AdminJob.job_type == "signal_process")
            .order_by(models.AdminJob.started_at.desc())
            .first()
        )
        
        if not last_job:
            print("❌ No signal processing jobs found")
            return
        
        print(f"📋 Last Signal Processing Job:")
        print(f"   ID: {last_job.id}")
        print(f"   Status: {last_job.status}")
        print(f"   Started: {last_job.started_at}")
        print(f"   Finished: {last_job.finished_at}")
        print(f"   Triggered by: {last_job.triggered_by}")
        
        # Check job details for error info
        if last_job.details:
            import json
            try:
                details = json.loads(last_job.details)
                if details.get("error"):
                    print(f"\n❌ Error in job details:")
                    print(f"   {details['error']}")
                if details.get("returncode") is not None:
                    print(f"\n   Return code: {details['returncode']}")
                if details.get("pid"):
                    print(f"   Process ID: {details['pid']}")
            except:
                print(f"\n   Details: {last_job.details}")
        
        # Get logs from log_db
        print(f"\n📝 Job Logs (last 50 lines):")
        print("=" * 80)
        log_content = log_db.get_log(last_job.id)
        if log_content:
            lines = log_content.splitlines()
            # Show last 50 lines
            for line in lines[-50:]:
                print(line)
        else:
            print("   No logs found in database")
            
            # Try to read from log_path if it exists
            if last_job.log_path and last_job.log_path != "DB" and os.path.exists(last_job.log_path):
                print(f"\n   Trying to read from log file: {last_job.log_path}")
                try:
                    with open(last_job.log_path, "r", encoding="utf-8", errors="ignore") as f:
                        file_lines = f.readlines()
                        for line in file_lines[-50:]:
                            print(line.rstrip())
                except Exception as e:
                    print(f"   Error reading log file: {e}")
        
        print("=" * 80)
        
    finally:
        db.close()

if __name__ == "__main__":
    check_signal_error()

