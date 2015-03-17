import datetime
import os
import sys

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
        return date.strftime("\nTime: %I:%M:%S %p")

    # Convert binary to date
    else:
        # Year, month, date
        Y, M, D = (int(binary[0:7], 2) + 1980), int(binary[7:11], 2), int(binary[11:17], 2) 
        date = datetime.date(Y, M, D)

        # Format: MMM DD, YYYY
        return date.strftime("\nDate: %b %d, %Y")

def main():

    # Handle command line arguments
    if len(sys.argv) == 4:

        module  = sys.argv[1] # -T or -D 
        format  = sys.argv[2] # -f or -h 
        input   = sys.argv[3] # filename or hex value

    else:

        # Print usage information
        print("\nmac_conversion -T|-D [-f filename | -h hex value]                        ")
        
        # -T
        print("-T Use time conversion module. Either -f or -h must be given.              ")

        # -D
        print("-D use date conversion module. Either -f or -h must be given.              ")
        
        # -f filename
        # Example usage: -f CSE469-input.txt
        print("-f filename                                                                ")
        print("      This specifies the path to a filename that includes a hex value      ")
        print("      of time or date. Note that the hex value should follow this          ")
        print("      notation: 0x1234. For the multiple hex values in either a file       ")
        print("      or a command line input, we consider only one hex value so the       ")
        print("      recursive mode for MAC conversion is optional.                       ")

        # -h hex value
        # Example usage: -h 0xF00
        print("-h hex value                                                               ")
        print("      This specifies the hex value for converting to either date or        ")
        print("      time value. Note that the hex value should follow this notation:     ")
        print("      0x1234. For the multiple hex values in either a file or a            ")
        print("      command line input, we consider only one hex value so the            ")
        print("      recursive mode for MAC conversion is optional.                       ")

        return

    print convert(module, format, input)

if __name__ == '__main__':
    main()

