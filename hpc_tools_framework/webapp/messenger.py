import json
import logging
from typing import Dict, Tuple


class Messenger:
    def __init__(self, socket):
        self.socket = socket

    def send(self, msg, data=None) -> None:
        if not data:
            data = dict()
        body = json.dumps({"message": msg, "data": data})
        logging.debug("Send:", body)
        self.socket.send_string(body)

    def receive(self) -> Tuple[str, Dict]:
        str_body = self.socket.recv_string()
        body = json.loads(str_body)
        logging.debug("Received:", body)
        return (body["message"], body.get("data", None))