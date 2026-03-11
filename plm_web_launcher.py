
import uvicorn
import webbrowser
import threading
import time
import os
import sys
from pathlib import Path

# Add repo root to sys.path
sys.path.append(str(Path(__file__).parent))

def open_browser():
    time.sleep(2)  # Wait for server to start
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    print("--- [PLM WEB LAUNCHER] ---")
    print("Evolution status: Online")
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start FastAPI server
    uvicorn.run("primordial_llm.api:app", host="127.0.0.1", port=8000, log_level="info")
