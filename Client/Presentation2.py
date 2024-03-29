import tkinter as tk
import sys
import time
from tkinter import ttk
from tkinter import messagebox
import inspect
import threading
import DataServiceClient.libClient as messageChannel
import DataServiceClient.socketComm as comm

MEDIUMFONT = ("Verdana", 18)
LARGEFONT = ("Verdana", 30)


class PresentationController:
 
    # __init__ function for class TicTacToePresentation 
    def __init__(self, parent, message_channel : messageChannel.Message): 
         
        self.messageChannel = message_channel
        self.root = parent
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

        self.currentPage = AuthPageToken
        self.show_frame(self.currentPage)
        self.message_buffer = []

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        print(self.frames[cont])
        frame = self.frames[cont]
        # self.currentPage = frame
        self.currentPage = cont
        frame.tkraise()

    # def messageChannel(self, comm : message.Message):
    #     messageChannel = comm




# # first window frame startpage
# class StartPage(tk.Frame):
#     def __init__(self, parent, controller): 
#         tk.Frame.__init__(self, parent)
         
#         # label of frame Layout 2
#         label = ttk.Label(self, text ="Startpage", font = LARGEFONT)
         
#         # putting the grid in its place by using grid
#         label.grid(row = 0, column = 4, padx = 10, pady = 10) 
  
#         button1 = ttk.Button(self, text ="Page 1", command = lambda : controller.show_frame(Page1))
     
#         # putting the button in its place by
#         # using grid
#         button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
#         ## button to show frame 2 with text layout2
#         button2 = ttk.Button(self, text ="Page 2", command = lambda : controller.show_frame(Page2))
     
#         # putting the button in its place by
#         # using grid
#         button2.grid(row = 2, column = 1, padx = 10, pady = 10)
  
          
  
  
# # second window frame page1 
# class Page1(tk.Frame):
     
#     def __init__(self, parent, controller):
         
#         tk.Frame.__init__(self, parent)
#         label = ttk.Label(self, text ="Page 1", font = LARGEFONT)
#         label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
#         # button to show frame 2 with text
#         # layout2
#         button1 = ttk.Button(self, text ="StartPage",
#                             command = lambda : controller.show_frame(StartPage))
     
#         # putting the button in its place 
#         # by using grid
#         button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
#         # button to show frame 2 with text
#         # layout2
#         button2 = ttk.Button(self, text ="Page 2",
#                             command = lambda : controller.show_frame(Page2))
     
#         # putting the button in its place by 
#         # using grid
#         button2.grid(row = 2, column = 1, padx = 10, pady = 10)
  
  
  
  
# # third window frame page2
# class Page2(tk.Frame): 
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = ttk.Label(self, text ="Page 2", font = LARGEFONT)
#         label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
#         # button to show frame 2 with text layout2
#         button1 = ttk.Button(self, text ="Page 1", command = lambda : controller.show_frame(Page1))
     
#         # putting the button in its place by using grid
#         button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
#         # button to show frame 3 with text layout3
#         button2 = ttk.Button(self, text ="Startpage",
#                             command = lambda : controller.show_frame(StartPage))

#         # putting the button in its place by using grid
#         button2.grid(row = 2, column = 1, padx = 10, pady = 10)



# """ Page for authentication with username and password
# """
# class AuthPagePassword(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)

#         # Create headline
#         headline_label = ttk.Label(self, text="Tic Tac Toe", font=LARGEFONT, background='#F0F0F0', foreground='#333333')
#         #headline_label.grid(row=0, column=0, columnspan=2, pady=(50, 20), sticky="n")
#         headline_label.place(relx=0.5, rely=0.1, anchor="center")

#         # Group auth objects 
#         detailsFrame = tk.Frame(self, bg="#F0F0F0", highlightbackground="#F0F0F0", highlightthickness=0)
#         #authFrame.grid(row=1, column=0, columnspan=2, pady=(50, 20), sticky="n")
#         detailsFrame.place(relx=0.5, rely=0.5, anchor="center")

