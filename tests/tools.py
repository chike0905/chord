from chord.chord import *

import pytest
import ipaddress

# Node A
# id: 5b9b2b3122bdac7e303b15bfc5895c10204de107f16bd16104f24184583c13ed
IP: ipaddress.IPv4Address = ipaddress.IPv4Address("127.0.0.1")
PORT: int = 3343

# Node B
# id: 1158ec9de62eb3c22228738cdfc05e90a98a9018de91b229f9ab5cb9e690af51
B_IP: ipaddress.IPv4Address = ipaddress.IPv4Address("192.168.56.2")
B_PORT = 3343

from chord.grpcprotos import peer_pb2
from chord.grpcprotos import peer_pb2_grpc

def getStub() -> peer_pb2_grpc.PeerStub:
    channel = grpc.insecure_channel(IP.compressed + ":" + str(PORT))
    return peer_pb2_grpc.PeerStub(channel)  # type: ignore

import threading
@pytest.fixture(scope="function")
def node(): # type: ignore
    server = NodeServer(IP, PORT)
    thread = threading.Thread(None, server.serve)
    thread.start()

    yield

    server.stop()
    thread.join()
