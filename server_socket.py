import socket

# setting up a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tcp server socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# binding the socket to an address so that it listens to calls on that address
server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)

# make the server socket listen for connections on above address, the accept() method then blocks until we have a connection, that method will then return the client's socket object, and its address
server_socket.listen()

# mark server_socker as non-blocking
server_socket.setblocking(False)

print("waiting for connections...")


connections = []
try:
    while True:
        try:
            connection, client_address = server_socket.accept()
            connection.setblocking(False)
            print(f'I got a connection from {client_address}!')
            connections.append(connection)
        except BlockingIOError: # you get this error because the given socket may have no data, at which point it asks you to check later..
            pass
        for connection in connections:
            try:
                buffer = b''
                while buffer[-2:] != b'\r\n':
                    data = connection.recv(2)
                    if not data:
                        break
                    else:
                        print(f'I got data: {data}!')
                        buffer = buffer + data

                print(f"All the data is: {buffer}")
                connection.sendall(buffer)
            
            except BlockingIOError:
                pass 
finally:
    server_socket.close()