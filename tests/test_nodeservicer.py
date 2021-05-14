from chord.chord import *

import ipaddress
import hashlib

from tests.tools import *

def test_NodeServicer() -> None:
    NodeServicer(IP, PORT)

def test_ServeGetSuccessor(node) -> None: # type: ignore
    stub = getStub()

    response = stub.getSuccessor(peer_pb2.GetSuccessor())
 
    assert response.id == hashlib.sha256(IP.packed).hexdigest()
    assert response.ip == IP.packed
    assert response.port == PORT

def test_ServeGetPredecessor(node) -> None: # type: ignore
    stub = getStub()

    response = stub.getPredecessor(peer_pb2.GetPredecessor())

    assert response.id == hashlib.sha256(IP.packed).hexdigest()
    assert response.ip == IP.packed
    assert response.port == PORT

def test_ServeUpdatePredecessor(node) -> None: # type: ignore
    stub = getStub()
 
    peer = RemotePeer(IP, PORT)
    response = stub.updatePredecessor(peer_pb2.NotifyPredecessor(ip=B_IP.packed, port=B_PORT)) 

    response = stub.getPredecessor(peer_pb2.GetPredecessor()) 
    assert response.id == hashlib.sha256(B_IP.packed).hexdigest()
    assert response.ip == B_IP.packed
    assert response.port == B_PORT

def test_ServeFindSuccessor(node) -> None: # type: ignore
    stub = getStub()
    
    key = Key("1".zfill(64))
    
    response = stub.findSuccessor(peer_pb2.FindSuccessor(key=key.value))
    assert response.id == hashlib.sha256(IP.packed).hexdigest()
    assert response.ip == IP.packed
    assert response.port == PORT
