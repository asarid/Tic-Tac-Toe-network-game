import sys
import socket
import selectors
import traceback
import libClient

import tkinter as tk
import inspect
import threading
import Presentation2 as pr
import socketComm as scktComm



from enum import Enum


class Action(Enum):
    REQUESR_NEW_USER = 1
    NEW_GAME = 2
    



class AppController(tk.Tk):
     
    # __init__ function for class TicTacToePresentation 
    def __init__(self, *args, **kwargs): 
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        self.configureRootWindow()
        
        # self.create_pages_and_widgets()
        
        print("[+] creating")
        self.s = scktComm.SocketCommunication(scktComm.hostIP, scktComm.hostPort)
        
        print("creating GUI")
        self.gui = pr.PresentationController(self, self.s.message)



        # # creating a container
        # self.container = tk.Frame(self)  
        # self.container.pack(side = "top", fill = "both", expand = True)
  
        # self.container.grid_rowconfigure(0, weight = 1)
        # self.container.grid_columnconfigure(0, weight = 1)
  
        # # initializing frames to an empty array
        # self.frames = {}
  
        
        # # Iterating through a tuple consisting of the different page layouts
        # # For that, find the names of the classes within the file
        # frame = inspect.currentframe()
        # module = inspect.getmodule(frame)
        # members = inspect.getmembers(module)
        # class_names = [globals()[member[0]] for member in members if inspect.isclass(member[1]) and member[0] != self.__class__.__name__]
        
        # #iterate all class names (the different pages) in the file except the first class, i.e. the root:
        # for F in class_names:
        #     frame = F(self.container, self)
  
        #     # initializing frame of that object from startpage, page1, page2 respectively with for loop
        #     self.frames[F] = frame

        #     frame.grid(row = 0, column = 0, sticky ="nsew")

        # self.currentFrame = AuthPageToken
        # self.show_frame(self.currentFrame)
  


    def configureRootWindow(self):
        # Center the window on the screen
        window_width = 700
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        #root.geometry(f"{window_width}x{window_height}+{x}+{y}")  # if we want all windows to be put exactly in the center
        self.geometry(f"{window_width}x{window_height}")
        self.configure(bg='#F0F0F0')
        self.resizable(False, False)


    # def socket_connections(self):
    #     print("[+] creating")
    #     self.s = scktComm.SocketCommunication(scktComm.hostIP, scktComm.hostPort)

        # print("[=] Loading Attributes")
        # self.s.load(self.ip_address, self.port, self.history,
        #             self.status, self.server_info)
        
        # print("[=] Bindings")
        # self.s.bind()




    # def create_request(action, value):
    #     if action == "search":
    #         return dict(
    #             type="text/json",
    #             encoding="utf-8",
    #             content=dict(action=action, value=value),
    #         )
    #     else:
    #         return dict(
    #             type="binary/custom-client-binary-type",
    #             encoding="binary",
    #             content=bytes(action + value, encoding="utf-8"),
    #         )



# if len(sys.argv) != 5:
#         print(f"Usage: {sys.argv[0]} <host> <port> <action> <value>")
#         sys.exit(1)



##########################################
##########################################
    
# Driver Code
        
root = AppController()
root.title("Tic Tac Toe Game")

root.mainloop()