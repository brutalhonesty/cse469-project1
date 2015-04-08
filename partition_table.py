import struct
from partition_entry import PartitionEntry


class PartitionTable(object):

    def __init__(self, data):
        self.disk_signature_0 = struct.unpack('<B', data[:1])[0]
        self.disk_signature_1 = struct.unpack('<B', data[1:2])[0]
        self.disk_signature_2 = struct.unpack('<B', data[2:3])[0]
        self.disk_signature_3 = struct.unpack('<B', data[3:4])[0]
        self.unused = struct.unpack('<H', data[4:6])[0]
        self.entry_0 = PartitionEntry(data[6:22])
        self.entry_1 = PartitionEntry(data[22:38])
        self.entry_2 = PartitionEntry(data[38:54])
        self.entry_3 = PartitionEntry(data[54:70])
        self.signature = struct.unpack('<H', data[70:72])[0]

    def __str__(self):
        return 'Disk Signature 0: ' + str(self.disk_signature_0) + '\n' \
        + 'Disk Signature 1: ' + str(self.disk_signature_1) + '\n' \
        + 'Disk Signature 2: ' + str(self.disk_signature_2) + '\n' \
        + 'Disk Signature 3: ' + str(self.disk_signature_3) + '\n' \
        + 'Unused: ' + str(self.unused) + '\n' \
        + 'Entry 0: ' + str(self.entry_0) + '\n' \
        + 'Entry 1: ' + str(self.entry_1) + '\n' \
        + 'Entry 2: ' + str(self.entry_2) + '\n' \
        + 'Entry 3: ' + str(self.entry_3) + '\n' \
        + 'Signature: ' + str(self.signature) + '\n' \
