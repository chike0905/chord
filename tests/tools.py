from chord.chord import *
from chord.grpcprotos import peer_pb2
from chord.grpcprotos import peer_pb2_grpc

import pytest
import ipaddress
import threading

from typing import Tuple, Optional

# Node A
# 9c9ce7cea14809cf88796f1706533f5e360f23d7207ab4452f9af433f7c6e1d8
IP: ipaddress.IPv4Address = ipaddress.IPv4Address("127.0.0.1")
PORT: int = 3341
ID: Key = Key(hashlib.sha256(IP.packed + bytes(PORT)).hexdigest())

# Node B
# e762d1fe20e89c6143cf49f7e0bd8a69df840fa9864971b195f2ccc2400b086a
B_IP: ipaddress.IPv4Address = ipaddress.IPv4Address("127.0.0.1")
B_PORT: int = 3342
B_ID: Key = Key(hashlib.sha256(B_IP.packed + bytes(B_PORT)).hexdigest())

# Node C
# bd565d1ec650fdb629ed893ccce97757f8c916b3b99f7f0290940a5ae0870146
C_IP: ipaddress.IPv4Address = ipaddress.IPv4Address("127.0.0.1")
C_PORT: int = 3343
C_ID: Key = Key(hashlib.sha256(C_IP.packed + bytes(C_PORT)).hexdigest())


def getStub() -> peer_pb2_grpc.PeerStub:
    channel = grpc.insecure_channel(IP.compressed + ":" + str(PORT))
    return peer_pb2_grpc.PeerStub(channel)  # type: ignore


def setupNodeThread(
        ip: ipaddress.IPv4Address,
        port: int,
        peer_ip: Optional[ipaddress.IPv4Address] = None,
        peer_port: Optional[int] = None) -> Tuple[threading.Thread, NodeServer]:
    server = NodeServer(ip, port, peer_ip, peer_port)
    thread = threading.Thread(None, server.serve)

    return thread, server


@pytest.fixture(scope="function")
def nodeA():  # type: ignore
    thread, server = setupNodeThread(IP, PORT)
    thread.start()

    yield server.servicer.node

    server.stop()
    thread.join()


@pytest.fixture(scope="function")
def nodeB():  # type: ignore
    thread, server = setupNodeThread(B_IP, B_PORT)
    thread.start()

    yield server.servicer.node

    server.stop()
    thread.join()


@pytest.fixture(scope="function")
def nodeC():  # type: ignore
    thread, server = setupNodeThread(C_IP, C_PORT)
    thread.start()

    yield server.servicer.node

    server.stop()
    thread.join()