#         # Create username label and entry
#         username_label = ttk.Label(detailsFrame, text="Username ", font=MEDIUMFONT, background='#F0F0F0', foreground='#333333')
#         username_label.grid(row=0, column=0, pady=(0, 20), sticky="e")
#         self.username_entry = tk.Entry(detailsFrame, font=("Verdana", 18))
#         self.username_entry.grid(row=0, column=1, pady=(0, 20), sticky="w")

#         # Create password label and entry
#         password_label = ttk.Label(detailsFrame, text="Password ", font=MEDIUMFONT, background='#F0F0F0', foreground='#333333')
#         password_label.grid(row=1, column=0, pady=(0, 20), sticky="e")
#         self.password_entry = tk.Entry(detailsFrame, show="*", font=("Verdana", 18))
#         self.password_entry.grid(row=1, column=1, pady=(0, 20), sticky="w")

#         # Create login button
#         login_button = tk.Button(detailsFrame, text="Sign in", command=self.authenticate, font=("Verdana", 18), bg='#4CAF50', fg='white')
#         login_button.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="n")
#         #login_button.place(relx=0.5, rely=0.9, anchor="center")


#         # Create Exit button
#         exit_button = tk.Button(self, text=" Exit ", command=self.exitTheGame, font=("Verdana", 18), bg='#4CAF50', fg='white')
#         #login_button.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="n")
#         exit_button.place(relx=0.5, rely=0.9, anchor="center")

    
#     def authenticate(self):
#         username = self.username_entry.get()
#         password = self.password_entry.get()

#         # Replace this with your authentication logic
#         if username == "admin" and password == "password":
#             messagebox.showinfo("Login Successful", "Welcome, {}".format(username))
#             # Add code to navigate to the next page or perform further actions after authentication
#         else:
#             messagebox.showerror("Login Failed", "Invalid username or password")

#     def exitTheGame(self):
#         pass


