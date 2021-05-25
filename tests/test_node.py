from chord.chord import *

import pytest
import ipaddress
import hashlib

from tests.tools import *


def test_init_node() -> None:
    node = LocalPeer(IP, PORT)
    node.join()

    assert node.ip == IP
    assert node.port == PORT

    assert node.id.value == ID.value

    assert node.table.successor.id.value == ID.value

    for finger in node.table.fingers:
        assert finger.node.id.value == ID.value  # type: ignore


@pytest.fixture(scope="function")
def initNode() -> None:  # type: ignore
    node = LocalPeer(IP, PORT)
    node.join()

    yield node


def test_getSuccessor(initNode: LocalPeer) -> None:
    node = initNode

    successor: Peer = node.getSuccessor()

    assert successor.id.value == node.id.value


def test_getPredecessor(initNode: LocalPeer) -> None:
    node = initNode

    predecessor: Peer = node.getPredecessor()

    assert predecessor.id.value == node.id.value


def test_findSuccessor(initNode: LocalPeer) -> None:
    node = initNode
    key = Key("1".zfill(64))

    suc = node.findSuccessor(key)

    assert suc.id.value == node.id.value


def test_updatePredecessor(initNode: LocalPeer) -> None:
    node = initNode

    new_predecessor: Peer = RemotePeer(B_IP, B_PORT)
    node.updatePredecessor(new_predecessor)

    predecessor: Peer = node.getPredecessor()
    assert predecessor.id.value == new_predecessor.id.value


def test_updateFingerTable(initNode: LocalPeer) -> None:
    # Note: This test performed without update other finger
    node = initNode                              # 9c9ce...
    new_finger: Peer = RemotePeer(B_IP, B_PORT)  # e762d...

    node.updateFingerTable(new_finger, 1)

    assert node.table.fingers[1].node.id.value == new_finger.id.value  # type: ignore

    node.updateFingerTable(new_finger, 0)

    assert node.table.fingers[0].node.id.value == new_finger.id.value  # type: ignore
    assert node.table.successor.id.value == new_finger.id.value
