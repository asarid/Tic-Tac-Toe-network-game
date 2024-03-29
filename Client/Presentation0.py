import tkinter as tk
import time
from tkinter import ttk
from tkinter import messagebox
import inspect
import threading
import DataServiceClient.libClient as message
import DataServiceClient.socketComm as comm

MEDIUMFONT = ("Verdana", 18)
LARGEFONT = ("Verdana", 30)


class PresentationController:
 
    # __init__ function for class TicTacToePresentation 
    def __init__(self, parent, messageChannel : message.Message): 
         
        self.messageChannel = messageChannel
        
        # creating a container
        self.container = tk.Frame(parent)  
        self.container.pack(side = "top", fill = "both", expand = True)
  
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {}  
  
        
        # Iterating through a tuple consisting of the different page layouts
        # For that, find the names of the classes within the file
        frame = inspect.currentframe()
        module = inspect.getmodule(frame)
        members = inspect.getmembers(module)
        class_names = [globals()[member[0]] for member in members if inspect.isclass(member[1]) and member[0] != self.__class__.__name__]
        
        #iterate all class names (the different pages) in the file except the first class, i.e. the root:
        for F in class_names:
            frame = F(self.container, self)
  
            # initializing frame of that object from startpage, page1, page2 respectively with for loop
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.currentFrame = AuthPageToken
        self.show_frame(self.currentFrame)
    

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        self.currentFrame = frame
        frame.tkraise()

    # def messageChannel(self, comm : message.Message):
    #     messageChannel = comm

# first window frame startpage
  
class StartPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
         
        # label of frame Layout 2
        label = ttk.Label(self, text ="Startpage", font = LARGEFONT)
         
        # putting the grid in its place by using grid
        label.grid(row = 0, column = 4, padx = 10, pady = 10) 
  
        button1 = ttk.Button(self, text ="Page 1", command = lambda : controller.show_frame(Page1))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text ="Page 2", command = lambda : controller.show_frame(Page2))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
  
          
  
  
