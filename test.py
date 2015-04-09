#!/usr/bin/python
import struct
import sys
import binascii
import argparse


def convert_to_little_endian(argv):
    string = str(argv)
    return ''.join(string[i:i + 2] for i in reversed(xrange(0, len(string), 2)))

parser = argparse.ArgumentParser(description='Testing VBR reading.')
parser.add_argument('-i', '--input', help='Path to input image file.')
args = parser.parse_args()
if(args.input is None):
  parser.print_help()
  sys.exit(0)
input_file = open(args.input, 'rb').read()
partition_1 = input_file[446:462]
partition_type = partition_1[4:5]
print 'partition_type', binascii.b2a_hex(partition_type), 'in hex'
partition_size = partition_1[12:16]
print 'partition_size', convert_to_little_endian(binascii.b2a_hex(partition_size)), 'in hex'
partition_address = partition_1[8:12]
print 'partition_address', convert_to_little_endian(binascii.b2a_hex(partition_address)), 'in hex'
partition_address = int(convert_to_little_endian(binascii.b2a_hex(partition_address)), 16)
start_partition_1 = partition_address * 512
end_partition_1 = start_partition_1 + 512
vbr = input_file[start_partition_1:end_partition_1]
bytes_per_sector = vbr[13]
print 'bytes_per_sector', binascii.b2a_hex(bytes_per_sector), 'in hex'
reserved_area = vbr[14:16]
reserved_area_int = int(convert_to_little_endian(binascii.b2a_hex(reserved_area)), 16)
print 'reserved_area', convert_to_little_endian(binascii.b2a_hex(reserved_area)), 'in hex'
sectors_per_cluster = vbr[13]
print 'sectors_per_cluster', int(convert_to_little_endian(binascii.b2a_hex(sectors_per_cluster)), 16)
# TODO Convert above to decimal
number_of_fats = vbr[16]
number_of_fats_int = int(convert_to_little_endian(binascii.b2a_hex(number_of_fats)), 16)
print 'number_of_fats', int(convert_to_little_endian(binascii.b2a_hex(number_of_fats)), 16)
# TODO Convert above to decimal
# This below works for FAT 32, use vbr[22:24] for FAT 16
size_of_each_fat_in_sectors = vbr[36:40]
print 'size_of_each_fat_in_sectors', convert_to_little_endian(binascii.b2a_hex(size_of_each_fat_in_sectors)), 'in hex'
# TODO Convert above to decimal int('0x000002e5', 16)
size_of_each_fat_in_sectors_int = int(convert_to_little_endian(binascii.b2a_hex(size_of_each_fat_in_sectors)), 16)
print 'first_sector_of_cluster_2', 63 + reserved_area_int + (size_of_each_fat_in_sectors_int * number_of_fats_int)
