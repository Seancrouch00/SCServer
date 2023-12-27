# SCServer
Secure Log Server

This repository contains a Python-based secure log server that accepts encrypted log messages from clients and writes them to a log file. The server can also generate a self-contained client script with predefined configurations for easy setup.

Features

- Encryption: Uses `cryptography` for secure message encryption and decryption.
- Client Script Generation: Generates a client script with predefined settings (key, IP, port).
- Logging: Logs all received messages with timestamps.
- Error Handling: Robust error handling and logging on both server and client sides.
- Custom Configuration: Allows setting custom IP and port for the server.

Requirements

- Python 3
- `cryptography` Python package

Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-github-username/secure-log-server.git
   ```
2. Navigate to the repository directory:
   ```bash
   cd secure-log-server
   ```
3. Install dependencies:
   ```bash
   pip install cryptography
   ```

Usage

Starting the Server

1. Run the server script:
   ```bash
   python server.py
   ```
2. Follow the prompts to set the server IP and port, and to manage encryption keys.

Generating and Using the Client Script

1. Use the server menu to generate a client script.
2. The `generated_client.py` script will be created in the same directory.
3. Run the client script on any machine:
   ```bash
   python generated_client.py
   ```
4. Enter log messages at the prompt. Type `exit` to stop.

Server Menu Options

- Generate Encryption Key: Creates a new encryption key.
- Set Encryption Key: Sets a custom encryption key.
- View Current Key: Displays the currently set encryption key.
- Start Server: Starts the log server.
- Stop Server: Stops the log server.
- Generate Client Script: Generates a client script with the current configuration.
- Exit: Stops the server (if running) and exits the program.

Contributing

Contributions, issues, and feature requests are welcome.

License

Distributed under the MIT License.
