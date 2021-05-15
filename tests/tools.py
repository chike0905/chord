from chord.chord import *

import pytest
import ipaddress

# Node A 
IP: ipaddress.IPv4Address = ipaddress.IPv4Address("127.0.0.1")
PORT: int = 3341
ID: str = hashlib.sha256(IP.packed + bytes(PORT)).hexdigest() # 9c9ce7cea14809cf88796f1706533f5e360f23d7207ab4452f9af433f7c6e1d8


# Node B
B_IP: ipaddress.IPv4Address = ipaddress.IPv4Address("127.0.0.1")
B_PORT: int = 3342
B_ID: str = hashlib.sha256(B_IP.packed + bytes(B_PORT)).hexdigest() # e762d1fe20e89c6143cf49f7e0bd8a69df840fa9864971b195f2ccc2400b086a

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

    yield server

    server.stop()
    thread.join()
