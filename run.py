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
    backend_dir = os.path.join(root_dir, 'Phase2_BackendAPI')
    frontend_dir = os.path.join(root_dir, 'Phase3_FrontendUI')

    # Check if DB exists
    db_path = os.path.join(root_dir, 'Phase1_DataPipeline', 'zomato.db')
    if not os.path.exists(db_path):
        print("⚠️ Warning: zomato.db not found. Please run Phase 1 data ingestion first.")
        print("  cd Phase1_DataPipeline && python data_ingestion.py")
        sys.exit(1)

    # Copy .env if not exists
    env_path = os.path.join(root_dir, '.env')
    env_example = os.path.join(root_dir, '.env.example')
    if not os.path.exists(env_path) and os.path.exists(env_example):
        import shutil
        shutil.copy(env_example, env_path)
        print("⚠️ Notice: Created a .env file from .env.example. Please open .env and add your GEMINI_API_KEY.")
    
    # Start Backend API
    print_header("Starting FastAPI Backend Server (Port 8000)")
    backend_process = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=backend_dir
    )
    
    time.sleep(2) # Give backend a moment to start
    
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
