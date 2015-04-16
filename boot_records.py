#!/usr/bin/python
import binascii
import argparse
import hashlib
import ntpath
import sys
import os
import struct

from partition_table import PartitionTable

PARTITION_TYPES = {
    0x01: 'DOS 12-bit FAT',
    0x04: 'DOS 16-bit FAT for partitions smaller than 32 MB',
    0x05: 'Extended partition',
    0x06: 'DOS 16-bit FAT for partitions larger than 32 MB',
    0x07: 'NTFS',
    0x08: 'AIX bootable partition',
    0x09: 'AIX data partition',
    0x0B: 'DOS 32-bit FAT',
    0x0C: 'DOS 32-bit FAT for interrupt 13 support',
    0x17: 'Hidden NTFS partition (XP and earlier)',
    0x1B: 'Hidden FAT32 partition',
    0x1E: 'Hidden VFAT partition',
    0x3C: 'Partition Magic recovery partition',
    0x66: 'Novell partitions',
    0x67: 'Novell partitions',
    0x68: 'Novell partitions',
    0x69: 'Novell partitions',
    0x81: 'Linux',
    0x82: 'Linux swap partition (can also be associated with Solaris partitions)',
    0x83: 'Linux native file system (Ext2, Ext3, Reiser, xiafs)',
    0x86: 'FAT16 volume/stripe set (Windows NT)',
    0x87: 'High Performace File System (HPFS) fault-tolerant mirrored partition or NTFS volume/stripe set',
    0xA5: 'FreeBSD and BSD/386',
    0xA6: 'OpenBSD',
    0xA9: 'NetBSD',
    0xC7: 'Typical of a corrupted NTFS volume/stripe set',
    0xEB: 'BeOS'
}

def convert_to_little_endian(argv):
    string = str(argv)
    return ''.join(string[i:i + 2] for i in reversed(xrange(0, len(string), 2)))


def _write_md5_file(file_name, hash_value):
    '''
    Write the md5 hash value to a file given the file name.

    @type file_name: string
    @param file_name: The file name of the file.
    @type hash_value: string
    @param hash_value: The hash in hex to store.
    @rtype: None
    @return: None
    '''
    md5_file = open('MD5-' + file_name + '.txt', 'w')
    md5_file.write(hash_value)
    md5_file.close()
    return None


def _write_sha1_file(file_name, hash_value):
    '''
    Write the sha1 hash value to a file given the file name.

    @type file_name: string
    @param file_name: The file name of the file.
    @type hash_value: string
    @param hash_value: The hash in hex to store.
    @rtype: None
    @return: None
    '''
    sha1_file = open('SHA1-' + file_name + '.txt', 'w')
    sha1_file.write(hash_value)
    sha1_file.close()
    return None


def _parse_mbr(input_file):
    '''
    Parse the MBR into the partition table class.

    @type input_file: string
    @param input_file: The binary file being read.
    @rtype: PartitionTable
    @return: The partition table class instantiated.
    '''
    boot_data = input_file[:440]
    partition_table_data = PartitionTable(input_file[440:])
    return partition_table_data


def _extract_vbr(partition_table, input_file):
	offsets = [0, 16, 32, 48]
	partition_size = 0
	for index, offset in enumerate(offsets):
		partition = input_file[(446 + offset):(462 + offset)]
		partition_type = partition[4:5]
		partition_address = partition[8:12]
		partition_address = int(convert_to_little_endian(binascii.b2a_hex(partition_address)), 16)
		start_partition = partition_address * 512
		end_partition = start_partition + 512
		vbr = input_file[start_partition:end_partition]
		bytes_per_sector = vbr[13]
		reserved_area = vbr[14:16]
		reserved_area_int = int(convert_to_little_endian(binascii.b2a_hex(reserved_area)), 16)
		sectors_per_cluster = vbr[13]
		sectors_per_cluster_int = int(convert_to_little_endian(binascii.b2a_hex(sectors_per_cluster)), 16)
		number_of_fats = vbr[16]
		number_of_fats_int = int(convert_to_little_endian(binascii.b2a_hex(number_of_fats)), 16)
		
		# This below works for FAT 32, use vbr[22:24] for FAT 16
		size_of_each_fat_in_sectors = vbr[36:40] if (to_value(partition_type) == 11) else vbr[22:24]
		size_of_each_fat_in_sectors_int = int(convert_to_little_endian(binascii.b2a_hex(size_of_each_fat_in_sectors)), 16)
		
		print('=======================================')
		print("Partition %d(%s)" % (index, to_type(to_value(partition_type))))
		print("Reserved area: Start sector: %d Ending sector: %d Size: %d sectors" % (0, (reserved_area_int - 1), (reserved_area_int - 1) + 1))
		print("Sectors per cluster: %d sectors" % (sectors_per_cluster_int))
		print("FAT area: Starting sector: %d Ending sector: %d" % (reserved_area_int, (reserved_area_int - 1 + (number_of_fats_int * size_of_each_fat_in_sectors_int))))
		print("# of FATs: %d" % (number_of_fats_int))
		print("The size of each FAT: %d sectors" % (size_of_each_fat_in_sectors_int))
		print("The first sector of cluster 2: %d sectors" % (partition_size + reserved_area_int + (size_of_each_fat_in_sectors_int * number_of_fats_int)))
		partition_size += int(convert_to_little_endian(binascii.b2a_hex(partition[12:16])), 16)
		


