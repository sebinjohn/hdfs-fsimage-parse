from google.protobuf.internal import decoder as decoder
import fsimage_pb2


class INode(object):
    def __init__(self):
        self.type = None
        self.id = None
        self.name = None


class INodeFile(object):

    def __init__(self):
        self.replication = None
        self.modification_time = None
        self.access_time = None
        self.blocks = []


class INodeSection(object):

    def __init__(self, start_pos):
        pass
        self._start_pos = start_pos
        self.num_inodes = None
        self.last_inode_id = None

    @property
    def start_pos(self):
        return self._start_pos

    def get_n_inodes(buf, b_pos, n):
        inode = fsimage_pb2.INodeSection()
        inodes = []
        for _ in xrange(n):
            (len, pos) = decoder._DecodeVarint(buf, b_pos)
            inode_bytes = buf[pos:pos + len]
            inode.ParseFromString(inode_bytes)
            inodes.append(inode)
