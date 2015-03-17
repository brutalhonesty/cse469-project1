import sys
import argparse


def _validate_input(args, parser):
    if not args.logical and not args.physical and not args.cluster:
        print 'Missing logical or physical or cluster'
        parser.print_help()
        sys.exit(1)
    if args.logical and not args.cluster_known and not args.physical_known:
        print 'Have logical, missing cluster_known or physical_known'
        # parser.print_help()
        sys.exit(1)
    if args.physical and not args.cluster_known and not args.logical_known:
        print 'Have physical, missing cluster_known or logical_known'
        parser.print_help()
        sys.exit(1)
    if args.cluster and not args.logical_known and not args.physical_known:
        print 'Have cluster, missing logical_known or physical_known'
        parser.print_help()
        sys.exit(1)


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
    parser.add_argument('-b', '--partition-start', type=int, help='This specifies the \
        physical address (sector number) of the start of the partition, and \
        defaults to 0 for ease in working with images of a single partition. \
        The offset vaulue will always translate into logical address 0.')
    parser.add_argument('-B', '--byte-address', type=int, help='Instead of returning \
        sector values for the conversion, this returns the byte address of \
        the calculated value, which is the number of sectors multiplied by \
        the number of bytes per sector.')
    parser.add_argument('-s', '--sector-size', type=int, help='When the -B option is used, \
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
    args = parser.parse_args()
    _validate_input(args, parser)

if __name__ == '__main__':
    main()
