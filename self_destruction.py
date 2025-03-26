import os
import json
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

UPLOADS_FOLDER = "uploads/"
ACCESS_LOG_FILE = "file_access_log.json"

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_file_deletion(filename, delay_hours):
    delete_time = datetime.now() + timedelta(hours = delay_hours)
    scheduler.add_job(delete_file, 'date', run_date = delete_time, args=[filename])
    print(f"Scheduled deletion for {filename} at {delete_time}")


def delete_file(filename):
    file_path = os.path.join(UPLOADS_FOLDER, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        remove_from_access_log(filename)
    else:
        print("File not found")

def track_file_access(filename, max_accesses):
    access_data = load_access_data()

    if filename not in access_data:
        access_data[filename] = 0

    access_data[filename] += 1

    if access_data[filename] >= max_accesses:
            delete_file(filename)
            del access_data[filename]

    save_access_data(access_data)

def load_access_data():
    if not os.path.exists(ACCESS_LOG_FILE):
        return {}
    with open(ACCESS_LOG_FILE, "r") as f:
        return json.load(f)
def save_access_data(access_data):
    """Saves the updated access count data to JSON storage."""
    with open(ACCESS_LOG_FILE, "w") as f:
        json.dump(access_data, f)

def remove_from_access_log(filename):
    access_data = load_access_data()
    if filename in access_data:
        del access_data[filename]
        save_access_data(access_data)