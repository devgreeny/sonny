import subprocess
import os
import time

print("🚀 Starting Sonny...")

# Start Flask backend
backend_path = os.path.join("backend", "app.py")
backend_proc = subprocess.Popen(["python3", backend_path])

# Wait a moment to let Flask start
time.sleep(2)

# Start frontend (HTTP server on port 3000)
frontend_path = os.path.join("frontend")
frontend_proc = subprocess.Popen(["python3", "-m", "http.server", "3000"], cwd=frontend_path)

print("✅ Flask running on http://localhost:5000")
print("✅ Frontend available at http://localhost:3000")
print("🔁 Press Ctrl+C to stop both servers.")

try:
    backend_proc.wait()
    frontend_proc.wait()
except KeyboardInterrupt:
    print("\n🛑 Stopping servers...")
    backend_proc.terminate()
    frontend_proc.terminate()
