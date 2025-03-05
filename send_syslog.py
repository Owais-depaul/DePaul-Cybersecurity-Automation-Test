import socket
import time

def send_syslog(log_file, host, protocol):
    try:
        with open(log_file, "r") as file:
            log_messages = file.readlines()
        
        if protocol.upper() == "TCP":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, 514))
        elif protocol.upper() == "UDP":
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            print("Invalid protocol specified.")
            return

        for message in log_messages:
            if protocol.upper() == "TCP":
                sock.sendall(message.encode())
            elif protocol.upper() == "UDP":
                sock.sendto(message.encode(), (host, 514))
            print(f"Sent: {message.strip()}")
            time.sleep(1)

        sock.close()

    except FileNotFoundError:
        print(f"Error: Log file '{log_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")

send_syslog("system2.log", "127.0.0.1", "UDP")  # Change to TCP if needed
