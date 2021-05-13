from chord.chord import *

import pytest
import ipaddress
import hashlib

# Node A
# id: 5b9b2b3122bdac7e303b15bfc5895c10204de107f16bd16104f24184583c13ed
IP = ipaddress.IPv4Address("127.0.0.1")
PORT = 3343

# Node B
# id: 1158ec9de62eb3c22228738cdfc05e90a98a9018de91b229f9ab5cb9e690af51
B_IP = ipaddress.IPv4Address("192.168.56.2")
B_PORT = 3343



def test_key() -> None:
    key1 = Key("5b9b2b3122bdac7e303b15bfc5895c10204de107f16bd16104f24184583c13ed")
    with pytest.raises(Exception):
        badkey = Key("d")

def test_add_key() -> None:
    key1 = Key("1".zfill(64))
    key2 = Key("f".zfill(64))
    res = Key("10".zfill(64))

    added_key = addKey(key1, key2)
    assert added_key.value == res.value
    
    # Overflow
    key1 = Key("1".ljust(64, "0"))
    key2 = Key("f".ljust(64, "0"))
    res = Key("0".zfill(64))
    
    added_key = addKey(key1, key2)
    assert added_key.value == res.value
    
    key1 = Key("1".zfill(64))
    key2 = Key("".ljust(64, "f"))
    res = Key("0".zfill(64))
    
    added_key = addKey(key1, key2)
    assert added_key.value == res.value

def test_isBetween() -> None:
    key1 = Key("1".ljust(64, "0"))  # 1000...0000
    key2 = Key("f".ljust(64, "0"))  # f000...0000
    
    key = Key("2".ljust(64, "0"))   # 2000...0000
    assert isBetween(key1, key2, key)
    assert not isBetween(key2, key1, key)
    
    key = Key("1".zfill(64))  # 0000...0001
    assert not isBetween(key1, key2, key)
    assert isBetween(key2, key1, key)

    

def test_init_node() -> None:
    node = Node(IP, PORT)
    assert node.ip == IP
    assert node.port == PORT

    nodeid = hashlib.sha256(IP.packed).hexdigest()
    assert nodeid == node.id.value

    assert nodeid == node.table.successor.id.value

    for finger in node.table.fingers:
        assert nodeid == finger.node.id.value

def test_findSuccessor() -> None:
    node = Node(IP, PORT)# id: 5b9b2b3122bdac7e303b15bfc5895c10204de107f16bd16104f24184583c13ed
    key = Key("1".zfill(64))
    suc = node.findSuccessor(key)
    assert suc.id.value == node.id.value

def test_NodeServicer() -> None:
    NodeServicer(IP, PORT)

import threading
@pytest.fixture(scope="function")
def node():
    server = NodeServer(IP, PORT)
    thread = threading.Thread(None, server.serve)
    thread.start()

    yield

    server.stop()
    thread.join()
    
from chord.grpcprotos import peer_pb2
from chord.grpcprotos import peer_pb2_grpc  
def test_ServeGetSuccessor(node) -> None:
    channel = grpc.insecure_channel("[::]:" + str(PORT))
    stub = peer_pb2_grpc.PeerStub(channel)

    node_id = "hoge"

    response = stub.getSuccessor(peer_pb2.GetSuccessor(id=node_id))
    assert response.suc_id == hashlib.sha256(IP.packed).hexdigest()
    assert response.suc_ip == IP.packed
    assert response.suc_port == PORT

def test_ServeFindSuccessor(node) -> None:
    channel = grpc.insecure_channel("[::]:" + str(PORT))
    stub = peer_pb2_grpc.PeerStub(channel)
    key = Key("1".zfill(64))
    
    response = stub.findSuccessor(peer_pb2.FindSuccessor(key=key.value))
    assert response.suc_id == hashlib.sha256(IP.packed).hexdigest()
    assert response.suc_ip == IP.packed
    assert response.suc_port == PORT

def test_findSuccessorOnRemotePeer(node):
    nodeid = hashlib.sha256(IP.packed).hexdigest()
    peer = RemotePeer(IP, PORT, Key(nodeid))
    key = Key("1".zfill(64))
    suc = peer.findSuccessor(key) # Note: There is a single node in a Chord ring. It returns RemotePeer itself.
    assert suc.id.value == nodeid


def test_initFingerWithInitialPeer(node) -> None:
    nodeid = hashlib.sha256(IP.packed).hexdigest()
    initial_peer = RemotePeer(IP, PORT, Key(nodeid))
    node = Node(B_IP, B_PORT, initial_peer)
    
    assert node.table.successor.id == nodeid 

