import time

from renjuu.network.const import RequestType, RequestParams
from renjuu.network.server import GameServer
from renjuu.network.client import GameClient


def test_send_message():
    server = GameServer('127.0.0.1', 5555, 2)
    client1 = GameClient('127.0.0.1', 5555)
    client2 = GameClient('127.0.0.1', 5555)
    client1.connect_server('test1')
    client2.connect_server('test2')
    time.sleep(1)
    client1.send_message({RequestParams.TYPE: RequestType.CONNECTING})
    time.sleep(1)
    assert client2.message_monitor.request[RequestParams.TYPE] \
        == RequestType.CONNECTING
    assert len(server.clients) == 2
    time.sleep(1)
    client1.close_event()
    time.sleep(1)
    client2.close_event()
    time.sleep(1)
    server.close()
