
import socket

def main():
    ip_address = "0.0.0.0"
    port = 12346

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((ip_address, port))
    udp_socket.settimeout(0.1)  # Setting a timeout

    print(f"Listening for incoming messages on port {port}...")

    try:
        while True:
            try:
                data, address = udp_socket.recvfrom(1024)
                print(f"Received message: '{data.decode('utf-8')}' from {address}")
            except socket.timeout:
                pass  # No data received, continue the loop
    except KeyboardInterrupt:
        print("\nExiting...")
        udp_socket.close()

if __name__ == "__main__":
    main()
