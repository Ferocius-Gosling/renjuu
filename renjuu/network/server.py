import socket
import threading
import pickle

from renjuu.game.const import Color
from renjuu.network.const import RequestType, RequestParams


class GameServer:
    def __init__(self, _ip: str, _port: int, max_clients: int):
        self._ip = _ip
        self._port = _port
        self.max_clients = max_clients
        self.clients = []
        self.clients_params = []

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((_ip, _port))
        self.server_socket.listen(max_clients)
        threading.Thread(target=self.connect_handler).start()
        # обработчик соединений

    def connect_handler(self):
        while True:
            client, address = self.server_socket.accept()
            if client not in self.clients:
                self.clients.append(client)
                data = client.recv(1024)
                data = pickle.loads(data)
                data[RequestParams.ID] = Color(len(self.clients))
                self.clients_params.append(data)
                threading.Thread(target=self.request_handler,
                                 args=(client,)).start()
                # обработчик запросов для каждого нового клиента
                response_data = {RequestParams.TYPE:
                                 RequestType.CURRENT_PLAYERS,
                                 RequestParams.PLAYERS: self.clients_params,
                                 RequestParams.MAX_PLAYERS: self.max_clients,
                                 RequestParams.ID: data[RequestParams.ID]}
                for client_socket in self.clients:
                    client_socket.send(pickle.dumps(response_data))

    def request_handler(self, client_socket: socket.socket):
        while True:
            request = pickle.loads(client_socket.recv(1024))
            if request[RequestParams.TYPE] == RequestType.EXIT:
                self.clients.remove(client_socket)
                break
            if request[RequestParams.TYPE] == RequestType.BEGIN or \
                    request[RequestParams.TYPE] == RequestType.RESTART:
                if request[RequestParams.ID] != 1:
                    continue
                client_socket.send(pickle.dumps(request))
            for client in self.clients:
                if client != client_socket:
                    client.send(pickle.dumps(request))

    def close(self):
        self.server_socket.close()
