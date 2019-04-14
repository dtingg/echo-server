"""
Port Services
Lookup services provided by a range of port numbers
"""

import sys
import socket


def port_services(low_bound, high_bound):
    """
    Lists the services provided by a given range of ports.
    :param low_bound: lower bound port number
    :param high_bound: higher bound port number
    :return: prints ports and services
    """

    if low_bound > high_bound:
        print(f"Error: The lower bound port {low_bound} is higher than the higher bound port {high_bound}.")
        return
    if low_bound < 0:
        print(f"The lower bound port {low_bound} is out of range. Please choose ports from 0-65535.")
        return
    if high_bound > 65535:
        print(f"The higher bound port {high_bound} is out of range. Please choose ports from 0-65535.")
        return

    for i in range(low_bound, high_bound + 1):
        try:
            service = socket.getservbyport(i)
            print(f"Port {i}: Service {service}")
        except OSError:
            continue


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage = '\nusage: python port_services.py lower_port higher_port\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    port_services(int(sys.argv[1]), int(sys.argv[2]))
