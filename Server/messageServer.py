import sys
import json
import struct
import socket


# import os
# conf_path = os.getcwd()
# level_up = conf_path[:conf_path.rfind("\\")]
# sys.path.insert(1, level_up)

import BusinessLogic as BL

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# Generate a key and IV (Initialization Vector)
key = b'\x04\x03|\xeb\x8dSh\xe0\xc5\xae\xe5\xe1l9\x0co\xca\xb1"\r-Oo\xbaiYa\x1e\xd1\xf7\xa2\xdf'
iv = b'#\xb59\xee\xa7\xc4@n\xe5r\xac\x97lV\xff\xf1'

# Function to encrypt plaintext using AES-CBC
def encrypt(plaintext):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext

# Function to decrypt ciphertext using AES-CBC
def decrypt(ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return decrypted_data


class Message:
    """manager of massages sent or received
    """
    def __init__(self, sock: socket, addr: tuple):
        """initialize socket, buffers for reading and writing and some flags

        Args:
            sock (socket): a socket object
            addr (tuple): (IP, PORT)
        """
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""  # buffer for reading bytes sent from clients
        self._send_buffer = b""  # buffer for writing bytes for sending to clients
        self._jsonheader_len = None  # flag that says if if have read the first two bytes of a message
        self.jsonheader = None       # flag that says if we have read all the header of a message
        
        self.response_created = True    # flag says if a response has already createda nad ready for sent
        
        self.request = None         # an object of response message
        self.false_request = False  # false request is a request that the server itself "planted"
                                    # into the receiving buffer, pretending the user did so.
        
        self.responses = []         # each entry in the list now is a tuple: (response: dict, isFalseRequest: bool)
                                    # 'isTrueRequest' is True if the response was created as a response to a real request
        
        self.toExit = False         # flag says if a client asked to exit

        self.between_read_to_write = False  # flag says if we are between the reading and writing operations (in process_events function)



    def process_events(self, mask: bytes):
        """determine which operation should be held, according to the mask

        Args:
            mask (bytes): a sequence of bytes meaning which oiperation should be held (01 - readinf, 10 - writing, 11 - both)
        """
        if mask & 0b01: # reading
            self.read()
            self.between_read_to_write = True
        
        if mask & 0b10: # writing
            self.write()
            self.between_read_to_write = False

    def read(self):
        """manage reading operation
        """
        isRead = self._read() # the actual reading operation
        
        if (isRead): # if we have read something, then a mesage awaits for interpreting
            if self._jsonheader_len is None:
                self.process_protoheader() # interpret the length of the header (first 2 bytes)

            if self._jsonheader_len is not None:
                if self.jsonheader is None: 
                    self.process_jsonheader() # interpret the header

            if self.jsonheader:
                if self.request is None:
                    self.process_request() # interpret the body of the message


    def _read(self) -> bool:
        """actual reading from the recv_buffer

        Returns:
            bool: if the recv_buffer had some bytes that we have read
        """
        try:
            # Should be ready to read
            data = decrypt(self.sock.recv(4096))
            # print("[=] Server reads <aviad>")
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
        """interpret first 2 bytes (meaning the length of the header)
        """
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack(">H", self._recv_buffer[:hdrlen])[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]


    def process_jsonheader(self):
        """interpret the bytes of the header

        Raises:
            ValueError: the header was not found
        """
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = self._json_decode(    # decode the header
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


    def _json_decode(self, json_bytes: bytes, encoding: str):
        """function for decoding bytes

        Args:
            json_bytes (bytes): the bytes to decode
            encoding (str): type of decoding (usually utf-8)

        Returns:
            var: the decoded object
        """
        bytes_decoded = json_bytes.decode(encoding=encoding)
        return json.loads(bytes_decoded)
    


    def process_request(self):
        """process the request (after all the parts of the message were interpreted)
        """
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.request = self._json_decode(data, encoding) # decode the body of the message
            

            match self.request[0]: # switch 'action'
                
                case "aMove": # the request is as follows: {"aMove": ((row, col, symbol), self.game_ID)}
                    BL.moveOnBoard(self.request[1][1], self.request[1][0], self.addr) 

                    self._jsonheader_len = None # for the next reading operation to work well, we zero these variables
                    self.jsonheader = None      
                    self.request = None         # now the writing function won't execute, there is no need in this case.

                case "veteranUser":  # 'not new' user request to sign in
                    result = BL.signInUser(self.request[1], self.addr, self.sock)
                    if (result == -1): # the token was not found in the DB
                        self.responses.append(({ "response": "0_tokenNotFound",
                                                    "value" : -1
                                                }, True))
                    elif (result == -2): # the user whose token is as given is already registered from anothe process, so refuse the connection
                        self.responses.append(({ "response": "0_AlreadyRegistered",
                                                    "value" : -1
                                                }, True))
                    else: # the reuest can be granted, the user is verified
                        self.responses.append(({ "response": "0_verified",
                                                    "value" : result
                                                }, True))
                case "newUser": # sign up request
                    result = BL.signUpUser(self.request[1], self.addr, self.sock)
                    if (result == -1): # an error was occurred
                        self.responses.append(({ "response": "1_errorHasOccured",
                                                    "value" : -1
                                                }, True))
                    else: # the request can be granted
                        self.responses.append(({ "response": "1_newUser",
                                                "value" : result               
                                                }, True))
                case "newGame": # 'new game' request
                    result = BL.registerNewGame(self.request[1], self.addr)
                    if (result == -1): # an error has occurred
                        self.responses.append(({ "response": "2_errorHasOccured",
                                                  "value" : -1
                                                }, True))
                    else: # a new game was created, pass to the usr the essential information
                        self.responses.append(({ "response": "2_newRegisteredGame",
                                                "value" : [result.game_ID, result.num_of_players]             
                                                }, True))
                case "fetchActiveGames": # fetch the open games (not games that was already over)
                    games = BL.fetchAllActiveGames()
                    gamesForSending = {}
                    for item in games.items():
                        # send to the client only the information he should has, i.e.  (1) the Game as Dict, 
                        # (2) number of active participants and (3) number of passive participants
                        gamesForSending[item[0]] = (item[1][0], len(item[1][1]), len(item[1][2]))

                    self.responses.append(({ "response": "3_allActiveGames",
                                             "value" : gamesForSending              
                                            }, True)) 
                case "logout": # logout from the system (not exitting the app)
                    BL.unregisterUser(self.addr)
                    
                    self._jsonheader_len = None # for the next reading operation to work well, we zero these variables
                    self.jsonheader = None      
                    self.request = None         # now the writing function won't execute, there is no need in this case.

                case "exit":
                    # the game is over, does not need to notify someone
                    if (self.request[1] == "a"):
                        BL.unregisterUser(self.addr)
                                 
                    # the game not yet over
                    else: # request is as follows: { "exit" : (self.game_ID, self.isSpectator) }
                        BL.exitTheGame(self.request[1][0], self.request[1][1], self.addr)
                    
                    self.responses.append(({ "response": "4_exit",
                                             "value" : "a"
                                            }, True))
                    self.toExit = True

                case "timeout":  # the time for the last move was over
                    BL.timeout(self.request[1])

                    self._jsonheader_len = None # for the next reading operation to work well, we zero these variables
                    self.jsonheader = None      
                    self.request = None
                    
                case "newJoined": # request is as follows: {"newJoined": (typeOfPlayer, game_ID)}
                    BL.joinToExistingGame(self.request[1][1], self.request[1][0], self.addr)
                    
                    # the response to that request will be handled using the falseRequest mechanism, so we don't set a normal ersponse
                    self._jsonheader_len = None # for the next reading operation to work well, we zero these variables
                    self.jsonheader      = None      
                    self.request         = None # now the writing function won't execute, there is no need in this case.
                

                case "fetchGamesHistory": # request is as follows: {"fetchGamesHistory": ""}
                    result = BL.fetchGamesHistory()
                
                    self.responses.append(({ "response": "16_gamesHistory",
                                                "value" : result
                                        }, True))
                    

                case "fetchUsersStats": # request is as follows: {"fetchUsersStats": ""}  
                    result = BL.fetchUsersStats()

                    self.responses.append(({ "response": "17_usersStats",
                                                "value" : result
                                        }, True))
                
                case "quitInMiddle": # request is as follows: {"quitInMiddle": (game_ID, self.is_spectator)}
                    BL.quitInMiddle(self.request[1][0], self.request[1][1], self.addr)
                    
                    self._jsonheader_len = None # for the next reading operation to work well, we zero these variables
                    self.jsonheader      = None      
                    self.request         = None # now the writing function won't execute, there is no need in this case.

            self.response_created = False
        else:
            # Binary or unknown content-type
            self.request = data
            print(
                f"Received {self.jsonheader['content-type']} "
                f"request from {self.addr}"
            )
        



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
    #     # self.selector.modify(self.sock, events, data=self)

    

    

    def write(self):
        """manage the writing operation
        """
        isThereFalseRequest = len(self.responses) > 0  and  self.responses[0][1] == False 
        
        # if there was a request or we have a response due to a falseRequest
        if self.request  or  isThereFalseRequest:
            if not self.response_created  or  isThereFalseRequest:
                self.create_response()

                # if we have a real request that demended a response, don't open the socket for reading
                # unless the response is already in the list of responsese, or we loss the old request due to 
                # new one.
                if (not (self.request and isThereFalseRequest)):
                    self.request = None             # in order to re-read when new messages from the client arrive
                    self.jsonheader = None
                    self._jsonheader_len = None

        self._write() # actual writing operation


    def _write(self):
        """the actual writing operation
        """
        if self._send_buffer:
            print(f"Sending {self._send_buffer!r} to {self.addr}")
            try:
                # Should be ready to write
                length = len(self._send_buffer)
                
                # if (length > 4096):
                #     data = self._send_buffer[:4096]
                # else:
                #     data = self._send_buffer
                self.sock.send(encrypt(self._send_buffer))
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[length:]
                if (self.toExit): # the user has asked to exit
                    self.close()
                


    def create_response(self):
        """create response in response to the request, if created
        """
        response = self._create_response_json_content()
        

        message = self._create_message(**response) # unpack response object and create a message
        self.response_created = True
        self._send_buffer += message # add the bytes for wsendiong to the sending buffer


########################
########################
        
    def _create_response_json_content(self):
        """create response with its properties with json content type

        Returns:
            dict: the response as dict
        """
        # return the first element in the first item in 'responses' list, which is the response itself
        content = self.responses.pop(0)[0]
        print("response: ", content)
        content_encoding = "utf-8"
        response = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        return response

########################
########################


    def _create_response_binary_content(self):
        """create response with its properties with binary content type

        Returns:
            dict: the response as dict
        """
        response = {
            "content_bytes": b"First 10 bytes of request: "
            + self.request[:10],
            "content_type": "binary/custom-server-binary-type",
            "content_encoding": "binary",
        }
        return response


    def _create_message(self, *, content_bytes: bytes, content_type: str, content_encoding: str):
        """create a message from the various parts from a response object

        Args:
            content_bytes (bytes): the bytes to create a message from
            content_type (str): the type of content (json, binary)
            content_encoding (str): type of encoding

        Returns:
            bytes: the message as bytes
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


    def _json_encode(self, obj: object, encoding: str) -> bytes:
        """encode the message for sending

        Args:
            obj (object): the object to encode
            encoding (str): type of encoding (usually utf-8)

        Returns:
            bytes: the encoded bytes
        """
        return json.dumps(obj, ensure_ascii=False).encode(encoding)




    def close(self):
        """close the socket
        """
        print(f"Closing connection to {self.addr}")
        try:
            self.sock.close()
        except OSError as e:
            print(f"Error: socket.close() exception for {self.addr}: {e!r}")
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None
