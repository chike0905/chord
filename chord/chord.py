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


class Peer(metaclass=ABCMeta):
    ip: ipaddress.IPv4Address
    port: int
    id: Key

    def __init__(self, ip: ipaddress.IPv4Address, port: int) -> None:
        self.ip = ip
        self.port = port
        self.id = self._generateId()

    def _generateId(self) -> Key:
        key_source = self.ip.packed + bytes(self.port)
        key_value = hashlib.sha256(key_source).hexdigest()
        return Key(key_value)

    @abstractmethod
    def getSuccessor(self) -> Peer:
        pass

    @abstractmethod
    def getPredecessor(self) -> Peer:
        pass

    @abstractmethod
    def updatePredecessor(self, predecessor: Peer) -> bool:
        pass

    @abstractmethod
    def updateFingerTable(self, s: Peer, i: int) -> bool:
        pass

    @abstractmethod
    def findSuccessor(self, id: Key) -> Peer:
        pass


class RemotePeer(Peer):
    def getSuccessor(self) -> Peer:
        stub = self._getStub()

        msg = peer_pb2.GetSuccessor()
        response = stub.getSuccessor(msg)
        ip = ipaddress.IPv4Address(response.ip)

        return RemotePeer(ip, response.port)

    def getPredecessor(self) -> Peer:
        stub = self._getStub()

        msg = peer_pb2.GetPredecessor()
        response = stub.getPredecessor(msg)
        ip = ipaddress.IPv4Address(response.ip)

        return RemotePeer(ip, response.port)

    def updatePredecessor(self, predecessor: Peer) -> bool:
        stub = self._getStub()

        msg = peer_pb2.NotifyPredecessor(ip=predecessor.ip.packed,
                                         port=predecessor.port)
        response = stub.updatePredecessor(msg)

        return response.res

    def updateFingerTable(self, s: Peer, i: int) -> bool:
        stub = self._getStub()

        msg = peer_pb2.UpdateFingerTable(index=i, ip=s.ip.packed, port=s.port)
        response = stub.updateFingerTable(msg)

        return response.res

    def findSuccessor(self, id: Key) -> Peer:
        stub = self._getStub()

        msg = peer_pb2.FindSuccessor(key=id.value)
        response = stub.findSuccessor(msg)
        ip = ipaddress.IPv4Address(response.ip)

        return RemotePeer(ip, response.port)

    def _getStub(self) -> peer_pb2_grpc.PeerStub:
        dist = self.ip.compressed + ":" + str(self.port)
        channel = grpc.insecure_channel(dist)
        return peer_pb2_grpc.PeerStub(channel)  # type: ignore


class Finger():
    start: Key
    interval: Optional[bytes]
    node: Optional[Peer]

    def __init__(self,
                 start: Key,
                 interval: bytes = None,
                 node: Optional[Peer] = None
                 ) -> None:
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
        self.fingers = [self._initFinger(i, node_id)
                        for i in range(0, KEYLENGTH)]

    def _initFinger(self, index: int, node_id: Key) -> Finger:
        start_key = addKey(node_id, Key(hex(2**index)[2:].zfill(64)))
        return Finger(start_key)


