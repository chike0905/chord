from chord.chord import *

import pytest
import ipaddress
import hashlib

from tests.tools import *

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
    node = LocalPeer(IP, PORT)
    assert node.ip == IP
    assert node.port == PORT

    nodeid = hashlib.sha256(IP.packed).hexdigest()
    assert nodeid == node.id.value

    assert nodeid == node.table.successor.id.value

    for finger in node.table.fingers:
        assert nodeid == finger.node.id.value # type: ignore

def test_getSuccessor() -> None:
    node = LocalPeer(IP, PORT)
    successor: Peer = node.getSuccessor()
    assert successor.id.value == node.id.value

def test_getPredecessor() -> None:
    node = LocalPeer(IP, PORT)
    predecessor: Peer = node.getPredecessor()
    assert predecessor.id.value == node.id.value

def test_findSuccessor() -> None:
    node = LocalPeer(IP, PORT)
    key = Key("1".zfill(64))
    suc = node.findSuccessor(key)
    assert suc.id.value == node.id.value

def test_updatePredecessor() -> None:
    node: Peer = LocalPeer(IP, PORT)

    new_predecessor: Peer = RemotePeer(B_IP, B_PORT)
    node.updatePredecessor(new_predecessor)
    
    predecessor: Peer = node.getPredecessor()
    assert predecessor.id.value == new_predecessor.id.value
