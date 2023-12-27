import socket
import logging
import threading
import sys
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(filename='server_received_logs.log', level=logging.INFO, format=''%(asctime)s - %(message)s'')

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()

class Server:
    def __init__(self, host='127.0.0.1', port=12345, key=b''):
        self.host = host
        self.port = port
        self.key = key
        self.running = False
        self.server_thread = None

    def start_server(self):
        if not self.key:
            print("Encryption key is not set. Please generate or set a key first.")
            return

        self.running = True
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()
        print("Server started.")

    def stop_server(self):
        if self.running:
            self.running = False
            self.server_thread.join()
            print("Server stopped.")
        else:
            print("Server is not running.")

    def run_server(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()

                print(f"Listening on {self.host}:{self.port}")

                while self.running:
                    conn, addr = s.accept()
                    with conn:
                        print(f"Connected by {addr}")
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            try:
                                decrypted_message = decrypt_message(data, self.key)
                                logging.info(decrypted_message)
                            except Exception as e:
                                logging.error(f"Error decrypting message: {e}")
        except Exception as e:
            logging.error(f"Server encountered an error: {e}")

    def generate_client_script(self):
        client_script = f"""import socket
from cryptography.fernet import Fernet

def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

key = {self.key}
host = '{self.host}'
port = {self.port}

def send_log_to_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        while True:
            user_input = input("Enter your input (or 'exit' to stop): ")
            if user_input.lower() == 'exit':
                break
            encrypted_message = encrypt_message(user_input, key)
            s.sendall(encrypted_message)

if __name__ == "__main__":
    send_log_to_server()
"""
        with open("generated_client.py", "w") as file:
            file.write(client_script)
        print("Client script 'generated_client.py' created.")

def main():
    host = input("Enter server host (default 127.0.0.1): ") or "127.0.0.1"
    port = input("Enter server port (default 12345): ") or 12345

    server = Server(host, int(port))

    while True:
        print("\nServer Menu")
        print("1. Generate Encryption Key")
        print("2. Set Encryption Key")
        print("3. View Current Key")
        print("4. Start Server")
        print("5. Stop Server")
        print("6. Generate Client Script")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            key = generate_key()
            print(f"Generated Key: {key}")
            server.key = key
        elif choice == '2':
            key = input("Enter the encryption key: ").encode()
            server.key = key
            print("Key set successfully.")
        elif choice == '3':
            if server.key:
                print(f"Current Key: {server.key}")
            else:
                print("No key is set.")
        elif choice == '4':
            server.start_server()
        elif choice == '5':
            server.stop_server()
        elif choice == '6':
            if server.key:
                server.generate_client_script()
            else:
                print("Please set an encryption key first.")
        elif choice == '7':
            server.stop_server()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
