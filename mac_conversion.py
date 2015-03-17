import datetime
import os
import sys
import argparse


def convert(module, format, input):

    # Check the format of the input
    if format == '-h':
        # Check for proper format of hexadecimal string
        if not ("0x" in input):
            return "\n'%s' is not in proper format." % (input)
        else:
            # Remove the "0x" from the hexadecimal string
            data = input[2:]
    else:
        # Check for existence of file
        if os.path.exists(input) and os.path.isfile(input):
            # Open and read the file
            with open(input, 'r') as fin:
                data = fin.read()
            # Check the data for correct format
            if len(data) and ("0x" in input):
                data = data[2:]
            else:
                return "\n'%s' is empty or improperly formatted." % (input)
        else:
            return "\n'%s' does not exist or is not a file." % (input)

    # Convert from hexadecimal to decimal and assume little endian ordering
    decimal = int(''.join([data[i:(i + 2)] for i in reversed(range(0, len(data), 2))]), 16)

    # Convert from decimal to 16-bit binary
    binary = "{0:016b}".format(decimal)

    # Convert binary to time
    if module == "-T":
        # Hour, minute, second
        H, M, S = int(binary[0:5], 2), int(binary[5:11], 2), int(binary[11:16], 2) * 2
        date = datetime.time(H, M, S)

        # Format: HH:MM:SS AM/PM
        return date.strftime("Time: %I:%M:%S %p")

    # Convert binary to date
    else:
        # Year, month, date
        Y, M, D = (int(binary[0:7], 2) + 1980), int(binary[7:11], 2), int(binary[11:17], 2)
        date = datetime.date(Y, M, D)

        # Format: MMM DD, YYYY
        return date.strftime("Date: %b %d, %Y")


def main():
    # Handle command line arguments
    parser = argparse.ArgumentParser(
        description='Performs MAC conversion based on input/output scheme.')
    parser.add_argument('-T', '--time', action='store_true',
                        help='Use time conversion module. \
                        Either -f or -h must be given.')
    parser.add_argument('-D', '--date', action='store_true',
                        help='Use date conversion module. \
                        Either -f or -h must be given.')
    parser.add_argument('-f', '--filename',
                        help='This specifies the path to a filename that \
                        includes a hex value of time or date. Note that \
                        the hex value should follow this notation: 0x1234. \
                        For the multiple hex values in either a file or a \
                        command line input, we consider only one \
                        hex value so the recursive mode for a MAC \
                        conversion is optional.')
    parser.add_argument('-hex', '--hex-value',
                        help='This specifies the hex value for converting \
                        to either date or time value. Note that \
                        the hex value should follow this notation: 0x1234. \
                        For the multiple hex values in either a file or a \
                        command line input, we consider only one \
                        hex value so the recursive mode for a MAC \
                        conversion is optional.')
    args = parser.parse_args()
    if not args.time and not args.date:
        parser.print_help()
        sys.exit(1)
    if not args.filename and not args.hex_value:
        parser.print_help()
        sys.exit(2)
    if args.time:
        module = '-T'
    elif args.date:
        module = '-D'
    if args.filename:
        format = '-f'
        input = args.filename
    elif args.hex_value:
        format = '-h'
        input = args.hex_value
    print convert(module, format, input)

if __name__ == '__main__':
    main()
