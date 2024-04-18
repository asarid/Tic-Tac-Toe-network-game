import sys
import json
import io
import struct
import socket as sckt
import os
from tkinter import messagebox

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


# Generate a key and IV (Initialization Vector)
key = b'\x04\x03|\xeb\x8dSh\xe0\xc5\xae\xe5\xe1l9\x0co\xca\xb1"\r-Oo\xbaiYa\x1e\xd1\xf7\xa2\xdf'
iv = b'#\xb59\xee\xa7\xc4@n\xe5r\xac\x97lV\xff\xf1'
backend1 = default_backend()

# Function to encrypt plaintext using AES-CBC
def encrypt(plaintext):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend1)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext

# Function to decrypt ciphertext using AES-CBC
def decrypt(ciphertext):
    print("inside decrypt 1")
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend1)
    print("inside decrypt 2")
    decryptor = cipher.decryptor()
    print("inside decrypt 3")
    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    print("inside decrypt 4")
    unpadder = padding.PKCS7(128).unpadder()
    print("inside decrypt 5")
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    print("inside decrypt 6")
    return decrypted_data


conf_path = os.getcwd()
sys.path.append(conf_path)
level_up = conf_path[:conf_path.rfind("\\")]
sys.path.append(level_up)


gui = None


class Message:
    def __init__(self, sock : sckt.socket, addr):
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
        self.moreResponsesExpected = False

    def process_events(self, mask):
        if mask & 0b01:
            self.read()
            self.last_event = "read"
            
        if mask & 0b10:
            self.write()
            self.last_event = "write"

            



    def read(self):
        isRead = self._read()
        if (isRead  or  self._recv_buffer != b""):

            if self._jsonheader_len is None:
                self.process_protoheader()

            if self._jsonheader_len is not None:
                if self.jsonheader is None:
                    self.process_jsonheader()

            if self.jsonheader:
                if self.responses == []  or  self.last_event == "read":
                    print("and condition")
                    self.process_response()


    
    def _read(self) -> bool:
        """try to read from the receiving buffer

        Returns:
            bool: is new data was read
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
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack(">H", self._recv_buffer[:hdrlen])[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]


    def process_jsonheader(self):
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = self._json_decode(
                self._recv_buffer[:hdrlen], "utf-8"
            )
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in (
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f"Missing required header '{reqhdr}'.")


    def process_response(self):
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            print("not enough data")
            return
        print("process_read")
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.responses.append(self._json_decode(data, encoding))
            print(f"Received response {self.responses[0]!r} from {self.addr}")
            self._process_response_json_content()
        else:
            # Binary or unknown content-type
            self.responses.append(data)
            print(
                f"Received {self.jsonheader['content-type']} "
                f"response from {self.addr}"
            )
            self._process_response_binary_content()
                
        self.jsonheader = None
        self._jsonheader_len = None

        # my revision - close only upon user exit
            
        # # Close when response has been processed
        # self.close()


    def _process_response_json_content(self):
        value = self.responses[0]["value"]
        currentPage = gui.currentPageInstance

        match self.responses[0]["response"]:
            case "9_afterOneMove":
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.restartTimer()
                    currentPage.updateBoardAndButton(value[0][0], value[0][1], value[0][2])
                    currentPage.game_turn_label.config(text="other's turn", bg="#0066cc", fg="#ffffff")
                    currentPage.message_buffer.append("## The next to play is: " + value[1])
                    self.responses.pop(0)

            case "10_YourMoveArrived":
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.restartTimer()
                    if (value[0] != -1):
                        currentPage.updateBoardAndButton(value[0], value[1], value[2])
                    else:
                        currentPage.message_buffer.append("## timeout for last player")
                    currentPage.game_turn_label.config(text="turn's yours", bg="#00cc00", fg="#ffffff")
                    currentPage.message_buffer.append("## it's your turn to play!")
                    currentPage.yourTurn = True
                    self.responses.pop(0)

            case "11_victory":
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.updateBoardAndButton(value[0][0], value[0][1], value[0][2])
                    currentPage.isStarted = False
                    currentPage.game_result = "over"
                    currentPage.game_turn_label.config(text="game's  over", bg="#ff0000", fg="#ffffff")
                    currentPage.message_buffer.append("## " + value[1] + " has won the game, well done!")
                    self.responses.pop(0)

            case "12_youWon":
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.isStarted = False
                    currentPage.game_result = "over"
                    currentPage.game_turn_label.config(text="  you won!  ", bg="#00cc00", fg="#ffffff")
                    currentPage.message_buffer.append("## you are the winner, congratulations!!!")
                    self.responses.pop(0)

            case "13_draw":
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.updateBoardAndButton(value[0], value[1], value[2])
                    currentPage.isStarted = False
                    currentPage.game_result = "over"
                    currentPage.game_turn_label.config(text="    draw    ", bg="#ff8000", fg="#ffffff")
                    currentPage.message_buffer.append("## it's a draw, the game is over.")
                    self.responses.pop(0)

            case "4_exit":
                self.close()

            case "5_newPlayer": # we get the following response due to false request: { "5_newPlayer" : <number of remaining num of players to join>}
                if currentPage.__class__.__name__ == "GamePage":
                    strForDisplay = "## waiting for " + str(value) + " more players to join and then we start!"
                    currentPage.message_buffer.append(strForDisplay)
                    self.responses.pop(0)
            
            case "14_newSpectator":  # we get the following response: { "14_newSpectator" : num_of_players-num_of_active_players }
                if currentPage.__class__.__name__ == "GamePage":
                    if (value == 0): # the game has already started
                        currentPage.message_buffer.append("## The game has already started, have a seat and enjoy watching!")
                    else: # num_of_players-num_of_active_players > 0, which means that the game has not yet started
                        strForDisplay = "## waiting for " + str(value) + " more players to join and then we start!"
                        currentPage.message_buffer.append(strForDisplay)
                    self.responses.pop(0)

            case "15_timeout":
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.restartTimer()
                    currentPage.game_turn_label.config(text="other's turn", bg="#0066cc", fg="#ffffff")
                    currentPage.message_buffer.append("## timeout for " + value[0] + ", the turn is passed to " + value[1])
                    self.responses.pop(0)

            case "6_beforeStart":
                if currentPage.__class__.__name__ == "GamePage":
                    strForDisplay = "## The game is about to begin, your turn is " + str(value[0]) + " and your symbol is " + gui.currentPageInstance.assignSymbol(value[1])
                    currentPage.message_buffer.append(strForDisplay)
                    currentPage.assignSymbol(value[1])
                    self.responses.pop(0)
            
            case "7_start":
                if currentPage.__class__.__name__ == "GamePage":
                    print("7_start")
                    currentPage.game_turn_label.config(text="started", bg="#00cc00", fg="#ffffff")
                    currentPage.game_result = "started"
                    currentPage.message_buffer.append("## Last player has joined, let the tournament begin!")
                    currentPage.message_buffer.append("## First to play is " + value + ". And remember, "+ str(currentPage.secondsForTimeout) + " seconds for a move, no excuse accepted!")
                    currentPage.restartTimer()
                    currentPage.isStarted = True
                    self.responses.pop(0)

            case "8_yourMove":
                print("8_yourMove")
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.message_buffer.append("## it's your turn to play, the clock is ticking!")
                    currentPage.game_turn_label.config(text="your turn", bg="#00cc00", fg="#ffffff")
                    currentPage.yourTurn = True
                    self.responses.pop(0)
            
            case "18_someoneQuitted":
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.message_buffer.append("## someone got out of the game, it is not valid anymore :-(")
                    currentPage.game_turn_label.config(text="game's paused", bg="#00cc00", fg="#ffffff")
                    currentPage.isStarted = False
                    currentPage.game_result = "over"
                    self.responses.pop(0)
            
        # result = content.get("result")
        # print(f"Got result: {result}")
        
        # ui.frames[ui.AuthPageToken].setTokenEntry("Mom")


########################
########################
        
    def _process_response_binary_content(self):
        content = self.responses[0]
        print(f"Got response: {content!r}")

########################
########################
        

    def _json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj





    def setRequest(self, action: str, value : str):
        print(f"set request: {action}, {value}")
        self.requests.append({
            "action" : action,
            "value" : value,
            "type" : "text/json",
            "encoding" : "utf-8"
        })
        self._request_queued = False




    def write(self):
        if not self._request_queued:
            self.queue_request()

        self._write()

        if self._request_queued:
            if not self._send_buffer:
                # Set selector to listen for read events, we're done writing.
                
                # self._set_selector_events_mask("r")
                # self._set_selector_events_mask("rw")
                pass



    def _write(self):
        if self._send_buffer:

            # self.response = None
            # self.jsonheader = None
            # self._jsonheader_len = None

            self.last_event = "write"

            print(f"Sending {self._send_buffer!r} to {self.addr}")
            try:
                
                # self.sock.connect_ex(self.addr)
                
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
            # except Exception:
            #     print("error")
            else:
                self._send_buffer = self._send_buffer[len(data):]


    def queue_request(self):
        action = self.requests[0]["action"]
        #content = "hello everyone!"
        
        value = self.requests[0]["value"]
        
        content_type = self.requests[0]["type"]
        #content_type = "text/json"

        content_encoding = self.requests[0]["encoding"]
        #content_encoding = "utf-8"
        
        if content_type == "text/json":
            req = {
                "content_bytes": self._json_encode((action, value), content_encoding),
                #"content_bytes": self._json_encode(content, content_encoding),
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        else:
            req = {
                "action_bytes": action,
                "value_bytes": value,
                #"content_bytes": content,
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        message = self._create_message(**req)
        self._send_buffer += message
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
        return json.dumps(obj, ensure_ascii=False).encode(encoding)


    def _create_message(self, *, content_bytes, content_type, content_encoding):
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
        try:
            if isClosedUnexpectedly == True:
                result = None
                result = messagebox.showerror("error", "the server is not connected, try and come back later  )-:")
                while (result == None):
                    pass
            print(f"Closing connection to {self.addr}")

            self.sock.close()
        except OSError as e:
            print(f"Error: socket.close() exception for {self.addr}: {e!r}")
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None


    def updateAccessToGUI(self, presentation_instance):
        global gui
        gui = presentation_instance