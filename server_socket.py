"""
What we've built is akin to a big part of what asyncio's event loop does under the
hood. In this case, the events that matter are sockets receiving data. Each iteration of
our event loop and the asyncio event loop is triggered by either a socket event happening, or a timeout triggering an iteration of the loop. In the asyncio event loop,
when any of these two things happen, coroutines that are waiting to run will do so until they either complete or they hit the next await statement. When we hit an await
in a coroutine that utilizes a non-blocking socket, it will register that socket with the
system's selector and keep track that the coroutine is paused waiting for a result. We
can translate this into pseudocode that demonstrates the concept:

paused = []
ready = []
while True:
    paused, new_sockets = run_ready_tasks(ready)
    selector.register(new_sockets)
    timeout = calculate_timeout()
    events = selector.select(timeout)
    ready = process_events(events)
"""

import selectors
import socket
from selectors import SelectorKey
from typing import List, Tuple

selector = selectors.DefaultSelector()

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('127.0.0.1', 8000)
server_socket.setblocking(False)
server_socket.bind(server_address)
server_socket.listen()

selector.register(server_socket, selectors.EVENT_READ)

while True:
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)
    if len(events) == 0:
        print('No events, waiting a bit more!')

    for event, _ in events:
        event_socket = event.fileobj
        if event_socket == server_socket:
            connection, address = server_socket.accept()
            connection.setblocking(False)
            print(f"I got a connection from {address}")
            selector.register(connection, selectors.EVENT_READ)

        else:
            data = event_socket.recv(1024)
            print(f"I got some data: {data}")
            event_socket.send(data)

