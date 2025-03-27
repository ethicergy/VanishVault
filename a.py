from self_destruction import track_file_access, load_access_data
import os
import json

# Ensure test file exists
test_filename = "test_file.txt"
upload_path = f"uploads/{test_filename}"
if not os.path.exists(upload_path):
    with open(upload_path, "w") as f:
        f.write("This is a test file.")

# Show initial access count
access_data = load_access_data()
print(f"Initial access count: {access_data.get(test_filename, 0)}")

# Simulate file access 3 times
for i in range(3):
    print(f"Access attempt {i+1}")
    track_file_access(test_filename, max_accesses=3)
    access_data = load_access_data()  # Reload access log
    print(f"Current access count: {access_data.get(test_filename, 'Deleted')}")

# Final check
if os.path.exists(upload_path):
    print("❌ Test Failed: File was NOT deleted after max accesses.")
else:
    print("✅ Test Passed: File was deleted after max accesses.")
