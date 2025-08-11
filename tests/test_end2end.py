import os
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
        response_generate_agenda = requests.post(f"http://127.0.0.1:{port}/tools/call/generate_agenda", json=body, headers=headers)
        assert response_generate_agenda.status_code == 200
        assert "Git" in response_generate_agenda.text


        response_generate_content = requests.post(f"http://127.0.0.1:{port}/tools/call/generate_content", json=body, headers=headers)
        assert response_generate_content.status_code == 200
        assert "Git" in response_generate_content.text
        with open("tests/e2e.md", "wt") as file:
            file.write(response_generate_content.text)
        assert len(response_generate_content.text) > len(response_generate_agenda.text)

        with open("tests/e2e.md", "rt") as file:
            response_export = requests.post(
                f"http://127.0.0.1:{port}/tools/call/export",
                headers={"Accept": "text/html"},
                files={"file": file}
            )

        assert response_export.status_code == 202
        job_id = response_export.json().get("job_id")

        # now we can pull regularly the export file
        success = False
        for _ in range(50):
            if not success:
                response_export_status = requests.get(f"http://127.0.0.1:{port}/tools/call/export_status?job_id={job_id}")
                if response_export_status.status_code == 200:
                    response_export_status_json = response_export_status.json()
                    if response_export_status_json["status"] == "done":
                        success = True
                        break
                    else:
                        time.sleep(5)
        if success:
            response_export_file = requests.get(f"http://127.0.0.1:{port}/tools/call/export?job_id={job_id}")
            with open(f"tests/e2e.pdf", "wb") as file:
                file.write(response_export_file.content)
        assert success == True
        assert os.path.exists("tests/e2e.pdf")
    finally:
        # Stop the server
        server.terminate()