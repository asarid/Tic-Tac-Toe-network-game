# import sys
import tkinter as tk
import os

# conf_path = os.getcwd()
# level_up = conf_path[:conf_path.rfind("\\")]
# sys.path.append(level_up)

import socketComm as scktComm
import Presentation as pr


class AppRoot(tk.Tk):
    """the root of the application on the client side, initialize GUI and socket communication
    """
    # __init__ function for class TicTacToePresentation 
    def __init__(self, *args, **kwargs): 
        """initialize GUI and socket communicatino hander, at last show the startup page of the application
        """
        super().__init__(*args, **kwargs)

        # Set up the main container for pages
        self.container = tk.Frame(self)
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
        """show a certain page of the GUI. There is an option to send an unlimited number of parameters to this function

        Args:
            cont (tk.Frame): container of the page the caller wanted to move to
            isNew (bool, optional): flag to know if the page should be recreated or just raised. Defaults to True.
        """
        if isNew:
            if self.currentPageInstance != None:
                self.currentPageInstance.destroy() # destroy the last page
            newInstance = cont(self.container, self, *rest) # create a new instance of page
            self.currentPageInstance = newInstance
        
        self.currentPage = cont
        self.currentPageInstance.grid(row = 0, column = 0, sticky ="nsew")
        print("before tkraise: ", self.currentPageInstance)
        self.currentPageInstance.tkraise() # raise the wanted page
        


    def exit(self):
        """exit the app, first destroying the GUI, then quitting the app
        """
        self.destroy()
        quit()




def configureRootWindow(root : AppRoot):
    """configure dimensions and other properties of the a window

    Args:
        root (AppRoot): the root of the app
    """
    root.title("Tic Tac Toe Game")

    # Center the window on the screen
    window_width = 750
    window_height = 500
    
    root.geometry(f"{window_width}x{window_height}")
    root.configure(bg='#F0F0F0')
    root.resizable(False, False) # not resizable, not in x-axis nor y-axis


if __name__ == "__main__":
    
    app = AppRoot()             # create the root of the app
    configureRootWindow(app)    
    
    app.mainloop()              # run the GUI (blocking instruction)
    os._exit(0)                 # after the GUI was closed, exit the app