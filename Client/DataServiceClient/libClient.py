import sys
import selectors
import json
import io
import struct
import socket as sckt
import os

conf_path = os.getcwd()
sys.path.append(conf_path)
level_up = conf_path[:conf_path.rfind("\\")]
sys.path.append(level_up)

# import Presentation2 as ui


gui = None


class Message:
    def __init__(self, selector, sock : sckt.socket, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.request = None
        self._recv_buffer = b""
        self._send_buffer = b""
        self._request_queued = True
        self._jsonheader_len = None
        self.jsonheader = None
        self.response = None

        self.last_event = "read"


    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            print("bitwise: ", mask & selectors.EVENT_READ)
            print(mask)
            print(selectors.EVENT_READ)
            self.read()
            self.last_event = "read"
            print("read")
        if mask & selectors.EVENT_WRITE:
            self.write()
            



    def read(self):
        print("trying to read...")
        isRead = self._read()
        if (isRead):
            if self._jsonheader_len is None:
                self.process_protoheader()

            if self._jsonheader_len is not None:
                if self.jsonheader is None:
                    self.process_jsonheader()

            if self.jsonheader:
                print("and condition")
                if self.response is None  or  self.last_event == "read":
                    self.process_response()


    


    def _read(self) -> bool:
        """try to read from the receiving buffer

        Returns:
            bool: is new data was read
        """
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
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
        print("process_read")
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.response = self._json_decode(data, encoding)
            print(f"Received response {self.response!r} from {self.addr}")
            self._process_response_json_content()
        else:
            # Binary or unknown content-type
            self.response = data
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
        
        match self.response["response"]:
            case "9_afterOneMove":
                currentPage = gui.currentPageInstance
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.restartTimer()
                    currentPage.updateBoardAndButton(self.response["value"][0][0], self.response["value"][0][1], self.response["value"][0][2])
                    currentPage.game_turn_label.config(text="other's turn", bg="#0066cc", fg="#ffffff")
                    currentPage.message_buffer.append("## The next to play is: " + self.response["value"][1])

            case "10_YourMoveArrived":
                currentPage = gui.currentPageInstance
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.restartTimer()
                    currentPage.updateBoardAndButton(self.response["value"][0], self.response["value"][1], self.response["value"][2])
                    currentPage.game_turn_label.config(text=" your turn! ", bg="#00cc00", fg="#ffffff")
                    currentPage.message_buffer.append("## it's your turn to play!")
                    currentPage.yourTurn = True
            
            case "11_victory":
                currentPage = gui.currentPageInstance
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.updateBoardAndButton(self.response["value"][0][0], self.response["value"][0][1], self.response["value"][0][2])
                    currentPage.isStarted = False
                    currentPage.game_result = "over"
                    currentPage.game_turn_label.config(text=" game  over ", bg="#ff0000", fg="#ffffff")
                    currentPage.message_buffer.append("## " + self.response["value"][1] + " has won the game, well done!")

            case "12_youWon":
                currentPage = gui.currentPageInstance
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.isStarted = False
                    currentPage.game_result = "over"
                    currentPage.game_turn_label.config(text="  you won!  ", bg="#00cc00", fg="#ffffff")
                    currentPage.message_buffer.append("## you are the winner, congratulations!!!")

            case "13_draw":
                currentPage = gui.currentPageInstance
                if currentPage.__class__.__name__ == "GamePage":
                    currentPage.updateBoardAndButton(self.response["value"][0], self.response["value"][1], self.response["value"][2])
                    currentPage.isStarted = False
                    currentPage.game_result = "over"
                    currentPage.game_turn_label.config(text="    draw    ", bg="#ff8000", fg="#ffffff")
                    currentPage.message_buffer.append("## it's a draw, the game is over.")

            case "4_exit":
                self.close()

            case "5_newPlayer": # we get the following response due to false request: { "5_newPlayer" : <number of remaining num of players to join>}
                if gui.currentPageInstance.__class__.__name__ == "GamePage":
                    strForDisplay = "## waiting for " + str(self.response["value"]) + " more players to join and then we start!"
                    gui.currentPageInstance.message_buffer.append(strForDisplay)
            
            case "14_newSpectator":  # we get the following response: { "14_newSpectator" : num_of_players-num_of_active_players }
                if gui.currentPageInstance.__class__.__name__ == "GamePage":
                    if (self.response["value"] == 0): # the game has already started
                        gui.currentPageInstance.message_buffer.append("## The game has already started, have a seat and enjoy watching!")
                    else: # num_of_players-num_of_active_players > 0, which means that the game has not yet started
                        strForDisplay = "## waiting for " + str(self.response["value"]) + " more players to join and then we start!"
                        gui.currentPageInstance.message_buffer.append(strForDisplay)

            case "6_beforeStart":
                if gui.currentPageInstance.__class__.__name__ == "GamePage":
                    strForDisplay = "## The game is about to begin, your turn is " + str(self.response["value"][0]) + " and your symbol is " + gui.currentPageInstance.assignSymbol(self.response["value"][1])
                    gui.currentPageInstance.message_buffer.append(strForDisplay)
                    gui.currentPageInstance.assignSymbol(self.response["value"][1])
            
            case "7_start":
                if gui.currentPageInstance.__class__.__name__ == "GamePage":
                    print("7_start")
                    gamePage = gui.currentPageInstance
                    gamePage.game_turn_label.config(text="started", bg="#00cc00", fg="#ffffff")
                    gamePage.game_result = "started"
                    gamePage.message_buffer.append("## Last player has joined, let the tournament begin!")
                    gamePage.message_buffer.append("## First to play is " + self.response["value"] + ". And remember: 30 seconds for a move, no excuse accepted!")
                    gamePage.restartTimer()
                    gamePage.isStarted = True

            case "8_yourMove":
                print("8_yourMove")
                if gui.currentPageInstance.__class__.__name__ == "GamePage":
                    gui.currentPageInstance.message_buffer.append("## it's your turn to play, the clock is ticking!")
                    gui.currentPageInstance.game_turn_label.config(text="your turn", bg="#00cc00", fg="#ffffff")
                    gui.currentPageInstance.yourTurn = True

        # result = content.get("result")
        # print(f"Got result: {result}")
        
        # ui.frames[ui.AuthPageToken].setTokenEntry("Mom")


########################
########################
        
    def _process_response_binary_content(self):
        content = self.response
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
        self.request = {
            "action" : action,
            "value" : value,
            "type" : "text/json",
            "encoding" : "utf-8"
        }
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

            self.response = None
            self.jsonheader = None
            self._jsonheader_len = None
            self.last_event = "write"

            print(f"Sending {self._send_buffer!r} to {self.addr}")
            try:
                
                # self.sock.connect_ex(self.addr)
                
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            # except Exception:
            #     print("error")
            else:
                self._send_buffer = self._send_buffer[sent:]


    def queue_request(self):
        action = self.request["action"]
        #content = "hello everyone!"
        
        value = self.request["value"]
        
        content_type = self.request["type"]
        #content_type = "text/json"

        content_encoding = self.request["encoding"]
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
        self._request_queued = True


    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {mode!r}.")
        self.selector.modify(self.sock, events, data=self)

    
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

    



    def close(self):
        print(f"Closing connection to {self.addr}")
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(
                f"Error: selector.unregister() exception for "
                f"{self.addr}: {e!r}"
            )

        try:
            self.sock.close()
        except OSError as e:
            print(f"Error: socket.close() exception for {self.addr}: {e!r}")
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None


    def updateAccessToGUI(self, presentation_instance):
        global gui
        gui = presentation_instance