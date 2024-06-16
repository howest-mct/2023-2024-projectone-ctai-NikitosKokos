import subprocess
import time

def run_flask_app():
    try:
        flask_app = subprocess.Popen(['python', './AI/backend/app.py'])
        return flask_app
    except Exception as e:
        print(f"Failed to start Flask app: {e}")

def run_socket_server():
    try:
        socket_server = subprocess.Popen(['python', './AI/socket_server/app.py'])
        return socket_server
    except Exception as e:
        print(f"Failed to start socket server: {e}")

if __name__ == '__main__':
    flask_app = run_flask_app()
    time.sleep(2)  # Give some time for Flask app to start

    socket_server = run_socket_server()
    time.sleep(2)  # Give some time for Socket server to start

    try:
        while True:
            time.sleep(1)  # Keep the main script running
    except KeyboardInterrupt:
        print("Stopping both servers...")

        # Terminate both servers gracefully
        if flask_app:
            flask_app.terminate()
        if socket_server:
            socket_server.terminate()
        
        print("Both servers stopped.")
