import socket
import threading
import pickle

from renjuu.game.vector import Vector
from renjuu.network.const import RequestParams, RequestType


class RequestMonitor(threading.Thread):
    def __init__(self, server_socket: socket.socket):
        super().__init__()
        self.server_socket = server_socket
        self.player_params = None
        self.max_players = None
        self.game = None
        self.start_button = None
        self.restart_button = None
        self.request = None
        self.id = None

    def run(self):
        while True:
            self.request = pickle.loads(self.server_socket.recv(1024))
            if self.request[RequestParams.TYPE] == RequestType.CURRENT_PLAYERS:
                self.player_params = self.request[RequestParams.PLAYERS]
                player_id = self.request[RequestParams.ID].value - 1
                player = self.request[RequestParams.PLAYERS][player_id]
                self.id = player[RequestParams.ID].value
                print(self.id, 'player id')
                self.max_players = self.request[RequestParams.MAX_PLAYERS]
                print(self.max_players)
            elif self.request[RequestParams.TYPE] == RequestType.BEGIN:
                self.start_button.is_pressed = self.id == 1
            elif self.request[RequestParams.TYPE] == RequestType.MOVE:
                place = self.request[RequestParams.MOVE]
                self.game.make_turn(Vector([place[0], place[1]]))
            elif self.request[RequestParams.TYPE] == RequestType.RESTART:
                self.restart_button.is_pressed = self.id == 1
            elif self.request[RequestParams.TYPE] == RequestType.WINNING:
                self.game.winner = self.request[RequestParams.ID]


class GameClient:
    def __init__(self, server_ip: str, port: int):
        self.client_socket = None
        self.message_monitor = None
        self.server_ip = server_ip
        self.port = port

    def connect_server(self, name: str):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.port))
        data_to_send = {RequestParams.NAME: name}
        print(data_to_send)
        data_to_send = pickle.dumps(data_to_send)
        print(data_to_send, 'from client')
        self.send_message(data_to_send)
        self.message_monitor = RequestMonitor(self.client_socket)
        self.message_monitor.start()

    def send_message(self, message):
        request_type = message[RequestParams.TYPE]
        if request_type == RequestType.EXIT:
            self.close_event()
        else:
            self.client_socket.send(pickle.dumps(message))
            print(message, 'from client in send')

    def close_event(self):
        request_exit = {RequestParams.TYPE: RequestType.EXIT}
        self.client_socket.send(pickle.dumps(request_exit))
        self.client_socket.close()
