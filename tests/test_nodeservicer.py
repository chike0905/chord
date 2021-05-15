from chord.chord import *

import ipaddress
import hashlib

from tests.tools import *

def test_NodeServicer() -> None:
    NodeServicer(IP, PORT)

def test_ServeGetSuccessor(node) -> None: # type: ignore
    stub = getStub()

    response = stub.getSuccessor(peer_pb2.GetSuccessor())
 
    assert response.id == ID
    assert response.ip == IP.packed
    assert response.port == PORT

def test_ServeGetPredecessor(node) -> None: # type: ignore
    stub = getStub()

    response = stub.getPredecessor(peer_pb2.GetPredecessor())

    assert response.id == ID
    assert response.ip == IP.packed
    assert response.port == PORT

def test_ServeUpdatePredecessor(node) -> None: # type: ignore
    stub = getStub()
 
    response = stub.updatePredecessor(peer_pb2.NotifyPredecessor(ip=B_IP.packed, port=B_PORT)) 

    response = stub.getPredecessor(peer_pb2.GetPredecessor()) 
    assert response.id == B_ID
    assert response.ip == B_IP.packed
    assert response.port == B_PORT

def test_ServeUpdateFingerTable(node) -> None: # type: ignore
    stub = getStub()

    response = stub.updateFingerTable(peer_pb2.UpdateFingerTable(index=1, ip=B_IP.packed, port=B_PORT))
    assert node.servicer.node.table.fingers[1].node.id.value == B_ID
    assert node.servicer.node.table.fingers[1].node.ip.packed == B_IP.packed
    assert node.servicer.node.table.fingers[1].node.port == B_PORT
    
    response = stub.updateFingerTable(peer_pb2.UpdateFingerTable(index=0, ip=B_IP.packed, port=B_PORT))
    assert node.servicer.node.table.successor.id.value == B_ID
    assert node.servicer.node.table.successor.ip.packed == B_IP.packed
    assert node.servicer.node.table.successor.port == B_PORT

def test_ServeFindSuccessor(node) -> None: # type: ignore
    stub = getStub()
    
    key = Key("1".zfill(64))
    
    response = stub.findSuccessor(peer_pb2.FindSuccessor(key=key.value))
    assert response.id == ID
    assert response.ip == IP.packed
    assert response.port == PORT
