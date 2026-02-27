import subprocess
import sys
import os
import time

def print_header(msg):
    print("\n" + "="*50)
    print(f"> {msg}")
    print("="*50 + "\n")

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, 'api')
    frontend_dir = root_dir  # Frontend is now in the root

    # Check if DB exists
    db_path = os.path.join(root_dir, 'api', 'zomato.db')
    if not os.path.exists(db_path):
        print("⚠️ Warning: zomato.db not found in api/ folder.")
        print("  Please run the optimization script or restore the database.")
        sys.exit(1)

    # Copy .env if not exists
    env_path = os.path.join(root_dir, '.env')
    env_example = os.path.join(root_dir, '.env.example')
    if not os.path.exists(env_path) and os.path.exists(env_example):
        import shutil
        shutil.copy(env_example, env_path)
        print("⚠️ Notice: Created a .env file from .env.example. Please open .env and add your GEMINI_API_KEY.")
    
    # Start Backend API
    print_header("Starting Vercel-Ready Backend (api/index.py on Port 8000)")
    # We use -m uvicorn so it works regardless of shell
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.index:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=root_dir
    )
    
    time.sleep(3) # Give backend a moment to start
    
    # Start Frontend Server
    print_header("Starting Frontend UI Server (Port 8080)")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8080"],
        cwd=frontend_dir
    )

    print_header("Servers are running!")
    print("👉 UI: http://localhost:8080")
    print("👉 API: http://localhost:8000/docs (Swagger UI)")
    print("Press Ctrl+C to stop both servers.")

    try:
        backend_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
