"""
Echo client
"""

import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    """
    Creates client socket.
    :param msg: Message to be sent to server
    :param log_buffer:
    :return: Message received from server
    """

    server_address = ('localhost', 10000)

    # Instantiate a TCP socket with IPv4 addressing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)

    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)

    # Connect your socket to the server
    sock.connect(("127.0.0.1", 10000))

    # Accumulate the entire message received back from the server
    received_message = ''

    try:
        print('sending "{0}"'.format(msg), file=log_buffer)

        # Send your message to the server
        sock.sendall(msg.encode("utf-8"))

        while True:
            # Get message in 16 byte chunks
            buffer_size = 16

            # Set timeout for socket in case no data is received
            sock.settimeout(1)

            chunk = sock.recv(buffer_size)

            if not chunk:
                break

            # Print each chunk received
            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)

            # Accumulate the chunks to build the entire reply from the server
            received_message += chunk.decode("utf8")

            # Break loop if you have the end of the message
            if len(chunk) < buffer_size:
                break

    except socket.timeout:
        pass

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

    finally:
        # Close your client socket
        sock.close()
        print('closing socket', file=log_buffer)

        # Return the entire reply from the server as the return value of this function
        return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
