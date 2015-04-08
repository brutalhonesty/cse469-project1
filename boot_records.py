import hashlib
import ntpath
import sys
import os
import argparse


def _write_md5_file(file_name, hash_value):
    md5_file = open('MD5-' + file_name + '.txt', 'w')
    md5_file.write(hash_value)
    md5_file.close()
    return None


def _write_sha1_file(file_name, hash_value):
    sha1_file = open('SHA1-' + file_name + '.txt', 'w')
    sha1_file.write(hash_value)
    sha1_file.close()
    return None


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
    input_file = open(args.input, 'r').read()
    file_name = ntpath.basename(args.input).split('.')[0]
    md5_hash = hashlib.md5(input_file).hexdigest()
    sha1_hash = hashlib.sha1(input_file).hexdigest()
    print 'MD5: ' + md5_hash + '\n'
    print 'SHA1: ' + sha1_hash + '\n'
    _write_md5_file(file_name, md5_hash)
    _write_sha1_file(file_name, sha1_hash)

if __name__ == '__main__':
    main()
