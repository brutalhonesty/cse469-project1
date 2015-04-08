import struct
import binascii


class PartitionEntry(object):

    def __init__(self, data):
        self.boot_flag = struct.unpack('<c', data[:1])[0]
        self.start_CHS_0 = struct.unpack('<B', data[1:2])[0]
        self.start_CHS_1 = struct.unpack('<B', data[2:3])[0]
        self.start_CHS_2 = struct.unpack('<B', data[3:4])[0]
        self.partition_type = struct.unpack('<c', data[4:5])[0]
        self.end_CHS_0 = struct.unpack('<B', data[5:6])[0]
        self.end_CHS_1 = struct.unpack('<B', data[6:7])[0]
        self.end_CHS_2 = struct.unpack('<B', data[7:8])[0]
        self.start_lba = struct.unpack('<I', data[8:12])[0]
        self.size_in_sectors = struct.unpack('<i', data[12:16])[0]

    def __str__(self):
        return 'Boot Flag: ' + str(self.to_value(self.boot_flag)) + '\n' \
        + 'Start CHS 0: ' + str(self.start_CHS_0) + '\n' \
        + 'Start CHS 1: ' + str(self.start_CHS_1) + '\n' \
        + 'Start CHS 2: ' + str(self.start_CHS_2) + '\n' \
        + 'Partition Type: ' + str(self.to_value(self.partition_type)) + '\n' \
        + 'End CHS 0: ' + str(self.end_CHS_0) + '\n' \
        + 'End CHS 1: ' + str(self.end_CHS_1) + '\n' \
        + 'End CHS 2: ' + str(self.end_CHS_2) + '\n' \
        + 'Start LBA: ' + str(self.start_lba) + '\n' \
        + 'Size in Sectors: ' + str(self.size_in_sectors) + '\n'

    def to_value(self, char):
        padded = '\x00\x00\x00' + str(char)
        val = int(struct.unpack('>I', padded)[0])
        return val
