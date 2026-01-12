import uvicorn
import os
import sys
import socket
import webbrowser
import threading
import time
from multiprocessing import freeze_support

# Ensure backend can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.main import app

def find_free_port(start_port=8000, max_port=8100):
    for port in range(start_port, max_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free ports found")

def open_browser(port):
    time.sleep(1.5) # Wait for server to start
    webbrowser.open(f"http://localhost:{port}")

if __name__ == "__main__":
    freeze_support()
    
    try:
        # Find a free port
        port = find_free_port()
        print(f"Starting server on port {port}...")
        
        # Start browser in a separate thread
        threading.Thread(target=open_browser, args=(port,), daemon=True).start()
        
        # Run the server
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    except Exception as e:
        print(f"Failed to start application: {e}")
        input("Press Enter to exit...")

