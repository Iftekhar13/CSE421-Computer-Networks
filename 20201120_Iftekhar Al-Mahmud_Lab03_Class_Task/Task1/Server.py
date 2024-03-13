import socket

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

while True:
    conn, addr = server.accept()
    print("connected to ", addr)
    connected = True

    while connected:
        initial = conn.recv(data).decode(format)
        print("Length of the message is to be sent ", initial)

        if initial:
            msg_length = int(initial)
            msg = conn.recv(msg_length).decode(format)

            if msg == disconnected_msg:
                print("Terminating Connection with ", addr)
                conn.send("Nice to meet you".encode(format))
                connected = False
            else:
                print(msg)
                conn.send("Received your message".encode(format))
    conn.close()