def _display_mbr(partition_table):
    '''
    Output the MBR data to the console.

    @type partition_table: PartitionTable
    @param partition_table: The partition table class instantiated.
    @rtype: None
    @return: None
    '''
    print '(0{0:x}) {1}, {2}, {3}'.format(
        to_value(partition_table.entry_0.partition_type),
        to_type(to_value(partition_table.entry_0.partition_type)),
        str(partition_table.entry_0.start_lba).zfill(10),
        str(partition_table.entry_0.size_in_sectors).zfill(10))
    print '(0{0:x}) {1}, {2}, {3}'.format(
        to_value(partition_table.entry_1.partition_type),
        to_type(to_value(partition_table.entry_1.partition_type)),
        str(partition_table.entry_1.start_lba).zfill(10),
        str(partition_table.entry_1.size_in_sectors).zfill(10))
    print '(0{0:x}) {1}, {2}, {3}'.format(
        to_value(partition_table.entry_2.partition_type),
        to_type(to_value(partition_table.entry_2.partition_type)),
        str(partition_table.entry_2.start_lba).zfill(10),
        str(partition_table.entry_2.size_in_sectors).zfill(10))
    print '(0{0:x}) {1}, {2}, {3}'.format(
        to_value(partition_table.entry_3.partition_type),
        to_type(to_value(partition_table.entry_3.partition_type)),
        str(partition_table.entry_3.start_lba).zfill(10),
        str(partition_table.entry_3.size_in_sectors).zfill(10))
    # print '======================================='


def _display_vbr(partition_table, vbr):
    print 'Partition 0({0}):'.format(
        to_type(to_value(partition_table.entry_0.partition_type)))
    print 'Reserved area: Start Sector: {0} Ending Sector: {1} Size: {2} sectors'.format()
    print 'Sectors per cluster: {0} sectors'.format()
    print 'FAT Area: Start Sector: {0} Ending Sector: {1}'.format()
    print '# of FATs: {0}'.format()
    print 'The size of each FAT: {0} sectors'.format()
    print 'The first sector of cluster 2: {0} sectors'.format()
    print '======================================='
    print 'Partition 1({0}):'.format(
        to_type(to_value(partition_table.entry_1.partition_type)))
    print 'Reserved area: Start Sector: {0} Ending Sector: {1} Size: {2} sectors'.format()
    print 'Sectors per cluster: {0} sectors'.format()
    print 'FAT Area: Start Sector: {0} Ending Sector: {1}'.format()
    print '# of FATs: {0}'.format()
    print 'The size of each FAT: {0} sectors'.format()
    print 'The first sector of cluster 2: {0} sectors'.format()
    print '======================================='
    print 'Partition 2({0}):'.format(
        to_type(to_value(partition_table.entry_2.partition_type)))
    print 'Reserved area: Start Sector: {0} Ending Sector: {1} Size: {2} sectors'.format()
    print 'Sectors per cluster: {0} sectors'.format()
    print 'FAT Area: Start Sector: {0} Ending Sector: {1}'.format()
    print '# of FATs: {0}'.format()
    print 'The size of each FAT: {0} sectors'.format()
    print 'The first sector of cluster 2: {0} sectors'.format()
    print '======================================='
    print 'Partition 3({0}):'.format(
        to_type(to_value(partition_table.entry_3.partition_type)))
    print 'Reserved area: Start Sector: {0} Ending Sector: {1} Size: {2} sectors'.format()
    print 'Sectors per cluster: {0} sectors'.format()
    print 'FAT Area: Start Sector: {0} Ending Sector: {1}'.format()
    print '# of FATs: {0}'.format()
    print 'The size of each FAT: {0} sectors'.format()
    print 'The first sector of cluster 2: {0} sectors'.format()


def to_value(char):
    padded = '\x00\x00\x00' + str(char)
    val = int(struct.unpack('>I', padded)[0])
    return val


def to_type(partition_type):
    return PARTITION_TYPES.get(partition_type)


def main():
    parser = argparse.ArgumentParser(
        description='Extract and read MBR and VBR for given image file.')
    parser.add_argument('-i', '--input', help='Path to a RAW image file.')
    args = parser.parse_args()
    if args.input is None:
        parser.print_help()
        sys.exit(1)
    if not os.path.isfile(args.input):
        print 'File does not exist.'
        sys.exit(1)
    input_file = open(args.input, 'rb').read()
    file_name = ntpath.basename(args.input).split('.')[0]
    md5_hash = hashlib.md5(input_file).hexdigest()
    sha1_hash = hashlib.sha1(input_file).hexdigest()
    print 'Checksums:'
    print '======================================='
    print 'MD5: ' + md5_hash + '\n'
    print 'SHA1: ' + sha1_hash
    print '======================================='
    _write_md5_file(file_name, md5_hash)
    _write_sha1_file(file_name, sha1_hash)
    input_file = open(args.input, 'rb').read()
    mbr = input_file[:512]
    partition_table = _parse_mbr(mbr)
    _display_mbr(partition_table)
    vbr = _extract_vbr(partition_table, input_file)
    # _display_vbr(partition_table, vbr)

if __name__ == '__main__':
    main()
