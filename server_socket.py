import asyncio
import socket
from asyncio import AbstractEventLoop

async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    while data := await loop.sock_recv(connection, 1024):
        data = b'hi, ' + data
        await loop.sock_sendall(connection, data)

async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)

        print(f"Got a connection from {address}")
        asyncio.create_task(echo(connection, loop))

async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    await listen_for_connection(server_socket, asyncio.get_event_loop())


asyncio.run(main())

# listen_for_connections is your one central coroutine (qualitatively the same as main) that sets off other coroutines, so it makes more sense to not have it wrapped into a task, and just plain awaited. code won't break if you wrapped that into a task too.. in fact, say you wanted to create 5 server sockets, then wrapping it into tasks would make perfect sense.