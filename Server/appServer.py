import socket
import messageServer
import time
import threading

# conf_path = os.getcwd()
# level_up = conf_path[:conf_path.rfind("\\")]
# sys.path.insert(1, level_up)

import BusinessLogic as BL


def handle_client(conn: socket, addr: tuple):
    """handle a single connection

    Args:
        conn (socket): a socket object
        addr (tuple): (IP,PORT)
    """
    message = addrs_messages[addr] # get a messaeg manager of the user with 'addr' address
    while True:
        try:
            message.process_events(mask) # manage read and write operations of this Message
            time.sleep(0.03)             # sleep between each call (solved the high CPU consumption problem)
        except Exception:
            # print(
            #     f"Main: Error: Exception for {addr}:\n"
            #     f"{traceback.format_exc()}"
            # )
            BL.someoneExitedAbruptly(addr) # notify other users if a player of their game exited abruptly
            if (message.toExit == False): # if it was True, the instruction 'message.close()' would already been called earlier
                message.close()
            addrs_messages.pop(addr, None) # pop the massage manager of this user from the dict
            break

if __name__ == "__main__":

    hostIP = "127.0.0.1"
    hostPort = 65432
    addr = (hostIP, hostPort)
    mask = 0b11 # '11' in binary, which means both reading ('01') and writing ('10')

    # dict to store addresses and their corresponding Message. Each pair is { addr : Message }
    addrs_messages = {}

    BL.addr_Message = addrs_messages # share a reference of all the sockets with the BL layer



        
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # make a socket communicate using IPv4 and TCP protocols
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind(addr)
    lsock.listen()
    print(f"Listening on {addr}")


    try:
        while True:
            conn, addr = lsock.accept()  # wait for a new connection (blocking command)
            print(f"Accepted connection from {addr}")
            conn.setblocking(False)      # set to False, we don't want a connection to block other connections from being handled
            message = messageServer.Message(conn, addr) # create a message manager (manage communication for 'addr' address)
            addrs_messages[addr] = message
            
            threading.Thread(target=handle_client, args=(conn,addr)).start() # handle this connection in a seperate thread (the GUI has to be the primarly thread)

    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
