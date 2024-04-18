import sys
import socket
import libServer
import time
import os
import threading

conf_path = os.getcwd()
level_up = conf_path[:conf_path.rfind("\\")]
sys.path.insert(1, level_up)

import BusinessLogic as BL



hostIP = "127.0.0.1"
hostPort = 65432
addr = (hostIP, hostPort)
mask = 0b11 # '11' in binary, which means both reading ('01') and writing ('10')

# dict to store addresses and their corresponding Message. Each pair is { addr : Message }
addrs_messages = {}

BL.addr_Message = addrs_messages




def handle_client(conn, addr):
    message = addrs_messages[addr]
    while True:
        try:
            message.process_events(mask)
            time.sleep(0.03)
        except Exception:
            # print(
            #     f"Main: Error: Exception for {addr}:\n"
            #     f"{traceback.format_exc()}"
            # )
            BL.someoneExitedAbruptly(addr)
            if (message.toExit == False):
                message.close()
            addrs_messages.pop(addr, None)
            break

    
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind(addr)
lsock.listen()
print(f"Listening on {addr}")


try:
    while True:
        conn, addr = lsock.accept()  # Should be ready to read (blocking command)
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        message = libServer.Message(conn, addr)
        addrs_messages[addr] = message
        
        threading.Thread(target=handle_client, args=(conn,addr)).start()

except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