# second window frame page1 
class Page1(tk.Frame):
     
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page 1", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="StartPage",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place 
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text ="Page 2",
                            command = lambda : controller.show_frame(Page2))
     
        # putting the button in its place by 
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
  
  
  
  
# third window frame page2
class Page2(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page 2", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text layout2
        button1 = ttk.Button(self, text ="Page 1", command = lambda : controller.show_frame(Page1))
     
        # putting the button in its place by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # button to show frame 3 with text layout3
        button2 = ttk.Button(self, text ="Startpage",
                            command = lambda : controller.show_frame(StartPage))

        # putting the button in its place by using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)


""" Page for authwntication with username and password
"""
class AuthPagePassword(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Create headline
        headline_label = ttk.Label(self, text="Tic Tac Toe", font=LARGEFONT, background='#F0F0F0', foreground='#333333')
        #headline_label.grid(row=0, column=0, columnspan=2, pady=(50, 20), sticky="n")
        headline_label.place(relx=0.5, rely=0.1, anchor="center")

        # Group auth objects 
        detailsFrame = tk.Frame(self, bg="#F0F0F0", highlightbackground="#F0F0F0", highlightthickness=0)
        #authFrame.grid(row=1, column=0, columnspan=2, pady=(50, 20), sticky="n")
        detailsFrame.place(relx=0.5, rely=0.5, anchor="center")

        # Create username label and entry
        username_label = ttk.Label(detailsFrame, text="Username ", font=MEDIUMFONT, background='#F0F0F0', foreground='#333333')
        username_label.grid(row=0, column=0, pady=(0, 20), sticky="e")
        self.username_entry = tk.Entry(detailsFrame, font=("Verdana", 18))
        self.username_entry.grid(row=0, column=1, pady=(0, 20), sticky="w")

        # Create password label and entry
        password_label = ttk.Label(detailsFrame, text="Password ", font=MEDIUMFONT, background='#F0F0F0', foreground='#333333')
        password_label.grid(row=1, column=0, pady=(0, 20), sticky="e")
        self.password_entry = tk.Entry(detailsFrame, show="*", font=("Verdana", 18))
        self.password_entry.grid(row=1, column=1, pady=(0, 20), sticky="w")

        # Create login button
        login_button = tk.Button(detailsFrame, text="Sign in", command=self.authenticate, font=("Verdana", 18), bg='#4CAF50', fg='white')
        login_button.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="n")
        #login_button.place(relx=0.5, rely=0.9, anchor="center")


        # Create Exit button
        exit_button = tk.Button(self, text=" Exit ", command=self.exitTheGame, font=("Verdana", 18), bg='#4CAF50', fg='white')
        #login_button.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="n")
        exit_button.place(relx=0.5, rely=0.9, anchor="center")

    
    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Replace this with your authentication logic
        if username == "admin" and password == "password":
            messagebox.showinfo("Login Successful", "Welcome, {}".format(username))
            # Add code to navigate to the next page or perform further actions after authentication
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def exitTheGame(self):
        pass




class AuthPageToken(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        # Create headline
        headline_label = ttk.Label(self, text="Tic Tac Toe", font=LARGEFONT, background='#F0F0F0', foreground='#333333')
        headline_label.place(relx=0.5, rely=0.1, anchor="center")

        # Group auth objects
        detailsFrame = tk.Frame(self, bg="#F0F0F0", highlightbackground="#F0F0F0", highlightthickness=0)
        detailsFrame.place(relx=0.5, rely=0.5, anchor="center")

        # Create username label and entry
        token_label = ttk.Label(detailsFrame, text="Enter Your Token: ", font=MEDIUMFONT, background='#F0F0F0', foreground='#333333')
        token_label.grid(row=0, column=0, pady=(0, 20), sticky="e")
        self.token_entry = tk.Entry(detailsFrame, font=("Verdana", 18))
        self.token_entry.grid(row=0, column=1, pady=(0, 20), sticky="w")
        
        # Create login button
        login_button = tk.Button(detailsFrame, text="Log in", command=self.authenticate, font=("Verdana", 18), bg='#4CAF50', fg='white')
        login_button.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="n")
        


        # Create Exit button
        exit_button = tk.Button(self, text=" Exit ", command=self.exitTheGame, font=("Verdana", 18), bg='#4CAF50', fg='white')
        exit_button.place(relx=0.6, rely=0.9)

        
        # Create Sign Up button
        signup_button = tk.Button(self, text="Sign Up", command=self.signUp, font=("Verdana", 18), bg='#4CAF50', fg='white')
        signup_button.place(relx=0.3, rely=0.9)



    def getTokenEntry(self):
        return self.token_entry.get()
    
    def setTokenEntry(self, tokenGenerated):
        self.token_entry.insert(0,tokenGenerated)


    def authenticate(self):
        token = self.token_entry.get()
        self.controller.messageChannel.setRequest("veteranUser", token)
        
        # Replace this with your authentication logic
        if token == "admin":
            messagebox.showinfo("Login Successful", "Welcome, {}".format(token))
            # Add code to navigate to the next page or perform further actions after authentication
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def signUp(self):
        pass

    def exitTheGame(self):
        pass
    


class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Create headline
        headline_label = ttk.Label(self, text="Tic Tac Toe", font=LARGEFONT, background='#F0F0F0', foreground='#333333')
        headline_label.place(relx=0.5, rely=0.1, anchor="center")

        # Group auth objects 
        detailsFrame = tk.Frame(self, bg="#F0F0F0", highlightbackground="#F0F0F0", highlightthickness=0)
        detailsFrame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Choose nikname
        nikName_label = ttk.Label(detailsFrame, text="Enter Your Nik Name: ", font=MEDIUMFONT, background='#F0F0F0', foreground='#333333')
        nikName_label.grid(row=0, column=0, pady=(0, 20), sticky="e")
        self.nikName_entry = tk.Entry(detailsFrame, font=("Verdana", 18))
        self.nikName_entry.grid(row=0, column=1, pady=(0, 20), sticky="w")

        # Create User button
        create_button = tk.Button(detailsFrame, text="Create New User", command=self.createUser, font=("Verdana", 18), bg='#4CAF50', fg='white')
        create_button.grid(row=1, column=0, columnspan=2, pady=(20, 50), sticky="n")

        # New Token label
        self.token_label1 = ttk.Label(detailsFrame, text="Your unique token is:", font=MEDIUMFONT, background='#F0F0F0', foreground='#333333')
        self.token_label1.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="w")
        self.token_label1.grid_forget()

        # actual token label
        self.token_label2 = ttk.Label(detailsFrame, text="_______", font=MEDIUMFONT, background='#F0F0F0', foreground='#333333')
        self.token_label2.grid(row=2, column=1, columnspan=2, pady=(20, 50), sticky="w")
        self.token_label2.grid_forget()



        # Create Exit button
        exit_button = tk.Button(self, text=" Exit ", command=self.exitTheGame, font=("Verdana", 18), bg='#4CAF50', fg='white')
        exit_button.place(relx=0.6, rely=0.9)

        
        # Create Sign In button
        signIn_button = tk.Button(self, text="Sign In", command=self.signIn, font=("Verdana", 18), bg='#4CAF50', fg='white')
        signIn_button.place(relx=0.3, rely=0.9)



    def createUser(self):
        token = 123

        # Replace this with your authentication logic
        if token == "admin":
            messagebox.showinfo("Login Successful", "Welcome, {}".format(token))
            # Add code to navigate to the next page or perform further actions after authentication
        else:
            #messagebox.showerror("Login Failed", "Invalid username or password")
            self.token_label1.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="w")
            self.token_label2.grid(row=2, column=1, columnspan=2, pady=(20, 50), sticky="w")


    def signIn(self):
        pass

    def exitTheGame(self):
        pass



class MainMenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Create headline
        headline_label = ttk.Label(self, text="Tic Tac Toe - Main menu", font=LARGEFONT, background='#F0F0F0', foreground='#333333')
        headline_label.place(relx=0.5, rely=0.1, anchor="center")

        # Group auth objects 
        optionsFrame = tk.Frame(self, bg="#F0F0F0", highlightbackground="#F0F0F0", highlightthickness=0)
        optionsFrame.place(relx=0.5, rely=0.5, anchor="center")
        
        # New Game button
        create_button = tk.Button(optionsFrame, text="New Game", command=self.createUser, font=("Verdana", 18), bg='#4CAF50', fg='white')
        create_button.grid(row=0, column=0, columnspan=2, pady=(20, 50))

        # Join Game button
        create_button = tk.Button(optionsFrame, text="Join A Game", command=self.createUser, font=("Verdana", 18), bg='#4CAF50', fg='white')
        create_button.grid(row=1, column=0, columnspan=2, pady=(20, 50))

        # View Leadership Table button
        create_button = tk.Button(optionsFrame, text="View Leadership Table", command=self.createUser, font=("Verdana", 18), bg='#4CAF50', fg='white')
        create_button.grid(row=2, column=0, columnspan=2, pady=(20, 50))




        # Create Exit button
        exit_button = tk.Button(self, text=" Exit ", command=self.exitTheGame, font=("Verdana", 18), bg='#4CAF50', fg='white')
        exit_button.place(relx=0.6, rely=0.9)

        
        # Create Log out button
        logout_button = tk.Button(self, text="Logout", command=self.signIn, font=("Verdana", 18), bg='#4CAF50', fg='white')
        logout_button.place(relx=0.3, rely=0.9)



    def createUser(self):
        token = 123

        # Replace this with your authentication logic
        if token == "admin":
            messagebox.showinfo("Login Successful", "Welcome, {}".format(token))
            # Add code to navigate to the next page or perform further actions after authentication
        else:
            #messagebox.showerror("Login Failed", "Invalid username or password")
            self.token_label1.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="w")
            self.token_label2.grid(row=2, column=1, columnspan=2, pady=(20, 50), sticky="w")


    def signIn(self):
        pass

    def exitTheGame(self):
        pass