class AuthPageToken(tk.Frame):
    """page for authentication with personal token. Inherited from tk.Frame
    """
    def __init__(self, parent, controller):
        """constructor for TokenPage

        Args:
            parent (Frame): inherits from tk.Frame
            controller (presentationController): the backbone of the GUI
        """
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        # Create headline
        headline_label = ttk.Label(self, text="Tic Tac Toe", font=LARGEFONT, background='#F0F0F0', foreground='#333333')
        headline_label.place(relx=0.5, rely=0.1, anchor="center")

        # Group auth objects
        detailsFrame = tk.Frame(self, bg="#F0F0F0", highlightbackground="#F0F0F0", highlightthickness=0)
        detailsFrame.place(relx=0.5, rely=0.5, anchor="center")

        # Create token label and token entry
        token_label = ttk.Label(detailsFrame, text="Enter Your Token: ", font=MEDIUMFONT, background='#F0F0F0', foreground='#333333')
        token_label.grid(row=0, column=0, pady=(0, 20), sticky="e")
        self.token_entry = tk.Entry(detailsFrame, font=("Verdana", 18))
        self.token_entry.grid(row=0, column=1, pady=(0, 20), sticky="w")
        
        # Create login button
        self.login_button = tk.Button(detailsFrame, text="Log in", command=self.authenticate, font=("Verdana", 18), bg='#4CAF50', fg='white')
        self.login_button.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="n")
        
        # Message label
        self.message_label = ttk.Label(detailsFrame, text="", font=MEDIUMFONT, background='#F0F0F0', foreground='#333333')
        self.message_label.grid(row=3, column=0, pady=(0, 20), sticky="e")
        

        # Create Exit button
        exit_button = tk.Button(self, text=" Exit ", command=self.exitTheGame, font=("Verdana", 18), bg='#4CAF50', fg='white')
        exit_button.place(relx=0.6, rely=0.9)

        
        # Create Sign Up button
        signup_button = tk.Button(self, text="Sign Up", command=lambda: controller.show_frame(SignUpPage), font=("Verdana", 18), bg='#4CAF50', fg='white')
        signup_button.place(relx=0.3, rely=0.9)



    def getTokenEntry(self):
        """get the text in the 'insert token' entry

        Returns:
            str: token, unique ID of the user
        """
        return self.token_entry.get()
    

    # def setTokenEntry(self, tokenGenerated):
    #     """set the content of the 'insert token' entry

    #     Args:
    #         tokenGenerated (str): the string of the generated token
    #     """
    #     self.token_entry.insert(0,tokenGenerated)


    def authenticate(self):
        """manage the authentication process using unique token
        """
        self.message_label.config(text = "")
        self.login_button["state"] = "disabled"
        
        token = self.token_entry.get()
        self.controller.messageChannel.setRequest("veteranUser", token)
        
        
        t = threading.Thread(target=self.authenticate_helper)
        t.start()
        schedule_check(self, t, self.check_if_auth_done.__name__)

        
    
    def authenticate_helper(self):
        """check if a response from the server about the auth request has arrived
        """
        while (self.controller.messageChannel.response == None):
            pass

        # # Replace this with your authentication logic
        # if token == "admin":
        #     messagebox.showinfo("Login Successful", "Welcome, {}".format(token))
        #     # Add code to navigate to the next page or perform further actions after authentication
        # else:
        #     messagebox.showerror("Login Failed", "Invalid username or password")

    def check_if_auth_done(self, t):
        """if the thread 't' is dead then it means a response from the server about the auth request has arrived,
            the function handle that response
        Args:
            t (Thread): the thread that is in charge of the auth response
        """
        # If the thread has finished, re-enable the button and show a message.
        if not t.is_alive():
            self.login_button["state"] = "normal"
            match self.controller.messageChannel.response["response"]:
                case "verified":
                    if self.controller.currentPage is AuthPageToken:
                        self.controller.show_frame(MainPage)
                        self.controller.message_buffer.append("registered successfully, " + self.controller.messageChannel.response["value"] + "!")
                case "tokenNotFound":
                    self.message_label.config(text = "this token was not found")
        else:
            # Otherwise check again after one second.
            schedule_check(self, t, self.check_if_auth_done.__name__)



    def exitTheGame(self):
        """upon clicking the 'exit' button, handle exiting the game gracefully by sending a message
            to the server
        """
        self.controller.messageChannel.setRequest("exit", "a")


class SignUpPage(tk.Frame):
    """page for registering new user to the system
    """
    def __init__(self, parent, controller):
        """constructor for SignUpPage

        Args:
            parent (Frame): a frame that inherits from the app root
            controller (PresentationController): the GUI controller
        """
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

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

        # 'Create User' button
        self.createUser_button = tk.Button(detailsFrame, text="Create New User", command=self.createUser, font=("Verdana", 18), bg='#4CAF50', fg='white')
        self.createUser_button.grid(row=1, column=0, columnspan=2, pady=(20, 50), sticky="n")

        # 'New Token' label
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
        signIn_button = tk.Button(self, text="Sign In", command=lambda: controller.show_frame(AuthPageToken), font=("Verdana", 18), bg='#4CAF50', fg='white')
        signIn_button.place(relx=0.3, rely=0.9)



    def createUser(self):
        """create new user by generating unique token and binding the chosen nik name to it
        """
        if self.nikName_entry.get() == "":
                messagebox.showinfo("nik name missing", "You have to insert a NikName!")

        else:
            if self.createUser_button.cget('text') ==  "Create New User":
                
                self.createUser_button["state"] = "disabled"
                nikName = self.nikName_entry.get()
                self.controller.messageChannel.setRequest("newUser", nikName)
                
                t = threading.Thread(target=self.signUp_helper)
                t.start()
                schedule_check(self, t, self.check_if_signUp_done.__name__)
        
            else: # continue to the Main page
                self.controller.show_frame(MainPage)

        # if 
        # print(self.token_label1.winfo_ismapped())
        # self.token_label1.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="w")
        # self.token_label2.grid(row=2, column=1, columnspan=2, pady=(20, 50), sticky="w")
        # token = 123

        # messagebox.showinfo("Login Successful", "Welcome, {}".format(token))
        
        
    def signUp_helper(self):
        """check if a response from the server about the auth request has arrived
        """
        while (self.controller.messageChannel.response == None):
            pass


    def check_if_signUp_done(self, t):
        """if the thread 't' is dead then it means a response from the server about the auth request has arrived,
            the function handle that response
        Args:
            t (Thread): the thread that is in charge of the signUp response
        """
        # If the thread has finished, re-enable the button and show a message.
        if not t.is_alive():
            self.createUser_button.config(text="continue")
            self.createUser_button["state"] = "normal"

            match self.controller.messageChannel.response["response"]:
                case "verified":
                    if self.controller.currentPage is SignUpPage:
                        self.token_label1.config(text="Your unique token is " + str(self.controller.messageChannel.response["value"]))
                        self.token_label1.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="w")
                case "errorHasOccured":
                        self.token_label1.config(text="error has occured, try again")
                        self.token_label1.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="w")        
        else:
            # Otherwise check again after one second.
            schedule_check(self, t, self.check_if_auth_done.__name__)


    def getNikNameEntry(self):
        """get the text in the 'insert token' entry

        Returns:
            str: token, unique ID of the user
        """
        return self.nikName_entry.get()
    


    def exitTheGame(self):
        """upon clicking the 'exit' button, handle exiting the game gracefully by sending a message
            to the server
        """
        self.controller.messageChannel.setRequest("exit", "a")


