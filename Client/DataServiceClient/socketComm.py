import socket
import selectors
import traceback
import libClient
import threading



sel = selectors.DefaultSelector()

hostIP = "127.0.0.1"
hostPort = 65432



class SocketCommunication:
    
    def __init__(self, ip, port, tkRoot):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hostIP = ip
        self.hostPort = port
        self.addr = (self.hostIP, self.hostPort)

        self.tkRoot = tkRoot
        
        #host, port = sys.argv[1], int(sys.argv[2])
        #action, value = sys.argv[3], sys.argv[4]
        #request = create_request(action, value)
        #start_connection(host, port, request)

        print("[+] Socket is now created")
        self.bind()


    def load(self, ip_address, port, text, status, server_info):
        self.ip_address = ip_address
        self.port = port
        self.history = text
        self.status = status
        self.server_info = server_info
        print("[=] Loading attributes is completed")
        return


    def bind(self):
        
        print("[=] Trying to bind")
        self.s.setblocking(False)
        self.s.connect_ex(self.addr)
        print("[+] Found connection to server")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.message = libClient.Message(sel, self.s, self.addr)
        sel.register(self.s, events, data=self.message)
        print("at beginning: ", self.s)
        
        threading.Thread(target = self.processEvents).start()
    
    

    def processEvents(self):
        try:
            while True:
                events = sel.select(timeout=1)
                for key, mask in events:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except Exception:
                        print(
                            f"Main: Error: Exception for {message.addr}:\n"
                            f"{traceback.format_exc()}"
                        )
                        message.close()
                
                # Check for a socket being monitored to continue.
                if not sel.get_map():
                    break
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            sel.close()
            self.tkRoot.exit()
