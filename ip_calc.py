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


def get_ip_from_raw_address(raw_address):
    """
    Get ip address and a mask separated by "/" and
    Return ip address
    >>> get_ip_from_raw_address("192.168.1.15/24")
    '192.168.1.15'
    """
    ip_address, _ = raw_address.split("/")
    return ip_address


def get_network_address_from_raw_address(raw_address):
    """
    Get network address from raw address
    >>> get_network_address_from_raw_address("215.017.125.177/28")
    '215.17.125.176'
    """
    ip_address, _ = raw_address.split("/")

    # convert mask to decimal
    bin_mask = get_binary_mask_from_raw_address(raw_address)
    decimal_mask = '.'.join([str(bin_to_decimal_address(block)) for block in bin_mask.split('.')])

    network_adress_blocks = []
    for decimal_mask_block, ip_address_block in zip(decimal_mask.split('.'), ip_address.split('.')):
        network_adress_blocks.append(f"{int(decimal_mask_block) & int(ip_address_block)}")
    return '.'.join(network_adress_blocks)


def get_broadcast_address_from_raw_address(raw_address):
    """
    Get broadcast address from raw address
    >>> get_broadcast_address_from_raw_address('230.250.33.233/13')
    '230.255.255.255'
    >>> get_broadcast_address_from_raw_address("192.168.10.10/16")
    '192.168.255.255'
    >>> get_broadcast_address_from_raw_address('215.017.125.177/28')
    '215.17.125.191'
    >>> get_broadcast_address_from_raw_address('91.124.230.205/30')
    '91.124.230.207'
    """
    ip_address, _ = raw_address.split("/")
    bin_mask = get_binary_mask_from_raw_address(raw_address)
    inverted_bin_mask = invert_bin_address(bin_mask)
    decimal_mask = bin_to_decimal_address(inverted_bin_mask)

    broadcast_address_blocks = []
    for decimal_mask_block, ip_address_block in zip(decimal_mask.split('.'), ip_address.split('.')):
        broadcast_address_blocks.append(f"{int(decimal_mask_block) | int(ip_address_block)}")
    return '.'.join(broadcast_address_blocks)


def get_binary_mask_from_raw_address(raw_address):
    """
    Get binary mask from raw address
    >>> get_binary_mask_from_raw_address('91.124.230.205/30')
    '11111111.11111111.11111111.11111100'
    >>> get_binary_mask_from_raw_address("215.017.125.177/28")
    '11111111.11111111.11111111.11110000'
    >>> get_binary_mask_from_raw_address("215.017.125.177/24")
    '11111111.11111111.11111111.00000000'
    """
    _, mask = raw_address.split("/")
    mask = int(mask)
    mask_bin = ''
    for i in range(1, 32 + 1):
        if i <= mask:
            mask_bin += '1'
        else:
            mask_bin += '0'
        if not i % 8 and i != 32:
            mask_bin += '.'
    return mask_bin


def get_first_usable_ip_address_from_raw_address(raw_address):
    """
    Get first usable ip address from raw address
    >>> get_first_usable_ip_address_from_raw_address('91.124.230.205/30')
    '91.124.230.205'
    """
    network_address = get_network_address_from_raw_address(raw_address)
    octets = network_address.split('.')
    octets[-1] = f"{int(octets[-1]) + 1}"
    first_usable_ip_address = '.'.join(octets)
    return first_usable_ip_address


def get_penultimate_usable_ip_address_from_raw_address(raw_address):
    """
    Get penultimate usable ip address from raw address
    >>> get_penultimate_usable_ip_address_from_raw_address('230.250.33.233/13')
    '230.255.255.253'
    >>> get_penultimate_usable_ip_address_from_raw_address("192.168.10.10/16")
    '192.168.255.253'
    >>> get_penultimate_usable_ip_address_from_raw_address('91.124.230.205/30')
    '91.124.230.205'
    """
    broadcast_address = get_broadcast_address_from_raw_address(raw_address)
    octets = broadcast_address.split('.')
    octets[-1] = f"{int(octets[-1]) - 2}"
    last_usable_ip_address = '.'.join(octets)
    return last_usable_ip_address


def get_number_of_usable_hosts_from_raw_address(raw_address):
    """
    Get number of usable hosts from raw address
    >>> get_number_of_usable_hosts_from_raw_address('91.124.230.205/30')
    2
    """
    _, mask = raw_address.split("/")
    mask_length = int(mask)
    return 2 ** (32 - mask_length) - 2


def get_ip_class_from_raw_address(raw_address):
    """
    Get ip class from raw address
    >>> get_ip_class_from_raw_address('91.124.230.205/30')
    'A'
    """
    ip_address, _ = raw_address.split("/")
    first_octet = int(ip_address.split('.')[0])
    if 0 <= first_octet <= 126:
        return 'A'
    if 128 <= first_octet <= 191:
        return 'B'
    if 192 <= first_octet <= 223:
        return 'C'
    if 224 <= first_octet <= 239:
        return 'D'
    if 247 <= first_octet <= 255:
        return 'E'
    return None


def check_private_ip_address_from_raw_address(raw_address):
    """
    Check private ip address from raw address
    >>> check_private_ip_address_from_raw_address('91.124.230.205/30')
    False
    """
    ip_address, _ = raw_address.split("/")
    if ip_address.startswith('10') or ip_address.startswith('192.168'):
        return True
    if ip_address.startswith('172'):
        octets = ip_address.split('.')
        second_octet = int(octets[1])
        if 16 <= second_octet <= 31:
            return True
    return False



