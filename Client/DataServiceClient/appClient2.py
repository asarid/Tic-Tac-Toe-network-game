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
        self.currentPageInstance.tkraise()


    def exit(self):
        self.destroy()
        quit()
    

#         self.configureRootWindow()
        
#         # self.create_pages_and_widgets()
        
#         print("[+] creating")
#         self.s = scktComm.SocketCommunication(scktComm.hostIP, scktComm.hostPort, self)
        
#         print("creating GUI")
#         self.gui = pr.PresentationController(self, self.s.message)


#         # kwargs={"root": self}

#         # # creating a container
#         # self.container = tk.Frame(self)  
#         # self.container.pack(side = "top", fill = "both", expand = True)
  
#         # self.container.grid_rowconfigure(0, weight = 1)
#         # self.container.grid_columnconfigure(0, weight = 1)
  
#         # # initializing frames to an empty array
#         # self.frames = {}
  
        
#         # # Iterating through a tuple consisting of the different page layouts
#         # # For that, find the names of the classes within the file
#         # frame = inspect.currentframe()
#         # module = inspect.getmodule(frame)
#         # members = inspect.getmembers(module)
#         # class_names = [globals()[member[0]] for member in members if inspect.isclass(member[1]) and member[0] != self.__class__.__name__]
        
#         # #iterate all class names (the different pages) in the file except the first class, i.e. the root:
#         # for F in class_names:
#         #     frame = F(self.container, self)
  
#         #     # initializing frame of that object from startpage, page1, page2 respectively with for loop
#         #     self.frames[F] = frame

#         #     frame.grid(row = 0, column = 0, sticky ="nsew")

#         # self.currentFrame = AuthPageToken
#         # self.show_frame(self.currentFrame)
  


# # if len(sys.argv) != 5:
# #         print(f"Usage: {sys.argv[0]} <host> <port> <action> <value>")
# #         sys.exit(1)



# ##########################################
# ##########################################
    
# # Driver Code
        



# root = AppController()
# root.title("Tic Tac Toe Game")


# root.mainloop()
# os._exit(0)



#########################################################
#########################################################
#########################################################

# # import tkinter as tk

# class Root(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Set up the main container for pages
#         self.container = tk.Frame(self)
#         self.container.pack(fill="both", expand=True)

#     def show_page(self, page_class):
#         """Show a page in the application."""
#         # Remove any existing pages from the container
#         for widget in self.container.winfo_children():
#             widget.pack_forget()

#         # Create the new page instance and add it to the container
#         page = page_class(self.container, self)
#         page.pack(fill="both", expand=True)

# class ExamplePage(tk.Frame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller

#         label = tk.Label(self, text="Example Page")
#         label.pack(padx=10, pady=10)

#         button = tk.Button(self, text="Go to Another Page", command=self.go_to_another_page)
#         button.pack(padx=10, pady=10)

#     def go_to_another_page(self):
#         self.controller.show_page(AnotherPage)

# class AnotherPage(tk.Frame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller

#         label = tk.Label(self, text="Another Page")
#         label.pack(padx=10, pady=10)

#         button = tk.Button(self, text="Go to Example Page", command=self.go_to_example_page)
#         button.pack(padx=10, pady=10)

#     def go_to_example_page(self):
#         self.controller.show_page(ExamplePage)


################################################################
################################################################
################################################################


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