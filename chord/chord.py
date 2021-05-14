from __future__ import annotations
from typing import List, Union, Optional

import hashlib
import ipaddress

from abc import ABCMeta
from abc import abstractmethod

import grpc
from chord.grpcprotos import peer_pb2
from chord.grpcprotos import peer_pb2_grpc  

from chord.key import *



KEYLENGTH = 256  # Note: we use sha256 hash as a key



class Peer(metaclass = ABCMeta):
    ip: ipaddress.IPv4Address
    port: int
    id: Key

    def __init__(self, ip: ipaddress.IPv4Address, port: int) -> None:
        self.ip = ip
        self.port = port
        self.id = self._generateId()
    
    def _generateId(self) -> Key:
        return Key(hashlib.sha256(self.ip.packed).hexdigest())

    @abstractmethod
    def getSuccessor(self) -> Peer:
        pass

    @abstractmethod
    def getPredecessor(self) -> Peer: 
        pass

    @abstractmethod
    def findSuccessor(self, id: Key) -> Peer:
        pass

class RemotePeer(Peer):
    def getSuccessor(self) -> Peer:
        stub = self._getStub()

        response = stub.getSuccessor(peer_pb2.GetSuccessor())
        ip = ipaddress.IPv4Address(response.suc_ip)
        
        return RemotePeer(ip, response.suc_port)
    
    def getPredecessor(self) -> Peer: 
        pass

    def findSuccessor(self, id: Key) -> Peer:
        stub = self._getStub()

        response = stub.findSuccessor(peer_pb2.FindSuccessor(key=id.value))       
        ip = ipaddress.IPv4Address(response.suc_ip)
        
        return RemotePeer(ip, response.suc_port)

    def _getStub(self) -> peer_pb2_grpc.PeerStub:
        channel = grpc.insecure_channel(self.ip.compressed +":" + str(self.port))
        return peer_pb2_grpc.PeerStub(channel) # type: ignore



class Finger():
    start: Key
    interval: Optional[bytes]
    node: Optional[Peer]
    
    def __init__(self, start: Key, interval: bytes = None, node: Optional[Peer] = None) -> None:
        self.start = start
        self.interval = interval
        self.node = node


class FingerTable():
    successor: Peer
    predecessor: Peer
    fingers: List[Finger]
    
    def __init__(self, node_id: Key) -> None:
        self._initFingers(node_id)

    def _initFingers(self, node_id: Key) -> None:
        self.fingers = [self._initFinger(i, node_id) for i in range(0, KEYLENGTH)]
    
    def _initFinger(self, index: int, node_id: Key) -> Finger:
        start_key = addKey(node_id, Key(hex(2**index)[2:].zfill(64)))
        return Finger(start_key)


class LocalPeer(Peer):
    table: FingerTable
    id: Key

    def __init__(self, ip: ipaddress.IPv4Address, port: int, initialpeer: Optional[RemotePeer] = None) -> None:
        super().__init__(ip, port)
        self.table = FingerTable(self.id)

        self._join(initialpeer)
    
    def _join(self, initialpeer: Optional[RemotePeer]) -> None:
        if initialpeer:
            self._initFingerTable(initialpeer)
        else:
            for i in range(KEYLENGTH):
                self.table.fingers[i].node = self
            self.table.successor = self.table.fingers[0].node #type: ignore
            self.table.predecessor = self

    def _initFingerTable(self, initialpeer: RemotePeer) -> None:
        pass

    def getSuccessor(self) -> Peer:
        return self.table.successor

    def getPredecessor(self): # type: ignore #Peer
        return self.table.predecessor

    def findSuccessor(self, key: Key): # type: ignore #Peer
        predecessor: Peer = self.findPredecessor(key)
        return predecessor.getSuccessor()
 
    def findPredecessor(self, key: Key) -> Peer:
        node: Peer = self
        suc: Peer = node.getSuccessor()
        while not isBetween(node.id, suc.id, key):
            print("Note: Not implemented")
        return node


class NodeServicer(peer_pb2_grpc.PeerServicer):
    def __init__(self, ip: ipaddress.IPv4Address, port: int) -> None:
        super().__init__()
        self.node = LocalPeer(ip, port)

    def getSuccessor(self, request, context): #type: ignore
        suc = self.node.table.successor
        return peer_pb2.Successor(suc_id=suc.id.value, suc_ip=suc.ip.packed, suc_port=suc.port)
    
    def findSuccessor(self, request, context): #type: ignore
        suc: Union[LocalPeer, RemotePeer] = self.node.findSuccessor(Key(request.key))
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
