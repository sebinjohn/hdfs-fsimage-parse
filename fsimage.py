# :D
import struct
from google.protobuf.internal import decoder as decoder
import fsimage_pb2

from file_summary import FileSummary


def get_file_summary_length(buf, n_bytes):
    b = buf[-n_bytes:]
    (n,) = struct.unpack('>i', b)
    return n


def get_n_inodes(buf, b_pos, n):
    inode = fsimage_pb2.INodeSection()
    inodes = []
    for _ in xrange(n):
        (len, pos) = decoder._DecodeVarint(buf, b_pos)
        inode_bytes = buf[pos:pos + len]
        inode.ParseFromString(inode_bytes)
        inodes.append(inode)


def start(input_file):
    FILE_SUMMARY_LENGTH_BYTES = 4
    with open(input_file) as f:
        buf = f.read()
    buf_length = len(buf)
    fs_length = get_file_summary_length(buf, FILE_SUMMARY_LENGTH_BYTES)
    pos = buf_length - fs_length - FILE_SUMMARY_LENGTH_BYTES
    fs = FileSummary(buf, pos)
    print fs.names

    # Process INODE Section
    n = 10
    get_n_inodes(buf, fs.get_section('INODE').offset, n)


