# -*- coding: utf-8 -*-
import socket

# Search for the real IP address in the following order
HEADER_PRECEDENCE_ORDER = (
    'HTTP_X_FORWARDED_FOR',  # client, proxy1, proxy2
    'http-x-forwarded-for',
    'HTTP_CLIENT_IP',
    'http-client-ip',
    'HTTP_X_REAL_IP',
    'http-x-real-ip',
    'HTTP_X_FORWARDED',
    'http-x-forwarded',
    'HTTP_X_CLUSTER_CLIENT_IP',
    'http-x-cluster-client-ip',
    'HTTP_FORWARDED_FOR',
    'http-forwarded-for',
    'HTTP_FORWARDED',
    'http-forwarded',
    'HTTP_VIA',
    'http-via',
    'REMOTE_ADDR',
    'remote-addr'
)

# Private IP addresses
# http://www.ietf.org/rfc/rfc3330.txt (IPv4)
# http://www.ietf.org/rfc/rfc5156.txt (IPv6)
# Regex would be ideal here, but keeping it simple
# as this is configurable via settings.py
PRIVATE_IP_PREFIX = (
    '0.', '1.', '2.',  # externally non-routable
    '10.',  # class A private block
    '169.254.',  # link-local block
    '172.16.', '172.17.', '172.18.', '172.19.',
    '172.20.', '172.21.', '172.22.', '172.23.',
    '172.24.', '172.25.', '172.26.', '172.27.',
    '172.28.', '172.29.', '172.30.', '172.31.',  # class B private blocks
    '192.0.2.',  # reserved for documentation and example code
    '192.168.',  # class C private block
    '255.255.255.',  # IPv4 broadcast address
) + (  # the following addresses MUST be in lowercase)
    '2001:db8:',  # reserved for documentation and example code
    'fc00:',  # IPv6 private block
    'fe80:',  # link-local unicast
    'ff00:',  # IPv6 multicast
)

NON_PUBLIC_IP_PREFIX = PRIVATE_IP_PREFIX + (
    '127.',  # IPv4 loopback device
    '::1',  # IPv6 loopback device
)


def is_valid_ipv4(ip_str):
    """
    Check the validity of an IPv4 address
    """
    try:
        socket.inet_pton(socket.AF_INET, ip_str)
    except AttributeError:
        try:
            socket.inet_aton(ip_str)
        except socket.error:
            return False
        return ip_str.count('.') == 3
    except socket.error:
        return False
    return True


def is_valid_ipv6(ip_str):
    """
    Check the validity of an IPv6 address
    """
    try:
        socket.inet_pton(socket.AF_INET6, ip_str)
    except socket.error:
        return False
    return True


def is_valid_ip(ip_str):
    """
    Check the validity of an IP address
    """
    return is_valid_ipv4(ip_str) or is_valid_ipv6(ip_str)


def get_ip(headers, real_ip_only=False):
    """
    Returns client's best-matched ip-address, or None
    """
    best_matched_ip = None
    for key in HEADER_PRECEDENCE_ORDER:
        value = headers.get(key, '').strip().lower()
        if value != '':
            for ip_str in [ip.strip() for ip in value.split(',')]:
                if ip_str and is_valid_ip(ip_str):
                    if ip_str.startswith(NON_PUBLIC_IP_PREFIX):
                        if not real_ip_only:
                            best_matched_ip = ip_str
                    else:
                        return ip_str
    return best_matched_ip


def get_real_ip(headers):
    """
    Returns client's best-matched `real` ip-address, or None
    """
    return get_ip(headers, real_ip_only=True)
