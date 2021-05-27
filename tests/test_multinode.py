from chord.chord import *

import ipaddress
import hashlib

from tests.tools import *


# Tools
def waitLocalNodeJoinProcess(localnode: LocalPeer) -> None:
    while True:
        if localnode.joined:
            break


@pytest.fixture(scope="function")
def nodeWithInitialPeer(nodeA):  # type: ignore
    nodeBthread, nodeBserver = setupNodeThread(B_IP, B_PORT, IP, PORT)
    nodeB = nodeBserver.servicer.node
    nodeBthread.start()
    print("waiting node B join...")
    waitLocalNodeJoinProcess(nodeB)

    yield nodeA, nodeB

    nodeBserver.stop()
    nodeBthread.join()


@pytest.fixture(scope="function")
def setup3NodeCluster(nodeA):  # type: ignore
    # nodeA: 9c9ce...
    # nodeB: e762d...
    # nodeC: bd565...
    nodeBthread, nodeBserver = setupNodeThread(B_IP, B_PORT, IP, PORT)
    nodeB = nodeBserver.servicer.node
    nodeBthread.start()
    waitLocalNodeJoinProcess(nodeB)

    nodeCthread, nodeCserver = setupNodeThread(C_IP, C_PORT, IP, PORT)
    nodeC = nodeCserver.servicer.node
    nodeCthread.start()
    waitLocalNodeJoinProcess(nodeC)

    yield nodeA, nodeB, nodeC

    nodeBserver.stop()
    nodeBthread.join()

    nodeCserver.stop()
    nodeCthread.join()


def test_3nodes(nodeWithInitialPeer: Tuple[LocalPeer, LocalPeer]) -> None:
    # nodeA: 9c9ce...
    # nodeB: e762d...
    nodeA, nodeB = nodeWithInitialPeer
    nodeC = NodeServer(C_IP, C_PORT, IP, PORT)  # bd565...

    localnode = nodeC.servicer.node
    thread = threading.Thread(None, nodeC.serve)
    thread.start()

    waitLocalNodeJoinProcess(localnode)

    # Finger Check for C
    for i in range(KEYLENGTH):
        if isBetween(B_ID, ID, localnode.table.fingers[i].start):
            assert localnode.table.fingers[i].node.id.value == ID.value    # type: ignore
        elif isBetween(ID, C_ID, localnode.table.fingers[i].start):
            assert localnode.table.fingers[i].node.id.value == C_ID.value  # type: ignore
        elif isBetween(C_ID, B_ID, localnode.table.fingers[i].start):
            assert localnode.table.fingers[i].node.id.value == B_ID.value  # type: ignore
        else:
            print("Finger is incollect")
            assert False

    # Finger Check for A
    for i in range(KEYLENGTH):
        if isBetween(B_ID, ID, nodeA.table.fingers[i].start):
            assert nodeA.table.fingers[i].node.id.value == ID.value    # type: ignore
        elif isBetween(ID, C_ID, nodeA.table.fingers[i].start):
            assert nodeA.table.fingers[i].node.id.value == C_ID.value  # type: ignore
        elif isBetween(C_ID, B_ID, nodeA.table.fingers[i].start):
            assert nodeA.table.fingers[i].node.id.value == B_ID.value  # type: ignore
        else:
            print("Finger is incollect")
            assert False

    # Finger Check for B
    for i in range(KEYLENGTH):
        if isBetween(B_ID, ID, nodeB.table.fingers[i].start):
            assert nodeB.table.fingers[i].node.id.value == ID.value    # type: ignore
        elif isBetween(ID, C_ID, nodeB.table.fingers[i].start):
            assert nodeB.table.fingers[i].node.id.value == C_ID.value  # type: ignore
        elif isBetween(C_ID, B_ID, nodeB.table.fingers[i].start):
            assert nodeB.table.fingers[i].node.id.value == B_ID.value  # type: ignore
        else:
            print("Finger is incollect")
            assert False

    # Teradown
    nodeC.stop()
    thread.join()


def findSuccessorFromNode(localnode: LocalPeer) -> None:
    key = Key("1".ljust(64, "0"))  # 1000...0000
    suc = localnode.findSuccessor(key)

    assert suc.id.value == ID.value

    key = Key("a".ljust(64, "0"))  # a000...0000
    suc = localnode.findSuccessor(key)

    assert suc.id.value == C_ID.value

    key = Key("d".ljust(64, "0"))  # c000...0000
    suc = localnode.findSuccessor(key)

    assert suc.id.value == B_ID.value


def test_findSuccessorWith3nodes(setup3NodeCluster: Tuple[LocalPeer, LocalPeer, LocalPeer]) -> None:
    # nodeA: 9c9ce...
    # nodeB: e762d...
    # nodeC: bd565...
    nodeA, nodeB, nodeC = setup3NodeCluster

    findSuccessorFromNode(nodeA)
    findSuccessorFromNode(nodeB)
    findSuccessorFromNode(nodeC)