class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Create headline
        headline_label = ttk.Label(self, text="Tic Tac Toe - Main menu", font=LARGEFONT, background='#F0F0F0', foreground='#333333')
        headline_label.place(relx=0.5, rely=0.1, anchor="center")

        # Group auth objects 
        optionsFrame = tk.Frame(self, bg="#F0F0F0", highlightbackground="#F0F0F0", highlightthickness=0)
        optionsFrame.place(relx=0.5, rely=0.5, anchor="center")
        
        # New Game button
        create_button = tk.Button(optionsFrame, text="New Game", command=self.createUser, font=("Verdana", 18), bg='#4CAF50', fg='white')
        create_button.grid(row=0, column=0, columnspan=2, pady=(20, 50))

        # Join Game button
        create_button = tk.Button(optionsFrame, text="Join A Game", command=self.createUser, font=("Verdana", 18), bg='#4CAF50', fg='white')
        create_button.grid(row=1, column=0, columnspan=2, pady=(20, 50))

        # View Leadership Table button
        create_button = tk.Button(optionsFrame, text="View Leadership Table", command=self.createUser, font=("Verdana", 18), bg='#4CAF50', fg='white')
        create_button.grid(row=2, column=0, columnspan=2, pady=(20, 50))




        # Create Exit button
        exit_button = tk.Button(self, text=" Exit ", command=self.exitTheGame, font=("Verdana", 18), bg='#4CAF50', fg='white')
        exit_button.place(relx=0.6, rely=0.9)

        
        # Create Log out button
        logout_button = tk.Button(self, text="Logout", command=self.signIn, font=("Verdana", 18), bg='#4CAF50', fg='white')
        logout_button.place(relx=0.3, rely=0.9)



    def createUser(self):
        token = 123

        # Replace this with your authentication logic
        if token == "admin":
            messagebox.showinfo("Login Successful", "Welcome, {}".format(token))
            # Add code to navigate to the next page or perform further actions after authentication
        else:
            #messagebox.showerror("Login Failed", "Invalid username or password")
            self.token_label1.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="w")
            self.token_label2.grid(row=2, column=1, columnspan=2, pady=(20, 50), sticky="w")


    def signIn(self):
        pass

    def exitTheGame(self):
        pass





class TicTacToeGamePage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.master = parent
        self.grid(row=0, column=0, sticky="nsew")
        self.timer_label = None  # Initialize timer_label attribute
        self.create_widgets()
        self.start_timer()


    def create_widgets(self):
        # Create the grid for the Tic Tac Toe game
        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self, text="", width=5, height=2, font=("Helvetica", 20), command=lambda row=i, col=j: self.button_click(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        # Create text view for messages
        self.message_label = tk.Label(self, text="Messages will appear here", font=("Helvetica", 12))
        self.message_label.grid(row=3, column=0, columnspan=3, pady=10)

        # Create timer label
        self.timer_label = tk.Label(self, text="Timer", font=("Helvetica", 12))
        self.timer_label.grid(row=0, column=3, rowspan=3, padx=10)

    def button_click(self, row, col):
        # Function to handle button clicks
        self.buttons[row][col].config(text="X", state=tk.DISABLED)  # Place X on the clicked button

        # You can implement more logic here for the game

    def start_timer(self):
        # Function to start the timer
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        # Function to update the timer label
        elapsed_time = time.time() - self.start_time
        self.timer_label.config(text=f"Timer: {int(elapsed_time)} sec")
        self.timer_label.after(1000, self.update_timer)


