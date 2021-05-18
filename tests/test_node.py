from chord.chord import *

import pytest
import ipaddress
import hashlib

from tests.tools import *


def test_key() -> None:
    key1 = \
        Key("5b9b2b3122bdac7e303b15bfc5895c10204de107f16bd16104f24184583c13ed")
    with pytest.raises(Exception):
        badkey = Key("d")


def test_add_key() -> None:
    key1 = Key("1".zfill(64))   # 0000...0001
    key2 = Key("f".zfill(64))   # 0000...000f
    res = Key("10".zfill(64))   # 0000...0010

    added_key = addKey(key1, key2)
    assert added_key.value == res.value

    # Overflow
    key1 = Key("1".ljust(64, "0"))  # 1000...0000
    key2 = Key("f".ljust(64, "0"))  # f000...0000
    res = Key("0".zfill(64))        # 0000...0000

    added_key = addKey(key1, key2)
    assert added_key.value == res.value

    key1 = Key("1".zfill(64))      # 0000...0001
    key2 = Key("".ljust(64, "f"))  # ffff...ffff
    res = Key("0".zfill(64))       # 0000...0000

    added_key = addKey(key1, key2)
    assert added_key.value == res.value


def test_subKey() -> None:
    key1 = Key("10".zfill(64))  # 0000...0010
    key2 = Key("1".zfill(64))   # 0000...0001
    res = Key("f".zfill(64))    # 0000...000f

    subed_key = subKey(key1, key2)
    assert subed_key.value == res.value

    # Overflow
    key1 = Key("0".zfill(64))       # 0000...0000
    key2 = Key("1".ljust(64, "0"))  # 1000...0000
    res = Key("f".ljust(64, "0"))   # f000...0000

    subed_key = subKey(key1, key2)
    assert subed_key.value == res.value

    key1 = Key("0".zfill(64))       # 0000...0000
    key2 = Key("1".zfill(64))       # 0000...0001
    res = Key("".ljust(64, "f"))    # ffff...ffff

    subed_key = subKey(key1, key2)
    assert subed_key.value == res.value


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
    node = LocalPeer(IP, PORT)
    node.join()

    assert node.ip == IP
    assert node.port == PORT

    assert node.id.value == ID

    assert node.table.successor.id.value == ID

    for finger in node.table.fingers:
        assert finger.node.id.value == ID  # type: ignore


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
