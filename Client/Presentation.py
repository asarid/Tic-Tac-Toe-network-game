import tkinter as tk
import time
from tkinter import ttk
from tkinter import messagebox
import threading
import datetime

MEDIUMFONT = ("Verdana", 15)
LARGEFONT = ("Verdana", 30)



class AuthPageToken(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        
        self.master = master
        self.controller = controller
        self.configure(bg="#f0f0f0")
        self.create_widgets()


    def create_widgets(self):
        # Create headline
        headline_label = ttk.Label(self, text="Tic Tac Toe", font=LARGEFONT, background='#F0F0F0', foreground='#333333')
        headline_label.pack(pady=10)
        
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
        signup_button = tk.Button(self, text="Sign Up", command=lambda: self.controller.show_page(SignUpPage), font=("Verdana", 18), bg='#4CAF50', fg='white')
        signup_button.place(relx=0.3, rely=0.9)

    
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
        while (self.controller.messageChannel.responses == []  or
               self.controller.messageChannel.responses[0]["response"][0] != "0"):
            pass


    def check_if_auth_done(self, t):
        """if the thread 't' is dead then it means a response from the server about the auth request has arrived,
            the function handle that response
        Args:
            t (Thread): the thread that is in charge of the auth response
        """
        # If the thread has finished, re-enable the button and show a message.
        if not t.is_alive():
            self.login_button["state"] = "normal"
            match self.controller.messageChannel.responses[0]["response"]:
                case "0_verified":
                    if self.controller.currentPage is AuthPageToken:
                        self.controller.show_page(MainPage)
                case "0_AlreadyRegistered":
                    self.message_label.config(text = "this user is already registered")
                case "0_tokenNotFound":
                    self.message_label.config(text = "this token was not found")
            self.controller.messageChannel.responses.pop(0)

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
        headline_label.pack(pady=10)

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

        
    def signUp_helper(self):
        """check if a response from the server about the signUp request has arrived.
            At first we check if the response is None i.e. no response has arrived, and then we verify
            that the response is what we expected to, i.e. "response" == "1_newUser", else we continue looping.
        """
        while (self.controller.messageChannel.responses == []  or  
               self.controller.messageChannel.responses[0]["response"][0] != "1"):
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

            match self.controller.messageChannel.responses[0]["response"]:
                case "1_newUser":
                    if self.controller.currentPage is SignUpPage:
                        self.token_label1.config(text="Your unique token is " + str(self.controller.messageChannel.responses[0]["value"]))
                        self.token_label1.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="w")
                case "1_errorHasOccured":
                        self.token_label1.config(text="error has occured, try again")
                        self.token_label1.grid(row=2, column=0, columnspan=2, pady=(20, 50), sticky="w")  
            self.controller.messageChannel.responses.pop(0)
      
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
        tk.Frame.__init__(self, master)
        
        self.master = master
        self.controller = controller
        self.configure(bg="#f0f0f0")
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
        view_games_button = tk.Button(self.buttons_frame, text="View Leadership Games", width=20, font=("Arial", 12), bg="#2196F3", fg="white", relief=tk.FLAT, command=lambda: self.controller.show_page(StatisticsPage))
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
        self.players_entry = tk.Entry(self.players_entry_frame, font=("Arial", 12), width=10, justify='center')
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
        while (self.controller.messageChannel.responses == []  or  
               self.controller.messageChannel.responses[0]["response"][0] != "2"):
            pass


    def check_if_newGame_done(self, t):
        """if the thread 't' is dead then it means a response from the server about the auth request has arrived,
            the function handle that response
        Args:
            t (Thread): the thread that is in charge of the newGame response
        """
        if not t.is_alive():
            match self.controller.messageChannel.responses[0]["response"]:
                case "2_newRegisteredGame":
                    game = self.controller.messageChannel.responses[0]["value"] # should be [ game_ID, numOfPlayers ]
                    print("check_new_game")
                    if self.controller.currentPage is MainPage:
                        self.controller.show_page(GamePage, game[1], game[0])
                        self.controller.currentPageInstance.message_buffer.append(f"## waiting for {game[1]-1} more players to join and then we start!")
                case "2_errorHasOccured":
                    messagebox.showinfo("message", "an error has occured during a try to initiate a new game")
            self.controller.messageChannel.responses.pop(0)

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
        
        self.controller.messageChannel.setRequest("fetchActiveGames", "a")


        t = threading.Thread(target=self.fetchActiveGames_helper)
        t.start()
        schedule_check(self, t, self.check_if_fetchActiveGames_done.__name__)


    def fetchActiveGames_helper(self):
        """check if a response from the server about 'fetching the games' request has arrived.
            At first we check if the response is None i.e. no response has arrived, and then we verify
            that the response is what we expected to, i.e. "response" == "3_allActiveGames", else we continue looping.
        """
        while (self.controller.messageChannel.responses == []  or  
               self.controller.messageChannel.responses[0]["response"][0] != "3"):
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

            games = self.controller.messageChannel.responses[0]["value"]
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
        
            self.controller.messageChannel.responses.pop(0)
      
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
                for index, game in enumerate(self.activeGames_occuring):
                    strForDisplay = f"Game {len(self.activeGames_initialized)+index+1} (opened for " + str(game[0]["num_of_players"]) + " players, waiting for " + str(game[0]["num_of_players"]-game[1]) + " more, " + str(game[2]) + " spectators" + ")"
                    self.games_listbox.insert("end", strForDisplay)
                # self.games_listbox.insert("end", *self.activeGames_occuring)

        self.player_last_type = player_type

    def on_game_select(self, event):
        # Function to handle clicking on a game entry

        selected_index = self.games_listbox.curselection()[0]
        print("selected index: ", selected_index)        

        # the user is a spectator in an occurring game
        if (selected_index >= len(self.activeGames_initialized)): 
            selectedGame = self.activeGames_occuring[selected_index-len(self.activeGames_initialized)][0]
            self.controller.show_page(GamePage, selectedGame["num_of_players"], selectedGame["game_ID"], selectedGame["board"], True)

        # the user is either an active player or a spectator in a game that has not yet started
        else:
            selectedGame = self.activeGames_initialized[selected_index][0]
            if self.player_type_var.get() == "spectator":
                self.controller.show_page(GamePage, selectedGame["num_of_players"], selectedGame["game_ID"], "", True)
            else:
                self.controller.show_page(GamePage, selectedGame["num_of_players"], selectedGame["game_ID"])
             

        # send a message to the server that a new player has now joined the game
        if self.player_type_var.get() == "active_player":
            self.controller.messageChannel.setRequest("newJoined", ("player", selectedGame["game_ID"]))
        
        # self.player_type_var.get() == "spectator"
        else:
            self.controller.currentPageInstance.spectator_label.pack()
            self.controller.messageChannel.setRequest("newJoined", ("spectator", selectedGame["game_ID"]))


    def logout(self):
        self.controller.messageChannel.setRequest("logout", "a")
        self.controller.show_page(AuthPageToken)

    def exit_app(self):
        """upon clicking the 'exit' button, handle exiting the game gracefully by sending a message
            to the server
        """
        self.controller.messageChannel.setRequest("exit", "a")


class StatisticsPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        self.master = master
        self.controller = controller
        
        self.games = []
        self.users = []


        self.create_widgets()
        
        self.fetchInfo()


    def create_widgets(self):
        self.headline_label = ttk.Label(self, text="Game Statistics", font=("Helvetica", 30, "bold"), foreground="blue")
        self.headline_label.pack(pady=10)

        self.tabControl = ttk.Notebook(self)

        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text="Games")

        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text="Users")

        self.tabControl.pack(expand=1, fill="x")
        self.tabControl.bind("<<NotebookTabChanged>>", self.tab_changed)

        self.table1_frame = ttk.Frame(self)
        self.table1_frame.pack(fill="both", expand=1, padx=20, pady=10)

        self.table2_frame = ttk.Frame(self)
        self.table2_frame.pack(fill="both", expand=1, padx=20, pady=10)

        self.treeViewGames = ttk.Treeview(self.table1_frame, columns=("index", "date", "duration", "num_of_players", "status", "winner"), show="headings")
        self.treeViewGames.heading("index", text="#")
        self.treeViewGames.heading("date", text="date")
        self.treeViewGames.heading("duration", text="duration")
        self.treeViewGames.heading("num_of_players", text="number of players")
        self.treeViewGames.heading("status", text="status")
        self.treeViewGames.heading("winner", text="winner")

        self.treeViewGames.column("index", width=50, anchor="center")
        self.treeViewGames.column("date", width=150, anchor="center")
        self.treeViewGames.column("duration", width=50, anchor="center")
        self.treeViewGames.column("num_of_players", width=100, anchor="center")
        self.treeViewGames.column("status", width=50, anchor="center")
        self.treeViewGames.column("winner", width=150, anchor="center")

        self.treeViewUsers = ttk.Treeview(self.table2_frame, columns=("user_name", "number_of_games", "number_of_winnings", "number_of_loses", "number_of_draws"), show="headings")
        self.treeViewUsers.heading("user_name", text="user name")
        self.treeViewUsers.heading("number_of_games", text="number of games")
        self.treeViewUsers.heading("number_of_winnings", text="won")
        self.treeViewUsers.heading("number_of_loses", text="lost")
        self.treeViewUsers.heading("number_of_draws", text="draw")

        self.treeViewUsers.column("user_name", width=150, anchor="center")
        self.treeViewUsers.column("number_of_games", width=100, anchor="center")
        self.treeViewUsers.column("number_of_winnings", width=100, anchor="center")
        self.treeViewUsers.column("number_of_loses", width=100, anchor="center")
        self.treeViewUsers.column("number_of_draws", width=100, anchor="center")

        self.treeViewGames.pack(side="left", fill="both", expand=True)
        self.treeViewUsers.pack(side="left", fill="both", expand=True)


        self.scrollbar1 = ttk.Scrollbar(self.table1_frame, orient="vertical", command=self.treeViewGames.yview)
        self.scrollbar1.pack(side="right", fill="y")
        self.treeViewGames.configure(yscroll=self.scrollbar1.set)

        self.scrollbar2 = ttk.Scrollbar(self.table2_frame, orient="vertical", command=self.treeViewUsers.yview)
        self.scrollbar2.pack(side="right", fill="y")
        self.treeViewUsers.configure(yscroll=self.scrollbar2.set)

        self.table2_frame.pack_forget()

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=10)

        self.exit_button = ttk.Button(self.button_frame, text="Exit", command=self.exitApp, width=10)
        self.exit_button.pack(side="left", padx=10)

        self.back_button = ttk.Button(self.button_frame, text="Back to Main", command=lambda: self.controller.show_page(MainPage), width=15)
        self.back_button.pack(side="left", padx=10)
        

        # Initialize style
        s = ttk.Style()

        # Create style for the first frame
        s.configure('TFrame', background='#f0f0f0')
        
        self.configure(bg="#f0f0f0")
        self.headline_label.configure(background="#f0f0f0")

        
    def fetchInfo(self):
        self.controller.messageChannel.setRequest("fetchGamesHistory", "")
        
        t = threading.Thread(target=self.gamesHistory_helper)
        t.start()
        schedule_check(self, t, self.check_if_gamesHistory_done.__name__)

        

    def gamesHistory_helper(self):
        """check if a response from the server about the 'fetchGamesHistory' request has arrived.
            At first we check if the response is None i.e. no response has arrived, and then we verify
            that the response is what we expected to, i.e. "response" == "16_gamesHistory", else we continue looping.
        """
        while (self.controller.messageChannel.responses == []  or
               self.controller.messageChannel.responses[0]["response"][0:2] != "16"):
            pass

    def check_if_gamesHistory_done(self, t):
        """if the thread 't' is dead then it means a response from the server about the 'gamesHistory' request has arrived,
            the function handle that response
        Args:
            t (Thread): the thread that is in charge of the gamesHistory response
        """
        if not t.is_alive():
            print("\ngames_history\n")
            games = self.controller.messageChannel.responses[0]["value"] # should be a list of lists: [... [game_ID: str, game: dict] ...]
            if self.controller.currentPage is StatisticsPage:
                self.games = games
                if games == []:
                    messagebox.showinfo("message", "it seems like the server has no information about games statistics")
                self.populate_table(1)
                self.controller.messageChannel.moreResponsesExpected = True
            print(len(self.controller.messageChannel.responses))
            self.controller.messageChannel.responses.pop(0)

            self.controller.messageChannel.setRequest("fetchUsersStats", "")
        
            t = threading.Thread(target=self.usersStats_helper)
            t.start()
            schedule_check(self, t, self.check_if_usersStats_done.__name__)

        else:
            # Otherwise check again after one second.
            schedule_check(self, t, self.check_if_gamesHistory_done.__name__)
    
    def usersStats_helper(self):
        """check if a response from the server about the 'fetchUsersStats' request has arrived.
            At first we check if the response is None i.e. no response has arrived, and then we verify
            that the response is what we expected to, i.e. "response" == "17_usersStats", else we continue looping.
        """
        while (self.controller.messageChannel.responses == []  or
               self.controller.messageChannel.responses[0]["response"][0:2] != "17"):
            pass            

    def check_if_usersStats_done(self, t):
        """if the thread 't' is dead then it means a response from the server about the 'userStats' request has arrived,
            the function handle that response
        Args:
            t (Thread): the thread that is in charge of the 'userStats' response
        """
        if not t.is_alive():
            usersStats = self.controller.messageChannel.responses[0]["value"] # should be a list of items: (nik name: str, user: dict)
            if self.controller.currentPage is StatisticsPage:
                self.users = usersStats
                if usersStats == []:
                    messagebox.showinfo("message", "it seems like the server has no information about user statistics")
                self.populate_table(2)
            self.controller.messageChannel.responses.pop(0)
        else:
            # Otherwise check again after one second.
            schedule_check(self, t, self.check_if_usersStats_done.__name__)


    def populate_table(self, table):

        # Populate table with data based on the selected tab index
        if table == 1:
            print("len(games): ", len(self.games))
            for i, game in enumerate(self.games):
                date = datetime.datetime.fromisoformat(game[1]["creation_date"]).strftime("%d/%m/%Y")
                duration_micro = str(datetime.timedelta(seconds = game[1]["duration"]))
                index = duration_micro.rfind(".")
                duration = duration_micro if index == -1 else duration_micro[:index]
                if game[1]["game_state"] == 'WON':    
                    status = "victory"
                    winner = game[1]["winner_name"]
                else:
                    status = "draw"
                    winner = "-"
            
                self.treeViewGames.insert("", "end", values=(str(i+1), date, duration, game[1]["num_of_players"], status, winner))
        else:
            self.table = self.treeViewUsers
            self.table.pack(side="left", fill="both", expand=True)
            for user in self.users:
                num_games = user[1]["games_participated"]
                victory = user[1]["games_won"]
                draw = user[1]["games_tie"]
                loses = num_games - victory - draw
                self.treeViewUsers.insert("", "end", values=(user[0], num_games, victory, loses, draw))



    def tab_changed(self, event):
        # Get the index of the currently selected tab
        tab_index = self.tabControl.index(self.tabControl.select())

        if (tab_index == 0):
            # Update the content of the table based on the selected tab
            self.button_frame.pack_forget()
            self.table1_frame.pack(fill="both", expand=1, padx=20, pady=10)
            self.table2_frame.pack_forget()
            self.button_frame.pack(pady=10)
            
        else: # tab_changed = 1
            self.button_frame.pack_forget()
            self.table2_frame.pack(fill="both", expand=1, padx=20, pady=10)
            self.table1_frame.pack_forget()
            self.button_frame.pack(pady=10)


    def exitApp(self):
        """upon clicking the 'exit' button, handle exiting the game gracefully by sending a message
            to the server
        """
        self.controller.messageChannel.setRequest("exit", "a")





