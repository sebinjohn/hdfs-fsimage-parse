# Class for representing FileSummary
# HDFS FSImage contains a section towards the end called FileSummary which
# contains the details of the other section in the serialized FSImage


import fsimage_pb2
from google.protobuf.internal import decoder as decoder


class Section(object):
    def __init__(elf, n, l, o):
        elf.name = n
        elf.length = l
        elf.offset = o

    @property
    def s_name(elf):
        return elf.name

    @property
    def s_length(elf):
        return elf.length

    @property
    def s_offset(elf):
        return elf.offset


class FileSummary(object):

    def __init__(self, buf, pos):
        self.fs_sections = None
        self.parse_file_summary(buf, pos)
        self.separate_sections()

    def parse_file_summary(self, buf, pos):
        (len, buf_pos) = decoder._DecodeVarint(buf, pos)
        fs_bytes = buf[buf_pos:buf_pos + len]
        fs = fsimage_pb2.FileSummary()
        fs.ParseFromString(fs_bytes)
        self.fs_sections = fs.sections

    def separate_sections(self):
        self.sections = {}
        for section in self.fs_sections:
            s = Section(section.name, section.length, section.offset)
            self.sections[section.name] = s
        return True

    @property
    def names(self):
        return self.sections.keys()

    def get_section(self, name):
        return self.sections[name]
