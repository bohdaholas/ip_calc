"""
This module works with IP addresses
Github repository: https://github.com/bohdaholas/ip_calc.git
"""


def bin_to_decimal_address(bin_address):
    """
    Convert binary address to decimal
    >>> bin_to_decimal_address('11111111.11111111.11111111.11111111')
    '255.255.255.255'
    """
    bin_blocks = bin_address.split('.')
    decimal_blocks = []
    for bin_block in bin_blocks:
        bin_block = reversed(bin_block)
        decimal_block = 0
        for power, digit in enumerate(bin_block):
            if digit == '1':
                decimal_block += 2 ** power
        decimal_blocks.append(str(decimal_block))
    return '.'.join(decimal_blocks)


def invert_bin_address(address):
    """
    Replace ones with zeros and zeros with ones
    >>> invert_bin_address('11111111.11111000.00000000.00000000')
    '00000000.00000111.11111111.11111111'
    >>> invert_bin_address('11111111.11111111.11111111.11110000')
    '00000000.00000000.00000000.00001111'
    """
    inverted_address = address.translate(str.maketrans("01", "10"))
    return inverted_address



