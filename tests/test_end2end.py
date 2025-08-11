import subprocess
import time
import requests
import socket

def get_free_port():
    """ Get a free dynamic port"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

def wait_for_server(port, timeout=10):
    """Wartet, bis der Server auf dem angegebenen Port erreichbar ist."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"http://127.0.0.1:{port}/healthz")
            if response.status_code == 200:
                return
        except requests.ConnectionError:
            pass
        time.sleep(1)
    raise TimeoutError(f"Server auf Port {port} nicht erreichbar.")

def test_full_stack_with_server():
    port = get_free_port()
    server = subprocess.Popen(["uvicorn", "main:app", "--port", str(port), "--host", "127.0.0.1", "--workers", "2" ,"--log-level", "error"])
    wait_for_server(port)
    arguments = {
          "topic": "Git Introduction",
          "audience": "Young IT Professionals",
          "style": "Fun educational content",
          "language": "English"
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }

    body = {
        "jsonrpc": "2.0",
        "params": {
            "arguments": arguments
        }
    }

    try:
        # Send a request on the /tools/call/generate_agenda endpoint
        response = requests.post(f"http://127.0.0.1:{port}/tools/call/generate_agenda", json=body, headers=headers)
        assert response.status_code == 200
        assert "Git" in response.text
    finally:
        # Stop the server
        server.terminate()