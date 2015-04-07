import sys
import argparse

args = None


def _validate_input(args, parser):
    '''
    Validates user input and prints the help menu if there are values missing.

    @type args: object
    @param args:
        The parsed arguments.
    @rtype: None
    @return: None
    '''
    if not args.logical and not args.physical and not args.cluster:
        parser.print_help()
        print 'Missing logical or physical or cluster.'
        sys.exit(1)
    if args.logical and not args.cluster_known and not args.physical_known:
        parser.print_help()
        print 'Have logical, missing cluster_known or physical_known.'
        sys.exit(1)
    if args.physical and not args.cluster_known and not args.logical_known:
        parser.print_help()
        print 'Have physical, missing cluster_known or logical_known.'
        sys.exit(1)
    if args.cluster and not args.logical_known and not args.physical_known:
        parser.print_help()
        print 'Have cluster, missing logical_known or physical_known.'
        sys.exit(1)


def _convert_cluster_to_physical(cluster_address):
    '''
    Converts a cluster address to a physical address.

    We use the arguments from the argparser and after globalizing them,
    we can use them in our calculations.

    @type cluster_address: int
    @param cluster_address:
        The cluster address to use in our calculations.
    @ rtype: int
    @ return: The physical address created.
    '''
    return args.partition_start + (cluster_address - 2) * args.cluster_size + args.reserved_sectors + (args.fat_tables * args.fat_length)


def _convert_logical_to_cluster(logical_address):
    '''
    Converts a logical address to a cluster address.

    We use the arguments from the argparser and after globalizing them,
    we can use them in our calculations.

    @type logical_address: int
    @param logical_address:
        The logical address to use in our calculations.
    @ rtype: int
    @ return: The cluster address created.
    '''
    return ((logical_address - args.reserved_sectors - (args.fat_tables * args.fat_length)) / args.cluster_size) + 2


def _calculate_logical_address(physical_address=None,
                               cluster_address=None, offset=0):
    '''
    Calculates the logical address value given either a physical address or cluster address.

    @type physical_address: int
    @param physical_address:
        The physical address to calculate with.
    @type cluster_address: int
    @param cluster_address:
        The cluster address to calculate with.
    @rtype: int
    @return: The logical address created.
    '''
    if cluster_address is None and physical_address is None:
        raise ValueError('Missing address to calculate logical address value.')
    if cluster_address is not None:
        address = _convert_cluster_to_physical(cluster_address)
    elif physical_address is not None:
        address = physical_address
    address = address - offset
    return address


def _calculate_physical_address(logical_address=None,
                                cluster_address=None, offset=0):
    '''
    Calculates the physical address value given either a logical address or cluster address.

    @type logical_address: int
    @param logical_address:
        The logical address to calculate with.
    @type cluster_address: int
    @param cluster_address:
        The cluster address to calculate with.
    @rtype: int
    @return: The physical address created.
    '''
    if cluster_address is None and logical_address is None:
        raise ValueError('Missing address to calculate physical address value.')
    if cluster_address is not None:
        address = _convert_cluster_to_physical(cluster_address)
    elif logical_address is not None:
        address = logical_address + offset
    else:
        address = None
    return address


def _calculate_cluster_address(physical_address=None,
                               logical_address=None, offset=0):
    '''
    Calculates the cluster address value given either a physical address or logical address.

    @type physical_address: int
    @param physical_address:
        The physical address to calculate with.
    @type logical_address: int
    @param logical_address:
        The logical address to calculate with.
    @rtype: int
    @return: The logical address created.
    '''
    if physical_address is None and logical_address is None:
        raise ValueError('Missing address to calculate cluster address value.')
    if logical_address is not None:
        address = _convert_logical_to_cluster(logical_address)
    elif physical_address is not None:
        address = physical_address - offset
    else:
        address = None
    return address


def main():
    parser = argparse.ArgumentParser(
        description='Convert between three different address types when an \
        address of a different type is given.')
    parser.add_argument('-L', '--logical', action='store_true', help='Calculate the logical address \
        from either the cluster address or the physical address. \
        Either -c or -p must be given.')
    parser.add_argument('-P', '--physical', action='store_true', help='Calculate the physical \
        address from either the cluster address or the logical address. \
        Either -c or -l must be given.')
    parser.add_argument('-C', '--cluster', action='store_true', help='Calculate the cluster address \
        from either the logical address or the physical address. \
        Either -l or -p must be given.')
    parser.add_argument('-b', '--partition-start', type=int, default=0, help='This specifies the \
        physical address (sector number) of the start of the partition, and \
        defaults to 0 for ease in working with images of a single partition. \
        The offset vaulue will always translate into logical address 0.')
    parser.add_argument('-B', '--byte-address', type=int, help='Instead of returning \
        sector values for the conversion, this returns the byte address of \
        the calculated value, which is the number of sectors multiplied by \
        the number of bytes per sector.')
    parser.add_argument('-s', '--sector-size', type=int, default=512, help='When the -B option is used, \
        this allows for a specification of bytes per sector other than the \
        default 512. Has no affect on output without -B.')
    parser.add_argument('-l', '--logical-known', type=int, help='This specifies the \
        known logical address for calculating either a cluster address or a \
        physical address. When used with the -L option, this simply \
        returns the value given for address.')
    parser.add_argument('-p', '--physical-known', type=int, help='This specifies the \
        known physical address for calculating either a cluster address or a \
        logical address. When used with the -P option, this simply \
        returns the value given for address.')
    parser.add_argument('-c', '--cluster-known', type=int, help='This specifies the \
        known cluster address for calculating either a logical address or a \
        physical address. When used with the -C option, this simply \
        returns the value given for address. Note that options -k, \
        -r, -t, and -f must be provided with this option.')
    parser.add_argument('-k', '--cluster-size', type=int, help='This specifies the \
        number of sector per cluster.')
    parser.add_argument('-r', '--reserved-sectors', type=int, help='This specifies the \
        number of reserved sectors in the partition.')
    parser.add_argument('-t', '--fat-tables', type=int, help='This specifies the \
        number of FAT tables, which is usually 2.')
    parser.add_argument('-f', '--fat-length', type=int, help='This specifies the \
        length of each FAT table in sectors.')
    # Globalize args so we can see it within our functions.
    global args
    args = parser.parse_args()
    # Validate user input.
    _validate_input(args, parser)
    if args.logical:
        print _calculate_logical_address(
            physical_address=args.physical_known,
            cluster_address=args.cluster_known,
            offset=args.partition_start)
        sys.exit(0)
    if args.physical:
        print _calculate_physical_address(
            logical_address=args.logical_known,
            cluster_address=args.cluster_known,
            offset=args.partition_start)
        sys.exit(0)
    if args.cluster:
        print _calculate_cluster_address(
            physical_address=args.physical_known,
            logical_address=logical_known,
            offset=args.partition_start)
        sys.exit(0)

if __name__ == '__main__':
    main()
