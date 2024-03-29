import sys
import selectors
import json
import io
import struct



import os
conf_path = os.getcwd()
level_up = conf_path[:conf_path.rfind("\\")]
sys.path.insert(1, level_up)

import BusinessLogic as BL
import BusinessEntities as BE

#from ..BusinessLogic import BusinessLogic as BL

request_search = {
    "morpheus": "Follow the white rabbit. \U0001f430",
    "ring": "In the caves beneath the Misty Mountains. \U0001f48d",
    "\U0001f436": "\U0001f43e Playing ball! \U0001f3d0",
}


class Message:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.response_created = False
        self.request_processed = False
        self.request = None
        self.response = None
        self.toExit = False



    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()


    def read(self):
        isRead = self._read()
        
        if (isRead):
            if self._jsonheader_len is None:
                self.process_protoheader()

            if self._jsonheader_len is not None:
                if self.jsonheader is None:
                    self.process_jsonheader()

            if self.jsonheader:
                if self.request is None:
                    print("so far so good")
                    self.process_request()


    def _read(self) -> bool:
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
            print("[=] Server reads <aviad>")
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


    def _json_decode(self, json_bytes, encoding):
        
        bytes_decoded = json_bytes.decode(encoding=encoding)
        return json.loads(bytes_decoded)
        
        # tiow = io.TextIOWrapper(
        #     io.BytesIO(json_bytes), encoding=encoding, newline=""
        # )
        # obj = json.load(tiow)
        # tiow.close()
        # return obj


    def process_request(self):
        print("so far so good")
        content_len = self.jsonheader["content-length"]
        print("1")
        if not len(self._recv_buffer) >= content_len:
            return
        print("2")
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            print(data)
            print(self._recv_buffer)
            self.request = self._json_decode(data, encoding)
            
            print(f"Received request {self.request!r} from {self.addr}")

            match self.request[0]: # swtich 'action'

                case "veteranUser":  # 'not new' user request to sign in
                    result = BL.signInUser(self.request[1], self.addr)
                    if (result == -1):
                        self.response = { "response": "tokenNotFound",
                                          "value" : -1
                                        }
                    else:
                        self.response = { "response": "verified",
                                          "value" : result
                                        }
                case "newUser":
                    result = BL.signUpUser(self.request[1], self.addr)
                    if (result == -1):
                        self.response = { "response": "errorHasOccured",
                                          "value" : -1
                                        }
                    else:
                        self.response = { "response": "verified",
                                          "value" : result               
                                        }
                case "exit": # exit the game
                    BL.unregisterUser(self.addr)
                    self.response = { "response": "exit",
                                          "value" : "a"
                                    }
                    self.toExit = True
            self.request_processed = True
            self.response_created = False
        else:
            # Binary or unknown content-type
            self.request = data
            print(
                f"Received {self.jsonheader['content-type']} "
                f"request from {self.addr}"
            )
        # # Set selector to listen for write events, we're done reading.
        # self._set_selector_events_mask("w")
        



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

    


    


    

    def write(self):
        if self.request:
            if not self.response_created and self.request_processed:
                self.create_response()
                self.request = None
                self.jsonheader = None
                self._jsonheader_len = None

        self._write()
    

    def _write(self):
        if self._send_buffer:
            print(f"Sending {self._send_buffer!r} to {self.addr}")
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                if (self.toExit):
                    self.close()
                
                # !$! my revision: close only when user exit! !$!

                # # Close when the buffer is drained. The response has been sent.
                # if sent and not self._send_buffer:
                #     self.close()


    def create_response(self):
        if self.jsonheader["content-type"] == "text/json":
            response = self._create_response_json_content()
        else:
            # Binary or unknown content-type
            response = self._create_response_binary_content()
        message = self._create_message(**response)
        self.response_created = True
        self.request_processed = False
        self._send_buffer += message


########################
########################
        
    def _create_response_json_content(self):
        
        # action = self.request.get("action")
        # if action == "search":
        #     query = self.request.get("value")
        #     answer = request_search.get(query) or f"No match for '{query}'."
        #     content = {"result": answer}
        # else:
        #     content = {"result": f"Error: invalid action '{action}'."}

        content = self.response
        
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
        response = {
            "content_bytes": b"First 10 bytes of request: "
            + self.request[:10],
            "content_type": "binary/custom-server-binary-type",
            "content_encoding": "binary",
        }
        return response


    def _create_message(
        self, *, content_bytes, content_type, content_encoding
    ):
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


    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)


    

    

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
