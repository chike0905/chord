from chord.chord import *

import ipaddress
import hashlib

from tests.tools import *


def test_NodeServicer() -> None:
    NodeServicer(IP, PORT)


def test_ServeGetSuccessor(nodeA: LocalPeer) -> None:
    stub = getStub()

    response = stub.getSuccessor(peer_pb2.GetSuccessor())

    assert response.id == ID.value
    assert response.ip == IP.packed
    assert response.port == PORT


def test_ServeGetPredecessor(nodeA: LocalPeer) -> None:
    stub = getStub()

    response = stub.getPredecessor(peer_pb2.GetPredecessor())

    assert response.id == ID.value
    assert response.ip == IP.packed
    assert response.port == PORT


def test_ServeUpdatePredecessor(nodeA: LocalPeer) -> None:
    stub = getStub()

    msg = peer_pb2.NotifyPredecessor(ip=B_IP.packed, port=B_PORT)
    response = stub.updatePredecessor(msg)

    response = stub.getPredecessor(peer_pb2.GetPredecessor())
    assert response.id == B_ID.value
    assert response.ip == B_IP.packed
    assert response.port == B_PORT


def test_ServeUpdateFingerTable(nodeA: LocalPeer) -> None:
    stub = getStub()

    msg = peer_pb2.UpdateFingerTable(index=1, ip=B_IP.packed, port=B_PORT)
    response = stub.updateFingerTable(msg)
    firstfinger = nodeA.table.fingers[1]
    assert firstfinger.node.id.value == B_ID.value      # type: ignore
    assert firstfinger.node.ip.packed == B_IP.packed    # type: ignore
    assert firstfinger.node.port == B_PORT              # type: ignore

    msg = peer_pb2.UpdateFingerTable(index=0, ip=B_IP.packed, port=B_PORT)
    response = stub.updateFingerTable(msg)
    assert nodeA.table.successor.id.value == B_ID.value
    assert nodeA.table.successor.ip.packed == B_IP.packed
    assert nodeA.table.successor.port == B_PORT


def test_ServeFindSuccessor(nodeA: LocalPeer) -> None:
    stub = getStub()

    key = Key("1".zfill(64))

    response = stub.findSuccessor(peer_pb2.FindSuccessor(key=key.value))
    assert response.id == ID.value
    assert response.ip == IP.packed
    assert response.port == PORT


def test_ServeClosestPrecedingFinger(nodeA: LocalPeer) -> None:
    # Note:
    # This test is on single node cluster.
    # Hence, ClosestProcerdingFinger returns the served node iteself.
    stub = getStub()

    key = Key("1".zfill(64))
    response = stub.closestPrecedingFinger(peer_pb2.ClosestPrecedingFinger(key=key.value))
    assert response.id == ID.value
    assert response.ip == IP.packed
    assert response.port == PORT
