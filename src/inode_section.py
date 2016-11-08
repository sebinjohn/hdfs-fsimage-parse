from google.protobuf.internal import decoder as decoder
import protobufs.fsimage_pb2 as fsimage_pb2


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

    def __init__(self, buf, fs_inode_section):
        self.buf = buf
        self._start_pos = fs_inode_section.offset
        self.num_inodes = None
        self.last_inode_id = None
        self.inode_section = self.load_inode_section()

    @property
    def start_pos(self):
        return self._start_pos

    def load_inode_section(self):
        inode_section = fsimage_pb2.INodeSection()
        (len, pos) = decoder._DecodeVarint(self.buf, self._start_pos)
        inode_section_bytes = self.buf[pos:pos + len]
        inode_section.ParseFromString(inode_section_bytes)
        self.num_inodes = inode_section.numInodes
        self.last_inode_id = inode_section.lastInodeId
        self._cur_pos = pos + len
        return inode_section

    def get_n_inodes(self, n, start_pos=None):
        if not start_pos:
            if not self._cur_pos:
                inode_sec = self.load_inode_section()
                start_pos = self._cur_pos
            else:
                start_pos = self._cur_pos
                inode_sec = self.inode_section
        else:
            inode_sec = self.inode_section

        new_pos = start_pos
        for _ in xrange(n):
            (len, pos) = decoder._DecodeVarint(self.buf, new_pos)
            inode_bytes = self.buf[pos:pos + len]
            inode = inode_sec.INode()
            inode.ParseFromString(inode_bytes)
            new_pos = pos + len
            yield inode