class GamePage(tk.Frame):

    def __init__(self, parent, controller, num_of_players : int,  game_ID: str = "", board = "", isSpectator = False):
        tk.Frame.__init__(self, parent)
        self.master = parent
        self.controller = controller
        self.game_ID = game_ID
        self.size = num_of_players + 1  # size of board in x and y axis
        self.configure(bg="#f0f0f0")    # Set background color
        
        # if a spectator has joined in the middle of a game, we need to initialize his board
        if board != "":
            self.board = board
        else:
            self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]

        
        self.symbol_player = 'no'
        self.isSpectator = isSpectator

        self.isStarted = False
        self.yourTurn = False

        self.message_buffer = []

        self.game_result = "waiting"
        self.secondsForTimeout = 30  # put here no more than 59

        self.create_widgets()
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
                self.buttons[i][j] = tk.Button(self.grid_frame, text=self.board[i][j], font=('Arial', 16, 'bold'), width=3, height=1,
                                                command=lambda i=i, j=j: self.on_button_click(i, j), bg="#ffffff", fg="#000000", bd=1, relief="solid")
                self.buttons[i][j].grid(row=i, column=j, sticky="nsew")
                
        
        # Frame for buttons and timer
        self.control_frame = tk.Frame(self, bg="#f0f0f0")
        self.control_frame.grid(row=0, column=1, padx=0, pady=0, sticky="n")
        self.control_frame.grid_propagate(False)

        self.buttons_frame = tk.Frame(self.control_frame, bg="#f0f0f0")
        self.buttons_frame.pack(side="top", fill="y", padx=0, pady=0)

        self.quit_button = tk.Button(self.buttons_frame, text="Quit Game", command=self.quit_game, font=('Arial', 12), bg="#d32f2f", fg="#ffffff", bd=1, relief="solid")
        self.quit_button.grid(row=0, column=0, pady=5, padx=5, sticky="ew")

        self.exit_button = tk.Button(self.buttons_frame, text="Exit", command=self.exit_app, font=('Arial', 12), bg="#303f9f", fg="#ffffff", bd=1, relief="solid")
        self.exit_button.grid(row=1, column=0, pady=5, padx=5, sticky="ew")

        self.timer_label = tk.Label(self.buttons_frame, text="", font=('Arial', 12), bg="#f0f0f0")
        self.timer_label.grid(row=2, column=0, pady=5, padx=5, sticky="ew")

        self.catchSpace_label = tk.Label(self.buttons_frame, text="", font=('Arial', 12), bg="#f0f0f0")
        self.catchSpace_label.grid(row=3, column=0, pady=5, padx=5, sticky="ew")

        self.game_turn_label = tk.Label(self.control_frame, text="you'll  wait", pady=10, padx=20, font=('Arial', 20), bg="#404040", fg="#ffffff")
        self.game_turn_label.pack(side="bottom", fill="y", padx=0, pady=5)

        self.spectator_label = tk.Label(self.control_frame, text="spectator", pady=10, padx=20, font=('Arial', 20), bg="#cc00cc", fg="#ffffff")
        self.spectator_label.pack(side="bottom", fill="y", padx=0, pady=5)
        self.spectator_label.pack_forget()

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
    
    def assignSymbol(self, symbol: int) -> str:
        self.symbol_player = symbol
        return symbol

    def restartTimer(self):
        self.start_time = time.time()

    def on_button_click(self, row, col):
        if self.yourTurn  and  self.board[row][col] == ' ':
                # self.board[row][col] = self.symbol_player
                self.buttons[row][col]['text'] = self.symbol_player
                self.yourTurn = False
                self.controller.messageChannel.setRequest("aMove", ((row, col, self.symbol_player), self.game_ID))

    def updateBoardAndButton(self, row, col, symbol):
        # self.board[row][col] = symbol
        self.buttons[row][col]['text'] = symbol

    def update_timer_and_messages(self):
        
        if (len(self.message_buffer) > 0):
            self.add_message(self.message_buffer.pop(0))
            
            
        if (self.isStarted):
            elapsed_time = int(time.time() - self.start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
        
            if (seconds == self.secondsForTimeout  and  self.yourTurn == True):
                self.yourTurn = False
                self.controller.messageChannel.setRequest("timeout", self.game_ID)

        self.timer_label.after(1000, self.update_timer_and_messages)

    def add_message(self, message):
        self.message_text.config(state=tk.NORMAL)  # Enable editing temporarily
        self.message_text.insert(tk.END, message + '\n\n')
        self.message_text.config(state=tk.DISABLED)  # Make read-only again
        self.message_text.see(tk.END)  # Scroll to the bottom

    def quit_game(self):
        if self.game_result != "over": # game is not over, ask if he is sure about him quitting the game
            if messagebox.askokcancel("Quit", "Are you sure you want to quit the game?"):
                self.controller.messageChannel.setRequest("quitInMiddle", (self.game_ID, self.isSpectator))
                self.controller.show_page(MainPage)
        else:
            self.controller.show_page(MainPage)

    def exit_app(self):
        """upon clicking the 'exit' button, handle exiting the game gracefully by sending a message
            to the server
        """
        if self.game_result != "over":
            if messagebox.askokcancel("Exit", "Are you sure you want to exit the application?"):
                self.controller.messageChannel.setRequest("exit", (self.game_ID, self.isSpectator))
        else:
            self.controller.messageChannel.setRequest("exit", "a")
        


##########################################################
##########################################################
##########################################################

def schedule_check(tk : tk.Tk, t : threading.Thread, func_name):
    """Schedule the execution of the 'check_if_done()' function after
        one second.

    Args:
        tk (tk.Tk): the frame from which the function was called
        t (threading.Thread): the thread that we monitor if it finished its work
        func_name: the name (not 'str') of the function to call after some time defined in the argument to 'after' function
    """
    func = getattr(tk,func_name)
    tk.after(500, func, t)

def validate_numbers_entry(text):
    """function to help validate an entry text if it has numbers only
    """
    return text.isdecimal()