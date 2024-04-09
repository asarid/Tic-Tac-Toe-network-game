import sys
import socket
import selectors
import traceback
import libServer
import time
import os

conf_path = os.getcwd()
level_up = conf_path[:conf_path.rfind("\\")]
sys.path.insert(1, level_up)

import BusinessLogic as BL

sel = selectors.DefaultSelector()
BL.selector = sel  # now the BL knows about the selector and can access it



hostIP = "127.0.0.1"
hostPort = 65432
addr = (hostIP, hostPort)



def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    message = libServer.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=message)


# if len(sys.argv) != 3:
#     print(f"Usage: {sys.argv[0]} <host> <port>")
#     sys.exit(1)

#host, port = sys.argv[1], int(sys.argv[2])
    
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind(addr)
lsock.listen()
print(f"Listening on {addr}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try:
                    message.process_events(mask)
                    time.sleep(0.03)
                except Exception:
                    print(
                        f"Main: Error: Exception for {message.addr}:\n"
                        f"{traceback.format_exc()}"
                    )
                    #BL.unregisterUser(message.addr)
                    BL.someoneExitedAbruptly(message.addr)
                    message.close()
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
