import sys
import json
import io
import struct
import socket as sckt
from tkinter import messagebox

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


# Generate a key and IV (Initialization Vector)
key = b'\x04\x03|\xeb\x8dSh\xe0\xc5\xae\xe5\xe1l9\x0co\xca\xb1"\r-Oo\xbaiYa\x1e\xd1\xf7\xa2\xdf'
iv = b'#\xb59\xee\xa7\xc4@n\xe5r\xac\x97lV\xff\xf1'
backend1 = default_backend()

def encrypt(plaintext: bytes):
    """function to encrypt plaintext using AES-CBC

    Args:
        plaintext (bytes): the bytes to encrypt

    Returns:
        bytes: the bytes after encryption
    """
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend1)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext

def decrypt(ciphertext: bytes):
    """ function to decrypt ciphertext using AES-CBC

    Args:
        ciphertext (bytes): the bytes to decrypt

    Returns:
        bytes: the bytes after decryption
    """
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend1)
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return decrypted_data


# conf_path = os.getcwd()
# sys.path.append(conf_path)
# level_up = conf_path[:conf_path.rfind("\\")]
# sys.path.append(level_up)


gui = None


class Message:
    """manage received and sent messages
    """
    def __init__(self, sock : sckt.socket, addr: tuple):
        """initialize socket, buffers and queues

        Args:
            sock (sckt.socket): a socket object
            addr (tuple): host IP, host PORT
        """
        self.sock = sock
        self.addr = addr
        self.requests = []
        self._recv_buffer = b""
        self._send_buffer = b""
        self._request_queued = True
        self._jsonheader_len = None
        self.jsonheader = None
        self.responses = []

        self.last_event = "read"

    def process_events(self, mask: bytes):
        """process reading and writing events

        Args:
            mask (bytes): a mask to distinguish between reading and writing operations
        """
        if mask & 0b01:
            self.read()
            self.last_event = "read"
            
        if mask & 0b10:
            self.write()
            self.last_event = "write"



    def read(self):
        """seperat ethe reading operation to the different parts of a message
        """
        isRead = self._read()
        if (isRead  or  self._recv_buffer != b""):

            if self._jsonheader_len is None:
                self.process_protoheader() # read and interpret the header length (first 2 bytes)

            if self._jsonheader_len is not None:
                if self.jsonheader is None:
                    self.process_jsonheader() # read and interpret the header

            if self.jsonheader:
                if self.responses == []  or  self.last_event == "read":
                    self.process_response() # read and interpret the content of the message


    
    def _read(self) -> bool:
        """try reading bytes from the receiving buffer and interpret it as a message

        Returns:
            bool: is new data that was read
        """
        try:
            # Should be ready to read
            data = decrypt(self.sock.recv(16384))
            print("\n", data, "\n")
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data
                return True
            else:
                # raise RuntimeError("Peer closed.")
                return False



    def process_protoheader(self):
        """read first 2 bytes which represent the header length and remove them from the receiving buffer
        """
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack(">H", self._recv_buffer[:hdrlen])[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]


    def process_jsonheader(self):
        """read and process header of message (size was received earlier in the first 2 bytes)

        Raises:
            ValueError: raise this exception if the header is not found
        """
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = self._json_decode(
                self._recv_buffer[:hdrlen], "utf-8"
            )
            self._recv_buffer = self._recv_buffer[hdrlen:] # remove the bytes that was read from the buffer
            for reqhdr in (
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f"Missing required header '{reqhdr}'.")


    def process_response(self):
        """read and process the content of the message
        """
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            print("not enough data")
            return
        data = self._recv_buffer[:content_len]              # extract the message content rom the buffer
        self._recv_buffer = self._recv_buffer[content_len:] # remove the bytes that was read from the buffer
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.responses.append(self._json_decode(data, encoding))
            print(f"Received response {self.responses[0]!r} from {self.addr}")
            self._process_response_json_content()           # handle the response according to its content
        else:
            # Binary or unknown content-type
            self.responses.append(data)
            print(
                f"Received {self.jsonheader['content-type']} "
                f"response from {self.addr}"
            )
            self._process_response_binary_content()
                
        self.jsonheader = None              # clear the header and header_len variables, enabling reading another response
        self._jsonheader_len = None



    def _process_response_json_content(self):
        """handle eahch response accoring to its content
        """
        value = self.responses[0]["value"]
        currentPage = gui.currentPageInstance # a link to the GUI

        match self.responses[0]["response"]: # examine the headline of the message
            case "9_afterOneMove": # after a move of a player, restart timer and append messages to display to the other players
                                   # 'value' should be: ( (row,col,symbol), nikName )
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.restartTimer()
                    currentPage.updateBoardAndButton(value[0][0], value[0][1], value[0][2])
                    currentPage.game_turn_label.config(text="other's turn", bg="#0066cc", fg="#ffffff")
                    currentPage.message_buffer.append("## The next to play is: " + value[1])
                    self.responses.pop(0) # pop this response from the queue, it has been handled

            case "10_YourMoveArrived": # a message sent only to the player whose turn has arrived
                                       # 'value' should be: ( row, col, symbol )
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.restartTimer()
                    if (value[0] != -1): # in case of timeout, value should be (-1, -1, -1)
                        currentPage.updateBoardAndButton(value[0], value[1], value[2])
                    else:
                        currentPage.message_buffer.append("## timeout for last player")
                    currentPage.game_turn_label.config(text="turn's yours", bg="#00cc00", fg="#ffffff")
                    currentPage.message_buffer.append("## it's your turn to play!")
                    currentPage.yourTurn = True
                    self.responses.pop(0) # pop this response from the queue, it has been handled

            case "11_victory": # a victory was declared by the server
                               # 'value' should be: ( (row,col,symbol), nikName_of_winner )
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.updateBoardAndButton(value[0][0], value[0][1], value[0][2])
                    currentPage.isStarted = False
                    currentPage.game_result = "over"
                    currentPage.game_turn_label.config(text="game's  over", bg="#ff0000", fg="#ffffff")
                    currentPage.message_buffer.append("## " + value[1] + " has won the game, well done!")
                    self.responses.pop(0) # pop this response from the queue, it has been handled

            case "12_youWon": # a seperat message for the winner itself
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.isStarted = False
                    currentPage.game_result = "over"
                    currentPage.game_turn_label.config(text="  you won!  ", bg="#00cc00", fg="#ffffff")
                    currentPage.message_buffer.append("## you are the winner, congratulations!!!")
                    self.responses.pop(0) # pop this response from the queue, it has been handled

            case "13_draw": # a draw was declared by the server
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.updateBoardAndButton(value[0], value[1], value[2])
                    currentPage.isStarted = False
                    currentPage.game_result = "over"
                    currentPage.game_turn_label.config(text="    draw    ", bg="#ff8000", fg="#ffffff")
                    currentPage.message_buffer.append("## it's a draw, the game is over.")
                    self.responses.pop(0) # pop this response from the queue, it has been handled

            case "4_exit": # exit the app response, arrive as a response to an exit request
                self.close()

            case "5_newPlayer": # we get the following response: { "5_newPlayer" : <number of remaining num of players to join>}
                if currentPage.__class__.__name__ == "GamePage":
                    strForDisplay = "## waiting for " + str(value) + " more players to join and then we start!"
                    currentPage.message_buffer.append(strForDisplay)
                    self.responses.pop(0) # pop this response from the queue, it has been handled
            
            case "14_newSpectator":  # we get the following response: { "14_newSpectator" : num_of_players-num_of_active_players }
                if currentPage.__class__.__name__ == "GamePage":
                    if (value == 0): # the game has already started
                        currentPage.message_buffer.append("## The game has already started, have a seat and enjoy watching!")
                    else: # num_of_players-num_of_active_players > 0, which means that the game has not yet started
                        strForDisplay = "## waiting for " + str(value) + " more players to join and then we start!"
                        currentPage.message_buffer.append(strForDisplay)
                    self.responses.pop(0) # pop this response from the queue, it has been handled

            case "15_timeout": # a timeout has occurred, notify this user about it
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.restartTimer()
                    currentPage.game_turn_label.config(text="other's turn", bg="#0066cc", fg="#ffffff")
                    currentPage.message_buffer.append("## timeout for " + value[0] + ", the turn is passed to " + value[1])
                    self.responses.pop(0) # pop this response from the queue, it has been handled

            case "6_beforeStart": # a seperate message for each player, informing him of his symbol and turn
                if currentPage.__class__.__name__ == "GamePage":
                    strForDisplay = "## The game is about to begin, your turn is " + str(value[0]) + " and your symbol is " + gui.currentPageInstance.assignSymbol(value[1])
                    currentPage.message_buffer.append(strForDisplay)
                    currentPage.assignSymbol(value[1])
                    self.responses.pop(0) # pop this response from the queue, it has been handled
            
            case "7_start": # start the game (initialize timer)
                if currentPage.__class__.__name__ == "GamePage":
                    print("7_start")
                    currentPage.game_turn_label.config(text="started", bg="#00cc00", fg="#ffffff")
                    currentPage.game_result = "started"
                    currentPage.message_buffer.append("## Last player has joined, let the tournament begin!")
                    currentPage.message_buffer.append("## First to play is " + value + ". And remember, "+ str(currentPage.secondsForTimeout) + " seconds for a move, no excuse accepted!")
                    currentPage.restartTimer()
                    currentPage.isStarted = True
                    self.responses.pop(0) # pop this response from the queue, it has been handled

            case "8_yourMove": # inform a player that it's his turn
                print("8_yourMove")
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.message_buffer.append("## it's your turn to play, the clock is ticking!")
                    currentPage.game_turn_label.config(text="your turn", bg="#00cc00", fg="#ffffff")
                    currentPage.yourTurn = True
                    self.responses.pop(0) # pop this response from the queue, it has been handled
            
            case "18_someoneQuitted": # someone exitted, inform the participants that the game is not valid anymore and stop the timer
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.message_buffer.append("## someone got out of the game, it is not valid anymore :-(")
                    currentPage.game_turn_label.config(text="game's paused", bg="#00cc00", fg="#ffffff")
                    currentPage.isStarted = False
                    currentPage.game_result = "over"
                    self.responses.pop(0) # pop this response from the queue, it has been handled
            

        
    def _process_response_binary_content(self):
        """process response in binery repr and not json repr
        """
        content = self.responses[0]
        print(f"Got response: {content!r}")

        

    def _json_decode(self, json_bytes: bytes, encoding: str):
        """decode the json object arrived from the server

        Args:
            json_bytes (bytes): the bytes to decode
            encoding (str): the type of format to decode to

        Returns:
            dict: a dict of property and its value
        """
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj





    def setRequest(self, action: str, value : str):
        """set the request designated for sending to the server

        Args:
            action (str): what action was occurred
            value (str): any content or information about the action
        """
        print(f"set request: {action}, {value}")
        self.requests.append({
            "action" : action,
            "value" : value,
            "type" : "text/json",
            "encoding" : "utf-8"
        })
        self._request_queued = False





    def write(self):
        """manage writing operation
        """
        if not self._request_queued:    # insert a new request only if all the requests were handled already
            self.queue_request()

        self._write() # actually write to the sending buffer

        if self._request_queued:
            if not self._send_buffer:                
                # self._set_selector_events_mask("r")
                # self._set_selector_events_mask("rw")
                pass



    def _write(self):
        """send some bytes to the server
        """
        if self._send_buffer:

            self.last_event = "write"

            # print(f"Sending {self._send_buffer!r} to {self.addr}")
            try:
                
                # Should be ready to write
                length = len(self._send_buffer)
                if (length > 2048):
                    data = self._send_buffer[:2048]
                else:
                    data = self._send_buffer

                self.sock.send(encrypt(data))
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass

            else:
                self._send_buffer = self._send_buffer[len(data):]


    def queue_request(self):
        """build a request with all its parts (header and content)
        """
        action = self.requests[0]["action"]
        
        value = self.requests[0]["value"]
        
        content_type = self.requests[0]["type"]

        content_encoding = self.requests[0]["encoding"]
        
        if content_type == "text/json":
            req = {
                "content_bytes": self._json_encode((action, value), content_encoding),
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        else:
            req = {
                "action_bytes": action,
                "value_bytes": value,
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        message = self._create_message(**req) # create the message from the 'req' variable
        self._send_buffer += message          # add 'message' to the sending buffer
        self.requests.pop(0)
        if (len(self.requests) == 0):
            self._request_queued = True


    # def _set_selector_events_mask(self, mode):
    #     """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
    #     if mode == "r":
    #         events = selectors.EVENT_READ
    #     elif mode == "w":
    #         events = selectors.EVENT_WRITE
    #     elif mode == "rw":
    #         events = selectors.EVENT_READ | selectors.EVENT_WRITE
    #     else:
    #         raise ValueError(f"Invalid events mask mode {mode!r}.")
    #     self.selector.modify(self.sock, events, data=self)

    
    def _json_encode(self, obj, encoding):
        """encode the message bytes a a json object

        Args:
            obj: object to encode
            encoding (str): type of encoding

        Returns:
            str: the encoded object as a string
        """
        return json.dumps(obj, ensure_ascii=False).encode(encoding)


    def _create_message(self, *, content_bytes: bytes, content_type: str, content_encoding: str):
        """create a sequence of bytes representing a message with all the differnet parts of a message

        Args:
            content_bytes (bytes): the bytes to send
            content_type (str): type of format (usually text/json)
            content_encoding (str): type of encoding (usually utf-8)

        Returns:
            bytes: the message as a sequence of bytes
        """
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    



    def close(self, isClosedUnexpectedly = False):
        """close this massage manager

        Args:
            isClosedUnexpectedly (bool, optional): flag to know if the connectino was closed abruplty. Defaults to False.
        """
        try:
            if isClosedUnexpectedly == True:
                result = None
                result = messagebox.showerror("error", "the server is not connected, try and come back later  )-:")
                while (result == None):
                    pass
            print(f"\nClosing connection to {self.addr}\n")

            self.sock.close()
        except OSError as e:
            print(f"Error: socket.close() exception for {self.addr}: {e!r}")
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None


    def updateAccessToGUI(self, presentation_instance):
        """update the variable through whioch this module can access the GUI

        Args:
            presentation_instance (AppRoot): an instance of the appRoot which holds a reference to the GUI
        """
        global gui
        gui = presentation_instance