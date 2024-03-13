import socket
import threading

port = 5060
format = "utf-8"
disconnected_msg = "Off"
data = 16
hostname = socket.gethostname()
host_addr = socket.gethostbyname(hostname)

server_socket_address = (host_addr, port)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_socket_address)

server.listen()
print("Server is listening")

def calculate_salary(hours_worked):
    if hours_worked <= 40:
        return hours_worked * 200
    else:
        return 8000 + (hours_worked - 40) * 300

def handler(conn, addr):
    print("Connected to ", addr)
    connected = True

    while connected:
        initial = conn.recv(data).decode(format)
        if initial:
            msg_length = int(initial)
            msg = conn.recv(msg_length).decode(format)

            if msg == disconnected_msg:
                print("Terminating Connection with ", addr)
                conn.send("Goodbye".encode(format))
                connected = False
            elif msg.isdigit():
                hours_worked = int(msg)
                salary = calculate_salary(hours_worked)
                conn.send(f"Salary for {hours_worked} hours is Tk {salary}".encode(format))
            else:
                conn.send("Please send a valid number of hours".encode(format))
    conn.close()

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handler, args=(conn, addr))
    thread.start()
