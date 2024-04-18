import socket
import selectors
import traceback
import libClient
import threading
import time


hostIP = "127.0.0.1"
hostPort = 65432


selector = selectors.DefaultSelector()


class SocketCommunication:
    
    def __init__(self, tkRoot):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (hostIP, hostPort)

        self.tkRoot = tkRoot
        self.mask = 0b11  # '11' in binary, which means both reading ('01') and writing ('10')

        # server closed unexpectedly
        self.closedUnexpectedly = False

        print("[+] Socket is now created")
        self.bind()



    def bind(self):
        
        print("[=] Trying to bind")
        self.sock.setblocking(False)
        self.sock.connect_ex(self.addr)
        print("[+] Found connection to server")
        self.message = libClient.Message(self.sock, self.addr)
        print("at beginning: ", self.sock)
        
        threading.Thread(target = self.processEvents, args=(self.message,)).start()
    
    

    def processEvents(self, message: libClient.Message):
        try:
            while True:
                try:
                    message.process_events(self.mask)
                    time.sleep(0.02)
                except Exception:
                    # print(
                    #     f"Main: Error: Exception for {message.addr}:\n"
                    #     f"{traceback.format_exc()}"
                    # )
                    message.close(True)
            
                # Check for a socket being monitored to continue.
                if message.sock == None:
                    break
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.tkRoot.exit()