import logging
from flask import Flask
from hpc_tools_framework.webapp.messenger import Messenger
import zmq
import hpc_tools_framework.webapp.routes as routes

# logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


if __name__ == "__main__":
    # app
    app = Flask(__name__)
    app.secret_key = "hpc_framework_tool"

    # socket
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")

    routes.init_app(app, Messenger(socket))
    app.run(debug=True)