from chord.chord import *

import ipaddress
import hashlib

from tests.tools import *
    
def test_getSuccessorOnRemotePeer(node) -> None: # type: ignore
    peer = RemotePeer(IP, PORT)
    
    suc = peer.getSuccessor() # Note: There is a single node in a Chord ring. It returns RemotePeer itself.
    assert suc.id.value == ID

def test_getPredecessorOnRemotePeer(node) -> None: # type: ignore
    nodeid = hashlib.sha256(IP.packed).hexdigest()
    peer = RemotePeer(IP, PORT)
    
    suc = peer.getPredecessor() # Note: There is a single node in a Chord ring. It returns RemotePeer itself.
    assert suc.id.value == ID

def test_updatePredecessorOnRemotePeer(node) -> None: # type: ignore
    peer = RemotePeer(IP, PORT)
    localnode = LocalPeer(B_IP, B_PORT)

    peer.updatePredecessor(localnode)

    assert peer.getPredecessor().id.value == localnode.id.value

def test_findSuccessorOnRemotePeer(node): # type: ignore
    peer = RemotePeer(IP, PORT)
    key = Key("1".zfill(64))
    suc = peer.findSuccessor(key) # Note: There is a single node in a Chord ring. It returns RemotePeer itself.
    assert suc.id.value == ID


def test_initFingerWithInitialPeer(node) -> None: # type: ignore
    initial_peer = RemotePeer(IP, PORT) # 9c9ce...
    localnode = LocalPeer(B_IP, B_PORT, initial_peer) # e762d... 
    # Note: The last finger would be localnode itself with following test configration
    #localnode = LocalPeer(B_IP, 3346, initial_peer) # 1df7...
    
    assert localnode.table.successor.id.value == ID
    suc_predecessor = localnode.table.successor.getPredecessor()
    assert suc_predecessor.id.value == localnode.id.value

    # TODO: Finger Check
    for i in range(KEYLENGTH):
        if isBetween(localnode.id, initial_peer.id, localnode.table.fingers[i].start):
            assert localnode.table.fingers[i].node.id.value == initial_peer.id.value
        else:
            assert localnode.table.fingers[i].node.id.value == localnode.id.value

def test_findSuccessorWithInitialPeer(node) -> None: # type: ignore
    initial_peer = RemotePeer(IP, PORT) # 9c9ce...
    localnode = LocalPeer(B_IP, B_PORT, initial_peer) # e762d...
   
    key = Key("1".ljust(64, "0")) # 1000...0000
    suc = localnode.findSuccessor(key)

    assert suc.id.value == initial_peer.id.value 

    key = Key("a".ljust(64, "0")) # a000...0000
    suc = localnode.findSuccessor(key)
    
    assert suc.id.value == localnode.id.value
