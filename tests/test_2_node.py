from chord.chord import *

import ipaddress
import hashlib

from tests.tools import *
    
def test_getSuccessorOnRemotePeer(node) -> None: # type: ignore
    nodeid = hashlib.sha256(IP.packed).hexdigest()
    peer = RemotePeer(IP, PORT)
    
    suc = peer.getSuccessor() # Note: There is a single node in a Chord ring. It returns RemotePeer itself.
    assert suc.id.value == nodeid

def test_getPredecessorOnRemotePeer(node) -> None: # type: ignore
    nodeid = hashlib.sha256(IP.packed).hexdigest()
    peer = RemotePeer(IP, PORT)
    
    suc = peer.getPredecessor() # Note: There is a single node in a Chord ring. It returns RemotePeer itself.
    assert suc.id.value == nodeid

def test_updatePredecessorOnRemotePeer(node) -> None: # type: ignore
    peer = RemotePeer(IP, PORT)
    localnode = LocalPeer(B_IP, B_PORT)

    peer.updatePredecessor(localnode)

    assert peer.getPredecessor().id.value == localnode.id.value

def test_findSuccessorOnRemotePeer(node): # type: ignore
    nodeid = hashlib.sha256(IP.packed).hexdigest()
    peer = RemotePeer(IP, PORT)
    key = Key("1".zfill(64))
    suc = peer.findSuccessor(key) # Note: There is a single node in a Chord ring. It returns RemotePeer itself.
    assert suc.id.value == nodeid


def test_initFingerWithInitialPeer(node) -> None: # type: ignore
    nodeid = hashlib.sha256(IP.packed).hexdigest()
    initial_peer = RemotePeer(IP, PORT)
    localnode = LocalPeer(B_IP, B_PORT, initial_peer)
    
    assert localnode.table.successor.id.value == nodeid 
    suc_predecessor = localnode.table.successor.getPredecessor()
    assert suc_predecessor.id.value == localnode.id.value
