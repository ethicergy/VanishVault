from self_destruction import track_file_access
import os

# Ensure the test file exists before testing
test_filename = "test_file.txt"
if not os.path.exists(f"uploads/{test_filename}"):
    with open(f"uploads/{test_filename}", "w") as f:
        f.write("This is a test file.")

# Simulate accessing the file 3 times
for i in range(3):
    print(f"Access attempt {i+1}")
    track_file_access(test_filename, max_accesses=3)

# Check if file still exists
if os.path.exists(f"uploads/{test_filename}"):
    print("❌ Test Failed: File was NOT deleted after max accesses.")
else:
    print("✅ Test Passed: File was deleted after max accesses.")
