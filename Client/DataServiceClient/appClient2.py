import sys
import tkinter as tk
import socketComm as scktComm


import os
conf_path = os.getcwd()
level_up = conf_path[:conf_path.rfind("\\")]
sys.path.append(level_up)

import Presentation2 as pr


# from enum import Enum


# class Action(Enum):
#     REQUESR_NEW_USER = 1
#     NEW_GAME = 2
    



class AppRoot(tk.Tk):
     
    # __init__ function for class TicTacToePresentation 
    def __init__(self, *args, **kwargs): 
         
        # __init__ function for class Tk
        super().__init__(*args, **kwargs)

        # Set up the main container for pages
        self.container = tk.Frame(self)
        # self.container.pack(fill="both", expand=True)
        self.container.pack(side = "top", fill = "both", expand = True)
        
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)


        

        print("[+] creating")
        self.sock = scktComm.SocketCommunication(self)
        print(self.sock)
        self.messageChannel = self.sock.message

        # set up the connection of Message to the GUI
        self.messageChannel.updateAccessToGUI(self)


        self.currentPage = pr.AuthPageToken
        self.currentPageInstance = None

        self.show_page(self.currentPage)



    # to display the current page passed as parameter
    def show_page(self, cont, *rest, isNew: bool = True):
        if isNew:
            if self.currentPageInstance != None:
                self.currentPageInstance.destroy()
            newInstance = cont(self.container, self, *rest)
            self.currentPageInstance = newInstance
        
        # frame = self.frames[cont]
        self.currentPage = cont
        self.currentPageInstance.grid(row = 0, column = 0, sticky ="nsew")
        print("before tkraise: ", self.currentPageInstance)
        self.currentPageInstance.tkraise()
        


    def exit(self):
        self.destroy()
        quit()




def configureRootWindow(root : AppRoot):
    
    root.title("Tic Tac Toe Game")

    # Center the window on the screen
    window_width = 750
    window_height = 500
    
    # screen_width = self.winfo_screenwidth()
    # screen_height = self.winfo_screenheight()
    # x = (screen_width // 2) - (window_width // 2)
    # y = (screen_height // 2) - (window_height // 2)

    # root.geometry(f"{window_width}x{window_height}+{x}+{y}")  # if we want all windows to be put exactly in the center
    root.geometry(f"{window_width}x{window_height}")
    root.configure(bg='#F0F0F0')
    root.resizable(False, False)



if __name__ == "__main__":
 
    
    app = AppRoot()
    configureRootWindow(app)
    print(app)
    
    
    app.mainloop()
    os._exit(0)