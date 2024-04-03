import tkinter as tk
import time
from tkinter import ttk
from tkinter import messagebox
import threading
import DataServiceClient.libClient as messageChannel

MEDIUMFONT = ("Verdana", 15)
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
  
        
        self.currentPage = AuthPageToken
        self.currentPageInstance = None
        self.show_page(self.currentPage)

        

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

        # self.currentPage = AuthPageToken
        # self.show_page(self.currentPage)
        # self.message_buffer = []

        

    # # to display the current frame passed as
    # # parameter
    # def show_page(self, cont, *rest, isNew: bool = False):
    #     if isNew:
    #         if (cont in self.frames):
    #             self.frames.pop(cont)
    #         newInstance = cont(self.container, self, *rest)
    #         self.frames[cont] = newInstance
        
    #     print(self.frames[cont])
    #     frame = self.frames[cont]
    #     self.currentPage = cont
    #     frame.tkraise()




          
  
  

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
        super().__init__(parent)
        print("2: ")
        self.parent = parent
        self.controller = controller


        # Create headline
        headline_label = ttk.Label(self, text="Tic Tac Toe", font=LARGEFONT, background='#F0F0F0', foreground='#333333')
        headline_label.place(relx=0.5, rely=0.1, anchor="center")
        # headline_label.pack(padx=10, pady=10, anchor="center")

        # Group auth objects
        detailsFrame = tk.Frame(self, bg="#F0F0F0", highlightbackground="#F0F0F0", highlightthickness=0)
        detailsFrame.place(relx=0.5, rely=0.5, anchor="center")

        # Create token label and token entry
        token_label = ttk.Label(detailsFrame, text="Enter Your Token: ", font=MEDIUMFONT, background='#F0F0F0', foreground='#333333')
        token_label.grid(row=0, column=0, pady=(0, 20), sticky="e")
        self.token_entry = tk.Entry(detailsFrame, font=("Verdana", 18))
        self.token_entry.grid(row=0, column=1, pady=(0, 20), sticky="w")
        self.token_entry.focus_set()
        
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
        signup_button = tk.Button(self, text="Sign Up", command=lambda: controller.show_page(SignUpPage), font=("Verdana", 18), bg='#4CAF50', fg='white')
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
        """check if a response from the server about the 'auth' request has arrived.
            At first we check if the response is None i.e. no response has arrived, and then we verify
            that the response is what we expected to, i.e. "response" == "0_verified", else we continue looping.
        """
        while (self.controller.messageChannel.response == None  or
               self.controller.messageChannel.response["response"][0] != "0"):
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
                case "0_verified":
                    if self.controller.currentPage is AuthPageToken:
                        self.controller.show_page(MainPage)
                        #self.controller.message_buffer.append("registered successfully, " + self.controller.messageChannel.response["value"] + "!")
                case "0_tokenNotFound":
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
        self.nikName_entry.focus_set()

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
        signIn_button = tk.Button(self, text="Sign In", command=lambda: controller.show_page(AuthPageToken), font=("Verdana", 18), bg='#4CAF50', fg='white')
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
                self.controller.show_page(MainPage)

        # if 
        # print(self.token_label1.winfo_ismapped())
        # self.token_label1.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="w")
        # self.token_label2.grid(row=2, column=1, columnspan=2, pady=(20, 50), sticky="w")
        # token = 123

        # messagebox.showinfo("Login Successful", "Welcome, {}".format(token))
        
        
    def signUp_helper(self):
        """check if a response from the server about the signUp request has arrived.
            At first we check if the response is None i.e. no response has arrived, and then we verify
            that the response is what we expected to, i.e. "response" == "1_newUser", else we continue looping.
        """
        while (self.controller.messageChannel.response == None  or  
               self.controller.messageChannel.response["response"][0] != "1"):
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
                case "1_newUser":
                    if self.controller.currentPage is SignUpPage:
                        self.token_label1.config(text="Your unique token is " + str(self.controller.messageChannel.response["value"]))
                        self.token_label1.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="w")
                case "1_errorHasOccured":
                        self.token_label1.config(text="error has occured, try again")
                        self.token_label1.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="w")        
        else:
            # Otherwise check again after one second.
            schedule_check(self, t, self.check_if_signUp_done.__name__)


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
        headline_label = tk.Label(self, text="Game Center", font=("Verdana", 24, "bold"), bg="#f0f0f0")
        headline_label.pack(pady=10)

        # Buttons frame
        self.buttons_frame = tk.Frame(self, bg="#f0f0f0")
        self.buttons_frame.pack()

        # New Game button
        self.new_game_button = tk.Button(self.buttons_frame, text="New Game", width=15, font=("Verdana", 12), bg="#4CAF50", fg="white", relief=tk.FLAT, command=self.new_game)
        self.new_game_button.grid(row=0, column=0, padx=10)

        # Join a Game button
        self.join_game_button = tk.Button(self.buttons_frame, text="Join a Game", width=15, font=("Arial", 12), bg="#FFC107", fg="white", relief=tk.FLAT, command=self.join_game)
        self.join_game_button.grid(row=0, column=1, padx=10)

        # View Leadership Games button
        view_games_button = tk.Button(self.buttons_frame, text="View Leadership Games", width=20, font=("Arial", 12), bg="#2196F3", fg="white", relief=tk.FLAT, command=self.view_leadership_games)
        view_games_button.grid(row=0, column=2, padx=10)

        # Games list frame (initially hidden)
        self.games_list_frame = tk.Frame(self, bg="#f0f0f0")
        self.games_list_frame.pack()

        # Listbox for games
        self.games_listbox = tk.Listbox(self.games_list_frame, width=50, height=10, font=("Arial", 12), bg="white", selectbackground="#FFC107")
        self.games_listbox.pack(side="left", fill="y", padx=5, pady=5)
        
        # Bind callback function to listbox selection event
        self.games_listbox.bind("<Double-Button-1>", self.on_game_select)
        
        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(self.games_list_frame, orient="vertical", command=self.games_listbox.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure listbox to use scrollbar
        self.games_listbox.config(yscrollcommand=scrollbar.set)


        self.activeGames_initialized = []
        self.activeGames_occuring = []

        # Text entry for number of players (initially hidden)
        self.players_entry_frame = tk.Frame(self, bg="#f0f0f0")
        self.players_entry_label = tk.Label(self.players_entry_frame, text="Number of Players:", font=("Verdana", 12), bg="#f0f0f0")
        self.players_entry_label.pack(side="left", padx=5, pady=5)
        self.players_entry = tk.Entry(self.players_entry_frame, font=("Arial", 12), width=10)
        self.players_entry.pack(side="left", padx=5, pady=5)
        self.players_entry_frame.pack()

        # Radio buttons for player type (initially hidden)
        self.player_type_frame = tk.Frame(self, bg="#f0f0f0")
        self.player_type_label = tk.Label(self.player_type_frame, text="Player Type:", font=("Arial", 12), bg="#f0f0f0")
        self.player_type_label.pack(side="left", padx=5, pady=5)

        self.player_type_var = tk.StringVar(value="active_player")
        self.player_last_type = "active_player" # used to verify that the user changed the radio button selection
                                                # and not just clicked on the same button

        style = ttk.Style()
        style.configure("TRadiobutton", background="#f0f0f0", font=("Arial", 12))

        self.active_player_radio = ttk.Radiobutton(self.player_type_frame, text="Active Player", variable=self.player_type_var, value="active_player", command=self.handle_radio_click)
        self.active_player_radio.pack(side="left", padx=5, pady=5)

        self.spectator_radio = ttk.Radiobutton(self.player_type_frame, text="Spectator", variable=self.player_type_var, value="spectator", command=self.handle_radio_click)
        self.spectator_radio.pack(side="left", padx=5, pady=5)

        self.player_type_frame.pack()

        # Logout and Exit buttons frame
        logout_exit_frame = tk.Frame(self, bg="#f0f0f0")
        logout_exit_frame.pack(side="bottom", fill="x")

        # Logout button
        logout_button = tk.Button(logout_exit_frame, text="Logout", width=10, font=("Arial", 12), bg="#FFC107", fg="white", relief=tk.FLAT, command=self.logout)
        logout_button.pack(side="left", padx=10, pady=10)

        # Exit button
        exit_button = tk.Button(logout_exit_frame, text="Exit", width=10, font=("Arial", 12), bg="#F44336", fg="white", relief=tk.FLAT, command=self.exit_app)
        exit_button.pack(side="right", padx=10, pady=10)

        # Hide the games list frame, players entry, and player type radio buttons initially
        self.games_list_frame.pack_forget()
        self.players_entry_frame.pack_forget()
        self.player_type_frame.pack_forget()
    
    def new_game(self):
        self.games_list_frame.pack_forget()  # hide the listbox
        self.player_type_frame.pack_forget() # hide the player type frame
        if (self.new_game_button.cget('text') == "New Game"):
            self.players_entry_frame.pack()
            self.new_game_button.config(text="start!")
        else:
            players_entry = self.players_entry.get()
            if (players_entry == ""  or  int(players_entry) < 2  or  int(players_entry) > 8):
                messagebox.showinfo("message", "please insert a valid number of players (2-8 allowed)")
            else:
                self.controller.messageChannel.setRequest("newGame", int(players_entry))

                t = threading.Thread(target=self.newGame_helper)
                t.start()
                schedule_check(self, t, self.check_if_newGame_done.__name__)

        # Function to handle New Game button click
        print("New Game button clicked")

    def newGame_helper(self):
        """check if a response from the server about the auth request has arrived.
            At first we check if the response is None i.e. no response has arrived, and then we verify
            that the response is what we expected to, i.e. "response" == "2_newRegisteredGame", else we continue looping.
        """
        while (self.controller.messageChannel.response == None  or  
               self.controller.messageChannel.response["response"][0] != "2"):
            pass

        # # Replace this with your authentication logic
        # if token == "admin":
        #     messagebox.showinfo("Login Successful", "Welcome, {}".format(token))
        #     # Add code to navigate to the next page or perform further actions after authentication
        # else:
        #     messagebox.showerror("Login Failed", "Invalid username or password")

    def check_if_newGame_done(self, t):
        """if the thread 't' is dead then it means a response from the server about the auth request has arrived,
            the function handle that response
        Args:
            t (Thread): the thread that is in charge of the newGame response
        """
        if not t.is_alive():
            match self.controller.messageChannel.response["response"]:
                case "2_newRegisteredGame":
                    game = self.controller.messageChannel.response["value"] # should be [ game_ID, numOfPlayers ]
                    print("check_new_game")
                    if self.controller.currentPage is MainPage:
                        self.controller.show_page(GamePage, game[1], game[0])
                        self.controller.currentPageInstance.message_buffer.append(f"waiting for {game[1]-1} more players to join and then we start!")
                case "2_errorHasOccured":
                    messagebox.showinfo("message", "an error has occured during a try to initiate a new game")
        else:
            # Otherwise check again after one second.
            schedule_check(self, t, self.check_if_newGame_done.__name__)

    def join_game(self):
        
        print("Join a Game button clicked")
        self.new_game_button.config(text="New Game")
        # Function to handle Join a Game button click
        self.players_entry_frame.pack_forget()
        self.games_list_frame.pack()
        
        self.join_game_button["state"] = "disabled"
        
        self.controller.messageChannel.setRequest("fetchGames", "a")


        t = threading.Thread(target=self.fetchActiveGames_helper)
        t.start()
        schedule_check(self, t, self.check_if_fetchActiveGames_done.__name__)


    def fetchActiveGames_helper(self):
        """check if a response from the server about 'fetching the games' request has arrived.
            At first we check if the response is None i.e. no response has arrived, and then we verify
            that the response is what we expected to, i.e. "response" == "3_allActiveGames", else we continue looping.
        """
        while (self.controller.messageChannel.response == None  or  
               self.controller.messageChannel.response["response"][0] != "3"):
            pass


    def check_if_fetchActiveGames_done(self, t):
        """if the thread 't' is dead then it means a response from the server about the auth request has arrived,
            the function handle that response
        Args:
            t (Thread): the thread that is in charge of the signUp response
        """
        if not t.is_alive():
            self.games_listbox.delete(0,"end")
            self.activeGames_initialized = []
            self.activeGames_occuring = []

            games = self.controller.messageChannel.response["value"]
            for key, game in games.items():
                # we get the following format: key = gameID, game = ({Game as dict}, number of active participants, number of passive participants - spectators)
                if (game[0]["game_state"] == "INITIALIZED"):
                    self.activeGames_initialized.append(game)
                elif (game[0]["game_state"] == "STARTED"):
                    self.activeGames_occuring.append(game)

            # building the list of games for displaying it to the user
            for index, game in enumerate(self.activeGames_initialized):
                strForDisplay = f"Game {index+1} (opened for " + str(game[0]["num_of_players"]) + " players, waiting for " + str(game[0]["num_of_players"]-game[1]) + " more, " + str(game[2]) + " spectators" + ")"
                self.games_listbox.insert("end", strForDisplay)
            
            self.player_type_frame.pack()
            self.join_game_button["state"] = "normal"

      
        else:
            # Otherwise check again after one second.
            schedule_check(self, t, self.check_if_fetchActiveGames_done.__name__)


    def handle_radio_click(self):
        # Function to handle clicking on a radio button
        player_type = self.player_type_var.get()
        print(f"Selected player type: {player_type}")
        if (player_type != self.player_last_type):
            if player_type == "active_player" and self.activeGames_occuring != []:
                self.games_listbox.delete(len(self.activeGames_initialized),len(self.activeGames_initialized)+len(self.activeGames_occuring)-1)
            elif player_type == "spectator":
                self.games_listbox.insert("end", *self.activeGames_occuring)

        self.player_last_type = player_type

    


    def on_game_select(self, event):
        # Function to handle clicking on a game entry

        selected_index = self.games_listbox.curselection()[0]
        print("selected index: ", selected_index)        

        # the user is a spectator in an occurring game
        if (selected_index >= len(self.activeGames_initialized)): 
            selectedGame = self.activeGames_occuring[selected_index-len(self.activeGames_initialized)][0]
            numOfActivePlayers = self.activeGames_occuring[selected_index-len(self.activeGames_initialized)][1]
            self.controller.show_page(GamePage, selectedGame["num_of_players"], selectedGame["game_ID"], board = selectedGame["board"])

        # the user is either an active player or a spectator in a game that has not yet started
        else:
            selectedGame = self.activeGames_initialized[selected_index][0]
            numOfActivePlayers = self.activeGames_initialized[selected_index][1]
            # print("selectedGame", selectedGame)
            self.controller.show_page(GamePage, selectedGame["num_of_players"], selectedGame["game_ID"])
        
        
        # send a message about how many more players nedd to join before we start, but only if
        # the user is a spectator and he chose to spectate a game that has not yet started. else,
        # a message will be sent by the server.
        if self.player_type_var.get() == "spectator"  and selected_index < len(self.activeGames_initialized):
            strForDisplay = "waiting for " + str(selectedGame["num_of_players"]-numOfActivePlayers) + " more players to join and then we start!"
            self.controller.currentPageInstance.message_buffer.append(strForDisplay)
        

        # send a message to the server that a new player has now joined the game
        if self.player_type_var.get() == "active_player":
            self.controller.messageChannel.setRequest("newJoined", ("player", selectedGame["game_ID"]))
        
        # self.player_type_var.get() == "spectator"
        else: 
            self.controller.messageChannel.setRequest("newJoined", ("spectator", selectedGame["game_ID"]))


    def view_leadership_games(self):
        # Function to handle View Leadership Games button click
        print("View Leadership Games button clicked")

    def logout(self):
        self.controller.messageChannel.setRequest("logout", "a")
        self.controller.show_page(AuthPageToken)

    def exit_app(self):
        """upon clicking the 'exit' button, handle exiting the game gracefully by sending a message
            to the server
        """
        self.controller.messageChannel.setRequest("exit", "a")



################################################################
################################################################
################################################################
        
    # def create_widgets(self):
    #     # # Headline label
    #     # # headline_label = tk.Label(self, text="Main Menu", font=("Arial", 24, "bold"), bg="#f0f0f0")
    #     # headline_label = tk.Label(self, text="Main Menu", font=LARGEFONT, bg="#f0f0f0")
    #     # headline_label.pack(pady=10)

    #     # # Buttons frame
    #     # buttons_frame = tk.Frame(self, bg="#f0f0f0")
    #     # buttons_frame.pack()

    #     # # New Game button
    #     # new_game_button = tk.Button(buttons_frame, text="New Game", width=15, font=MEDIUMFONT, bg="#4CAF50", fg="white", relief=tk.FLAT, command=self.new_game)
    #     # new_game_button.grid(row=0, column=0, padx=10)

    #     # # Join a Game button
    #     # self.join_game_button = tk.Button(buttons_frame, text="Join a Game", width=15, font=MEDIUMFONT, bg="#FFC107", fg="white", relief=tk.FLAT, command=self.join_game)
    #     # self.join_game_button.grid(row=0, column=1, padx=10)

    #     # # View Leadership Games button
    #     # view_games_button = tk.Button(buttons_frame, text="View Leadership Games", width=20, font=MEDIUMFONT, bg="#2196F3", fg="white", relief=tk.FLAT, command=self.view_leadership_games)
    #     # view_games_button.grid(row=0, column=2, padx=10)

    #     # # Games list frame (initially hidden)
    #     # self.games_list_frame = tk.Frame(self, bg="#f0f0f0")
    #     # self.games_list_frame.pack()

    #     # # Listbox for games
    #     # self.games_listbox = tk.Listbox(self.games_list_frame, width=50, height=10, font=("Arial", 12), bg="white", selectbackground="#FFC107")
    #     # self.games_listbox.pack(side="left", fill="y", padx=5, pady=5)

    #     # # Scrollbar for listbox
    #     # scrollbar = tk.Scrollbar(self.games_list_frame, orient="vertical", command=self.games_listbox.yview)
    #     # scrollbar.pack(side="right", fill="y")

    #     # # Configure listbox to use scrollbar
    #     # self.games_listbox.config(yscrollcommand=scrollbar.set)

    #     # # Example games
    #     # self.games_listbox.insert("end", "Game 1 (Owner: Alice, Participants: 3)")
    #     # self.games_listbox.insert("end", "Game 2 (Owner: Bob, Participants: 2)")
    #     # self.games_listbox.insert("end", "Game 3 (Owner: Charlie, Participants: 4)")

    #     # # Bind click event to games listbox
    #     # self.games_listbox.bind("<Double-Button-1>", self.on_game_select)

    #     # # Logout and Exit buttons frame
    #     # logout_exit_frame = tk.Frame(self, bg="#f0f0f0")
    #     # logout_exit_frame.pack(side="bottom", fill="x")

    #     # # Logout button
    #     # logout_button = tk.Button(logout_exit_frame, text="Logout", width=10, font=("Arial", 12), bg="#FFC107", fg="white", relief=tk.FLAT, command=self.logout)
    #     # logout_button.pack(side="left", padx=10, pady=10)

    #     # # Exit button
    #     # exit_button = tk.Button(logout_exit_frame, text="Exit", width=10, font=("Arial", 12), bg="#F44336", fg="white", relief=tk.FLAT, command=self.exit_app)
    #     # exit_button.pack(side="right", padx=10, pady=10)

    #     # # Hide the games list frame initially
    #     # self.games_list_frame.pack_forget()



    #     # Headline label
    #     headline_label = tk.Label(self, text="Tic Tac Toe - Main menu", font=LARGEFONT, bg="#f0f0f0")
    #     headline_label.pack(pady=10)

    #     # Buttons frame
    #     self.buttons_frame = tk.Frame(self, bg="#f0f0f0")
    #     self.buttons_frame.pack()

    #     # New Game button
    #     self.new_game_button = tk.Button(self.buttons_frame, text="New Game", width=15, font=MEDIUMFONT, bg="#4CAF50", fg="white", relief=tk.FLAT, command=self.new_game)
    #     self.new_game_button.grid(row=0, column=0, padx=10)

    #     # Join a Game button
    #     self.join_game_button = tk.Button(self.buttons_frame, text="Join a Game", width=15, font=MEDIUMFONT, bg="#FFC107", fg="white", relief=tk.FLAT, command=self.join_game)
    #     self.join_game_button.grid(row=0, column=1, padx=10)

    #     # View Leadership Games button
    #     view_games_button = tk.Button(self.buttons_frame, text="View Leadership Games", width=20, font=MEDIUMFONT, bg="#2196F3", fg="white", relief=tk.FLAT, command=self.view_leadership_games)
    #     view_games_button.grid(row=0, column=2, padx=10)

    #     # Games list frame (initially hidden)
    #     self.games_list_frame = tk.Frame(self, bg="#f0f0f0")
    #     self.games_list_frame.pack()

    #     # Listbox for games
    #     self.games_listbox = tk.Listbox(self.games_list_frame, width=50, height=10, font=("Arial", 12), bg="white", selectbackground="#FFC107")
    #     self.games_listbox.pack(side="left", fill="y", padx=5, pady=5)

    #     # Scrollbar for listbox
    #     scrollbar = tk.Scrollbar(self.games_list_frame, orient="vertical", command=self.games_listbox.yview)
    #     scrollbar.pack(side="right", fill="y")

    #     # Configure listbox to use scrollbar
    #     self.games_listbox.config(yscrollcommand=scrollbar.set)

    #     # Example games
    #     self.games_listbox.insert("end", "Game 1 (Owner: Alice, Participants: 3)")
    #     self.games_listbox.insert("end", "Game 2 (Owner: Bob, Participants: 2)")
    #     self.games_listbox.insert("end", "Game 3 (Owner: Charlie, Participants: 4)")

    #     # Bind click event to games listbox
    #     self.games_listbox.bind("<Double-Button-1>", self.on_game_select)

    #     # Text entry for number of players (initially hidden)
    #     self.players_entry_frame = tk.Frame(self, bg="#f0f0f0")
    #     self.players_entry_label = tk.Label(self.players_entry_frame, text="Number of Players:", font=("Arial", 12), bg="#f0f0f0")
    #     self.players_entry_label.pack(side="left", padx=5, pady=5)
    #     self.players_entry = tk.Entry(self.players_entry_frame, validate="key", validatecommand=(self.master.register(validate_numbers_entry), "%S") ,font=("Arial", 12), width=10)
    #     self.players_entry.pack(side="left", padx=5, pady=5)

    #     # Logout and Exit buttons frame
    #     logout_exit_frame = tk.Frame(self, bg="#f0f0f0")
    #     logout_exit_frame.pack(side="bottom", fill="x")

    #     # Logout button
    #     logout_button = tk.Button(logout_exit_frame, text="Logout", width=10, font=("Arial", 12), bg="#FFC107", fg="white", relief=tk.FLAT, command=self.logout)
    #     logout_button.pack(side="left", padx=10, pady=10)

    #     # Exit button
    #     exit_button = tk.Button(logout_exit_frame, text="Exit", width=10, font=("Arial", 12), bg="#F44336", fg="white", relief=tk.FLAT, command=self.exit_app)
    #     exit_button.pack(side="right", padx=10, pady=10)

    #     # Hide the games list frame and players entry initially
    #     self.games_list_frame.pack_forget()
    #     self.players_entry_frame.pack_forget()

    # def new_game(self):
    #     self.games_list_frame.pack_forget() # hide the listbox
    #     if (self.new_game_button.cget('text') == "New Game"):
    #         self.players_entry_frame.pack()
    #         self.new_game_button.config(text="start!")
    #     else:
    #         players_entry = self.players_entry.get()
    #         if (players_entry == ""  or  int(players_entry) < 2  or  int(players_entry) > 8):
    #             messagebox.showinfo("message", "please insert a valid number of players (2-8 allowed)")
    #         else:
    #             self.controller.messageChannel.setRequest("newGame", int(players_entry))

    #             t = threading.Thread(target=self.newGame_helper)
    #             t.start()
    #             schedule_check(self, t, self.check_if_newGame_done.__name__)



    #     # Function to handle New Game button click
    #     print("New Game button clicked")

    # def newGame_helper(self):
    #     """check if a response from the server about the auth request has arrived
    #     """
    #     while (self.controller.messageChannel.response == None):
    #         pass

    #     # # Replace this with your authentication logic
    #     # if token == "admin":
    #     #     messagebox.showinfo("Login Successful", "Welcome, {}".format(token))
    #     #     # Add code to navigate to the next page or perform further actions after authentication
    #     # else:
    #     #     messagebox.showerror("Login Failed", "Invalid username or password")

    # def check_if_newGame_done(self, t):
    #     """if the thread 't' is dead then it means a response from the server about the auth request has arrived,
    #         the function handle that response
    #     Args:
    #         t (Thread): the thread that is in charge of the newGame response
    #     """
    #     if not t.is_alive():
    #         match self.controller.messageChannel.response["response"]:
    #             case "newRegisteredGame":
    #                 print("check_new_game")
    #                 if self.controller.currentPage is MainPage:
    #                     self.controller.show_page(GamePage, self.controller.messageChannel.response["value"], isNew = True)
    #                     # self.controller.message_buffer.append("registered successfully, " + self.controller.messageChannel.response["value"] + "!")
    #             case "errorHasOccured":
    #                 messagebox.showinfo("message", "an error has occured during a try to initiate a new game")
    #     else:
    #         # Otherwise check again after one second.
    #         schedule_check(self, t, self.check_if_newGame_done.__name__)

    # def join_game(self):
    #     # Function to handle Join a Game button click
    #     self.players_entry_frame.pack_forget()
    #     self.games_list_frame.pack()
    #     print("Join a Game button clicked")

    # def view_leadership_games(self):
    #     # Function to handle View Leadership Games button click
    #     print("View Leadership Games button clicked")

    # def on_game_select(self, event):
    #     # Function to handle clicking on a game entry
    #     selected_index = self.games_listbox.curselection()
    #     if selected_index:
    #         selected_game = self.games_listbox.get(selected_index)
    #         print(f"Selected game: {selected_game}")

    # def logout(self):
    #     self.controller.messageChannel.setRequest("logout", "a")
    #     self.controller.show_page(AuthPageToken)


    # def exit_app(self):
    #     """upon clicking the 'exit' button, handle exiting the game gracefully by sending a message
    #         to the server
    #     """
    #     self.controller.messageChannel.setRequest("exit", "a")



##############################################################
##############################################################
##############################################################
        

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




##########################################################
##########################################################
##########################################################


# class GamePage(tk.Frame):
    
#     def __init__(self, parent, controller, game_ID: str = ""):
#         tk.Frame.__init__(self, parent)
#         self.master = parent
#         self.grid(row=0, column=0, sticky="nsew")
#         self.timer_label = None  # Initialize timer_label attribute
#         self.create_widgets()
#         self.start_timer()

#         self.game_ID = game_ID


#     def create_widgets(self):
#         # Create the grid for the Tic Tac Toe game
#         self.buttons = []
#         for i in range(3):
#             row_buttons = []
#             for j in range(3):
#                 button = tk.Button(self, text="", width=5, height=2, font=("Helvetica", 20), command=lambda row=i, col=j: self.button_click(row, col))
#                 button.grid(row=i, column=j, padx=5, pady=5)
#                 row_buttons.append(button)
#             self.buttons.append(row_buttons)

#         # Create text view for messages
#         self.message_label = tk.Label(self, text="Messages will appear here", font=("Helvetica", 12))
#         self.message_label.grid(row=3, column=0, columnspan=3, pady=10)

#         # Create timer label
#         self.timer_label = tk.Label(self, text="Timer", font=("Helvetica", 12))
#         self.timer_label.grid(row=0, column=3, rowspan=3, padx=10)

#     def button_click(self, row, col):
#         # Function to handle button clicks
#         self.buttons[row][col].config(text="X", state=tk.DISABLED)  # Place X on the clicked button

#         # You can implement more logic here for the game

#     def start_timer(self):
#         # Function to start the timer
#         self.start_time = time.time()
#         self.update_timer()

#     def update_timer(self):
#         # Function to update the timer label
#         elapsed_time = time.time() - self.start_time
#         self.timer_label.config(text=f"Timer: {int(elapsed_time)} sec")
#         self.timer_label.after(1000, self.update_timer)


##########################################################
##########################################################
##########################################################

class GamePage(tk.Frame):

    def __init__(self, parent, controller, num_of_players : int,  game_ID: str = "", board = ""):
        tk.Frame.__init__(self, parent)
        self.master = parent
        self.game_ID = game_ID
        self.size = num_of_players + 1  # size of board in x and y axis
        self.configure(bg="#f0f0f0")    # Set background color
        if board != "":
            self.board = board
            self.joinedAfterStart = True
        else:
            self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
            self.joinedAfterStart = False
        
        self.symbol_player = 'O'
        

        self.isStarted = False
        self.yourTurn = False

        self.message_buffer = []


        self.create_widgets()
        self.start_time = time.time()
        self.update_timer_and_messages()

    def create_widgets(self):
        # Frame for the grid
        self.grid_frame = tk.Frame(self, bg="#f0f0f0")
        self.grid_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            self.grid_frame.grid_columnconfigure(i, weight=1)  # Expand columns equally
            self.grid_frame.grid_rowconfigure(i, weight=1)     # Expand rows equally
            for j in range(self.size):
                self.buttons[i][j] = tk.Button(self.grid_frame, text='', font=('Arial', 16, 'bold'), width=3, height=1,
                                                command=lambda i=i, j=j: self.on_button_click(i, j), bg="#ffffff", fg="#000000", bd=1, relief="solid")
                self.buttons[i][j].grid(row=i, column=j, sticky="nsew")
                
        # if a spectator has joined in the middle of a game, we need to initialize his board
        if (self.joinedAfterStart):
            for i in range(self.size):
                for j in range(self.size):
                    self.buttons[i][j].config(text=self.board[i][j])
        
        # Frame for buttons and timer
        self.bottom_frame = tk.Frame(self, bg="#f0f0f0")
        self.bottom_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.quit_button = tk.Button(self.bottom_frame, text="Quit Game", command=self.quit_game, font=('Arial', 12), bg="#d32f2f", fg="#ffffff", bd=1, relief="solid")
        self.quit_button.grid(row=0, column=0, pady=5, padx=5, sticky="ew")

        self.exit_button = tk.Button(self.bottom_frame, text="Exit", command=self.exit_app, font=('Arial', 12), bg="#303f9f", fg="#ffffff", bd=1, relief="solid")
        self.exit_button.grid(row=1, column=0, pady=5, padx=5, sticky="ew")

        self.timer_label = tk.Label(self.bottom_frame, text="", font=('Arial', 12), bg="#f0f0f0")
        self.timer_label.grid(row=2, column=0, pady=5, padx=5, sticky="ew")

        # Frame for messages with scrollable area
        self.message_frame = tk.Frame(self, bg="#f0f0f0")
        self.message_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.message_scrollbar = tk.Scrollbar(self.message_frame)
        self.message_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_text = tk.Text(self.message_frame, height=5, width=50, font=('Arial', 12), bg="#ffffff", fg="#000000", bd=1, relief="solid")
        self.message_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.message_text.config(state=tk.DISABLED)  # Make text area read-only

        self.message_scrollbar.config(command=self.message_text.yview)
        self.message_text.config(yscrollcommand=self.message_scrollbar.set)

        # Configure row and column weights to make the message frame stretchable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
    
    def assignSymbol(self, num: int):
        match num:
            case 1:
                self.symbol_player = 'O'
            case 2:
                self.symbol_player = 'X'
            case 3:
                self.symbol_player = '$'
            case 4:
                self.symbol_player = '#'
            case 5:
                self.symbol_player = '@'
            case 6:
                self.symbol_player = '+'
            case 7:
                self.symbol_player = '%'
            case 8:
                self.symbol_player = '='     
    

    def on_button_click(self, row, col):
        if self.yourTurn:
            if self.board[row][col] == ' ':
                self.board[row][col] = self.symbol_player
                self.buttons[row][col]['text'] = self.symbol_player
                # if self.check_winner(row, col):
                #     self.add_message(f"Player {self.current_player} wins!")
                #     self.disable_buttons()
                # elif self.check_draw():
                #     self.add_message("It's a draw!")
                #     self.disable_buttons()
                # else:
                #     self.current_player = 'O' if self.current_player == 'X' else 'X'
                #     self.start_time = time.time()  # Restart timer for next move
                #     self.update_timer()

    def check_winner(self, row, col):
        # Check row
        if all(self.board[row][c] == self.current_player for c in range(self.size)):
            return True
        # Check column
        if all(self.board[r][col] == self.current_player for r in range(self.size)):
            return True
        # Check diagonals if applicable
        if row == col:
            if all(self.board[i][i] == self.current_player for i in range(self.size)):
                return True
        if row + col == self.size - 1:
            if all(self.board[i][self.size - 1 - i] == self.current_player for i in range(self.size)):
                return True
        return False

    def check_draw(self):
        return all(self.board[row][col] != ' ' for row in range(self.size) for col in range(self.size))

    def disable_buttons(self):
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j].config(state=tk.DISABLED)

    def update_timer_and_messages(self):
        
        if (len(self.message_buffer) != 0):
            for message in self.message_buffer:
                self.add_message(message)
            self.message_buffer.clear()

        if (self.isStarted):
            elapsed_time = int(time.time() - self.start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
        
        self.timer_label.after(1000, self.update_timer_and_messages)

    def add_message(self, message):
        self.message_text.config(state=tk.NORMAL)  # Enable editing temporarily
        self.message_text.insert('1.0', message + '\n')
        self.message_text.config(state=tk.DISABLED)  # Make read-only again
        self.message_text.see('1.0')  # Scroll to the bottom

    def quit_game(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit the game?"):
            self.destroy()

    def exit_app(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit the application?"):
            self.quit()


##########################################################
##########################################################
##########################################################

def schedule_check(tk : tk.Tk, t : threading.Thread, func_name):
    """
    Schedule the execution of the `check_if_done()` function after
    one second.
    """
    func = getattr(tk,func_name)
    tk.after(500, func, t)

def validate_numbers_entry(text):
    return text.isdecimal()