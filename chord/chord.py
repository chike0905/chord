import hashlib
import ipaddress

from abc import ABCMeta
from abc import abstractmethod

import grpc
from chord.grpcprotos import peer_pb2
from chord.grpcprotos import peer_pb2_grpc  

from typing import List, Union, Optional


KEYLENGTH = 256  # Note: we use sha256 hash as a key

# Calc tools
class Key():
    value: str

    def __init__(self, value: str) -> None:
        if len(value) != 64:
            raise Exception
        self.value = value

def addKey(key1: Key, key2: Key) -> Key: 
    newvalue = int(key1.value, 16) + int(key2.value, 16)
    if len(hex(newvalue)[2:]) > 64:
        newvalue = newvalue - int("".ljust(64, "f"), 16) - 1
    return Key(hex(newvalue)[2:].zfill(64))

def isBetween(start: Key, end: Key, target: Key) -> bool:
    if start.value < end.value:
        return start.value < target.value <= end.value
    else: # start.value >= end.value
        return start.value < target.value or target.value <= end.value


class Peer(metaclass = ABCMeta):
    ip: ipaddress.IPv4Address
    port: int
    id: Key

    def __init__(self, ip: ipaddress.IPv4Address, port: int, id: Key) -> None:
        self.ip = ip
        self.port = port
        self.id = id

    @abstractmethod
    def successor(self):  # type: ignore
        pass


class LocalPeer(Peer):
    def successor(self) -> Peer:
        return self


class RemotePeer(Peer):
    def successor(self) -> Peer:
        print("not implemented")
        return self


class Finger():
    start: Key
    interval: Optional[bytes]
    node: Optional[Peer]
    
    def __init__(self, start: Key, interval: bytes = None, node: Peer = None) -> None:
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


class Node():
    ip: ipaddress.IPv4Address
    port: int
    id: Key 
    table: FingerTable
    
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
            for i in range(KEYLENGTH):
                self.table.fingers[i].node = LocalPeer(self.ip, self.port, self.id)
            self.table.successor = self.table.fingers[0].node #type: ignore
            self.table.predecessor = LocalPeer(self.ip, self.port, self.id)

    def _generateNodeId(self) -> Key:
        return Key(hashlib.sha256(self.ip.packed).hexdigest())

    def findSuccessor(self, key: Key) -> Union[LocalPeer, RemotePeer]:
        predecessor: Union[LocalPeer, RemotePeer] = self.findPredecessor(key)
        return predecessor.successor()

    def findPredecessor(self, key: Key) -> Peer:
        node = LocalPeer(self.ip, self.port, self.id) 
        suc = self.table.successor.id
        while not isBetween(node.id, suc, key):
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