class LocalPeer(Peer):
    table: FingerTable
    id: Key
    initialpeer: Optional[RemotePeer] = None
    joined: bool = False

    def __init__(self,
                 ip: ipaddress.IPv4Address,
                 port: int,
                 initialpeer_ip: Optional[ipaddress.IPv4Address] = None,
                 initialpeer_port: Optional[int] = None
                 ) -> None:
        super().__init__(ip, port)
        self.table = FingerTable(self.id)
        if initialpeer_ip and initialpeer_port:
            self.initialpeer = RemotePeer(initialpeer_ip, initialpeer_port)

    def join(self) -> None:
        if self.initialpeer:
            self._initFingerTable(self.initialpeer)
        else:
            for i in range(KEYLENGTH):
                self.table.fingers[i].node = self
            self.table.successor = self.table.fingers[0].node  # type: ignore
            self.table.predecessor = self
        self.joined = True

    def _initFingerTable(self, initialpeer: RemotePeer) -> None:
        self.table.fingers[0].node = \
            initialpeer.findSuccessor(self.table.fingers[0].start)
        self.table.successor = self.table.fingers[0].node  # type: ignore
        self.table.successor.updatePredecessor(self)

        for i in range(KEYLENGTH - 1):
            if isBetween(self.id,
                         self.table.fingers[i].node.id,     # type: ignore
                         self.table.fingers[i + 1].start):  # type: ignore
                self.table.fingers[i + 1].node = self.table.fingers[i].node
            else:
                self.table.fingers[i + 1].node = \
                    initialpeer.findSuccessor(self.table.fingers[i + 1].start)
        self._update_others()

    def _update_others(self) -> None:
        for i in range(KEYLENGTH):
            key = subKey(self.id, Key(hex(2**i)[2:].zfill(64)))
            p = self.findPredecessor(key)
            p.updateFingerTable(self, i)

    def updateFingerTable(self, s: Peer, i: int) -> bool:
        if isBetween(self.id,                        # type: ignore
                     self.table.fingers[i].node.id,  # type: ignore
                     s.id):                          # type: ignore
            self.table.fingers[i].node = s
            if i == 0:
                self.table.successor = s

            if self.table.predecessor.id.value != self.id.value:
                self.table.predecessor.updateFingerTable(s, i)
        return True

    def getSuccessor(self) -> Peer:
        return self.table.successor

    def getPredecessor(self) -> Peer:
        return self.table.predecessor

    def updatePredecessor(self, predecessor: Peer) -> bool:
        # TODO: Validation of proposed predecessor
        self.table.predecessor = predecessor
        return True

    def findSuccessor(self, key: Key) -> Peer:
        predecessor: Peer = self.findPredecessor(key)
        return predecessor.getSuccessor()

    def findPredecessor(self, key: Key) -> Peer:
        node: Peer = self
        suc: Peer = node.getSuccessor()
        while not isBetween(node.id, suc.id, key):
            node = self.closestPrecedingFinger(key)
        return node

    def closestPrecedingFinger(self, key: Key) -> Peer:
        for i in reversed(range(KEYLENGTH)):
            if isBetween(self.id,                         # type: ignore
                         key,
                         self.table.fingers[i].node.id):  # type: ignore
                return self.table.fingers[i].node  # type: ignore
        return self


class NodeServicer(peer_pb2_grpc.PeerServicer):
    def __init__(self,
                 ip: ipaddress.IPv4Address,
                 port: int,
                 initial_ip: Optional[ipaddress.IPv4Address] = None,
                 initial_port: Optional[int] = None) -> None:
        super().__init__()
        self.node = LocalPeer(ip, port, initial_ip, initial_port)

    def getSuccessor(self, request, context):  # type: ignore
        peer = self.node.getSuccessor()
        return peer_pb2.PeerResponse(id=peer.id.value,
                                     ip=peer.ip.packed,
                                     port=peer.port)

    def getPredecessor(self, request, context):  # type: ignore
        peer = self.node.getPredecessor()
        return peer_pb2.PeerResponse(id=peer.id.value,
                                     ip=peer.ip.packed,
                                     port=peer.port)

    def updatePredecessor(self, request, context):  # type: ignore
        ip = ipaddress.IPv4Address(request.ip)
        new_predecessor = RemotePeer(ip, request.port)
        res = self.node.updatePredecessor(new_predecessor)
        return peer_pb2.StatusResponse(res=res)

    def updateFingerTable(self, request, context):  # type: ignore
        ip = ipaddress.IPv4Address(request.ip)
        new_finger = RemotePeer(ip, request.port)
        res = self.node.updateFingerTable(new_finger, request.index)
        return peer_pb2.StatusResponse(res=res)

    def findSuccessor(self, request, context):  # type: ignore
        suc: Union[LocalPeer, RemotePeer] = \
            self.node.findSuccessor(Key(request.key))
        return peer_pb2.PeerResponse(id=suc.id.value,
                                     ip=suc.ip.packed,
                                     port=suc.port)


# Node Server
from concurrent import futures
import time

_ALIVE_CHECK_INTERVAL = 1


class NodeServer():
    def __init__(self,
                 ip: ipaddress.IPv4Address,
                 port: int,
                 initial_ip: Optional[ipaddress.IPv4Address] = None,
                 initial_port: Optional[int] = None) -> None:
        self.servicer = NodeServicer(ip, port, initial_ip, initial_port)
        self.alive = True
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        peer_pb2_grpc.add_PeerServicer_to_server(self.servicer, self.server)   # type: ignore
        ip_port: str = ip.compressed + ":" + str(port)
        self.server.add_insecure_port(ip_port)

    def serve(self) -> None:
        self.server.start()
        self.servicer.node.join()
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
