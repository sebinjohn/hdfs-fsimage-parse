# :D
import sys
import struct
from file_summary import FileSummary
from inode_section import INodeSection


def get_file_summary_length(buf, file_summary_length_bytes=4):
    file_summary_length_bytes = 4
    if len(buf) < file_summary_length_bytes:
        raise Exception('buffer length less than ' + str(file_summary_length_bytes))
    b = buf[-file_summary_length_bytes:]
    (n,) = struct.unpack('>i', b)
    return n


def read_input_file(input_file):
    """
    input_file:
    """
    with open(input_file) as f:
        buf = f.read()
    return buf


def parse_file_summary(buf):
    FILE_SUMMARY_LENGTH_BYTES = 4
    buf_length = len(buf)
    fs_length = get_file_summary_length(buf, FILE_SUMMARY_LENGTH_BYTES)
    pos = buf_length - fs_length - FILE_SUMMARY_LENGTH_BYTES
    fs = FileSummary(buf, pos)
    return fs


def parse_inode_section(buf, file_summary):
    # Process INODE Section
    inode_section = INodeSection(buf, file_summary.get_section('INODE'))
    return inode_section


def write_a_million(outf, temp):
    interim = [x.name for x in temp]
    outf.write('\n'.join(interim))


def main():
    buf = read_input_file(sys.argv[1])
    file_summary = parse_file_summary(buf)
    inode_section = parse_inode_section(buf, file_summary)
    inodes = inode_section.get_n_inodes(inode_section.num_inodes)
    with open('file_names.sc', 'w') as outf:
        n = 0
        MILLION = 1000000
        a = inode_section.num_inodes / MILLION
        while n <= a * MILLION:
            outf.write('\n'.join(next(inodes).name for _ in xrange(MILLION)))
            n += MILLION
        outf.write('\n'.join(next(inodes).name for _ in xrange(inode_section.num_inodes - n)))

if __name__ == '__main__':
    main()
