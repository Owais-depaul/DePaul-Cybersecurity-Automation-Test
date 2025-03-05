import socket
import time

def send_syslog(log_file, host, protocol):
    """ Reads a log file and sends syslog messages over TCP or UDP at 1-second intervals. """

    # Validate Protocol
    if protocol.upper() not in ["TCP", "UDP"]:
        print("Invalid protocol specified.")
        return

    # Open Log File
    try:
        with open(log_file, "r") as file:
            logs = file.readlines()
    except FileNotFoundError:
        print(f"Error: Log file '{log_file}' not found.")
        return

    # TCP Connection
    if protocol.upper() == "TCP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, 514))  # Syslog default port
        except Exception as e:
            print(f"TCP Connection failed: {e}")
            return

    # UDP Connection (No need to connect beforehand)
    elif protocol.upper() == "UDP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send Logs One by One with 1-Second Interval
    for log in logs:
        message = log.strip().encode()  # Convert log string to bytes
        try:
            if protocol.upper() == "TCP":
                sock.sendall(message)
            else:
                sock.sendto(message, (host, 514))

            print(f"Sent: {log.strip()}")

        except Exception as e:
            print(f"Error sending log: {e}")
            break

        time.sleep(1)  # Wait 1 second before sending the next log

    sock.close()

# Example Usage:
send_syslog("system2.log", "192.168.1.100", "TCP")  # Replace with actual host IP