class MainPage(tk.Frame):
    def __init__(self, master, controller):
        #super().__init__(master)
        tk.Frame.__init__(self, master)
        
        self.master = master
        self.controller = controller
        self.configure(bg="#f0f0f0")
        self.grid(row=0, column=0, sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        # Headline label
        headline_label = tk.Label(self, text="Game Center", font=("Arial", 24, "bold"), bg="#f0f0f0")
        headline_label.pack(pady=10)

        # Buttons frame
        buttons_frame = tk.Frame(self, bg="#f0f0f0")
        buttons_frame.pack()

        # New Game button
        new_game_button = tk.Button(buttons_frame, text="New Game", width=15, font=("Arial", 12), bg="#4CAF50", fg="white", relief=tk.FLAT, command=self.new_game)
        new_game_button.grid(row=0, column=0, padx=10)

        # Join a Game button
        self.join_game_button = tk.Button(buttons_frame, text="Join a Game", width=15, font=("Arial", 12), bg="#FFC107", relief=tk.FLAT, command=self.join_game)
        self.join_game_button.grid(row=0, column=1, padx=10)

        # View Leadership Games button
        view_games_button = tk.Button(buttons_frame, text="View Leadership Games", width=20, font=("Arial", 12), bg="#2196F3", fg="white", relief=tk.FLAT, command=self.view_leadership_games)
        view_games_button.grid(row=0, column=2, padx=10)

        # Games list frame (initially hidden)
        self.games_list_frame = tk.Frame(self, bg="#f0f0f0")
        self.games_list_frame.pack()

        # Listbox for games
        self.games_listbox = tk.Listbox(self.games_list_frame, width=50, height=10, font=("Arial", 12), bg="white", selectbackground="#FFC107")
        self.games_listbox.pack(side="left", fill="y", padx=5, pady=5)

        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(self.games_list_frame, orient="vertical", command=self.games_listbox.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure listbox to use scrollbar
        self.games_listbox.config(yscrollcommand=scrollbar.set)

        # Example games
        self.games_listbox.insert("end", "Game 1 (Owner: Alice, Participants: 3)")
        self.games_listbox.insert("end", "Game 2 (Owner: Bob, Participants: 2)")
        self.games_listbox.insert("end", "Game 3 (Owner: Charlie, Participants: 4)")

        # Bind click event to games listbox
        self.games_listbox.bind("<Double-Button-1>", self.on_game_select)

        # Logout and Exit buttons frame
        logout_exit_frame = tk.Frame(self, bg="#f0f0f0")
        logout_exit_frame.pack(side="bottom", fill="x")

        # Logout button
        logout_button = tk.Button(logout_exit_frame, text="Logout", width=10, font=("Arial", 12), bg="#FFC107", fg="white", relief=tk.FLAT, command=self.logout)
        logout_button.pack(side="left", padx=10, pady=10)

        # Exit button
        exit_button = tk.Button(logout_exit_frame, text="Exit", width=10, font=("Arial", 12), bg="#F44336", fg="white", relief=tk.FLAT, command=self.exit_app)
        exit_button.pack(side="right", padx=10, pady=10)

        # Hide the games list frame initially
        self.games_list_frame.pack_forget()

    def new_game(self):
        # Function to handle New Game button click
        print("New Game button clicked")

    def join_game(self):
        # Function to handle Join a Game button click
        self.games_list_frame.pack()
        self.join_game_button.pack_forget()
        print("Join a Game button clicked")

    def view_leadership_games(self):
        # Function to handle View Leadership Games button click
        print("View Leadership Games button clicked")

    def on_game_select(self, event):
        # Function to handle clicking on a game entry
        selected_index = self.games_listbox.curselection()
        if selected_index:
            selected_game = self.games_listbox.get(selected_index)
            print(f"Selected game: {selected_game}")

    def logout(self):
        # Function to handle Logout button click
        print("Logout button clicked")

    def exit_app(self):
        # Function to handle Exit button click
        print("Exit button clicked")
        self.master.destroy()


# below is old version of the page 'main page'
        
# class MainPage(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)

#         # Create headline
#         headline_label = ttk.Label(self, text="Tic Tac Toe - Main menu", font=LARGEFONT, background='#F0F0F0', foreground='#333333')
#         headline_label.place(relx=0.5, rely=0.1, anchor="center")

#         # Group auth objects 
#         optionsFrame = tk.Frame(self, bg="#F0F0F0", highlightbackground="#F0F0F0", highlightthickness=0)
#         optionsFrame.place(relx=0.5, rely=0.5, anchor="center")
        
#         # New Game button
#         create_button = tk.Button(optionsFrame, text="New Game", command=self.createUser, font=("Verdana", 18), bg='#4CAF50', fg='white')
#         create_button.grid(row=0, column=0, columnspan=2, pady=(20, 50))

#         # Join Game button
#         create_button = tk.Button(optionsFrame, text="Join A Game", command=self.createUser, font=("Verdana", 18), bg='#4CAF50', fg='white')
#         create_button.grid(row=1, column=0, columnspan=2, pady=(20, 50))

#         # View Leadership Table button
#         create_button = tk.Button(optionsFrame, text="View Leadership Table", command=self.createUser, font=("Verdana", 18), bg='#4CAF50', fg='white')
#         create_button.grid(row=2, column=0, columnspan=2, pady=(20, 50))




#         # Create Exit button
#         exit_button = tk.Button(self, text=" Exit ", command=self.exitTheGame, font=("Verdana", 18), bg='#4CAF50', fg='white')
#         exit_button.place(relx=0.6, rely=0.9)

        
#         # Create Log out button
#         logout_button = tk.Button(self, text="Logout", command=self.signIn, font=("Verdana", 18), bg='#4CAF50', fg='white')
#         logout_button.place(relx=0.3, rely=0.9)



#     def createUser(self):
#         token = 123

#         # Replace this with your authentication logic
#         if token == "admin":
#             messagebox.showinfo("Login Successful", "Welcome, {}".format(token))
#             # Add code to navigate to the next page or perform further actions after authentication
#         else:
#             #messagebox.showerror("Login Failed", "Invalid username or password")
#             self.token_label1.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="w")
#             self.token_label2.grid(row=2, column=1, columnspan=2, pady=(20, 50), sticky="w")


#     def signIn(self):
#         pass

#     def exitTheGame(self):
#         pass


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




def schedule_check(tk : tk.Tk, t : threading.Thread, func_name):
    """
    Schedule the execution of the `check_if_done()` function after
    one second.
    """
    func = getattr(tk,func_name)
    tk.after(500, func, t)