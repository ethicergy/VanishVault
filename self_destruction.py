import os
import json
import logging
import tempfile
import re
import threading
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

# 🔹 Directories
UPLOADS_FOLDER = "uploads/"
ACCESS_LOG_FILE = "file_access_log.json"

# 🔹 Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("vanishvault.log"),
        logging.StreamHandler()
    ]
)

# 🔹 Scheduler Initialization
scheduler = BackgroundScheduler()
scheduler.start()

# 🔹 Thread Lock for Safe File Access
access_lock = threading.Lock()

def secure_filename(filename: str) -> str:
    """Sanitizes file names to prevent directory traversal attacks."""
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)

def schedule_file_deletion(filename, delay_hours):
    filename = secure_filename(filename)
    delete_time = datetime.now() + timedelta(hours=delay_hours)

    existing_jobs = scheduler.get_jobs()
    if any(job.args == [filename] for job in existing_jobs):
        logging.info(f"Deletion for {filename} is already scheduled.")
        return

    scheduler.add_job(delete_file, 'date', run_date=delete_time, args=[filename])
    logging.info(f"Scheduled deletion for {filename} at {delete_time}")

def delete_file(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(UPLOADS_FOLDER, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        remove_from_access_log(filename)
        logging.info(f"File {filename} deleted successfully.")
    else:
        logging.warning(f"Attempted to delete non-existent file: {filename}.")

def track_file_access(filename, max_accesses):
    filename = secure_filename(filename)
    with access_lock:
        access_data = load_access_data()

        if filename not in access_data:
            access_data[filename] = 0

        access_data[filename] += 1

        if access_data[filename] >= max_accesses:
            delete_file(filename)
            del access_data[filename]  # Ensure it's removed after deletion

        save_access_data(access_data)

def load_access_data():
    if not os.path.exists(ACCESS_LOG_FILE):
        return {}
    with open(ACCESS_LOG_FILE, "r") as f:
        return json.load(f)

def save_access_data(access_data):
    """Saves the updated access count data safely to JSON storage."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
    json.dump(access_data, temp_file)
    temp_file.close()
    os.replace(temp_file.name, ACCESS_LOG_FILE)  # Atomic write to prevent corruption

def remove_from_access_log(filename):
    with access_lock:
        access_data = load_access_data()
        if filename in access_data:
            del access_data[filename]
            save_access_data(access_data)
