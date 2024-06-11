import socket
import threading
from detection import capture_images_with_yolo
from split import split_dataset_by_class
from train_detection import train_detection
from best import get_the_best_model
from predict import predict_user
import os

CONCURRENT_CONNECTIONS = 5
semaphore = threading.Semaphore(CONCURRENT_CONNECTIONS)
lock = threading.Lock()
task_running = False
server = None

def handle_client(client_socket):
    global task_running
    with semaphore:
        try:
            with lock:
                if not task_running:
                    task_running = True
                else:
                    response = "Task is already running. Please try again later."
                    client_socket.send(response.encode('utf-8'))
                    return

            task_info = client_socket.recv(1024).decode('utf-8').split(' ')
            task_type = task_info[0]
            user_id = task_info[1]

            if task_type == "CAPTURE":
                response = capture_images_with_yolo(user_id)
            elif task_type == "SPLIT":
                class_name = user_id  # Assuming user_id is used as class_name for splitting
                split_dataset_by_class(class_name)
                response = "Dataset split finished."
            elif task_type == "TRAIN":
                response = train_detection()
            elif task_type == "BEST":
                get_the_best_model()
                response = "The best model found"
            elif task_type == "PREDICT":
                response = predict_user(user_id)
            else:
                response = "Unknown task type."

            client_socket.send(response.encode('utf-8'))
        except Exception as e:
            response = f"Exception in handling client: {e}"
            client_socket.send(response.encode('utf-8'))
        finally:
            client_socket.close()
            with lock:
                task_running = False

def start_server(host='127.0.0.1', port=65432):
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("Stopping the server...")
        if server:
            server.close()
        print("Server stopped.")
