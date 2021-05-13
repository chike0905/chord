import hashlib
import ipaddress

from abc import ABCMeta
from abc import abstractmethod

import grpc
from chord.grpcprotos import peer_pb2
from chord.grpcprotos import peer_pb2_grpc  

from chord.key import *

from typing import List, Union, Optional


KEYLENGTH = 256  # Note: we use sha256 hash as a key



class Peer(metaclass = ABCMeta):
    ip: ipaddress.IPv4Address
    port: int
    id: Key

    def __init__(self, ip: ipaddress.IPv4Address, port: int, id: Key) -> None:
        self.ip = ip
        self.port = port
        self.id = id

    @abstractmethod
    def getSuccessor(self):  # type: ignore
        pass


class RemotePeer(Peer):
    def getSuccessor(self): # type: ignore #RemotePeer
        print("not implemented")
        return self

class LocalPeer(Peer):
    successor: RemotePeer

    def __init__(self, ip: ipaddress.IPv4Address, port: int, id: Key, successor: RemotePeer) -> None:
        super().__init__(ip, port, id)
        self.successor = successor

    def getSuccessor(self) -> RemotePeer:
        return self.successor


class Finger():
    start: Key
    interval: Optional[bytes]
    node: Optional[Peer]
    
    def __init__(self, start: Key, interval: bytes = None, node: Peer = None) -> None:
        self.start = start
        self.interval = interval
        self.node = node


class FingerTable():
    successor: Union[LocalPeer, RemotePeer]
    predecessor: Union[LocalPeer, RemotePeer]
    fingers: List[Finger]
    
    def __init__(self, node_id: Key) -> None:
        self._initFingers(node_id)

    def _initFingers(self, node_id: Key) -> None:
        self.fingers = [self._initFinger(i, node_id) for i in range(0, KEYLENGTH)]
    
    def _initFinger(self, index: int, node_id: Key) -> Finger:
        start_key = addKey(node_id, Key(hex(2**index)[2:].zfill(64)))
        return Finger(start_key)


class Node():
    ip: ipaddress.IPv4Address
    port: int
    id: Key 
    table: FingerTable
    localpeer: LocalPeer
    
    def __init__(self, ip: ipaddress.IPv4Address, port: int, initialpeer: Optional[RemotePeer] = None) -> None:
        self.ip = ip
        self.port = port
        self.id = self._generateNodeId()
        self.table = FingerTable(self.id)

        self._initFingerTable(initialpeer)
    
    def _initFingerTable(self, initialpeer: Optional[RemotePeer]) -> None:
        if initialpeer:
            print("Note: Not implemented")
        else:
            self.localpeer = LocalPeer(self.ip, self.port, self.id, RemotePeer(self.ip, self.port, self.id))
            for i in range(KEYLENGTH):
                self.table.fingers[i].node = self.localpeer
            self.table.successor = self.table.fingers[0].node #type: ignore
            self.table.predecessor = self.localpeer

    def _generateNodeId(self) -> Key:
        return Key(hashlib.sha256(self.ip.packed).hexdigest())

    def findSuccessor(self, key: Key) -> Union[LocalPeer, RemotePeer]:
        predecessor: Union[LocalPeer, RemotePeer] = self.findPredecessor(key)
        return predecessor.getSuccessor()

    def findPredecessor(self, key: Key) -> Union[LocalPeer, RemotePeer]:
        node = self.localpeer
        suc = node.getSuccessor()
        while not isBetween(node.id, suc.id, key):
            print("not implemented")
        return node


class NodeServicer(peer_pb2_grpc.PeerServicer):
    def __init__(self, ip: ipaddress.IPv4Address, port: int) -> None:
        super().__init__()
        self.node = Node(ip, port)

    def getSuccessor(self, request, context): #type: ignore
        suc = self.node.table.successor
        return peer_pb2.Successor(suc_id=suc.id.value, suc_ip=suc.ip.packed, suc_port=suc.port)

from concurrent import futures
import time

_ALIVE_CHECK_INTERVAL = 1
class NodeServer():
    def __init__(self, ip: ipaddress.IPv4Address, port: int) -> None:
        self.servicer = NodeServicer(ip, port)
        self.alive = True
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        peer_pb2_grpc.add_PeerServicer_to_server(self.servicer, self.server) #type: ignore
        self.server.add_insecure_port("[::]:"+str(port))
        
    def serve(self) -> None:
        self.server.start()
        try:
            while True:
                time.sleep(_ALIVE_CHECK_INTERVAL)
                if not self.alive:
                    break
        except KeyboardInterrupt:
            self.stop()        

    def stop(self) -> None:
        self.server.stop(0)
        self.alive = False
