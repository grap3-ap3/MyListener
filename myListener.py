#!/usr/bin/python3
# Author: Phil Grimes @grap3_ap3
# Updated for Python 3
# Description: A basic listener that opens a port on localhost, listens to connections, and allows logging.

import socket
import os
from datetime import datetime

# Get user input for setup
listener_address = input("Listener IP Address (ENTER for localhost): ") or 'localhost'
listener_port = input("Listener Port (ENTER for 8008): ") or '8008'
listener_port = int(listener_port)  # Convert port to integer

save_file = input("Do you want to save results? (Y/N): ").strip().upper()

# Initialize the log file if required
log_file_path = 'log.txt' if save_file == 'Y' else None

if log_file_path:
    mode = 'a' if os.path.exists(log_file_path) else 'w'
    with open(log_file_path, mode) as file:
        if mode == 'w':
            file.write('Begin Log: \n')
        file.write(f'New Log Entry: {datetime.now()}\n')
    print(f"Saving results to {log_file_path}")
else:
    print("Not saving results.")

# Set up socket
try:
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((listener_address, listener_port))
    my_socket.listen(1)
    print(f"Listener connected on {listener_address}:{listener_port}")
    print("<CTRL>+C to quit.")
except socket.error as e:
    print(f"Socket error: {e}")
    exit(1)

# Accept incoming connection
try:
    conn, addr = my_socket.accept()
    print(f"Connection from {addr}")
except socket.error as e:
    print(f"Error accepting connection: {e}")
    my_socket.close()
    exit(1)

# Handle data transmission
try:
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break

        if log_file_path:
            with open(log_file_path, 'a') as file:
                file.write(f"{datetime.now()}: {data}\n")
            print(f"Alert Logged: {data}")
        else:
            print(f"Alert Received: {data}")
finally:
    conn.close()
    my_socket.close()
    print("Connection closed.")
