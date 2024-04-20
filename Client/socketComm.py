import socket
import traceback
import messageClient
import threading
import time


hostIP = "127.0.0.1"
hostPort = 65432



class SocketCommunication:
    """the class that in charge of managing the communication with the server
    """
    def __init__(self, tkRoot):
        """initialize socket connection and bind it to the (host IP, host PORT) determined above

        Args:
            tkRoot (AppRoot): the app root
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (hostIP, hostPort)

        self.tkRoot = tkRoot
        self.mask = 0b11  # '11' in binary, which means both reading ('01') and writing ('10')

        # server closed unexpectedly
        self.closedUnexpectedly = False

        print("[+] Socket is now created")
        self.bind() # bind to the (host IP, host PORT) address



    def bind(self):
        """define the connection, create a Message manager and output the handling of the communication to a seperate thread
        """
        print("[=] Trying to bind")
        self.sock.setblocking(False)
        self.sock.connect_ex(self.addr)
        print("[+] Found connection to server")
        self.message = messageClient.Message(self.sock, self.addr)
        print("at beginning: ", self.sock)
        
        threading.Thread(target = self.processEvents, args=(self.message,)).start()
    
    

    def processEvents(self, message: messageClient.Message):
        try:
            while True:
                try:
                    message.process_events(self.mask) # process reading and writing
                    time.sleep(0.02) # sleep a while between proccessing each event
                except Exception:
                    # print(
                    #     f"Main: Error: Exception for {message.addr}:\n"
                    #     f"{traceback.format_exc()}"
                    # )
                    message.close(True) # close the Message manager
            
                # Check for a socket being monitored to continue.
                if message.sock == None:
                    break
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.tkRoot.exit()