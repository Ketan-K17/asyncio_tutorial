import asyncio
import socket
from asyncio import AbstractEventLoop
import logging

async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    try:
        while data := await loop.sock_recv(connection, 1024):
            print('got data!')
            if data == b'boom\r\n':
                raise Exception("Unexpected network error")
            data = b'hi, ' + data
            await loop.sock_sendall(connection, data)

    except Exception as ex: 
        logging.exception(ex)
    finally:
        connection.close()
    # handling the exception here solves our issue, and also allows us to close the connection safely, in all failure scenarios

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

# Exception handling in tasks is a slightly special business, in that they don't just
# propagate up the call stack... so if you don't retrieve the exception at some point,
# it will go as 'unretrieved', logged when the task is garbage collected. This could
# break your application in subtle ways (silent failures) or clutter logs.

# When a task runs into an error, it's marked done, and its exception is stored as
# whatever exception the coroutine actually raised (e.g. ValueError). You need to
# retrieve this by awaiting the task (or calling .exception()/.result()) at some point.
# Separately, if a task is cancelled, awaiting it raises asyncio.CancelledError instead.

# Hence the rule: always await your tasks (or otherwise retrieve their result) and
# handle any possible exceptions there.