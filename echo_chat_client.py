"""
Echo Chat Client
"""
import socket
import sys
import traceback


def client(log_buffer=sys.stderr):
    """
    Creates chat client socket.
    """

    server_address = ('localhost', 10000)

    # Instantiate a TCP socket with IPv4 addressing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)

    # Connect your socket to the server
    sock.connect(server_address)

    # Make socket nonblocking
    sock.setblocking(False)

    try:
        while True:
            try:
                msg = input("Enter a message: ")
                print('sending "{0}"'.format(msg), file=log_buffer)
                # Send your message to the server
                sock.sendall(msg.encode("utf-8"))
            except Exception:
                print("error 1")

            try:
                incoming = sock.recv(1024)

                if incoming:
                    print('received "{}"'.format(incoming.decode("utf8")), file=log_buffer)

            except BlockingIOError:
                continue

            except Exception as e:
                traceback.print_exc()
                sys.exit(1)

    except KeyboardInterrupt:
        sock.close()
        print('closing socket', file=log_buffer)


if __name__ == '__main__':
    client()
    sys.exit(0)
