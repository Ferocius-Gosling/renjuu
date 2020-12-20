import socket
import threading
import time
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
                data = pickle.loads(pickle.loads(data))
                data[RequestParams.ID] = Color(len(self.clients))
                self.clients_params.append(data)
                threading.Thread(target=self.request_handler,
                                 args=(client,)).start()
                # обработчик запросов для каждого нового клиента
                response_data = {RequestParams.TYPE: RequestType.CURRENT_PLAYERS,
                                 RequestParams.PLAYERS: self.clients_params,
                                 RequestParams.MAX_PLAYERS: self.max_clients,
                                 RequestParams.ID: data[RequestParams.ID]}
                for client_socket in self.clients:
                    client_socket.send(pickle.dumps(response_data))
            time.sleep(1)

    def request_handler(self, client_socket: socket.socket):
        while True:
            request = client_socket.recv(1024)
            request = pickle.loads(request)
            if request[RequestParams.TYPE] == RequestType.EXIT:
                self.clients.remove(client_socket)
                self.clients_params.remove(
                    {RequestParams.NAME: request[RequestParams.NAME],
                     RequestParams.ID: request[RequestParams.ID]})
                break

            for client in self.clients:
                if client != client_socket:
                    client.send(request)
            time.sleep(1)
